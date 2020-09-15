from invoke import task
from tasks.shared import is_local

@task
def ms(ctx):
    """deploy locally metrics-server api v0.3.7"""
    if is_local():
      ctx.run('kubectl apply -f metrics/metrics-server --recursive')

@task
def ksm(ctx):
    """deploy locally kube-state-metrics api v1.9.7"""
    if is_local():
      ctx.run('kubectl apply -f metrics/kube-state-metrics --recursive')

@task
def dash(ctx):
    """deploy locally kubernetes dashboard v2.0.3"""
    if is_local():
      ctx.run("kubectl apply -f dashboard/dashboard-namespace.yaml")
      ctx.run('kubectl apply -f dashboard/ --recursive')

@task
def istio(ctx):
    """deploy istio locally (current 1.7.0)"""

    INSTALL_ISTIO="""
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
  name: istiocontrolplane
spec:
  profile: default
  tag: 1.7.0-distroless
  meshConfig.accessLogFile: "/dev/stdout"
  meshConfig.accessLogEncoding: "JSON"
  components:
    ingressGateways:
    - enabled: true
      k8s:
        resources:
          limits:
            cpu: 250m
            memory: 256Mi
          requests:
            cpu: 100m
            memory: 128Mi
  values:
    kiali:
      createDemoSecret: true
      tag: v1.23.0
"""
    if is_local():
      # ctx.run("istioctl operator init")
      # ctx.run("kubectl create ns istio-system")
      ctx.run(f"echo '{INSTALL_ISTIO}' | kubectl apply -f - ")

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

@task
def bookinfo(ctx):
    if is_local():
      ctx.run("kubectl apply -f bookinfo/bookinfo-namespace.yaml")
      ctx.run("kubectl apply -f bookinfo --recursive")

@task
def dnsconf(ctx):
    """configure dns"""
    if is_local():
      print('pending config dns')
    
@task
def localdomain(ctx, domain):
    """Use mkcert to generate a valid cert for a local CA"""
    ctx.run(f"mkcert -cert-file {domain}.localhost.crt -key-file {domain}.localhost.key {domain}.localhost \"*.{domain}.localhost\"")
    ctx.run(f"kubectl create -n istio-system secret tls {domain}-credential --key={domain}.localhost.key --cert={domain}.localhost.crt")



kubectl apply -f - <<EOF
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
  name: istiocontrolplane
spec:
  profile: default
  tag: 1.7.0-distroless
  meshConfig.accessLogFile: "/dev/stdout"
  meshConfig.accessLogEncoding: "JSON"
  components:
    ingressGateways:
    - enabled: true
      k8s:
        resources:
          limits:
            cpu: 250m
            memory: 256Mi
          requests:
            cpu: 100m
            memory: 128Mi
  values:
    kiali:
      createDemoSecret: true
      tag: v1.23.0
EOF
