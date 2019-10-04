from invoke import task
from pathlib import Path

# pull these versions - task used during development to manage local copies of service versions
GET_ISTIO_VERSION = '1.2.2'

# local paths
VERSIONS_PATH = 'versions/'
ISTIO_PATH = VERSIONS_PATH + 'istio-' + GET_ISTIO_VERSION

@task
def versions(ctx):
    """download specified versions of core services"""

    # istio
    if not Path(ISTIO_PATH).is_dir():
        ctx.run('curl -L https://git.io/getLatestIstio  | ISTIO_VERSION={} sh - && mv istio-{} {}'.format(GET_ISTIO_VERSION, GET_ISTIO_VERSION, ISTIO_PATH))
