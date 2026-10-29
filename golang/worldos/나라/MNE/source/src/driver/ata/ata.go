/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "порт"
import . "конзола"

const Bajtovapersector int = 512

type TНапредноТехнологијаattachment struct {
	glavni		bool
	dataПорт	TПорт16bit
	грешкаПорт	TПорт8bit
	sectorcountПорт	TПорт8bit
	lbaTihoПорт	TПорт8bit
	lbamidПорт	TПорт8bit
	lbahiПорт	TПорт8bit
	уређајПорт	TПорт8bit
	наредбаПорт	TПорт8bit
	контролПорт	TПорт8bit
}

func (isti *TНапредноТехнологијаattachment) Init(glavni bool, портbase uint16) {
	isti.glavni = glavni
	isti.dataПорт.Init(портbase)
	isti.грешкаПорт.Init(портbase + 0x1)
	isti.sectorcountПорт.Init(портbase + 0x2)
	isti.lbaTihoПорт.Init(портbase + 0x3)
	isti.lbamidПорт.Init(портbase + 0x4)
	isti.lbahiПорт.Init(портbase + 0x5)
	isti.уређајПорт.Init(портbase + 0x6)
	isti.наредбаПорт.Init(портbase + 0x7)
	isti.контролПорт.Init(портbase + 0x8)

}

func (isti *TНапредноТехнологијаattachment) Identify() {

	var конзола_2 = TКонзола{}

	if isti.glavni {
		isti.уређајПорт.Upis(0xA0)
	} else {
		isti.уређајПорт.Upis(0xB0)
	}
	isti.контролПорт.Upis(0)
	isti.уређајПорт.Upis(0xA0)

	var стање uint8 = isti.наредбаПорт.Читање()
	if стање == 0xFF {
		конзола_2.MŠtampaj(([]byte)("Invalid Status"))
		return
	}

	if isti.glavni {
		isti.уређајПорт.Upis(0xA0)
	} else {
		isti.уређајПорт.Upis(0xB0)
	}
	isti.sectorcountПорт.Upis(0)
	isti.lbaTihoПорт.Upis(0)
	isti.lbamidПорт.Upis(0)
	isti.lbahiПорт.Upis(0)
	isti.наредбаПорт.Upis(0xEC)

	стање = isti.наредбаПорт.Читање()
	if стање == 0x00 {
		конзола_2.MŠtampaj(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (стање&0x80) == 0x80 && (стање&0x01) != 0x01 {
		стање = isti.наредбаПорт.Читање()
	}

	if (стање & 0x01) != 0 {
		конзола_2.MŠtampaj(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = isti.dataПорт.Читање()
		текст := []byte("  ")
		текст[0] = uint8((data >> 8) & 0xFF)
		текст[1] = uint8(data & 0xFF)

	}
	конзола_2.MŠtampajxy(([]byte)("ata ok"), 10, 22)

}
func (isti *TНапредноТехнологијаattachment) Читање28(sector uint32, data *[]byte, count int) {
	var конзола_2 = TКонзола{}
	if (sector & 0xF0000000) != 0 {
		конзола_2.MŠtampaj(([]byte)("ata read error "))
		return
	}
	if count > Bajtovapersector {
		конзола_2.MŠtampaj(([]byte)("ata read error "))
		return
	}

	if isti.glavni {
		isti.уређајПорт.Upis(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		isti.уређајПорт.Upis(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	isti.грешкаПорт.Upis(0)
	isti.sectorcountПорт.Upis(1)

	isti.lbaTihoПорт.Upis(uint8(sector & 0x000000FF))
	isti.lbamidПорт.Upis(uint8((sector & 0x0000FF00) >> 8))
	isti.lbahiПорт.Upis(uint8((sector & 0x00FF0000) >> 16))
	isti.наредбаПорт.Upis(0x20)

	var стање uint8 = isti.наредбаПорт.Читање()
	for ((стање & 0x80) == 0x80) && ((стање & 0x01) != 0x01) {
		стање = isti.наредбаПорт.Читање()
	}

	if (стање & 0x01) != 0 {
		конзола_2.MŠtampaj(([]byte)("ata read error "))
		return
	}

	конзола_2.MŠtampajxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = isti.dataПорт.Читање()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Bajtovapersector; i += 2 {
		isti.dataПорт.Читање()
	}
}
func (isti *TНапредноТехнологијаattachment) Upis28(sectorброј uint32, data []byte, count uint32) {

	if sectorброј > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if isti.glavni {
		isti.уређајПорт.Upis(uint8(0xE0 | uint8((sectorброј&0x0F000000)>>24)))
	} else {
		isti.уређајПорт.Upis(uint8(0xF0 | uint8((sectorброј&0x0F000000)>>24)))
	}

	isti.грешкаПорт.Upis(0)
	isti.sectorcountПорт.Upis(1)
	isti.lbaTihoПорт.Upis(uint8(sectorброј & 0x000000FF))
	isti.lbamidПорт.Upis(uint8((sectorброј & 0x0000FF00) >> 8))
	isti.lbahiПорт.Upis(uint8((sectorброј & 0x00FF0000) >> 16))
	isti.наредбаПорт.Upis(0x30)

	var конзола_2 = TКонзола{}
	конзола_2.MŠtampaj(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		isti.dataПорт.Upis(wdata)

		текст := []byte("  ")
		текст[0] = uint8((wdata >> 8) & 0xFF)
		текст[1] = uint8(wdata & 0xFF)

		конзола_2.MŠtampaj(текст)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		isti.dataПорт.Upis(0x0000)
	}

}

func (isti *TНапредноТехнологијаattachment) Flush() {
	if isti.glavni {
		isti.уређајПорт.Upis(0xE0)
	} else {
		isti.уређајПорт.Upis(0xF0)
	}
	isti.наредбаПорт.Upis(0xE7)

	var конзола_2 = TКонзола{}

	var стање uint8 = isti.наредбаПорт.Читање()
	if стање == 0x00 {
		return
	}

	for ((стање & 0x80) == 0x80) && ((стање & 0x01) != 0x01) {
		стање = isti.наредбаПорт.Читање()
	}
	if (стање & 0x01) != 0 {
		конзола_2.MŠtampaj(([]byte)(" ata flush error"))
		return
	}

}
