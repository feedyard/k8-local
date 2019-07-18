from invoke import task
from subprocess import run, PIPE


ISTIO_VERSION='1.1.1'

METRICS_SERVER_VERSION='0.3.1'
METRICS_SERVER='metrics-server-' + METRICS_SERVER_VERSION
KUBE_STATE_METRICS_VERSION='1.5.0'
DASHBOARD_VERSION='v1.10.1'


@task(optional=['rm'])
def metrics(ctx, rm=False):
    cmd = 'delete' if rm  else 'apply'
    ctx.run('kubectl {} -f metrics/ --recursive'.format(cmd))
    ctx.run('kubectl apply -f dashboard/')

@task
def dash(ctx):
    p = run("kubectl -n kube-system describe secret kubernetes-dashboard-head-token | awk '{for(i=1;i<=NF;i++) {if($i~\"token:\") {print $(i+1)}}}'", shell=True, stdout=PIPE, encoding='ascii')
    cmd = "echo \"{}\" | pbcopy".format(p.stdout)
    ctx.run(cmd)
    print('dashboard token copied to clipboard')
    ctx.run('open http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard-head:/proxy/')
    ctx.run('kubectl proxy &')

@task
def istio(ctx):
    ctx.run('kubectl apply -f charts/istio-' + ISTIO_VERSION + '/install/kubernetes/namespace.yaml ')
    ctx.run('kubectl apply -f istio-deploy/istio-init --recursive')
    ctx.run('kubectl apply -f istio-deploy/istio --recursive')
    ctx.run('kubectl apply -f istio-deploy/standard-istio-non_mtls_policy.yaml')


@task(optional=['logzio'])
def efk(ctx, logzio=False):
    if logzio:
        print('deploy logzio based logging')
        ctx.run('kubectl apply -f efk/logzio/')
    else:
        print('deploy local EfK logging')
        ctx.run('kubectl apply -f efk/elasticsearch/')
        time.sleep(30)
        ctx.run('kubectl apply -f efk/fluentd/')
        time.sleep(20)
        ctx.run('kubectl apply -f efk/kibana/')
        ctx.run('kubectl describe svc kibana -n kube-system')

@task
def generatemetricsserver(ctx):
    CMD = "helm template charts/metrics-server-" + METRICS_SERVER_VERSION + "/metrics-server --name metrics-server --namespace kube-system " \
          "--set rbac.create=true " \
          "--set serviceAccount.create=true " \
          "--set serviceAccount.name=metrics-server " \
          "--set apiService.create=true " \
          "--set image.tag=" + METRICS_SERVER_VERSION + " " \
          "--set args={--logtostderr\,--metric-resolution=10s} " \
          "--output-dir metrics-server"
    ctx.run(CMD)

@task
def generateistio(ctx):
    CMD = "helm template versions/istio-" + ISTIO_VERSION + "/install/kubernetes/helm/istio-init --name istio-init --namespace istio-system " \
          "--set certmanager.enabled=true " \
          "--output-dir istio-deploy"
    ctx.run(CMD)

    CMD = "helm template versions/istio-" + ISTIO_VERSION + "/install/kubernetes/helm/istio --name istio --namespace istio-system " \
          "--set sidecarInjectorWebhook.enabled=true " \
          "--set certmanager.enabled=true " \
          "--set gateways.istio-ingressgateway.enabled=true " \
          "--set gateways.istio-egressgateway.enabled=true " \
          "--set gateways.istio-ingressgateway.type=NodePort " \
          "--set gateways.istio-egressgateway.type=NodePort " \
          "--set gateways.istio-ingressgateway.sds.enabled=true " \
          "--set grafana.enabled=true " \
          "--set tracing.enabled=true " \
          "--set kiali.enabled=true " \
          "--set kiali.createDemoSecret=true " \
          "--set \"kiali.dashboard.jaegerURL=http://$(kubectl get svc tracing -n istio-system -o jsonpath='{.spec.clusterIP}'):80\" " \
          "--set \"kiali.dashboard.grafanaURL=http://$(kubectl get svc grafana -n istio-system -o jsonpath='{.spec.clusterIP}'):3000\" " \
          "--set prometheus.enabled=true " \
          "--set global.refreshInterval=2s " \
          "--set global.disablePolicyChecks=false " \
          "--set global.proxy.accessLogEncoding=JSON " \
          "--set global.imagePullPolicy=IfNotPresent " \
          "--set global.controlPlaneSecurityEnabled=true	 " \
          "--set global.policyCheckFailOpen=false " \
          "--set global.enableTracing=true " \
          "--set global.useMCP=true " \
          "--set global.sds.enabled=true " \
          "--set global.sds.useNormalJwt=true " \
          "--output-dir istio-deploy"
    ctx.run(CMD)


@task
def update(ctx, service):
    # update versions to current

    if service == 'metrics-server':
        ctx.run('rm -rf versions/{} && rm -rf metrics/metrics-server/1.8+'.format(METRICS_SERVER))
        ctx.run('curl -L https://github.com/kubernetes-incubator/metrics-server/archive/v{}.zip -o {}'.format(METRICS_SERVER_VERSION, METRICS_SERVER + '.zip'))
        ctx.run('unzip {} -d versions/ && mv versions/{}/deploy/1.8+ metrics/metrics-server/'.format(METRICS_SERVER + '.zip', METRICS_SERVER))
        ctx.run('rm {}'.format(METRICS_SERVER + '.zip'))

    if service == 'kube-state-metrics':
        ctx.run('rm -rf metrics/kube-state-metrics/kubernetes && rm -rf versions/kube-state-metrics-{}'.format(KUBE_STATE_METRICS_VERSION))
        ctx.run('curl -L https://github.com/kubernetes/kube-state-metrics/archive/v{0}.zip -o {1}'.format(KUBE_STATE_METRICS_VERSION, 'ksm' + KUBE_STATE_METRICS_VERSION))
        ctx.run('unzip {} -d versions/ && mv versions/kube-state-metrics-{}/kubernetes metrics/kube-state-metrics/ '.format('ksm' + KUBE_STATE_METRICS_VERSION, KUBE_STATE_METRICS_VERSION))
        ctx.run('rm -rf rm {}'.format('ksm' + KUBE_STATE_METRICS_VERSION))

    if service == 'eventrouter':
        K8_EVENT_ROUTER="eventrouter.yaml"
        K8_EVENT_ROUTER_PATH="https://raw.githubusercontent.com/heptiolabs/eventrouter/master/yaml/" + K8_EVENT_ROUTER
        ctx.run('curl -L {0} -o versions/eventrouter/{1} && cp versions/eventrouter/{1} metrics/eventrouter/{1}'.format(K8_EVENT_ROUTER_PATH,K8_EVENT_ROUTER))

    if service == 'dashboard':
        DASHBOARD="kubernetes-dashboard-head.yaml"
        DASHBOARD_PATH="https://raw.githubusercontent.com/kubernetes/dashboard/master/aio/deploy/recommended/" + DASHBOARD
        #DASHBOARD_PATH="https://raw.githubusercontent.com/kubernetes/dashboard/" + DASHBOARD_VERSION + "/src/deploy/recommended/" + DASHBOARD
        ctx.run('curl -L {0} -o {1} && mv {1} dashboard/{1}'.format(DASHBOARD_PATH, DASHBOARD))

    if service == 'istio':
        ctx.run('curl -L https://git.io/getLatestIstio | sh -')

@task
def cheat(ctx):
    ctx.run('cat cheat_sheet.md')
