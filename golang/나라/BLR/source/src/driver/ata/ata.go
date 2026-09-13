package ata

import . "порт"
import . "console"

const Байтаўpersector int = 512

type TДадатковаТэхналогіяattachment struct {
	агульны		bool
	dataПорт	TПорт16bit
	памылкаПорт	TПорт8bit
	sectorcountПорт	TПорт8bit
	lbaНізкіПорт	TПорт8bit
	lbamidПорт	TПорт8bit
	lbahiПорт	TПорт8bit
	прыладаПорт	TПорт8bit
	загадПорт	TПорт8bit
	ctrlПорт	TПорт8bit
}

func (self *TДадатковаТэхналогіяattachment) Init(агульны bool, портbase uint16) {
	self.агульны = агульны
	self.dataПорт.Init(портbase)
	self.памылкаПорт.Init(портbase + 0x1)
	self.sectorcountПорт.Init(портbase + 0x2)
	self.lbaНізкіПорт.Init(портbase + 0x3)
	self.lbamidПорт.Init(портbase + 0x4)
	self.lbahiПорт.Init(портbase + 0x5)
	self.прыладаПорт.Init(портbase + 0x6)
	self.загадПорт.Init(портbase + 0x7)
	self.ctrlПорт.Init(портbase + 0x8)

}

func (self *TДадатковаТэхналогіяattachment) Identify() {

	var console_2 = TConsole{}

	if self.агульны {
		self.прыладаПорт.Запіс(0xA0)
	} else {
		self.прыладаПорт.Запіс(0xB0)
	}
	self.ctrlПорт.Запіс(0)
	self.прыладаПорт.Запіс(0xA0)

	var стан uint8 = self.загадПорт.Чытанне()
	if стан == 0xFF {
		console_2.MДрукаваць(([]byte)("Invalid Status"))
		return
	}

	if self.агульны {
		self.прыладаПорт.Запіс(0xA0)
	} else {
		self.прыладаПорт.Запіс(0xB0)
	}
	self.sectorcountПорт.Запіс(0)
	self.lbaНізкіПорт.Запіс(0)
	self.lbamidПорт.Запіс(0)
	self.lbahiПорт.Запіс(0)
	self.загадПорт.Запіс(0xEC)

	стан = self.загадПорт.Чытанне()
	if стан == 0x00 {
		console_2.MДрукаваць(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (стан&0x80) == 0x80 && (стан&0x01) != 0x01 {
		стан = self.загадПорт.Чытанне()
	}

	if (стан & 0x01) != 0 {
		console_2.MДрукаваць(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = self.dataПорт.Чытанне()
		тэкст := []byte("  ")
		тэкст[0] = uint8((data >> 8) & 0xFF)
		тэкст[1] = uint8(data & 0xFF)

	}
	console_2.MДрукавацьxy(([]byte)("ata ok"), 10, 22)

}
func (self *TДадатковаТэхналогіяattachment) Чытанне28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MДрукаваць(([]byte)("ata read error "))
		return
	}
	if count > Байтаўpersector {
		console_2.MДрукаваць(([]byte)("ata read error "))
		return
	}

	if self.агульны {
		self.прыладаПорт.Запіс(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.прыладаПорт.Запіс(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.памылкаПорт.Запіс(0)
	self.sectorcountПорт.Запіс(1)

	self.lbaНізкіПорт.Запіс(uint8(sector & 0x000000FF))
	self.lbamidПорт.Запіс(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiПорт.Запіс(uint8((sector & 0x00FF0000) >> 16))
	self.загадПорт.Запіс(0x20)

	var стан uint8 = self.загадПорт.Чытанне()
	for ((стан & 0x80) == 0x80) && ((стан & 0x01) != 0x01) {
		стан = self.загадПорт.Чытанне()
	}

	if (стан & 0x01) != 0 {
		console_2.MДрукаваць(([]byte)("ata read error "))
		return
	}

	console_2.MДрукавацьxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = self.dataПорт.Чытанне()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Байтаўpersector; i += 2 {
		self.dataПорт.Чытанне()
	}
}
func (self *TДадатковаТэхналогіяattachment) Запіс28(sectorНУМАР uint32, data []byte, count uint32) {

	if sectorНУМАР > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if self.агульны {
		self.прыладаПорт.Запіс(uint8(0xE0 | uint8((sectorНУМАР&0x0F000000)>>24)))
	} else {
		self.прыладаПорт.Запіс(uint8(0xF0 | uint8((sectorНУМАР&0x0F000000)>>24)))
	}

	self.памылкаПорт.Запіс(0)
	self.sectorcountПорт.Запіс(1)
	self.lbaНізкіПорт.Запіс(uint8(sectorНУМАР & 0x000000FF))
	self.lbamidПорт.Запіс(uint8((sectorНУМАР & 0x0000FF00) >> 8))
	self.lbahiПорт.Запіс(uint8((sectorНУМАР & 0x00FF0000) >> 16))
	self.загадПорт.Запіс(0x30)

	var console_2 = TConsole{}
	console_2.MДрукаваць(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		self.dataПорт.Запіс(wdata)

		тэкст := []byte("  ")
		тэкст[0] = uint8((wdata >> 8) & 0xFF)
		тэкст[1] = uint8(wdata & 0xFF)

		console_2.MДрукаваць(тэкст)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		self.dataПорт.Запіс(0x0000)
	}

}

func (self *TДадатковаТэхналогіяattachment) Flush() {
	if self.агульны {
		self.прыладаПорт.Запіс(0xE0)
	} else {
		self.прыладаПорт.Запіс(0xF0)
	}
	self.загадПорт.Запіс(0xE7)

	var console_2 = TConsole{}

	var стан uint8 = self.загадПорт.Чытанне()
	if стан == 0x00 {
		return
	}

	for ((стан & 0x80) == 0x80) && ((стан & 0x01) != 0x01) {
		стан = self.загадПорт.Чытанне()
	}
	if (стан & 0x01) != 0 {
		console_2.MДрукаваць(([]byte)(" ata flush error"))
		return
	}

}
