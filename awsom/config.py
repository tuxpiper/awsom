from awsom.entity import Entity, Factory
from os import getenv, path

from yaml import load as yload, dump as ydump
try:
    from yaml import CLoader as YLoader, CDumper as YDumper
except ImportError:
    from yaml import Loader as YLoader, Dumper as YDumper

def find_config_file():
    """
    Locate configuration file, by default these locations are searched:
        * AWSOMRC environment variable file
        * $VIRTUAL_ENV/.awsomrc.yaml
        * $HOME/.awsomrc.yaml
    Only one is used
    """
    awsomrc_path = getenv("AWSOMRC")
    virtenv_path = getenv("VIRTUAL_ENV") and path.join(getenv("VIRTUAL_ENV"), ".awsomrc.yaml")
    home_path = getenv("HOME") and path.join(getenv("HOME"), ".awsomrc.yaml")
    
    # Check existing file
    if awsomrc_path and path.isfile(awsomrc_path): return awsomrc_path
    if virtenv_path and path.isfile(virtenv_path): return virtenv_path
    if home_path and path.isfile(home_path): return home_path
    
    # If no existing file, determine where it should be created
    final_path = awsomrc_path or virtenv_path or home_path
    return final_path

class AwsomConfig():
    def __init__(self):
        self.fname = find_config_file()
        if path.isfile(self.fname):
            f = open(self.fname)
            self._config = yload(f, Loader=YLoader)
            f.close()
        else:
            self._config = {"awsom":{"accounts":{}}}
    def save(self):
        f = open(self.fname, "w")
        f.write(ydump(self._config, Dumper=YDumper))
        f.close()
    def get_account_names(self):
        """
        Return names of configured accounts 
        """
        return self._config["awsom"]["accounts"].keys()
    def get_account(self, name):
        return self._config["awsom"]["accounts"][name]
    def add_account(self, name):
        dic = { "name": name }
        self._config["awsom"]["accounts"][name] = dic
        return dic

config = AwsomConfig()        

class BotoConnection(object):
    """
    This is basically a container for the parameters that need to be passed
    to boto connection classes.
    A connection object is disabled until set_connection_class is called
    and provided a non-null value, corresponding to the boto class that
    generates the connection.
    """
    def __init__(self, **conn_args):
        self.conn_args = conn_args
        self.connection_class = None
    def set_connection_class(self, the_class):
        self.connection_class = the_class
    def get_connection(self):
        if self.connection_class == None:
            raise Exception("Connection disabled")
        return self.connection_class(**self.conn_args)
    def clone(self):
        """
        Return a copy of the connection object
        """
        c = BotoConnection(**self.conn_args)
        c.connection_class = self.connection_class
        return c

class AccountEntity(Entity):
    def __init__(self, parent, name, **attrs):
        super(AccountEntity, self).__init__(parent=parent, name=name, factory=AccountFactory(self))
        # Bind to configuration
        global config
        if name in config.get_account_names():
            self._entity_attrs = config.get_account(name)
        else:
            self._entity_attrs = config.add_account(name)
            # Make sure all essential attributes are defined
            self.add_attr("access_key_id")
            self.add_attr("secret_access_key")
            # Copy in attributes
            if attrs.has_key("access_key_id"):
                self.access_key_id = attrs["access_key_id"]
            if attrs.has_key("secret_access_key"):
                self.secret_access_key = attrs["secret_access_key"]
        #
        self._connection = BotoConnection(
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key)
    def __setattr__(self, name, value):
        # Behavior when connection attributes are modified
        super(AccountEntity, self).__setattr__(name, value)
        # Internal attributes don't trigger anything
        if name[0] == "_": return
        # If connection credentials are modified invalidate children and
        # re-create connection
        if name in [ "access_key_id", "secret_access_key" ]:
            self._invalidate_children()
            self._connection = BotoConnection(
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key)
        # Save config
        global config
        config.save()

class AccountFactory(Factory):
    def __init__(self, entity):
        super(AccountFactory, self).__init__(entity)
    def populate(self):
        # Add access to AWS services
        from awsom.services.ec2 import EC2RootEntity
        self.entity._add_child("ec2", EC2RootEntity(parent=self.entity))
        return True
