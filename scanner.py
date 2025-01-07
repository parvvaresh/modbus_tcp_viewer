from pyModbusTCP.client import ModbusClient
from tabulate import tabulate
import time
import sys

def read_modbus_data(client, unit_id, start_addresses):
    data = {}
    # Set the unit ID
    client.unit_id = unit_id  # Corrected assignment
    
    # Read Coils
    try:
        coils = client.read_coils(start_addresses['coils'][0], start_addresses['coils'][1])
        if coils is not None:
            data['Coils'] = coils
        else:
            data['Coils'] = ['Error'] * start_addresses['coils'][1]
    except Exception as e:
        print(f"Error reading coils for Unit {unit_id}: {e}")
        data['Coils'] = ['Error'] * start_addresses['coils'][1]
    
    # Read Discrete Inputs
    try:
        discrete_inputs = client.read_discrete_inputs(start_addresses['discrete_inputs'][0], start_addresses['discrete_inputs'][1])
        if discrete_inputs is not None:
            data['Discrete Inputs'] = discrete_inputs
        else:
            data['Discrete Inputs'] = ['Error'] * start_addresses['discrete_inputs'][1]
    except Exception as e:
        print(f"Error reading discrete inputs for Unit {unit_id}: {e}")
        data['Discrete Inputs'] = ['Error'] * start_addresses['discrete_inputs'][1]
    
    # Read Holding Registers
    try:
        holding_registers = client.read_holding_registers(start_addresses['holding_registers'][0], start_addresses['holding_registers'][1])
        if holding_registers is not None:
            data['Holding Registers'] = holding_registers
        else:
            data['Holding Registers'] = ['Error'] * start_addresses['holding_registers'][1]
    except Exception as e:
        print(f"Error reading holding registers for Unit {unit_id}: {e}")
        data['Holding Registers'] = ['Error'] * start_addresses['holding_registers'][1]
    
    # Read Input Registers
    try:
        input_registers = client.read_input_registers(start_addresses['input_registers'][0], start_addresses['input_registers'][1])
        if input_registers is not None:
            data['Input Registers'] = input_registers
        else:
            data['Input Registers'] = ['Error'] * start_addresses['input_registers'][1]
    except Exception as e:
        print(f"Error reading input registers for Unit {unit_id}: {e}")
        data['Input Registers'] = ['Error'] * start_addresses['input_registers'][1]
    
    return data

def display_data(units_data, unit_id, start_addresses):
    rows = []
    # Determine the maximum number of data points among all categories
    max_length = max(len(units_data['Coils']),
                    len(units_data['Discrete Inputs']),
                    len(units_data['Holding Registers']),
                    len(units_data['Input Registers']))
    
    for i in range(max_length):
        # Coils
        if i < len(units_data['Coils']):
            row_coil = {
                'Unit ID': unit_id,
                'Type': 'Coil',
                'Address': start_addresses['coils'][0] + i,
                'Value': units_data['Coils'][i]
            }
            rows.append(row_coil)
        # Discrete Inputs
        if i < len(units_data['Discrete Inputs']):
            row_di = {
                'Unit ID': unit_id,
                'Type': 'Discrete Input',
                'Address': start_addresses['discrete_inputs'][0] + i,
                'Value': units_data['Discrete Inputs'][i]
            }
            rows.append(row_di)
        # Holding Registers
        if i < len(units_data['Holding Registers']):
            row_hr = {
                'Unit ID': unit_id,
                'Type': 'Holding Register',
                'Address': start_addresses['holding_registers'][0] + i,
                'Value': units_data['Holding Registers'][i]
            }
            rows.append(row_hr)
        # Input Registers
        if i < len(units_data['Input Registers']):
            row_ir = {
                'Unit ID': unit_id,
                'Type': 'Input Register',
                'Address': start_addresses['input_registers'][0] + i,
                'Value': units_data['Input Registers'][i]
            }
            rows.append(row_ir)
    
    # Convert to tabular format
    table = []
    headers = ["Unit ID", "Type", "Address", "Value"]
    for row in rows:
        table.append([row['Unit ID'], row['Type'], row['Address'], row['Value']])
    
    print(tabulate(table, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    # Configuration
    SERVER_HOST = "127.0.0.1"  # Replace with your Modbus server IP
    SERVER_PORT = 502              # Replace with your Modbus server port if different
    UNIT_IDS = [1, 2]              # List of unit IDs you want to query
    
    # Define start addresses and quantities for each data type
    units_start_addresses = {
        'coils': (0, 10),             # (start_address, quantity)
        'discrete_inputs': (0, 10),
        'holding_registers': (0, 10),
        'input_registers': (0, 10)
    }
    
    # Initialize Modbus client
    client = ModbusClient(host=SERVER_HOST, port=SERVER_PORT, auto_open=True)
    
    if not client.is_open:  # Corrected: Removed parentheses
        if not client.open():
            print(f"Unable to connect to Modbus server at {SERVER_HOST}:{SERVER_PORT}")
            sys.exit(1)
    
    try:
        while True:
            for unit_id in UNIT_IDS:
                data = read_modbus_data(client, unit_id, units_start_addresses)
                display_data(data, unit_id, units_start_addresses)
            print("\nRefreshing data in 5 seconds...\n")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        client.close()