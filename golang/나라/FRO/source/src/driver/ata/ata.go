package ata

import . "port"
import . "console"

const Býtpersector int = 512

type TFramkomiðtechnologyattachment struct {
	master		bool
	dataport	TPort16bit
	brekport	TPort8bit
	sectorcountport	TPort8bit
	lbaLágurport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	deviceport	TPort8bit
	stýriboðport	TPort8bit
	controlport	TPort8bit
}

func (self *TFramkomiðtechnologyattachment) Init(master bool, portbase uint16) {
	self.master = master
	self.dataport.Init(portbase)
	self.brekport.Init(portbase + 0x1)
	self.sectorcountport.Init(portbase + 0x2)
	self.lbaLágurport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.deviceport.Init(portbase + 0x6)
	self.stýriboðport.Init(portbase + 0x7)
	self.controlport.Init(portbase + 0x8)

}

func (self *TFramkomiðtechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.deviceport.Skriva(0xA0)
	} else {
		self.deviceport.Skriva(0xB0)
	}
	self.controlport.Skriva(0)
	self.deviceport.Skriva(0xA0)

	var status uint8 = self.stýriboðport.Lesa()
	if status == 0xFF {
		console_2.MPrint(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.deviceport.Skriva(0xA0)
	} else {
		self.deviceport.Skriva(0xB0)
	}
	self.sectorcountport.Skriva(0)
	self.lbaLágurport.Skriva(0)
	self.lbamidport.Skriva(0)
	self.lbahiport.Skriva(0)
	self.stýriboðport.Skriva(0xEC)

	status = self.stýriboðport.Lesa()
	if status == 0x00 {
		console_2.MPrint(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (status&0x80) == 0x80 && (status&0x01) != 0x01 {
		status = self.stýriboðport.Lesa()
	}

	if (status & 0x01) != 0 {
		console_2.MPrint(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataport.Lesa()
		text := []byte("  ")
		text[0] = uint8((data >> 8) & 0xFF)
		text[1] = uint8(data & 0xFF)

	}
	console_2.MPrintxy(([]byte)("ata ok"), 10, 22)

}
func (self *TFramkomiðtechnologyattachment) Lesa28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MPrint(([]byte)("ata read error "))
		return
	}
	if count > Býtpersector {
		console_2.MPrint(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.deviceport.Skriva(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.deviceport.Skriva(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.brekport.Skriva(0)
	self.sectorcountport.Skriva(1)

	self.lbaLágurport.Skriva(uint8(sector & 0x000000FF))
	self.lbamidport.Skriva(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Skriva(uint8((sector & 0x00FF0000) >> 16))
	self.stýriboðport.Skriva(0x20)

	var status uint8 = self.stýriboðport.Lesa()
	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.stýriboðport.Lesa()
	}

	if (status & 0x01) != 0 {
		console_2.MPrint(([]byte)("ata read error "))
		return
	}

	console_2.MPrintxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataport.Lesa()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Býtpersector; i += 2 {
		self.dataport.Lesa()
	}
}
func (self *TFramkomiðtechnologyattachment) Skriva28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.deviceport.Skriva(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.deviceport.Skriva(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.brekport.Skriva(0)
	self.sectorcountport.Skriva(1)
	self.lbaLágurport.Skriva(uint8(sectornumber & 0x000000FF))
	self.lbamidport.Skriva(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiport.Skriva(uint8((sectornumber & 0x00FF0000) >> 16))
	self.stýriboðport.Skriva(0x30)

	var console_2 = TConsole{}
	console_2.MPrint(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataport.Skriva(wdata)

		text := []byte("  ")
		text[0] = uint8((wdata >> 8) & 0xFF)
		text[1] = uint8(wdata & 0xFF)

		console_2.MPrint(text)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataport.Skriva(0x0000)
	}

}

func (self *TFramkomiðtechnologyattachment) Flush() {
	if self.master {
		self.deviceport.Skriva(0xE0)
	} else {
		self.deviceport.Skriva(0xF0)
	}
	self.stýriboðport.Skriva(0xE7)

	var console_2 = TConsole{}

	var status uint8 = self.stýriboðport.Lesa()
	if status == 0x00 {
		return
	}

	for ((status & 0x80) == 0x80) && ((status & 0x01) != 0x01) {
		status = self.stýriboðport.Lesa()
	}
	if (status & 0x01) != 0 {
		console_2.MPrint(([]byte)(" ata flush error"))
		return
	}

}
