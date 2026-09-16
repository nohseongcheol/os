/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "konzola"

const Bajtovapersector int = 512

type TNaprednoTehnologijaattachment struct {
	glavni		bool
	dataPort	TPort16bit
	greškaPort	TPort8bit
	sectorcountPort	TPort8bit
	lbaTihoPort	TPort8bit
	lbamidPort	TPort8bit
	lbahiPort	TPort8bit
	uređajPort	TPort8bit
	naredbaPort	TPort8bit
	kontrolPort	TPort8bit
}

func (isti *TNaprednoTehnologijaattachment) Init(glavni bool, portbase uint16) {
	isti.glavni = glavni
	isti.dataPort.Init(portbase)
	isti.greškaPort.Init(portbase + 0x1)
	isti.sectorcountPort.Init(portbase + 0x2)
	isti.lbaTihoPort.Init(portbase + 0x3)
	isti.lbamidPort.Init(portbase + 0x4)
	isti.lbahiPort.Init(portbase + 0x5)
	isti.uređajPort.Init(portbase + 0x6)
	isti.naredbaPort.Init(portbase + 0x7)
	isti.kontrolPort.Init(portbase + 0x8)

}

func (isti *TNaprednoTehnologijaattachment) Identify() {

	var konzola_2 = TKonzola{}

	if isti.glavni {
		isti.uređajPort.Piše(0xA0)
	} else {
		isti.uređajPort.Piše(0xB0)
	}
	isti.kontrolPort.Piše(0)
	isti.uređajPort.Piše(0xA0)

	var stanje uint8 = isti.naredbaPort.Čitanje()
	if stanje == 0xFF {
		konzola_2.MŠtampaj(([]byte)("Invalid Status"))
		return
	}

	if isti.glavni {
		isti.uređajPort.Piše(0xA0)
	} else {
		isti.uređajPort.Piše(0xB0)
	}
	isti.sectorcountPort.Piše(0)
	isti.lbaTihoPort.Piše(0)
	isti.lbamidPort.Piše(0)
	isti.lbahiPort.Piše(0)
	isti.naredbaPort.Piše(0xEC)

	stanje = isti.naredbaPort.Čitanje()
	if stanje == 0x00 {
		konzola_2.MŠtampaj(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (stanje&0x80) == 0x80 && (stanje&0x01) != 0x01 {
		stanje = isti.naredbaPort.Čitanje()
	}

	if (stanje & 0x01) != 0 {
		konzola_2.MŠtampaj(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = isti.dataPort.Čitanje()
		tekst := []byte("  ")
		tekst[0] = uint8((data >> 8) & 0xFF)
		tekst[1] = uint8(data & 0xFF)

	}
	konzola_2.MŠtampajxy(([]byte)("ata ok"), 10, 22)

}
func (isti *TNaprednoTehnologijaattachment) Čitanje28(sector uint32, data *[]byte, count int) {
	var konzola_2 = TKonzola{}
	if (sector & 0xF0000000) != 0 {
		konzola_2.MŠtampaj(([]byte)("ata read error "))
		return
	}
	if count > Bajtovapersector {
		konzola_2.MŠtampaj(([]byte)("ata read error "))
		return
	}

	if isti.glavni {
		isti.uređajPort.Piše(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		isti.uređajPort.Piše(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	isti.greškaPort.Piše(0)
	isti.sectorcountPort.Piše(1)

	isti.lbaTihoPort.Piše(uint8(sector & 0x000000FF))
	isti.lbamidPort.Piše(uint8((sector & 0x0000FF00) >> 8))
	isti.lbahiPort.Piše(uint8((sector & 0x00FF0000) >> 16))
	isti.naredbaPort.Piše(0x20)

	var stanje uint8 = isti.naredbaPort.Čitanje()
	for ((stanje & 0x80) == 0x80) && ((stanje & 0x01) != 0x01) {
		stanje = isti.naredbaPort.Čitanje()
	}

	if (stanje & 0x01) != 0 {
		konzola_2.MŠtampaj(([]byte)("ata read error "))
		return
	}

	konzola_2.MŠtampajxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = isti.dataPort.Čitanje()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bajtovapersector; i += 2 {
		isti.dataPort.Čitanje()
	}
}
func (isti *TNaprednoTehnologijaattachment) Piše28(sectorbroj uint32, data []byte, count uint32) {

	if sectorbroj > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if isti.glavni {
		isti.uređajPort.Piše(uint8(0xE0 | uint8((sectorbroj&0x0F000000)>>24)))
	} else {
		isti.uređajPort.Piše(uint8(0xF0 | uint8((sectorbroj&0x0F000000)>>24)))
	}

	isti.greškaPort.Piše(0)
	isti.sectorcountPort.Piše(1)
	isti.lbaTihoPort.Piše(uint8(sectorbroj & 0x000000FF))
	isti.lbamidPort.Piše(uint8((sectorbroj & 0x0000FF00) >> 8))
	isti.lbahiPort.Piše(uint8((sectorbroj & 0x00FF0000) >> 16))
	isti.naredbaPort.Piše(0x30)

	var konzola_2 = TKonzola{}
	konzola_2.MŠtampaj(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		isti.dataPort.Piše(wdata)

		tekst := []byte("  ")
		tekst[0] = uint8((wdata >> 8) & 0xFF)
		tekst[1] = uint8(wdata & 0xFF)

		konzola_2.MŠtampaj(tekst)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		isti.dataPort.Piše(0x0000)
	}

}

func (isti *TNaprednoTehnologijaattachment) Flush() {
	if isti.glavni {
		isti.uređajPort.Piše(0xE0)
	} else {
		isti.uređajPort.Piše(0xF0)
	}
	isti.naredbaPort.Piše(0xE7)

	var konzola_2 = TKonzola{}

	var stanje uint8 = isti.naredbaPort.Čitanje()
	if stanje == 0x00 {
		return
	}

	for ((stanje & 0x80) == 0x80) && ((stanje & 0x01) != 0x01) {
		stanje = isti.naredbaPort.Čitanje()
	}
	if (stanje & 0x01) != 0 {
		konzola_2.MŠtampaj(([]byte)(" ata flush error"))
		return
	}

}
