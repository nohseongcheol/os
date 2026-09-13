package ata

import . "ぽーと"
import . "こんそーる"

const Bばいとpersector int = 512

type Tしょうさいしようぎじゅつattachment struct {
	ますたー		bool
	でーたぽーと		Tぽーと16bit
	えらーぽーと		Tぽーと8bit
	sectorかうんとぽーと	Tぽーと8bit
	lbaひくいぽーと	Tぽーと8bit
	lbamidぽーと	Tぽーと8bit
	lbahiぽーと	Tぽーと8bit
	でばいすぽーと		Tぽーと8bit
	こまんどぽーと		Tぽーと8bit
	せいぎょぽーと		Tぽーと8bit
}

func (self *Tしょうさいしようぎじゅつattachment) Init(ますたー bool, ぽーとbase uint16) {
	self.ますたー = ますたー
	self.でーたぽーと.Init(ぽーとbase)
	self.えらーぽーと.Init(ぽーとbase + 0x1)
	self.sectorかうんとぽーと.Init(ぽーとbase + 0x2)
	self.lbaひくいぽーと.Init(ぽーとbase + 0x3)
	self.lbamidぽーと.Init(ぽーとbase + 0x4)
	self.lbahiぽーと.Init(ぽーとbase + 0x5)
	self.でばいすぽーと.Init(ぽーとbase + 0x6)
	self.こまんどぽーと.Init(ぽーとbase + 0x7)
	self.せいぎょぽーと.Init(ぽーとbase + 0x8)

}

func (self *Tしょうさいしようぎじゅつattachment) Identify() {

	var こんそーる_2 = Tこんそーる{}

	if self.ますたー {
		self.でばいすぽーと.Wかきこみ(0xA0)
	} else {
		self.でばいすぽーと.Wかきこみ(0xB0)
	}
	self.せいぎょぽーと.Wかきこみ(0)
	self.でばいすぽーと.Wかきこみ(0xA0)

	var じょうたい uint8 = self.こまんどぽーと.Rよみこみ()
	if じょうたい == 0xFF {
		こんそーる_2.Mいんさつ(([]byte)("Invalid Status"))
		return
	}

	if self.ますたー {
		self.でばいすぽーと.Wかきこみ(0xA0)
	} else {
		self.でばいすぽーと.Wかきこみ(0xB0)
	}
	self.sectorかうんとぽーと.Wかきこみ(0)
	self.lbaひくいぽーと.Wかきこみ(0)
	self.lbamidぽーと.Wかきこみ(0)
	self.lbahiぽーと.Wかきこみ(0)
	self.こまんどぽーと.Wかきこみ(0xEC)

	じょうたい = self.こまんどぽーと.Rよみこみ()
	if じょうたい == 0x00 {
		こんそーる_2.Mいんさつ(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (じょうたい&0x80) == 0x80 && (じょうたい&0x01) != 0x01 {
		じょうたい = self.こまんどぽーと.Rよみこみ()
	}

	if (じょうたい & 0x01) != 0 {
		こんそーる_2.Mいんさつ(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var でーた = self.でーたぽーと.Rよみこみ()
		てきすと := []byte("  ")
		てきすと[0] = uint8((でーた >> 8) & 0xFF)
		てきすと[1] = uint8(でーた & 0xFF)

	}
	こんそーる_2.Mいんさつxy(([]byte)("ata ok"), 10, 22)

}
func (self *Tしょうさいしようぎじゅつattachment) Rよみこみ28(sector uint32, でーた *[]byte, かうんと int) {
	var こんそーる_2 = Tこんそーる{}
	if (sector & 0xF0000000) != 0 {
		こんそーる_2.Mいんさつ(([]byte)("ata read error "))
		return
	}
	if かうんと > Bばいとpersector {
		こんそーる_2.Mいんさつ(([]byte)("ata read error "))
		return
	}

	if self.ますたー {
		self.でばいすぽーと.Wかきこみ(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.でばいすぽーと.Wかきこみ(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.えらーぽーと.Wかきこみ(0)
	self.sectorかうんとぽーと.Wかきこみ(1)

	self.lbaひくいぽーと.Wかきこみ(uint8(sector & 0x000000FF))
	self.lbamidぽーと.Wかきこみ(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiぽーと.Wかきこみ(uint8((sector & 0x00FF0000) >> 16))
	self.こまんどぽーと.Wかきこみ(0x20)

	var じょうたい uint8 = self.こまんどぽーと.Rよみこみ()
	for ((じょうたい & 0x80) == 0x80) && ((じょうたい & 0x01) != 0x01) {
		じょうたい = self.こまんどぽーと.Rよみこみ()
	}

	if (じょうたい & 0x01) != 0 {
		こんそーる_2.Mいんさつ(([]byte)("ata read error "))
		return
	}

	こんそーる_2.Mいんさつxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < かうんと; i += 2 {
		var wdata uint16 = self.でーたぽーと.Rよみこみ()

		(*でーた)[i] = uint8(wdata & 0x00FF)
		if i+1 < かうんと {

			(*でーた)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (かうんと + (かうんと % 2)); i < Bばいとpersector; i += 2 {
		self.でーたぽーと.Rよみこみ()
	}
}
func (self *Tしょうさいしようぎじゅつattachment) Wかきこみ28(sectornumber uint32, でーた []byte, かうんと uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if かうんと > 512 {
		return
	}

	if self.ますたー {
		self.でばいすぽーと.Wかきこみ(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.でばいすぽーと.Wかきこみ(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.えらーぽーと.Wかきこみ(0)
	self.sectorかうんとぽーと.Wかきこみ(1)
	self.lbaひくいぽーと.Wかきこみ(uint8(sectornumber & 0x000000FF))
	self.lbamidぽーと.Wかきこみ(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiぽーと.Wかきこみ(uint8((sectornumber & 0x00FF0000) >> 16))
	self.こまんどぽーと.Wかきこみ(0x30)

	var こんそーる_2 = Tこんそーる{}
	こんそーる_2.Mいんさつ(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < かうんと; i += 2 {

		var wdata uint16 = uint16(でーた[i])

		if i+1 < かうんと {
			wdata = wdata | (uint16(でーた[i+1]) << 8)
		}

		self.でーたぽーと.Wかきこみ(wdata)

		てきすと := []byte("  ")
		てきすと[0] = uint8((wdata >> 8) & 0xFF)
		てきすと[1] = uint8(wdata & 0xFF)

		こんそーる_2.Mいんさつ(てきすと)
	}

	for i := (かうんと + (かうんと % 2)); i < 512; i += 2 {
		self.でーたぽーと.Wかきこみ(0x0000)
	}

}

func (self *Tしょうさいしようぎじゅつattachment) Flush() {
	if self.ますたー {
		self.でばいすぽーと.Wかきこみ(0xE0)
	} else {
		self.でばいすぽーと.Wかきこみ(0xF0)
	}
	self.こまんどぽーと.Wかきこみ(0xE7)

	var こんそーる_2 = Tこんそーる{}

	var じょうたい uint8 = self.こまんどぽーと.Rよみこみ()
	if じょうたい == 0x00 {
		return
	}

	for ((じょうたい & 0x80) == 0x80) && ((じょうたい & 0x01) != 0x01) {
		じょうたい = self.こまんどぽーと.Rよみこみ()
	}
	if (じょうたい & 0x01) != 0 {
		こんそーる_2.Mいんさつ(([]byte)(" ata flush error"))
		return
	}

}
