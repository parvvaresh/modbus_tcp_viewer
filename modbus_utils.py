from pyModbusTCP.client import ModbusClient

def read_modbus_data(unit_id=1, host="127.0.0.1", port=1502, address_map=None):
    if address_map is None:
        address_map = {
            'coils': (0, 5),
            'discrete_inputs': (0, 5),
            'holding_registers': (0, 5),
            'input_registers': (0, 5)
        }

    client = ModbusClient(host=host, port=port, auto_open=True, unit_id=unit_id)

    if not client.open():
        return {"error": f"Cannot connect to Modbus server at {host}:{port}"}

    def safe_read(fn, name, start, count):
        try:
            values = fn(start, count)
            return values if values is not None else ["Error"] * count
        except:
            return ["Error"] * count

    data = {
        'unit_id': unit_id,
        'coils': safe_read(client.read_coils, "coils", *address_map['coils']),
        'discrete_inputs': safe_read(client.read_discrete_inputs, "discrete_inputs", *address_map['discrete_inputs']),
        'holding_registers': safe_read(client.read_holding_registers, "holding_registers", *address_map['holding_registers']),
        'input_registers': safe_read(client.read_input_registers, "input_registers", *address_map['input_registers']),
    }

    client.close()
    return data
