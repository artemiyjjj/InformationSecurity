import sys

import alphabet
from io_utils import read_config, print_separator
from curve import Curve
from point import Point

def main():
    curve = Curve(-1, 1, 751)

    if len(sys.argv) < 2:
        print("Укажите название файла с параметрами!")
        return

    input_file = None
    for i in range(1, len(sys.argv)):
        if sys. argv[i] == '-f' and i + 1 < len(sys.argv):
            input_file = sys.argv[i + 1]

    doc = read_config(input_file)
    secret_key = doc["n"]
    curve_list = doc["cyphertext"]

    decrypted_text: str = ""
    for pair in curve_list:
        kg = Point(pair["p1"]["x"], pair["p1"]["y"])
        crypted = Point(pair["p2"]["x"], pair["p2"]["y"])

        print(f"Зашифрованная точка {kg}, {crypted}")

        decrypted = curve.elliptic_add(crypted, curve.elliptic_mul(curve.elliptic_neg(kg), secret_key))

        letter = [letter for letter, point in alphabet.ALPHABET.items() if point == decrypted]
        if len(letter) > 0:
            decrypted_text += letter[0]
            print(f"Расшифрованый символ {letter}")
        print_separator()

    print(f"Расшифрованный текст: \"{decrypted_text}\"")

if __name__ == "__main__":
    main()
