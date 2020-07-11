#!/usr/bin/env python

# Do necessary imports
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link

if '__main__' == __name__:

    net = Mininet()

    # Add Hosts
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    # Add Routers
    r1 = net.addHost('r1')
    r2 = net.addHost('r2')
    r3 = net.addHost('r3')

    # Add links
    net.addLink(h1, r1 , intfName1 = 'h1-eth0', intfName2 = 'r1-eth0')
    net.addLink(r1, r2 , intfName1 = 'r1-eth1', intfName2 = 'r2-eth0')
    net.addLink(r2, r3 , intfName1 = 'r2-eth1', intfName2 = 'r3-eth0')
    net.addLink(r3, h2 , intfName1 = 'r3-eth1', intfName2 = 'h2-eth0')

    net.build()

    # Remove default IP addresses from host's interfaces 
    h1.cmd("ifconfig h1-eth0 0")
    h2.cmd("ifconfig h2-eth0 0")

    # Assign IP Address to Hosts as ususal
    h1.cmd("ifconfig h1-eth0 10.1.1.1 netmask 255.255.255.0")
    h2.cmd("ifconfig h2-eth0 13.1.1.2 netmask 255.255.255.0")

    # Default Route in hosts
    h1.cmd("ip route add default via 10.1.1.2 dev h1-eth0")
    h2.cmd("ip route add default via 13.1.1.1 dev h2-eth0")

    # config loop back addresses of hosts
    h1.cmd("ifconfig lo 122.1.1.4 netmask 255.255.255.255")
    h2.cmd("ifconfig lo 122.1.1.5 netmask 255.255.255.255")
    
    # config Router R1
    r1.cmd("ifconfig r1-eth0 0")
    r1.cmd("ifconfig r1-eth1 0")
    r1.cmd("ifconfig r1-eth0 10.1.1.2 netmask 255.255.255.0")
    r1.cmd("ifconfig r1-eth1 11.1.1.2 netmask 255.255.255.0")
    r1.cmd("ifconfig lo 122.1.1.1 netmask 255.255.255.255")
    
    # config Router R2
    r2.cmd("ifconfig r2-eth0 0")
    r2.cmd("ifconfig r2-eth1 0")
    r2.cmd("ifconfig r2-eth0 11.1.1.1 netmask 255.255.255.0")
    r2.cmd("ifconfig r2-eth1 12.1.1.1 netmask 255.255.255.0")
    r2.cmd("ifconfig lo 122.1.1.2 netmask 255.255.255.255")
    
    # config Router R3
    r3.cmd("ifconfig r3-eth0 0")
    r3.cmd("ifconfig r3-eth1 0")
    r3.cmd("ifconfig r3-eth0 12.1.1.2 netmask 255.255.255.0")
    r3.cmd("ifconfig r3-eth1 13.1.1.1 netmask 255.255.255.0")
    r3.cmd("ifconfig lo 122.1.1.3 netmask 255.255.255.255")

    #enable IP forwarding on Router
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    #install L3 routes on the router R1 for all remote subnets
    r1.cmd("ip route add to 122.1.1.4/32 via 10.1.1.1 dev r1-eth0") # Route to h1
    r1.cmd("ip route add to 122.1.1.2/32 via 11.1.1.1 dev r1-eth1") # Route to r2
    r1.cmd("ip route add to 122.1.1.3/32 via 11.1.1.1 dev r1-eth1") # Route to r3
    r1.cmd("ip route add to 122.1.1.5/32 via 11.1.1.1 dev r1-eth1") # Route to h2
    r1.cmd("ip route add to 12.1.1.0/24  via 11.1.1.1 dev r1-eth1") # Route to subnet S3
    r1.cmd("ip route add to 13.1.1.0/24  via 11.1.1.1 dev r1-eth1") # Route to subnet S4

    #install L3 routes on the router R2 for all remote subnets
    r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r2.cmd("ip route add to 122.1.1.4/32 via 11.1.1.2 dev r2-eth0") # Route to h1
    r2.cmd("ip route add to 122.1.1.1/32 via 11.1.1.2 dev r2-eth0") # Route to r1
    r2.cmd("ip route add to 122.1.1.3/32 via 12.1.1.2 dev r2-eth1") # Route to r3
    r2.cmd("ip route add to 122.1.1.5/32 via 12.1.1.2 dev r2-eth1") # Route to h2
    r2.cmd("ip route add to 10.1.1.0/24  via 11.1.1.2 dev r2-eth0") # Route to subnet S1
    r2.cmd("ip route add to 13.1.1.0/24  via 12.1.1.2 dev r2-eth1") # Route to subnet S4

    #install L3 routes on the router R3 for all remote subnets
    r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r3.cmd("ip route add to 122.1.1.4/32 via 12.1.1.1 dev r3-eth0") # Route to h1
    r3.cmd("ip route add to 122.1.1.1/32 via 12.1.1.1 dev r3-eth0") # Route to r1
    r3.cmd("ip route add to 122.1.1.2/32 via 12.1.1.2 dev r3-eth0") # Route to r2
    r3.cmd("ip route add to 122.1.1.5/32 via 13.1.1.2 dev r3-eth1") # Route to h2
    r3.cmd("ip route add to 10.1.1.0/24  via 12.1.1.1 dev r3-eth0") # Route to subnet S1
    r3.cmd("ip route add to 11.1.1.0/24  via 12.1.1.1 dev r3-eth0") # Route to subnet S2

    #install L3 routes on the host h1 for all remote subnets
    h1.cmd("ip route add to 122.1.1.1/32 via 10.1.1.2 dev h1-eth0") # Route to r1
    h1.cmd("ip route add to 122.1.1.2/32 via 10.1.1.2 dev h1-eth0") # Route to r2
    h1.cmd("ip route add to 122.1.1.3/32 via 10.1.1.2 dev h1-eth0") # Route to r3
    h1.cmd("ip route add to 122.1.1.5/32 via 10.1.1.2 dev h1-eth0") # Route to h2
    h1.cmd("ip route add to 11.1.1.0/24  via 10.1.1.2 dev h1-eth0") # Route to subnet S2
    h1.cmd("ip route add to 12.1.1.0/24  via 10.1.1.2 dev h1-eth0") # Route to subnet S3
    h1.cmd("ip route add to 13.1.1.0/24  via 10.1.1.2 dev h1-eth0") # Route to subnet S4

    #install L3 routes on the host h2 for all remote subnets
    h2.cmd("ip route add to 122.1.1.1/32 via 13.1.1.1 dev h2-eth0") # Route to r1
    h2.cmd("ip route add to 122.1.1.2/32 via 13.1.1.1 dev h2-eth0") # Route to r2
    h2.cmd("ip route add to 122.1.1.3/32 via 13.1.1.1 dev h2-eth0") # Route to r3
    h2.cmd("ip route add to 122.1.1.4/32 via 13.1.1.1 dev h2-eth0") # Route to h2
    h2.cmd("ip route add to 11.1.1.0/24  via 13.1.1.1 dev h2-eth0") # Route to subnet S2
    h2.cmd("ip route add to 12.1.1.0/24  via 13.1.1.1 dev h2-eth0") # Route to subnet S3
    h2.cmd("ip route add to 10.1.1.0/24  via 13.1.1.1 dev h2-eth0") # Route to subnet S1
    
    # Start Mininet Cli prompt
    CLI(net)

    net.stop()
