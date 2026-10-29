/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "конзола"
import . "driver/ata"
import . "датотекаСистем/msdospartition"
import . "меморијаmanager"

type TBiosparameterБлок32 struct {
	jmp			[3]uint8
	softНазив		[8]byte
	бајтоваpersector	uint16
	sectorspercluster	uint8
	заузетоsectors		uint16
	fatУмножи		uint8
	коренДиректоријумунос	uint16
	укупноsectors		uint16
	медијВрста		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	скривенsectors		uint32
	укупноsectorcount	uint32

	табелаВеличина	uint32
	extПараметри	uint16
	fatИздање	uint16
	коренcluster	uint32
	fatПодаци	uint16
	backupsector	uint16
	заузето0	[12]uint8
	driveброј	uint8
	заузето		uint8
	bootsignature	uint8
	гласноћаИБ	uint32
	гласноћаНатпис	[11]byte
	fatВрстаНатпис	[8]byte
}

func (исти *TBiosparameterБлок32) Init(data []byte) {
	copy(исти.jmp[:3], data[0:3])
	copy(исти.softНазив[:8], data[3:11])

	исти.бајтоваpersector = (uint16(data[11]) | uint16(data[12])<<8)
	исти.sectorspercluster = data[13]
	исти.заузетоsectors = (uint16(data[14]) | uint16(data[15])<<8)
	исти.fatУмножи = data[16]
	исти.коренДиректоријумунос = (uint16(data[17]) | uint16(data[18])<<8)
	исти.укупноsectors = (uint16(data[19]) | uint16(data[20])<<8)
	исти.медијВрста = data[21]
	исти.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	исти.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	исти.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	исти.скривенsectors = Unsignedinteger32r(Низtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	исти.укупноsectorcount = Unsignedinteger32r(Низtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	исти.табелаВеличина = Unsignedinteger32r(Низtounsignedinteger32(buffer1))

	исти.extПараметри = (uint16(data[40]) | uint16(data[41])<<8)
	исти.fatИздање = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	исти.коренcluster = Unsignedinteger32r(Низtounsignedinteger32(buffer1))

	исти.fatПодаци = (uint16(data[48]) | uint16(data[49])<<8)
	исти.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(исти.заузето0[:12], data[52:64])

	исти.driveброј = data[64]
	исти.заузето = data[65]
	исти.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	исти.гласноћаИБ = Unsignedinteger32r(Низtounsignedinteger32(buffer1))

	copy(исти.гласноћаНатпис[:11], data[71:82])
	copy(исти.fatВрстаНатпис[:8], data[82:90])

}

var конзола_2 = TКонзола{}

func (исти *TBiosparameterБлок32) Len(hd *TНапредноТехнологијаattachment, partунос TPartitionТабелаунос, датотека []byte) uint32 {

	if partунос.PartitionИБ == 0x00 {
		return 0
	}

	меморијаmanager := TМеморијаmanager{}
	bpbПоказивач := меморијаmanager.Malloc(90)
	bpbБајтова := GetБајтовасаПоказивач(uintptr(bpbПоказивач), 90, 90)
	var partitionoffset = partунос.Покрениlba

	hd.Читање28(partitionoffset, &bpbБајтова, 90)

	var bpb = TBiosparameterБлок32{}
	bpb.Init(bpbБајтова)

	var fatПокрени = partitionoffset + uint32(bpb.заузетоsectors)
	var fatВеличина = bpb.табелаВеличина

	var dataПокрени = fatПокрени + fatВеличина*uint32(bpb.fatУмножи)

	var коренПокрени = dataПокрени + uint32(bpb.sectorspercluster)*(bpb.коренcluster-2)

	direntПоказивач := меморијаmanager.Malloc(512)
	direntБајтова := GetБајтовасаПоказивач(uintptr(direntПоказивач), 512, 512)
	hd.Читање28(коренПокрени, &direntБајтова, 512)

	var dirent = [16]TДиректоријумуносfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБајтова[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].назив[0] == 0x00 {
			break
		}

		if dirent[i].величина >= 0xFFFFFFFF {
			continue
		}

		if !ИстаБајтова(датотека, dirent[i].назив[:len(датотека)]) {
			continue
		}

		меморијаmanager.Слободно(bpbПоказивач)
		меморијаmanager.Слободно(direntПоказивач)
		return dirent[i].величина
	}
	меморијаmanager.Слободно(bpbПоказивач)
	меморијаmanager.Слободно(direntПоказивач)
	return 0
}
func (исти *TBiosparameterБлок32) Читање(hd *TНапредноТехнологијаattachment, partунос TPartitionТабелаунос, датотека []byte, data []byte) {

	if partунос.PartitionИБ == 0x00 {
		return
	}

	меморијаmanager := TМеморијаmanager{}
	bpbПоказивач := меморијаmanager.Malloc(90)
	bpbБајтова := GetБајтовасаПоказивач(uintptr(bpbПоказивач), 90, 90)
	var partitionoffset = partунос.Покрениlba

	hd.Читање28(partitionoffset, &bpbБајтова, 90)

	var bpb = TBiosparameterБлок32{}
	bpb.Init(bpbБајтова)

	var fatПокрени = partitionoffset + uint32(bpb.заузетоsectors)
	var fatВеличина = bpb.табелаВеличина

	var dataПокрени = fatПокрени + fatВеличина*uint32(bpb.fatУмножи)

	var коренПокрени = dataПокрени + uint32(bpb.sectorspercluster)*(bpb.коренcluster-2)

	direntПоказивач := меморијаmanager.Malloc(512)
	direntБајтова := GetБајтовасаПоказивач(uintptr(direntПоказивач), 512, 512)
	hd.Читање28(коренПокрени, &direntБајтова, 512)

	var dirent = [16]TДиректоријумуносfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБајтова[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].назив[0] == 0x00 {
			break
		}

		if dirent[i].величина >= 0xFFFFFFFF {
			continue
		}

		if !ИстаБајтова(датотека, dirent[i].назив[:len(датотека)]) {
			continue
		}

		var firstДатотекаcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterТихо))

		var Величина = int32(dirent[i].величина)
		var следећеДатотекаcluster = int32(firstДатотекаcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Величина > 0 {
			var датотекаsector = dataПокрени + uint32(bpb.sectorspercluster)*uint32(следећеДатотекаcluster-2)
			var sectoroffset int = 0

			for ; Величина > 0; Величина -= 512 {

				var buffer3 []byte

				if dirent[i].величина > 512 {
					buffer3 = buffer_2[:512]
					hd.Читање28(датотекаsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].величина]
					hd.Читање28(датотекаsector+uint32(sectoroffset), &buffer3, int(dirent[i].величина))
				}

				copy(data[int32(dirent[i].величина)-Величина:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforТренутноcluster = uint32(следећеДатотекаcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Читање28(fatПокрени+fatsectorforТренутноcluster, &fatbuf, 512)

			var fatoffsetПримљеноsectorforТренутноcluster = следећеДатотекаcluster % 128
			var покрениoffset = fatoffsetПримљеноsectorforТренутноcluster * 4
			var krajoffset = fatoffsetПримљеноsectorforТренутноcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[покрениoffset:krajoffset])

			следећеДатотекаcluster = int32(Unsignedinteger32r(Низtounsignedinteger32(buffer4)))
		}
	}
	меморијаmanager.Слободно(bpbПоказивач)
	меморијаmanager.Слободно(direntПоказивач)
}

type TДиректоријумуносfat32 struct {
	назив			[8]byte
	ext			[3]byte
	attributes		uint8
	заузето			uint8
	cВремеtenth		uint8
	cВреме			uint16
	cДатум			uint16
	aВреме			uint16
	firstclusterhi		uint16
	wВреме			uint16
	wДатум			uint16
	firstclusterТихо	uint16
	величина		uint32
}

func (исти *TДиректоријумуносfat32) Init(data [32]byte) {
	copy(исти.назив[:8], data[0:8])
	copy(исти.ext[:3], data[8:11])
	исти.attributes = data[11]
	исти.заузето = data[12]
	исти.cВремеtenth = data[13]
	исти.cВреме = uint16(data[14]) | uint16(data[15])<<8
	исти.cДатум = uint16(data[16]) | uint16(data[17])<<8
	исти.aВреме = uint16(data[18]) | uint16(data[19])<<8
	исти.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	исти.wВреме = uint16(data[22]) | uint16(data[23])<<8
	исти.wДатум = uint16(data[24]) | uint16(data[25])<<8
	исти.firstclusterТихо = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	исти.величина = Unsignedinteger32r(Низtounsignedinteger32(buffer))
}
