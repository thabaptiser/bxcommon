class OutboundPeerModel(object):
    def __init__(self, ip, port, idx=None, node_id=None, is_internal=False):

        self.ip = ip
        self.port = port
        self.idx = idx
        self.node_id = node_id
        self.is_internal = is_internal

    def __str__(self):
        return "({}, {}, {}, {}, {})".format(self.ip, self.port, self.idx, self.node_id, self.is_internal)

    def __repr__(self):
        return "OutboundPeerModel" + self.__str__()

    def __eq__(self, other):
        return isinstance(other, OutboundPeerModel) and other.ip == self.ip and other.port == self.port \
               and other.idx == self.idx and other.is_internal == self.is_internal

    def __hash__(self):
        return hash(self.__repr__())
