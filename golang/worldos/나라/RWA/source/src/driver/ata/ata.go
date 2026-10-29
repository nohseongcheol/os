/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "umuyoboro"
import . "console"

const Bayitepersector int = 512

type TUrwegorwohejurutechnologyattachment struct {
	master			bool
	dataUmuyoboro		TUmuyoboro16bit
	ikosaUmuyoboro		TUmuyoboro8bit
	sectorcountUmuyoboro	TUmuyoboro8bit
	lbalowUmuyoboro		TUmuyoboro8bit
	lbamidUmuyoboro		TUmuyoboro8bit
	lbahiUmuyoboro		TUmuyoboro8bit
	ububikoUmuyoboro	TUmuyoboro8bit
	icyowifuzaUmuyoboro	TUmuyoboro8bit
	controlUmuyoboro	TUmuyoboro8bit
}

func (self *TUrwegorwohejurutechnologyattachment) Init(master bool, umuyoborobase uint16) {
	self.master = master
	self.dataUmuyoboro.Init(umuyoborobase)
	self.ikosaUmuyoboro.Init(umuyoborobase + 0x1)
	self.sectorcountUmuyoboro.Init(umuyoborobase + 0x2)
	self.lbalowUmuyoboro.Init(umuyoborobase + 0x3)
	self.lbamidUmuyoboro.Init(umuyoborobase + 0x4)
	self.lbahiUmuyoboro.Init(umuyoborobase + 0x5)
	self.ububikoUmuyoboro.Init(umuyoborobase + 0x6)
	self.icyowifuzaUmuyoboro.Init(umuyoborobase + 0x7)
	self.controlUmuyoboro.Init(umuyoborobase + 0x8)

}

func (self *TUrwegorwohejurutechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.ububikoUmuyoboro.Kwandika(0xA0)
	} else {
		self.ububikoUmuyoboro.Kwandika(0xB0)
	}
	self.controlUmuyoboro.Kwandika(0)
	self.ububikoUmuyoboro.Kwandika(0xA0)

	var imimerere uint8 = self.icyowifuzaUmuyoboro.Gusoma()
	if imimerere == 0xFF {
		console_2.MGucapa(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.ububikoUmuyoboro.Kwandika(0xA0)
	} else {
		self.ububikoUmuyoboro.Kwandika(0xB0)
	}
	self.sectorcountUmuyoboro.Kwandika(0)
	self.lbalowUmuyoboro.Kwandika(0)
	self.lbamidUmuyoboro.Kwandika(0)
	self.lbahiUmuyoboro.Kwandika(0)
	self.icyowifuzaUmuyoboro.Kwandika(0xEC)

	imimerere = self.icyowifuzaUmuyoboro.Gusoma()
	if imimerere == 0x00 {
		console_2.MGucapa(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (imimerere&0x80) == 0x80 && (imimerere&0x01) != 0x01 {
		imimerere = self.icyowifuzaUmuyoboro.Gusoma()
	}

	if (imimerere & 0x01) != 0 {
		console_2.MGucapa(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataUmuyoboro.Gusoma()
		umwandiko := []byte("  ")
		umwandiko[0] = uint8((data >> 8) & 0xFF)
		umwandiko[1] = uint8(data & 0xFF)

	}
	console_2.MGucapaxy(([]byte)("ata ok"), 10, 22)

}
func (self *TUrwegorwohejurutechnologyattachment) Gusoma28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MGucapa(([]byte)("ata read error "))
		return
	}
	if count > Bayitepersector {
		console_2.MGucapa(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.ububikoUmuyoboro.Kwandika(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.ububikoUmuyoboro.Kwandika(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.ikosaUmuyoboro.Kwandika(0)
	self.sectorcountUmuyoboro.Kwandika(1)

	self.lbalowUmuyoboro.Kwandika(uint8(sector & 0x000000FF))
	self.lbamidUmuyoboro.Kwandika(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiUmuyoboro.Kwandika(uint8((sector & 0x00FF0000) >> 16))
	self.icyowifuzaUmuyoboro.Kwandika(0x20)

	var imimerere uint8 = self.icyowifuzaUmuyoboro.Gusoma()
	for ((imimerere & 0x80) == 0x80) && ((imimerere & 0x01) != 0x01) {
		imimerere = self.icyowifuzaUmuyoboro.Gusoma()
	}

	if (imimerere & 0x01) != 0 {
		console_2.MGucapa(([]byte)("ata read error "))
		return
	}

	console_2.MGucapaxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataUmuyoboro.Gusoma()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bayitepersector; i += 2 {
		self.dataUmuyoboro.Gusoma()
	}
}
func (self *TUrwegorwohejurutechnologyattachment) Kwandika28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.ububikoUmuyoboro.Kwandika(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.ububikoUmuyoboro.Kwandika(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.ikosaUmuyoboro.Kwandika(0)
	self.sectorcountUmuyoboro.Kwandika(1)
	self.lbalowUmuyoboro.Kwandika(uint8(sectornumber & 0x000000FF))
	self.lbamidUmuyoboro.Kwandika(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiUmuyoboro.Kwandika(uint8((sectornumber & 0x00FF0000) >> 16))
	self.icyowifuzaUmuyoboro.Kwandika(0x30)

	var console_2 = TConsole{}
	console_2.MGucapa(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataUmuyoboro.Kwandika(wdata)

		umwandiko := []byte("  ")
		umwandiko[0] = uint8((wdata >> 8) & 0xFF)
		umwandiko[1] = uint8(wdata & 0xFF)

		console_2.MGucapa(umwandiko)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataUmuyoboro.Kwandika(0x0000)
	}

}

func (self *TUrwegorwohejurutechnologyattachment) Flush() {
	if self.master {
		self.ububikoUmuyoboro.Kwandika(0xE0)
	} else {
		self.ububikoUmuyoboro.Kwandika(0xF0)
	}
	self.icyowifuzaUmuyoboro.Kwandika(0xE7)

	var console_2 = TConsole{}

	var imimerere uint8 = self.icyowifuzaUmuyoboro.Gusoma()
	if imimerere == 0x00 {
		return
	}

	for ((imimerere & 0x80) == 0x80) && ((imimerere & 0x01) != 0x01) {
		imimerere = self.icyowifuzaUmuyoboro.Gusoma()
	}
	if (imimerere & 0x01) != 0 {
		console_2.MGucapa(([]byte)(" ata flush error"))
		return
	}

}
