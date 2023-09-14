from topology import Topology

c1 = open("ibnetdiscover-output.txt").readlines()

t = Topology(c1)
t.topology()
