awsom - AWS Object Model
========================

Browse your AWS resources using a hierarchical object model

Usage
-----

Fire up your python interpreter RPEL. All usage of the module is done through an 'aws' instance exported by the main module, so you do:

    >>> from awsom import aws

First time, you will want to configure an account, for instance:

    >>> aws.add_account("myaws", access_key_id="xxxx", secret_access_key="yyyy")

Your account details are saved automatically to awsom's config file, so next time you use it, the account will already be there. The account is accessible as a children node (named "myaws"), you can print it out:

    >>> print aws.myaws
    aws > myaws
      Type: <class 'awsom.config.AccountEntity'>
      Attributes:
        .access_key_id = "xxxxxxxxxxxxxxxxxxxx"
        .name = "myaws"
        .secret_access_key = "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
      Methods:
        .add_attr()
        .find()
      Children (1):
        ['ec2']

So far we only have access to some ec2 instance info, you can print your instance list

    >>> print aws.myaws.ec2.instances
    aws > myaws > ec2 > instances
      Type: <class 'awsom.services.ec2.EC2InstancesRootEntity'>
      Attributes:
        .name = "instances"
      Methods:
        .add_attr()
        .find()
      Children (2):
        ['i_xxxxxxxx']
        ['i_yyyyyyyy']

And some info about some instance:

    >>> print aws.myaws.ec2.instances.i_xxxxxxxx
    aws > myaws > ec2 > instances > i_xxxxxxxx
      Type: <class 'awsom.services.ec2.EC2InstanceEntity'>
      Attributes:
        .architecture = x86_64
        .dns_name = ec2-xx-yy-zz-ccc.compute-1.amazonaws.com
        .id = i-xxxxxxxx
        .instance_type = m1.large
        .name = i_xxxxxxxx
        .private_ip_address = 10.xxx.yyy.ccc
        .region = RegionInfo:us-east-1
        .tags = {}
      Methods:
        .add_attr()
        .find()
        .get_console_output()
      Children (0):

Another thing to try:

    >>> for i in aws.myaws.ec2.instances: print aws.myaws.ec2.instances[i]
