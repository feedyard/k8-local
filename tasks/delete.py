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
      ctx.run("istioctl manifest generate --set profile=default --set telemetry.enabled=true | kubectl delete -f -")

@task
def dash(ctx):
    """delete kubernetes dashboard"""
    if is_local():
      ctx.run('kubectl delete -f dashboard/ --recursive')

@task
def buildkite(ctx):
    """delete standard buildkite agent"""
    if is_local():
      ctx.run("kubectl delete secret buildkite-secret --ignore-not-found")
      ctx.run("kubectl delete --filename buildkite --recursive")

@task
def bookinfo(ctx):
    if is_local():
      ctx.run("istio/samples/bookinfo/platform/kube/cleanup.sh")