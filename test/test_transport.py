"""Test transport module"""
import pytest
import pymodbus.transport as t_tcp


@pytest.mark.asyncio
async def test_transport():
    """Test transport."""

    my_obj = t_tcp.TCPtransport(False, None)
    my_obj.setup()
    await my_obj.async_start()
