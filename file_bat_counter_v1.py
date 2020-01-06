MB = 1024 * 1024
TS_SIZE = 188
SYNC_BYTE = 0x47

#in_filename = 'TS-03_2.ts_Partial.trp' #input('Input file name : ')
in_filename = 'TS33_Tech_epgmissing_1912_2.ts'
out_filename = in_filename + 'BAT_count_result.txt'

BAT_PID = 0x11
BAT_TID = 0x4A
BOUQUET_ID_ANDROID = 0x610C


length = 0
packet_number = -1

error_count = 0
recover_failed = 0

def isBat(table_id):
	if table_id == BAT_TID:
		return True
	else:
		return False

bat_info = { }

with open(in_filename, 'rb') as in_file:
#	while length < MB * TS_SIZE:
	while True:
		packet_number += 1
		
		data = in_file.read(TS_SIZE)
		length += TS_SIZE
		
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
			
		# payload unit start indicator check	
		if ((data[1]) & 0x40) != 0x40:
			continue
		
		pid = ((data[1] << 8) + data[2]) & 0x1FFF
		#print(data[1], data[2], pid)
		if BAT_PID != pid:
			continue
			
		table_id = data[5]
		if not isBat(table_id):
			continue
		
		bouquet_id = (data[8] << 8) + data[9]
		if not bouquet_id == BOUQUET_ID_ANDROID:
			continue
			
		version_number = (data[10] >> 1) & 0x1F
		
		section_number = data[11]
		last_section_number = data[12]
		section = (bouquet_id, section_number, last_section_number, version_number)
		
		if section in bat_info:
			bat_info[section].append(packet_number)
		else:
			bat_info[section] = []
			bat_info[section].append(packet_number)
		#print('tsid:0x%x, svcid:0x%x, section number:%d' % (tsid, svc_id, section_number))
		
		length += TS_SIZE
	print("Packet number %d" % packet_number)
	
bat_list = [(k,v) for k,v in bat_info.items()]
bat_list.sort()

for element in bat_list:
	print(str(element[0]) + ', num of packet:' + str(len(element[1])) + ', ' + str(element[1]))


#with open(out_filename, 'wb') as out_file:
#	out_file.write('present/following eit')
#	for key in pf_eit:
#		out_file.write(key, pf_eit[key])
	
#	out_file.write('scheduled eit')
#	for key in sch_eit:
#		out_file.write(key, sch_eit[key])

		
#		if pid == int(EIT_PID):
#			out_file.write(data)
#		length += TS_SIZE

# print('length : %d' % length)
