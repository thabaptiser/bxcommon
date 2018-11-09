from bxcommon.constants import HDR_COMMON_OFF
from bxcommon.messages.bloxroute.bloxroute_message_type import BloxrouteMessageType
from bxcommon.messages.bloxroute.message import Message
from bxcommon.utils.crypto import SHA256_HASH_LEN
from bxcommon.utils.object_hash import ObjectHash


class BroadcastMessage(Message):
    MESSAGE_TYPE = BloxrouteMessageType.BROADCAST

    def __init__(self, msg_hash=None, blob=None, buf=None):
        if buf is None:
            self.buf = bytearray(HDR_COMMON_OFF + SHA256_HASH_LEN + len(blob))

            off = HDR_COMMON_OFF
            self.buf[off:off + SHA256_HASH_LEN] = msg_hash.binary
            off += SHA256_HASH_LEN
            self.buf[off:off + len(blob)] = blob
            off += len(blob)

            super(BroadcastMessage, self).__init__(self.MESSAGE_TYPE, off - HDR_COMMON_OFF, self.buf)
        else:
            assert not isinstance(buf, str)
            self.buf = buf
            self._memoryview = memoryview(self.buf)

        self._blob = self._msg_hash = None

    def msg_hash(self):
        if self._msg_hash is None:
            off = HDR_COMMON_OFF
            self._msg_hash = ObjectHash(self._memoryview[off:off + SHA256_HASH_LEN])
        return self._msg_hash

    def blob(self):
        if self._blob is None:
            off = HDR_COMMON_OFF + SHA256_HASH_LEN
            self._blob = self._memoryview[off:off + self.payload_len()]

        return self._blob