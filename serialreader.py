import serial
import re

def read_last_two_numbers(port='/dev/ttyACM0', baud_rate=9600):
    try:
        # Open the serial port
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {port} at {baud_rate} baud rate.")
        
        while True:
            if ser.in_waiting > 0:
                # Read a line from the serial port
                data = ser.readline().rstrip()
                print(f"Received data: {data}")
                
                # Extract all numbers from the data using regular expressions
                numbers = data
                
                
                return data
    
    except serial.SerialException as e:
        print(f"Error: {e}")
    
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

# Example usage:
result = read_last_two_numbers()
print(f"Last two numbers: {result}")
