/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdosразделДиска

import . "консоль"
import . "утилита"

import . "драйвер/ata"

type TРазделДискаТаблицазапись struct {
	bootable	uint8

	пускhead	uint8
	пускsector	uint8
	пускcylinder	uint16

	РазделДискаИДЕНТИФИКАТОР	uint8

	концеhead	uint8
	концеsector	uint8
	концеcylinder	uint16

	Пускlba	uint32
	длина	uint32
}

func (текущий *TРазделДискаТаблицазапись) Init(данные [16]byte) {
	текущий.bootable = данные[0]

	текущий.пускhead = данные[1]
	текущий.пускsector = (данные[2] >> 2)
	текущий.пускcylinder = Unsignedinteger16r(uint16(данные[2]&0x03) | uint16(данные[3]))

	текущий.РазделДискаИДЕНТИФИКАТОР = данные[4]

	текущий.концеhead = данные[5]
	текущий.концеsector = (данные[6] >> 2)
	текущий.концеcylinder = Unsignedinteger16r(uint16(данные[6]&0x03) | uint16(данные[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], данные[8:12])
	текущий.Пускlba = Unsignedinteger32r(Массивкunsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], данные[12:16])
	текущий.длина = Unsignedinteger32r(Массивкunsignedinteger32(buffer2))
}

type TГлавная_загрузочная_запись struct {
	bootloader	[440]byte
	signature	uint32
	неиспользовано	uint16

	PrimaryразделДиска	[4]TРазделДискаТаблицазапись

	magicnumber	uint16
}
type TmsdosразделДискаТаблица struct {
	Mbr TГлавная_загрузочная_запись
}

func (текущий *TmsdosразделДискаТаблица) ЧитатьразделДиска(hd *TДополнительноТехнологияattachment) {

	консоль_2 := TКонсоль{}
	консоль_2.MПечать(([]byte)("Reading MBR"))

	var разделДискаБайт [512]byte
	var buffer_2 = разделДискаБайт[:]
	hd.Читать28(0, &buffer_2, 512)

	текущий.Mbr = TГлавная_загрузочная_запись{}
	var i int = 0
	for ; i < 440; i++ {
		текущий.Mbr.bootloader[i] = разделДискаБайт[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], разделДискаБайт[i:i+4])
	текущий.Mbr.signature = Unsignedinteger32r(Массивкunsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], разделДискаБайт[i:i+2])
	текущий.Mbr.неиспользовано = Unsignedinteger16r(Массивкunsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], разделДискаБайт[i:i+16])
	текущий.Mbr.PrimaryразделДиска[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], разделДискаБайт[i:i+16])
	текущий.Mbr.PrimaryразделДиска[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], разделДискаБайт[i:i+16])
	текущий.Mbr.PrimaryразделДиска[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], разделДискаБайт[i:i+16])
	текущий.Mbr.PrimaryразделДиска[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], разделДискаБайт[i:i+2])
	текущий.Mbr.magicnumber = Unsignedinteger16r(Массивкunsignedinteger16(buffer6))

	if текущий.Mbr.magicnumber != 0xAA55 {
		консоль_2.MПечать(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if текущий.Mbr.PrimaryразделДиска[i].РазделДискаИДЕНТИФИКАТОР == 0x00 {
			continue
		}

	}
}
