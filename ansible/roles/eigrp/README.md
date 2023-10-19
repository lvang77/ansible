bgp
=========

Installs EIGRP routing configs on Cisco IOS through CLI.

Requirements
------------

Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

eigrp_config:
  as: EIGRP AS
  rid: EIGRP route-id
  networks:
    - "10.1.2.0 0.0.0.255" Address and wildcard mask for network advertisement

Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1"
  hosts: site1-dist1
  connection: network_cli

  roles:
    - eigrp

License
-------

BSD

Author Information
------------------

Lucky Vang
