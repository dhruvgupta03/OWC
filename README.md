# OWC
This project is for transmitting and receiving over an OWC channel. The data is sent using a serial port (USB). We use a USB to UART convertor after that. The UART signals are then used for Intensity Modulation of Laser
The Transmitter_Pck_Mk1.py and Receiver_Pck_Mk1.py files are to show transfer of 10 sample packets from one node to another. More of a initial test experiment and Proof of Concept
The Tx_side_v3.py and Rx_side_v1.py are working codes for transmitting files from UART to UART. They haven't worked for OWC yet probably because one of the receivers is defunct and ACK can't come in. 
Next objective if to write a pair of codes which will not use Acknowledgement.
