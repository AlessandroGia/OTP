from argparse import ArgumentParser
from random import randint 
from struct import pack
from sys import exit


class OTP:

    def __init__(self) -> None:
        pass

    @staticmethod
    def __read(file: str) -> None:
        try:
            with open(file, "rb") as f:
                return bytearray(f.read())
        except Exception as e:
            exit("Error while reading file: {}.".format(e))

    @staticmethod
    def __write(file: str, byte_array: bytearray):
        try:
            with open(file, "wb") as f:
                f.write(byte_array)
        except Exception as e:
            exit("Error while writing file: {}.".format(e))

    @staticmethod
    def __create_key_array(ln_key: int) -> bytearray:
        return bytearray([randint(0, 255) for x in range(ln_key)])

    @staticmethod
    def __xor(file_byte_array: bytearray, key_array: bytearray) -> bytearray:
       return bytearray([byte ^ key_array[i] for i, byte in enumerate(file_byte_array)])
    

    def encode(self, file: str, output: str) -> None:
        file_byte_array = self.__read(file)
        key_array = self.__create_key_array(len(file_byte_array))
        new_byte_array = self.__xor(file_byte_array, key_array)
        self.__write(file, new_byte_array)
        key_array = [pack('B', x) for x in key_array]
        key = bytes()
        for k in key_array: key += k
        self.__write(output, key)
        print("{} encrypted.".format(file))
        print("Key written in: {}.".format(output))


    def decode(self, file: str, key: str):
        file_byte_array = self.__read(file)
        key_array = self.__read(key)
        if len(file_byte_array) != len(key_array):
            exit("Key doesn't match file.")
        new_byte_array = self.__xor(file_byte_array, key_array)
        self.__write(file, new_byte_array)
        print("{} decrypted.".format(file))

if __name__ == '__main__':
    parser = ArgumentParser(description="One Time Padding.")
    parser.add_argument('-f', '--file', action='store', required=True, dest='file', help='File to Encrypt/Decrypt.')
    parser.add_argument('-o', '--output', action='store', required=False, dest='output', default=None,  help='File output for the key.')
    parser.add_argument('-k', '--key', action='store', required=False, dest='key', default=None, help='Key file to decrypt the given file.')
    parser.add_argument('-e', '--encode', action='store_true', required=False, default=False, dest='encode', help='Encrypt the file with a random key.')
    parser.add_argument('-d', '--decode', action='store_true', required=False, default=False, dest='decode', help='Decrypt the file with the given key.')
    args = parser.parse_args()

    if not args.encode and not args.decode:
        exit('You have to choice a mode: -e or -d.')
    if args.encode and args.decode:
        exit('You have to choice just one mode.')
    if args.encode and not args.output:
        exit('You have to specify the output file.')
    if args.decode and not args.key:
        exit('You have to specify the key file.')
    
    otp = OTP()
    otp.decode(args.file, args.key) if args.decode else otp.encode(args.file, args.output)
    