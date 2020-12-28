from invoke import task
from tasks.shared import is_local
from tasks import metrics
from tasks import istio
from tasks import dashboard
from tasks import domain

@task
def start(ctx):
    """start minikube with extra-config values and tunnel lb"""
    START_K8S="""
minikube start \
--extra-config=kubelet.authentication-token-webhook=true \
--extra-config=kubelet.authorization-mode=Webhook \
--extra-config=scheduler.address=0.0.0.0 \
--extra-config=controller-manager.address=0.0.0.0
"""

    ctx.run(START_K8S)
    ctx.run('minikube tunnel &')


@task
def init(ctx, ns, localdomain):
    """deploy locally metrics-server api v0.4.1, kube-state-metrics api v1.9.7"""
    if is_local():
      metrics.add(ctx)
      istio.add(ctx)
      domain.add(ns, localdomain)

@task
def bench(ctx):
    """Display results from kube-bench run against local cluster"""
    if is_local():
      ctx.run('bash tasks/kube-bench.sh')

