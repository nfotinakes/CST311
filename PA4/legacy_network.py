#!/usr/bin/env python3

# Names: Alonso Vega, Daniel Letterman, Gabe Williams, & Nicholas Fotinakes
# Team: 10
# Date: 6-18-2022
# Title: PA4 - legacy_network.py
# Description: This script creates the topology for our network/subnets acting as
# West/East coast networks connected via the internet. The script is modified to
# build correctly with static routes implemented, as well as launching the chat and
# web servers

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.term import makeTerm
import time

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    # Rearranged switch/router build order to avoid "build errors"
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    # Edited IP address of r3 for our network/subnets
    r3 = net.addHost('r3', cls=Node, ip='10.0.1.3/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    # Edited IP address of r4 for our network/subnets
    r4 = net.addHost('r4', cls=Node, ip='192.168.1.2/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    # Edited IP address of r5 for our network/subnets
    r5 = net.addHost('r5', cls=Node, ip='10.0.2.3')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    # Assigned hosts with IP to match network diagram and default route
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.1/24', defaultRoute='via 10.0.1.3')
    h2 = net.addHost('h2', cls=Host, ip='10.0.1.2/24', defaultRoute='via 10.0.1.3')
    h3 = net.addHost('h3', cls=Host, ip='10.0.2.1/24', defaultRoute='via 10.0.2.3')
    h4 = net.addHost('h4', cls=Host, ip='10.0.2.2/24', defaultRoute='via 10.0.2.3')

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(s1, r3)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s2, r5)
    # Add interface names for links between r3, r4, and r5
    net.addLink(r3, r4, intfname1='r3-eth1', params1={'ip':'192.168.1.1/30'}, intfname2='r4-eth0', params2={'ip':'192.168.1.2/30'})
    net.addLink(r4, r5, intfname1='r4-eth1', params1={'ip':'192.168.2.2/30'}, intfname2='r5-eth1', params2={'ip':'192.168.2.1/30'})
    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])

    # Add static routes to specify how to traverse subnets
    info('*** Adding static routes\n')
    # Static routes for r3 to reach subnets
    r3.cmd('ip route add 10.0.2.0/24 via 192.168.1.2 dev r3-eth1')
    r3.cmd('ip route add 192.168.2.0/30 via 192.168.1.2 dev r3-eth1')

    # Static routes for r4 to reach subnets
    r4.cmd('ip route add 10.0.1.0/24 via 192.168.1.1 dev r4-eth0')
    r4.cmd('ip route add 10.0.2.0/24 via 192.168.2.1 dev r4-eth1')

    # Static routes for r5 to reach subnets
    r5.cmd('ip route add 10.0.1.0/24 via 192.168.2.2 dev r5-eth1')
    r5.cmd('ip route add 192.168.1.0/30 via 192.168.2.2 dev r5-eth1')

    # Launch xTerm windows for h1, h3, and h4 to launch the chat server/clients
    makeTerm(h4, title='Node', term='xterm', display=None, cmd='python3 /home/mininet/CST311/PA4/chat_server.py')
    time.sleep(1)
    makeTerm(h1, title='Node', term='xterm', display=None, cmd='python3 /home/mininet/CST311/PA4/chat_client.py')
    time.sleep(1)
    makeTerm(h3, title='Node', term='xterm', display=None, cmd='python3 /home/mininet/CST311/PA4/chat_client.py')
    time.sleep(1)
    # Create and issue TLS certificate and then launch web server on h2
    h2.cmd('python3 /home/mininet/CST311/PA4/cert_auth.py')
    time.sleep(2)
    makeTerm(h2, title='Node', term='xterm', display=None, cmd='python3 /home/mininet/CST311/PA4/web_server.py')

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
