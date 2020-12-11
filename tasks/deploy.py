from invoke import task
from tasks.shared import is_local

@task
def k8s(ctx):
    """start minikube with extra-config values and tunnel lb"""
    ctx.run('minikube start --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook --extra-config=scheduler.address=0.0.0.0 --extra-config=controller-manager.address=0.0.0.0')
    ctx.run('minikube tunnel &')


@task
def metrics(ctx):
    """deploy locally metrics-server api v0.4.1, kube-state-metrics api v1.9.7"""
    if is_local():
      ctx.run('kubectl apply -f metrics/metrics-server --recursive')
      ctx.run('kubectl apply -f metrics/kube-state-metrics --recursive')


@task
def istio(ctx):
    """deploy istio locally (current 1.8.1)"""

    INSTALL_ISTIO="""
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
  name: istiocontrolplane
spec:
  profile: default
  tag: 1.8.1-distroless
  meshConfig:
    accessLogFile: /dev/stdout
    accessLogEncoding: JSON
    enableTracing: true
  components:
    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
      k8s:
        resources:
          limits:
            cpu: 250m
            memory: 256Mi
          requests:
            cpu: 100m
            memory: 128Mi
"""
    if is_local():
      ctx.run("istioctl operator init && sleep 8")
      ctx.run("kubectl apply -f tasks/namespaces.yaml")
      ctx.run(f"echo '{INSTALL_ISTIO}' | kubectl apply -f - ")
      

@task
def istiotools(ctx):
    """deploy prometheus, grafana, jaeger, kiali to local kubernetes"""
    if is_local():
      ctx.run("kubectl apply --recursive -f istiotools/")
      ctx.run("helm install --set cr.create=true --set cr.namespace=istio-system --set spec.auth.strategy=anonymous --namespace kiali-operator --repo https://kiali.org/helm-charts kiali-operator kiali-operator")


@task
def dash(ctx):
    """deploy locally kubernetes dashboard v2.0.5"""
    if is_local():
      ctx.run("kubectl apply -f dashboard/00_dashboard-namespace.yaml")
      ctx.run('kubectl apply -f dashboard/ --recursive')

    
@task
def localdomain(ctx, ns, domain):
    """Create local dev namespcae with istio config and use mkcert to generate a valid cert for a local CA"""
    CREATE_NAMESPACE="""
apiVersion: v1
kind: Namespace
metadata:
  name: {}
  labels:
    istio-injection: enabled
"""
    devnamespace=CREATE_NAMESPACE.format(ns)
    
    ctx.run(f"echo '{devnamespace}' | kubectl apply -f - ")
    ctx.run(f"mkcert -cert-file {domain}.crt -key-file {domain}.key {domain} \"*.{domain}\"")
    ctx.run(f"kubectl create -n istio-system secret tls {domain}-credential --key={domain}.key --cert={domain}.crt")


@task
def all(ctx):
    """Run after minikube start to deploy all k8s services"""
    if is_local():
      metrics(ctx)
      istio(ctx)
      istiotools(ctx)
      dash(ctx)

@task(optional=['tls'])
def httpbin(ctx, tls=None):
    """httpbin ingress examples"""
    if is_local():
      ctx.run("kubectl apply -f httpbin/deploy/httpbin-namespace.yaml")
      ctx.run("kubectl apply -f httpbin/deploy --recursive")
      if tls:
        print('using tls')
        ctx.run('mkcert -cert-file httpbin.localhost.crt -key-file httpbin.localhost.key httpbin.localhost localhost 127.0.0.1 ::1')
        ctx.run('kubectl create -n istio-system secret tls httpbin-credential --key=httpbin.localhost.key --cert=httpbin.localhost.crt')
        ctx.run("kubectl apply -f httpbin/tls --recursive")
      else:
        ctx.run("kubectl apply -f httpbin/simple --recursive")

# @task
# def bookinfo(ctx):
#     if is_local():
#       ctx.run("kubectl apply -f bookinfo/bookinfo-namespace.yaml")
#       ctx.run("kubectl apply -f bookinfo --recursive")

