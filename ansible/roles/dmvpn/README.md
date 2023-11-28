dmvpn
=========

Installs DMVPN configs on Cisco IOS-XE through CLI.

Requirements
------------

Ansible
Jinja2

Role Variables
--------------

ansible_user:
ansible_password:

### hostvars.yml

dmvpn:
  layer: "spoke"
  tunnel:
    ip_addr: 10.10.0.3 255.255.255.0
  isp_intf:
    interface: GigabitEthernet2
    description: "ISP Gi5"
    ip_addr: 172.16.3.2
    mask: 255.255.255.0
    gateway: 172.16.3.1
  hub:
    tun_addr: 10.10.0.1
    isp_addr: 172.16.0.2

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
