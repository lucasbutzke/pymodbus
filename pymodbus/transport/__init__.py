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

# The following classes are available for use outside the module.
from .transport_base import BaseTransport, BaseTransportProtocol
from .transport_tcp import TCPtransport
from .transport_tls import TLStransport
from .transport_udp import UDPtransport
from .transport_serial import SERIALtransport

__all__ = [
    "BaseTransport",
    "BaseTransportProtocol",
    "TCPtransport",
    "TLStransport",
    "UDPtransport",
    "SERIALtransport",
]
