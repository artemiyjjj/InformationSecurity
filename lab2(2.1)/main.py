from rsa import decrypt_block, calculate_phi, find_d_component
from ferma import ferma_attack
from io_utils import int_to_bytes, read_config

def decrypt_ciphertexts(N, e, ciphertexts, p, q):
    """Дешифрует список шифротекстов и возвращает расшифрованные байты."""
    bytes = []
    phi = calculate_phi(p, q)
    print(f'Результат вычисления функции Эйлера: {phi}')
    d = find_d_component(e, phi)
    print(f'Результат вычисления параметра d: {d}\n')

    for c in ciphertexts:
        decrypted_block = decrypt_block(d, c, N)
        bytes.append(int_to_bytes(decrypted_block))

    decrypted_bytes = b''.join(bytes)
    return decrypted_bytes

def main():
    N, e, ciphertexts = read_config('config.json')
    p, q = ferma_attack(N)
    
    print("Результат факторизации Ферма:")
    print(f"p = {p}, q = {q}\n")
    decrypted_bytes = decrypt_ciphertexts(N, e, ciphertexts, p, q)
    try:
        plaintext = decrypted_bytes.decode('cp1251')
        print("Расшифрованный текст:")
        print(plaintext)
    except UnicodeDecodeError:
        print("Ошибка декодирования сообщения:",)
        print(decrypted_bytes)

if __name__ == "__main__":
    main()
