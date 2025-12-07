import socket
from utils import parity_bit, parity_2d, crc16, hamming_control, internet_checksum

def generate_control_info(data, method):
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
    print("Client 1 - Data Sender")
    print("="*50)
    print("\nAvailable Methods:")
    print("1. PARITY - Parity bit")
    print("2. PARITY2D - 2D Parity")
    print("3. CRC - Cyclic Redundancy Check")
    print("4. HAMMING - Hamming code")
    print("5. CHECKSUM - Internet Checksum (IP checksum)")
    
    text = input("\nEnter text to send: ")
    if not text:
        print("Error: Empty input")
        return
    
    print("\nSelect method (1-5): ", end='')
    choice = input().strip()
    
    method_map = {
        '1': 'PARITY',
        '2': 'PARITY2D',
        '3': 'CRC',
        '4': 'HAMMING',
        '5': 'CHECKSUM'
    }
    
    method = method_map.get(choice, 'CRC')
    control_info = generate_control_info(text, method)
    
    packet = f"{text}|{method}|{control_info}"
    
    print("\n" + "="*50)
    print("Generated Packet     :", packet)
    print("Data                 :", text)
    print("Method               :", method)
    print("Control Information  :", control_info)
    print("="*50)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8888))
        sock.sendall(packet.encode('utf-8'))
        sock.close()
        print("\nPacket sent to server successfully!")
    except Exception as e:
        print(f"\nError sending packet: {e}")

if __name__ == '__main__':
    main()

