multicast_nxos
=========

Installs Multicast routing configs on Cisco NXOS through CLI.

Requirements
------------

NXOS
Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

multicast:
  layer: "spine"
  rp_address: 1.2.3.4
  lo0_addr: 1.0.0.2
  group_list: 224.0.0.0/4
  ssm_range: 232.0.0.0/8

Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1 Core"
  hosts: site1-core1
  connection: network_cli

  roles:
    - multicast_nxos

License
-------

BSD

Author Information
------------------

Lucky Vang
