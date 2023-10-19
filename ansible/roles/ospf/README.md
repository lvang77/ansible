bgp
=========

Installs OSPF routing configs on Cisco IOS through CLI.

Requirements
------------

Cisco IOS
Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

ospf_config:
  pid: OSPF Process ID
  rid: OSPF router-id
  networks:
    - "10.2.1.0 0.0.0.255 area 0"


Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1"
  hosts: site2-dist1
  connection: network_cli

  roles:
    - ospf

License
-------

BSD

Author Information
------------------

Lucky Vang
