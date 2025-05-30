import serial
import time
import os
import tkinter as tk
from tkinter import filedialog

def send_file_via_uart(file_path, port, baudrate=115200, chunk_size=1024):
    try:
        # Open the UART port
        ser = serial.Serial(port, baudrate, timeout=1)
        print("UART Port Opened.")
        
        # Read the file size
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size} bytes")
        
        with open(file_path, "rb") as file:
            packet_id = 0
            bytes_sent = 0
            start_time = time.time()  # Start time for rate calculation
            
            while bytes_sent < file_size:
                # Read a chunk of data
                data = file.read(chunk_size)
                
                # Create a packet with packet ID and checksum
                checksum = sum(data) % 256
                packet = packet_id.to_bytes(2, 'big') + len(data).to_bytes(2, 'big') + data + checksum.to_bytes(1, 'big')
                
                # Send the packet
                ser.write(packet)
                print(f"Sent packet {packet_id}, size: {len(data)} bytes")
                
                # Update counters without waiting for ACK
                packet_id += 1
                bytes_sent += len(data)
                
                # Calculate and display the transfer rate
                elapsed_time = time.time() - start_time
                rate = bytes_sent / elapsed_time if elapsed_time > 0 else 0
                print(f"Data sent: {bytes_sent}/{file_size} bytes ({rate:.2f} B/s)")
        
        # Send end-of-transmission signal (if needed)
        ser.write(b'\x17')
        print("File transmission complete.")
        ser.close()
    except Exception as e:
        print(f"Error: {e}")

# Example usage
# Hide the root window
root = tk.Tk()
root.withdraw()

# Open file dialog
input_file_path = filedialog.askopenfilename(title="Select a file to send")

# Print the selected file path
if input_file_path:
    print("Selected file:", input_file_path)
    send_file_via_uart(input_file_path, "COM5")
else:
    print("No file selected.")

