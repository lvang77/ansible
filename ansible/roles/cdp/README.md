bgp
=========

Installs interface configs on Cisco IOS through CLI.

Requirements
------------

Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

interfaces:
  - interface: "Gi0/1"
    description: "site1-core1 Gi3"
    ip: "10.1.2.2 255.255.255.0"


Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1"
  hosts: site1-dist1
  connection: network_cli

  roles:
    - interfaces

License
-------

BSD

Author Information
------------------

Lucky Vang
