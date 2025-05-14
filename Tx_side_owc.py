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
            
            while bytes_sent < file_size:
                # Read a chunk of data
                data = file.read(chunk_size)
                
                # Create a packet with packet ID and checksum
                checksum = sum(data) % 256
                packet = packet_id.to_bytes(2, 'big') + len(data).to_bytes(2, 'big') + data + checksum.to_bytes(1, 'big')
                
                # Send the packet
                ser.write(packet)
                print(f"Sent packet {packet_id}, size: {len(data)} bytes")
                
                # Update counters
                packet_id += 1
                bytes_sent += len(data)
                print(f"Data sent: {bytes_sent}/{file_size} bytes")
        
        # Send end-of-transmission signal (if needed)
        ser.write(b'\x17')
        print("File transmission complete.")
        ser.close()
    except Exception as e:
        print(f"Error: {e}")

# Hide the root window
root = tk.Tk()
root.withdraw()

# Open file dialog
input_file_path = filedialog.askopenfilename(title="Select a file to send")

# Print the selected file path and call function
if input_file_path:
    print("Selected file:", input_file_path)
    send_file_via_uart(input_file_path, "COM15")
else:
    print("No file selected.")

