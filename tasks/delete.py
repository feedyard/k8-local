from invoke import task

@task
def metrics(ctx):
    """delete metrics apis locally"""
    ctx.run('kubectl delete -f metrics/ --recursive')

@task
def istio(ctx):
    """delete istio locally"""
    ctx.run('kubectl delete -f istio/istio --recursive')
    ctx.run('kubectl delete -f istio/istio-init --recursive')
    ctx.run('kubectl delete -f istio/istio-namespace.yaml')

@task
def dashboard(ctx):
    """deploy kubernetes dashboard"""
    ctx.run('kubectl delete -f dashboard/')
