from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class MininetRouterModified( Node ):
    "A Node with IP forwarding enabled."

    def config( self, loo_addr, **params ):
        super( MininetRouterModified, self).config( **params )
        # Enable forwarding on the router
        # Create Loopback Interface and Assign Loopback Address to the Router
        # All loopback addresses have mask 32
        loo_config = 'ifconfig lo:1 ' + loo_addr + ' netmask 255.255.255.255 up'
        self.cmd(loo_config)
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( MininetRouterModified, self ).terminate()

class NetworkTopo( Topo ):

    def build(self, **_opts):

            # Create a Router Object
            #r1_obj = MininetRouter('122.1.1.1', name="r1")
            # Add Router object to the topology
        r1 = self.addNode(name='r1',loo_addr='122.1.1.1', cls=MininetRouterModified)


if __name__ == '__main__':
    customTopo = NetworkTopo()

    #Get handle to net to manage your topology
    net = Mininet(topo=customTopo, controller=DefaultController)

    #start/deploy the Topology
    net.start()

    #Get Halt at Mininet CLI prompt
    CLI(net)

    #Destroy and stop the topology
    net.stop()
