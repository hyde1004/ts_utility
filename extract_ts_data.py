import os
import struct


class ExtractData:
    def __init__(self, input_string):
        hex_values = []

        if input_string is not None:
            strip_string = ''.join(
                input_string.split())
            # https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string-in-python
            for i in range(0, len(strip_string) - 1, 2):
                hex_value = int(strip_string[i:i + 2], 16)
                hex_values.append(hex_value)

        self.buffer = hex_values

    def set_buffer(self, input_string):
        hex_values = []

        if input_string is not None:
            strip_string = ''.join(
                input_string.split())
            # https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string-in-python
            for i in range(0, len(strip_string) - 1, 2):
                hex_value = int(strip_string[i:i + 2], 16)
                hex_values.append(hex_value)

        self.buffer = hex_values

    def write(self, output_file_name):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/' + output_file_name, 'wb') as bin_file:
            for byte in self.buffer:
                # https://stackoverflow.com/questions/18367007/python-how-to-write-to-a-binary-file
                bin_file.write(struct.pack('B', byte))


if __name__ == "__main__":
    dst_raw_string = '''
0000 B09D 0016 FB00 0000 00E0 1008 9DE1
F408 A0E3 2008 A1E3 8408 C3F0 CC08 B2EA
2808 C7F2 5C08 C9F3 2408 CAF3 8808 CEF5
1808 CFF5 7C08 BCF5 5408 D9F9 6408 DAF9
C808 DBFA 2C08 BAED 4808 9AE0 C808 9CE1
9008 9EE2 5808 9FE2 BC08 CCF4 5008 A4E4
B008 A7E5 DC08 A8E6 4008 ABE7 6C08 ACE7
D008 B1E9 C408 B0E9 6008 B3EA 8C08 B4EA
F008 BBED AC08 A5E5 1408 ADE8 3408 B5EB
5408 A9E6 A417 86F7 8608 A3E3 E8                                      
                                           
    '''
    binary_output = ExtractData(None)

    binary_output.set_buffer(dst_raw_string)
    binary_output.write('dst.bin')
