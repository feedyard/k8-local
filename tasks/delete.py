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

    INSTALL_DELETE="""
    istioctl manifest generate  --set profile=demo \
                                --set tag=1.6.5-distroless \
                                --set values.kiali.tag=v1.21.0 | kubectl delete -f -
    """
    if is_local():
      ctx.run(INSTALL_DELETE)

@task
def dash(ctx):
    """delete kubernetes dashboard"""
    if is_local():
      ctx.run('kubectl delete -f dashboard/ --recursive')

@task
def httpbin(ctx):
    """httpbin ingress examples"""
    if is_local():
      ctx.run("kubectl delete ns httpbin")
      ctx.run("kubectl delete secret -n istio-system httpbin-credential")

@task
def bookinfo(ctx):
    if is_local():
      ctx.run("kubectl delete -f bookinfo --recursive")
