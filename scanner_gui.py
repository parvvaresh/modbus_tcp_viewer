import tkinter as tk
from tkinter import ttk
from pyModbusTCP.client import ModbusClient
import time
import sys

class ModbusGUI:
    def __init__(self, root, server_host, server_port, unit_ids, start_addresses, refresh_interval=1000):
        self.root = root
        self.server_host = server_host
        self.server_port = server_port
        self.unit_ids = unit_ids
        self.start_addresses = start_addresses
        self.refresh_interval = refresh_interval  # in milliseconds

        # Initialize Modbus client
        self.client = ModbusClient(host=self.server_host, port=self.server_port, auto_open=True)
        if not self.client.is_open:
            if not self.client.open():
                print(f"Unable to connect to Modbus server at {self.server_host}:{self.server_port}")
                sys.exit(1)

        # Create main notebook for devices
        self.device_notebook = ttk.Notebook(root)
        self.device_notebook.pack(expand=1, fill='both')

        # Dictionary to hold references to Treeviews for easy updates
        self.treeviews = {}

        # Create tabs for each device
        for unit_id in self.unit_ids:
            device_frame = ttk.Frame(self.device_notebook)
            self.device_notebook.add(device_frame, text=f"Unit {unit_id}")

            # Create a sub-notebook for data types within the device tab
            data_notebook = ttk.Notebook(device_frame)
            data_notebook.pack(expand=1, fill='both')

            # Initialize treeviews for each data type
            self.treeviews[unit_id] = {}

            for data_type in ['Coils', 'Discrete Inputs', 'Holding Registers', 'Input Registers']:
                type_frame = ttk.Frame(data_notebook)
                data_notebook.add(type_frame, text=data_type)

                # Create Treeview
                tree = ttk.Treeview(type_frame, columns=('Address', 'Value'), show='headings')
                tree.heading('Address', text='Address')
                tree.heading('Value', text='Value')
                tree.column('Address', width=100, anchor='center')
                tree.column('Value', width=100, anchor='center')

                # Add vertical scrollbar
                scrollbar = ttk.Scrollbar(type_frame, orient="vertical", command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.pack(side='right', fill='y')
                tree.pack(expand=1, fill='both')

                # Store treeview reference
                self.treeviews[unit_id][data_type] = tree

        # Start the periodic update
        self.update_data()

    def read_modbus_data(self, client, unit_id, start_addresses):
        data = {}
        # Set the unit ID
        client.unit_id = unit_id
        
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

    def update_table(self, tree, data, start_address, data_type):
        # Clear the existing table
        for item in tree.get_children():
            tree.delete(item)
        
        # Populate with new data
        for idx, value in enumerate(data):
            address = start_address + idx
            # Handle boolean values for Coils and Discrete Inputs
            if data_type in ['Coils', 'Discrete Inputs']:
                value_str = 'ON' if value else 'OFF'
            else:
                value_str = str(value)
            tree.insert('', 'end', values=(address, value_str))

    def update_data(self):
        for unit_id in self.unit_ids:
            data = self.read_modbus_data(self.client, unit_id, self.start_addresses)
            for data_type in ['Coils', 'Discrete Inputs', 'Holding Registers', 'Input Registers']:
                tree = self.treeviews[unit_id][data_type]
                data_values = data.get(data_type, [])
                start_addr, _ = self.start_addresses[self.get_data_key(data_type)]
                self.update_table(tree, data_values, start_addr, data_type)
        # Schedule the next update
        self.root.after(self.refresh_interval, self.update_data)

    def get_data_key(self, data_type):
        """Helper method to map display names to keys."""
        mapping = {
            'Coils': 'coils',
            'Discrete Inputs': 'discrete_inputs',
            'Holding Registers': 'holding_registers',
            'Input Registers': 'input_registers'
        }
        return mapping.get(data_type, '')

def main():
    # Configuration
    SERVER_HOST = "127.0.0.1"  # Replace with your Modbus server IP
    SERVER_PORT = 502              # Replace with your Modbus server port if different
    UNIT_IDS = [1, 2]               # List of unit IDs you want to query
    
    # Define start addresses and quantities for each data type
    start_addresses = {
        'coils': (0, 10),             # (start_address, quantity)
        'discrete_inputs': (0, 10),
        'holding_registers': (0, 10),
        'input_registers': (0, 10)
    }

    # Initialize Tkinter root
    root = tk.Tk()
    root.title("Modbus Live Data Viewer")
    root.geometry("600x400")  # Set a default size; can be adjusted as needed

    # Create the Modbus GUI application
    app = ModbusGUI(root, SERVER_HOST, SERVER_PORT, UNIT_IDS, start_addresses, refresh_interval=1000)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()