from invoke import task
from tasks.shared import is_local

@task
def ms(ctx):
    """deploy locally metrics-server api v0.3.6"""
    if is_local():
      ctx.run('kubectl apply -f metrics/metrics-server --recursive')

@task
def ksm(ctx):
    """deploy locally kube-state-metrics api v1.9.7"""
    if is_local():
      ctx.run('kubectl apply -f metrics/kube-state-metrics --recursive')

@task
def dash(ctx):
    """deploy locally kubernetes dashboard v2.0.0"""
    if is_local():
      ctx.run("kubectl apply -f dashboard/dashboard-namespace.yaml")
      ctx.run('kubectl apply -f dashboard/ --recursive')

@task
def istio(ctx):
    """deploy istio locally (current 1.6.5)"""

    INSTALL_ISTIO="""
    istioctl install --set profile=demo \
                     --set tag=1.6.5-distroless \
                     --set meshConfig.accessLogFile="/dev/stdout" \
                     --set meshConfig.accessLogEncoding="JSON" \
                     --set values.kiali.tag=v1.21.0
    """
    if is_local():
      ctx.run(INSTALL_ISTIO)

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

  #ctx.run("kubectl apply -f istio/samples/bookinfo/networking/bookinfo-gateway.yaml")
      # ctx.run("export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')")
      # ctx.run("export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')")
      # ctx.run("export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].port}')")
      # ctx.run("export TCP_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="tcp")].port}')")
      # ctx.run("export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT")
      # ctx.run("curl -s "http://${GATEWAY_URL}/productpage" | grep -o "<title>.*</title>"")

@task
def dnsconf(ctx):
    """configure dns"""
    if is_local():
      print('pending config dns')
    

@task
def localcert(ctx):
    ctx.run('')



  #   openssl req -x509 -out localhost.crt -keyout localhost.key \
  # -newkey rsa:2048 -nodes -sha256 \
  # -subj '/CN=localhost' -extensions EXT -config <( \
  #  printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
