/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "порта"
import . "console"

const Бајтиpersector int = 512

type TНапредноtechnologyattachment struct {
	master			bool
	dataПорта		TПорта16bit
	грешкаПорта		TПорта8bit
	sectorcountПорта	TПорта8bit
	lbalowПорта		TПорта8bit
	lbamidПорта		TПорта8bit
	lbahiПорта		TПорта8bit
	уредПорта		TПорта8bit
	командаПорта		TПорта8bit
	controlПорта		TПорта8bit
}

func (само *TНапредноtechnologyattachment) Init(master bool, портаbase uint16) {
	само.master = master
	само.dataПорта.Init(портаbase)
	само.грешкаПорта.Init(портаbase + 0x1)
	само.sectorcountПорта.Init(портаbase + 0x2)
	само.lbalowПорта.Init(портаbase + 0x3)
	само.lbamidПорта.Init(портаbase + 0x4)
	само.lbahiПорта.Init(портаbase + 0x5)
	само.уредПорта.Init(портаbase + 0x6)
	само.командаПорта.Init(портаbase + 0x7)
	само.controlПорта.Init(портаbase + 0x8)

}

func (само *TНапредноtechnologyattachment) Identify() {

	var console_2 = TConsole{}

	if само.master {
		само.уредПорта.Запиши(0xA0)
	} else {
		само.уредПорта.Запиши(0xB0)
	}
	само.controlПорта.Запиши(0)
	само.уредПорта.Запиши(0xA0)

	var статус uint8 = само.командаПорта.Читај()
	if статус == 0xFF {
		console_2.MПечати(([]byte)("Invalid Status"))
		return
	}

	if само.master {
		само.уредПорта.Запиши(0xA0)
	} else {
		само.уредПорта.Запиши(0xB0)
	}
	само.sectorcountПорта.Запиши(0)
	само.lbalowПорта.Запиши(0)
	само.lbamidПорта.Запиши(0)
	само.lbahiПорта.Запиши(0)
	само.командаПорта.Запиши(0xEC)

	статус = само.командаПорта.Читај()
	if статус == 0x00 {
		console_2.MПечати(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (статус&0x80) == 0x80 && (статус&0x01) != 0x01 {
		статус = само.командаПорта.Читај()
	}

	if (статус & 0x01) != 0 {
		console_2.MПечати(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = само.dataПорта.Читај()
		текст := []byte("  ")
		текст[0] = uint8((data >> 8) & 0xFF)
		текст[1] = uint8(data & 0xFF)

	}
	console_2.MПечатиxy(([]byte)("ata ok"), 10, 22)

}
func (само *TНапредноtechnologyattachment) Читај28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MПечати(([]byte)("ata read error "))
		return
	}
	if count > Бајтиpersector {
		console_2.MПечати(([]byte)("ata read error "))
		return
	}

	if само.master {
		само.уредПорта.Запиши(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		само.уредПорта.Запиши(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	само.грешкаПорта.Запиши(0)
	само.sectorcountПорта.Запиши(1)

	само.lbalowПорта.Запиши(uint8(sector & 0x000000FF))
	само.lbamidПорта.Запиши(uint8((sector & 0x0000FF00) >> 8))
	само.lbahiПорта.Запиши(uint8((sector & 0x00FF0000) >> 16))
	само.командаПорта.Запиши(0x20)

	var статус uint8 = само.командаПорта.Читај()
	for ((статус & 0x80) == 0x80) && ((статус & 0x01) != 0x01) {
		статус = само.командаПорта.Читај()
	}

	if (статус & 0x01) != 0 {
		console_2.MПечати(([]byte)("ata read error "))
		return
	}

	console_2.MПечатиxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = само.dataПорта.Читај()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Бајтиpersector; i += 2 {
		само.dataПорта.Читај()
	}
}
func (само *TНапредноtechnologyattachment) Запиши28(sectornumber uint32, data []byte, count uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if само.master {
		само.уредПорта.Запиши(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		само.уредПорта.Запиши(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	само.грешкаПорта.Запиши(0)
	само.sectorcountПорта.Запиши(1)
	само.lbalowПорта.Запиши(uint8(sectornumber & 0x000000FF))
	само.lbamidПорта.Запиши(uint8((sectornumber & 0x0000FF00) >> 8))
	само.lbahiПорта.Запиши(uint8((sectornumber & 0x00FF0000) >> 16))
	само.командаПорта.Запиши(0x30)

	var console_2 = TConsole{}
	console_2.MПечати(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		само.dataПорта.Запиши(wdata)

		текст := []byte("  ")
		текст[0] = uint8((wdata >> 8) & 0xFF)
		текст[1] = uint8(wdata & 0xFF)

		console_2.MПечати(текст)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		само.dataПорта.Запиши(0x0000)
	}

}

func (само *TНапредноtechnologyattachment) Flush() {
	if само.master {
		само.уредПорта.Запиши(0xE0)
	} else {
		само.уредПорта.Запиши(0xF0)
	}
	само.командаПорта.Запиши(0xE7)

	var console_2 = TConsole{}

	var статус uint8 = само.командаПорта.Читај()
	if статус == 0x00 {
		return
	}

	for ((статус & 0x80) == 0x80) && ((статус & 0x01) != 0x01) {
		статус = само.командаПорта.Читај()
	}
	if (статус & 0x01) != 0 {
		console_2.MПечати(([]byte)(" ata flush error"))
		return
	}

}
