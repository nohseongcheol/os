/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "consola"
import . "driver/ata"
import . "fitxerSistema/msdospartition"
import . "memòriamanager"

type TBiosparameterBloc32 struct {
	jmp			[3]uint8
	softNom			[8]byte
	bytespersector		uint16
	sectorspercluster	uint8
	reservatsectors		uint16
	fatCopia		uint8
	arrelDirectorientrada	uint16
	totalsectors		uint16
	mitjansTipus		uint8
	fatsectorRecompte	uint16
	sectorpertrack		uint16
	headRecompte		uint16
	ocultsectors		uint32
	totalsectorRecompte	uint32

	taulaMida		uint32
	extSenyaladors		uint16
	fatVersió		uint16
	arrelcluster		uint32
	fatInformació		uint16
	backupsector		uint16
	reservat0		[12]uint8
	driveNombre		uint8
	reservat		uint8
	bootsignature		uint8
	volumIdentificador	uint32
	volumetiqueta		[11]byte
	fatTipusetiqueta	[8]byte
}

func (unmateix *TBiosparameterBloc32) Init(data []byte) {
	copy(unmateix.jmp[:3], data[0:3])
	copy(unmateix.softNom[:8], data[3:11])

	unmateix.bytespersector = (uint16(data[11]) | uint16(data[12])<<8)
	unmateix.sectorspercluster = data[13]
	unmateix.reservatsectors = (uint16(data[14]) | uint16(data[15])<<8)
	unmateix.fatCopia = data[16]
	unmateix.arrelDirectorientrada = (uint16(data[17]) | uint16(data[18])<<8)
	unmateix.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	unmateix.mitjansTipus = data[21]
	unmateix.fatsectorRecompte = (uint16(data[22]) | uint16(data[23])<<8)
	unmateix.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	unmateix.headRecompte = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	unmateix.ocultsectors = Unsignedinteger32r(Matriutounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	unmateix.totalsectorRecompte = Unsignedinteger32r(Matriutounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	unmateix.taulaMida = Unsignedinteger32r(Matriutounsignedinteger32(buffer1))

	unmateix.extSenyaladors = (uint16(data[40]) | uint16(data[41])<<8)
	unmateix.fatVersió = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	unmateix.arrelcluster = Unsignedinteger32r(Matriutounsignedinteger32(buffer1))

	unmateix.fatInformació = (uint16(data[48]) | uint16(data[49])<<8)
	unmateix.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(unmateix.reservat0[:12], data[52:64])

	unmateix.driveNombre = data[64]
	unmateix.reservat = data[65]
	unmateix.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	unmateix.volumIdentificador = Unsignedinteger32r(Matriutounsignedinteger32(buffer1))

	copy(unmateix.volumetiqueta[:11], data[71:82])
	copy(unmateix.fatTipusetiqueta[:8], data[82:90])

}

var consola_2 = TConsola{}

func (unmateix *TBiosparameterBloc32) Len(hd *TAvançatTecnologiaattachment, partentrada TPartitionTaulaentrada, nomdelfitxer []byte) uint32 {

	if partentrada.PartitionIdentificador == 0x00 {
		return 0
	}

	memòriamanager := TMemòriamanager{}
	bpbPunter := memòriamanager.Malloc(90)
	bpbbytes := GetbytesdesdePunter(uintptr(bpbPunter), 90, 90)
	var partitionoffset = partentrada.Inicialba

	hd.Lectura28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterBloc32{}
	bpb.Init(bpbbytes)

	var fatInicia = partitionoffset + uint32(bpb.reservatsectors)
	var fatMida = bpb.taulaMida

	var dataInicia = fatInicia + fatMida*uint32(bpb.fatCopia)

	var arrelInicia = dataInicia + uint32(bpb.sectorspercluster)*(bpb.arrelcluster-2)

	direntPunter := memòriamanager.Malloc(512)
	direntbytes := GetbytesdesdePunter(uintptr(direntPunter), 512, 512)
	hd.Lectura28(arrelInicia, &direntbytes, 512)

	var dirent = [16]TDirectorientradafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nom[0] == 0x00 {
			break
		}

		if dirent[i].mida >= 0xFFFFFFFF {
			continue
		}

		if !Igualbytes(nomdelfitxer, dirent[i].nom[:len(nomdelfitxer)]) {
			continue
		}

		memòriamanager.Lliure(bpbPunter)
		memòriamanager.Lliure(direntPunter)
		return dirent[i].mida
	}
	memòriamanager.Lliure(bpbPunter)
	memòriamanager.Lliure(direntPunter)
	return 0
}
func (unmateix *TBiosparameterBloc32) Lectura(hd *TAvançatTecnologiaattachment, partentrada TPartitionTaulaentrada, nomdelfitxer []byte, data []byte) {

	if partentrada.PartitionIdentificador == 0x00 {
		return
	}

	memòriamanager := TMemòriamanager{}
	bpbPunter := memòriamanager.Malloc(90)
	bpbbytes := GetbytesdesdePunter(uintptr(bpbPunter), 90, 90)
	var partitionoffset = partentrada.Inicialba

	hd.Lectura28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterBloc32{}
	bpb.Init(bpbbytes)

	var fatInicia = partitionoffset + uint32(bpb.reservatsectors)
	var fatMida = bpb.taulaMida

	var dataInicia = fatInicia + fatMida*uint32(bpb.fatCopia)

	var arrelInicia = dataInicia + uint32(bpb.sectorspercluster)*(bpb.arrelcluster-2)

	direntPunter := memòriamanager.Malloc(512)
	direntbytes := GetbytesdesdePunter(uintptr(direntPunter), 512, 512)
	hd.Lectura28(arrelInicia, &direntbytes, 512)

	var dirent = [16]TDirectorientradafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nom[0] == 0x00 {
			break
		}

		if dirent[i].mida >= 0xFFFFFFFF {
			continue
		}

		if !Igualbytes(nomdelfitxer, dirent[i].nom[:len(nomdelfitxer)]) {
			continue
		}

		var firstFitxercluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterBaixa))

		var Mida = int32(dirent[i].mida)
		var següentFitxercluster = int32(firstFitxercluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Mida > 0 {
			var fitxersector = dataInicia + uint32(bpb.sectorspercluster)*uint32(següentFitxercluster-2)
			var sectoroffset int = 0

			for ; Mida > 0; Mida -= 512 {

				var buffer3 []byte

				if dirent[i].mida > 512 {
					buffer3 = buffer_2[:512]
					hd.Lectura28(fitxersector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].mida]
					hd.Lectura28(fitxersector+uint32(sectoroffset), &buffer3, int(dirent[i].mida))
				}

				copy(data[int32(dirent[i].mida)-Mida:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforActualcluster = uint32(següentFitxercluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lectura28(fatInicia+fatsectorforActualcluster, &fatbuf, 512)

			var fatoffsetasectorforActualcluster = següentFitxercluster % 128
			var iniciaoffset = fatoffsetasectorforActualcluster * 4
			var finaloffset = fatoffsetasectorforActualcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[iniciaoffset:finaloffset])

			següentFitxercluster = int32(Unsignedinteger32r(Matriutounsignedinteger32(buffer4)))
		}
	}
	memòriamanager.Lliure(bpbPunter)
	memòriamanager.Lliure(direntPunter)
}

type TDirectorientradafat32 struct {
	nom			[8]byte
	ext			[3]byte
	atributs		uint8
	reservat		uint8
	cHoratenth		uint8
	cHora			uint16
	cData			uint16
	aHora			uint16
	firstclusterhi		uint16
	wHora			uint16
	wData			uint16
	firstclusterBaixa	uint16
	mida			uint32
}

func (unmateix *TDirectorientradafat32) Init(data [32]byte) {
	copy(unmateix.nom[:8], data[0:8])
	copy(unmateix.ext[:3], data[8:11])
	unmateix.atributs = data[11]
	unmateix.reservat = data[12]
	unmateix.cHoratenth = data[13]
	unmateix.cHora = uint16(data[14]) | uint16(data[15])<<8
	unmateix.cData = uint16(data[16]) | uint16(data[17])<<8
	unmateix.aHora = uint16(data[18]) | uint16(data[19])<<8
	unmateix.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	unmateix.wHora = uint16(data[22]) | uint16(data[23])<<8
	unmateix.wData = uint16(data[24]) | uint16(data[25])<<8
	unmateix.firstclusterBaixa = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	unmateix.mida = Unsignedinteger32r(Matriutounsignedinteger32(buffer))
}
