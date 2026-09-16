/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "bağlantıNoktası"
import . "konsol"

const Baytpersector int = 512

type TGelişmişTeknolojiattachment struct {
	ana				bool
	dataBağlantıNoktası		TBağlantıNoktası16bit
	hataBağlantıNoktası		TBağlantıNoktası8bit
	sectorcountBağlantıNoktası	TBağlantıNoktası8bit
	lbaDüşükBağlantıNoktası		TBağlantıNoktası8bit
	lbamidBağlantıNoktası		TBağlantıNoktası8bit
	lbahiBağlantıNoktası		TBağlantıNoktası8bit
	aygıtBağlantıNoktası		TBağlantıNoktası8bit
	komutBağlantıNoktası		TBağlantıNoktası8bit
	ctrlBağlantıNoktası		TBağlantıNoktası8bit
}

func (self *TGelişmişTeknolojiattachment) Init(ana bool, bağlantıNoktasıbase uint16) {
	self.ana = ana
	self.dataBağlantıNoktası.Init(bağlantıNoktasıbase)
	self.hataBağlantıNoktası.Init(bağlantıNoktasıbase + 0x1)
	self.sectorcountBağlantıNoktası.Init(bağlantıNoktasıbase + 0x2)
	self.lbaDüşükBağlantıNoktası.Init(bağlantıNoktasıbase + 0x3)
	self.lbamidBağlantıNoktası.Init(bağlantıNoktasıbase + 0x4)
	self.lbahiBağlantıNoktası.Init(bağlantıNoktasıbase + 0x5)
	self.aygıtBağlantıNoktası.Init(bağlantıNoktasıbase + 0x6)
	self.komutBağlantıNoktası.Init(bağlantıNoktasıbase + 0x7)
	self.ctrlBağlantıNoktası.Init(bağlantıNoktasıbase + 0x8)

}

func (self *TGelişmişTeknolojiattachment) Identify() {

	var konsol_2 = TKonsol{}

	if self.ana {
		self.aygıtBağlantıNoktası.Yazma(0xA0)
	} else {
		self.aygıtBağlantıNoktası.Yazma(0xB0)
	}
	self.ctrlBağlantıNoktası.Yazma(0)
	self.aygıtBağlantıNoktası.Yazma(0xA0)

	var durum uint8 = self.komutBağlantıNoktası.Okuma()
	if durum == 0xFF {
		konsol_2.MYazdır(([]byte)("Invalid Status"))
		return
	}

	if self.ana {
		self.aygıtBağlantıNoktası.Yazma(0xA0)
	} else {
		self.aygıtBağlantıNoktası.Yazma(0xB0)
	}
	self.sectorcountBağlantıNoktası.Yazma(0)
	self.lbaDüşükBağlantıNoktası.Yazma(0)
	self.lbamidBağlantıNoktası.Yazma(0)
	self.lbahiBağlantıNoktası.Yazma(0)
	self.komutBağlantıNoktası.Yazma(0xEC)

	durum = self.komutBağlantıNoktası.Okuma()
	if durum == 0x00 {
		konsol_2.MYazdır(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (durum&0x80) == 0x80 && (durum&0x01) != 0x01 {
		durum = self.komutBağlantıNoktası.Okuma()
	}

	if (durum & 0x01) != 0 {
		konsol_2.MYazdır(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataBağlantıNoktası.Okuma()
		metin := []byte("  ")
		metin[0] = uint8((data >> 8) & 0xFF)
		metin[1] = uint8(data & 0xFF)

	}
	konsol_2.MYazdırxy(([]byte)("ata ok"), 10, 22)

}
func (self *TGelişmişTeknolojiattachment) Okuma28(sector uint32, data *[]byte, count int) {
	var konsol_2 = TKonsol{}
	if (sector & 0xF0000000) != 0 {
		konsol_2.MYazdır(([]byte)("ata read error "))
		return
	}
	if count > Baytpersector {
		konsol_2.MYazdır(([]byte)("ata read error "))
		return
	}

	if self.ana {
		self.aygıtBağlantıNoktası.Yazma(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.aygıtBağlantıNoktası.Yazma(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.hataBağlantıNoktası.Yazma(0)
	self.sectorcountBağlantıNoktası.Yazma(1)

	self.lbaDüşükBağlantıNoktası.Yazma(uint8(sector & 0x000000FF))
	self.lbamidBağlantıNoktası.Yazma(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiBağlantıNoktası.Yazma(uint8((sector & 0x00FF0000) >> 16))
	self.komutBağlantıNoktası.Yazma(0x20)

	var durum uint8 = self.komutBağlantıNoktası.Okuma()
	for ((durum & 0x80) == 0x80) && ((durum & 0x01) != 0x01) {
		durum = self.komutBağlantıNoktası.Okuma()
	}

	if (durum & 0x01) != 0 {
		konsol_2.MYazdır(([]byte)("ata read error "))
		return
	}

	konsol_2.MYazdırxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataBağlantıNoktası.Okuma()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Baytpersector; i += 2 {
		self.dataBağlantıNoktası.Okuma()
	}
}
func (self *TGelişmişTeknolojiattachment) Yazma28(sectorSayı uint32, data []byte, count uint32) {

	if sectorSayı > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.ana {
		self.aygıtBağlantıNoktası.Yazma(uint8(0xE0 | uint8((sectorSayı&0x0F000000)>>24)))
	} else {
		self.aygıtBağlantıNoktası.Yazma(uint8(0xF0 | uint8((sectorSayı&0x0F000000)>>24)))
	}

	self.hataBağlantıNoktası.Yazma(0)
	self.sectorcountBağlantıNoktası.Yazma(1)
	self.lbaDüşükBağlantıNoktası.Yazma(uint8(sectorSayı & 0x000000FF))
	self.lbamidBağlantıNoktası.Yazma(uint8((sectorSayı & 0x0000FF00) >> 8))
	self.lbahiBağlantıNoktası.Yazma(uint8((sectorSayı & 0x00FF0000) >> 16))
	self.komutBağlantıNoktası.Yazma(0x30)

	var konsol_2 = TKonsol{}
	konsol_2.MYazdır(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataBağlantıNoktası.Yazma(wdata)

		metin := []byte("  ")
		metin[0] = uint8((wdata >> 8) & 0xFF)
		metin[1] = uint8(wdata & 0xFF)

		konsol_2.MYazdır(metin)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataBağlantıNoktası.Yazma(0x0000)
	}

}

func (self *TGelişmişTeknolojiattachment) Flush() {
	if self.ana {
		self.aygıtBağlantıNoktası.Yazma(0xE0)
	} else {
		self.aygıtBağlantıNoktası.Yazma(0xF0)
	}
	self.komutBağlantıNoktası.Yazma(0xE7)

	var konsol_2 = TKonsol{}

	var durum uint8 = self.komutBağlantıNoktası.Okuma()
	if durum == 0x00 {
		return
	}

	for ((durum & 0x80) == 0x80) && ((durum & 0x01) != 0x01) {
		durum = self.komutBağlantıNoktası.Okuma()
	}
	if (durum & 0x01) != 0 {
		konsol_2.MYazdır(([]byte)(" ata flush error"))
		return
	}

}
