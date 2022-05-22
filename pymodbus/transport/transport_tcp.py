"""Transport implementation for TCP."""
import asyncio
from .transport_base import BaseTransport, BaseTransportProtocol


class TCPtransport(BaseTransport, asyncio.Protocol):
    """Modbus tcp transport layer."""

    def __init__(
        self, is_server: bool = False, callbacks: BaseTransportProtocol = None
    ) -> None:
        """Initialize interface."""
        super().__init__(is_server, callbacks)
        self._host: str = "127.0.0.1"
        self._port: int = 502

    def setup(self, host: str, port: int) -> None:  # pylint: disable=arguments-differ
        """Set parameters for implementation class."""
        self._host = host
        self._port = port

    async def _async_start_client(self) -> None:
        """Start client."""
        self._transport, self._protocol = self._loop.create_connection(
            self, self._host, self._port
        )

    async def _async_start_server(self) -> None:
        """Start server."""

    async def async_send(self, data: bytes) -> None:
        """Send data to client/server."""
        await super().async_send(data)

    async def _async_stop_client(self) -> None:
        """Stop client."""

    async def _async_stop_server(self) -> None:
        """Stop server."""
