import argparse
import subprocess
import sys

# 1. Define the external libraries your application needs
REQUIRED_PACKAGES = ["csv", "minimalmodbus", "pyserial"]

def install_dependencies():
    """Checks and installs missing packages using the current Python environment."""
    for package in REQUIRED_PACKAGES:
        try:
            # Check if the package is already installed
            __import__(package)
        except ImportError:
            print(f"[{package}] not found. Installing...")
            # Use sys.executable to ensure pip targets the internal executable environment
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
    
import tools

parser = argparse.ArgumentParser(description='Write multiple values to a modbus device.')
parser.add_argument('--dictionary', default='dict.csv', type=str, help='The path to the CSV dictionary file.')
parser.add_argument('--values', type=str, default='params.csv', help='The path to the CSV file containing values to write.')
parser.add_argument('--port', type=str, default='COM13', help='The serial port to use (default: COM13).')
parser.add_argument('--slave_address', type=int, default=1, help='The slave address of the modbus device (default: 1).')    
parser.add_argument('--baud_rate', type=int, default=9600, help='The baud rate for the serial connection (default: 9600).') 
parser.add_argument('--parity', type=str, default='N', choices=['N', 'E', 'O'], help='The parity for the serial connection (default: N).')
parser.add_argument('--timeout', type=int, default=1, help='The timeout for the serial connection in seconds (default: 1).')

if __name__ == "__main__":
    args = parser.parse_args()
    
    # Read the dictionary and values from CSV files
    dictionary = tools.read_csv_table(args.dictionary)
    values = tools.read_csv_table(args.values)

    # Connect to the Modbus device
    instrument = tools.modbus_connect(args.port, args.slave_address, args.baud_rate, args.parity, args.timeout)

    # Write values to the Modbus device
    for param, value in values:
        register_address = tools.param2address(param, dictionary)
        if register_address is not None:
            try:
                tools.write_register(instrument, register_address, float(value))
                print(f'Successfully wrote {value} to {param} (address {register_address})')
            except Exception as e:
                print(f'Error writing {value} to {param} (address {register_address}): {e}')