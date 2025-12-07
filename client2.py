import socket
from utils import parity_bit, parity_2d, crc16, hamming_control, internet_checksum

def calculate_control_info(data, method):
    method = method.upper()
    
    match method:
        case 'PARITY':
            return parity_bit(data, 'even')
        case 'PARITY2D':
            return parity_2d(data)
        case 'CRC':
            return crc16(data)
        case 'HAMMING': 
            return hamming_control(data)
        case 'CHECKSUM':
            return internet_checksum(data)
        case _:
            return ''

def main():
    print("="*50)
    print("Client 2 - Receiver + Error Checker")
    print("="*50)
    print("Waiting for data from server on port 9999...\n")
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            data = client_socket.recv(4096).decode('utf-8')
            client_socket.close()
            
            if not data:
                continue
            
            parts = data.split('|')
            if len(parts) != 3:
                print("="*50)
                print("Invalid packet format received")
                print("="*50)
                continue
            
            received_data, method, sent_control = parts
            
            computed_control = calculate_control_info(received_data, method)
            
            status = "DATA CORRECT" if sent_control == computed_control else "DATA CORRUPTED"
            
            print("\n" + "="*50)
            print("Client 2 - Received Packet")
            print("="*50)
            print("Received Data        :", received_data)
            print("Method               :", method)
            print("Sent Check Bits      :", sent_control)
            print("Computed Check Bits  :", computed_control)
            print("Status               :", status)
            print("="*50 + "\n")
            
    except KeyboardInterrupt:
        print("\nClient 2 shutting down...")
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()

