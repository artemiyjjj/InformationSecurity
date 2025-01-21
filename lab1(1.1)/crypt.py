import enum
import sys
import re

class Language(enum.Enum):
    en = 1
    ru = 2
Language.ru.amount = 32 # без "ё"
Language.en.amount = 26

def get_ru_alpha():
    return list(map(chr, range(ord('а'), ord('я') + 1)))

def get_en_alpha():
    return list(map(chr, range(ord('a'), ord('z') + 1)))

def get_crypt_list(key: str, offset:int, language: Language) -> dict[str, str]:
    alphabet: list[str]
    match_table: dict[str, str]
    values: list[str] = []

    assert(len(key) <= language.amount)
    match language:
        case Language.en:
            alphabet = get_en_alpha()
            values.extend(list(key))
            [values.append(char) for char in alphabet if char not in values]
            pre_values = values[:language.amount - offset]
            post_values = values[language.amount - offset:]
            values = post_values + pre_values
            match_table = {alphabet[i]: values[i] for i in range(language.amount)}
        case Language.ru:
            alphabet = get_ru_alpha()
            values.extend(list(key))
            [values.append(char) for char in alphabet if char not in values]
            pre_values = values[:language.amount - offset]
            post_values = values[language.amount - offset:]
            values = post_values + pre_values
            match_table = {alphabet[i]: values[i] for i in range(language.amount)}
        case _:
            raise ValueError("Can not create encryption table for language {0}", language.name)     
    # print(pre_values)
    # print(post_values)
    # print(match_table)
    return match_table

def encrypt(key:str, word_split: list[str], language: Language, offset: int = 3):
    encrypted_word_list = []
    crypt_dict = get_crypt_list(key, offset, language)
    [encrypted_word_list.append(crypt_dict.get(word_split[i])) for i in range(len(word_split))]
    print(key)
    print(word_split)
    print(encrypted_word_list)

def decrypt(key:str, word_split: list[str], language: Language, offset: int = 3):
    decrypted_word_list = []
    crypt_dict = get_crypt_list(key, offset, language)
    decrypt_dict = dict((v,k) for k,v in crypt_dict.items())
    [decrypted_word_list.append(decrypt_dict.get(word_split[i])) for i in range(len(word_split))]
    print(key)
    print(word_split)
    print(decrypted_word_list)


def help():
    print("\
Ceasar method for encryption and decryption of a string\n\
Usage: crypt.py mode [key] [offset] [word]\n\
Mode: one of:\n\
\thelp - show information about the usage, alaviable parameters\n\
\tencrypt - encrypt word provided in 'word' parameter with provided 'offset' value, 'word' and 'offset'  must be provided.\n\
\tdecrypt - decrypt word provided in 'word' parameter with provided 'offset' value, 'word' and 'offset'  must be provided.\n\
")


def get_language(word: str) -> Language:
    def get_ru_regexp(length: int):
        return '[А-Яа-я_]{%s}'%length
    def get_en_regexp(length: int):
        return '[A-Za-z_]{%s}'%length

    reg_res_ru = re.fullmatch(get_ru_regexp(len(word)), word)
    reg_res_en = re.fullmatch(get_en_regexp(len(word)), word)
    # print(reg_res_ru)
    # print(reg_res_en)
    if reg_res_ru is not None:
        return Language.ru
    elif reg_res_en is not None:
        return Language.en
    else:
        raise ValueError("Provided word contains symbols from unsupported languages or special characters")

def get_and_validate_params(program_params: list = sys.argv) -> (str, list[str], int, Language):
    offset: int
    language_key: Language
    language_word: Language
    key: str
    word: str
    word_split: list[str]

    key = sys.argv[2].lower()
    if len(set(key)) != len(key):
        raise ValueError("Key should contain unique characters")
    if sys.argv[3].isdigit():
        offset = int(sys.argv[3])
    else:
        raise ValueError("Offset should be integer")
    word = sys.argv[4]
    word_split = list(word.replace(" ", "_").lower())
    # [word_split.append(char) for char in word if char.isalpha() or char == "_"]
    # if len(word) != len(word_split):
    #     raise ValueError("Provided word contains non alphabetic symbols")

    language_key = get_language(key)
    language_word = get_language(word)
    if language_key is not language_word:
        raise ValueError("Key and word languages are different")
    return (key, word_split, offset, language_key)

mode: str
offset: int
word_split: list[str]
language: Language

try:
    mode = sys.argv[1]
    match mode:
        case "encrypt":
            key, word_split, offset, language = get_and_validate_params(sys.argv)
            encrypt(key=key, word_split=word_split, language=language, offset=offset)
        case "decrypt":
            key, word_split, offset, language = get_and_validate_params(sys.argv)
            decrypt(key=key, word_split=word_split, language=language, offset=offset)
        case "help":
            help()
        case _:
            print("Unsupported 'mode' parameter provided")
            help()
except IndexError:
    print("Mode parameter is not provided")
    help()
except ValueError as e:
    print(e)
