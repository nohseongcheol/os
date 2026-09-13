package fat

import . "util"
import . "konsoli"
import . "driver/ata"
import . "tiedostoJärjestelmä/msdospartition"
import . "muistimanager"

type TTiedostojärjestelmän_parametrit32 struct {
	jmp			[3]uint8
	softNimi		[8]byte
	tavuapersector		uint16
	sectorspercluster	uint8
	varattusectors		uint16
	fatKopioi		uint8
	juuriKansiohakusana	uint16
	yhteensäsectors		uint16
	mediaTyyppi		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	piilotettusectors	uint32
	yhteensäsectorcount	uint32

	taulukkoKoko	uint32
	extLiput	uint16
	fatVersio	uint16
	juuricluster	uint32
	fatTieto	uint16
	backupsector	uint16
	varattu0	[12]uint8
	driveNumero	uint8
	varattu		uint8
	bootsignature	uint8
	määräTUNNISTE	uint32
	määräNimike	[11]byte
	fatTyyppiNimike	[8]byte
}

func (itse *TTiedostojärjestelmän_parametrit32) Init(data []byte) {
	copy(itse.jmp[:3], data[0:3])
	copy(itse.softNimi[:8], data[3:11])

	itse.tavuapersector = (uint16(data[11]) | uint16(data[12])<<8)
	itse.sectorspercluster = data[13]
	itse.varattusectors = (uint16(data[14]) | uint16(data[15])<<8)
	itse.fatKopioi = data[16]
	itse.juuriKansiohakusana = (uint16(data[17]) | uint16(data[18])<<8)
	itse.yhteensäsectors = (uint16(data[19]) | uint16(data[20])<<8)
	itse.mediaTyyppi = data[21]
	itse.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	itse.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	itse.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	itse.piilotettusectors = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	itse.yhteensäsectorcount = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	itse.taulukkoKoko = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer1))

	itse.extLiput = (uint16(data[40]) | uint16(data[41])<<8)
	itse.fatVersio = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	itse.juuricluster = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer1))

	itse.fatTieto = (uint16(data[48]) | uint16(data[49])<<8)
	itse.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(itse.varattu0[:12], data[52:64])

	itse.driveNumero = data[64]
	itse.varattu = data[65]
	itse.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	itse.määräTUNNISTE = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer1))

	copy(itse.määräNimike[:11], data[71:82])
	copy(itse.fatTyyppiNimike[:8], data[82:90])

}

var konsoli_2 = TKonsoli{}

func (itse *TTiedostojärjestelmän_parametrit32) Len(hd *TLisäasetuksetTekniikkaattachment, parthakusana TPartitionTaulukkohakusana, tiedostonimi []byte) uint32 {

	if parthakusana.PartitionTUNNISTE == 0x00 {
		return 0
	}

	muistimanager := TMuistimanager{}
	bpbOsoitin := muistimanager.Varaa_muistia(90)
	bpbtavua := GettavualähteestäOsoitin(uintptr(bpbOsoitin), 90, 90)
	var partitionoffset = parthakusana.Käynnistälba

	hd.Luku28(partitionoffset, &bpbtavua, 90)

	var tiedostojärjestelmän_parametrit = TTiedostojärjestelmän_parametrit32{}
	tiedostojärjestelmän_parametrit.Init(bpbtavua)

	var fatKäynnistä = partitionoffset + uint32(tiedostojärjestelmän_parametrit.varattusectors)
	var fatKoko = tiedostojärjestelmän_parametrit.taulukkoKoko

	var dataKäynnistä = fatKäynnistä + fatKoko*uint32(tiedostojärjestelmän_parametrit.fatKopioi)

	var juuriKäynnistä = dataKäynnistä + uint32(tiedostojärjestelmän_parametrit.sectorspercluster)*(tiedostojärjestelmän_parametrit.juuricluster-2)

	direntOsoitin := muistimanager.Varaa_muistia(512)
	direnttavua := GettavualähteestäOsoitin(uintptr(direntOsoitin), 512, 512)
	hd.Luku28(juuriKäynnistä, &direnttavua, 512)

	var dirent = [16]TKansiohakusanafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direnttavua[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nimi[0] == 0x00 {
			break
		}

		if dirent[i].koko >= 0xFFFFFFFF {
			continue
		}

		if !Samankokoinentavua(tiedostonimi, dirent[i].nimi[:len(tiedostonimi)]) {
			continue
		}

		muistimanager.Vapaana(bpbOsoitin)
		muistimanager.Vapaana(direntOsoitin)
		return dirent[i].koko
	}
	muistimanager.Vapaana(bpbOsoitin)
	muistimanager.Vapaana(direntOsoitin)
	return 0
}
func (itse *TTiedostojärjestelmän_parametrit32) Luku(hd *TLisäasetuksetTekniikkaattachment, parthakusana TPartitionTaulukkohakusana, tiedostonimi []byte, data []byte) {

	if parthakusana.PartitionTUNNISTE == 0x00 {
		return
	}

	muistimanager := TMuistimanager{}
	bpbOsoitin := muistimanager.Varaa_muistia(90)
	bpbtavua := GettavualähteestäOsoitin(uintptr(bpbOsoitin), 90, 90)
	var partitionoffset = parthakusana.Käynnistälba

	hd.Luku28(partitionoffset, &bpbtavua, 90)

	var tiedostojärjestelmän_parametrit = TTiedostojärjestelmän_parametrit32{}
	tiedostojärjestelmän_parametrit.Init(bpbtavua)

	var fatKäynnistä = partitionoffset + uint32(tiedostojärjestelmän_parametrit.varattusectors)
	var fatKoko = tiedostojärjestelmän_parametrit.taulukkoKoko

	var dataKäynnistä = fatKäynnistä + fatKoko*uint32(tiedostojärjestelmän_parametrit.fatKopioi)

	var juuriKäynnistä = dataKäynnistä + uint32(tiedostojärjestelmän_parametrit.sectorspercluster)*(tiedostojärjestelmän_parametrit.juuricluster-2)

	direntOsoitin := muistimanager.Varaa_muistia(512)
	direnttavua := GettavualähteestäOsoitin(uintptr(direntOsoitin), 512, 512)
	hd.Luku28(juuriKäynnistä, &direnttavua, 512)

	var dirent = [16]TKansiohakusanafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direnttavua[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nimi[0] == 0x00 {
			break
		}

		if dirent[i].koko >= 0xFFFFFFFF {
			continue
		}

		if !Samankokoinentavua(tiedostonimi, dirent[i].nimi[:len(tiedostonimi)]) {
			continue
		}

		var firstTiedostocluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterMatala))

		var Koko = int32(dirent[i].koko)
		var seuraavaTiedostocluster = int32(firstTiedostocluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Koko > 0 {
			var tiedostosector = dataKäynnistä + uint32(tiedostojärjestelmän_parametrit.sectorspercluster)*uint32(seuraavaTiedostocluster-2)
			var sectoroffset int = 0

			for ; Koko > 0; Koko -= 512 {

				var buffer3 []byte

				if dirent[i].koko > 512 {
					buffer3 = buffer_2[:512]
					hd.Luku28(tiedostosector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].koko]
					hd.Luku28(tiedostosector+uint32(sectoroffset), &buffer3, int(dirent[i].koko))
				}

				copy(data[int32(dirent[i].koko)-Koko:], buffer3)

				sectoroffset++

				if sectoroffset > int(tiedostojärjestelmän_parametrit.sectorspercluster) {
					break
				}

			}

			var fatsectorforNykyinencluster = uint32(seuraavaTiedostocluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Luku28(fatKäynnistä+fatsectorforNykyinencluster, &fatbuf, 512)

			var fatoffsetSaapuvasectorforNykyinencluster = seuraavaTiedostocluster % 128
			var käynnistäoffset = fatoffsetSaapuvasectorforNykyinencluster * 4
			var loppuajankohtaoffset = fatoffsetSaapuvasectorforNykyinencluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[käynnistäoffset:loppuajankohtaoffset])

			seuraavaTiedostocluster = int32(Unsignedinteger32r(Taulukkotounsignedinteger32(buffer4)))
		}
	}
	muistimanager.Vapaana(bpbOsoitin)
	muistimanager.Vapaana(direntOsoitin)
}

type TKansiohakusanafat32 struct {
	nimi			[8]byte
	ext			[3]byte
	attribuutit		uint8
	varattu			uint8
	cAikatenth		uint8
	cAika			uint16
	cPäiväys		uint16
	aAika			uint16
	firstclusterhi		uint16
	wAika			uint16
	wPäiväys		uint16
	firstclusterMatala	uint16
	koko			uint32
}

func (itse *TKansiohakusanafat32) Init(data [32]byte) {
	copy(itse.nimi[:8], data[0:8])
	copy(itse.ext[:3], data[8:11])
	itse.attribuutit = data[11]
	itse.varattu = data[12]
	itse.cAikatenth = data[13]
	itse.cAika = uint16(data[14]) | uint16(data[15])<<8
	itse.cPäiväys = uint16(data[16]) | uint16(data[17])<<8
	itse.aAika = uint16(data[18]) | uint16(data[19])<<8
	itse.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	itse.wAika = uint16(data[22]) | uint16(data[23])<<8
	itse.wPäiväys = uint16(data[24]) | uint16(data[25])<<8
	itse.firstclusterMatala = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	itse.koko = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer))
}
