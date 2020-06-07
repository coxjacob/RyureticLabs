#####################################################################
# Ryuretic: A Modular Framework for RYU                             #
# !/mininet/custum/Ryuretic_Topo.py                                 #
# Author:                                                           #
#   Jacob Cox                                                       #
# Ryuretic_Topo.py                                                  #
# date 6 June 2020                                                  #
#####################################################################
# Copyright (C) 2020 Jacob Cox - All Rights Reserved                #
# You may use, distribute and modify this code under the            #
# terms of the Ryuretic license, provided this work is cited        #
# in the work for which it is used.                                 #
# For latest updates, please visit:                                 #
#                   https://github.com/Ryuretic/RyureticLabs        #
#####################################################################
"""How To Run This Program
This program sets up a mininet architecture consisting of one NAT router,
one switch, and 6 hosts. 

Startup Instructions:
    In terminal 1:
    1) Start Controller
       a) cd env
       b) source py38_env/bin/activate
       c) cd ../ryu
       d) PYTHONPATH=. ./bin/ryu-manager ryu/app/Ryuretic/Ryuretic_Intf.py
    In terminal 2:
    1) Startup Topology
       a) sudo mn -c
       b) sudo mn --custom ~/mininet/custom/Ryuretic_Topo.py ~topo mytopo
Shutdown Instructions:
    In terminal 2:
    1) Teardown Topology
       a) exit
       b) sudo mn -c
    In terminal 1:
       a) cntl + c
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import custom
from mininet.node import RemoteController,OVSSwitch
from mininet.log import setLogLevel, info
from mininet.nodelib import NAT
from mininet.cli import CLI
from mininet.util import run

#Topology to be instantiated in Mininet
class RyureticTopo(Topo):
    "Mininet Security Rev Test topology"
    
    def __init__(self, cpu=.1, max_queue_size=None, **params):
        print( '''
        nat+--+              +-----------+h1
              |              +-----------+h2
              +-------+s1+---+-----------+h3
              CNTLR+---+     +-----------+h4
                             +-----------+h5
                             +-----------+h6
        ''' )
        # Initialize topo
        Topo.__init__(self, **params)
        ###Thanks to Sean Donivan for the NAT code####
        natIP= '10.0.0.254'
        # Host and link configuration
        hostConfig = {'cpu': cpu, 'defaultRoute': 'via ' + natIP }
        LinkConfig = {'bw': 10, 'delay': '1ms', 'loss': 0,
                   'max_queue_size': max_queue_size }
        #################################################

        #add Single Switch
        print( "*** Creating switch (s1) *** \n" )
        s1  = self.addSwitch('s1', protocols='OpenFlow13')
      
        #add six hosts with IP assigned
        print( "*** Creating hosts (h1, h2, h3, h4, h5, h6) *** \n" )
        print( "*** Linking hosts to switch (s1) *** /n" )
        h1 = self.addHost('h1', mac='00:00:00:00:00:01', ip="10.0.0.1", **hostConfig)
        self.addLink(s1, h1, 1, 1, **LinkConfig)
        
        h2 = self.addHost('h2', mac='00:00:00:00:00:02', ip="10.0.0.2", **hostConfig)
        self.addLink(s1, h2, 2, 1, **LinkConfig)
        
        h3 = self.addHost('h3', mac='00:00:00:00:00:03', ip="10.0.0.3", **hostConfig)
        self.addLink(s1, h3, 3, 1, **LinkConfig)
        
        h4 = self.addHost('h4', mac='00:00:00:00:00:04', ip="10.0.0.4", **hostConfig)
        self.addLink(s1, h4, 4, 1, **LinkConfig)
        
        h5 = self.addHost('h5', mac='00:00:00:00:00:05', ip="10.0.0.5", **hostConfig)
        self.addLink(s1, h5, 5, 1, **LinkConfig)
        
        h6 = self.addHost('h6', mac='00:00:00:00:00:06', ip="10.0.0.6", **hostConfig)
        self.addLink(s1, h6, 6, 1, **LinkConfig)

        # Create and add NAT
        print( " Creating NAT (nat1) *** \n" )
        print( " Linking NAT to switch (s1) *** \n" )
        self.nat = self.addNode( 'nat', cls=NAT, ip=natIP,
                            inNamespace=False)	
        self.addLink(s1, self.nat, port1=8 )	


topo_pick = RyureticTopo()
info('*** Starting Mininet *** \n')
print( '*** Starting Mininet *** \n' )
net = Mininet(topo=topo_pick, link=TCLink, controller=RemoteController)
info('*** Topology Created *** \n')
print( " ***Toplology Created*** \n" )

net.start()
run("ovs-vsctl set bridge s1 protocols=OpenFlow13")
print('Network Started')
info('***attempting to start dhcp server***')
info('*** Running CLI *** \n')
CLI( net )

info ('*** Stopping Network ***')
net.stop()
print("Exiting Network")
