/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "fileSistema/msdospartition"
import . "memoriamanager"

type TParametri_del_file_system32 struct {
	jmp			[3]uint8
	softNome		[8]byte
	bytepersector		uint16
	sectorspercluster	uint8
	riservatosectors	uint16
	fatCopia		uint8
	radiceCartellavoce	uint16
	totalesectors		uint16
	supportiTipo		uint8
	fatsectorConteggio	uint16
	sectorpertrack		uint16
	headConteggio		uint16
	nascostisectors		uint32
	totalesectorConteggio	uint32

	tabellaDimensione	uint32
	extFlag			uint16
	fatVersione		uint16
	radicecluster		uint32
	fatInformazioni		uint16
	backupsector		uint16
	riservato0		[12]uint8
	driveNumero		uint8
	riservato		uint8
	bootsignature		uint8
	volumeid		uint32
	volumeetichetta		[11]byte
	fatTipoetichetta	[8]byte
}

func (séstesso *TParametri_del_file_system32) Init(data []byte) {
	copy(séstesso.jmp[:3], data[0:3])
	copy(séstesso.softNome[:8], data[3:11])

	séstesso.bytepersector = (uint16(data[11]) | uint16(data[12])<<8)
	séstesso.sectorspercluster = data[13]
	séstesso.riservatosectors = (uint16(data[14]) | uint16(data[15])<<8)
	séstesso.fatCopia = data[16]
	séstesso.radiceCartellavoce = (uint16(data[17]) | uint16(data[18])<<8)
	séstesso.totalesectors = (uint16(data[19]) | uint16(data[20])<<8)
	séstesso.supportiTipo = data[21]
	séstesso.fatsectorConteggio = (uint16(data[22]) | uint16(data[23])<<8)
	séstesso.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	séstesso.headConteggio = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	séstesso.nascostisectors = Unsignedinteger32r(Serietounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	séstesso.totalesectorConteggio = Unsignedinteger32r(Serietounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	séstesso.tabellaDimensione = Unsignedinteger32r(Serietounsignedinteger32(buffer1))

	séstesso.extFlag = (uint16(data[40]) | uint16(data[41])<<8)
	séstesso.fatVersione = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	séstesso.radicecluster = Unsignedinteger32r(Serietounsignedinteger32(buffer1))

	séstesso.fatInformazioni = (uint16(data[48]) | uint16(data[49])<<8)
	séstesso.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(séstesso.riservato0[:12], data[52:64])

	séstesso.driveNumero = data[64]
	séstesso.riservato = data[65]
	séstesso.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	séstesso.volumeid = Unsignedinteger32r(Serietounsignedinteger32(buffer1))

	copy(séstesso.volumeetichetta[:11], data[71:82])
	copy(séstesso.fatTipoetichetta[:8], data[82:90])

}

var console_2 = TConsole{}

func (séstesso *TParametri_del_file_system32) Len(hd *TAvanzateTecnologiaattachment, partvoce TPartitionTabellavoce, nomedelfile []byte) uint32 {

	if partvoce.Partitionid == 0x00 {
		return 0
	}

	memoriamanager := TMemoriamanager{}
	bpbPuntatore := memoriamanager.Alloca_memoria(90)
	bpbByte := GetBytefromPuntatore(uintptr(bpbPuntatore), 90, 90)
	var partitionoffset = partvoce.Avvialba

	hd.Lettura28(partitionoffset, &bpbByte, 90)

	var parametri_del_file_system = TParametri_del_file_system32{}
	parametri_del_file_system.Init(bpbByte)

	var fatAvvia = partitionoffset + uint32(parametri_del_file_system.riservatosectors)
	var fatDimensione = parametri_del_file_system.tabellaDimensione

	var dataAvvia = fatAvvia + fatDimensione*uint32(parametri_del_file_system.fatCopia)

	var radiceAvvia = dataAvvia + uint32(parametri_del_file_system.sectorspercluster)*(parametri_del_file_system.radicecluster-2)

	direntPuntatore := memoriamanager.Alloca_memoria(512)
	direntByte := GetBytefromPuntatore(uintptr(direntPuntatore), 512, 512)
	hd.Lettura28(radiceAvvia, &direntByte, 512)

	var dirent = [16]TCartellavocefat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nome[0] == 0x00 {
			break
		}

		if dirent[i].dimensione >= 0xFFFFFFFF {
			continue
		}

		if !UgualeByte(nomedelfile, dirent[i].nome[:len(nomedelfile)]) {
			continue
		}

		memoriamanager.Libero(bpbPuntatore)
		memoriamanager.Libero(direntPuntatore)
		return dirent[i].dimensione
	}
	memoriamanager.Libero(bpbPuntatore)
	memoriamanager.Libero(direntPuntatore)
	return 0
}
func (séstesso *TParametri_del_file_system32) Lettura(hd *TAvanzateTecnologiaattachment, partvoce TPartitionTabellavoce, nomedelfile []byte, data []byte) {

	if partvoce.Partitionid == 0x00 {
		return
	}

	memoriamanager := TMemoriamanager{}
	bpbPuntatore := memoriamanager.Alloca_memoria(90)
	bpbByte := GetBytefromPuntatore(uintptr(bpbPuntatore), 90, 90)
	var partitionoffset = partvoce.Avvialba

	hd.Lettura28(partitionoffset, &bpbByte, 90)

	var parametri_del_file_system = TParametri_del_file_system32{}
	parametri_del_file_system.Init(bpbByte)

	var fatAvvia = partitionoffset + uint32(parametri_del_file_system.riservatosectors)
	var fatDimensione = parametri_del_file_system.tabellaDimensione

	var dataAvvia = fatAvvia + fatDimensione*uint32(parametri_del_file_system.fatCopia)

	var radiceAvvia = dataAvvia + uint32(parametri_del_file_system.sectorspercluster)*(parametri_del_file_system.radicecluster-2)

	direntPuntatore := memoriamanager.Alloca_memoria(512)
	direntByte := GetBytefromPuntatore(uintptr(direntPuntatore), 512, 512)
	hd.Lettura28(radiceAvvia, &direntByte, 512)

	var dirent = [16]TCartellavocefat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nome[0] == 0x00 {
			break
		}

		if dirent[i].dimensione >= 0xFFFFFFFF {
			continue
		}

		if !UgualeByte(nomedelfile, dirent[i].nome[:len(nomedelfile)]) {
			continue
		}

		var firstfilecluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterBasso))

		var Dimensione = int32(dirent[i].dimensione)
		var successivofilecluster = int32(firstfilecluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Dimensione > 0 {
			var filesector = dataAvvia + uint32(parametri_del_file_system.sectorspercluster)*uint32(successivofilecluster-2)
			var sectoroffset int = 0

			for ; Dimensione > 0; Dimensione -= 512 {

				var buffer3 []byte

				if dirent[i].dimensione > 512 {
					buffer3 = buffer_2[:512]
					hd.Lettura28(filesector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].dimensione]
					hd.Lettura28(filesector+uint32(sectoroffset), &buffer3, int(dirent[i].dimensione))
				}

				copy(data[int32(dirent[i].dimensione)-Dimensione:], buffer3)

				sectoroffset++

				if sectoroffset > int(parametri_del_file_system.sectorspercluster) {
					break
				}

			}

			var fatsectorforCorrentecluster = uint32(successivofilecluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lettura28(fatAvvia+fatsectorforCorrentecluster, &fatbuf, 512)

			var fatoffsetIngressosectorforCorrentecluster = successivofilecluster % 128
			var avviaoffset = fatoffsetIngressosectorforCorrentecluster * 4
			var fineoffset = fatoffsetIngressosectorforCorrentecluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[avviaoffset:fineoffset])

			successivofilecluster = int32(Unsignedinteger32r(Serietounsignedinteger32(buffer4)))
		}
	}
	memoriamanager.Libero(bpbPuntatore)
	memoriamanager.Libero(direntPuntatore)
}

type TCartellavocefat32 struct {
	nome			[8]byte
	ext			[3]byte
	attributi		uint8
	riservato		uint8
	cOratenth		uint8
	cOra			uint16
	cData			uint16
	aOra			uint16
	firstclusterhi		uint16
	wOra			uint16
	wData			uint16
	firstclusterBasso	uint16
	dimensione		uint32
}

func (séstesso *TCartellavocefat32) Init(data [32]byte) {
	copy(séstesso.nome[:8], data[0:8])
	copy(séstesso.ext[:3], data[8:11])
	séstesso.attributi = data[11]
	séstesso.riservato = data[12]
	séstesso.cOratenth = data[13]
	séstesso.cOra = uint16(data[14]) | uint16(data[15])<<8
	séstesso.cData = uint16(data[16]) | uint16(data[17])<<8
	séstesso.aOra = uint16(data[18]) | uint16(data[19])<<8
	séstesso.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	séstesso.wOra = uint16(data[22]) | uint16(data[23])<<8
	séstesso.wData = uint16(data[24]) | uint16(data[25])<<8
	séstesso.firstclusterBasso = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	séstesso.dimensione = Unsignedinteger32r(Serietounsignedinteger32(buffer))
}
