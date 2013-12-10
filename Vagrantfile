# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "debian72"

  config.vm.box_url = "https://bitbucket.org/keimlink/django-workshop/downloads/debian72.box"
  config.vm.box_download_checksum_type = "sha1"
  config.vm.box_download_checksum = "f29e08d39b252c20e10ad56d1a668a1ac6dc7720"
  config.vm.provider "vmware_fusion" do |v, override|
    override.vm.box_url = "https://bitbucket.org/keimlink/django-workshop/downloads/debian72_vmware.box"
    override.vm.box_download_checksum = "f197cad61586c6a8c8447e55c5366bac86a37e94"
  end

  # Port forwarding for Django's development server.
  config.vm.network "forwarded_port", guest: 8000, host: 8000,
    auto_correct: true

  config.vm.synced_folder "salt/roots/", "/srv/"

  config.vm.provision :salt do |salt|

    salt.minion_config = "salt/minion"
    salt.run_highstate = true

  end
end
