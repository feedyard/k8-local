from invoke import task
from tasks.shared import is_local

@task
def metrics(ctx):
    """delete metrics apis"""
    if is_local():
      ctx.run('kubectl delete -f metrics/ --recursive')

@task
def istio(ctx):
    """delete istio"""
    if is_local():
      ctx.run("istioctl manifest generate | kubectl delete -f -")
      ctx.run("kubectl delete ns istio-system --grace-period=0 --force")

@task
def dash(ctx):
    """delete kubernetes dashboard"""
    if is_local():
      ctx.run('kubectl delete -f dashboard/ --recursive')

@task
def httpbin(ctx):
    """httpbin ingress examples"""
    if is_local():
      ctx.run("kubectl delete ns httpbin --grace-period=0 --force")
      ctx.run("kubectl delete secret -n istio-system httpbin-credential")

@task
def bookinfo(ctx):
    if is_local():
      ctx.run("kubectl delete -f bookinfo --recursive")
