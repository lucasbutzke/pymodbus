"""Async serial client."""
import logging
import asyncio
from serial_asyncio import create_serial_connection

from pymodbus.client.asynchronous.async_io import ModbusClientProtocol
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.factory import ClientDecoder


# ----------------------------------------------------------------------- #
# configure the client logging
# ----------------------------------------------------------------------- #
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x01


async def start_async_test(client):
    """Start async test."""
    # ----------------------------------------------------------------------- #
    # specify slave to query
    # ----------------------------------------------------------------------- #
    # The slave to query is specified in an optional parameter for each
    # individual request. This can be done by specifying the `unit` parameter
    # which defaults to `0x00`
    # ----------------------------------------------------------------------- #
    log.debug("Reading Coils")
    rr = client.read_coils(1, 1, unit=UNIT)

    # ----------------------------------------------------------------------- #
    # example requests
    # ----------------------------------------------------------------------- #
    # simply call the methods that you would like to use. An example session
    # is displayed below along with some assert checks. Note that some modbus
    # implementations differentiate holding/input discrete/coils and as such
    # you will not be able to write to these, therefore the starting values
    # are not known to these tests. Furthermore, some use the same memory
    # blocks for the two sets, so a change to one is a change to the other.
    # Keep both of these cases in mind when testing as the following will
    # _only_ pass with the supplied asynchronous modbus server (script supplied).
    # ----------------------------------------------------------------------- #
    log.debug("Write to a Coil and read back")
    rq = await client.write_coil(0, True, unit=UNIT)
    rr = await client.read_coils(0, 1, unit=UNIT)
    assert rq.function_code < 0x80  # nosec test that we are not an error
    assert rr.bits[0]  # nosec test the expected value

    log.debug("Write to multiple coils and read back- test 1")
    rq = await client.write_coils(1, [True] * 8, unit=UNIT)
    assert rq.function_code < 0x80  # nosec test that we are not an error
    rr = await client.read_coils(1, 21, unit=UNIT)
    assert rr.function_code < 0x80  # nosec test that we are not an error
    resp = [True] * 21
    resp.extend([False] * 3)
    assert rr.bits == resp  # nosec test the expected value

    rq = await client.write_coils(1, [False] * 8, unit=UNIT)
    rr = await client.read_coils(1, 8, unit=UNIT)
    assert rq.function_code < 0x80  # nosec test that we are not an error
    assert rr.bits == [False] * 8  # nosec test the expected value

    rr = await client.read_discrete_inputs(0, 8, unit=UNIT)
    assert rq.function_code < 0x80  # nosec test that we are not an error

    rq = await client.write_register(1, 10, unit=UNIT)
    rr = await client.read_holding_registers(1, 1, unit=UNIT)
    assert rq.function_code < 0x80  # nosec test that we are not an error
    assert rr.registers[0] == 10  # nosec test the expected value

    rq = await client.write_registers(1, [10] * 8, unit=UNIT)
    rr = await client.read_holding_registers(1, 8, unit=UNIT)
    assert rq.function_code < 0x80  # nosec test that we are not an error
    assert rr.registers == [10] * 8  # nosec test the expected value

    rr = await client.read_input_registers(1, 8, unit=UNIT)
    assert rq.function_code < 0x80  # nosec test that we are not an error

    arguments = {
        "read_address": 1,
        "read_count": 8,
        "write_address": 1,
        "write_registers": [20] * 8,
    }
    rq = await client.readwrite_registers(unit=UNIT, **arguments)
    rr = await client.read_holding_registers(1, 8, unit=UNIT)
    assert rq.function_code < 0x80  # nosec test that we are not an error
    assert rq.registers == [20] * 8  # nosec test the expected value
    assert rr.registers == [20] * 8  # nosec test the expected value


# create_serial_connection doesn"t allow to pass arguments
# to protocol so that this is kind of workaround
def make_protocol():
    """Make protocol."""
    return ModbusClientProtocol(framer=ModbusRtuFramer(ClientDecoder()))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = create_serial_connection(
        loop, make_protocol, "/tmp/ttyp0", baudrate=9600  # nosec
    )
    transport, protocol = loop.run_until_complete(asyncio.gather(coro))[0]
    loop.run_until_complete(start_async_test(protocol))
    loop.close()
