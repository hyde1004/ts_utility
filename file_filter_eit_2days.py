MB = 1024 * 1024
TS_SIZE = 188
SYNC_BYTE = 0x47

#in_filename = 'HTS_Frequency_11010_SR_32720_17May19.ts' #input('Input file name : ')
in_filename = 'TS-03_2.ts'
#in_filename = 'TS-03_2.ts_Partial.trp'
out_filename = in_filename + 'Skip2Days.ts'

EIT_PID = 0x12
PF_ACT_TID = 0x4E
PF_OTHER_TID = 0x4F
SCH_ACT_1DAY_TID = 0x50
SCH_OTHER_1DAY_TID = 0x60
SECTION_NUMBER_UNTIL_2_DAYS = 120
length = 0
packet_number = -1

def isEit(table_id):
	if table_id == PF_ACT_TID or table_id == PF_OTHER_TID or table_id == SCH_ACT_1DAY_TID or table_id == SCH_OTHER_1DAY_TID:
		return True
	else:
		return False

pf_eit = { }
sch_eit = { }
skip = False
with open(in_filename, 'rb') as in_file, open(out_filename, 'wb') as out_file:
#	while length < MB * TS_SIZE:
	while True:
		packet_number += 1
		
		data = in_file.read(TS_SIZE)
		if len(data) != TS_SIZE:
			print('end of ts')
			break
		
		if data[0] != SYNC_BYTE:
			print('sync byte error')
			break
			
		pid = ((data[1] << 8) + data[2]) & 0x1FFF
		#print(data[1], data[2], pid)

		# payload unit start indicator check	
		start_indicator = ((data[1]) & 0x40) == 0x40
		
		table_id = data[5]
				
		svc_id = (data[8] << 8) + data[9]

		version_number = (data[10] >> 1) & 0x1F
		
		section_number = data[11]

		new_data = bytearray(data)
		if pid == EIT_PID:
			if start_indicator:
				if section_number > SECTION_NUMBER_UNTIL_2_DAYS:
					new_data[2] = new_data[2] | 0x1F
					new_data[3] = 0xFF
					skip = True
					print('packet:' + str(packet_number))
				else:
					skip = False
			else:
				if skip == True:
					new_data[2] = new_data[2] | 0x1F
					new_data[3] = 0xFF
					print('packet:' + str(packet_number))

			
		out_file.write(new_data)





