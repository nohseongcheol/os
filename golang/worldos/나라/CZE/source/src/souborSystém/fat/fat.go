/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "konzole"
import . "driver/ata"
import . "souborSystém/msdospartition"
import . "paměťmanager"

type TParametry_souborového_systému32 struct {
	jmp			[3]uint8
	softNázev		[8]byte
	bytůpersector		uint16
	sectorspercluster	uint8
	reservovanásectors	uint16
	fatKopírovat		uint8
	kořenadresářZáznam	uint16
	celkemsectors		uint16
	médiaTyp		uint8
	fatsectorPočet		uint16
	sectorpertrack		uint16
	headPočet		uint16
	skrytásectors		uint32
	celkemsectorPočet	uint32

	tabulkaVelikost		uint32
	extPříznaky		uint16
	fatVerze		uint16
	kořencluster		uint32
	fatInformace		uint16
	backupsector		uint16
	reservovaná0		[12]uint8
	driveČíslo		uint8
	reservovaná		uint8
	bootsignature		uint8
	hlasitostid		uint32
	hlasitostPopisek	[11]byte
	fatTypPopisek		[8]byte
}

func (self *TParametry_souborového_systému32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softNázev[:8], data[3:11])

	self.bytůpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservovanásectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatKopírovat = data[16]
	self.kořenadresářZáznam = (uint16(data[17]) | uint16(data[18])<<8)
	self.celkemsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.médiaTyp = data[21]
	self.fatsectorPočet = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headPočet = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.skrytásectors = Unsignedinteger32r(Poledounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.celkemsectorPočet = Unsignedinteger32r(Poledounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tabulkaVelikost = Unsignedinteger32r(Poledounsignedinteger32(buffer1))

	self.extPříznaky = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatVerze = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.kořencluster = Unsignedinteger32r(Poledounsignedinteger32(buffer1))

	self.fatInformace = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reservovaná0[:12], data[52:64])

	self.driveČíslo = data[64]
	self.reservovaná = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.hlasitostid = Unsignedinteger32r(Poledounsignedinteger32(buffer1))

	copy(self.hlasitostPopisek[:11], data[71:82])
	copy(self.fatTypPopisek[:8], data[82:90])

}

var konzole_2 = TKonzole{}

func (self *TParametry_souborového_systému32) Len(hd *TPokročiléTechnologieattachment, partZáznam TPartitionTabulkaZáznam, názevsouboru []byte) uint32 {

	if partZáznam.Partitionid == 0x00 {
		return 0
	}

	paměťmanager := TPaměťmanager{}
	bpbKurzor := paměťmanager.Přidělit_paměť(90)
	bpbBytů := GetBytůzKurzor(uintptr(bpbKurzor), 90, 90)
	var partitionoffset = partZáznam.Spustitlba

	hd.Čtení28(partitionoffset, &bpbBytů, 90)

	var parametry_souborového_systému = TParametry_souborového_systému32{}
	parametry_souborového_systému.Init(bpbBytů)

	var fatSpustit = partitionoffset + uint32(parametry_souborového_systému.reservovanásectors)
	var fatVelikost = parametry_souborového_systému.tabulkaVelikost

	var dataSpustit = fatSpustit + fatVelikost*uint32(parametry_souborového_systému.fatKopírovat)

	var kořenSpustit = dataSpustit + uint32(parametry_souborového_systému.sectorspercluster)*(parametry_souborového_systému.kořencluster-2)

	direntKurzor := paměťmanager.Přidělit_paměť(512)
	direntBytů := GetBytůzKurzor(uintptr(direntKurzor), 512, 512)
	hd.Čtení28(kořenSpustit, &direntBytů, 512)

	var dirent = [16]TAdresářZáznamfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBytů[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].název[0] == 0x00 {
			break
		}

		if dirent[i].velikost >= 0xFFFFFFFF {
			continue
		}

		if !TotožnéBytů(názevsouboru, dirent[i].název[:len(názevsouboru)]) {
			continue
		}

		paměťmanager.Volné(bpbKurzor)
		paměťmanager.Volné(direntKurzor)
		return dirent[i].velikost
	}
	paměťmanager.Volné(bpbKurzor)
	paměťmanager.Volné(direntKurzor)
	return 0
}
func (self *TParametry_souborového_systému32) Čtení(hd *TPokročiléTechnologieattachment, partZáznam TPartitionTabulkaZáznam, názevsouboru []byte, data []byte) {

	if partZáznam.Partitionid == 0x00 {
		return
	}

	paměťmanager := TPaměťmanager{}
	bpbKurzor := paměťmanager.Přidělit_paměť(90)
	bpbBytů := GetBytůzKurzor(uintptr(bpbKurzor), 90, 90)
	var partitionoffset = partZáznam.Spustitlba

	hd.Čtení28(partitionoffset, &bpbBytů, 90)

	var parametry_souborového_systému = TParametry_souborového_systému32{}
	parametry_souborového_systému.Init(bpbBytů)

	var fatSpustit = partitionoffset + uint32(parametry_souborového_systému.reservovanásectors)
	var fatVelikost = parametry_souborového_systému.tabulkaVelikost

	var dataSpustit = fatSpustit + fatVelikost*uint32(parametry_souborového_systému.fatKopírovat)

	var kořenSpustit = dataSpustit + uint32(parametry_souborového_systému.sectorspercluster)*(parametry_souborového_systému.kořencluster-2)

	direntKurzor := paměťmanager.Přidělit_paměť(512)
	direntBytů := GetBytůzKurzor(uintptr(direntKurzor), 512, 512)
	hd.Čtení28(kořenSpustit, &direntBytů, 512)

	var dirent = [16]TAdresářZáznamfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBytů[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].název[0] == 0x00 {
			break
		}

		if dirent[i].velikost >= 0xFFFFFFFF {
			continue
		}

		if !TotožnéBytů(názevsouboru, dirent[i].název[:len(názevsouboru)]) {
			continue
		}

		var firstSouborcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterNízká))

		var Velikost = int32(dirent[i].velikost)
		var následujícíSouborcluster = int32(firstSouborcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Velikost > 0 {
			var souborsector = dataSpustit + uint32(parametry_souborového_systému.sectorspercluster)*uint32(následujícíSouborcluster-2)
			var sectoroffset int = 0

			for ; Velikost > 0; Velikost -= 512 {

				var buffer3 []byte

				if dirent[i].velikost > 512 {
					buffer3 = buffer_2[:512]
					hd.Čtení28(souborsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].velikost]
					hd.Čtení28(souborsector+uint32(sectoroffset), &buffer3, int(dirent[i].velikost))
				}

				copy(data[int32(dirent[i].velikost)-Velikost:], buffer3)

				sectoroffset++

				if sectoroffset > int(parametry_souborového_systému.sectorspercluster) {
					break
				}

			}

			var fatsectorforSoučasnýcluster = uint32(následujícíSouborcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Čtení28(fatSpustit+fatsectorforSoučasnýcluster, &fatbuf, 512)

			var fatoffsetVstupsectorforSoučasnýcluster = následujícíSouborcluster % 128
			var spustitoffset = fatoffsetVstupsectorforSoučasnýcluster * 4
			var konecoffset = fatoffsetVstupsectorforSoučasnýcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[spustitoffset:konecoffset])

			následujícíSouborcluster = int32(Unsignedinteger32r(Poledounsignedinteger32(buffer4)))
		}
	}
	paměťmanager.Volné(bpbKurzor)
	paměťmanager.Volné(direntKurzor)
}

type TAdresářZáznamfat32 struct {
	název			[8]byte
	ext			[3]byte
	atributy		uint8
	reservovaná		uint8
	cČastenth		uint8
	cČas			uint16
	cDatum			uint16
	aČas			uint16
	firstclusterhi		uint16
	wČas			uint16
	wDatum			uint16
	firstclusterNízká	uint16
	velikost		uint32
}

func (self *TAdresářZáznamfat32) Init(data [32]byte) {
	copy(self.název[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.atributy = data[11]
	self.reservovaná = data[12]
	self.cČastenth = data[13]
	self.cČas = uint16(data[14]) | uint16(data[15])<<8
	self.cDatum = uint16(data[16]) | uint16(data[17])<<8
	self.aČas = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wČas = uint16(data[22]) | uint16(data[23])<<8
	self.wDatum = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterNízká = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.velikost = Unsignedinteger32r(Poledounsignedinteger32(buffer))
}
