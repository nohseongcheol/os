/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "konsola"
import . "driver/ata"
import . "plikSystemowe/msdospartition"
import . "pamięćmanager"

type TParametry_systemu_plików32 struct {
	jmp				[3]uint8
	softNazwa			[8]byte
	bajtypersector			uint16
	sectorspercluster		uint8
	zastrzeżonesectors		uint16
	fatKopiuj			uint8
	elementgłównyKatalogwpis	uint16
	łączniesectors			uint16
	nośnikiTyp			uint8
	fatsectorLiczba			uint16
	sectorpertrack			uint16
	headLiczba			uint16
	ukrytesectors			uint32
	łączniesectorLiczba		uint32

	tabelaRozmiar		uint32
	extZnaczniki		uint16
	fatWersja		uint16
	elementgłównycluster	uint32
	fatInformacja		uint16
	backupsector		uint16
	zastrzeżone0		[12]uint8
	driveLiczba		uint8
	zastrzeżone		uint8
	bootsignature		uint8
	głośnośćIdentyfikator	uint32
	głośnośćetykieta	[11]byte
	fatTypetykieta		[8]byte
}

func (bieżący *TParametry_systemu_plików32) Init(data []byte) {
	copy(bieżący.jmp[:3], data[0:3])
	copy(bieżący.softNazwa[:8], data[3:11])

	bieżący.bajtypersector = (uint16(data[11]) | uint16(data[12])<<8)
	bieżący.sectorspercluster = data[13]
	bieżący.zastrzeżonesectors = (uint16(data[14]) | uint16(data[15])<<8)
	bieżący.fatKopiuj = data[16]
	bieżący.elementgłównyKatalogwpis = (uint16(data[17]) | uint16(data[18])<<8)
	bieżący.łączniesectors = (uint16(data[19]) | uint16(data[20])<<8)
	bieżący.nośnikiTyp = data[21]
	bieżący.fatsectorLiczba = (uint16(data[22]) | uint16(data[23])<<8)
	bieżący.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	bieżący.headLiczba = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	bieżący.ukrytesectors = Unsignedinteger32r(Tablicatounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	bieżący.łączniesectorLiczba = Unsignedinteger32r(Tablicatounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	bieżący.tabelaRozmiar = Unsignedinteger32r(Tablicatounsignedinteger32(buffer1))

	bieżący.extZnaczniki = (uint16(data[40]) | uint16(data[41])<<8)
	bieżący.fatWersja = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	bieżący.elementgłównycluster = Unsignedinteger32r(Tablicatounsignedinteger32(buffer1))

	bieżący.fatInformacja = (uint16(data[48]) | uint16(data[49])<<8)
	bieżący.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(bieżący.zastrzeżone0[:12], data[52:64])

	bieżący.driveLiczba = data[64]
	bieżący.zastrzeżone = data[65]
	bieżący.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	bieżący.głośnośćIdentyfikator = Unsignedinteger32r(Tablicatounsignedinteger32(buffer1))

	copy(bieżący.głośnośćetykieta[:11], data[71:82])
	copy(bieżący.fatTypetykieta[:8], data[82:90])

}

var konsola_2 = TKonsola{}

func (bieżący *TParametry_systemu_plików32) Len(hd *TZaawansowaneTechnologiaattachment, partwpis TPartitionTabelawpis, nazwapliku []byte) uint32 {

	if partwpis.PartitionIdentyfikator == 0x00 {
		return 0
	}

	pamięćmanager := TPamięćmanager{}
	bpbKursor := pamięćmanager.Przydziel_pamięć(90)
	bpbBajty := GetBajtyzKursor(uintptr(bpbKursor), 90, 90)
	var partitionPrzesunięcie = partwpis.Uruchomlba

	hd.Odczyt28(partitionPrzesunięcie, &bpbBajty, 90)

	var parametry_systemu_plików = TParametry_systemu_plików32{}
	parametry_systemu_plików.Init(bpbBajty)

	var fatUruchom = partitionPrzesunięcie + uint32(parametry_systemu_plików.zastrzeżonesectors)
	var fatRozmiar = parametry_systemu_plików.tabelaRozmiar

	var dataUruchom = fatUruchom + fatRozmiar*uint32(parametry_systemu_plików.fatKopiuj)

	var elementgłównyUruchom = dataUruchom + uint32(parametry_systemu_plików.sectorspercluster)*(parametry_systemu_plików.elementgłównycluster-2)

	direntKursor := pamięćmanager.Przydziel_pamięć(512)
	direntBajty := GetBajtyzKursor(uintptr(direntKursor), 512, 512)
	hd.Odczyt28(elementgłównyUruchom, &direntBajty, 512)

	var dirent = [16]TKatalogwpisfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajty[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nazwa[0] == 0x00 {
			break
		}

		if dirent[i].rozmiar >= 0xFFFFFFFF {
			continue
		}

		if !OdpowiedniBajty(nazwapliku, dirent[i].nazwa[:len(nazwapliku)]) {
			continue
		}

		pamięćmanager.Wolne(bpbKursor)
		pamięćmanager.Wolne(direntKursor)
		return dirent[i].rozmiar
	}
	pamięćmanager.Wolne(bpbKursor)
	pamięćmanager.Wolne(direntKursor)
	return 0
}
func (bieżący *TParametry_systemu_plików32) Odczyt(hd *TZaawansowaneTechnologiaattachment, partwpis TPartitionTabelawpis, nazwapliku []byte, data []byte) {

	if partwpis.PartitionIdentyfikator == 0x00 {
		return
	}

	pamięćmanager := TPamięćmanager{}
	bpbKursor := pamięćmanager.Przydziel_pamięć(90)
	bpbBajty := GetBajtyzKursor(uintptr(bpbKursor), 90, 90)
	var partitionPrzesunięcie = partwpis.Uruchomlba

	hd.Odczyt28(partitionPrzesunięcie, &bpbBajty, 90)

	var parametry_systemu_plików = TParametry_systemu_plików32{}
	parametry_systemu_plików.Init(bpbBajty)

	var fatUruchom = partitionPrzesunięcie + uint32(parametry_systemu_plików.zastrzeżonesectors)
	var fatRozmiar = parametry_systemu_plików.tabelaRozmiar

	var dataUruchom = fatUruchom + fatRozmiar*uint32(parametry_systemu_plików.fatKopiuj)

	var elementgłównyUruchom = dataUruchom + uint32(parametry_systemu_plików.sectorspercluster)*(parametry_systemu_plików.elementgłównycluster-2)

	direntKursor := pamięćmanager.Przydziel_pamięć(512)
	direntBajty := GetBajtyzKursor(uintptr(direntKursor), 512, 512)
	hd.Odczyt28(elementgłównyUruchom, &direntBajty, 512)

	var dirent = [16]TKatalogwpisfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBajty[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nazwa[0] == 0x00 {
			break
		}

		if dirent[i].rozmiar >= 0xFFFFFFFF {
			continue
		}

		if !OdpowiedniBajty(nazwapliku, dirent[i].nazwa[:len(nazwapliku)]) {
			continue
		}

		var firstPlikcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterNiski))

		var Rozmiar = int32(dirent[i].rozmiar)
		var następnyPlikcluster = int32(firstPlikcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Rozmiar > 0 {
			var pliksector = dataUruchom + uint32(parametry_systemu_plików.sectorspercluster)*uint32(następnyPlikcluster-2)
			var sectorPrzesunięcie int = 0

			for ; Rozmiar > 0; Rozmiar -= 512 {

				var buffer3 []byte

				if dirent[i].rozmiar > 512 {
					buffer3 = buffer_2[:512]
					hd.Odczyt28(pliksector+uint32(sectorPrzesunięcie), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].rozmiar]
					hd.Odczyt28(pliksector+uint32(sectorPrzesunięcie), &buffer3, int(dirent[i].rozmiar))
				}

				copy(data[int32(dirent[i].rozmiar)-Rozmiar:], buffer3)

				sectorPrzesunięcie++

				if sectorPrzesunięcie > int(parametry_systemu_plików.sectorspercluster) {
					break
				}

			}

			var fatsectorforBieżącycluster = uint32(następnyPlikcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Odczyt28(fatUruchom+fatsectorforBieżącycluster, &fatbuf, 512)

			var fatPrzesunięcieWchodzącysectorforBieżącycluster = następnyPlikcluster % 128
			var uruchomPrzesunięcie = fatPrzesunięcieWchodzącysectorforBieżącycluster * 4
			var koniecPrzesunięcie = fatPrzesunięcieWchodzącysectorforBieżącycluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[uruchomPrzesunięcie:koniecPrzesunięcie])

			następnyPlikcluster = int32(Unsignedinteger32r(Tablicatounsignedinteger32(buffer4)))
		}
	}
	pamięćmanager.Wolne(bpbKursor)
	pamięćmanager.Wolne(direntKursor)
}

type TKatalogwpisfat32 struct {
	nazwa			[8]byte
	ext			[3]byte
	atrybuty		uint8
	zastrzeżone		uint8
	cCzastenth		uint8
	cCzas			uint16
	cData			uint16
	aCzas			uint16
	firstclusterhi		uint16
	wCzas			uint16
	wData			uint16
	firstclusterNiski	uint16
	rozmiar			uint32
}

func (bieżący *TKatalogwpisfat32) Init(data [32]byte) {
	copy(bieżący.nazwa[:8], data[0:8])
	copy(bieżący.ext[:3], data[8:11])
	bieżący.atrybuty = data[11]
	bieżący.zastrzeżone = data[12]
	bieżący.cCzastenth = data[13]
	bieżący.cCzas = uint16(data[14]) | uint16(data[15])<<8
	bieżący.cData = uint16(data[16]) | uint16(data[17])<<8
	bieżący.aCzas = uint16(data[18]) | uint16(data[19])<<8
	bieżący.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	bieżący.wCzas = uint16(data[22]) | uint16(data[23])<<8
	bieżący.wData = uint16(data[24]) | uint16(data[25])<<8
	bieżący.firstclusterNiski = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	bieżący.rozmiar = Unsignedinteger32r(Tablicatounsignedinteger32(buffer))
}
