/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "console"

const Bajtovapersector int = 512

type TNaprednoTehnologijaattachment struct {
	master		bool
	dataport	TPort16bit
	greškaport	TPort8bit
	sectorcountport	TPort8bit
	lbaNIskoport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	uređajport	TPort8bit
	naredbaport	TPort8bit
	ctrlport	TPort8bit
}

func (sam *TNaprednoTehnologijaattachment) Init(master bool, portbase uint16) {
	sam.master = master
	sam.dataport.Init(portbase)
	sam.greškaport.Init(portbase + 0x1)
	sam.sectorcountport.Init(portbase + 0x2)
	sam.lbaNIskoport.Init(portbase + 0x3)
	sam.lbamidport.Init(portbase + 0x4)
	sam.lbahiport.Init(portbase + 0x5)
	sam.uređajport.Init(portbase + 0x6)
	sam.naredbaport.Init(portbase + 0x7)
	sam.ctrlport.Init(portbase + 0x8)

}

func (sam *TNaprednoTehnologijaattachment) Identify() {

	var console_2 = TConsole{}

	if sam.master {
		sam.uređajport.Zapiši(0xA0)
	} else {
		sam.uređajport.Zapiši(0xB0)
	}
	sam.ctrlport.Zapiši(0)
	sam.uređajport.Zapiši(0xA0)

	var stanje uint8 = sam.naredbaport.Čitaj()
	if stanje == 0xFF {
		console_2.MIspis(([]byte)("Invalid Status"))
		return
	}

	if sam.master {
		sam.uređajport.Zapiši(0xA0)
	} else {
		sam.uređajport.Zapiši(0xB0)
	}
	sam.sectorcountport.Zapiši(0)
	sam.lbaNIskoport.Zapiši(0)
	sam.lbamidport.Zapiši(0)
	sam.lbahiport.Zapiši(0)
	sam.naredbaport.Zapiši(0xEC)

	stanje = sam.naredbaport.Čitaj()
	if stanje == 0x00 {
		console_2.MIspis(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (stanje&0x80) == 0x80 && (stanje&0x01) != 0x01 {
		stanje = sam.naredbaport.Čitaj()
	}

	if (stanje & 0x01) != 0 {
		console_2.MIspis(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = sam.dataport.Čitaj()
		tekst := []byte("  ")
		tekst[0] = uint8((data >> 8) & 0xFF)
		tekst[1] = uint8(data & 0xFF)

	}
	console_2.MIspisxy(([]byte)("ata ok"), 10, 22)

}
func (sam *TNaprednoTehnologijaattachment) Čitaj28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MIspis(([]byte)("ata read error "))
		return
	}
	if count > Bajtovapersector {
		console_2.MIspis(([]byte)("ata read error "))
		return
	}

	if sam.master {
		sam.uređajport.Zapiši(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		sam.uređajport.Zapiši(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	sam.greškaport.Zapiši(0)
	sam.sectorcountport.Zapiši(1)

	sam.lbaNIskoport.Zapiši(uint8(sector & 0x000000FF))
	sam.lbamidport.Zapiši(uint8((sector & 0x0000FF00) >> 8))
	sam.lbahiport.Zapiši(uint8((sector & 0x00FF0000) >> 16))
	sam.naredbaport.Zapiši(0x20)

	var stanje uint8 = sam.naredbaport.Čitaj()
	for ((stanje & 0x80) == 0x80) && ((stanje & 0x01) != 0x01) {
		stanje = sam.naredbaport.Čitaj()
	}

	if (stanje & 0x01) != 0 {
		console_2.MIspis(([]byte)("ata read error "))
		return
	}

	console_2.MIspisxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = sam.dataport.Čitaj()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bajtovapersector; i += 2 {
		sam.dataport.Čitaj()
	}
}
func (sam *TNaprednoTehnologijaattachment) Zapiši28(sectorBROJ uint32, data []byte, count uint32) {

	if sectorBROJ > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if sam.master {
		sam.uređajport.Zapiši(uint8(0xE0 | uint8((sectorBROJ&0x0F000000)>>24)))
	} else {
		sam.uređajport.Zapiši(uint8(0xF0 | uint8((sectorBROJ&0x0F000000)>>24)))
	}

	sam.greškaport.Zapiši(0)
	sam.sectorcountport.Zapiši(1)
	sam.lbaNIskoport.Zapiši(uint8(sectorBROJ & 0x000000FF))
	sam.lbamidport.Zapiši(uint8((sectorBROJ & 0x0000FF00) >> 8))
	sam.lbahiport.Zapiši(uint8((sectorBROJ & 0x00FF0000) >> 16))
	sam.naredbaport.Zapiši(0x30)

	var console_2 = TConsole{}
	console_2.MIspis(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		sam.dataport.Zapiši(wdata)

		tekst := []byte("  ")
		tekst[0] = uint8((wdata >> 8) & 0xFF)
		tekst[1] = uint8(wdata & 0xFF)

		console_2.MIspis(tekst)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		sam.dataport.Zapiši(0x0000)
	}

}

func (sam *TNaprednoTehnologijaattachment) Flush() {
	if sam.master {
		sam.uređajport.Zapiši(0xE0)
	} else {
		sam.uređajport.Zapiši(0xF0)
	}
	sam.naredbaport.Zapiši(0xE7)

	var console_2 = TConsole{}

	var stanje uint8 = sam.naredbaport.Čitaj()
	if stanje == 0x00 {
		return
	}

	for ((stanje & 0x80) == 0x80) && ((stanje & 0x01) != 0x01) {
		stanje = sam.naredbaport.Čitaj()
	}
	if (stanje & 0x01) != 0 {
		console_2.MIspis(([]byte)(" ata flush error"))
		return
	}

}
