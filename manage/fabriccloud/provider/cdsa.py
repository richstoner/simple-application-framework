__author__ = 'stonerri'

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import *
from fabric.api import *


def setDefaults():
    ''' Configures the fabric environment to support an aws environment.

    '''
    env.user = 'cdsaadmin'
    env.hosts = ['digitalslidearchive.emory.edu']
    env.password = 'cdsar0ckz!'

    import csv

    # access_key = ''
    # access_secret = ''
    # csv_in = csv.reader(open('credentials.csv', 'r'))
    # for line in csv_in:
    #     if line[0] is not 'User Name':
    #         access_key = line[1]
    #         access_secret = line[2]

    # env.aws_access_key_id = access_key
    # env.aws_secret_access_key = access_secret
    # env.key_filename = '/Users/stonerri/.ssh/isic-archive-keypair.pem'



def sync():

    if not exists('/vagrant'):
        sudo('mkdir /vagrant')
        sudo('chown cdsaadmin:cdsaadmin /vagrant')
        
    exclude_list = [
        '.git',
        '.vagrant',
        'Vagrantfile',
        'readme.md',
        '.idea',
        'last.ini',
        'fabfile.py',
        'fabriccloud',
        '.DS_Store',
        'manage/.git/',
        'doc',
        'manage/.vagrant/',
        'manage/.idea/',
        '_build',
        '_sources',
        '_templates',
        'manage/.DS_Store',
        'server/apps/annotator/venv'
    ]

    rsync_project('/vagrant', local_dir='../', exclude=exclude_list)




def printssh():
    ''' prints an easy-to-use ssh string to console (and mac's clipboard)

    '''

    if env.key_filename:
        print 'ssh -i %s %s@%s' % (env.key_filename, env.user, env.host_string)
        local('echo "ssh -i %s ubuntu@%s" | pbcopy ' % (env.key_filename, env.host_string))
    else:
        print 'ssh ubuntu@%s' % (env.host_string)
        local('echo "ssh -i %s ubuntu@%s" | pbcopy ' % (env.key_filename, env.host_string))


def printhttp():
    ''' prints an easy-to-use http string to console (and mac's clipboard)

    '''

    print 'http://%s' % (env.host_string)
    local('echo "http://%s" | pbcopy ' % (env.host_string))


def systemInformation():
    ''' unimplemented
    '''
    pass



            # def terminate():
# 	#terminate_instances
# 	with settings(warn_only = True):
# 		print 'killing last instance'
# 		conn = ec2.EC2Connection(aws_access_key_id, aws_secret_access_key)
# 		conn.terminate_instances(env.last_instance)
# 		time.sleep(1)
#
#
#
# def createXL():
# 	_create('m3.xlarge')
#
# def createL():
# 	_create('m1.large')
#
#
# def createCustom():
# 	'''usage: fab --set ec2=m2.xlarge createCustom '''
# 	_create(env.ec2)
#
# def createS():
# 	_create('m1.small')
#
# def createXXL():
# 	_create('m2.2xlarge')
#
# def _create(size):
# 	'''Creates a new large instance on ec2'''
# 	with settings(warn_only = True):
# 		conn = ec2.EC2Connection(aws_access_key_id, aws_secret_access_key)
#
# 		time.sleep(1)
# 		reservation = conn.run_instances(precise_12_04_2, instance_type=size, placement='us-east-1d', key_name=ec2keypairname, security_groups=['default', 'irods-web'])
# 		time.sleep(1)
# 		instance = reservation.instances[0]
# 		time.sleep(1)
#
# 		print 'Starting instance %s' %(instance)
# 		while not instance.update() == 'running':
# 			time.sleep(1)
#
# 		instance.add_tag('Name', 'ipython-deploy')
#
# 		time.sleep(1)
#
# 		print 'Instance started: %s' % instance.__dict__['id']
# 		print 'Private DNS: %s' % instance.__dict__['private_dns_name']
# 		print 'Private IP: %s' % instance.__dict__['private_ip_address']
# 		print 'Public DNS: %s' % instance.__dict__['public_dns_name']
#
#
# 		# write temporary settings in case something goes wrong mid-configuration
# 		import ConfigParser
# 		import sys
#
# 		parser = ConfigParser.SafeConfigParser()
# 		parser.add_section('lastLaunch')
# 		parser.set('lastLaunch', 'host_string', str(instance.__dict__['public_dns_name']))
# 		parser.set('lastLaunch', 'keypath', localkeypath)
# 		parser.set('lastLaunch', 'username', 'ubuntu')
# 		parser.set('lastLaunch', 'instance', instance.__dict__['id'])
# 		parser.write(open('lastLaunch.ini', 'w'))
#
# 		env.user = 'ubuntu'
# 		env.host_string = instance.__dict__['public_dns_name']
# 		env.key_filename = [localkeypath]
#
# 		print 'Instance has been launched successfully'
# 		print 'To access, open a browser to http://%s' % (instance.__dict__['public_dns_name'])
# 		print 'ssh -i %s ubuntu@%s' % (localkeypath, instance.__dict__['public_dns_name'])
#
#


#
# def attachebs():
#
# 	with settings(warn_only=True):
#
# 		v_to_mount = ''
# 		conn = ec2.EC2Connection(aws_access_key_id, aws_secret_access_key)
# 		vol = conn.get_all_volumes()
# 		for v in vol:
# 			if v.id == volid:
# 				v_to_mount = v
#
# 		print 'trying to attach volume %s to instance %s' % (v_to_mount, env.last_instance)
#
# 		if v_to_mount.attachment_state() == None:
# 			print 'volume not attached, continuing'
# 			result = v_to_mount.attach(env.last_instance, '/dev/xvdf')
#
# 		else:
# 			print v_to_mount.attachment_state()
#
#
# def mountebs():
#
# 	with settings(warn_only=True):
#
# 		if not exists('/vol'):
# 			sudo('mkdir -m 000 /vol')
# 			sudo('mount /dev/xvdf /vol')
#
# 		# # sudo mkfs.ext4 /dev/xvdf
#
# def unmountebs():
#
# 	with settings(warn_only=True):
#
# 		sudo('umount /dev/xvdf')
#
# 		v_to_unmount = ''
# 		conn = ec2.EC2Connection(aws_access_key_id, aws_secret_access_key)
# 		vol = conn.get_all_volumes()
# 		for v in vol:
# 			if v.id == volid:
# 				v_to_unmount = v
#
# 		result = v_to_unmount.detach(force=True)
# 		if result == True:
# 			print 'volume detached successfully'
# 		else:
# 			print 'volume not attached successfully'
# 		print v_to_unmount.attachment_state()
