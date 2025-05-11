import serial
import time
import re

def receive_packets():
    # Configure the serial port (adjust parameters as needed)
    serial_port = 'COM7'  # Replace with your serial port, e.g., 'COM3' on Windows
    baud_rate = 9600            # Baud rate for communication
    timeout = 1                 # Timeout in seconds

    try:
        # Initialize the serial connection
        ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
        print(f"Listening on serial port: {serial_port}")

        start_time = None  # To track when the first packet was received
        correct_count = 0  # Counter for correctly received packets

        while True:
            # Read a line from the serial port
            packet = ser.readline().decode('utf-8').strip()  # Read and decode the packet
            if start_time!=None and time.time() - start_time > 7:
                    print("Reception timeout reached (7 seconds).")
                    break
            if packet:
                # Record the time when the first packet is received
                if start_time is None:
                    start_time = time.time()
                
                # Validate packet format
                if re.match(r"^Packet \d+$", packet):  # Regex to check "Packet X" format
                    print(f"Received: {packet}")
                    correct_count += 1
                    #print(correct_count)
                else:
                    print(f"Incorrect packet: {packet}")

                # Stop receiving after 7 seconds from the first packet
                

        print(f"Number of correctly received packets: {correct_count}")

    except serial.SerialException as e:
        print(f"Error: Could not open serial port: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the serial connection if it was opened
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    receive_packets()
