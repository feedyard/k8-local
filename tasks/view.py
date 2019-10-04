from invoke import task
from subprocess import run, PIPE
import os

@task
def db(ctx):
    """proxy kubernetes web ui and open window"""
    p = run("kubectl -n kubernetes-dashboard describe secret admin-user | awk '{for(i=1;i<=NF;i++) {if($i~/token:/) print $(i+1)}}'", shell=True, stdout=PIPE, encoding='ascii')
    cmd = "echo \"{}\" | pbcopy".format(p.stdout)
    ctx.run(cmd)
    print('dashboard token copied to clipboard')
    dashboard = 'kubectl proxy &'
    os.system(dashboard)
    ctx.run("open http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/")

@task
def off(ctx):
    """kill all port-forwarders"""
    ctx.run('pkill kubectl')
