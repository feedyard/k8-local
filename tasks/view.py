from invoke import task
from subprocess import run, PIPE
import os

@task
def istio(ctx, window=False):
    """proxy istio UI and open shortcuts window"""
    prometheus = "kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=prometheus -o jsonpath='{.items[0].metadata.name}') 9090:9090 &"
    grafana = "kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=grafana -o jsonpath='{.items[0].metadata.name}') 3000:3000 &"
    jaeger = "kubectl port-forward -n istio-system $(kubectl get pod -n istio-system -l app=jaeger -o jsonpath='{.items[0].metadata.name}') 16686:16686 &"
    kiali = "kubectl -n istio-system port-forward $(kubectl -n istio-system get pod -l app=kiali -o jsonpath='{.items[0].metadata.name}') 20001:20001 &"

    os.system(prometheus)
    os.system(grafana)
    os.system(jaeger)
    os.system(kiali)

    if window:
        ctx.run('open dashboard/istio-ui.html')

@task
def dash(ctx):
    """proxy kubernetes web ui and open window"""
    p = run("kubectl -n kube-system describe secret kubernetes-dashboard-head-token | awk '{for(i=1;i<=NF;i++) {if($i~\"token:\") {print $(i+1)}}}'", shell=True, stdout=PIPE, encoding='ascii')
    cmd = "echo \"{}\" | pbcopy".format(p.stdout)
    ctx.run(cmd)
    print('dashboard token copied to clipboard')
    dashboard = 'kubectl proxy &'
    os.system(dashboard)
    ctx.run("open http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard-head:/proxy/")

@task
def off(ctx):
    """kill all port-forwarders"""
    ctx.run('pkill kubectl')