MB = 1024 * 1024
TS_SIZE = 188
SYNC_BYTE = 0x47

#in_filename = input('Input file name : ')
in_filename = 'TS33_Tech_epgmissing_1912_2.ts'
#to_be_removed_PID = input('To be removed PID : ')
to_be_removed_PID = [
	0x0024, 0x00C0, 3390, 3401, 3601, 3701, 4615, 4616, 5402, 5873,
	7502,
	0x1B6D, 0x1B77, 0x1B81, 0x1B8B, 0x1B95, 0x1B9F, 0x1BA9, 0x1BDB, 
	0x1BE5, 0x1BEF, 0x1BF9, 0x1C03, 0x1C0D, 0x1C17, 0x1C21, 0x1C2B,
	0x1C35, 0x1C3F, 0x1C49, 0x1C53, 0x1C5D, 0x1C67, 0x1C71, 0x1C7B,
	0x1C85, 0x1C8F, 0x1CAD, 0x1CB7, 0x1CC1, 0x1CCB, 0x1CDF, 0x1CFD, 
	0x1D11, 0x1D1B, 0x1D25, 0x1D11, 0x1FFF ]
out_filename = in_filename + '_' + 'removed.trp'

length = 0
error_count = 0
recover_failed = 0

with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
#	while length < MB * TS_SIZE:
	while True:
		data = in_file.read(TS_SIZE)
		if len(data) != TS_SIZE:
			print('end of ts')
			break
		
		if data[0] != SYNC_BYTE:
			print('sync byte error at %d' % length)
			while True:
				error_count += 1
				data = in_file.read(1)
				if data[0] == SYNC_BYTE:
					error_count = 0
					data += in_file.read(187)
					break
				if error_count > TS_SIZE:
					print('error_count : %d' % error_count)
					recover_failed = 1
					break
			
			if recover_failed == 1:
				break

		pid = ((data[1] << 8) + data[2]) & 0x1FFF
		#print(data[1], data[2], pid)
		if not pid in to_be_removed_PID:
			out_file.write(data)
		length += TS_SIZE

print('length : %d' % length)
