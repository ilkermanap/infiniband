from topology import Topology

c1 = open("ibnetdiscover-nash-compute.txt").readlines()
c2 = open("ibnet.txt").readlines()

t = Topology(c1)
t.topology()
