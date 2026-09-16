/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "konzola"
import . "util"

import . "driver/ata"

type TPartitionTabuľkapoložka struct {
	bootable	uint8

	spustiťhead	uint8
	spustiťsector	uint8
	spustiťcylinder	uint16

	PartitionIdentifikátor	uint8

	koniechead	uint8
	koniecsector	uint8
	konieccylinder	uint16

	Spustiťlba	uint32
	dĺžka		uint32
}

func (vlastný *TPartitionTabuľkapoložka) Init(data [16]byte) {
	vlastný.bootable = data[0]

	vlastný.spustiťhead = data[1]
	vlastný.spustiťsector = (data[2] >> 2)
	vlastný.spustiťcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	vlastný.PartitionIdentifikátor = data[4]

	vlastný.koniechead = data[5]
	vlastný.koniecsector = (data[6] >> 2)
	vlastný.konieccylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	vlastný.Spustiťlba = Unsignedinteger32r(Poletounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	vlastný.dĺžka = Unsignedinteger32r(Poletounsignedinteger32(buffer2))
}

type THlavnýbootNahrávka struct {
	bootloader	[440]byte
	signature	uint32
	nepoužité	uint16

	Primarypartition	[4]TPartitionTabuľkapoložka

	magicnumber	uint16
}
type TmsdospartitionTabuľka struct {
	Mbr THlavnýbootNahrávka
}

func (vlastný *TmsdospartitionTabuľka) Čítaniepartition(hd *TPokročiléTechnológiaattachment) {

	konzola_2 := TKonzola{}
	konzola_2.MTlačiť(([]byte)("Reading MBR"))

	var partitionBajty [512]byte
	var buffer_2 = partitionBajty[:]
	hd.Čítanie28(0, &buffer_2, 512)

	vlastný.Mbr = THlavnýbootNahrávka{}
	var i int = 0
	for ; i < 440; i++ {
		vlastný.Mbr.bootloader[i] = partitionBajty[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBajty[i:i+4])
	vlastný.Mbr.signature = Unsignedinteger32r(Poletounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBajty[i:i+2])
	vlastný.Mbr.nepoužité = Unsignedinteger16r(Poletounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBajty[i:i+16])
	vlastný.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajty[i:i+16])
	vlastný.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajty[i:i+16])
	vlastný.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajty[i:i+16])
	vlastný.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBajty[i:i+2])
	vlastný.Mbr.magicnumber = Unsignedinteger16r(Poletounsignedinteger16(buffer6))

	if vlastný.Mbr.magicnumber != 0xAA55 {
		konzola_2.MTlačiť(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if vlastný.Mbr.Primarypartition[i].PartitionIdentifikátor == 0x00 {
			continue
		}

	}
}
