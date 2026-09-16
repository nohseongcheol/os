/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionPreglednicavnos struct {
	bootable	uint8

	začnihead	uint8
	začnisector	uint8
	začnicylinder	uint16

	Partitionid	uint8

	endhead		uint8
	endsector	uint8
	endcylinder	uint16

	Začnilba	uint32
	dolžina		uint32
}

func (sam *TPartitionPreglednicavnos) Init(data [16]byte) {
	sam.bootable = data[0]

	sam.začnihead = data[1]
	sam.začnisector = (data[2] >> 2)
	sam.začnicylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	sam.Partitionid = data[4]

	sam.endhead = data[5]
	sam.endsector = (data[6] >> 2)
	sam.endcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	sam.Začnilba = Unsignedinteger32r(Poljetounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	sam.dolžina = Unsignedinteger32r(Poljetounsignedinteger32(buffer2))
}

type TGlavnibootSnemanje struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionPreglednicavnos

	magicnumber	uint16
}
type TmsdospartitionPreglednica struct {
	Mbr TGlavnibootSnemanje
}

func (sam *TmsdospartitionPreglednica) Branjepartition(hd *TNaprednoTehnologijaattachment) {

	console_2 := TConsole{}
	console_2.MNatisni(([]byte)("Reading MBR"))

	var partitionBajtov [512]byte
	var buffer_2 = partitionBajtov[:]
	hd.Branje28(0, &buffer_2, 512)

	sam.Mbr = TGlavnibootSnemanje{}
	var i int = 0
	for ; i < 440; i++ {
		sam.Mbr.bootloader[i] = partitionBajtov[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBajtov[i:i+4])
	sam.Mbr.signature = Unsignedinteger32r(Poljetounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBajtov[i:i+2])
	sam.Mbr.unused = Unsignedinteger16r(Poljetounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBajtov[i:i+16])
	sam.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtov[i:i+16])
	sam.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtov[i:i+16])
	sam.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtov[i:i+16])
	sam.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBajtov[i:i+2])
	sam.Mbr.magicnumber = Unsignedinteger16r(Poljetounsignedinteger16(buffer6))

	if sam.Mbr.magicnumber != 0xAA55 {
		console_2.MNatisni(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if sam.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
