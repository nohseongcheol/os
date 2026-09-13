package ata

import . "порт"
import . "консол"

const Байтpersector int = 512

type TӨргөтгөсөнtechnologyattachment struct {
	master		bool
	dataПорт	TПорт16bit
	алдааПорт	TПорт8bit
	sectorcountПорт	TПорт8bit
	lbaБагаПорт	TПорт8bit
	lbamidПорт	TПорт8bit
	lbahiПорт	TПорт8bit
	төхөөрөмжПорт	TПорт8bit
	тушаалПорт	TПорт8bit
	controlПорт	TПорт8bit
}

func (self *TӨргөтгөсөнtechnologyattachment) Init(master bool, портbase uint16) {
	self.master = master
	self.dataПорт.Init(портbase)
	self.алдааПорт.Init(портbase + 0x1)
	self.sectorcountПорт.Init(портbase + 0x2)
	self.lbaБагаПорт.Init(портbase + 0x3)
	self.lbamidПорт.Init(портbase + 0x4)
	self.lbahiПорт.Init(портbase + 0x5)
	self.төхөөрөмжПорт.Init(портbase + 0x6)
	self.тушаалПорт.Init(портbase + 0x7)
	self.controlПорт.Init(портbase + 0x8)

}

func (self *TӨргөтгөсөнtechnologyattachment) Identify() {

	var консол_2 = TКонсол{}

	if self.master {
		self.төхөөрөмжПорт.Бичих(0xA0)
	} else {
		self.төхөөрөмжПорт.Бичих(0xB0)
	}
	self.controlПорт.Бичих(0)
	self.төхөөрөмжПорт.Бичих(0xA0)

	var төлөв uint8 = self.тушаалПорт.Унших()
	if төлөв == 0xFF {
		консол_2.MХэвлэх(([]byte)("Invalid Status"))
		return
	}

	if self.master {
		self.төхөөрөмжПорт.Бичих(0xA0)
	} else {
		self.төхөөрөмжПорт.Бичих(0xB0)
	}
	self.sectorcountПорт.Бичих(0)
	self.lbaБагаПорт.Бичих(0)
	self.lbamidПорт.Бичих(0)
	self.lbahiПорт.Бичих(0)
	self.тушаалПорт.Бичих(0xEC)

	төлөв = self.тушаалПорт.Унших()
	if төлөв == 0x00 {
		консол_2.MХэвлэх(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (төлөв&0x80) == 0x80 && (төлөв&0x01) != 0x01 {
		төлөв = self.тушаалПорт.Унших()
	}

	if (төлөв & 0x01) != 0 {
		консол_2.MХэвлэх(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataПорт.Унших()
		текст := []byte("  ")
		текст[0] = uint8((data >> 8) & 0xFF)
		текст[1] = uint8(data & 0xFF)

	}
	консол_2.MХэвлэхxy(([]byte)("ata ok"), 10, 22)

}
func (self *TӨргөтгөсөнtechnologyattachment) Унших28(sector uint32, data *[]byte, count int) {
	var консол_2 = TКонсол{}
	if (sector & 0xF0000000) != 0 {
		консол_2.MХэвлэх(([]byte)("ata read error "))
		return
	}
	if count > Байтpersector {
		консол_2.MХэвлэх(([]byte)("ata read error "))
		return
	}

	if self.master {
		self.төхөөрөмжПорт.Бичих(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.төхөөрөмжПорт.Бичих(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.алдааПорт.Бичих(0)
	self.sectorcountПорт.Бичих(1)

	self.lbaБагаПорт.Бичих(uint8(sector & 0x000000FF))
	self.lbamidПорт.Бичих(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiПорт.Бичих(uint8((sector & 0x00FF0000) >> 16))
	self.тушаалПорт.Бичих(0x20)

	var төлөв uint8 = self.тушаалПорт.Унших()
	for ((төлөв & 0x80) == 0x80) && ((төлөв & 0x01) != 0x01) {
		төлөв = self.тушаалПорт.Унших()
	}

	if (төлөв & 0x01) != 0 {
		консол_2.MХэвлэх(([]byte)("ata read error "))
		return
	}

	консол_2.MХэвлэхxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataПорт.Унших()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Байтpersector; i += 2 {
		self.dataПорт.Унших()
	}
}
func (self *TӨргөтгөсөнtechnologyattachment) Бичих28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.master {
		self.төхөөрөмжПорт.Бичих(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.төхөөрөмжПорт.Бичих(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.алдааПорт.Бичих(0)
	self.sectorcountПорт.Бичих(1)
	self.lbaБагаПорт.Бичих(uint8(sectornumber & 0x000000FF))
	self.lbamidПорт.Бичих(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiПорт.Бичих(uint8((sectornumber & 0x00FF0000) >> 16))
	self.тушаалПорт.Бичих(0x30)

	var консол_2 = TКонсол{}
	консол_2.MХэвлэх(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataПорт.Бичих(wdata)

		текст := []byte("  ")
		текст[0] = uint8((wdata >> 8) & 0xFF)
		текст[1] = uint8(wdata & 0xFF)

		консол_2.MХэвлэх(текст)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataПорт.Бичих(0x0000)
	}

}

func (self *TӨргөтгөсөнtechnologyattachment) Flush() {
	if self.master {
		self.төхөөрөмжПорт.Бичих(0xE0)
	} else {
		self.төхөөрөмжПорт.Бичих(0xF0)
	}
	self.тушаалПорт.Бичих(0xE7)

	var консол_2 = TКонсол{}

	var төлөв uint8 = self.тушаалПорт.Унших()
	if төлөв == 0x00 {
		return
	}

	for ((төлөв & 0x80) == 0x80) && ((төлөв & 0x01) != 0x01) {
		төлөв = self.тушаалПорт.Унших()
	}
	if (төлөв & 0x01) != 0 {
		консол_2.MХэвлэх(([]byte)(" ata flush error"))
		return
	}

}
