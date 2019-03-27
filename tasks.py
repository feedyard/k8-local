from invoke import task
from subprocess import run, PIPE

METRICS_SERVER_CHART_VERSION='2.5.0'
METRICS_SERVER_VERSION='v0.3.1'

DASHBOARD_VERSION='v1.10.1'

ISTIO_VERSION='1.0.6'

@task
def init(ctx):
    print('baseline config')
    ctx.run('kubectl apply -f metrics-server/ --recursive')
    ctx.run('kubectl apply -f eventrouter/')
    ctx.run('kubectl apply -f dashboard/')
    p = run("kubectl -n kube-system describe secret kubernetes-dashboard-token | awk '{for(i=1;i<=NF;i++) {if($i~\"token:\") {print $(i+1)}}}'", shell=True, stdout=PIPE, encoding='ascii')
    cmd = "echo \"{}\" | pbcopy".format(p.stdout)
    ctx.run(cmd)
    ctx.run('cat dashboard/usage.md')

@task
def dash(ctx):
    p = run("kubectl -n kube-system describe secret kubernetes-dashboard-token | awk '{for(i=1;i<=NF;i++) {if($i~\"token:\") {print $(i+1)}}}'", shell=True, stdout=PIPE, encoding='ascii')
    cmd = "echo \"{}\" | pbcopy".format(p.stdout)
    ctx.run(cmd)
    print('dashboard token copied to clipboard')
    ctx.run('open http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/')
    ctx.run('kubectl proxy &')

@task
def istio(ctx):
    ctx.run('kubectl apply -f charts/istio-' + ISTIO_VERSION + '/install/kubernetes/namespace.yaml ')
    ctx.run('kubectl apply -f istio-deploy/istio/templates --recursive')
    ctx.run('kubectl apply -f istio-deploy/istio/charts --recursive')
    ctx.run('kubectl apply -f istio-deploy/standard-istio-non_mtls_policy.yaml')

@task
def kiali(ctx):
    CMD = "helm template charts/istio-" + ISTIO_VERSION + "/install/kubernetes/helm/istio --name istio --namespace istio-system " \
          "--set kiali.enabled=true " \
          "--set \"kiali.dashboard.jaegerURL=http://$(kubectl get svc tracing -n istio-system -o jsonpath='{.spec.clusterIP}'):80\" " \
          "--set \"kiali.dashboard.grafanaURL=http://$(kubectl get svc grafana -n istio-system -o jsonpath='{.spec.clusterIP}'):3000\" " \
          "--output-dir istio-deploy-kiali"
    ctx.run(CMD)
    ctx.run('kubectl apply -f istio-deploy-kiali/kiali-secret.yaml')
    ctx.run('kubectl apply -f istio-deploy-kiali/istio/charts/kiali --recursive')

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
    CMD = "helm template charts/istio-" + ISTIO_VERSION + "/install/kubernetes/helm/istio --name istio --namespace istio-system " \
          "--set security.enabled=true " \
          "--set ingress.enabled=true " \
          "--set gateways.istio-ingressgateway.enabled=true " \
          "--set gateways.istio-egressgateway.enabled=true " \
          "--set gateways.istio-ingressgateway.type=NodePort " \
          "--set gateways.istio-egressgateway.type=NodePort " \
          "--set pilot.sidecar=true " \
          "--set galley.enabled=true " \
          "--set mixer.enabled=true " \
          "--set grafana.enabled=true " \
          "--set tracing.enabled=true " \
          "--set kiali.enabled=true " \
          "--set prometheus.enabled=true " \
          "--set sidecarInjectorWebhook.enabled=true " \
          "--set global.refreshInterval=3s " \
          "--set global.proxy.envoyStatsd.enabled=false " \
          "--set global.disablePolicyChecks=false " \
          "--set global.proxy.envoyStatsd.enabled=false " \
          "--output-dir istio-deploy"
    ctx.run(CMD)


@task
def update(ctx, service):
    # update versions to current

    if service == 'metrics-server':
        ctx.run('helm fetch stable/metrics-server -d charts --untar --untardir metrics-server-{} --version={}'.format(METRICS_SERVER_VERSION, METRICS_SERVER_CHART_VERSION))
        print('add namespace directives to metrics-server templates')

    if service == 'eventrouter':
        K8_EVENT_ROUTER="eventrouter.yaml"
        K8_EVENT_ROUTER_PATH="https://raw.githubusercontent.com/heptiolabs/eventrouter/master/yaml/" + K8_EVENT_ROUTER
        ctx.run('curl -L {0} -o {1} && mv {1} eventrouter/{1}'.format(K8_EVENT_ROUTER_PATH,K8_EVENT_ROUTER))

    if service == 'dashboard':
        DASHBOARD="kubernetes-dashboard.yaml"
        DASHBOARD_PATH="https://raw.githubusercontent.com/kubernetes/dashboard/" + DASHBOARD_VERSION + "v1.10.1/src/deploy/recommended/" + DASHBOARD
        ctx.run('curl -L {0} -o {1} && mv {1} dashboard/{1}'.format(DASHBOARD_PATH, DASHBOARD))

    if service == 'istio':
        ctx.run('curl -L https://git.io/getLatestIstio | sh -')

@task
def cheat(ctx):
    ctx.run('cat cheat_sheet.md')
