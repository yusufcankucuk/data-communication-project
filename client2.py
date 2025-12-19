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
    print("="*50, flush=True)
    print("Client 2 - Receiver + Error Checker", flush=True)
    print("="*50, flush=True)
    print("Waiting for data from server on port 9999...\n", flush=True)
    
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
                print("="*50, flush=True)
                print("Invalid packet format received", flush=True)
                print("="*50, flush=True)
                continue
            
            received_data, method, sent_control = parts
            
            computed_control = calculate_control_info(received_data, method)
            
            status = "DATA CORRECT" if sent_control == computed_control else "DATA CORRUPTED"
            is_corrupted = sent_control != computed_control
            
            print("\n" + "="*50, flush=True)
            print("Received Data :", received_data, flush=True)
            print("Method :", method, flush=True)
            print("Sent Check Bits :", sent_control, flush=True)
            print("Computed Check Bits :", computed_control, flush=True)
            print("Status :", status, flush=True)
            print("="*50 + "\n", flush=True)
            
    except KeyboardInterrupt:
        print("\nClient 2 shutting down...", flush=True)
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()

