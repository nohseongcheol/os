/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "datotekaSustav/msdospartition"
import . "memorijamanager"

type TBiosparameterBlokiraj32 struct {
	jmp			[3]uint8
	softIme			[8]byte
	bajtovapersector	uint16
	sectorspercluster	uint8
	rezerviranosectors	uint16
	fatKopiraj		uint8
	korijenDirektorijentry	uint16
	ukupnosectors		uint16
	nosačpodatakaVrsta	uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	skrivenosectors		uint32
	ukupnosectorcount	uint32

	tablicaVeličina		uint32
	extZastavice		uint16
	fatInačica		uint16
	korijencluster		uint32
	fatInformacije		uint16
	backupsector		uint16
	rezervirano0		[12]uint8
	driveBROJ		uint8
	rezervirano		uint8
	bootsignature		uint8
	glasnoćaIdentifikacija	uint32
	glasnoćaNatpis		[11]byte
	fatVrstaNatpis		[8]byte
}

func (sam *TBiosparameterBlokiraj32) Init(data []byte) {
	copy(sam.jmp[:3], data[0:3])
	copy(sam.softIme[:8], data[3:11])

	sam.bajtovapersector = (uint16(data[11]) | uint16(data[12])<<8)
	sam.sectorspercluster = data[13]
	sam.rezerviranosectors = (uint16(data[14]) | uint16(data[15])<<8)
	sam.fatKopiraj = data[16]
	sam.korijenDirektorijentry = (uint16(data[17]) | uint16(data[18])<<8)
	sam.ukupnosectors = (uint16(data[19]) | uint16(data[20])<<8)
	sam.nosačpodatakaVrsta = data[21]
	sam.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	sam.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	sam.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	sam.skrivenosectors = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	sam.ukupnosectorcount = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	sam.tablicaVeličina = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	sam.extZastavice = (uint16(data[40]) | uint16(data[41])<<8)
	sam.fatInačica = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	sam.korijencluster = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	sam.fatInformacije = (uint16(data[48]) | uint16(data[49])<<8)
	sam.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(sam.rezervirano0[:12], data[52:64])

	sam.driveBROJ = data[64]
	sam.rezervirano = data[65]
	sam.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	sam.glasnoćaIdentifikacija = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	copy(sam.glasnoćaNatpis[:11], data[71:82])
	copy(sam.fatVrstaNatpis[:8], data[82:90])

}

var console_2 = TConsole{}

func (sam *TBiosparameterBlokiraj32) Len(hd *TNaprednoTehnologijaattachment, partentry TPartitionTablicaentry, imedatoteke []byte) uint32 {

	if partentry.PartitionIdentifikacija == 0x00 {
		return 0
	}

	memorijamanager := TMemorijamanager{}
	bpbPokazivač := memorijamanager.Malloc(90)
	bpbBajtova := GetBajtovafromPokazivač(uintptr(bpbPokazivač), 90, 90)
	var partitionoffset = partentry.Pokrenilba

	hd.Čitaj28(partitionoffset, &bpbBajtova, 90)

	var bpb = TBiosparameterBlokiraj32{}
	bpb.Init(bpbBajtova)

	var fatPokreni = partitionoffset + uint32(bpb.rezerviranosectors)
	var fatVeličina = bpb.tablicaVeličina

	var dataPokreni = fatPokreni + fatVeličina*uint32(bpb.fatKopiraj)

	var korijenPokreni = dataPokreni + uint32(bpb.sectorspercluster)*(bpb.korijencluster-2)

	direntPokazivač := memorijamanager.Malloc(512)
	direntBajtova := GetBajtovafromPokazivač(uintptr(direntPokazivač), 512, 512)
	hd.Čitaj28(korijenPokreni, &direntBajtova, 512)

	var dirent = [16]TDirektorijentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajtova[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ime[0] == 0x00 {
			break
		}

		if dirent[i].veličina >= 0xFFFFFFFF {
			continue
		}

		if !JednakoBajtova(imedatoteke, dirent[i].ime[:len(imedatoteke)]) {
			continue
		}

		memorijamanager.Slobodno(bpbPokazivač)
		memorijamanager.Slobodno(direntPokazivač)
		return dirent[i].veličina
	}
	memorijamanager.Slobodno(bpbPokazivač)
	memorijamanager.Slobodno(direntPokazivač)
	return 0
}
func (sam *TBiosparameterBlokiraj32) Čitaj(hd *TNaprednoTehnologijaattachment, partentry TPartitionTablicaentry, imedatoteke []byte, data []byte) {

	if partentry.PartitionIdentifikacija == 0x00 {
		return
	}

	memorijamanager := TMemorijamanager{}
	bpbPokazivač := memorijamanager.Malloc(90)
	bpbBajtova := GetBajtovafromPokazivač(uintptr(bpbPokazivač), 90, 90)
	var partitionoffset = partentry.Pokrenilba

	hd.Čitaj28(partitionoffset, &bpbBajtova, 90)

	var bpb = TBiosparameterBlokiraj32{}
	bpb.Init(bpbBajtova)

	var fatPokreni = partitionoffset + uint32(bpb.rezerviranosectors)
	var fatVeličina = bpb.tablicaVeličina

	var dataPokreni = fatPokreni + fatVeličina*uint32(bpb.fatKopiraj)

	var korijenPokreni = dataPokreni + uint32(bpb.sectorspercluster)*(bpb.korijencluster-2)

	direntPokazivač := memorijamanager.Malloc(512)
	direntBajtova := GetBajtovafromPokazivač(uintptr(direntPokazivač), 512, 512)
	hd.Čitaj28(korijenPokreni, &direntBajtova, 512)

	var dirent = [16]TDirektorijentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajtova[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ime[0] == 0x00 {
			break
		}

		if dirent[i].veličina >= 0xFFFFFFFF {
			continue
		}

		if !JednakoBajtova(imedatoteke, dirent[i].ime[:len(imedatoteke)]) {
			continue
		}

		var firstDatotekacluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterNIsko))

		var Veličina = int32(dirent[i].veličina)
		var slijedećeDatotekacluster = int32(firstDatotekacluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Veličina > 0 {
			var datotekasector = dataPokreni + uint32(bpb.sectorspercluster)*uint32(slijedećeDatotekacluster-2)
			var sectoroffset int = 0

			for ; Veličina > 0; Veličina -= 512 {

				var buffer3 []byte

				if dirent[i].veličina > 512 {
					buffer3 = buffer_2[:512]
					hd.Čitaj28(datotekasector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].veličina]
					hd.Čitaj28(datotekasector+uint32(sectoroffset), &buffer3, int(dirent[i].veličina))
				}

				copy(data[int32(dirent[i].veličina)-Veličina:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforTrenutnocluster = uint32(slijedećeDatotekacluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Čitaj28(fatPokreni+fatsectorforTrenutnocluster, &fatbuf, 512)

			var fatoffsetPovećajsectorforTrenutnocluster = slijedećeDatotekacluster % 128
			var pokrenioffset = fatoffsetPovećajsectorforTrenutnocluster * 4
			var krajoffset = fatoffsetPovećajsectorforTrenutnocluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[pokrenioffset:krajoffset])

			slijedećeDatotekacluster = int32(Unsignedinteger32r(Niztounsignedinteger32(buffer4)))
		}
	}
	memorijamanager.Slobodno(bpbPokazivač)
	memorijamanager.Slobodno(direntPokazivač)
}

type TDirektorijentryfat32 struct {
	ime			[8]byte
	ext			[3]byte
	atributi		uint8
	rezervirano		uint8
	cVrijemetenth		uint8
	cVrijeme		uint16
	cDatum			uint16
	aVrijeme		uint16
	firstclusterhi		uint16
	wVrijeme		uint16
	wDatum			uint16
	firstclusterNIsko	uint16
	veličina		uint32
}

func (sam *TDirektorijentryfat32) Init(data [32]byte) {
	copy(sam.ime[:8], data[0:8])
	copy(sam.ext[:3], data[8:11])
	sam.atributi = data[11]
	sam.rezervirano = data[12]
	sam.cVrijemetenth = data[13]
	sam.cVrijeme = uint16(data[14]) | uint16(data[15])<<8
	sam.cDatum = uint16(data[16]) | uint16(data[17])<<8
	sam.aVrijeme = uint16(data[18]) | uint16(data[19])<<8
	sam.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	sam.wVrijeme = uint16(data[22]) | uint16(data[23])<<8
	sam.wDatum = uint16(data[24]) | uint16(data[25])<<8
	sam.firstclusterNIsko = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	sam.veličina = Unsignedinteger32r(Niztounsignedinteger32(buffer))
}
