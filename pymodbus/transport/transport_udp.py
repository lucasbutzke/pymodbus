"""Transport implementation for TCP sync."""
from .transport_base import BaseTransport, BaseTransportProtocol


class UDPtransport(BaseTransport):
    """Modbus tcp transport layer."""

    def __init__(
        self, is_server: bool = False, callbacks: BaseTransportProtocol = None
    ) -> None:
        """Initialize interface."""
        super().__init__(is_server, callbacks)

    def setup(self) -> None:
        """Set parameters for implementation class."""

    async def _async_start_client(self) -> None:
        """Connect to server."""

    async def _async_start_server(self) -> None:
        """Start server and accept client connections."""

    async def async_send(self, data: bytes) -> None:
        """Send data to client/server."""

    async def _async_stop_client(self) -> None:
        """Disconnect from client/."""

    async def _async_stop_server(self) -> None:
        """Disconnect from server."""
