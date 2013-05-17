#!/usr/bin/python

class Entity(object):
    """
    Super-class of all objects in the awsom tree. Each entity consists of
      * parent entity (accessible as _parent)
      * connection object (accessible as _connection)
      * children (dictionary with entity IDs as keys) 
      * entity attributes
    """
    def __init__(self, parent=None, connection=None, factory=None, name="[entity]"):
        self._parent = parent
        self._connection = connection or ((parent != None) and parent._connection)
        self._factory = factory
        self._children = {}
        self._populated = False
        self._entity_attrs = {}
        self._valid = True
        self.add_attr("name", name)
    def find(self, **criteria):
        """
        Traverse tree to find all entities that comply with the given criteria
        """
        pass
    def add_attr(self, name, value=None):
        """
        Define a new attribute for the entity, does nothing if the attribute
        has previously been added
        """
        if not self._entity_attrs.has_key(name):
            self._entity_attrs[name] = value
    def _invalidate(self):
        """
        Invalidates this object and its children recursively. This provides
        means for the user to avoid using entities that are stale
        """
        self._valid = False
        self._invalidate_children()
    def _add_child(self, name, value):
        """ Add/set a child of this entity"""
        self._children[name] = value
    def _invalidate_children(self):
        """
        Invalidates and unlists entities' children
        """
        for e in self._children.values():
            if e._valid: e._invalidate()
        self._children = {}
        self._populated = False
    def _get_connection(self):
        """
        Convenience method for obtaining the connection relative to the entity
        """
        return self._connection.get_connection()
    def _set_attr(self, name, value):
        """
        Modify attribute directly in the dictionary, without triggering any
        other kind of behavior. Does nothing if the attribute has not been
        previously added
        """
        if self._entity_attrs.has_key(name):
            self._entity_attrs[name] = value
    def _populate(self):
        """
        Use the factory for populating the entity
        """
        if not self._populated:
            if self._factory and self._factory.populate():
                self._populated = True
    # Traversal operator
    def __getattribute__(self, name):
        """
        Traverse through the entity with the "." operator, we implement a
        custom lookup that follows these priorities
            1. Entity attributes
            2. Class attributes and methods (python built-in)
            3. Children by id
        Names starting with "_" are reserved
        """
        if name[0] == "_":
            return super(Entity,self).__getattribute__(name)
        if self._entity_attrs.has_key(name):
            return self._entity_attrs[name]
        else:
            try:
                return super(Entity,self).__getattribute__(name)
            except AttributeError as e:
                self._populate()
                if self._children.has_key(name):
                    return self._children[name]
                else:
                    raise e
    def __setattr__(self, name, value):
        """
        Set the value of defined attributes or, if not defined, regular
        class attributes (python built-in)
        """
        if name[0] == "_":
            return super(Entity,self).__setattr__(name, value)
        if self._entity_attrs.has_key(name):
            self._entity_attrs[name] = value
        else:
            super(Entity,self).__setattr__(name, value)
    # Operators to emulate container type
    def __len__(self):
        """ Return children count """
        self._populate()
        return len(self._children)
    def __getitem__(self, key):
        """
        Children can be accessed through the [] operator using their id
        """
        self._populate()
        if self._children.has_key(key):
            return self._children[key]
        else:
            raise KeyError("Child %s doesn't exist" % key)
    def __setitem__(self, key, value):
        raise Exception("Unsupported")
    def __delitem__(self, key):
        raise Exception("Unsupported")
    def __iter__(self):
        """ Iterate through child IDs """
        self._populate()
        return self._children.__iter__()
    def __contains__(self, item):
        """ Entity contains child with id """
        self._populate()
        return self._children.has_key(item)
    # Printing and other
    def _get_breadcrumbs_str(self):
        """ Return string representing the path of this entity within the tree """
        ret = self.name
        p = self._parent
        while p:
            ret = p.name + " > " + ret
            p = p._parent
        return ret
    def __str__(self):
        """ Return print out of the entity """
        ret = self._get_breadcrumbs_str() + "\n"
        ret = ret + "  Type: %s\n" % str(self.__class__)
        ret = ret + "  Attributes:\n"
        for attr in sorted(self._entity_attrs.keys()):
            val = self.__getattribute__(attr)
            if val:
                if isinstance(val, str):
                    ret = ret + "    .%s = \"%s\"\n" % (attr, val)
                else:
                    ret = ret + "    .%s = %s\n" % (attr, str(val))
            else:
                ret = ret + "    .%s = (unset)\n" % attr
        ret = ret + "  Methods:\n"
        for attr in sorted(dir(self)):
            if attr[0] == "_": continue
            attr_val = super(Entity,self).__getattribute__(attr)
            if callable(attr_val): ret = ret + "    .%s()\n" % attr
            else: ret = ret + "    ." + attr + "\n"
        ret = ret + "  Children (%d):\n" % len(self)
        for k in self:
            ret = ret + "    ['%s']\n" % k
        return ret
    
class Factory(object):
    """
    A factory populates an entity object with the appropriate children
    """
    def __init__(self, entity):
        self.entity = entity
    def populate(self):
        """
        This method creates the entity children. Return True if the operation
        has been successful
        """
        return True


