/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "qapı"
import . "console"

const Baytpersector int = 512

type TƏtraflıtechnologyattachment struct {
	master		bool
	dataQapı	TQapı16bit
	xətaQapı	TQapı8bit
	sectorcountQapı	TQapı8bit
	lbaAlçaqQapı	TQapı8bit
	lbamidQapı	TQapı8bit
	lbahiQapı	TQapı8bit
	avadanlıqQapı	TQapı8bit
	əmrQapı		TQapı8bit
	controlQapı	TQapı8bit
}

func (self *TƏtraflıtechnologyattachment) Init(master bool, qapıbase uint16) {
	self.master = master
	self.dataQapı.Init(qapıbase)
	self.xətaQapı.Init(qapıbase + 0x1)
	self.sectorcountQapı.Init(qapıbase + 0x2)
	self.lbaAlçaqQapı.Init(qapıbase + 0x3)
	self.lbamidQapı.Init(qapıbase + 0x4)
	self.lbahiQapı.Init(qapıbase + 0x5)
	self.avadanlıqQapı.Init(qapıbase + 0x6)
	self.əmrQapı.Init(qapıbase + 0x7)
	self.controlQapı.Init(qapıbase + 0x8)

}

func (self *TƏtraflıtechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.avadanlıqQapı.Yazma(0xA0)
	} else {
		self.avadanlıqQapı.Yazma(0xB0)
	}
	self.controlQapı.Yazma(0)
	self.avadanlıqQapı.Yazma(0xA0)

	var vəziyyət uint8 = self.əmrQapı.Oxuma()
	if vəziyyət == 0xFF {
		console_2.MÇapEt(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.avadanlıqQapı.Yazma(0xA0)
	} else {
		self.avadanlıqQapı.Yazma(0xB0)
	}
	self.sectorcountQapı.Yazma(0)
	self.lbaAlçaqQapı.Yazma(0)
	self.lbamidQapı.Yazma(0)
	self.lbahiQapı.Yazma(0)
	self.əmrQapı.Yazma(0xEC)

	vəziyyət = self.əmrQapı.Oxuma()
	if vəziyyət == 0x00 {
		console_2.MÇapEt(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (vəziyyət&0x80) == 0x80 && (vəziyyət&0x01) != 0x01 {
		vəziyyət = self.əmrQapı.Oxuma()
	}

	if (vəziyyət & 0x01) != 0 {
		console_2.MÇapEt(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataQapı.Oxuma()
		mətn := []byte("  ")
		mətn[0] = uint8((data >> 8) & 0xFF)
		mətn[1] = uint8(data & 0xFF)

	}
	console_2.MÇapEtxy(([]byte)("ata ok"), 10, 22)

}
func (self *TƏtraflıtechnologyattachment) Oxuma28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MÇapEt(([]byte)("ata read error "))
		return
	}
	if count > Baytpersector {
		console_2.MÇapEt(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.avadanlıqQapı.Yazma(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.avadanlıqQapı.Yazma(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.xətaQapı.Yazma(0)
	self.sectorcountQapı.Yazma(1)

	self.lbaAlçaqQapı.Yazma(uint8(sector & 0x000000FF))
	self.lbamidQapı.Yazma(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiQapı.Yazma(uint8((sector & 0x00FF0000) >> 16))
	self.əmrQapı.Yazma(0x20)

	var vəziyyət uint8 = self.əmrQapı.Oxuma()
	for ((vəziyyət & 0x80) == 0x80) && ((vəziyyət & 0x01) != 0x01) {
		vəziyyət = self.əmrQapı.Oxuma()
	}

	if (vəziyyət & 0x01) != 0 {
		console_2.MÇapEt(([]byte)("ata read error "))
		return
	}

	console_2.MÇapEtxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataQapı.Oxuma()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Baytpersector; i += 2 {
		self.dataQapı.Oxuma()
	}
}
func (self *TƏtraflıtechnologyattachment) Yazma28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.avadanlıqQapı.Yazma(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.avadanlıqQapı.Yazma(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.xətaQapı.Yazma(0)
	self.sectorcountQapı.Yazma(1)
	self.lbaAlçaqQapı.Yazma(uint8(sectornumber & 0x000000FF))
	self.lbamidQapı.Yazma(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiQapı.Yazma(uint8((sectornumber & 0x00FF0000) >> 16))
	self.əmrQapı.Yazma(0x30)

	var console_2 = TConsole{}
	console_2.MÇapEt(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataQapı.Yazma(wdata)

		mətn := []byte("  ")
		mətn[0] = uint8((wdata >> 8) & 0xFF)
		mətn[1] = uint8(wdata & 0xFF)

		console_2.MÇapEt(mətn)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataQapı.Yazma(0x0000)
	}

}

func (self *TƏtraflıtechnologyattachment) Flush() {
	if self.master {
		self.avadanlıqQapı.Yazma(0xE0)
	} else {
		self.avadanlıqQapı.Yazma(0xF0)
	}
	self.əmrQapı.Yazma(0xE7)

	var console_2 = TConsole{}

	var vəziyyət uint8 = self.əmrQapı.Oxuma()
	if vəziyyət == 0x00 {
		return
	}

	for ((vəziyyət & 0x80) == 0x80) && ((vəziyyət & 0x01) != 0x01) {
		vəziyyət = self.əmrQapı.Oxuma()
	}
	if (vəziyyət & 0x01) != 0 {
		console_2.MÇapEt(([]byte)(" ata flush error"))
		return
	}

}
