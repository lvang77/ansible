# Ansible Automation of Remote Sites through Cisco SDWAN

This repo is a lab POC in EVE-NG using MPLS L3VPN to connect 3 remote sites to a DC Core site.
The entire Cisco network devices, including the ISP routers were configured through Ansible network 
automation using Jinja2 templates and Ansible roles. Cisco IOS-XE devices were all configured through 
RESTCONF while vIOS routers were configured through the Ansible ios_config module. NXOS devices were 
configured through the cli using the Ansible nxos_config module.  All BGP configurations were done through 
Jinja2 templates in Ansible roles.

![Lab Diagram](lab.jpg)

## Images Used

Cisco Catalyst 8000V: 17.10.01a

Cisco Nexus 9500v: nxos64-cs.10.2.3.F.bin

vIOS Router: VIOS-ADVENTERPRISEK9-M

## EVE-NG Lab File

The EVE-NG lab file was exported and is available in the repo for you to import into EVE-NG yourself.

eve-ng-ansible.zip

## Network Details

The MGMT Cloud0 network (192.168.50.0/24) is the only connection to devices outside of the EVE-NG lab. 
All IP class A and B private networks can only connect within the EVE-NG lab. Class B private networks
are used to simulate Internet connectivity while Class A private networks used to simulate private
networks.

All remote sites and the DC Core use a MPLS L3VPN underlay in the IPS core and PE routers with a DMVPN
Phase3 overlay connecting each site's core router. Each remote site runs either EIGRP or OSPF underlay
for eBGP to have connectivity to neighbor peers through loopback interfaces.

## ISP Details

Four Cisco Catalyst 8000V are used to simulate MPLS provider core with four additional Catalyst 8000V
used as PE routers for MPLS connectivity.

## DC Core

The DC Core site contains NXOS switches running VXLAN in a single site deployment.

## Remote Site Details

Remote Site 1 routers are running EIGRP underlay for eBGP to have peer neighbor connectivity. Remote Site 2 and 3
both run OSPF underlay.

## Initial Configuration i.e. Bootstrap Configs

Using EVE-NG options, all Cisco network devices and VPCs have basic bootstrap startup configurations to allow
you to connect to them through the MGMT network and run automation scripts against them. The startup configurations
were saved to EVE-NG startup configs so you can wipe any Cisco network device to start over again with automation.

One thing to note, the vIOS routers would not accept their static IP address for their MGMT network connection and
each vIOS router required an extra step to manually configure the MGMT network or a manual reboot.

## Default Username and Passwords

All Cisco devices use local authentication with the username admin and password of admin.

## Setup Order

The YAML files in the main ansible directory with numbers in front, i.e. 1_isp.yml are the order that I automated
the entire network.

## Additional Automation Tools

The additional folders contains automation scripts using Nornir, Napalm, Scrapli, Pytest, and Pyats to show some basic troubleshooting
scripts along with automated backing up of configurations and restore.

## POC Next Steps

I designed this lab to be compatible with the free EVE-NG community version. My next step is to use the paid
Pro version and run Dockers for a TIG stack to implement some MDT configurations. If there are enough CPU resources
in my server, I would like to automate some high availability configurations along with Cisco ISE, FTD, and Windows AD.
