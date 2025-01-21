import json

def int_to_bytes(m):
    """Метод конфертации чисел в байты"""
    hex_str = hex(m)[2:]
    if len(hex_str) % 2:
        hex_str = '0' + hex_str
    return bytes.fromhex(hex_str)

def read_config(file_path):
    """Метод чтения параметров из конфигурационного файла."""
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config['N'], config['e'], config['ciphertexts']

