MB = 1024 * 1024
TS_SIZE = 188
SYNC_BYTE = 0x47

in_filename = 'HTS_Frequency_11010_SR_32720_17May19.ts' #input('Input file name : ')
#in_filename = 'TS-03_2.ts'
out_filename = in_filename + 'EIT_count_result.txt'

EIT_PID = 0x12
PF_ACT_TID = 0x4E
PF_OTHER_TID = 0x4F
SCH_ACT_1DAY_TID = 0x50
SCH_OTHER_1DAY_TID = 0x60

length = 0
packet_number = -1

def isEit(table_id):
	if table_id == PF_ACT_TID or table_id == PF_OTHER_TID or table_id == SCH_ACT_1DAY_TID or table_id == SCH_OTHER_1DAY_TID:
		return True
	else:
		return False

pf_eit = { }
sch_eit = { }
with open(in_filename, 'rb') as in_file:
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
			
		# payload unit start indicator check	
		if ((data[1]) & 0x40) != 0x40:
			continue
		
		pid = ((data[1] << 8) + data[2]) & 0x1FFF
		#print(data[1], data[2], pid)
		if EIT_PID != pid:
			continue
			
		table_id = data[5]
		if not isEit(table_id):
			continue
		
		svc_id = (data[8] << 8) + data[9]

		version_number = (data[10] >> 1) & 0x1F
		
		section_number = data[11]
		tsid = (data[13] << 8) + data[14]
		section = (tsid, svc_id, section_number, version_number)
		
		if table_id == PF_ACT_TID or table_id == PF_OTHER_TID:		
			if section in pf_eit:
				pf_eit[section].append(packet_number)
			else:
				pf_eit[section] = []
				pf_eit[section].append(packet_number)
		else:
			if section in sch_eit:
				sch_eit[section].append(packet_number)
			else:
				sch_eit[section] = []		
				sch_eit[section].append(packet_number)
		#print('tsid:0x%x, svcid:0x%x, section number:%d' % (tsid, svc_id, section_number))


pf_eit_list = [(k,v) for k,v in pf_eit.items()]
pf_eit_list.sort()
print('present/following eit')
for element in pf_eit_list:
	print(str(element[0]) + ', num of packet:' + str(len(element[1])) + ', ' + str(element[1]))

sch_eit_list = [(k,v) for k,v in sch_eit.items()]
sch_eit_list.sort()
print('scheduled eit')
for element in sch_eit_list:
	print(str(element[0]) + ', num of packet:' + str(len(element[1])) + ', ' + str(element[1]))

