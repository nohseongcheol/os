/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "console"

const Baytlarpersector int = 512

type TMurakkabTexnologiyaattachment struct {
	master		bool
	dataport	TPort16bit
	xatoport	TPort8bit
	sectorcountport	TPort8bit
	lbaPastport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	uskunaport	TPort8bit
	buyruqport	TPort8bit
	controlport	TPort8bit
}

func (self *TMurakkabTexnologiyaattachment) Init(master bool, portbase uint16) {
	self.master = master
	self.dataport.Init(portbase)
	self.xatoport.Init(portbase + 0x1)
	self.sectorcountport.Init(portbase + 0x2)
	self.lbaPastport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.uskunaport.Init(portbase + 0x6)
	self.buyruqport.Init(portbase + 0x7)
	self.controlport.Init(portbase + 0x8)

}

func (self *TMurakkabTexnologiyaattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.uskunaport.Yozish(0xA0)
	} else {
		self.uskunaport.Yozish(0xB0)
	}
	self.controlport.Yozish(0)
	self.uskunaport.Yozish(0xA0)

	var holat uint8 = self.buyruqport.Oʻqish()
	if holat == 0xFF {
		console_2.MChopetish(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.uskunaport.Yozish(0xA0)
	} else {
		self.uskunaport.Yozish(0xB0)
	}
	self.sectorcountport.Yozish(0)
	self.lbaPastport.Yozish(0)
	self.lbamidport.Yozish(0)
	self.lbahiport.Yozish(0)
	self.buyruqport.Yozish(0xEC)

	holat = self.buyruqport.Oʻqish()
	if holat == 0x00 {
		console_2.MChopetish(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (holat&0x80) == 0x80 && (holat&0x01) != 0x01 {
		holat = self.buyruqport.Oʻqish()
	}

	if (holat & 0x01) != 0 {
		console_2.MChopetish(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataport.Oʻqish()
		matn := []byte("  ")
		matn[0] = uint8((data >> 8) & 0xFF)
		matn[1] = uint8(data & 0xFF)

	}
	console_2.MChopetishxy(([]byte)("ata ok"), 10, 22)

}
func (self *TMurakkabTexnologiyaattachment) Oʻqish28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MChopetish(([]byte)("ata read error "))
		return
	}
	if count > Baytlarpersector {
		console_2.MChopetish(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.uskunaport.Yozish(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.uskunaport.Yozish(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.xatoport.Yozish(0)
	self.sectorcountport.Yozish(1)

	self.lbaPastport.Yozish(uint8(sector & 0x000000FF))
	self.lbamidport.Yozish(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Yozish(uint8((sector & 0x00FF0000) >> 16))
	self.buyruqport.Yozish(0x20)

	var holat uint8 = self.buyruqport.Oʻqish()
	for ((holat & 0x80) == 0x80) && ((holat & 0x01) != 0x01) {
		holat = self.buyruqport.Oʻqish()
	}

	if (holat & 0x01) != 0 {
		console_2.MChopetish(([]byte)("ata read error "))
		return
	}

	console_2.MChopetishxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataport.Oʻqish()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Baytlarpersector; i += 2 {
		self.dataport.Oʻqish()
	}
}
func (self *TMurakkabTexnologiyaattachment) Yozish28(sectorRAQAM uint32, data []byte, count uint32) {

	if sectorRAQAM > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.uskunaport.Yozish(uint8(0xE0 | uint8((sectorRAQAM&0x0F000000)>>24)))
	} else {
		self.uskunaport.Yozish(uint8(0xF0 | uint8((sectorRAQAM&0x0F000000)>>24)))
	}

	self.xatoport.Yozish(0)
	self.sectorcountport.Yozish(1)
	self.lbaPastport.Yozish(uint8(sectorRAQAM & 0x000000FF))
	self.lbamidport.Yozish(uint8((sectorRAQAM & 0x0000FF00) >> 8))
	self.lbahiport.Yozish(uint8((sectorRAQAM & 0x00FF0000) >> 16))
	self.buyruqport.Yozish(0x30)

	var console_2 = TConsole{}
	console_2.MChopetish(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataport.Yozish(wdata)

		matn := []byte("  ")
		matn[0] = uint8((wdata >> 8) & 0xFF)
		matn[1] = uint8(wdata & 0xFF)

		console_2.MChopetish(matn)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataport.Yozish(0x0000)
	}

}

func (self *TMurakkabTexnologiyaattachment) Flush() {
	if self.master {
		self.uskunaport.Yozish(0xE0)
	} else {
		self.uskunaport.Yozish(0xF0)
	}
	self.buyruqport.Yozish(0xE7)

	var console_2 = TConsole{}

	var holat uint8 = self.buyruqport.Oʻqish()
	if holat == 0x00 {
		return
	}

	for ((holat & 0x80) == 0x80) && ((holat & 0x01) != 0x01) {
		holat = self.buyruqport.Oʻqish()
	}
	if (holat & 0x01) != 0 {
		console_2.MChopetish(([]byte)(" ata flush error"))
		return
	}

}
