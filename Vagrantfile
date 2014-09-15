# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

	# base instance = ubuntu 12.04 LTS

	config.vm.box = "hashicorp/precise64"

	# landrush configuratino -> dynamic dns

	config.landrush.enabled = true
	config.landrush.tld = 'uda2study.dev'
	config.landrush.guest_redirect_dns = false

	config.vm.hostname = "uda2study.dev"

	# mapped folders

	config.vm.synced_folder "../applications", "/applications"

	# useful for figuring out safeboot issues, also nice to have

	config.vm.provider :virtualbox do |vb|
	  vb.gui = true
	end

end

