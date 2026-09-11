import csv
import minimalmodbus
import serial  

def read_csv_table(filepath):
    table = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            table.append(row)
    
    return table

def modbus_connect(port, slave_address, baud_rate=9600, parity=serial.PARITY_NONE, timeout=1):
    instrument = minimalmodbus.Instrument(port, slave_address)
    instrument.serial.baudrate = baud_rate
    instrument.serial.parity = parity
    instrument.mode = minimalmodbus.MODE_RTU  # Use RTU mode
    instrument.serial.timeout = timeout
    return instrument

def write_register(instrument, register_address, value):
    """
    Write a value to a specific register of a Modbus device.
    
    Args:
        instrument (minimalmodbus.Instrument): The Modbus instrument instance
        register_address (int): The address of the register to write to
        value (int or float): The value to write to the register
    """
    try:
        instrument.write_register(register_address, value)
    except Exception as e:
        print(f'Error writing to Modbus device: {e}')

def param2address(parameter_name, dictionary):
    for row in dictionary:
        if row[0] == parameter_name:
            return int(row[1])  # Assuming the address is in the second column
    return None