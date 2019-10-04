from invoke import task


ISTIO_VERSION = '1.3.1'

@task
def istio(ctx):
    """render istio deployment for cluster"""
    CMD = "helm template versions/istio-" + ISTIO_VERSION + "/install/kubernetes/helm/istio-init --name istio-init --namespace istio-system " \
          "--output-dir istio"
    ctx.run(CMD)

    CMD = "helm template versions/istio-" + ISTIO_VERSION + "/install/kubernetes/helm/istio --name istio --namespace istio-system " \
          "--values versions/istio-" + ISTIO_VERSION + "/install/kubernetes/helm/istio/values-istio-demo-auth.yaml " \
          "--output-dir istio"
    ctx.run(CMD)

          # "--set grafana.enabled=true " \
          # "--set kiali.enabled=true " \
          # "--set \"kiali.dashboard.jaegerURL=http://jaeger-query:16686\"" \
          # "--set \"kiali.dashboard.grafanaURL=http://grafana:3000\"" \
