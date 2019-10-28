from invoke import task

@task
def kubebench(ctx):
    ctx.run("bash conformance/kube-bench.sh")
