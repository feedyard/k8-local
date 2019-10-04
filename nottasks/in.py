from invoke import Collection
#from tasks import download_versions
from tasks import render
from tasks import deploy
from tasks import view
from tasks import delete

ns = Collection()

#ns.add_collection(download_versions, name='get')
ns.add_collection(render)
ns.add_collection(deploy)
ns.add_collection(delete)
ns.add_collection(view)
