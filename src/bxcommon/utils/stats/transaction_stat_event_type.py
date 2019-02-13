class TransactionStatEventType(object):
    TX_RECEIVED_FROM_BLOCKCHAIN_NODE = "TxReceivedFromBlockchainNode"
    TX_RECEIVED_FROM_BLOCKCHAIN_NODE_IGNORE_SEEN = "TxReceivedFromBlockchainNodeIgnoreSeen"
    TX_SENT_FROM_GATEWAY_TO_PEERS = "TxSentFromGatewayToPeers"
    TX_SENT_FROM_GATEWAY_TO_BLOCKCHAIN_NODE = "TxSentFromGatewayToBlockchainNode"
    TX_RECEIVED_BY_GATEWAY_FROM_PEER = "TxReceivedByGatewayFromPeer"
    TX_RECEIVED_BY_GATEWAY_FROM_PEER_IGNORE_SEEN = "TxReceivedByGatewayFromPeerIgnoreSeen"
    TX_RECEIVED_BY_RELAY_FROM_PEER = "TxReceivedByRelayFromPeer"
    TX_RECEIVED_BY_RELAY_FROM_PEER_IGNORE_SEEN = "TxReceivedByRelayFromPeerIgnoreSeen"
    TX_SHORT_ID_ASSIGNED_BY_RELAY = "TxShortIdAssignedByRelay"
    TX_SHORT_ID_STORED_BY_GATEWAY = "TxShortIdStoredByGateway"
    TX_SHORT_ID_EMPTY_IN_MSG_FROM_RELAY = "TxShortIdEmptyInMsgFromRelay"
    TX_SENT_FROM_RELAY_TO_PEERS = "TxSentFromRelayToPeers"
    TX_UNKNOWN_SHORT_IDS_REQUESTED_BY_GATEWAY_FROM_RELAY = "TxUnknownShortIdsRequestedByGatewayFromRelay"
    TX_UNKNOWN_SHORT_IDS_REPLY_RECEIVED_BY_GATEWAY_FROM_RELAY = "TxUnknownShortIdsReplyReceivedByGatewayFromRelay"
    TX_UNKNOWN_SHORT_IDS_REPLY_SENT_BY_RELAY_TO_GATEWAY = "TxUnknownShortIdsReplySentByRelayToGateway"



