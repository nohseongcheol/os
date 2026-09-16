/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "console"

const Bytespersector int = 512

type TAdvancedtechnologyattachment struct {
	master		bool
	dataport	TPort16bit
	хатоport	TPort8bit
	sectorcountport	TPort8bit
	lbalowport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	дастгоҳport	TPort8bit
	commandport	TPort8bit
	controlport	TPort8bit
}

func (self *TAdvancedtechnologyattachment) Init(master bool, portbase uint16) {
	self.master = master
	self.dataport.Init(portbase)
	self.хатоport.Init(portbase + 0x1)
	self.sectorcountport.Init(portbase + 0x2)
	self.lbalowport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.дастгоҳport.Init(portbase + 0x6)
	self.commandport.Init(portbase + 0x7)
	self.controlport.Init(portbase + 0x8)

}

func (self *TAdvancedtechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.дастгоҳport.Навиштан(0xA0)
	} else {
		self.дастгоҳport.Навиштан(0xB0)
	}
	self.controlport.Навиштан(0)
	self.дастгоҳport.Навиштан(0xA0)

	var status uint8 = self.commandport.Хондан()
	if status == 0xFF {
		console_2.MЧопкардан(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.дастгоҳport.Навиштан(0xA0)
	} else {
		self.дастгоҳport.Навиштан(0xB0)
	}
	self.sectorcountport.Навиштан(0)
	self.lbalowport.Навиштан(0)
	self.lbamidport.Навиштан(0)
	self.lbahiport.Навиштан(0)
	self.commandport.Навиштан(0xEC)

	status = self.commandport.Хондан()
	if status == 0x00 {
		console_2.MЧопкардан(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = self.commandport.Хондан()
	}

	if (status & 0x01) != 0 {
		console_2.MЧопкардан(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataport.Хондан()
		text := []byte("  ")
		text[0] = uint8((data >> 8) & 0xFF)
		text[1] = uint8(data & 0xFF)

	}
	console_2.MЧопкарданxy(([]byte)("ata ok"), 10, 22)

}
func (self *TAdvancedtechnologyattachment) Хондан28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MЧопкардан(([]byte)("ata read error "))
		return
	}
	if count > Bytespersector {
		console_2.MЧопкардан(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.дастгоҳport.Навиштан(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.дастгоҳport.Навиштан(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.хатоport.Навиштан(0)
	self.sectorcountport.Навиштан(1)

	self.lbalowport.Навиштан(uint8(sector & 0x000000FF))
	self.lbamidport.Навиштан(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Навиштан(uint8((sector & 0x00FF0000) >> 16))
	self.commandport.Навиштан(0x20)

	var status uint8 = self.commandport.Хондан()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.commandport.Хондан()
	}

	if (status & 0x01) != 0 {
		console_2.MЧопкардан(([]byte)("ata read error "))
		return
	}

	console_2.MЧопкарданxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataport.Хондан()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bytespersector; i += 2 {
		self.dataport.Хондан()
	}
}
func (self *TAdvancedtechnologyattachment) Навиштан28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.дастгоҳport.Навиштан(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.дастгоҳport.Навиштан(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.хатоport.Навиштан(0)
	self.sectorcountport.Навиштан(1)
	self.lbalowport.Навиштан(uint8(sectornumber & 0x000000FF))
	self.lbamidport.Навиштан(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiport.Навиштан(uint8((sectornumber & 0x00FF0000) >> 16))
	self.commandport.Навиштан(0x30)

	var console_2 = TConsole{}
	console_2.MЧопкардан(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataport.Навиштан(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		console_2.MЧопкардан(text)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataport.Навиштан(0x0000)
	}

}

func (self *TAdvancedtechnologyattachment) Flush() {
	if self.master {
		self.дастгоҳport.Навиштан(0xE0)
	} else {
		self.дастгоҳport.Навиштан(0xF0)
	}
	self.commandport.Навиштан(0xE7)

	var console_2 = TConsole{}

	var status uint8 = self.commandport.Хондан()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.commandport.Хондан()
	}
	if (status & 0x01) != 0 {
		console_2.MЧопкардан(([]byte)(" ata flush error"))
		return
	}

}
