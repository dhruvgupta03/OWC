import serial
import time
import tkinter as tk
from tkinter import filedialog

def receive_file_via_uart(output_file_path, port, baudrate=115200):
    try:
        # Open the UART port
        ser = serial.Serial(port, baudrate, timeout=1)
        print("UART Port Opened.")
        
        with open(output_file_path, "wb") as file:
            total_bytes_received = 0
            start_time = time.time()  # Start time for rate calculation
            
            while True:
                # Read the packet header
                header = ser.read(4)  # 2 bytes for ID, 2 bytes for length
                if len(header) == 1 and header == b'\x17':
                    break
                if len(header) < 4:
                    continue  # Incomplete header
                
                packet_id = int.from_bytes(header[:2], 'big')
                data_length = int.from_bytes(header[2:], 'big')
                
                # Read the data and checksum
                data = ser.read(data_length)
                checksum = ser.read(1)
                
                if len(data) < data_length or len(checksum) < 1:
                    continue  # Incomplete data
                
                # Validate checksum
                if sum(data) % 256 == checksum[0]:
                    file.write(data)
                    total_bytes_received += len(data)
                    print(f"Received packet {packet_id}, size: {len(data)} bytes")
                    
                    # Calculate and display the reception rate
                    elapsed_time = time.time() - start_time
                    rate = total_bytes_received / elapsed_time if elapsed_time > 0 else 0
                    print(f"Data received: {total_bytes_received} bytes ({rate:.2f} B/s)")
                else:
                    print(f"Checksum mismatch for packet {packet_id}. Ignored.")
            
        print("File reception complete.")
        ser.close()
    except Exception as e:
        print(f"Error: {e}")

# Example usage
# Hide the root window
root = tk.Tk()
root.withdraw()
output_file_path = filedialog.asksaveasfilename(title="Save received file as", defaultextension="")
if output_file_path:
    print("Selected file:", output_file_path)
else:
    print("No save path selected. Exiting.")
    exit()
receive_file_via_uart(output_file_path, "COM7")
