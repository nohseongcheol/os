/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTabelemne struct {
	bootable	uint8

	begyndhead	uint8
	begyndsector	uint8
	begyndcylinder	uint16

	Partitionid	uint8

	slutningenhead		uint8
	slutningensector	uint8
	slutningencylinder	uint16

	Begyndlba	uint32
	længde		uint32
}

func (selv *TPartitionTabelemne) Init(data [16]byte) {
	selv.bootable = data[0]

	selv.begyndhead = data[1]
	selv.begyndsector = (data[2] >> 2)
	selv.begyndcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	selv.Partitionid = data[4]

	selv.slutningenhead = data[5]
	selv.slutningensector = (data[6] >> 2)
	selv.slutningencylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	selv.Begyndlba = Unsignedinteger32r(Tabeltounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	selv.længde = Unsignedinteger32r(Tabeltounsignedinteger32(buffer2))
}

type TMasterbootOptag struct {
	bootloader	[440]byte
	signature	uint32
	ubrugt		uint16

	Primarypartition	[4]TPartitionTabelemne

	magicnumber	uint16
}
type TmsdospartitionTabel struct {
	Mbr TMasterbootOptag
}

func (selv *TmsdospartitionTabel) Læsepartition(hd *TAvanceretTeknologiattachment) {

	console_2 := TConsole{}
	console_2.MUdskriv(([]byte)("Reading MBR"))

	var partitionByte [512]byte
	var buffer_2 = partitionByte[:]
	hd.Læse28(0, &buffer_2, 512)

	selv.Mbr = TMasterbootOptag{}
	var i int = 0
	for ; i < 440; i++ {
		selv.Mbr.bootloader[i] = partitionByte[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionByte[i:i+4])
	selv.Mbr.signature = Unsignedinteger32r(Tabeltounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionByte[i:i+2])
	selv.Mbr.ubrugt = Unsignedinteger16r(Tabeltounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionByte[i:i+16])
	selv.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	selv.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	selv.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	selv.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionByte[i:i+2])
	selv.Mbr.magicnumber = Unsignedinteger16r(Tabeltounsignedinteger16(buffer6))

	if selv.Mbr.magicnumber != 0xAA55 {
		console_2.MUdskriv(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if selv.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
