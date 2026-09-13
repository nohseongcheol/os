package ata

import . "پورٹ"
import . "console"

const Bبائٹسpersector int = 512

type Tاعلیٹیکنالوجیattachment struct {
	master		bool
	dataپورٹ	Tپورٹ16bit
	غلطیپورٹ	Tپورٹ8bit
	sectorcountپورٹ	Tپورٹ8bit
	lbaکمپورٹ	Tپورٹ8bit
	lbamidپورٹ	Tپورٹ8bit
	lbahiپورٹ	Tپورٹ8bit
	آلہپورٹ		Tپورٹ8bit
	کمانڈپورٹ	Tپورٹ8bit
	controlپورٹ	Tپورٹ8bit
}

func (self *Tاعلیٹیکنالوجیattachment) Init(master bool, پورٹbase uint16) {
	self.master = master
	self.dataپورٹ.Init(پورٹbase)
	self.غلطیپورٹ.Init(پورٹbase + 0x1)
	self.sectorcountپورٹ.Init(پورٹbase + 0x2)
	self.lbaکمپورٹ.Init(پورٹbase + 0x3)
	self.lbamidپورٹ.Init(پورٹbase + 0x4)
	self.lbahiپورٹ.Init(پورٹbase + 0x5)
	self.آلہپورٹ.Init(پورٹbase + 0x6)
	self.کمانڈپورٹ.Init(پورٹbase + 0x7)
	self.controlپورٹ.Init(پورٹbase + 0x8)

}

func (self *Tاعلیٹیکنالوجیattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.آلہپورٹ.Wلکھیں(0xA0)
	} else {
		self.آلہپورٹ.Wلکھیں(0xB0)
	}
	self.controlپورٹ.Wلکھیں(0)
	self.آلہپورٹ.Wلکھیں(0xA0)

	var حالت uint8 = self.کمانڈپورٹ.Rپڑھیں()
	if حالت == 0xFF {
		console_2.Mچھاپیں(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.آلہپورٹ.Wلکھیں(0xA0)
	} else {
		self.آلہپورٹ.Wلکھیں(0xB0)
	}
	self.sectorcountپورٹ.Wلکھیں(0)
	self.lbaکمپورٹ.Wلکھیں(0)
	self.lbamidپورٹ.Wلکھیں(0)
	self.lbahiپورٹ.Wلکھیں(0)
	self.کمانڈپورٹ.Wلکھیں(0xEC)

	حالت = self.کمانڈپورٹ.Rپڑھیں()
	if حالت == 0x00 {
		console_2.Mچھاپیں(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (حالت&0x80) == 0x80 && (حالت&0x01) != 0x01 {
		حالت = self.کمانڈپورٹ.Rپڑھیں()
	}

	if (حالت & 0x01) != 0 {
		console_2.Mچھاپیں(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataپورٹ.Rپڑھیں()
		متن := []byte("  ")
		متن[0] = uint8((data >> 8) & 0xFF)
		متن[1] = uint8(data & 0xFF)

	}
	console_2.Mچھاپیںxy(([]byte)("ata ok"), 10, 22)

}
func (self *Tاعلیٹیکنالوجیattachment) Rپڑھیں28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.Mچھاپیں(([]byte)("ata read error "))
		return
	}
	if count > Bبائٹسpersector {
		console_2.Mچھاپیں(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.آلہپورٹ.Wلکھیں(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.آلہپورٹ.Wلکھیں(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.غلطیپورٹ.Wلکھیں(0)
	self.sectorcountپورٹ.Wلکھیں(1)

	self.lbaکمپورٹ.Wلکھیں(uint8(sector & 0x000000FF))
	self.lbamidپورٹ.Wلکھیں(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiپورٹ.Wلکھیں(uint8((sector & 0x00FF0000) >> 16))
	self.کمانڈپورٹ.Wلکھیں(0x20)

	var حالت uint8 = self.کمانڈپورٹ.Rپڑھیں()
	for ((حالت & 0x80) == 0x80) && ((حالت & 0x01) != 0x01) {
		حالت = self.کمانڈپورٹ.Rپڑھیں()
	}

	if (حالت & 0x01) != 0 {
		console_2.Mچھاپیں(([]byte)("ata read error "))
		return
	}

	console_2.Mچھاپیںxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataپورٹ.Rپڑھیں()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bبائٹسpersector; i += 2 {
		self.dataپورٹ.Rپڑھیں()
	}
}
func (self *Tاعلیٹیکنالوجیattachment) Wلکھیں28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.آلہپورٹ.Wلکھیں(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.آلہپورٹ.Wلکھیں(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.غلطیپورٹ.Wلکھیں(0)
	self.sectorcountپورٹ.Wلکھیں(1)
	self.lbaکمپورٹ.Wلکھیں(uint8(sectornumber & 0x000000FF))
	self.lbamidپورٹ.Wلکھیں(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiپورٹ.Wلکھیں(uint8((sectornumber & 0x00FF0000) >> 16))
	self.کمانڈپورٹ.Wلکھیں(0x30)

	var console_2 = TConsole{}
	console_2.Mچھاپیں(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataپورٹ.Wلکھیں(wdata)

		متن := []byte("  ")
		متن[0] = uint8((wdata >> 8) & 0xFF)
		متن[1] = uint8(wdata & 0xFF)

		console_2.Mچھاپیں(متن)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataپورٹ.Wلکھیں(0x0000)
	}

}

func (self *Tاعلیٹیکنالوجیattachment) Flush() {
	if self.master {
		self.آلہپورٹ.Wلکھیں(0xE0)
	} else {
		self.آلہپورٹ.Wلکھیں(0xF0)
	}
	self.کمانڈپورٹ.Wلکھیں(0xE7)

	var console_2 = TConsole{}

	var حالت uint8 = self.کمانڈپورٹ.Rپڑھیں()
	if حالت == 0x00 {
		return
	}

	for ((حالت & 0x80) == 0x80) && ((حالت & 0x01) != 0x01) {
		حالت = self.کمانڈپورٹ.Rپڑھیں()
	}
	if (حالت & 0x01) != 0 {
		console_2.Mچھاپیں(([]byte)(" ata flush error"))
		return
	}

}
