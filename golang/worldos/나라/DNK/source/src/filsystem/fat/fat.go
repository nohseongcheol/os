/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "filsystem/msdospartition"
import . "hukommelsemanager"

type TBiosparameterBlok32 struct {
	jmp			[3]uint8
	softNavn		[8]byte
	bytepersector		uint16
	sectorspercluster	uint8
	reserveretsectors	uint16
	fatKopiér		uint8
	rodMappeemne		uint16
	totalsectors		uint16
	medietype		uint8
	fatsectorAntal		uint16
	sectorpertrack		uint16
	headAntal		uint16
	skjultsectors		uint32
	totalsectorAntal	uint32

	tabelStørrelse	uint32
	extFlag		uint16
	fatversion	uint16
	rodcluster	uint32
	fatInformation	uint16
	backupsector	uint16
	reserveret0	[12]uint8
	driveTal	uint8
	reserveret	uint8
	bootsignature	uint8
	lydstyrkeid	uint32
	lydstyrkeEtiket	[11]byte
	fattypeEtiket	[8]byte
}

func (selv *TBiosparameterBlok32) Init(data []byte) {
	copy(selv.jmp[:3], data[0:3])
	copy(selv.softNavn[:8], data[3:11])

	selv.bytepersector = (uint16(data[11]) | uint16(data[12])<<8)
	selv.sectorspercluster = data[13]
	selv.reserveretsectors = (uint16(data[14]) | uint16(data[15])<<8)
	selv.fatKopiér = data[16]
	selv.rodMappeemne = (uint16(data[17]) | uint16(data[18])<<8)
	selv.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	selv.medietype = data[21]
	selv.fatsectorAntal = (uint16(data[22]) | uint16(data[23])<<8)
	selv.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	selv.headAntal = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	selv.skjultsectors = Unsignedinteger32r(Tabeltounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	selv.totalsectorAntal = Unsignedinteger32r(Tabeltounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	selv.tabelStørrelse = Unsignedinteger32r(Tabeltounsignedinteger32(buffer1))

	selv.extFlag = (uint16(data[40]) | uint16(data[41])<<8)
	selv.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	selv.rodcluster = Unsignedinteger32r(Tabeltounsignedinteger32(buffer1))

	selv.fatInformation = (uint16(data[48]) | uint16(data[49])<<8)
	selv.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(selv.reserveret0[:12], data[52:64])

	selv.driveTal = data[64]
	selv.reserveret = data[65]
	selv.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	selv.lydstyrkeid = Unsignedinteger32r(Tabeltounsignedinteger32(buffer1))

	copy(selv.lydstyrkeEtiket[:11], data[71:82])
	copy(selv.fattypeEtiket[:8], data[82:90])

}

var console_2 = TConsole{}

func (selv *TBiosparameterBlok32) Len(hd *TAvanceretTeknologiattachment, partemne TPartitionTabelemne, filnavn []byte) uint32 {

	if partemne.Partitionid == 0x00 {
		return 0
	}

	hukommelsemanager := THukommelsemanager{}
	bpbMarkør := hukommelsemanager.Malloc(90)
	bpbByte := GetBytefraMarkør(uintptr(bpbMarkør), 90, 90)
	var partitionForskydning = partemne.Begyndlba

	hd.Læse28(partitionForskydning, &bpbByte, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbByte)

	var fatBegynd = partitionForskydning + uint32(bpb.reserveretsectors)
	var fatStørrelse = bpb.tabelStørrelse

	var dataBegynd = fatBegynd + fatStørrelse*uint32(bpb.fatKopiér)

	var rodBegynd = dataBegynd + uint32(bpb.sectorspercluster)*(bpb.rodcluster-2)

	direntMarkør := hukommelsemanager.Malloc(512)
	direntByte := GetBytefraMarkør(uintptr(direntMarkør), 512, 512)
	hd.Læse28(rodBegynd, &direntByte, 512)

	var dirent = [16]TMappeemnefat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].navn[0] == 0x00 {
			break
		}

		if dirent[i].størrelse >= 0xFFFFFFFF {
			continue
		}

		if !EqualByte(filnavn, dirent[i].navn[:len(filnavn)]) {
			continue
		}

		hukommelsemanager.Fri(bpbMarkør)
		hukommelsemanager.Fri(direntMarkør)
		return dirent[i].størrelse
	}
	hukommelsemanager.Fri(bpbMarkør)
	hukommelsemanager.Fri(direntMarkør)
	return 0
}
func (selv *TBiosparameterBlok32) Læse(hd *TAvanceretTeknologiattachment, partemne TPartitionTabelemne, filnavn []byte, data []byte) {

	if partemne.Partitionid == 0x00 {
		return
	}

	hukommelsemanager := THukommelsemanager{}
	bpbMarkør := hukommelsemanager.Malloc(90)
	bpbByte := GetBytefraMarkør(uintptr(bpbMarkør), 90, 90)
	var partitionForskydning = partemne.Begyndlba

	hd.Læse28(partitionForskydning, &bpbByte, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbByte)

	var fatBegynd = partitionForskydning + uint32(bpb.reserveretsectors)
	var fatStørrelse = bpb.tabelStørrelse

	var dataBegynd = fatBegynd + fatStørrelse*uint32(bpb.fatKopiér)

	var rodBegynd = dataBegynd + uint32(bpb.sectorspercluster)*(bpb.rodcluster-2)

	direntMarkør := hukommelsemanager.Malloc(512)
	direntByte := GetBytefraMarkør(uintptr(direntMarkør), 512, 512)
	hd.Læse28(rodBegynd, &direntByte, 512)

	var dirent = [16]TMappeemnefat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].navn[0] == 0x00 {
			break
		}

		if dirent[i].størrelse >= 0xFFFFFFFF {
			continue
		}

		if !EqualByte(filnavn, dirent[i].navn[:len(filnavn)]) {
			continue
		}

		var firstFilcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterLav))

		var Størrelse = int32(dirent[i].størrelse)
		var næsteFilcluster = int32(firstFilcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Størrelse > 0 {
			var filsector = dataBegynd + uint32(bpb.sectorspercluster)*uint32(næsteFilcluster-2)
			var sectorForskydning int = 0

			for ; Størrelse > 0; Størrelse -= 512 {

				var buffer3 []byte

				if dirent[i].størrelse > 512 {
					buffer3 = buffer_2[:512]
					hd.Læse28(filsector+uint32(sectorForskydning), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].størrelse]
					hd.Læse28(filsector+uint32(sectorForskydning), &buffer3, int(dirent[i].størrelse))
				}

				copy(data[int32(dirent[i].størrelse)-Størrelse:], buffer3)

				sectorForskydning++

				if sectorForskydning > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforAktivecluster = uint32(næsteFilcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Læse28(fatBegynd+fatsectorforAktivecluster, &fatbuf, 512)

			var fatForskydningIndsectorforAktivecluster = næsteFilcluster % 128
			var begyndForskydning = fatForskydningIndsectorforAktivecluster * 4
			var slutningenForskydning = fatForskydningIndsectorforAktivecluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[begyndForskydning:slutningenForskydning])

			næsteFilcluster = int32(Unsignedinteger32r(Tabeltounsignedinteger32(buffer4)))
		}
	}
	hukommelsemanager.Fri(bpbMarkør)
	hukommelsemanager.Fri(direntMarkør)
}

type TMappeemnefat32 struct {
	navn		[8]byte
	ext		[3]byte
	attributter	uint8
	reserveret	uint8
	cTidtenth	uint8
	cTid		uint16
	cDato		uint16
	aTid		uint16
	firstclusterhi	uint16
	wTid		uint16
	wDato		uint16
	firstclusterLav	uint16
	størrelse	uint32
}

func (selv *TMappeemnefat32) Init(data [32]byte) {
	copy(selv.navn[:8], data[0:8])
	copy(selv.ext[:3], data[8:11])
	selv.attributter = data[11]
	selv.reserveret = data[12]
	selv.cTidtenth = data[13]
	selv.cTid = uint16(data[14]) | uint16(data[15])<<8
	selv.cDato = uint16(data[16]) | uint16(data[17])<<8
	selv.aTid = uint16(data[18]) | uint16(data[19])<<8
	selv.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	selv.wTid = uint16(data[22]) | uint16(data[23])<<8
	selv.wDato = uint16(data[24]) | uint16(data[25])<<8
	selv.firstclusterLav = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	selv.størrelse = Unsignedinteger32r(Tabeltounsignedinteger32(buffer))
}
