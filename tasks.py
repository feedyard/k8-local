from invoke import task
from subprocess import run, PIPE

@task
def init(ctx):
    print('baseline config')
    ctx.run('kubectl apply -f metrics-server-1.8+/')
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
    ctx.run('kubectl apply -f istio-1.0.6/install/kubernetes/namespace.yaml ')
    ctx.run('kubectl apply -f istio-deploy/istio/templates --recursive')
    ctx.run('kubectl apply -f istio-deploy/istio/charts --recursive')

@task
def kiali(ctx):
    CMD = "helm template istio-1.0.6/install/kubernetes/helm/istio --name istio --namespace istio-system " \
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
def generateistio(ctx):
    CMD = "helm template istio-1.0.6/install/kubernetes/helm/istio --name istio --namespace istio-system " \
          "--set grafana.enabled=true " \
          "--set tracing.enabled=true " \
          "--set prometheus.enabled=true " \
          "--set pilot.sidecar=true " \
          "--set galley.enabled=true " \
          "--set mixer.enabled=true " \
          "--set sidecarInjectorWebhook.enabled=true " \
          "--set security.enabled=true " \
          "--set ingress.enabled=true " \
          "--set gateways.istio-ingressgateway.type=NodePort " \
          "--set gateways.istio-egressgateway.type=NodePort " \
          "--set gateways.istio-ingressgateway.enabled=true " \
          "--set gateways.istio-egressgateway.enabled=true " \
          "--set global.proxy.envoyStatsd.enabled=false " \
          "--output-dir istio-deploy"
    ctx.run(CMD)


@task
def update(ctx):
    # update versions to current
    K8_EVENT_ROUTER="eventrouter.yaml"
    K8_EVENT_ROUTER_PATH="https://raw.githubusercontent.com/heptiolabs/eventrouter/master/yaml/" + K8_EVENT_ROUTER
    ctx.run('curl -L {0} -o {1} && mv {1} monitoring/eventrouter/{1}'.format(K8_EVENT_ROUTER_PATH,K8_EVENT_ROUTER))

    DASHBOARD="kubernetes-dashboard.yaml"
    DASHBOARD_PATH="https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/" + DASHBOARD
    ctx.run('curl -L {0} -o {1} && mv {1} dashboard/{1}'.format(DASHBOARD_PATH, DASHBOARD))

    ctx.run('curl -L https://git.io/getLatestIstio | sh -')

@task
def cheat(ctx):
    ctx.run('cat cheat_sheet.md')