import random
import re

def print_as_c(random_bytes):
    # number of bytes to print per line
    chunk_size = 8
    # first convert to chunks of bytes
    chunks = [random_bytes[index:index+chunk_size] for index in range(0, len(random_bytes), chunk_size)]
    chunck_len = len(chunks)
    print(chunks)  # todo:test
    indent = 4
    for index, chunk in enumerate(chunks):
        print(' ' * indent, end='')
        for byte in chunk:
            print(f'{byte}, ', end='')
        if index == chunck_len - 1:
            print('')
        else:
            print('\\')


def get_non_zero_byte():
    non_zero_val = random.randint(1, 255)
    return f'{non_zero_val:02x}'


def main(nbytes: int = 64, non_zero: bool = False):
    random_bytes_string = str(random.randbytes(nbytes).hex())
    # split string into bytes
    random_bytes = re.findall('..', random_bytes_string)
    print(f'{random_bytes=}')  # todo:test
    # replace zeroes
    if non_zero:
        random_bytes = [byte if byte != '00' else get_non_zero_byte() for byte in random_bytes]

    print(f'{random_bytes=}')  # todo:test
    print_as_c(random_bytes)


if __name__ == '__main__':
    main(64, non_zero=True)
