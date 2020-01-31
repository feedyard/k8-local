from invoke import Collection
from tasks import deploy
from tasks import view
from tasks import delete
from tasks import test

ns = Collection()

ns.add_collection(deploy)
ns.add_collection(view)
ns.add_collection(delete, name='del')
ns.add_collection(test)
