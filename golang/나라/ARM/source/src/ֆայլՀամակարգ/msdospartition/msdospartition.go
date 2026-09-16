/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionԱղյուսակentry struct {
	bootable	uint8

	սկիզբhead	uint8
	սկիզբsector	uint8
	սկիզբcylinder	uint16

	Partitionid	uint8

	վերջhead	uint8
	վերջsector	uint8
	վերջcylinder	uint16

	Սկիզբlba	uint32
	երկարություն	uint32
}

func (ինքնուրույն *TPartitionԱղյուսակentry) Init(data [16]byte) {
	ինքնուրույն.bootable = data[0]

	ինքնուրույն.սկիզբhead = data[1]
	ինքնուրույն.սկիզբsector = (data[2] >> 2)
	ինքնուրույն.սկիզբcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	ինքնուրույն.Partitionid = data[4]

	ինքնուրույն.վերջhead = data[5]
	ինքնուրույն.վերջsector = (data[6] >> 2)
	ինքնուրույն.վերջcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	ինքնուրույն.Սկիզբlba = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	ինքնուրույն.երկարություն = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer2))
}

type TՎարպետbootՁայնագրել struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionԱղյուսակentry

	magicnumber	uint16
}
type TmsdospartitionԱղյուսակ struct {
	Mbr TՎարպետbootՁայնագրել
}

func (ինքնուրույն *TmsdospartitionԱղյուսակ) Ընթերցումpartition(hd *TԸնդլայնվածՏեխնոլոգիաattachment) {

	console_2 := TConsole{}
	console_2.MՏպել(([]byte)("Reading MBR"))

	var partitionԲայթեր [512]byte
	var buffer_2 = partitionԲայթեր[:]
	hd.Ընթերցում28(0, &buffer_2, 512)

	ինքնուրույն.Mbr = TՎարպետbootՁայնագրել{}
	var i int = 0
	for ; i < 440; i++ {
		ինքնուրույն.Mbr.bootloader[i] = partitionԲայթեր[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionԲայթեր[i:i+4])
	ինքնուրույն.Mbr.signature = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionԲայթեր[i:i+2])
	ինքնուրույն.Mbr.unused = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionԲայթեր[i:i+16])
	ինքնուրույն.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionԲայթեր[i:i+16])
	ինքնուրույն.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionԲայթեր[i:i+16])
	ինքնուրույն.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionԲայթեր[i:i+16])
	ինքնուրույն.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionԲայթեր[i:i+2])
	ինքնուրույն.Mbr.magicnumber = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer6))

	if ինքնուրույն.Mbr.magicnumber != 0xAA55 {
		console_2.MՏպել(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if ինքնուրույն.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
