from invoke import task

@task
def ms(ctx):
    """deploy metrics-server api"""
    ctx.run('kubectl apply -f metrics/metrics-server --recursive')

@task
def ksm(ctx):
    """deploy kube-state-metrics api"""
    ctx.run('kubectl apply -f metrics/kube-state-metrics --recursive')

@task
def db(ctx):
    """deploy kubernetes 2.0 dashboard"""
    ctx.run('kubectl apply -f dashboard/ --recursive')

@task
def istio(ctx):
    """deploy istio locally"""
    ctx.run('kubectl apply -f istio/istio-namespace.yaml')
    ctx.run('kubectl apply -f istio/istio-init --recursive')
    ctx.run('kubectl apply -f istio/istio --recursive')
