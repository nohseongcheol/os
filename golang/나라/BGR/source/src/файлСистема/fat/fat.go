package fat

import . "util"
import . "console"
import . "driver/ata"
import . "файлСистема/msdospartition"
import . "паметmanager"

type TBiosparameterБлок32 struct {
	jmp			[3]uint8
	softИме			[8]byte
	байтовеpersector	uint16
	sectorspercluster	uint8
	резервираноsectors	uint16
	fatКопиране		uint8
	коренпапказапис		uint16
	общоsectors		uint16
	носителТип		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	скритsectors		uint32
	общоsectorcount		uint32

	таблицаРазмер			uint32
	extФлагове			uint16
	fatВерсия			uint16
	коренcluster			uint32
	fatИнформация			uint16
	backupsector			uint16
	резервирано0			[12]uint8
	driveЧисло			uint8
	резервирано			uint8
	bootsignature			uint8
	силаназвукаИДЕНТИФИКАТОР	uint32
	силаназвукаЕтикет		[11]byte
	fatТипЕтикет			[8]byte
}

func (себеси *TBiosparameterБлок32) Init(data []byte) {
	copy(себеси.jmp[:3], data[0:3])
	copy(себеси.softИме[:8], data[3:11])

	себеси.байтовеpersector = (uint16(data[11]) | uint16(data[12])<<8)
	себеси.sectorspercluster = data[13]
	себеси.резервираноsectors = (uint16(data[14]) | uint16(data[15])<<8)
	себеси.fatКопиране = data[16]
	себеси.коренпапказапис = (uint16(data[17]) | uint16(data[18])<<8)
	себеси.общоsectors = (uint16(data[19]) | uint16(data[20])<<8)
	себеси.носителТип = data[21]
	себеси.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	себеси.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	себеси.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	себеси.скритsectors = Unsignedinteger32r(Масивtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	себеси.общоsectorcount = Unsignedinteger32r(Масивtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	себеси.таблицаРазмер = Unsignedinteger32r(Масивtounsignedinteger32(buffer1))

	себеси.extФлагове = (uint16(data[40]) | uint16(data[41])<<8)
	себеси.fatВерсия = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	себеси.коренcluster = Unsignedinteger32r(Масивtounsignedinteger32(buffer1))

	себеси.fatИнформация = (uint16(data[48]) | uint16(data[49])<<8)
	себеси.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(себеси.резервирано0[:12], data[52:64])

	себеси.driveЧисло = data[64]
	себеси.резервирано = data[65]
	себеси.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	себеси.силаназвукаИДЕНТИФИКАТОР = Unsignedinteger32r(Масивtounsignedinteger32(buffer1))

	copy(себеси.силаназвукаЕтикет[:11], data[71:82])
	copy(себеси.fatТипЕтикет[:8], data[82:90])

}

var console_2 = TConsole{}

func (себеси *TBiosparameterБлок32) Len(hd *TДопълнителниТехнологияattachment, partзапис TPartitionТаблицазапис, именафайл []byte) uint32 {

	if partзапис.PartitionИДЕНТИФИКАТОР == 0x00 {
		return 0
	}

	паметmanager := TПаметmanager{}
	bpbПоказалци := паметmanager.Malloc(90)
	bpbБайтове := GetБайтовеfromПоказалци(uintptr(bpbПоказалци), 90, 90)
	var partitionoffset = partзапис.Стартиранеlba

	hd.Четене28(partitionoffset, &bpbБайтове, 90)

	var bpb = TBiosparameterБлок32{}
	bpb.Init(bpbБайтове)

	var fatСтартиране = partitionoffset + uint32(bpb.резервираноsectors)
	var fatРазмер = bpb.таблицаРазмер

	var dataСтартиране = fatСтартиране + fatРазмер*uint32(bpb.fatКопиране)

	var коренСтартиране = dataСтартиране + uint32(bpb.sectorspercluster)*(bpb.коренcluster-2)

	direntПоказалци := паметmanager.Malloc(512)
	direntБайтове := GetБайтовеfromПоказалци(uintptr(direntПоказалци), 512, 512)
	hd.Четене28(коренСтартиране, &direntБайтове, 512)

	var dirent = [16]TПапказаписfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайтове[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].име[0] == 0x00 {
			break
		}

		if dirent[i].размер >= 0xFFFFFFFF {
			continue
		}

		if !ЕднакъвБайтове(именафайл, dirent[i].име[:len(именафайл)]) {
			continue
		}

		паметmanager.Свободно(bpbПоказалци)
		паметmanager.Свободно(direntПоказалци)
		return dirent[i].размер
	}
	паметmanager.Свободно(bpbПоказалци)
	паметmanager.Свободно(direntПоказалци)
	return 0
}
func (себеси *TBiosparameterБлок32) Четене(hd *TДопълнителниТехнологияattachment, partзапис TPartitionТаблицазапис, именафайл []byte, data []byte) {

	if partзапис.PartitionИДЕНТИФИКАТОР == 0x00 {
		return
	}

	паметmanager := TПаметmanager{}
	bpbПоказалци := паметmanager.Malloc(90)
	bpbБайтове := GetБайтовеfromПоказалци(uintptr(bpbПоказалци), 90, 90)
	var partitionoffset = partзапис.Стартиранеlba

	hd.Четене28(partitionoffset, &bpbБайтове, 90)

	var bpb = TBiosparameterБлок32{}
	bpb.Init(bpbБайтове)

	var fatСтартиране = partitionoffset + uint32(bpb.резервираноsectors)
	var fatРазмер = bpb.таблицаРазмер

	var dataСтартиране = fatСтартиране + fatРазмер*uint32(bpb.fatКопиране)

	var коренСтартиране = dataСтартиране + uint32(bpb.sectorspercluster)*(bpb.коренcluster-2)

	direntПоказалци := паметmanager.Malloc(512)
	direntБайтове := GetБайтовеfromПоказалци(uintptr(direntПоказалци), 512, 512)
	hd.Четене28(коренСтартиране, &direntБайтове, 512)

	var dirent = [16]TПапказаписfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайтове[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].име[0] == 0x00 {
			break
		}

		if dirent[i].размер >= 0xFFFFFFFF {
			continue
		}

		if !ЕднакъвБайтове(именафайл, dirent[i].име[:len(именафайл)]) {
			continue
		}

		var firstФайлcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterНисък))

		var Размер = int32(dirent[i].размер)
		var следващоФайлcluster = int32(firstФайлcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Размер > 0 {
			var файлsector = dataСтартиране + uint32(bpb.sectorspercluster)*uint32(следващоФайлcluster-2)
			var sectoroffset int = 0

			for ; Размер > 0; Размер -= 512 {

				var buffer3 []byte

				if dirent[i].размер > 512 {
					buffer3 = buffer_2[:512]
					hd.Четене28(файлsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].размер]
					hd.Четене28(файлsector+uint32(sectoroffset), &buffer3, int(dirent[i].размер))
				}

				copy(data[int32(dirent[i].размер)-Размер:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforТекущадатаcluster = uint32(следващоФайлcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Четене28(fatСтартиране+fatsectorforТекущадатаcluster, &fatbuf, 512)

			var fatoffsetВходящsectorforТекущадатаcluster = следващоФайлcluster % 128
			var стартиранеoffset = fatoffsetВходящsectorforТекущадатаcluster * 4
			var крайoffset = fatoffsetВходящsectorforТекущадатаcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[стартиранеoffset:крайoffset])

			следващоФайлcluster = int32(Unsignedinteger32r(Масивtounsignedinteger32(buffer4)))
		}
	}
	паметmanager.Свободно(bpbПоказалци)
	паметmanager.Свободно(direntПоказалци)
}

type TПапказаписfat32 struct {
	име			[8]byte
	ext			[3]byte
	атрибути		uint8
	резервирано		uint8
	cВремеtenth		uint8
	cВреме			uint16
	cДата			uint16
	aВреме			uint16
	firstclusterhi		uint16
	wВреме			uint16
	wДата			uint16
	firstclusterНисък	uint16
	размер			uint32
}

func (себеси *TПапказаписfat32) Init(data [32]byte) {
	copy(себеси.име[:8], data[0:8])
	copy(себеси.ext[:3], data[8:11])
	себеси.атрибути = data[11]
	себеси.резервирано = data[12]
	себеси.cВремеtenth = data[13]
	себеси.cВреме = uint16(data[14]) | uint16(data[15])<<8
	себеси.cДата = uint16(data[16]) | uint16(data[17])<<8
	себеси.aВреме = uint16(data[18]) | uint16(data[19])<<8
	себеси.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	себеси.wВреме = uint16(data[22]) | uint16(data[23])<<8
	себеси.wДата = uint16(data[24]) | uint16(data[25])<<8
	себеси.firstclusterНисък = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	себеси.размер = Unsignedinteger32r(Масивtounsignedinteger32(buffer))
}
