from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*10),
    co=ModbusSequentialDataBlock(0, [1]*10),
    hr=ModbusSequentialDataBlock(0, [123]*10),
    ir=ModbusSequentialDataBlock(0, [456]*10)
)
context = ModbusServerContext(slaves={1: store}, single=False)

StartTcpServer(context, address=("localhost", 1502))
