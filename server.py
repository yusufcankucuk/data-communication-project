import socket
import random
import threading

def bit_flip(data):
    binary = ''.join(format(ord(c), '08b') for c in data)
    if not binary:
        return data
    
    pos = random.randint(0, len(binary) - 1)
    flipped = list(binary)
    flipped[pos] = '1' if flipped[pos] == '0' else '0'
    
    result = ''
    for i in range(0, len(flipped), 8):
        byte = ''.join(flipped[i:i+8])
        if len(byte) == 8:
            result += chr(int(byte, 2))
    
    return result

def character_substitution(data):
    if not data:
        return data
    pos = random.randint(0, len(data) - 1)
    new_char = chr(random.randint(33, 126))
    return data[:pos] + new_char + data[pos+1:]

def character_deletion(data):
    if len(data) <= 1:
        return data
    pos = random.randint(0, len(data) - 1)
    return data[:pos] + data[pos+1:]

def character_insertion(data):
    if not data:
        return chr(random.randint(33, 126))
    pos = random.randint(0, len(data))
    new_char = chr(random.randint(33, 126))
    return data[:pos] + new_char + data[pos:]

def character_swapping(data):
    if len(data) < 2:
        return data
    pos = random.randint(0, len(data) - 2)
    chars = list(data)
    chars[pos], chars[pos+1] = chars[pos+1], chars[pos]
    return ''.join(chars)

def multiple_bit_flips(data):
    binary = ''.join(format(ord(c), '08b') for c in data)
    if not binary:
        return data
    
    num_flips = random.randint(2, min(5, len(binary)))
    flipped = list(binary)
    positions = random.sample(range(len(binary)), num_flips)
    
    for pos in positions:
        flipped[pos] = '1' if flipped[pos] == '0' else '0'
    
    result = ''
    for i in range(0, len(flipped), 8):
        byte = ''.join(flipped[i:i+8])
        if len(byte) == 8:
            result += chr(int(byte, 2))
    
    return result

def burst_error(data):
    if len(data) < 3:
        return data
    
    start = random.randint(0, max(0, len(data) - 3))
    length = random.randint(3, min(8, len(data) - start))
    
    corrupted = list(data)
    for i in range(start, start + length):
        corrupted[i] = chr(random.randint(33, 126))
    
    return ''.join(corrupted)

def inject_error(data, error_type=None):
    if error_type is None:
        error_type = random.choice([1, 2, 3, 4, 5, 6, 7])
    
    error_methods = {
        1: ("Bit Flip", bit_flip),
        2: ("Character Substitution", character_substitution),
        3: ("Character Deletion", character_deletion),
        4: ("Character Insertion", character_insertion),
        5: ("Character Swapping", character_swapping),
        6: ("Multiple Bit Flips", multiple_bit_flips),
        7: ("Burst Error", burst_error)
    }
    
    method_name, method_func = error_methods.get(error_type, ("Character Substitution", character_substitution))
    corrupted = method_func(data)
    return corrupted, method_name

def handle_client(client_socket, addr):
    try:
        data = client_socket.recv(4096).decode('utf-8')
        if not data:
            return
        
        parts = data.split('|')
        if len(parts) != 3:
            print("="*50, flush=True)
            print("Invalid packet format from", addr, flush=True)
            print("="*50, flush=True)
            client_socket.close()
            return
        
        original_data, method, control_info = parts
        
        should_corrupt = random.random() < 0.75
        
        if should_corrupt:
            corrupted_data, error_method = inject_error(original_data)
        else:
            corrupted_data = original_data
        
        packet = f"{corrupted_data}|{method}|{control_info}"
        
        client2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2_socket.connect(('localhost', 9999))
        client2_socket.sendall(packet.encode('utf-8'))
        client2_socket.close()
        
    except Exception as e:
        print("="*50, flush=True)
        print("Error handling client", addr, ":", e, flush=True)
        print("="*50, flush=True)
    finally:
        client_socket.close()

def main():
    print("="*50, flush=True)
    print("Server - Intermediate Node + Data Corruptor", flush=True)
    print("="*50, flush=True)
    print("Listening on port 8888 for Client 1...", flush=True)
    print("Forwarding to Client 2 on port 9999...\n", flush=True)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(5)
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...", flush=True)
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()

