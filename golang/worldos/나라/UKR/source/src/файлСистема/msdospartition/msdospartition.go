/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "консоль"
import . "util"

import . "driver/ата"

type TPartitionТаблицязапис struct {
	bootable	uint8

	запуститиhead		uint8
	запуститиsector		uint8
	запуститиcylinder	uint16

	PartitionІДЕНТИФІКАТОР	uint8

	кінецьhead	uint8
	кінецьsector	uint8
	кінецьcylinder	uint16

	Запуститиlba	uint32
	довжина		uint32
}

func (поточний *TPartitionТаблицязапис) Init(data [16]byte) {
	поточний.bootable = data[0]

	поточний.запуститиhead = data[1]
	поточний.запуститиsector = (data[2] >> 2)
	поточний.запуститиcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	поточний.PartitionІДЕНТИФІКАТОР = data[4]

	поточний.кінецьhead = data[5]
	поточний.кінецьsector = (data[6] >> 2)
	поточний.кінецьcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	поточний.Запуститиlba = Unsignedinteger32r(Масивтоunsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	поточний.довжина = Unsignedinteger32r(Масивтоunsignedinteger32(buffer2))
}

type TГоловний_завантажувальний_запис struct {
	bootloader		[440]byte
	signature		uint32
	невикористовується	uint16

	Primarypartition	[4]TPartitionТаблицязапис

	magicnumber	uint16
}
type TmsdospartitionТаблиця struct {
	Mbr TГоловний_завантажувальний_запис
}

func (поточний *TmsdospartitionТаблиця) Читанняpartition(hd *TДодатковоТехнологіяattachment) {

	консоль_2 := TКонсоль{}
	консоль_2.MДрук(([]byte)("Reading MBR"))

	var partitionБайт [512]byte
	var buffer_2 = partitionБайт[:]
	hd.Читання28(0, &buffer_2, 512)

	поточний.Mbr = TГоловний_завантажувальний_запис{}
	var i int = 0
	for ; i < 440; i++ {
		поточний.Mbr.bootloader[i] = partitionБайт[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionБайт[i:i+4])
	поточний.Mbr.signature = Unsignedinteger32r(Масивтоunsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionБайт[i:i+2])
	поточний.Mbr.невикористовується = Unsignedinteger16r(Масивтоunsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionБайт[i:i+16])
	поточний.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайт[i:i+16])
	поточний.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайт[i:i+16])
	поточний.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайт[i:i+16])
	поточний.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionБайт[i:i+2])
	поточний.Mbr.magicnumber = Unsignedinteger16r(Масивтоunsignedinteger16(buffer6))

	if поточний.Mbr.magicnumber != 0xAA55 {
		консоль_2.MДрук(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if поточний.Mbr.Primarypartition[i].PartitionІДЕНТИФІКАТОР == 0x00 {
			continue
		}

	}
}
