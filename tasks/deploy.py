from invoke import task
from tasks.shared import is_local

@task
def metrics(ctx):
    """local metrics-server v0.3.6, kube-state-metrics api v1.9.3"""
    if is_local():
      ctx.run('kubectl apply -f metrics/ --recursive')

@task
def dash(ctx):
    """local kubernetes dashboard v2.0.0-rc2"""
    if is_local():
      ctx.run("kubectl apply -f dashboard/dashboard-namespace.yaml")
      ctx.run('kubectl apply -f dashboard/ --recursive')

@task
def istio(ctx):
    """deploy istio locally v1.4.3"""
    if is_local():
      ctx.run("kubectl apply --filename istio/install/kubernetes/namespace.yamlm")
      ctx.run("kubectl apply --filename templates/kiali-secrets.yaml")
      ctx.run("istioctl manifest apply --set profile=default --set values.tracing.enabled=true --set telemetry.enabled=true")
      ctx.run("istioctl manifest apply --set values.kiali.enabled=true --set values.kiali.dashboard.jaegerURL=http://jaeger-query:16686 --set values.kiali.dashboard.grafanaURL=http://grafana:3000")

def buildkite(ctx):
    """deploy standard buildkite agent"""
    if is_local():
      ctx.run("kubectl delete secret buildkite-secret --ignore-not-found")
      ctx.run("kubectl create secret generic buildkite-secret --from-literal=buildkite-agent-token=$BUILDKITE_AGENT_TOKEN")
      ctx.run("kubectl apply --filename buildkite --recursive")

# @task
# def bookinfo(ctx):
#     """Deploy istio bookinfo example. See doc/examples.md for description"""
#     if is_local():
#       ctx.run("kubectl apply -f bookinfo/namespace.yaml")
#       --set namespace="local"
#       ctx.run("kubectl label namespace default istio-injection=enabled --overwrite")
#       ctx.run("kubectl apply -f istio/samples/bookinfo/platform/kube/bookinfo.yaml")
#       ctx.run("kubectl apply -f istio/samples/bookinfo/networking/bookinfo-gateway.yaml")
#       ctx.run("export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')")
#       ctx.run("export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name==\"http2\")].port}')")
#       ctx.run("export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name==\"https\")].port}')")

@task
def localcert(ctx):
    ctx.run('')

@task
def metallb(ctx):
    ctx.run("kubectl apply -f metallb/namespace.yaml")
    ctx.run("kubectl apply -f metallb/metallb-rbac.yaml")
    ctx.run("kubectl apply -f metallb/metallb-deploy.yaml")
    ctx.run("kubectl apply -f metallb/metallb-configmap.yaml")

