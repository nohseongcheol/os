/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "порт"
import . "конзола"

const Бајтоваpersector int = 512

type TНапредноТехнологијаattachment struct {
	главни		bool
	dataПорт	TПорт16bit
	грешкаПорт	TПорт8bit
	sectorcountПорт	TПорт8bit
	lbaТихоПорт	TПорт8bit
	lbamidПорт	TПорт8bit
	lbahiПорт	TПорт8bit
	уређајПорт	TПорт8bit
	наредбаПорт	TПорт8bit
	контролПорт	TПорт8bit
}

func (исти *TНапредноТехнологијаattachment) Init(главни bool, портbase uint16) {
	исти.главни = главни
	исти.dataПорт.Init(портbase)
	исти.грешкаПорт.Init(портbase + 0x1)
	исти.sectorcountПорт.Init(портbase + 0x2)
	исти.lbaТихоПорт.Init(портbase + 0x3)
	исти.lbamidПорт.Init(портbase + 0x4)
	исти.lbahiПорт.Init(портbase + 0x5)
	исти.уређајПорт.Init(портbase + 0x6)
	исти.наредбаПорт.Init(портbase + 0x7)
	исти.контролПорт.Init(портbase + 0x8)

}

func (исти *TНапредноТехнологијаattachment) Identify() {

	var конзола_2 = TКонзола{}

	if исти.главни {
		исти.уређајПорт.Пише(0xA0)
	} else {
		исти.уређајПорт.Пише(0xB0)
	}
	исти.контролПорт.Пише(0)
	исти.уређајПорт.Пише(0xA0)

	var стање uint8 = исти.наредбаПорт.Читање()
	if стање == 0xFF {
		конзола_2.MШтампај(([]byte)("Invalid Status"))
		return
	}

	if исти.главни {
		исти.уређајПорт.Пише(0xA0)
	} else {
		исти.уређајПорт.Пише(0xB0)
	}
	исти.sectorcountПорт.Пише(0)
	исти.lbaТихоПорт.Пише(0)
	исти.lbamidПорт.Пише(0)
	исти.lbahiПорт.Пише(0)
	исти.наредбаПорт.Пише(0xEC)

	стање = исти.наредбаПорт.Читање()
	if стање == 0x00 {
		конзола_2.MШтампај(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (стање&0x80) == 0x80 && (стање&0x01) != 0x01 {
		стање = исти.наредбаПорт.Читање()
	}

	if (стање & 0x01) != 0 {
		конзола_2.MШтампај(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = исти.dataПорт.Читање()
		текст := []byte("  ")
		текст[0] = uint8((data >> 8) & 0xFF)
		текст[1] = uint8(data & 0xFF)

	}
	конзола_2.MШтампајxy(([]byte)("ata ok"), 10, 22)

}
func (исти *TНапредноТехнологијаattachment) Читање28(sector uint32, data *[]byte, count int) {
	var конзола_2 = TКонзола{}
	if (sector & 0xF0000000) != 0 {
		конзола_2.MШтампај(([]byte)("ata read error "))
		return
	}
	if count > Бајтоваpersector {
		конзола_2.MШтампај(([]byte)("ata read error "))
		return
	}

	if исти.главни {
		исти.уређајПорт.Пише(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		исти.уређајПорт.Пише(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	исти.грешкаПорт.Пише(0)
	исти.sectorcountПорт.Пише(1)

	исти.lbaТихоПорт.Пише(uint8(sector & 0x000000FF))
	исти.lbamidПорт.Пише(uint8((sector & 0x0000FF00) >> 8))
	исти.lbahiПорт.Пише(uint8((sector & 0x00FF0000) >> 16))
	исти.наредбаПорт.Пише(0x20)

	var стање uint8 = исти.наредбаПорт.Читање()
	for ((стање & 0x80) == 0x80) && ((стање & 0x01) != 0x01) {
		стање = исти.наредбаПорт.Читање()
	}

	if (стање & 0x01) != 0 {
		конзола_2.MШтампај(([]byte)("ata read error "))
		return
	}

	конзола_2.MШтампајxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = исти.dataПорт.Читање()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Бајтоваpersector; i += 2 {
		исти.dataПорт.Читање()
	}
}
func (исти *TНапредноТехнологијаattachment) Пише28(sectorброј uint32, data []byte, count uint32) {

	if sectorброј > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if исти.главни {
		исти.уређајПорт.Пише(uint8(0xE0 | uint8((sectorброј&0x0F000000)>>24)))
	} else {
		исти.уређајПорт.Пише(uint8(0xF0 | uint8((sectorброј&0x0F000000)>>24)))
	}

	исти.грешкаПорт.Пише(0)
	исти.sectorcountПорт.Пише(1)
	исти.lbaТихоПорт.Пише(uint8(sectorброј & 0x000000FF))
	исти.lbamidПорт.Пише(uint8((sectorброј & 0x0000FF00) >> 8))
	исти.lbahiПорт.Пише(uint8((sectorброј & 0x00FF0000) >> 16))
	исти.наредбаПорт.Пише(0x30)

	var конзола_2 = TКонзола{}
	конзола_2.MШтампај(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		исти.dataПорт.Пише(wdata)

		текст := []byte("  ")
		текст[0] = uint8((wdata >> 8) & 0xFF)
		текст[1] = uint8(wdata & 0xFF)

		конзола_2.MШтампај(текст)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		исти.dataПорт.Пише(0x0000)
	}

}

func (исти *TНапредноТехнологијаattachment) Flush() {
	if исти.главни {
		исти.уређајПорт.Пише(0xE0)
	} else {
		исти.уређајПорт.Пише(0xF0)
	}
	исти.наредбаПорт.Пише(0xE7)

	var конзола_2 = TКонзола{}

	var стање uint8 = исти.наредбаПорт.Читање()
	if стање == 0x00 {
		return
	}

	for ((стање & 0x80) == 0x80) && ((стање & 0x01) != 0x01) {
		стање = исти.наредбаПорт.Читање()
	}
	if (стање & 0x01) != 0 {
		конзола_2.MШтампај(([]byte)(" ata flush error"))
		return
	}

}
