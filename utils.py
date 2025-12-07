import random

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def parity_bit(text, parity_type='even'):
    binary = text_to_binary(text)
    ones_count = binary.count('1')
    if parity_type == 'even':
        parity = '0' if ones_count % 2 == 0 else '1'
    else:
        parity = '1' if ones_count % 2 == 0 else '0'
    return parity

def parity_2d(text, rows=8, cols=8):
    binary = text_to_binary(text)
    total_bits = rows * cols
    if len(binary) < total_bits:
        binary = binary.ljust(total_bits, '0')
    elif len(binary) > total_bits:
        binary = binary[:total_bits]
    
    matrix = []
    for i in range(rows):
        row = binary[i*cols:(i+1)*cols]
        matrix.append(list(row))
    
    row_parities = []
    for row in matrix:
        ones = row.count('1')
        row_parities.append('1' if ones % 2 == 1 else '0')
    
    col_parities = []
    for j in range(cols):
        ones = sum(1 for row in matrix if row[j] == '1')
        col_parities.append('1' if ones % 2 == 1 else '0')
    
    return ''.join(row_parities) + ''.join(col_parities)

def crc8(data):
    polynomial = 0x07
    crc = 0
    for byte in data.encode('utf-8'):
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFF
    return format(crc, '02X')

def crc16(data):
    polynomial = 0x1021
    crc = 0xFFFF
    for byte in data.encode('utf-8'):
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF
    return format(crc, '04X')

def crc32(data):
    polynomial = 0xEDB88320
    crc = 0xFFFFFFFF
    for byte in data.encode('utf-8'):
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
    crc ^= 0xFFFFFFFF
    return format(crc, '08X')

def hamming_encode_block(block):
    if len(block) < 4:
        block = block.ljust(4, '0')
    elif len(block) > 4:
        block = block[:4]
    
    data_bits = [int(bit) for bit in block]
    
    p1 = data_bits[0] ^ data_bits[1] ^ data_bits[3]
    p2 = data_bits[0] ^ data_bits[2] ^ data_bits[3]
    p4 = data_bits[1] ^ data_bits[2] ^ data_bits[3]
    
    encoded = [p1, p2, data_bits[0], p4, data_bits[1], data_bits[2], data_bits[3]]
    return ''.join(str(bit) for bit in encoded)

def hamming_code(text):
    binary = text_to_binary(text)
    encoded_blocks = []
    for i in range(0, len(binary), 4):
        block = binary[i:i+4]
        encoded_blocks.append(hamming_encode_block(block))
    return ''.join(encoded_blocks)

def hamming_decode(encoded_bits):
    if len(encoded_bits) < 7:
        return None
    bits = [int(b) for b in encoded_bits[:7]]
    
    p1 = bits[0]
    p2 = bits[1]
    p4 = bits[3]
    
    c1 = p1 ^ bits[2] ^ bits[4] ^ bits[6]
    c2 = p2 ^ bits[2] ^ bits[5] ^ bits[6]
    c4 = p4 ^ bits[4] ^ bits[5] ^ bits[6]
    
    error_pos = c1 + 2*c2 + 4*c4
    
    if error_pos > 0:
        bits[error_pos - 1] ^= 1
    
    return ''.join(str(bits[i]) for i in [2, 4, 5, 6])

def hamming_control(text):
    binary = text_to_binary(text)
    check_bits = []
    for i in range(0, len(binary), 4):
        block = binary[i:i+4]
        if len(block) < 4:
            block = block.ljust(4, '0')
        encoded = hamming_encode_block(block)
        check_bits.append(encoded[:3])
    return ''.join(check_bits)

def internet_checksum(data):
    if len(data) % 2 == 1:
        data += '\x00'
    
    checksum = 0
    for i in range(0, len(data), 2):
        word = (ord(data[i]) << 8) + ord(data[i+1])
        checksum += word
        if checksum > 0xFFFF:
            checksum = (checksum & 0xFFFF) + 1
    
    checksum = ~checksum & 0xFFFF
    return format(checksum, '04X')

