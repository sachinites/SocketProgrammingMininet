#!/usr/bin/env python

# Topology
#
#                                                                                                              
#                                                        +--------+                                                 
#                                                        |        |                                            
#                                                        |   r    |                                            
#                                                        |        |                                            
#           +--------+                                   +---+----+                                      +----+---+
#           |        |                         10.0.10.254/24|r-eth0.10, vlan 10                         |        |
#           |  h1    | h1-eth0                 10.0.20.254/24|r-eth0.20, vlan 20             10.0.20.2/24|  h4    |
#           |        +----------+                            |                                +----------+        |
#           +--------+10.0.10.1/24                           |                                |  h4-eth0 |        |
#                               |                            |                                |          +--++----+
#                               |                            |s5-eth4.10, vlan 10             |                
#                               |                            |s5-eth4.20, vlan 20             |                
#                               |                  s5-eth0+--+------+s5-eth3                  |
#                               +-------------------------+         +-------------------------+
#                                                   vlan10|   s5    +vlan20                                     
#                                                  s5-eth1|  vlan10 |s5-eth2                                     
#                               +-------------------------+  vlan20 +-------------------------+           
#                               |                   vlan10+---------+vlan20                   |           
#                               |                                                             |           
#                               |                                                             |           
#                               |                                                             |           
#          +---------+          |                                                             |          +-------+
#          |         | h2-eth0  |                                                           10.0.20.1/24 |       |
#          |   h2    +----------+                                                             +----------+  h3   |
#          |         |10.0.10.2/24                                                               h3-eth0 |       |
#          +---------+                                                                                   +-------|
#

# Do necessary imports
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link,TCLink,Intf

if '__main__' == __name__:

    net = Mininet(link=TCLink)

    # Add Hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')

    #Add L2 Switch s5
    s5 = net.addHost('s5')

    #r is a router
    r = net.addHost('r')

    Link(h1, s5) # h1-(h1-eth0)------------(s5-eth0)-s5
    Link(h2, s5) # h2-(h2-eth0)------------(s5-eth1)-s5
    Link(h3, s5) # h3-(h3-eth0)------------(s5-eth2)-s5
    Link(h4, s5) # h4-(h4-eth0)------------(s5-eth3)-s5
    Link(s5, r)  # s5-(s5-eth4)------------(r-eth0)-r

    net.build()

    # Remove default IP addresses from host's interfaces 
    h1.cmd("ifconfig h1-eth0 0")
    h2.cmd("ifconfig h2-eth0 0")
    h3.cmd("ifconfig h3-eth0 0")
    h4.cmd("ifconfig h4-eth0 0")

    # Remove default IP addresses from Switch's Interfaces
    s5.cmd("ifconfig s5-eth0 0")
    s5.cmd("ifconfig s5-eth1 0")
    s5.cmd("ifconfig s5-eth2 0")
    s5.cmd("ifconfig s5-eth3 0")
    s5.cmd("ifconfig s5-eth4 0")

    # Remove default IP addresses from Router's Interface
    r.cmd("ifconfig r-eth0 0")

    # s5-eth4 interface of switch s5 is connected to L3 router r.
    # Therefore for InterVlan routing, s5-eth4 interface need to 
    # operate in Trunk mode in vlan 10 and 20. This is achieved by
    # creating two virtual interfaces viz s5-eth4.10 and s5-eth4.20 
    # out of actual physical interface s5-eth4 first. And then we 
    # will add them to vlan 10 and 20 respectively. 
    # This is equivalent to :
    # a. Make s5-eth4 of L2switch as Trunk, and
    # b. Adding s5-eth4 to vlan 10 and 20 both
    # Note : To use vconfig, you should have vlan pkg install.
    # apt-get install vlan
    s5.cmd("vconfig add s5-eth4 10") # Create a Virtual Interface s5-eth4.10 and mark it as Trunk 
    s5.cmd("vconfig add s5-eth4 20") # Create a Virtual Interface s5-eth4.20 and mark it as Trunk
    
    # bring the new vlan ports up
    s5.cmd("ifconfig s5-eth4.10 up")
    s5.cmd("ifconfig s5-eth4.20 up")


    # Router's r-eth0 physical interface is connected to L2 swotch s5.
    # We need to do same thing here, Create Virtual interface out of
    # r-eth0 viz r-eth0.10 and r-eth0.20
    r.cmd("vconfig add r-eth0 10") # Create a Virtual Interface r-eth0.10 and mark it as Trunk
    r.cmd("vconfig add r-eth0 20") # Create a Virtual Interface r-eth0.20 and mark it as Trunk

    # Create a vlan 10 on Switch s5
    # Note to use brctl, you must have bridge-utils pkg installed.
    # apt-get install bridge-utils
    s5.cmd("brctl addbr vlan10")
    # Create a vlan 20 on Switch s5
    s5.cmd("brctl addbr vlan20")


    # Add s5-eth0 to vlan 10 on L2 siwtch in Access mode
    s5.cmd("brctl addif vlan10 s5-eth0")
    # Add s5-eth1 to vlan 10 on L2 siwtch in Access mode
    s5.cmd("brctl addif vlan10 s5-eth1")
    # Add s5-eth4.10 to vlan 10 on L2 siwtch in Trunk Mode
    s5.cmd("brctl addif vlan10 s5-eth4.10")
    # Add s5-eth2 to vlan 20 on L2 siwtch in Access mode
    s5.cmd("brctl addif vlan20 s5-eth2")
    # Add s5-eth3 to vlan 20 on L2 siwtch in Access mode
    s5.cmd("brctl addif vlan20 s5-eth3")
    # Add s5-eth4.20 to vlan 20 on L2 siwtch in Trunk Mode
    s5.cmd("brctl addif vlan20 s5-eth4.20")

    # Bring up the Vlan interfaces on L2 switch up
    s5.cmd("ifconfig vlan10 up")
    s5.cmd("ifconfig vlan20 up")
    
    # Enable IP Forwarding on Router r
    r.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    # Assign IP Address to Virtual Interfaces on Router. By assigning
    # IP address, r-eth0.10 becomes SVI (Switch Virtual Interface)
    r.cmd("ifconfig r-eth0.10 10.0.10.254 netmask 255.255.255.0")
    r.cmd("ifconfig r-eth0.20 10.0.20.254 netmask 255.255.255.0")
    
    # Assign IP Address to Hosts as ususal
    h1.cmd("ifconfig h1-eth0 10.0.10.1 netmask 255.255.255.0")
    h2.cmd("ifconfig h2-eth0 10.0.10.2 netmask 255.255.255.0")
    h3.cmd("ifconfig h3-eth0 10.0.20.1 netmask 255.255.255.0")
    h4.cmd("ifconfig h4-eth0 10.0.20.2 netmask 255.255.255.0")

    # Lets us add actual L3 route to h1 instead of default. We have
    # commented out the default route entry for h1
    h1.cmd("ip route add to 10.0.20.0/24 via 10.0.10.254 dev h1-eth0")
    #h1.cmd("ip route add default via 10.0.10.254 dev h1-eth0")
    
    h2.cmd("ip route add to 10.0.20.0/24 via 10.0.10.254 dev h2-eth0")
    h2.cmd("ip route add default via 10.0.10.254 dev h2-eth0")

    h3.cmd("ip route add default via 10.0.20.254 dev h3-eth0")
    h4.cmd("ip route add default via 10.0.20.254 dev h4-eth0")

    # Start Mininet Cli prompt
    CLI(net)

    net.stop()
