/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "konzola"

const Bajtypersector int = 512

type TPokročiléTechnológiaattachment struct {
	hlavný		bool
	dataport	TPort16bit
	chybaport	TPort8bit
	sectorcountport	TPort8bit
	lbaNízkaport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	zariadenieport	TPort8bit
	príkazport	TPort8bit
	ovládanieport	TPort8bit
}

func (vlastný *TPokročiléTechnológiaattachment) Init(hlavný bool, portbase uint16) {
	vlastný.hlavný = hlavný
	vlastný.dataport.Init(portbase)
	vlastný.chybaport.Init(portbase + 0x1)
	vlastný.sectorcountport.Init(portbase + 0x2)
	vlastný.lbaNízkaport.Init(portbase + 0x3)
	vlastný.lbamidport.Init(portbase + 0x4)
	vlastný.lbahiport.Init(portbase + 0x5)
	vlastný.zariadenieport.Init(portbase + 0x6)
	vlastný.príkazport.Init(portbase + 0x7)
	vlastný.ovládanieport.Init(portbase + 0x8)

}

func (vlastný *TPokročiléTechnológiaattachment) Identify() {

	var konzola_2 = TKonzola{}

	if vlastný.hlavný {
		vlastný.zariadenieport.Zápis(0xA0)
	} else {
		vlastný.zariadenieport.Zápis(0xB0)
	}
	vlastný.ovládanieport.Zápis(0)
	vlastný.zariadenieport.Zápis(0xA0)

	var stav uint8 = vlastný.príkazport.Čítanie()
	if stav == 0xFF {
		konzola_2.MTlačiť(([]byte)("Invalid Status"))
		return
	}

	if vlastný.hlavný {
		vlastný.zariadenieport.Zápis(0xA0)
	} else {
		vlastný.zariadenieport.Zápis(0xB0)
	}
	vlastný.sectorcountport.Zápis(0)
	vlastný.lbaNízkaport.Zápis(0)
	vlastný.lbamidport.Zápis(0)
	vlastný.lbahiport.Zápis(0)
	vlastný.príkazport.Zápis(0xEC)

	stav = vlastný.príkazport.Čítanie()
	if stav == 0x00 {
		konzola_2.MTlačiť(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (stav&0x80) == 0x80 && (stav&0x01) != 0x01 {
		stav = vlastný.príkazport.Čítanie()
	}

	if (stav & 0x01) != 0 {
		konzola_2.MTlačiť(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = vlastný.dataport.Čítanie()
		spracovanietextu := []byte("  ")
		spracovanietextu[0] = uint8((data >> 8) & 0xFF)
		spracovanietextu[1] = uint8(data & 0xFF)

	}
	konzola_2.MTlačiťxy(([]byte)("ata ok"), 10, 22)

}
func (vlastný *TPokročiléTechnológiaattachment) Čítanie28(sector uint32, data *[]byte, count int) {
	var konzola_2 = TKonzola{}
	if (sector & 0xF0000000) != 0 {
		konzola_2.MTlačiť(([]byte)("ata read error "))
		return
	}
	if count > Bajtypersector {
		konzola_2.MTlačiť(([]byte)("ata read error "))
		return
	}

	if vlastný.hlavný {
		vlastný.zariadenieport.Zápis(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		vlastný.zariadenieport.Zápis(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	vlastný.chybaport.Zápis(0)
	vlastný.sectorcountport.Zápis(1)

	vlastný.lbaNízkaport.Zápis(uint8(sector & 0x000000FF))
	vlastný.lbamidport.Zápis(uint8((sector & 0x0000FF00) >> 8))
	vlastný.lbahiport.Zápis(uint8((sector & 0x00FF0000) >> 16))
	vlastný.príkazport.Zápis(0x20)

	var stav uint8 = vlastný.príkazport.Čítanie()
	for ((stav & 0x80) == 0x80) && ((stav & 0x01) != 0x01) {
		stav = vlastný.príkazport.Čítanie()
	}

	if (stav & 0x01) != 0 {
		konzola_2.MTlačiť(([]byte)("ata read error "))
		return
	}

	konzola_2.MTlačiťxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = vlastný.dataport.Čítanie()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bajtypersector; i += 2 {
		vlastný.dataport.Čítanie()
	}
}
func (vlastný *TPokročiléTechnológiaattachment) Zápis28(sectorČíslo uint32, data []byte, count uint32) {

	if sectorČíslo > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if vlastný.hlavný {
		vlastný.zariadenieport.Zápis(uint8(0xE0 | uint8((sectorČíslo&0x0F000000)>>24)))
	} else {
		vlastný.zariadenieport.Zápis(uint8(0xF0 | uint8((sectorČíslo&0x0F000000)>>24)))
	}

	vlastný.chybaport.Zápis(0)
	vlastný.sectorcountport.Zápis(1)
	vlastný.lbaNízkaport.Zápis(uint8(sectorČíslo & 0x000000FF))
	vlastný.lbamidport.Zápis(uint8((sectorČíslo & 0x0000FF00) >> 8))
	vlastný.lbahiport.Zápis(uint8((sectorČíslo & 0x00FF0000) >> 16))
	vlastný.príkazport.Zápis(0x30)

	var konzola_2 = TKonzola{}
	konzola_2.MTlačiť(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		vlastný.dataport.Zápis(wdata)

		spracovanietextu := []byte("  ")
		spracovanietextu[0] = uint8((wdata >> 8) & 0xFF)
		spracovanietextu[1] = uint8(wdata & 0xFF)

		konzola_2.MTlačiť(spracovanietextu)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		vlastný.dataport.Zápis(0x0000)
	}

}

func (vlastný *TPokročiléTechnológiaattachment) Flush() {
	if vlastný.hlavný {
		vlastný.zariadenieport.Zápis(0xE0)
	} else {
		vlastný.zariadenieport.Zápis(0xF0)
	}
	vlastný.príkazport.Zápis(0xE7)

	var konzola_2 = TKonzola{}

	var stav uint8 = vlastný.príkazport.Čítanie()
	if stav == 0x00 {
		return
	}

	for ((stav & 0x80) == 0x80) && ((stav & 0x01) != 0x01) {
		stav = vlastný.príkazport.Čítanie()
	}
	if (stav & 0x01) != 0 {
		konzola_2.MTlačiť(([]byte)(" ata flush error"))
		return
	}

}
