/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "שער"
import . "console"

const Bבתיםpersector int = 512

type Tמתקדםטכנולוגיהattachment struct {
	master		bool
	dataשער		Tשער16bit
	שגיאהשער	Tשער8bit
	sectorcountשער	Tשער8bit
	lbaנמוךשער	Tשער8bit
	lbamidשער	Tשער8bit
	lbahiשער	Tשער8bit
	התקןשער		Tשער8bit
	פקודהשער	Tשער8bit
	בקרהשער		Tשער8bit
}

func (self *Tמתקדםטכנולוגיהattachment) Init(master bool, שערbase uint16) {
	self.master = master
	self.dataשער.Init(שערbase)
	self.שגיאהשער.Init(שערbase + 0x1)
	self.sectorcountשער.Init(שערbase + 0x2)
	self.lbaנמוךשער.Init(שערbase + 0x3)
	self.lbamidשער.Init(שערbase + 0x4)
	self.lbahiשער.Init(שערbase + 0x5)
	self.התקןשער.Init(שערbase + 0x6)
	self.פקודהשער.Init(שערbase + 0x7)
	self.בקרהשער.Init(שערbase + 0x8)

}

func (self *Tמתקדםטכנולוגיהattachment) Identify() {

	var console_2 = TConsole{}

	if self.master {
		self.התקןשער.Wכתיבה(0xA0)
	} else {
		self.התקןשער.Wכתיבה(0xB0)
	}
	self.בקרהשער.Wכתיבה(0)
	self.התקןשער.Wכתיבה(0xA0)

	var מצב_2 uint8 = self.פקודהשער.Rקריאה()
	if מצב_2 == 0xFF {
		console_2.Mהדפסה(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.התקןשער.Wכתיבה(0xA0)
	} else {
		self.התקןשער.Wכתיבה(0xB0)
	}
	self.sectorcountשער.Wכתיבה(0)
	self.lbaנמוךשער.Wכתיבה(0)
	self.lbamidשער.Wכתיבה(0)
	self.lbahiשער.Wכתיבה(0)
	self.פקודהשער.Wכתיבה(0xEC)

	מצב_2 = self.פקודהשער.Rקריאה()
	if מצב_2 == 0x00 {
		console_2.Mהדפסה(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (מצב_2&0x80) == 0x80 && (מצב_2&0x01) != 0x01 {
		מצב_2 = self.פקודהשער.Rקריאה()
	}

	if (מצב_2 & 0x01) != 0 {
		console_2.Mהדפסה(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataשער.Rקריאה()
		טקסט := []byte("  ")
		טקסט[0] = uint8((data >> 8) & 0xFF)
		טקסט[1] = uint8(data & 0xFF)

	}
	console_2.Mהדפסהxy(([]byte)("ata ok"), 10, 22)

}
func (self *Tמתקדםטכנולוגיהattachment) Rקריאה28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.Mהדפסה(([]byte)("ata read error "))
		return
	}
	if count > Bבתיםpersector {
		console_2.Mהדפסה(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.התקןשער.Wכתיבה(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.התקןשער.Wכתיבה(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.שגיאהשער.Wכתיבה(0)
	self.sectorcountשער.Wכתיבה(1)

	self.lbaנמוךשער.Wכתיבה(uint8(sector & 0x000000FF))
	self.lbamidשער.Wכתיבה(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiשער.Wכתיבה(uint8((sector & 0x00FF0000) >> 16))
	self.פקודהשער.Wכתיבה(0x20)

	var מצב_2 uint8 = self.פקודהשער.Rקריאה()
	for ((מצב_2 & 0x80) == 0x80) && ((מצב_2 & 0x01) != 0x01) {
		מצב_2 = self.פקודהשער.Rקריאה()
	}

	if (מצב_2 & 0x01) != 0 {
		console_2.Mהדפסה(([]byte)("ata read error "))
		return
	}

	console_2.Mהדפסהxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataשער.Rקריאה()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bבתיםpersector; i += 2 {
		self.dataשער.Rקריאה()
	}
}
func (self *Tמתקדםטכנולוגיהattachment) Wכתיבה28(sectorמספר uint32, data []byte, count uint32) {

	if sectorמספר > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.התקןשער.Wכתיבה(uint8(0xE0 | uint8((sectorמספר&0x0F000000)>>24)))
	} else {
		self.התקןשער.Wכתיבה(uint8(0xF0 | uint8((sectorמספר&0x0F000000)>>24)))
	}

	self.שגיאהשער.Wכתיבה(0)
	self.sectorcountשער.Wכתיבה(1)
	self.lbaנמוךשער.Wכתיבה(uint8(sectorמספר & 0x000000FF))
	self.lbamidשער.Wכתיבה(uint8((sectorמספר & 0x0000FF00) >> 8))
	self.lbahiשער.Wכתיבה(uint8((sectorמספר & 0x00FF0000) >> 16))
	self.פקודהשער.Wכתיבה(0x30)

	var console_2 = TConsole{}
	console_2.Mהדפסה(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataשער.Wכתיבה(wdata)

		טקסט := []byte("  ")
		טקסט[0] = uint8((wdata >> 8) & 0xFF)
		טקסט[1] = uint8(wdata & 0xFF)

		console_2.Mהדפסה(טקסט)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataשער.Wכתיבה(0x0000)
	}

}

func (self *Tמתקדםטכנולוגיהattachment) Flush() {
	if self.master {
		self.התקןשער.Wכתיבה(0xE0)
	} else {
		self.התקןשער.Wכתיבה(0xF0)
	}
	self.פקודהשער.Wכתיבה(0xE7)

	var console_2 = TConsole{}

	var מצב_2 uint8 = self.פקודהשער.Rקריאה()
	if מצב_2 == 0x00 {
		return
	}

	for ((מצב_2 & 0x80) == 0x80) && ((מצב_2 & 0x01) != 0x01) {
		מצב_2 = self.פקודהשער.Rקריאה()
	}
	if (מצב_2 & 0x01) != 0 {
		console_2.Mהדפסה(([]byte)(" ata flush error"))
		return
	}

}
