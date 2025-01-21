import yaml

def read_config(input_file):
    """Метод чтения параметров из конфигурационного файла."""
    with open(input_file, 'r') as file:
        file_contents = file.read()
    return yaml.safe_load(file_contents)

def print_separator():
    print("-----------------------------------------------------------------")