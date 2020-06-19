from mininet.net import Mininet
from mininet.node import DefaultController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, TCLink

#reference : http://intronetworks.cs.luc.edu/current/html/mininet.html

def topology():

    net = Mininet()

    #Add Controller to the Topology
    c0 = net.addController( 'c0', 
         controller=DefaultController) 

    # Add hosts and switches
    h1 = net.addHost('h1')

    #Below line do not configure IP, but configure mac
    #h1 = net.addHost( 'h1', ip='100.168.0.1/24', mac = '00:00:00:00:00:01')

    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    #Add L2 Switch
    s1 = net.addSwitch('s1')

    #Add links
    link_h1s1 = net.addLink( h1, s1 , intfName1 = 'h1-s1', intfName2 = 's1-h1')
    link_h2s1 = net.addLink( h2, s1 , intfName1 = 'h2-s1', intfName2 = 's1-h2')
    link_h3s1 = net.addLink( h3, s1 , intfName1 = 'h3-s1', intfName2 = 's1-h3')

    #Below line do not configure IP, we will add IP later via another method
    #link_h3s1 = net.addLink( h3, s1 , intfName1 = 'h3-s1', intfName2 = 's1-h3', params2 = {'ip' : '100.168.0.3/24'})
   
    # Below line configure MAC, but do not configure IP, we will add IP later via another method
    #link_h1s1.intf1.config(ip='100.168.0.1/24', mac = '00:00:00:00:00:01')
    #link_h2s1.intf1.config(ip='100.168.0.2/24', mac = '00:00:00:00:00:02')
    #link_h3s1.intf1.config(ip='100.168.0.3/24', mac = '00:00:00:00:00:03') 

    # configure mac address on switch interfaces
    link_h1s1.intf2.config(ip=None, mac = '00:00:00:00:00:04')
    link_h2s1.intf2.config(ip=None, mac = '00:00:00:00:00:05')
    link_h3s1.intf2.config(ip=None, mac = '00:00:00:00:00:06')


    #finished building the Topology
    net.build()
   
    # ip address and mac should be set after net.build()
    h1.setIP('100.168.0.1', prefixLen=24, intf='h1-s1')
    h2.setIP('100.168.0.2', prefixLen=24, intf='h2-s1')
    h3.setIP('100.168.0.3', prefixLen=24, intf='h3-s1')

    h1.setMAC('00:00:00:00:00:01', intf='h1-s1')
    h2.setMAC('00:00:00:00:00:02', intf='h2-s1')
    h3.setMAC('00:00:00:00:00:03', intf='h3-s1')

    #start the network
    net.start()

    # Once the network is built and started, we can now run command on 
    # device's linux shell as below to configure them further
    # This is another method you can configure IP and MAC on device's
    # interfaces. But be reminded, any config done using cmd wont reflect 
    # in 'dump' output on mininet shell
    #h1.cmd('ifconfig h1-s1 100.168.0.1 netmask 255.255.255.0')
    #h2.cmd('ifconfig h2-s1 100.168.0.2 netmask 255.255.255.0')
    #h3.cmd('ifconfig h3-s1 100.168.0.3 netmask 255.255.255.0')

    #Setting lo IP addresses
    h1.cmd('ifconfig lo 122.1.1.1 netmask 255.255.255.255')
    h2.cmd('ifconfig lo 122.1.1.2 netmask 255.255.255.255')
    h3.cmd('ifconfig lo 122.1.1.3 netmask 255.255.255.255')

    # Setting up routes in host's Routing Table to reach each other 
    # loopback addresses

    #Enable IP forwarding
    h1.cmd('sysctl net.ipv4.ip_forward=1')
    h1.cmd('ip route add to 122.1.1.2/32 via 100.168.0.2 dev h1-s1')
    h1.cmd('ip route add to 122.1.1.3/32 via 100.168.0.3 dev h1-s1')

    h2.cmd('sysctl net.ipv4.ip_forward=1')
    h2.cmd('ip route add to 122.1.1.1/32 via 100.168.0.1 dev h2-s1')
    h2.cmd('ip route add to 122.1.1.3/32 via 100.168.0.3 dev h2-s1')

    h3.cmd('sysctl net.ipv4.ip_forward=1')
    h3.cmd('ip route add to 122.1.1.1/32 via 100.168.0.1 dev h3-s1')
    h3.cmd('ip route add to 122.1.1.2/32 via 100.168.0.2 dev h3-s1')

    #Start the Controller
    #c0.start()

    #start the Switches
    #s1.start( [c0] )

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':

    setLogLevel( 'info' )

    topology() 
