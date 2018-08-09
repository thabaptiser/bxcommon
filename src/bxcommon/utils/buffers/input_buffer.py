from collections import deque


class InputBuffer(object):
    def __init__(self):
        self.input_list = deque()
        self.length = 0

    def endswith(self, suffix):
        if self.input_list:
            return False

        if len(self.input_list[-1]) >= len(suffix):
            return self.input_list[-1].endswith(suffix)
        else:
            # FIXME self_input_list, self.suffix are undefined, change
            #   to self.input_list, suffix and test
            raise RuntimeError("FIXME")

        # elif len(self_input_list) > 1:
        #     first_len = len(self.input_list[-1])
        #
        #     return self.suffix[-first_len:] == self.input_list[-1] and \
        #            self.input_list[-2].endswith(self.suffix[:-first_len])
        # return False

    # Adds a bytearray to the end of the input buffer.
    def add_bytes(self, piece):
        assert isinstance(piece, bytearray)
        self.input_list.append(piece)
        self.length += len(piece)

    # Removes the first num_bytes bytes in the input buffer and returns them.
    def remove_bytes(self, num_bytes):
        assert self.length >= num_bytes > 0

        to_return = bytearray(0)
        while self.input_list and num_bytes >= len(self.input_list[0]):
            next_piece = self.input_list.popleft()
            to_return.extend(next_piece)
            num_bytes -= len(next_piece)
            self.length -= len(next_piece)

        assert self.input_list or num_bytes == 0

        if self.input_list:
            to_return.extend(self.input_list[0][:num_bytes])
            self.input_list[0] = self.input_list[0][num_bytes:]
            self.length -= num_bytes

        return to_return

    # Returns the first bytes_to_peek bytes in the input buffer.
    # The assumption is that these bytes are all part of the same message.
    # Thus, we combine pieces if we cannot just return the first message.
    def peek_message(self, bytes_to_peek):
        if bytes_to_peek > self.length:
            return bytearray(0)

        while bytes_to_peek > len(self.input_list[0]):
            head = self.input_list.popleft()
            head.extend(self.input_list.popleft())
            self.input_list.appendleft(head)

        return self.input_list[0]

    # Gets a slice of the inputbuffer from start to end.
    # We assume that this slice is a piece of a single bitcoin message
    # for performance reasons (with respect to the number of copies).
    # Additionally, the start value of the slice must exist.
    def get_slice(self, start, end):
        assert self.length >= start

        # Combine all of the pieces in this slice into the first item on the list.
        # Since we will need to do so anyway when handing the message.
        while end > len(self.input_list[0]) and len(self.input_list) > 1:
            head = self.input_list.popleft()
            head.extend(self.input_list.popleft())
            self.input_list.appendleft(head)

        return self.input_list[0][start:end]