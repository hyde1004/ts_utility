# in_filename = 'E:/Airtel Capture/11480V_28800_20160823.TRP'
# out_filename = 'C:/Stream/11480V_28800_20160823_Partial.TRP'
MB = 1024 * 1024

in_filename = input('Input file name : ')
out_filename = in_filename + '_Partial.trp'
out_file_size = input('Output file size (MB) : ')

length = 0

with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
	while length < int(out_file_size)*MB:
		data = in_file.read(MB)
		out_file.write(data)
		length += MB
