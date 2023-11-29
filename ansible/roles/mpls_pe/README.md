mpls_pe
=========

Installs MPLS on Pe routres on Cisco IOS-XE through CLI.

Requirements
------------

Cisco IOS-XE
Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

mpls_config:
  vrfs:
    - vrf: CUSTOMER1
      rd: "100:1"
      interface: GigabitEthernet2
      intf_ip_addr: 172.16.2.1 255.255.255.0
      ospf_pid: 2
      ospf_rid: "33.33.33.33"
      ospf_network: 172.16.2.0 0.0.0.255
      ospf_area: 0

bgp_config:
  asn: 100
  neighbors:
    - neighbor: 11.11.11.11
    - neighbor: 22.22.22.22
    - neighbor: 44.44.44.44
  loopback: Loopback0


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
