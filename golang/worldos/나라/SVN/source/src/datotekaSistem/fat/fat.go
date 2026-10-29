/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "datotekaSistem/msdospartition"
import . "pomnilnikmanager"

type TBiosparameterBlok32 struct {
	jmp			[3]uint8
	softIme			[8]byte
	bajtovpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatKopiraj		uint8
	vrhMapavnos		uint16
	skupnosectors		uint16
	medijiVrsta		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	skritosectors		uint32
	skupnosectorcount	uint32

	preglednicaVelikost	uint32
	extZastavice		uint16
	fatRazličica		uint16
	vrhcluster		uint32
	fatPodatki		uint16
	backupsector		uint16
	reserved0		[12]uint8
	driveŠtevilka		uint8
	reserved		uint8
	bootsignature		uint8
	glasnostid		uint32
	glasnostOznaka		[11]byte
	fatVrstaOznaka		[8]byte
}

func (sam *TBiosparameterBlok32) Init(data []byte) {
	copy(sam.jmp[:3], data[0:3])
	copy(sam.softIme[:8], data[3:11])

	sam.bajtovpersector = (uint16(data[11]) | uint16(data[12])<<8)
	sam.sectorspercluster = data[13]
	sam.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	sam.fatKopiraj = data[16]
	sam.vrhMapavnos = (uint16(data[17]) | uint16(data[18])<<8)
	sam.skupnosectors = (uint16(data[19]) | uint16(data[20])<<8)
	sam.medijiVrsta = data[21]
	sam.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	sam.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	sam.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	sam.skritosectors = Unsignedinteger32r(Poljetounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	sam.skupnosectorcount = Unsignedinteger32r(Poljetounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	sam.preglednicaVelikost = Unsignedinteger32r(Poljetounsignedinteger32(buffer1))

	sam.extZastavice = (uint16(data[40]) | uint16(data[41])<<8)
	sam.fatRazličica = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	sam.vrhcluster = Unsignedinteger32r(Poljetounsignedinteger32(buffer1))

	sam.fatPodatki = (uint16(data[48]) | uint16(data[49])<<8)
	sam.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(sam.reserved0[:12], data[52:64])

	sam.driveŠtevilka = data[64]
	sam.reserved = data[65]
	sam.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	sam.glasnostid = Unsignedinteger32r(Poljetounsignedinteger32(buffer1))

	copy(sam.glasnostOznaka[:11], data[71:82])
	copy(sam.fatVrstaOznaka[:8], data[82:90])

}

var console_2 = TConsole{}

func (sam *TBiosparameterBlok32) Len(hd *TNaprednoTehnologijaattachment, partvnos TPartitionPreglednicavnos, imedatoteke []byte) uint32 {

	if partvnos.Partitionid == 0x00 {
		return 0
	}

	pomnilnikmanager := TPomnilnikmanager{}
	bpbKazalnik := pomnilnikmanager.Malloc(90)
	bpbBajtov := GetBajtovfromKazalnik(uintptr(bpbKazalnik), 90, 90)
	var partitionoffset = partvnos.Začnilba

	hd.Branje28(partitionoffset, &bpbBajtov, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbBajtov)

	var fatZačni = partitionoffset + uint32(bpb.reservedsectors)
	var fatVelikost = bpb.preglednicaVelikost

	var dataZačni = fatZačni + fatVelikost*uint32(bpb.fatKopiraj)

	var vrhZačni = dataZačni + uint32(bpb.sectorspercluster)*(bpb.vrhcluster-2)

	direntKazalnik := pomnilnikmanager.Malloc(512)
	direntBajtov := GetBajtovfromKazalnik(uintptr(direntKazalnik), 512, 512)
	hd.Branje28(vrhZačni, &direntBajtov, 512)

	var dirent = [16]TMapavnosfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajtov[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ime[0] == 0x00 {
			break
		}

		if dirent[i].velikost >= 0xFFFFFFFF {
			continue
		}

		if !EqualBajtov(imedatoteke, dirent[i].ime[:len(imedatoteke)]) {
			continue
		}

		pomnilnikmanager.Prosto(bpbKazalnik)
		pomnilnikmanager.Prosto(direntKazalnik)
		return dirent[i].velikost
	}
	pomnilnikmanager.Prosto(bpbKazalnik)
	pomnilnikmanager.Prosto(direntKazalnik)
	return 0
}
func (sam *TBiosparameterBlok32) Branje(hd *TNaprednoTehnologijaattachment, partvnos TPartitionPreglednicavnos, imedatoteke []byte, data []byte) {

	if partvnos.Partitionid == 0x00 {
		return
	}

	pomnilnikmanager := TPomnilnikmanager{}
	bpbKazalnik := pomnilnikmanager.Malloc(90)
	bpbBajtov := GetBajtovfromKazalnik(uintptr(bpbKazalnik), 90, 90)
	var partitionoffset = partvnos.Začnilba

	hd.Branje28(partitionoffset, &bpbBajtov, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbBajtov)

	var fatZačni = partitionoffset + uint32(bpb.reservedsectors)
	var fatVelikost = bpb.preglednicaVelikost

	var dataZačni = fatZačni + fatVelikost*uint32(bpb.fatKopiraj)

	var vrhZačni = dataZačni + uint32(bpb.sectorspercluster)*(bpb.vrhcluster-2)

	direntKazalnik := pomnilnikmanager.Malloc(512)
	direntBajtov := GetBajtovfromKazalnik(uintptr(direntKazalnik), 512, 512)
	hd.Branje28(vrhZačni, &direntBajtov, 512)

	var dirent = [16]TMapavnosfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajtov[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ime[0] == 0x00 {
			break
		}

		if dirent[i].velikost >= 0xFFFFFFFF {
			continue
		}

		if !EqualBajtov(imedatoteke, dirent[i].ime[:len(imedatoteke)]) {
			continue
		}

		var prviDatotekacluster = (uint32(dirent[i].prviclusterhi)<<16 | uint32(dirent[i].prviclusterNizko))

		var Velikost = int32(dirent[i].velikost)
		var naslednjeDatotekacluster = int32(prviDatotekacluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Velikost > 0 {
			var datotekasector = dataZačni + uint32(bpb.sectorspercluster)*uint32(naslednjeDatotekacluster-2)
			var sectoroffset int = 0

			for ; Velikost > 0; Velikost -= 512 {

				var buffer3 []byte

				if dirent[i].velikost > 512 {
					buffer3 = buffer_2[:512]
					hd.Branje28(datotekasector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].velikost]
					hd.Branje28(datotekasector+uint32(sectoroffset), &buffer3, int(dirent[i].velikost))
				}

				copy(data[int32(dirent[i].velikost)-Velikost:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(naslednjeDatotekacluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Branje28(fatZačni+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetVhodnosectorforcurrentcluster = naslednjeDatotekacluster % 128
			var začnioffset = fatoffsetVhodnosectorforcurrentcluster * 4
			var endoffset = fatoffsetVhodnosectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[začnioffset:endoffset])

			naslednjeDatotekacluster = int32(Unsignedinteger32r(Poljetounsignedinteger32(buffer4)))
		}
	}
	pomnilnikmanager.Prosto(bpbKazalnik)
	pomnilnikmanager.Prosto(direntKazalnik)
}

type TMapavnosfat32 struct {
	ime			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cČastenth		uint8
	cČas			uint16
	cDatum			uint16
	aČas			uint16
	prviclusterhi		uint16
	wČas			uint16
	wDatum			uint16
	prviclusterNizko	uint16
	velikost		uint32
}

func (sam *TMapavnosfat32) Init(data [32]byte) {
	copy(sam.ime[:8], data[0:8])
	copy(sam.ext[:3], data[8:11])
	sam.attributes = data[11]
	sam.reserved = data[12]
	sam.cČastenth = data[13]
	sam.cČas = uint16(data[14]) | uint16(data[15])<<8
	sam.cDatum = uint16(data[16]) | uint16(data[17])<<8
	sam.aČas = uint16(data[18]) | uint16(data[19])<<8
	sam.prviclusterhi = uint16(data[20]) | uint16(data[21])<<8
	sam.wČas = uint16(data[22]) | uint16(data[23])<<8
	sam.wDatum = uint16(data[24]) | uint16(data[25])<<8
	sam.prviclusterNizko = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	sam.velikost = Unsignedinteger32r(Poljetounsignedinteger32(buffer))
}
