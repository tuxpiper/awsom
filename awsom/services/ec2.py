from awsom.entity import Entity, Factory

from boto.ec2.connection import EC2Connection

class EC2RootEntity(Entity):
    def __init__(self, parent, name="ec2", **attrs):
        super(EC2RootEntity, self).__init__(parent=parent, name=name, factory=EC2RootFactory(self))
        # Make connection EC2 specific
        self._connection = self._connection.clone()
        self._connection.set_connection_class(EC2Connection)
    
class EC2RootFactory(Factory):    
    def __init__(self, entity):
        super(EC2RootFactory, self).__init__(entity) 
    def populate(self):
        self.entity._add_child("instances", EC2InstancesRootEntity(parent=self.entity))
        return True

class EC2InstancesRootEntity(Entity):
    def __init__(self, parent, name="instances", **attrs):
        super(EC2InstancesRootEntity, self).__init__(parent=parent, name=name, factory=EC2InstancesFactory(self))
    def _get_instance_name(self, instance):
        """
        This method returns the name that a children instance should have
        """
        return instance.id.replace('-','_')

class EC2InstancesFactory(Factory):
    def __init__(self, entity):
        super(EC2InstancesFactory, self).__init__(entity) 
    def populate(self):
        ec2conn = self.entity._get_connection()
        for r in ec2conn.get_all_instances(filters={'instance-state-name' : 'running'}):
            for i in filter(lambda i: i.state == 'running', r.instances):
                i_name = self.entity._get_instance_name(i)
                self.entity._add_child(
                    i_name,
                    EC2InstanceEntity(
                        parent = self.entity,
                        name = i_name,
                        ec2boto_obj = i)
                )

class EC2InstanceEntity(Entity):
    """
    The entity type for EC2 instances. This is a terminal node in the entity
    tree, by definition, it has no children
    """
    def __init__(self, parent, name, ec2boto_obj, **attrs):
        super(EC2InstanceEntity,self).__init__(parent=parent, name=name)
        self._ec2boto_obj = ec2boto_obj
        # Copy attributes from boto instance object
        for attr in ["id", "tags", "architecture", "dns_name", "region", "instance_type", "private_ip_address"]:
            self.add_attr(attr, vars(ec2boto_obj)[attr])
    def get_console_output(self):
        return self._ec2boto_obj.get_console_output().output


