package ata

import . "port"
import . "console"

const Baitipersector int = 512

type TLaiendatudTehnoloogiaattachment struct {
	valjus		bool
	dataport	TPort16biti
	vigaport	TPort8biti
	sectorcountport	TPort8biti
	lbaMadalport	TPort8biti
	lbamidport	TPort8biti
	lbahiport	TPort8biti
	seadeport	TPort8biti
	käskport	TPort8biti
	juhtport	TPort8biti
}

func (ise *TLaiendatudTehnoloogiaattachment) Init(valjus bool, portbase uint16) {
	ise.valjus = valjus
	ise.dataport.Init(portbase)
	ise.vigaport.Init(portbase + 0x1)
	ise.sectorcountport.Init(portbase + 0x2)
	ise.lbaMadalport.Init(portbase + 0x3)
	ise.lbamidport.Init(portbase + 0x4)
	ise.lbahiport.Init(portbase + 0x5)
	ise.seadeport.Init(portbase + 0x6)
	ise.käskport.Init(portbase + 0x7)
	ise.juhtport.Init(portbase + 0x8)

}

func (ise *TLaiendatudTehnoloogiaattachment) Identify() {

	var console_2 = TConsole{}

	if ise.valjus {
		ise.seadeport.Kirjutamine(0xA0)
	} else {
		ise.seadeport.Kirjutamine(0xB0)
	}
	ise.juhtport.Kirjutamine(0)
	ise.seadeport.Kirjutamine(0xA0)

	var olek uint8 = ise.käskport.Lugemine()
	if olek == 0xFF {
		console_2.MPrindi(([]byte)("Invalid Status"))
		return
	}

	if ise.valjus {
		ise.seadeport.Kirjutamine(0xA0)
	} else {
		ise.seadeport.Kirjutamine(0xB0)
	}
	ise.sectorcountport.Kirjutamine(0)
	ise.lbaMadalport.Kirjutamine(0)
	ise.lbamidport.Kirjutamine(0)
	ise.lbahiport.Kirjutamine(0)
	ise.käskport.Kirjutamine(0xEC)

	olek = ise.käskport.Lugemine()
	if olek == 0x00 {
		console_2.MPrindi(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (olek&0x80) == 0x80 && (olek&0x01) != 0x01 {
		olek = ise.käskport.Lugemine()
	}

	if (olek & 0x01) != 0 {
		console_2.MPrindi(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = ise.dataport.Lugemine()
		tekst := []byte("  ")
		tekst[0] = uint8((data >> 8) & 0xFF)
		tekst[1] = uint8(data & 0xFF)

	}
	console_2.MPrindixy(([]byte)("ata ok"), 10, 22)

}
func (ise *TLaiendatudTehnoloogiaattachment) Lugemine28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MPrindi(([]byte)("ata read error "))
		return
	}
	if count > Baitipersector {
		console_2.MPrindi(([]byte)("ata read error "))
		return
	}

	if ise.valjus {
		ise.seadeport.Kirjutamine(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		ise.seadeport.Kirjutamine(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	ise.vigaport.Kirjutamine(0)
	ise.sectorcountport.Kirjutamine(1)

	ise.lbaMadalport.Kirjutamine(uint8(sector & 0x000000FF))
	ise.lbamidport.Kirjutamine(uint8((sector & 0x0000FF00) >> 8))
	ise.lbahiport.Kirjutamine(uint8((sector & 0x00FF0000) >> 16))
	ise.käskport.Kirjutamine(0x20)

	var olek uint8 = ise.käskport.Lugemine()
	for ((olek & 0x80) == 0x80) && ((olek & 0x01) != 0x01) {
		olek = ise.käskport.Lugemine()
	}

	if (olek & 0x01) != 0 {
		console_2.MPrindi(([]byte)("ata read error "))
		return
	}

	console_2.MPrindixy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = ise.dataport.Lugemine()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Baitipersector; i += 2 {
		ise.dataport.Lugemine()
	}
}
func (ise *TLaiendatudTehnoloogiaattachment) Kirjutamine28(sectorArv uint32, data []byte, count uint32) {

	if sectorArv > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if ise.valjus {
		ise.seadeport.Kirjutamine(uint8(0xE0 | uint8((sectorArv&0x0F000000)>>24)))
	} else {
		ise.seadeport.Kirjutamine(uint8(0xF0 | uint8((sectorArv&0x0F000000)>>24)))
	}

	ise.vigaport.Kirjutamine(0)
	ise.sectorcountport.Kirjutamine(1)
	ise.lbaMadalport.Kirjutamine(uint8(sectorArv & 0x000000FF))
	ise.lbamidport.Kirjutamine(uint8((sectorArv & 0x0000FF00) >> 8))
	ise.lbahiport.Kirjutamine(uint8((sectorArv & 0x00FF0000) >> 16))
	ise.käskport.Kirjutamine(0x30)

	var console_2 = TConsole{}
	console_2.MPrindi(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		ise.dataport.Kirjutamine(wdata)

		tekst := []byte("  ")
		tekst[0] = uint8((wdata >> 8) & 0xFF)
		tekst[1] = uint8(wdata & 0xFF)

		console_2.MPrindi(tekst)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		ise.dataport.Kirjutamine(0x0000)
	}

}

func (ise *TLaiendatudTehnoloogiaattachment) Flush() {
	if ise.valjus {
		ise.seadeport.Kirjutamine(0xE0)
	} else {
		ise.seadeport.Kirjutamine(0xF0)
	}
	ise.käskport.Kirjutamine(0xE7)

	var console_2 = TConsole{}

	var olek uint8 = ise.käskport.Lugemine()
	if olek == 0x00 {
		return
	}

	for ((olek & 0x80) == 0x80) && ((olek & 0x01) != 0x01) {
		olek = ise.käskport.Lugemine()
	}
	if (olek & 0x01) != 0 {
		console_2.MPrindi(([]byte)(" ata flush error"))
		return
	}

}
