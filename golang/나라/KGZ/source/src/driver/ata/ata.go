/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "порт"
import . "console"

const Байтpersector int = 512

type TКеңейтилгенТехнологияattachment struct {
	master		bool
	dataПорт	TПорт16bit
	катаПорт	TПорт8bit
	sectorcountПорт	TПорт8bit
	lbalowПорт	TПорт8bit
	lbamidПорт	TПорт8bit
	lbahiПорт	TПорт8bit
	түзүлүшүПорт	TПорт8bit
	командаПорт	TПорт8bit
	controlПорт	TПорт8bit
}

func (self *TКеңейтилгенТехнологияattachment) Init(master bool, портbase uint16) {
	self.master = master
	self.dataПорт.Init(портbase)
	self.катаПорт.Init(портbase + 0x1)
	self.sectorcountПорт.Init(портbase + 0x2)
	self.lbalowПорт.Init(портbase + 0x3)
	self.lbamidПорт.Init(портbase + 0x4)
	self.lbahiПорт.Init(портbase + 0x5)
	self.түзүлүшүПорт.Init(портbase + 0x6)
	self.командаПорт.Init(портbase + 0x7)
	self.controlПорт.Init(портbase + 0x8)

}

func (self *TКеңейтилгенТехнологияattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.түзүлүшүПорт.Жазуу(0xA0)
	} else {
		self.түзүлүшүПорт.Жазуу(0xB0)
	}
	self.controlПорт.Жазуу(0)
	self.түзүлүшүПорт.Жазуу(0xA0)

	var абалы uint8 = self.командаПорт.Окуу()
	if абалы == 0xFF {
		console_2.MБасма(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.түзүлүшүПорт.Жазуу(0xA0)
	} else {
		self.түзүлүшүПорт.Жазуу(0xB0)
	}
	self.sectorcountПорт.Жазуу(0)
	self.lbalowПорт.Жазуу(0)
	self.lbamidПорт.Жазуу(0)
	self.lbahiПорт.Жазуу(0)
	self.командаПорт.Жазуу(0xEC)

	абалы = self.командаПорт.Окуу()
	if абалы == 0x00 {
		console_2.MБасма(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (абалы&0x80) == 0x80 && (абалы&0x01) != 0x01 {
		абалы = self.командаПорт.Окуу()
	}

	if (абалы & 0x01) != 0 {
		console_2.MБасма(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataПорт.Окуу()
		текст := []byte("  ")
		текст[0] = uint8((data >> 8) & 0xFF)
		текст[1] = uint8(data & 0xFF)

	}
	console_2.MБасмаxy(([]byte)("ata ok"), 10, 22)

}
func (self *TКеңейтилгенТехнологияattachment) Окуу28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MБасма(([]byte)("ata read error "))
		return
	}
	if count > Байтpersector {
		console_2.MБасма(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.түзүлүшүПорт.Жазуу(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.түзүлүшүПорт.Жазуу(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.катаПорт.Жазуу(0)
	self.sectorcountПорт.Жазуу(1)

	self.lbalowПорт.Жазуу(uint8(sector & 0x000000FF))
	self.lbamidПорт.Жазуу(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiПорт.Жазуу(uint8((sector & 0x00FF0000) >> 16))
	self.командаПорт.Жазуу(0x20)

	var абалы uint8 = self.командаПорт.Окуу()
	for ((абалы & 0x80) == 0x80) && ((абалы & 0x01) != 0x01) {
		абалы = self.командаПорт.Окуу()
	}

	if (абалы & 0x01) != 0 {
		console_2.MБасма(([]byte)("ata read error "))
		return
	}

	console_2.MБасмаxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataПорт.Окуу()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Байтpersector; i += 2 {
		self.dataПорт.Окуу()
	}
}
func (self *TКеңейтилгенТехнологияattachment) Жазуу28(sectorНОМЕР uint32, data []byte, count uint32) {

	if sectorНОМЕР > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.түзүлүшүПорт.Жазуу(uint8(0xE0 | uint8((sectorНОМЕР&0x0F000000)>>24)))
	} else {
		self.түзүлүшүПорт.Жазуу(uint8(0xF0 | uint8((sectorНОМЕР&0x0F000000)>>24)))
	}

	self.катаПорт.Жазуу(0)
	self.sectorcountПорт.Жазуу(1)
	self.lbalowПорт.Жазуу(uint8(sectorНОМЕР & 0x000000FF))
	self.lbamidПорт.Жазуу(uint8((sectorНОМЕР & 0x0000FF00) >> 8))
	self.lbahiПорт.Жазуу(uint8((sectorНОМЕР & 0x00FF0000) >> 16))
	self.командаПорт.Жазуу(0x30)

	var console_2 = TConsole{}
	console_2.MБасма(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataПорт.Жазуу(wdata)

		текст := []byte("  ")
		текст[0] = uint8((wdata >> 8) & 0xFF)
		текст[1] = uint8(wdata & 0xFF)

		console_2.MБасма(текст)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataПорт.Жазуу(0x0000)
	}

}

func (self *TКеңейтилгенТехнологияattachment) Flush() {
	if self.master {
		self.түзүлүшүПорт.Жазуу(0xE0)
	} else {
		self.түзүлүшүПорт.Жазуу(0xF0)
	}
	self.командаПорт.Жазуу(0xE7)

	var console_2 = TConsole{}

	var абалы uint8 = self.командаПорт.Окуу()
	if абалы == 0x00 {
		return
	}

	for ((абалы & 0x80) == 0x80) && ((абалы & 0x01) != 0x01) {
		абалы = self.командаПорт.Окуу()
	}
	if (абалы & 0x01) != 0 {
		console_2.MБасма(([]byte)(" ata flush error"))
		return
	}

}
