#!/usr/bin/python
from awsom.entity import Entity, Factory
from awsom.config import AccountEntity, config

class ModelRootFactory(Factory):
    def __init__(self, entity):
        super(ModelRootFactory, self).__init__(entity)
    def populate(self):
        # Attach all configuration-defined accounts as children of the entity
        for account in config.get_account_names():
            self.entity._add_child(account, AccountEntity(parent=self.entity, **config.get_account(account)))
        return True

class ModelRootEntity(Entity):
    def __init__(self, name):
        super(ModelRootEntity, self).__init__(factory=ModelRootFactory(self),name=name)
    def add_account(self, name, **attrs):
        self._add_child(name, AccountEntity(parent=self, name=name, **attrs))

# Upon import, the registered accounts should be loaded into the model root, so the
# recommended usage would be something like:
#    from awsom import model as aws
# So you can do something like:
#	 aws.add_account('devel_ls', access_key_id=xxxx, secret_access_key=yyyy)
# and then:
#    aws.devel_ls.ec2.instances

model = ModelRootEntity(name='model')
