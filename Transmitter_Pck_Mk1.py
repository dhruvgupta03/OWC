import serial
import time

def send_packets():
    # Configure the serial port (adjust parameters as needed)
    serial_port = 'COM5'  # Replace with your serial port, e.g., 'COM3'
    baud_rate = 9600            # Baud rate for communication
    timeout = 1                 # Timeout in seconds

    try:
        # Initialize the serial connection
        ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
        print(f"Opened serial port: {serial_port}")
 
        # Send packets from Packet 1 to Packet 10
        for i in range(1, 11):
            packet = f"Packet {i}\n"  # Append newline character to the packet
            ser.write(packet.encode('utf-8'))  # Encode the string into bytes and send
            print(f"Sent: {packet.strip()}")
            time.sleep(0.5)  # Wait for 0.5 seconds before sending the next packet

        print("All packets sent!")

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
    send_packets()
