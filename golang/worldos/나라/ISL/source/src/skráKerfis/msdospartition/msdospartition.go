/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTaflaentry struct {
	bootable	uint8

	ræsahead	uint8
	ræsasector	uint8
	ræsacylinder	uint16

	PartitionAuðkenni	uint8

	endhead		uint8
	endsector	uint8
	endcylinder	uint16

	Ræsalba	uint32
	lengd	uint32
}

func (sjálft *TPartitionTaflaentry) Init(data [16]byte) {
	sjálft.bootable = data[0]

	sjálft.ræsahead = data[1]
	sjálft.ræsasector = (data[2] >> 2)
	sjálft.ræsacylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	sjálft.PartitionAuðkenni = data[4]

	sjálft.endhead = data[5]
	sjálft.endsector = (data[6] >> 2)
	sjálft.endcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	sjálft.Ræsalba = Unsignedinteger32r(Fylkitounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	sjálft.lengd = Unsignedinteger32r(Fylkitounsignedinteger32(buffer2))
}

type TMasterbootrecord struct {
	bootloader	[440]byte
	signature	uint32
	ónotað		uint16

	Primarypartition	[4]TPartitionTaflaentry

	magicnumber	uint16
}
type TmsdospartitionTafla struct {
	Mbr TMasterbootrecord
}

func (sjálft *TmsdospartitionTafla) Lesturpartition(hd *TNánarTækniattachment) {

	console_2 := TConsole{}
	console_2.MPrenta(([]byte)("Reading MBR"))

	var partitionBæti [512]byte
	var buffer_2 = partitionBæti[:]
	hd.Lestur28(0, &buffer_2, 512)

	sjálft.Mbr = TMasterbootrecord{}
	var i int = 0
	for ; i < 440; i++ {
		sjálft.Mbr.bootloader[i] = partitionBæti[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBæti[i:i+4])
	sjálft.Mbr.signature = Unsignedinteger32r(Fylkitounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBæti[i:i+2])
	sjálft.Mbr.ónotað = Unsignedinteger16r(Fylkitounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBæti[i:i+16])
	sjálft.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBæti[i:i+16])
	sjálft.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBæti[i:i+16])
	sjálft.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBæti[i:i+16])
	sjálft.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBæti[i:i+2])
	sjálft.Mbr.magicnumber = Unsignedinteger16r(Fylkitounsignedinteger16(buffer6))

	if sjálft.Mbr.magicnumber != 0xAA55 {
		console_2.MPrenta(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if sjálft.Mbr.Primarypartition[i].PartitionAuðkenni == 0x00 {
			continue
		}

	}
}
