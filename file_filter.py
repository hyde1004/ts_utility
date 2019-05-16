# in_filename = 'E:/Airtel Capture/11480V_28800_20160823.TRP'
# out_filename = 'C:/Stream/11480V_28800_20160823_Partial.TRP'
MB = 1024 * 1024
TS_SIZE = 188

in_filename = input('Input file name : ')
in_PID = input('Input PID : ')
out_filename = in_filename + '_' + in_PID + '_Partial.trp'

length = 0

with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
#	while length < MB * TS_SIZE:
	while True:
		data = in_file.read(TS_SIZE)
		pid = ((data[1] << 8) + data[2]) & 0x1FFF
		#print(data[1], data[2], pid)
		if pid == int(in_PID):
			out_file.write(data)
		length += TS_SIZE
		#print(length)
