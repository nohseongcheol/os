/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "порт"
import . "console"

const Байтовеpersector int = 512

type TДопълнителниТехнологияattachment struct {
	главен		bool
	dataПорт	TПорт16bit
	грешкаПорт	TПорт8bit
	sectorcountПорт	TПорт8bit
	lbaНисъкПорт	TПорт8bit
	lbamidПорт	TПорт8bit
	lbahiПорт	TПорт8bit
	устройствоПорт	TПорт8bit
	командаПорт	TПорт8bit
	ctrlПорт	TПорт8bit
}

func (себеси *TДопълнителниТехнологияattachment) Init(главен bool, портbase uint16) {
	себеси.главен = главен
	себеси.dataПорт.Init(портbase)
	себеси.грешкаПорт.Init(портbase + 0x1)
	себеси.sectorcountПорт.Init(портbase + 0x2)
	себеси.lbaНисъкПорт.Init(портbase + 0x3)
	себеси.lbamidПорт.Init(портbase + 0x4)
	себеси.lbahiПорт.Init(портbase + 0x5)
	себеси.устройствоПорт.Init(портbase + 0x6)
	себеси.командаПорт.Init(портbase + 0x7)
	себеси.ctrlПорт.Init(портbase + 0x8)

}

func (себеси *TДопълнителниТехнологияattachment) Identify() {

	var console_2 = TConsole{}

	if себеси.главен {
		себеси.устройствоПорт.Писане(0xA0)
	} else {
		себеси.устройствоПорт.Писане(0xB0)
	}
	себеси.ctrlПорт.Писане(0)
	себеси.устройствоПорт.Писане(0xA0)

	var състояние uint8 = себеси.командаПорт.Четене()
	if състояние == 0xFF {
		console_2.MПечат(([]byte)("Invalid Status"))
		return
	}

	if себеси.главен {
		себеси.устройствоПорт.Писане(0xA0)
	} else {
		себеси.устройствоПорт.Писане(0xB0)
	}
	себеси.sectorcountПорт.Писане(0)
	себеси.lbaНисъкПорт.Писане(0)
	себеси.lbamidПорт.Писане(0)
	себеси.lbahiПорт.Писане(0)
	себеси.командаПорт.Писане(0xEC)

	състояние = себеси.командаПорт.Четене()
	if състояние == 0x00 {
		console_2.MПечат(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (състояние&0x80) == 0x80 && (състояние&0x01) != 0x01 {
		състояние = себеси.командаПорт.Четене()
	}

	if (състояние & 0x01) != 0 {
		console_2.MПечат(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var data = себеси.dataПорт.Четене()
		текст := []byte("  ")
		текст[0] = uint8((data >> 8) & 0xFF)
		текст[1] = uint8(data & 0xFF)

	}
	console_2.MПечатxy(([]byte)("ata ok"), 10, 22)

}
func (себеси *TДопълнителниТехнологияattachment) Четене28(sector uint32, data *[]byte, count int) {
	var console_2 = TConsole{}
	if (sector & 0xF0000000) != 0 {
		console_2.MПечат(([]byte)("ata read error "))
		return
	}
	if count > Байтовеpersector {
		console_2.MПечат(([]byte)("ata read error "))
		return
	}

	if себеси.главен {
		себеси.устройствоПорт.Писане(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		себеси.устройствоПорт.Писане(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	себеси.грешкаПорт.Писане(0)
	себеси.sectorcountПорт.Писане(1)

	себеси.lbaНисъкПорт.Писане(uint8(sector & 0x000000FF))
	себеси.lbamidПорт.Писане(uint8((sector & 0x0000FF00) >> 8))
	себеси.lbahiПорт.Писане(uint8((sector & 0x00FF0000) >> 16))
	себеси.командаПорт.Писане(0x20)

	var състояние uint8 = себеси.командаПорт.Четене()
	for ((състояние & 0x80) == 0x80) && ((състояние & 0x01) != 0x01) {
		състояние = себеси.командаПорт.Четене()
	}

	if (състояние & 0x01) != 0 {
		console_2.MПечат(([]byte)("ata read error "))
		return
	}

	console_2.MПечатxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < count; i += 2 {
		var wdata uint16 = себеси.dataПорт.Четене()

		(*data)[i] = uint8(wdata & 0x00FF)
		if i+1 < count {

			(*data)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (count + (count % 2)); i < Байтовеpersector; i += 2 {
		себеси.dataПорт.Четене()
	}
}
func (себеси *TДопълнителниТехнологияattachment) Писане28(sectorЧисло uint32, data []byte, count uint32) {

	if sectorЧисло > 0x0FFFFFFF {
		return
	}

	if count > 512 {
		return
	}

	if себеси.главен {
		себеси.устройствоПорт.Писане(uint8(0xE0 | uint8((sectorЧисло&0x0F000000)>>24)))
	} else {
		себеси.устройствоПорт.Писане(uint8(0xF0 | uint8((sectorЧисло&0x0F000000)>>24)))
	}

	себеси.грешкаПорт.Писане(0)
	себеси.sectorcountПорт.Писане(1)
	себеси.lbaНисъкПорт.Писане(uint8(sectorЧисло & 0x000000FF))
	себеси.lbamidПорт.Писане(uint8((sectorЧисло & 0x0000FF00) >> 8))
	себеси.lbahiПорт.Писане(uint8((sectorЧисло & 0x00FF0000) >> 16))
	себеси.командаПорт.Писане(0x30)

	var console_2 = TConsole{}
	console_2.MПечат(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < count; i += 2 {

		var wdata uint16 = uint16(data[i])

		if i+1 < count {
			wdata = wdata | (uint16(data[i+1]) << 8)
		}

		себеси.dataПорт.Писане(wdata)

		текст := []byte("  ")
		текст[0] = uint8((wdata >> 8) & 0xFF)
		текст[1] = uint8(wdata & 0xFF)

		console_2.MПечат(текст)
	}

	for i := (count + (count % 2)); i < 512; i += 2 {
		себеси.dataПорт.Писане(0x0000)
	}

}

func (себеси *TДопълнителниТехнологияattachment) Flush() {
	if себеси.главен {
		себеси.устройствоПорт.Писане(0xE0)
	} else {
		себеси.устройствоПорт.Писане(0xF0)
	}
	себеси.командаПорт.Писане(0xE7)

	var console_2 = TConsole{}

	var състояние uint8 = себеси.командаПорт.Четене()
	if състояние == 0x00 {
		return
	}

	for ((състояние & 0x80) == 0x80) && ((състояние & 0x01) != 0x01) {
		състояние = себеси.командаПорт.Четене()
	}
	if (състояние & 0x01) != 0 {
		console_2.MПечат(([]byte)(" ata flush error"))
		return
	}

}
