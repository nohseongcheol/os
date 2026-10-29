/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "პორტი"
import . "console"

const Bბაიტიpersector int = 512

type Tდეტალურიtechnologyattachment struct {
	master			bool
	dataპორტი		Tპორტი16bit
	შეცდომაპორტი		Tპორტი8bit
	sectorcountპორტი	Tპორტი8bit
	lbalowპორტი		Tპორტი8bit
	lbamidპორტი		Tპორტი8bit
	lbahiპორტი		Tპორტი8bit
	მოწყობილობაპორტი	Tპორტი8bit
	ბრძანებაპორტი		Tპორტი8bit
	controlპორტი		Tპორტი8bit
}

func (self *Tდეტალურიtechnologyattachment) Init(master bool, პორტიbase uint16) {
	self.master = master
	self.dataპორტი.Init(პორტიbase)
	self.შეცდომაპორტი.Init(პორტიbase + 0x1)
	self.sectorcountპორტი.Init(პორტიbase + 0x2)
	self.lbalowპორტი.Init(პორტიbase + 0x3)
	self.lbamidპორტი.Init(პორტიbase + 0x4)
	self.lbahiპორტი.Init(პორტიbase + 0x5)
	self.მოწყობილობაპორტი.Init(პორტიbase + 0x6)
	self.ბრძანებაპორტი.Init(პორტიbase + 0x7)
	self.controlპორტი.Init(პორტიbase + 0x8)

}

func (self *Tდეტალურიtechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.მოწყობილობაპორტი.Wჩაწერა(0xA0)
	} else {
		self.მოწყობილობაპორტი.Wჩაწერა(0xB0)
	}
	self.controlპორტი.Wჩაწერა(0)
	self.მოწყობილობაპორტი.Wჩაწერა(0xA0)

	var სტატუსი uint8 = self.ბრძანებაპორტი.Rკითხვა()
	if სტატუსი == 0xFF {
		console_2.Mბეჭდვა(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.მოწყობილობაპორტი.Wჩაწერა(0xA0)
	} else {
		self.მოწყობილობაპორტი.Wჩაწერა(0xB0)
	}
	self.sectorcountპორტი.Wჩაწერა(0)
	self.lbalowპორტი.Wჩაწერა(0)
	self.lbamidპორტი.Wჩაწერა(0)
	self.lbahiპორტი.Wჩაწერა(0)
	self.ბრძანებაპორტი.Wჩაწერა(0xEC)

	სტატუსი = self.ბრძანებაპორტი.Rკითხვა()
	if სტატუსი == 0x00 {
		console_2.Mბეჭდვა(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (სტატუსი&0x80) == 0x80 && (სტატუსი&0x01) != 0x01 {
		სტატუსი = self.ბრძანებაპორტი.Rკითხვა()
	}

	if (სტატუსი & 0x01) != 0 {
		console_2.Mბეჭდვა(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataპორტი.Rკითხვა()
		ტექსტი := []byte("  ")
		ტექსტი[0] = uint8((data >> 8) & 0xFF)
		ტექსტი[1] = uint8(data & 0xFF)

	}
	console_2.Mბეჭდვაxy(([]byte)("ata ok"), 10, 22)

}
func (self *Tდეტალურიtechnologyattachment) Rკითხვა28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.Mბეჭდვა(([]byte)("ata read error "))
		return
	}
	if count > Bბაიტიpersector {
		console_2.Mბეჭდვა(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.მოწყობილობაპორტი.Wჩაწერა(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.მოწყობილობაპორტი.Wჩაწერა(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.შეცდომაპორტი.Wჩაწერა(0)
	self.sectorcountპორტი.Wჩაწერა(1)

	self.lbalowპორტი.Wჩაწერა(uint8(sector & 0x000000FF))
	self.lbamidპორტი.Wჩაწერა(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiპორტი.Wჩაწერა(uint8((sector & 0x00FF0000) >> 16))
	self.ბრძანებაპორტი.Wჩაწერა(0x20)

	var სტატუსი uint8 = self.ბრძანებაპორტი.Rკითხვა()
	for ((სტატუსი & 0x80) == 0x80) && ((სტატუსი & 0x01) != 0x01) {
		სტატუსი = self.ბრძანებაპორტი.Rკითხვა()
	}

	if (სტატუსი & 0x01) != 0 {
		console_2.Mბეჭდვა(([]byte)("ata read error "))
		return
	}

	console_2.Mბეჭდვაxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataპორტი.Rკითხვა()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bბაიტიpersector; i += 2 {
		self.dataპორტი.Rკითხვა()
	}
}
func (self *Tდეტალურიtechnologyattachment) Wჩაწერა28(sectorრიცხვი uint32, data []byte, count uint32) {

	if sectorრიცხვი > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.მოწყობილობაპორტი.Wჩაწერა(uint8(0xE0 | uint8((sectorრიცხვი&0x0F000000)>>24)))
	} else {
		self.მოწყობილობაპორტი.Wჩაწერა(uint8(0xF0 | uint8((sectorრიცხვი&0x0F000000)>>24)))
	}

	self.შეცდომაპორტი.Wჩაწერა(0)
	self.sectorcountპორტი.Wჩაწერა(1)
	self.lbalowპორტი.Wჩაწერა(uint8(sectorრიცხვი & 0x000000FF))
	self.lbamidპორტი.Wჩაწერა(uint8((sectorრიცხვი & 0x0000FF00) >> 8))
	self.lbahiპორტი.Wჩაწერა(uint8((sectorრიცხვი & 0x00FF0000) >> 16))
	self.ბრძანებაპორტი.Wჩაწერა(0x30)

	var console_2 = TConsole{}
	console_2.Mბეჭდვა(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataპორტი.Wჩაწერა(wdata)

		ტექსტი := []byte("  ")
		ტექსტი[0] = uint8((wdata >> 8) & 0xFF)
		ტექსტი[1] = uint8(wdata & 0xFF)

		console_2.Mბეჭდვა(ტექსტი)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataპორტი.Wჩაწერა(0x0000)
	}

}

func (self *Tდეტალურიtechnologyattachment) Flush() {
	if self.master {
		self.მოწყობილობაპორტი.Wჩაწერა(0xE0)
	} else {
		self.მოწყობილობაპორტი.Wჩაწერა(0xF0)
	}
	self.ბრძანებაპორტი.Wჩაწერა(0xE7)

	var console_2 = TConsole{}

	var სტატუსი uint8 = self.ბრძანებაპორტი.Rკითხვა()
	if სტატუსი == 0x00 {
		return
	}

	for ((სტატუსი & 0x80) == 0x80) && ((სტატუსი & 0x01) != 0x01) {
		სტატუსი = self.ბრძანებაპორტი.Rკითხვა()
	}
	if (სტატუსი & 0x01) != 0 {
		console_2.Mბეჭდვა(([]byte)(" ata flush error"))
		return
	}

}
