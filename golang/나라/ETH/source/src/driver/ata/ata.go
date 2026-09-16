/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "port"
import . "console"

const Bባይትስpersector int = 512

type Tጠለቅቴክኖሎጂattachment struct {
	ዋናው		bool
	dataport	TPort16bit
	ስህተትport	TPort8bit
	sectorcountport	TPort8bit
	lbaዝቅተኛport	TPort8bit
	lbamidport	TPort8bit
	lbahiport	TPort8bit
	ዲቫይስport	TPort8bit
	ትእዛዝport	TPort8bit
	controlport	TPort8bit
}

func (self *Tጠለቅቴክኖሎጂattachment) Init(ዋናው bool, portbase uint16) {
	self.ዋናው = ዋናው
	self.dataport.Init(portbase)
	self.ስህተትport.Init(portbase + 0x1)
	self.sectorcountport.Init(portbase + 0x2)
	self.lbaዝቅተኛport.Init(portbase + 0x3)
	self.lbamidport.Init(portbase + 0x4)
	self.lbahiport.Init(portbase + 0x5)
	self.ዲቫይስport.Init(portbase + 0x6)
	self.ትእዛዝport.Init(portbase + 0x7)
	self.controlport.Init(portbase + 0x8)

}

func (self *Tጠለቅቴክኖሎጂattachment) Identify() {

	var console_2 = TConsole{}

	if self.ዋናው {
		self.ዲቫይስport.Wመጻፊያ(0xA0)
	} else {
		self.ዲቫይስport.Wመጻፊያ(0xB0)
	}
	self.controlport.Wመጻፊያ(0)
	self.ዲቫይስport.Wመጻፊያ(0xA0)

	var ሁኔታ uint8 = self.ትእዛዝport.Rማንበቢያ()
	if ሁኔታ == 0xFF {
		console_2.Mማተሚያ(([]byte)("Invalid Status"))
		return
	}

	if self.ዋናው {
		self.ዲቫይስport.Wመጻፊያ(0xA0)
	} else {
		self.ዲቫይስport.Wመጻፊያ(0xB0)
	}
	self.sectorcountport.Wመጻፊያ(0)
	self.lbaዝቅተኛport.Wመጻፊያ(0)
	self.lbamidport.Wመጻፊያ(0)
	self.lbahiport.Wመጻፊያ(0)
	self.ትእዛዝport.Wመጻፊያ(0xEC)

	ሁኔታ = self.ትእዛዝport.Rማንበቢያ()
	if ሁኔታ == 0x00 {
		console_2.Mማተሚያ(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (ሁኔታ&0x80) == 0x80 && (ሁኔታ&0x01) != 0x01 {
		ሁኔታ = self.ትእዛዝport.Rማንበቢያ()
	}

	if (ሁኔታ & 0x01) != 0 {
		console_2.Mማተሚያ(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataport.Rማንበቢያ()
		ጽሁፍ := []byte("  ")
		ጽሁፍ[0] = uint8((data >> 8) & 0xFF)
		ጽሁፍ[1] = uint8(data & 0xFF)

	}
	console_2.Mማተሚያxy(([]byte)("ata ok"), 10, 22)

}
func (self *Tጠለቅቴክኖሎጂattachment) Rማንበቢያ28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.Mማተሚያ(([]byte)("ata read error "))
		return
	}
	if count > Bባይትስpersector {
		console_2.Mማተሚያ(([]byte)("ata read error "))
		return
	}

	if self.ዋናው {
		self.ዲቫይስport.Wመጻፊያ(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.ዲቫይስport.Wመጻፊያ(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.ስህተትport.Wመጻፊያ(0)
	self.sectorcountport.Wመጻፊያ(1)

	self.lbaዝቅተኛport.Wመጻፊያ(uint8(sector & 0x000000FF))
	self.lbamidport.Wመጻፊያ(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiport.Wመጻፊያ(uint8((sector & 0x00FF0000) >> 16))
	self.ትእዛዝport.Wመጻፊያ(0x20)

	var ሁኔታ uint8 = self.ትእዛዝport.Rማንበቢያ()
	for ((ሁኔታ & 0x80) == 0x80) && ((ሁኔታ & 0x01) != 0x01) {
		ሁኔታ = self.ትእዛዝport.Rማንበቢያ()
	}

	if (ሁኔታ & 0x01) != 0 {
		console_2.Mማተሚያ(([]byte)("ata read error "))
		return
	}

	console_2.Mማተሚያxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataport.Rማንበቢያ()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bባይትስpersector; i += 2 {
		self.dataport.Rማንበቢያ()
	}
}
func (self *Tጠለቅቴክኖሎጂattachment) Wመጻፊያ28(sectorቁጥር uint32, data []byte, count uint32) {

	if sectorቁጥር > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.ዋናው {
		self.ዲቫይስport.Wመጻፊያ(uint8(0xE0 | uint8((sectorቁጥር&0x0F000000)>>24)))
	} else {
		self.ዲቫይስport.Wመጻፊያ(uint8(0xF0 | uint8((sectorቁጥር&0x0F000000)>>24)))
	}

	self.ስህተትport.Wመጻፊያ(0)
	self.sectorcountport.Wመጻፊያ(1)
	self.lbaዝቅተኛport.Wመጻፊያ(uint8(sectorቁጥር & 0x000000FF))
	self.lbamidport.Wመጻፊያ(uint8((sectorቁጥር & 0x0000FF00) >> 8))
	self.lbahiport.Wመጻፊያ(uint8((sectorቁጥር & 0x00FF0000) >> 16))
	self.ትእዛዝport.Wመጻፊያ(0x30)

	var console_2 = TConsole{}
	console_2.Mማተሚያ(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataport.Wመጻፊያ(wdata)

		ጽሁፍ := []byte("  ")
		ጽሁፍ[0] = uint8((wdata >> 8) & 0xFF)
		ጽሁፍ[1] = uint8(wdata & 0xFF)

		console_2.Mማተሚያ(ጽሁፍ)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataport.Wመጻፊያ(0x0000)
	}

}

func (self *Tጠለቅቴክኖሎጂattachment) Flush() {
	if self.ዋናው {
		self.ዲቫይስport.Wመጻፊያ(0xE0)
	} else {
		self.ዲቫይስport.Wመጻፊያ(0xF0)
	}
	self.ትእዛዝport.Wመጻፊያ(0xE7)

	var console_2 = TConsole{}

	var ሁኔታ uint8 = self.ትእዛዝport.Rማንበቢያ()
	if ሁኔታ == 0x00 {
		return
	}

	for ((ሁኔታ & 0x80) == 0x80) && ((ሁኔታ & 0x01) != 0x01) {
		ሁኔታ = self.ትእዛዝport.Rማንበቢያ()
	}
	if (ሁኔታ & 0x01) != 0 {
		console_2.Mማተሚያ(([]byte)(" ata flush error"))
		return
	}

}
