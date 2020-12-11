from invoke import task
from subprocess import run, PIPE
import os
from tasks.shared import is_local

@task
def dash(ctx):
    """proxy kubernetes web ui and open window"""
    if is_local():
      p = run("kubectl -n kubernetes-dashboard describe secret admin-user | awk '{for(i=1;i<=NF;i++) {if($i~/token:/) print $(i+1)}}'", shell=True, stdout=PIPE, encoding='ascii')
      cmd = "echo \"{}\" | pbcopy".format(p.stdout)
      ctx.run(cmd)
      print('dashboard token copied to clipboard')
      dashboard = 'kubectl proxy &'
      os.system(dashboard)
      ctx.run("open http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/")

@task
def token(ctx):
    if is_local():
      p = run("kubectl -n kubernetes-dashboard describe secret admin-user | awk '{for(i=1;i<=NF;i++) {if($i~/token:/) print $(i+1)}}'", shell=True, stdout=PIPE, encoding='ascii')
      print(p.stdout)
      cmd = "echo \"{}\" | pbcopy".format(p.stdout)
      ctx.run(cmd)
      print('dashboard token copied to clipboard')

@task
def dashoff(ctx):
    """kill all port-forwarders"""
    if is_local():
      ctx.run('pkill kubectl')

@task
def bench(ctx):
    """Display results from kube-bench run against local cluster"""
    if is_local():
      ctx.run('bash tasks/kube-bench.sh')

@task
def cert(ctx,domain):
    """curl and display certificate information for provided domain"""
    ctx.run(f"curl -I -v --cacert {domain}.localhost.crt 'https://{domain}.localhost/productpage'")

# curl -I -v --cacert bookinfo.localhost.crt 'https://bookinfo.localhost/productpage'
