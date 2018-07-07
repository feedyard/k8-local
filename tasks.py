from invoke import task

@task
def init(ctx):
    ctx.run('bash ./update_dns.sh | kubectl apply -f -')
    ctx.run('kubectl delete --namespace=kube-system deployment kube-dns')
    ctx.run('bash init.sh')

@task
def test(ctx):
    print('test')