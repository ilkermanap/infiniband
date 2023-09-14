NODE = 0
SWITCH = 1

class Switch:
    def __init__(self, switch_id):
        self.guid = switch_id
        self.ports = {}

    def nodes(self):
        temp = []
        for port in self.ports.values():
            if port.connected_to is NODE:
                temp.append(port)
        return temp

    def switches(self):
        temp = []
        for port in self.ports.values():
            if port.connected_to is SWITCH:
                if port.dev not in temp:
                    temp.append(port.dev)
        return temp

    def addport(self, line):
        p = Port(line)
        self.ports[p.portno] = p
        
    def report(self):
        print(self.guid)
        for pno, port in self.ports.items():
            print("   ", pno, port.name, port.lid, port.speed, port.connected_to)

    def topology(self):
        temp = f"SwitchName={self.guid}"
        switches = self.switches()
        if len(switches) > 0:
            temp += " Switches="
            for switch in switches:
                temp += switch + ","
            temp = temp[:-1]
        nodes = self.nodes()
        if len(nodes) > 0:
            temp +=" Nodes="
            for node in nodes:
                temp += node.name + ","
        return temp[:-1]


class Port:
    def __init__(self, line):
        line = line.strip()
        parts = line.split()
        self.portno = line.split("[")[1].split("]")[0]
        self.connected_to = None
        self.dev = line.split('"')[1]
        self.name = line.split('"')[3].split()[0]
        if self.dev.startswith("H") is True:
            self.connected_to = NODE
        elif self.dev.startswith("S") is True:
            self.connected_to = SWITCH
        self.speed = parts[-1]
        self.lid = parts[-2]


class Topology:
    def __init__(self, ibnetdiscover_content):
        self.nodes = {}
        self.switches = {}
        self.parse(ibnetdiscover_content)
        
    def topology(self):
        for switch in self.switches.values():
            print(switch.topology())

    def parse(self, content):
        switch = None
        for line in content:
            if line.find("Mellanox Technologies Aggregation Node") > -1:
                pass
            else:
                if line.startswith("switchguid") is True:
                    guid = line.split("=")[1].split("(")[0]
                    switch = Switch(guid)
                    
                if switch is not None:
                    if line.strip() == "":
                        self.switches[switch.guid] = switch
                        switch = None

                    if line.startswith("[") is True:
                        switch.addport(line)