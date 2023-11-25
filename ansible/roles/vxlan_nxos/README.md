vxlan
=========

Configure VXLANS in Cisco NXOS through CLI.

Requirements
------------

Cisco NXOS
Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

ospf_config:
  pid: 1
  rid: 192.168.50.37
  interfaces:
    - interface: e1/1
      area: 0
    - interface: e1/2
      area: 0
  loopback:
    - interface: loopback0
      ip_addr: 1.0.0.7
      mask: 255.255.255.255
      area: 0


Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1"
  hosts: site2-dist1
  connection: network_cli

  roles:
    - ospf_nxos

License
-------

BSD

Author Information
------------------

Lucky Vang
