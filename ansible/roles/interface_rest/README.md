bgp
=========

Installs interface configs on Cisco IOSXE through RESTCONF.

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

interface_config:
  ietf-interfaces:interfaces:
    interface:
    - name: GigabitEthernet1
      description: MGMT
      type: iana-if-type:ethernetCsmacd
      enabled: true
      ietf-ip:ipv4:
        address:
        - ip: 192.168.50.18
          netmask: 255.255.255.0
    - name: Loopback0
      type: iana-if-type:softwareLoopback
      enabled: true
      ietf-ip:ipv4:
        address:
        - ip: 1.1.1.10
          netmask: 255.255.255.255


Dependencies
------------


Example Playbook
----------------

- name: "Setup Site1"
  hosts: site1-core1
  connection: network_cli

  roles:
    - interface_rest

License
-------

BSD

Author Information
------------------

Lucky Vang
