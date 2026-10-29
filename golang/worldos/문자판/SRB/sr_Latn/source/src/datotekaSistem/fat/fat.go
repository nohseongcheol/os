/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "konzola"
import . "driver/ata"
import . "datotekaSistem/msdospartition"
import . "memorijamanager"

type TBiosparameterBlok32 struct {
	jmp			[3]uint8
	softNaziv		[8]byte
	bajtovapersector	uint16
	sectorspercluster	uint8
	zauzetosectors		uint16
	fatUmnoži		uint8
	korenDirektorijumunos	uint16
	ukupnosectors		uint16
	medijVrsta		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	skrivensectors		uint32
	ukupnosectorcount	uint32

	tabelaVeličina	uint32
	extParametri	uint16
	fatIzdanje	uint16
	korencluster	uint32
	fatPodaci	uint16
	backupsector	uint16
	zauzeto0	[12]uint8
	drivebroj	uint8
	zauzeto		uint8
	bootsignature	uint8
	glasnoćaIB	uint32
	glasnoćaNatpis	[11]byte
	fatVrstaNatpis	[8]byte
}

func (isti *TBiosparameterBlok32) Init(data []byte) {
	copy(isti.jmp[:3], data[0:3])
	copy(isti.softNaziv[:8], data[3:11])

	isti.bajtovapersector = (uint16(data[11]) | uint16(data[12])<<8)
	isti.sectorspercluster = data[13]
	isti.zauzetosectors = (uint16(data[14]) | uint16(data[15])<<8)
	isti.fatUmnoži = data[16]
	isti.korenDirektorijumunos = (uint16(data[17]) | uint16(data[18])<<8)
	isti.ukupnosectors = (uint16(data[19]) | uint16(data[20])<<8)
	isti.medijVrsta = data[21]
	isti.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	isti.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	isti.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	isti.skrivensectors = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	isti.ukupnosectorcount = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	isti.tabelaVeličina = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	isti.extParametri = (uint16(data[40]) | uint16(data[41])<<8)
	isti.fatIzdanje = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	isti.korencluster = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	isti.fatPodaci = (uint16(data[48]) | uint16(data[49])<<8)
	isti.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(isti.zauzeto0[:12], data[52:64])

	isti.drivebroj = data[64]
	isti.zauzeto = data[65]
	isti.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	isti.glasnoćaIB = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	copy(isti.glasnoćaNatpis[:11], data[71:82])
	copy(isti.fatVrstaNatpis[:8], data[82:90])

}

var konzola_2 = TKonzola{}

func (isti *TBiosparameterBlok32) Len(hd *TNaprednoTehnologijaattachment, partunos TPartitionTabelaunos, datoteka []byte) uint32 {

	if partunos.PartitionIB == 0x00 {
		return 0
	}

	memorijamanager := TMemorijamanager{}
	bpbPokazivač := memorijamanager.Malloc(90)
	bpbBajtova := GetBajtovasaPokazivač(uintptr(bpbPokazivač), 90, 90)
	var partitionoffset = partunos.Pokrenilba

	hd.Čitanje28(partitionoffset, &bpbBajtova, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbBajtova)

	var fatPokreni = partitionoffset + uint32(bpb.zauzetosectors)
	var fatVeličina = bpb.tabelaVeličina

	var dataPokreni = fatPokreni + fatVeličina*uint32(bpb.fatUmnoži)

	var korenPokreni = dataPokreni + uint32(bpb.sectorspercluster)*(bpb.korencluster-2)

	direntPokazivač := memorijamanager.Malloc(512)
	direntBajtova := GetBajtovasaPokazivač(uintptr(direntPokazivač), 512, 512)
	hd.Čitanje28(korenPokreni, &direntBajtova, 512)

	var dirent = [16]TDirektorijumunosfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajtova[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].naziv[0] == 0x00 {
			break
		}

		if dirent[i].veličina >= 0xFFFFFFFF {
			continue
		}

		if !IstaBajtova(datoteka, dirent[i].naziv[:len(datoteka)]) {
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
func (isti *TBiosparameterBlok32) Čitanje(hd *TNaprednoTehnologijaattachment, partunos TPartitionTabelaunos, datoteka []byte, data []byte) {

	if partunos.PartitionIB == 0x00 {
		return
	}

	memorijamanager := TMemorijamanager{}
	bpbPokazivač := memorijamanager.Malloc(90)
	bpbBajtova := GetBajtovasaPokazivač(uintptr(bpbPokazivač), 90, 90)
	var partitionoffset = partunos.Pokrenilba

	hd.Čitanje28(partitionoffset, &bpbBajtova, 90)

	var bpb = TBiosparameterBlok32{}
	bpb.Init(bpbBajtova)

	var fatPokreni = partitionoffset + uint32(bpb.zauzetosectors)
	var fatVeličina = bpb.tabelaVeličina

	var dataPokreni = fatPokreni + fatVeličina*uint32(bpb.fatUmnoži)

	var korenPokreni = dataPokreni + uint32(bpb.sectorspercluster)*(bpb.korencluster-2)

	direntPokazivač := memorijamanager.Malloc(512)
	direntBajtova := GetBajtovasaPokazivač(uintptr(direntPokazivač), 512, 512)
	hd.Čitanje28(korenPokreni, &direntBajtova, 512)

	var dirent = [16]TDirektorijumunosfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajtova[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].naziv[0] == 0x00 {
			break
		}

		if dirent[i].veličina >= 0xFFFFFFFF {
			continue
		}

		if !IstaBajtova(datoteka, dirent[i].naziv[:len(datoteka)]) {
			continue
		}

		var firstDatotekacluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterTiho))

		var Veličina = int32(dirent[i].veličina)
		var sledećeDatotekacluster = int32(firstDatotekacluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Veličina > 0 {
			var datotekasector = dataPokreni + uint32(bpb.sectorspercluster)*uint32(sledećeDatotekacluster-2)
			var sectoroffset int = 0

			for ; Veličina > 0; Veličina -= 512 {

				var buffer3 []byte

				if dirent[i].veličina > 512 {
					buffer3 = buffer_2[:512]
					hd.Čitanje28(datotekasector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].veličina]
					hd.Čitanje28(datotekasector+uint32(sectoroffset), &buffer3, int(dirent[i].veličina))
				}

				copy(data[int32(dirent[i].veličina)-Veličina:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforTrenutnocluster = uint32(sledećeDatotekacluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Čitanje28(fatPokreni+fatsectorforTrenutnocluster, &fatbuf, 512)

			var fatoffsetPrimljenosectorforTrenutnocluster = sledećeDatotekacluster % 128
			var pokrenioffset = fatoffsetPrimljenosectorforTrenutnocluster * 4
			var krajoffset = fatoffsetPrimljenosectorforTrenutnocluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[pokrenioffset:krajoffset])

			sledećeDatotekacluster = int32(Unsignedinteger32r(Niztounsignedinteger32(buffer4)))
		}
	}
	memorijamanager.Slobodno(bpbPokazivač)
	memorijamanager.Slobodno(direntPokazivač)
}

type TDirektorijumunosfat32 struct {
	naziv			[8]byte
	ext			[3]byte
	attributes		uint8
	zauzeto			uint8
	cVremetenth		uint8
	cVreme			uint16
	cDatum			uint16
	aVreme			uint16
	firstclusterhi		uint16
	wVreme			uint16
	wDatum			uint16
	firstclusterTiho	uint16
	veličina		uint32
}

func (isti *TDirektorijumunosfat32) Init(data [32]byte) {
	copy(isti.naziv[:8], data[0:8])
	copy(isti.ext[:3], data[8:11])
	isti.attributes = data[11]
	isti.zauzeto = data[12]
	isti.cVremetenth = data[13]
	isti.cVreme = uint16(data[14]) | uint16(data[15])<<8
	isti.cDatum = uint16(data[16]) | uint16(data[17])<<8
	isti.aVreme = uint16(data[18]) | uint16(data[19])<<8
	isti.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	isti.wVreme = uint16(data[22]) | uint16(data[23])<<8
	isti.wDatum = uint16(data[24]) | uint16(data[25])<<8
	isti.firstclusterTiho = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	isti.veličina = Unsignedinteger32r(Niztounsignedinteger32(buffer))
}
