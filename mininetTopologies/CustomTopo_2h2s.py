"""Custom topology example

Two directly connected switches plus a host for each switch:

host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.

To run this program, on terminal trigger the below command :
    
    sudo python CustomTopo_2h2s.py

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

#Topology Description here
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

# Execution of Program starts here

#Create the Topology Object
customTopo = MyTopo()

#Get handle to net to manage your topology
net = Mininet(topo=customTopo)

#start/deploy the Topology
net.start()

print "Dumping host connections"
dumpNodeConnections(net.hosts)

print "Testing network connectivity"
net.pingAll()

#Get Halt at Mininet CLI prompt
CLI(net)

#Destroy and stop the topology
net.stop()

# program ends here
