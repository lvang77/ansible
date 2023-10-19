bgp
=========

Saves running config through RESTCONF.

Requirements
------------

Cisco IOSXE
Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1"
  hosts: site2-core1
  connection: network_cli

  roles:
    - save_config_rest

License
-------

BSD

Author Information
------------------

Lucky Vang
