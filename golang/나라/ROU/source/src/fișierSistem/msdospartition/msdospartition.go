/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTabelînregistrare struct {
	bootable	uint8

	porneștehead		uint8
	porneștesector		uint8
	porneștecylinder	uint16

	Partitionid	uint8

	sfârșithead	uint8
	sfârșitsector	uint8
	sfârșitcylinder	uint16

	Porneștelba	uint32
	durată		uint32
}

func (sine *TPartitionTabelînregistrare) Init(data [16]byte) {
	sine.bootable = data[0]

	sine.porneștehead = data[1]
	sine.porneștesector = (data[2] >> 2)
	sine.porneștecylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	sine.Partitionid = data[4]

	sine.sfârșithead = data[5]
	sine.sfârșitsector = (data[6] >> 2)
	sine.sfârșitcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	sine.Porneștelba = Unsignedinteger32r(Vectortounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	sine.durată = Unsignedinteger32r(Vectortounsignedinteger32(buffer2))
}

type TPrincipalbootÎnregistrare struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionTabelînregistrare

	magicnumber	uint16
}
type TmsdospartitionTabel struct {
	Mbr TPrincipalbootÎnregistrare
}

func (sine *TmsdospartitionTabel) Citirepartition(hd *TAvansateTehnologieattachment) {

	console_2 := TConsole{}
	console_2.MTipărește(([]byte)("Reading MBR"))

	var partitionOcteți [512]byte
	var buffer_2 = partitionOcteți[:]
	hd.Citire28(0, &buffer_2, 512)

	sine.Mbr = TPrincipalbootÎnregistrare{}
	var i int = 0
	for ; i < 440; i++ {
		sine.Mbr.bootloader[i] = partitionOcteți[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionOcteți[i:i+4])
	sine.Mbr.signature = Unsignedinteger32r(Vectortounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionOcteți[i:i+2])
	sine.Mbr.unused = Unsignedinteger16r(Vectortounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionOcteți[i:i+16])
	sine.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOcteți[i:i+16])
	sine.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOcteți[i:i+16])
	sine.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOcteți[i:i+16])
	sine.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionOcteți[i:i+2])
	sine.Mbr.magicnumber = Unsignedinteger16r(Vectortounsignedinteger16(buffer6))

	if sine.Mbr.magicnumber != 0xAA55 {
		console_2.MTipărește(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if sine.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
