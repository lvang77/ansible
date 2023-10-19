bgp
=========

Installs BGP routing configs on Cisco IOS through CLI.

Requirements
------------

Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

bgp_config:
  asn: Local BGP ASN
  rid: BGP router-id
  networks:
    - address: Network to advertise
      mask: Network mast
  neighbors:
    - neighbor: Neighbor IP
      peer_asn: Neighbor BGP ASN
  vedge_neighbor:
    - neighbor: vEdge neighbor IP
      peer_asn: vEdge peer ASN

Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1 Core"
  hosts: site1-core1
  connection: network_cli

  roles:
    - bgp

License
-------

BSD

Author Information
------------------

Lucky Vang
