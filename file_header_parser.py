import argparse

TS_SIZE = 188
SYNC_BYTE = 0x47

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-file', dest="in_filename", action='store')
args = parser.parse_args()

# in_filename = input('Input file name : ')

in_filename = args.in_filename
with open(in_filename, 'rb') as in_file:
    packet_number = 0
    while True:
        data = in_file.read(TS_SIZE)
        if len(data) != TS_SIZE:
            print('end of ts')
            break

        if packet_number >= 10000:
            break

        transport_error_indicator = (data[1] & 0x80) >> 7
        payload_unit_start_indicator = (data[1] & 0x40) >> 6
        transport_priority = (data[1] & 0x20) >> 5
        pid = ((data[1] << 8) + data[2]) & 0x1FFF
        transport_scrambling_control = (data[3] & 0xC0) >> 6
        adaptation_field_control = (data[3] & 0x30) >> 4
        continuity_counter = data[3] & 0x0F

        print("Header : {:02X} {:02X} {:02X} {:02X}".format(data[0], data[1], data[2], data[3]))
        print("\tpacket number : ", packet_number)
        print("\tsync byte : ", hex(data[0]))
        print("\ttransport error indicator : ", bin(transport_error_indicator))
        print("\tpayload unit start indicator : ", bin(payload_unit_start_indicator))
        print("\ttransport_priority : ", bin(transport_priority))
        print("\tpid : 0x{:04X}".format(pid))
        print("\ttransport scrambling control : ", bin(transport_scrambling_control))
        print("\tadaptation field control : ", bin(adaptation_field_control))
        print("\tcontinuity counter : ", hex(continuity_counter))
        print("")

        packet_number += 1
