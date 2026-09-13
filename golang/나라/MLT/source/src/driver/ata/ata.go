package ata

import . "port"
import . "console"

const Bytespersector int = 512

type TAdvancedtechnologyattachment struct {
	master		bool
	dataport	TPort16bit
	errorport	TPort8bit
	sectorcountport	TPort8bit
	lbalowport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	deviceport	TPort8bit
	commandport	TPort8bit
	controlport	TPort8bit
}

func (self *TAdvancedtechnologyattachment) Init(master bool, portbase uint16) {
	self.master = master
	self.dataport.Init(portbase)
	self.errorport.Init(portbase + 0x1)
	self.sectorcountport.Init(portbase + 0x2)
	self.lbalowport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.deviceport.Init(portbase + 0x6)
	self.commandport.Init(portbase + 0x7)
	self.controlport.Init(portbase + 0x8)

}

func (self *TAdvancedtechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.deviceport.Ikteb(0xA0)
	} else {
		self.deviceport.Ikteb(0xB0)
	}
	self.controlport.Ikteb(0)
	self.deviceport.Ikteb(0xA0)

	var status uint8 = self.commandport.Aqra()
	if status == 0xFF {
		console_2.MPrint(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.deviceport.Ikteb(0xA0)
	} else {
		self.deviceport.Ikteb(0xB0)
	}
	self.sectorcountport.Ikteb(0)
	self.lbalowport.Ikteb(0)
	self.lbamidport.Ikteb(0)
	self.lbahiport.Ikteb(0)
	self.commandport.Ikteb(0xEC)

	status = self.commandport.Aqra()
	if status == 0x00 {
		console_2.MPrint(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = self.commandport.Aqra()
	}

	if (status & 0x01) != 0 {
		console_2.MPrint(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataport.Aqra()
		text := []byte("  ")
		text[0] = uint8((data >> 8) & 0xFF)
		text[1] = uint8(data & 0xFF)

	}
	console_2.MPrintxy(([]byte)("ata ok"), 10, 22)

}
func (self *TAdvancedtechnologyattachment) Aqra28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MPrint(([]byte)("ata read error "))
		return
	}
	if count > Bytespersector {
		console_2.MPrint(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.deviceport.Ikteb(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.deviceport.Ikteb(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.errorport.Ikteb(0)
	self.sectorcountport.Ikteb(1)

	self.lbalowport.Ikteb(uint8(sector & 0x000000FF))
	self.lbamidport.Ikteb(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Ikteb(uint8((sector & 0x00FF0000) >> 16))
	self.commandport.Ikteb(0x20)

	var status uint8 = self.commandport.Aqra()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.commandport.Aqra()
	}

	if (status & 0x01) != 0 {
		console_2.MPrint(([]byte)("ata read error "))
		return
	}

	console_2.MPrintxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataport.Aqra()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bytespersector; i += 2 {
		self.dataport.Aqra()
	}
}
func (self *TAdvancedtechnologyattachment) Ikteb28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.deviceport.Ikteb(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.deviceport.Ikteb(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.errorport.Ikteb(0)
	self.sectorcountport.Ikteb(1)
	self.lbalowport.Ikteb(uint8(sectornumber & 0x000000FF))
	self.lbamidport.Ikteb(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiport.Ikteb(uint8((sectornumber & 0x00FF0000) >> 16))
	self.commandport.Ikteb(0x30)

	var console_2 = TConsole{}
	console_2.MPrint(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataport.Ikteb(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		console_2.MPrint(text)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataport.Ikteb(0x0000)
	}

}

func (self *TAdvancedtechnologyattachment) Flush() {
	if self.master {
		self.deviceport.Ikteb(0xE0)
	} else {
		self.deviceport.Ikteb(0xF0)
	}
	self.commandport.Ikteb(0xE7)

	var console_2 = TConsole{}

	var status uint8 = self.commandport.Aqra()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.commandport.Aqra()
	}
	if (status & 0x01) != 0 {
		console_2.MPrint(([]byte)(" ata flush error"))
		return
	}

}
