package ata

import . "port"
import . "console"

const Octețipersector int = 512

type TAvansateTehnologieattachment struct {
	principal	bool
	dataport	TPort16bit
	eroareport	TPort8bit
	sectorcountport	TPort8bit
	lbaScăzutăport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	dispozitivport	TPort8bit
	comandăport	TPort8bit
	controlport	TPort8bit
}

func (sine *TAvansateTehnologieattachment) Init(principal bool, portbase uint16) {
	sine.principal = principal
	sine.dataport.Init(portbase)
	sine.eroareport.Init(portbase + 0x1)
	sine.sectorcountport.Init(portbase + 0x2)
	sine.lbaScăzutăport.Init(portbase + 0x3)
	sine.lbamidport.Init(portbase + 0x4)
	sine.lbahiport.Init(portbase + 0x5)
	sine.dispozitivport.Init(portbase + 0x6)
	sine.comandăport.Init(portbase + 0x7)
	sine.controlport.Init(portbase + 0x8)

}

func (sine *TAvansateTehnologieattachment) Identify() {

	var console_2 = TConsole{}

	if sine.principal {
		sine.dispozitivport.Scriere(0xA0)
	} else {
		sine.dispozitivport.Scriere(0xB0)
	}
	sine.controlport.Scriere(0)
	sine.dispozitivport.Scriere(0xA0)

	var stare uint8 = sine.comandăport.Citire()
	if stare == 0xFF {
		console_2.MTipărește(([]byte)("Invalid Status"))
		return
	}

	if sine.principal {
		sine.dispozitivport.Scriere(0xA0)
	} else {
		sine.dispozitivport.Scriere(0xB0)
	}
	sine.sectorcountport.Scriere(0)
	sine.lbaScăzutăport.Scriere(0)
	sine.lbamidport.Scriere(0)
	sine.lbahiport.Scriere(0)
	sine.comandăport.Scriere(0xEC)

	stare = sine.comandăport.Citire()
	if stare == 0x00 {
		console_2.MTipărește(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (stare&0x80) == 0x80 && (stare&0x01) != 0x01 {
		stare = sine.comandăport.Citire()
	}

	if (stare & 0x01) != 0 {
		console_2.MTipărește(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = sine.dataport.Citire()
		text := []byte("  ")
		text[0] = uint8((data >> 8) & 0xFF)
		text[1] = uint8(data & 0xFF)

	}
	console_2.MTipăreștexy(([]byte)("ata ok"), 10, 22)

}
func (sine *TAvansateTehnologieattachment) Citire28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MTipărește(([]byte)("ata read error "))
		return
	}
	if count > Octețipersector {
		console_2.MTipărește(([]byte)("ata read error "))
		return
	}

	if sine.principal {
		sine.dispozitivport.Scriere(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		sine.dispozitivport.Scriere(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	sine.eroareport.Scriere(0)
	sine.sectorcountport.Scriere(1)

	sine.lbaScăzutăport.Scriere(uint8(sector & 0x000000FF))
	sine.lbamidport.Scriere(uint8((sector & 0x0000FF00) >> 8))
	sine.lbahiport.Scriere(uint8((sector & 0x00FF0000) >> 16))
	sine.comandăport.Scriere(0x20)

	var stare uint8 = sine.comandăport.Citire()
	for ((stare & 0x80) == 0x80) && ((stare & 0x01) != 0x01) {
		stare = sine.comandăport.Citire()
	}

	if (stare & 0x01) != 0 {
		console_2.MTipărește(([]byte)("ata read error "))
		return
	}

	console_2.MTipăreștexy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = sine.dataport.Citire()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Octețipersector; i += 2 {
		sine.dataport.Citire()
	}
}
func (sine *TAvansateTehnologieattachment) Scriere28(sectorNumăr uint32, data []byte, count uint32) {

	if sectorNumăr > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if sine.principal {
		sine.dispozitivport.Scriere(uint8(0xE0 | uint8((sectorNumăr&0x0F000000)>>24)))
	} else {
		sine.dispozitivport.Scriere(uint8(0xF0 | uint8((sectorNumăr&0x0F000000)>>24)))
	}

	sine.eroareport.Scriere(0)
	sine.sectorcountport.Scriere(1)
	sine.lbaScăzutăport.Scriere(uint8(sectorNumăr & 0x000000FF))
	sine.lbamidport.Scriere(uint8((sectorNumăr & 0x0000FF00) >> 8))
	sine.lbahiport.Scriere(uint8((sectorNumăr & 0x00FF0000) >> 16))
	sine.comandăport.Scriere(0x30)

	var console_2 = TConsole{}
	console_2.MTipărește(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		sine.dataport.Scriere(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		console_2.MTipărește(text)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		sine.dataport.Scriere(0x0000)
	}

}

func (sine *TAvansateTehnologieattachment) Flush() {
	if sine.principal {
		sine.dispozitivport.Scriere(0xE0)
	} else {
		sine.dispozitivport.Scriere(0xF0)
	}
	sine.comandăport.Scriere(0xE7)

	var console_2 = TConsole{}

	var stare uint8 = sine.comandăport.Citire()
	if stare == 0x00 {
		return
	}

	for ((stare & 0x80) == 0x80) && ((stare & 0x01) != 0x01) {
		stare = sine.comandăport.Citire()
	}
	if (stare & 0x01) != 0 {
		console_2.MTipărește(([]byte)(" ata flush error"))
		return
	}

}
