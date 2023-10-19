bgp
=========

Installs OSPF routing configs on Cisco IOSXE through RESTCONF.

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

ospf_config:
  Cisco-IOS-XE-native:router:
    Cisco-IOS-XE-ospf:router-ospf:
      ospf:
        process-id:
        - id: 2
          network:
          - ip: 10.2.0.0
            wildcard: 0.0.0.255
            area: 0
          router-id: 192.168.50.20


Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1"
  hosts: site2-core1
  connection: network_cli

  roles:
    - ospf_rest

License
-------

BSD

Author Information
------------------

Lucky Vang
