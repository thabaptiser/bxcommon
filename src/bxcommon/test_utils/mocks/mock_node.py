from bxcommon.connections.node_type import NodeType
from bxcommon.services.transaction_service import TransactionService
from bxcommon.utils.alarm import AlarmQueue
from bxcommon.connections.abstract_node import AbstractNode


class MockNode(AbstractNode):
    node_type = NodeType.RELAY

    def __init__(self, external_ip, external_port):
        mock_opts = MockOpts()
        mock_opts.external_port = external_port
        mock_opts.external_ip = external_ip
        self.opts = mock_opts
        self.alarm_queue = AlarmQueue()
        self.tx_service = TransactionService(self)
        self.connection_pool = []

        self.broadcast_messages = []
        mock_opts = MockOpts()
        super(MockNode, self).__init__(mock_opts)

    def broadcast(self, msg, requester):
        self.broadcast_messages.append(msg)


class MockOpts(object):

    def __init__(self):
        self.node_id = "foo"
        self.external_ip = "127.0.0.1"
        self.external_port = 8000
        self.internal_ip = "127.0.0.1"
        self.internal_port = 8000
        self.log_path = "./"
        self.to_stdout = True
        self.index = 1
        self.sid_start = 1
        self.sid_end = 100000
        self.sid_expire_time = 99999
        self.outbound_peers = False
