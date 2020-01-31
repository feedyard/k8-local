from invoke import task
from tasks.shared import is_local
import os

@task
def kubebench(ctx):
    """run kube-bench"""
    if is_local():
      ctx.run("bash conformance/kube-bench.sh")

@task
def ms(ctx):
    """test health of metrics-server"""
    if is_local():
      ctx.run("inspec exec test/metrics-server.rb")

@task
def ksm(ctx):
    """test healt hof kube-state-metrics"""
    if is_local():
      ctx.run("inspec exec test/kube-state-metrics.rb")

@task
def bookinfo(ctx):
    authn("details")
    

def authn(app):
    os.system(f"istioctl authn tls-check -n default $(kubectl get pod -l app={app} -n default -o jsonpath={{.items..metadata.name}}) {app}.default.svc.cluster.local")