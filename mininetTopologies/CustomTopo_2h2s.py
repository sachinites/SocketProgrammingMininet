"""Custom topology example

Two directly connected switches plus a host for each switch:

host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.

To run this program, on terminal trigger the below command :
    
    sudo mn --custom CustomTopo_2h2s.py  --test pingall

"""

"""

+--------+                    +--------+                      +--------+                      +-------+
|        |                    +        |                      |        |                      |       |
|  h1    +--------------------+  s1    +----------------------+   s2   +----------------------+  h2   |
|        |                    |        |                      |        |                      |       |
+--------+                    +--------+                      +--------+                      +-------+

"""


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
from mininet.node import OVSController

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )

        # Add links
        self.addLink( h1, s1 )
        self.addLink( s1, s2 )
        self.addLink( s2, h2 )

customTopo = MyTopo()
net = Mininet(topo=customTopo)
#c0 = net.addController(name='c0')
net.start()
print "Dumping host connections"
dumpNodeConnections(net.hosts)
print "Testing network connectivity"
net.pingAll()
CLI(net)
net.stop()

