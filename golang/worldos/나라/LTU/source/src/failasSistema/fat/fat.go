/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "failasSistema/msdospartition"
import . "atmintismanager"

type TBiosparameterBlokas32 struct {
	jmp			[3]uint8
	softPavadinimas		[8]byte
	baitųpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatKopijuoti		uint8
	šakniskatalogasįrašas	uint16
	išvisosectors		uint16
	laikmenosTipas		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	paslėptassectors	uint32
	išvisosectorcount	uint32

	lentelėDydis	uint32
	extParametrai	uint16
	fatVersija	uint16
	šakniscluster	uint32
	fatInformacija	uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveSkaičius	uint8
	reserved	uint8
	bootsignature	uint8
	garsisid	uint32
	garsisUžrašas	[11]byte
	fatTipasUžrašas	[8]byte
}

func (self *TBiosparameterBlokas32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softPavadinimas[:8], data[3:11])

	self.baitųpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatKopijuoti = data[16]
	self.šakniskatalogasįrašas = (uint16(data[17]) | uint16(data[18])<<8)
	self.išvisosectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.laikmenosTipas = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.paslėptassectors = Unsignedinteger32r(Masyvastounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.išvisosectorcount = Unsignedinteger32r(Masyvastounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.lentelėDydis = Unsignedinteger32r(Masyvastounsignedinteger32(buffer1))

	self.extParametrai = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatVersija = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.šakniscluster = Unsignedinteger32r(Masyvastounsignedinteger32(buffer1))

	self.fatInformacija = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveSkaičius = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.garsisid = Unsignedinteger32r(Masyvastounsignedinteger32(buffer1))

	copy(self.garsisUžrašas[:11], data[71:82])
	copy(self.fatTipasUžrašas[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterBlokas32) Len(hd *TIšsamiauTechnologijaattachment, partįrašas TPartitionLentelėįrašas, failopavadinimas []byte) uint32 {

	if partįrašas.Partitionid == 0x00 {
		return 0
	}

	atmintismanager := TAtmintismanager{}
	bpbRodyklė := atmintismanager.Malloc(90)
	bpbBaitų := GetBaitųfromRodyklė(uintptr(bpbRodyklė), 90, 90)
	var partitionoffset = partįrašas.Paleistilba

	hd.Skaitymas28(partitionoffset, &bpbBaitų, 90)

	var bpb = TBiosparameterBlokas32{}
	bpb.Init(bpbBaitų)

	var fatPaleisti = partitionoffset + uint32(bpb.reservedsectors)
	var fatDydis = bpb.lentelėDydis

	var dataPaleisti = fatPaleisti + fatDydis*uint32(bpb.fatKopijuoti)

	var šaknisPaleisti = dataPaleisti + uint32(bpb.sectorspercluster)*(bpb.šakniscluster-2)

	direntRodyklė := atmintismanager.Malloc(512)
	direntBaitų := GetBaitųfromRodyklė(uintptr(direntRodyklė), 512, 512)
	hd.Skaitymas28(šaknisPaleisti, &direntBaitų, 512)

	var dirent = [16]TKatalogasįrašasfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBaitų[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].pavadinimas[0] == 0x00 {
			break
		}

		if dirent[i].dydis >= 0xFFFFFFFF {
			continue
		}

		if !SuvienodintiBaitų(failopavadinimas, dirent[i].pavadinimas[:len(failopavadinimas)]) {
			continue
		}

		atmintismanager.Laisva(bpbRodyklė)
		atmintismanager.Laisva(direntRodyklė)
		return dirent[i].dydis
	}
	atmintismanager.Laisva(bpbRodyklė)
	atmintismanager.Laisva(direntRodyklė)
	return 0
}
func (self *TBiosparameterBlokas32) Skaitymas(hd *TIšsamiauTechnologijaattachment, partįrašas TPartitionLentelėįrašas, failopavadinimas []byte, data []byte) {

	if partįrašas.Partitionid == 0x00 {
		return
	}

	atmintismanager := TAtmintismanager{}
	bpbRodyklė := atmintismanager.Malloc(90)
	bpbBaitų := GetBaitųfromRodyklė(uintptr(bpbRodyklė), 90, 90)
	var partitionoffset = partįrašas.Paleistilba

	hd.Skaitymas28(partitionoffset, &bpbBaitų, 90)

	var bpb = TBiosparameterBlokas32{}
	bpb.Init(bpbBaitų)

	var fatPaleisti = partitionoffset + uint32(bpb.reservedsectors)
	var fatDydis = bpb.lentelėDydis

	var dataPaleisti = fatPaleisti + fatDydis*uint32(bpb.fatKopijuoti)

	var šaknisPaleisti = dataPaleisti + uint32(bpb.sectorspercluster)*(bpb.šakniscluster-2)

	direntRodyklė := atmintismanager.Malloc(512)
	direntBaitų := GetBaitųfromRodyklė(uintptr(direntRodyklė), 512, 512)
	hd.Skaitymas28(šaknisPaleisti, &direntBaitų, 512)

	var dirent = [16]TKatalogasįrašasfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBaitų[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].pavadinimas[0] == 0x00 {
			break
		}

		if dirent[i].dydis >= 0xFFFFFFFF {
			continue
		}

		if !SuvienodintiBaitų(failopavadinimas, dirent[i].pavadinimas[:len(failopavadinimas)]) {
			continue
		}

		var firstFailascluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterŽemas))

		var Dydis = int32(dirent[i].dydis)
		var kitasFailascluster = int32(firstFailascluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Dydis > 0 {
			var failassector = dataPaleisti + uint32(bpb.sectorspercluster)*uint32(kitasFailascluster-2)
			var sectoroffset int = 0

			for ; Dydis > 0; Dydis -= 512 {

				var buffer3 []byte

				if dirent[i].dydis > 512 {
					buffer3 = buffer_2[:512]
					hd.Skaitymas28(failassector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].dydis]
					hd.Skaitymas28(failassector+uint32(sectoroffset), &buffer3, int(dirent[i].dydis))
				}

				copy(data[int32(dirent[i].dydis)-Dydis:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforDabartiniscluster = uint32(kitasFailascluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Skaitymas28(fatPaleisti+fatsectorforDabartiniscluster, &fatbuf, 512)

			var fatoffsetĮsectorforDabartiniscluster = kitasFailascluster % 128
			var paleistioffset = fatoffsetĮsectorforDabartiniscluster * 4
			var paboffset = fatoffsetĮsectorforDabartiniscluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[paleistioffset:paboffset])

			kitasFailascluster = int32(Unsignedinteger32r(Masyvastounsignedinteger32(buffer4)))
		}
	}
	atmintismanager.Laisva(bpbRodyklė)
	atmintismanager.Laisva(direntRodyklė)
}

type TKatalogasįrašasfat32 struct {
	pavadinimas		[8]byte
	ext			[3]byte
	požymiai		uint8
	reserved		uint8
	cLaikastenth		uint8
	cLaikas			uint16
	cData			uint16
	aLaikas			uint16
	firstclusterhi		uint16
	wLaikas			uint16
	wData			uint16
	firstclusterŽemas	uint16
	dydis			uint32
}

func (self *TKatalogasįrašasfat32) Init(data [32]byte) {
	copy(self.pavadinimas[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.požymiai = data[11]
	self.reserved = data[12]
	self.cLaikastenth = data[13]
	self.cLaikas = uint16(data[14]) | uint16(data[15])<<8
	self.cData = uint16(data[16]) | uint16(data[17])<<8
	self.aLaikas = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wLaikas = uint16(data[22]) | uint16(data[23])<<8
	self.wData = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterŽemas = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.dydis = Unsignedinteger32r(Masyvastounsignedinteger32(buffer))
}
