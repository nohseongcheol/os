/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "poort"
import . "console"

const Bytespersector int = 512

type TGeavanceerdTechnologieattachment struct {
	master			bool
	dataPoort		TPoort16bit
	foutPoort		TPoort8bit
	sectorAantalPoort	TPoort8bit
	lbaLaagPoort		TPoort8bit
	lbamidPoort		TPoort8bit
	lbahiPoort		TPoort8bit
	apparaatPoort		TPoort8bit
	opdrachtPoort		TPoort8bit
	bedieningPoort		TPoort8bit
}

func (zelf *TGeavanceerdTechnologieattachment) Init(master bool, poortbase uint16) {
	zelf.master = master
	zelf.dataPoort.Init(poortbase)
	zelf.foutPoort.Init(poortbase + 0x1)
	zelf.sectorAantalPoort.Init(poortbase + 0x2)
	zelf.lbaLaagPoort.Init(poortbase + 0x3)
	zelf.lbamidPoort.Init(poortbase + 0x4)
	zelf.lbahiPoort.Init(poortbase + 0x5)
	zelf.apparaatPoort.Init(poortbase + 0x6)
	zelf.opdrachtPoort.Init(poortbase + 0x7)
	zelf.bedieningPoort.Init(poortbase + 0x8)

}

func (zelf *TGeavanceerdTechnologieattachment) Identify() {

	var console_2 = TConsole{}

	if zelf.master {
		zelf.apparaatPoort.Schrijven(0xA0)
	} else {
		zelf.apparaatPoort.Schrijven(0xB0)
	}
	zelf.bedieningPoort.Schrijven(0)
	zelf.apparaatPoort.Schrijven(0xA0)

	var status uint8 = zelf.opdrachtPoort.Lezen()
	if status == 0xFF {
		console_2.MAfdrukken(([]byte)("Invalid Status"))
		return
	}

	if zelf.master {
		zelf.apparaatPoort.Schrijven(0xA0)
	} else {
		zelf.apparaatPoort.Schrijven(0xB0)
	}
	zelf.sectorAantalPoort.Schrijven(0)
	zelf.lbaLaagPoort.Schrijven(0)
	zelf.lbamidPoort.Schrijven(0)
	zelf.lbahiPoort.Schrijven(0)
	zelf.opdrachtPoort.Schrijven(0xEC)

	status = zelf.opdrachtPoort.Lezen()
	if status == 0x00 {
		console_2.MAfdrukken(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = zelf.opdrachtPoort.Lezen()
	}

	if (status & 0x01) != 0 {
		console_2.MAfdrukken(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = zelf.dataPoort.Lezen()
		tekst := []byte("  ")
		tekst[0] = uint8((data >> 8) & 0xFF)
		tekst[1] = uint8(data & 0xFF)

	}
	console_2.MAfdrukkenxy(([]byte)("ata ok"), 10, 22)

}
func (zelf *TGeavanceerdTechnologieattachment) Lezen28(sector uint32, data *[]byte, aantal int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MAfdrukken(([]byte)("ata read error "))
		return
	}
	if aantal > Bytespersector {
		console_2.MAfdrukken(([]byte)("ata read error "))
		return
	}

	if zelf.master {
		zelf.apparaatPoort.Schrijven(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		zelf.apparaatPoort.Schrijven(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	zelf.foutPoort.Schrijven(0)
	zelf.sectorAantalPoort.Schrijven(1)

	zelf.lbaLaagPoort.Schrijven(uint8(sector & 0x000000FF))
	zelf.lbamidPoort.Schrijven(uint8((sector & 0x0000FF00) >> 8))
	zelf.lbahiPoort.Schrijven(uint8((sector & 0x00FF0000) >> 16))
	zelf.opdrachtPoort.Schrijven(0x20)

	var status uint8 = zelf.opdrachtPoort.Lezen()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = zelf.opdrachtPoort.Lezen()
	}

	if (status & 0x01) != 0 {
		console_2.MAfdrukken(([]byte)("ata read error "))
		return
	}

	console_2.MAfdrukkenxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < aantal; i += 2 {
		var wdata uint16 = zelf.dataPoort.Lezen()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < aantal {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (aantal + (aantal % 2)); i < Bytespersector; i += 2 {
		zelf.dataPoort.Lezen()
	}
}
func (zelf *TGeavanceerdTechnologieattachment) Schrijven28(sectorGetal uint32, data []byte, aantal uint32) {

	if sectorGetal > 0x0FFFFFFF {
		return
	}

	if aantal > 512 {
		return
	}

	if zelf.master {
		zelf.apparaatPoort.Schrijven(uint8(0xE0 | uint8((sectorGetal&0x0F000000)>>24)))
	} else {
		zelf.apparaatPoort.Schrijven(uint8(0xF0 | uint8((sectorGetal&0x0F000000)>>24)))
	}

	zelf.foutPoort.Schrijven(0)
	zelf.sectorAantalPoort.Schrijven(1)
	zelf.lbaLaagPoort.Schrijven(uint8(sectorGetal & 0x000000FF))
	zelf.lbamidPoort.Schrijven(uint8((sectorGetal & 0x0000FF00) >> 8))
	zelf.lbahiPoort.Schrijven(uint8((sectorGetal & 0x00FF0000) >> 16))
	zelf.opdrachtPoort.Schrijven(0x30)

	var console_2 = TConsole{}
	console_2.MAfdrukken(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < aantal; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < aantal {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		zelf.dataPoort.Schrijven(wdata)

		tekst := []byte("  ")
		tekst[0] = uint8((wdata >> 8) & 0xFF)
		tekst[1] = uint8(wdata & 0xFF)

		console_2.MAfdrukken(tekst)
	}

	for i := (aantal + (aantal % 2)); i < 512; i += 2 {
		zelf.dataPoort.Schrijven(0x0000)
	}

}

func (zelf *TGeavanceerdTechnologieattachment) Flush() {
	if zelf.master {
		zelf.apparaatPoort.Schrijven(0xE0)
	} else {
		zelf.apparaatPoort.Schrijven(0xF0)
	}
	zelf.opdrachtPoort.Schrijven(0xE7)

	var console_2 = TConsole{}

	var status uint8 = zelf.opdrachtPoort.Lezen()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = zelf.opdrachtPoort.Lezen()
	}
	if (status & 0x01) != 0 {
		console_2.MAfdrukken(([]byte)(" ata flush error"))
		return
	}

}
