/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "konsoli"
import . "util"

import . "driver/ata"

type TPartitionTaulukkohakusana struct {
	bootable	uint8

	käynnistähead		uint8
	käynnistäsector		uint8
	käynnistäcylinder	uint16

	PartitionTUNNISTE	uint8

	loppuajankohtahead	uint8
	loppuajankohtasector	uint8
	loppuajankohtacylinder	uint16

	Käynnistälba	uint32
	kesto		uint32
}

func (itse *TPartitionTaulukkohakusana) Init(data [16]byte) {
	itse.bootable = data[0]

	itse.käynnistähead = data[1]
	itse.käynnistäsector = (data[2] >> 2)
	itse.käynnistäcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	itse.PartitionTUNNISTE = data[4]

	itse.loppuajankohtahead = data[5]
	itse.loppuajankohtasector = (data[6] >> 2)
	itse.loppuajankohtacylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	itse.Käynnistälba = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	itse.kesto = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer2))
}

type TPääkäynnistystietue struct {
	bootloader	[440]byte
	signature	uint32
	eikäytössä	uint16

	Primarypartition	[4]TPartitionTaulukkohakusana

	magicnumber	uint16
}
type TmsdospartitionTaulukko struct {
	Mbr TPääkäynnistystietue
}

func (itse *TmsdospartitionTaulukko) Lukupartition(hd *TLisäasetuksetTekniikkaattachment) {

	konsoli_2 := TKonsoli{}
	konsoli_2.MTulosta(([]byte)("Reading MBR"))

	var partitiontavua [512]byte
	var buffer_2 = partitiontavua[:]
	hd.Luku28(0, &buffer_2, 512)

	itse.Mbr = TPääkäynnistystietue{}
	var i int = 0
	for ; i < 440; i++ {
		itse.Mbr.bootloader[i] = partitiontavua[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitiontavua[i:i+4])
	itse.Mbr.signature = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitiontavua[i:i+2])
	itse.Mbr.eikäytössä = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitiontavua[i:i+16])
	itse.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitiontavua[i:i+16])
	itse.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitiontavua[i:i+16])
	itse.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitiontavua[i:i+16])
	itse.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitiontavua[i:i+2])
	itse.Mbr.magicnumber = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer6))

	if itse.Mbr.magicnumber != 0xAA55 {
		konsoli_2.MTulosta(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if itse.Mbr.Primarypartition[i].PartitionTUNNISTE == 0x00 {
			continue
		}

	}
}
