"""Transport level.

This async module is an abstraction of different transport types:
- TCP
- TCP/TLS
- UDP
- Serial
- Custom
And the protocol layer, for servers by calling startServer(),
and clients by calling accept()

The module transport bytes (the "how", where protocol does the "what").

Callbacks to handle the data exchange.

For future extensions it is possible to use a custom transport class.
"""
from __future__ import annotations
import logging
import abc
import asyncio
from typing import Any

_logger = logging.getLogger(__name__)


class BaseTransportProtocol(metaclass=abc.ABCMeta):
    """Base class for callbacks."""

    def cb_connection_made(self, transport: BaseTransport) -> None:
        """Call when a new connection is establisehd."""
        self._log_event("Connection made", transport)

    def cb_data_received(self, data: bytes) -> None:
        """Call when data is received."""
        self._log_event("Data received", data)

    def cb_data_sent(self, exc: Exception = None) -> None:
        """Call when data have been sent."""
        self._log_event("Data sent", exc)

    def cb_connection_lost(self, exc: Exception = None) -> None:
        """Call when connection is lost (disconnect)."""
        self._log_event("Connection lost", exc)

    def _log_event(self, title: str, extras: Any) -> None:
        """Call to log callback call"""
        txt = f"Callback: {title}: {self} {extras}"
        _logger.debug(txt)


class BaseTransport(metaclass=abc.ABCMeta):
    """Modbus transport layer interface class."""

    @abc.abstractmethod
    def __init__(self, is_server: bool, callbacks: BaseTransportProtocol) -> None:
        """Initialize interface."""
        self._is_server = is_server
        self._cbs = BaseTransportProtocol()
        self._loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self._transport = None
        self._protocol = None

    @abc.abstractmethod
    def setup(self) -> None:
        """Set parameters for implementation class."""

    async def async_start(self) -> None:
        """Start client/server."""
        if self._is_server:
            await self._async_start_server()
        else:
            await self._async_start_client()

    @abc.abstractmethod
    async def async_send(self, data: bytes) -> None:
        """Send data to client/server."""

    async def async_stop(self) -> None:
        """Stop client/server."""
        if self._is_server:
            await self._async_stop_server()
        else:
            await self._async_stop_client()

    @abc.abstractmethod
    async def _async_start_client(self) -> None:
        """Start client."""

    @abc.abstractmethod
    async def _async_start_server(self) -> None:
        """Start server."""

    @abc.abstractmethod
    async def _async_stop_client(self) -> None:
        """Stop client."""

    @abc.abstractmethod
    async def _async_stop_server(self) -> None:
        """Stop server."""

    # ----------------------
    # Callbacks from asyncio
    # ----------------------

    def connection_made(self, transport: Transport):
        """Call from asyncio when a connection is made.

        :param transport: transport class object.
        """
        self._transport = transport
        self._cbs.cb_connection_made(transport)

    def data_received(self, data: bytes) -> None:
        """Call from asyncio when data is received.

        :param data: bytes received
        """
        self._cbs.cb_data_received(data)

    def connection_lost(self, exc: Exception = None) -> None:
        """Call from asyncio when connection is lost (disconnect).

        :param exc: Reason (exception) for disconnect
        """
        self._cbs.cb_connection_lost(exc)
