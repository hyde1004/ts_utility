MB = 1024 * 1024
TS_SIZE = 188
SYNC_BYTE = 0x47

in_filename = input('Input file name : ')
in_PID = input('Input PID : ')
out_filename = in_filename + '_' + in_PID + '_Partial.trp'
start_packet = 13040909
end_packet = 19863028

length = 0
error_count = 0
recover_failed = 0
packet_number = -1

with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
#	while length < MB * TS_SIZE:
	while True:
		data = in_file.read(TS_SIZE)
		packet_number += 1
		
		if len(data) != TS_SIZE:
			print('end of ts')
			break
		
		if (packet_number < start_packet or packet_number >= end_packet):
			continue
			
		if data[0] != SYNC_BYTE:
			print('sync byte error at %d' % length)
			while True:
				error_count += 1
				data = in_file.read(1)
				if data[0] == SYNC_BYTE:
					error_count = 0
					data += in_file.read(TS_SIZE-1)
					break
				if error_count > TS_SIZE:
					print('error_count : %d' % error_count)
					recover_failed = 1
					break
			
			if recover_failed == 1:
				break

		pid = ((data[1] << 8) + data[2]) & 0x1FFF
		#print(data[1], data[2], pid)
		if pid == int(in_PID):
			out_file.write(data)
		length += TS_SIZE

print('length : %d' % length)
