from invoke import task
import time

@task(optional=['edge'])
def init(ctx, edge=False):

    if edge:
        print('includes edge options')

    print('initial config')
    ctx.run('kubectl apply -f metrics-server-1.8+/')
    ctx.run('kubectl apply -f monitoring/eventrouter/')
    ctx.run('kubectl apply -f dashboard/')
    ctx.run("kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')")
    ctx.run('cat README.md')


@task(optional=['edge'])
def monitor(ctx, edge=False):

    if edge:
        print('no edge options for monitoring yet')

    print('deploy monitoring tools')
    #ctx.run('kubectl apply -f monitoring/monitoring-namespace.yaml')
    ctx.run('kubectl apply -f monitoring/heapster/influxdb/')
    time.sleep(20)
    ctx.run('kubectl apply -f monitoring/heapster/heapster/')
    time.sleep(20)
    ctx.run('kubectl apply -f monitoring/heapster/grafana/')
    ctx.run('kubectl describe svc grafana -n monitoring')
    ctx.run('kubectl apply -f monitoring/elasticsearch/')
    time.sleep(90)
    ctx.run('kubectl apply -f monitoring/fluentd/')
    time.sleep(60)
    ctx.run('kubectl apply -f monitoring/kibana/')
    ctx.run('kubectl describe svc kibana -n monitoring')

@task(optional=['edge'])
def ingress(ctx, edge=False):

    if edge:
        print('no edge options for ingress yet')

    print('deploy traefik ingress controller')
    ctx.run('kubectl apply -f ingress/')
    ctx.run('kubectl describe svc -n kube-system traefik-ingress-service')

@task
def test(ctx):
    print('test')
