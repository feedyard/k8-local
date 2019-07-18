from invoke import task

@task
def metrics(ctx):
    """deploy metrics apis locally"""
    ctx.run('kubectl apply -f metrics/ --recursive')

@task
def istio(ctx):
    """deploy istio locally"""
    ctx.run('kubectl apply -f istio/istio-namespace.yaml')
    ctx.run('kubectl apply -f istio/istio-init --recursive')
    ctx.run('kubectl apply -f istio/istio --recursive')

@task
def dashboard(ctx):
    """deploy kubernetes dashboard"""
    ctx.run('kubectl apply -f dashboard/kubernetes-dashboard-namespace.yaml')
    ctx.run('kubectl apply -f dashboard/kubernetes-dashboard-deployment.yaml')
    ctx.run('kubectl apply -f dashboard/kubernetes-dashboard-admin-user.yaml')
    ctx.run("kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')")


