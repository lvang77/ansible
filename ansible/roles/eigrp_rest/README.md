bgp
=========

Installs EIGRP routing configs on Cisco IOSXE through RESTCONF.

Requirements
------------

Cisco IOSXE
Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

eigrp_config:
  Cisco-IOS-XE-native:router:
    Cisco-IOS-XE-eigrp:router-eigrp:
      eigrp:
        classic-mode:
        - autonomous-system: 1
          eigrp:
            router-id: 192.168.50.18
          network:
            address-wildcard:
            - ipv4-address: 10.1.1.0
              wildcard: 0.0.0.255


Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1"
  hosts: site1-core1
  connection: network_cli

  roles:
    - eigrp_rest

License
-------

BSD

Author Information
------------------

Lucky Vang
