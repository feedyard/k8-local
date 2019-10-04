from invoke import Collection
from tasks import deploy
from tasks import download
from tasks import render
from tasks import view
from tasks import delete

ns = Collection()

ns.add_collection(deploy)
ns.add_collection(download, name='get')
ns.add_collection(render)
ns.add_collection(view)
ns.add_collection(delete, name='del')
