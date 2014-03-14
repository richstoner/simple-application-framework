__author__ = 'stonerri'

from fabric.api import *

def setDefaults():
    env.user = 'root'
    env.hosts = ['192.241.156.224']


def sync():

    pass


#
# def printssh():
# 	print 'ssh -i %s ubuntu@%s' % (localkeypath, env.host_string)
# 	local('echo "ssh -i %s ubuntu@%s" | pbcopy ' % (localkeypath, env.host_string))
#
# def printhttp():
# 	print 'http://%s' % (env.host_string)
# 	local('echo "http://%s" | pbcopy ' % (env.host_string))
#
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
# def mountstatus():
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
# 		if v_to_mount.attachment_state() == None:
# 			print 'Volume not attached'
# 		else:
# 			print 'Volume attached with status: %s' % v_to_mount.attachment_state()
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
