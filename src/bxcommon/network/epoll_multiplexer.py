import errno
import select

from bxcommon.network.abstract_multiplexer import AbstractMultiplexer
from bxcommon.network.socket_connection import SocketConnection
from bxcommon.network.socket_connection_state import SocketConnectionState
from bxcommon.utils import logger


class EpollMultiplexer(AbstractMultiplexer):
    def __init__(self, communication_strategy):
        logger.debug("Before contructor")
        super(EpollMultiplexer, self).__init__(communication_strategy)
        self._epoll = select.epoll()
        logger.debug("After contructor")

    def run(self):
        logger.debug("Start multiplexer loop")

        try:
            self._start_server()

            timeout = self._communication_strategy.on_first_sleep()

            while True:
                self._establish_outbound_connections()

                # Grab all events.
                try:
                    if timeout is None:
                        timeout = -1

                    events = self._epoll.poll(timeout)
                except IOError as ioe:
                    if ioe.errno == errno.EINTR:
                        logger.info("got interrupted in epoll")
                        continue
                    raise ioe

                for fileno, event in events:

                    if fileno in self._socket_connections:
                        socket_connection = self._socket_connections[fileno]
                        assert isinstance(socket_connection, SocketConnection)

                        if socket_connection.is_server:
                            self._handle_incoming_connections(socket_connection)
                        else:
                            # Mark this connection for close if we received a POLLHUP. No other functions will be called
                            #   on this connection.
                            if event & select.EPOLLHUP:
                                socket_connection.set_state(SocketConnectionState.MARK_FOR_CLOSE)
                                self._communication_strategy.on_connection_closed(fileno)

                            if event & select.EPOLLOUT and \
                                    not socket_connection.state & SocketConnectionState.MARK_FOR_CLOSE:
                                # If connect received EINPROGRESS, we will receive an EPOLLOUT if connect succeeded
                                if not socket_connection.state & SocketConnectionState.INITIALIZED:
                                    socket_connection.set_state(SocketConnectionState.INITIALIZED)

                                # Mark the connection as sendable and send as much as we can from the outputbuffer.
                                socket_connection.can_send = True

                                self._send(socket_connection)
                    else:
                        assert False, "Connection not handled!"

                # Handle EPOLLIN events.
                for fileno, event in events:

                    socket_connection = self._socket_connections[fileno]
                    assert isinstance(socket_connection, SocketConnection)

                    # we already handled the new connections above, no need to handle them again
                    if not socket_connection.is_server:

                        if event & select.EPOLLIN and \
                                not socket_connection.state & SocketConnectionState.MARK_FOR_CLOSE:
                            self._receive(socket_connection)

                        # Done processing. Close socket if it got put on the blacklist or was marked for close.
                        if socket_connection.state & SocketConnectionState.MARK_FOR_CLOSE:
                            logger.debug("Connection to {0} closing".format(socket_connection.connection_id()))
                            socket_connection.close()
                            self._communication_strategy.on_connection_closed(fileno)

                if self._communication_strategy.on_chance_to_exit():
                    logger.debug("Ending Epoll loop. Shutdown has been requested.")
                    break

                timeout = self._communication_strategy.on_sleep(not events)
        finally:
            self.close()

    def close(self):
        super(EpollMultiplexer, self).close()

        self._epoll.close()

    def _register_socket(self, new_socket, address, is_server=False, initialized=True, from_me=False):
        super(EpollMultiplexer, self)._register_socket(new_socket, address, is_server, initialized, from_me)

        if is_server:
            self._epoll.register(new_socket.fileno(), select.EPOLLIN | select.EPOLLET)
        else:
            self._epoll.register(new_socket.fileno(),
                                 select.EPOLLOUT | select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP | select.EPOLLET)
