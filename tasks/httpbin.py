from invoke import task
from tasks.shared import is_local


@task(optional=['tls'])
def deploy(ctx, tls=None):
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
def rm(ctx):
    """httpbin ingress examples"""
    if is_local():
      ctx.run("kubectl delete ns httpbin --grace-period=0 --force")
      ctx.run("kubectl delete secret -n istio-system httpbin-credential")
