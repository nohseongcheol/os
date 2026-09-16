/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "konsola"
import . "util"

import . "driver/ata"

type TPartitionTabelawpis struct {
	bootable	uint8

	uruchomhead	uint8
	uruchomsector	uint8
	uruchomcylinder	uint16

	PartitionIdentyfikator	uint8

	koniechead	uint8
	koniecsector	uint8
	konieccylinder	uint16

	Uruchomlba	uint32
	długość		uint32
}

func (bieżący *TPartitionTabelawpis) Init(data [16]byte) {
	bieżący.bootable = data[0]

	bieżący.uruchomhead = data[1]
	bieżący.uruchomsector = (data[2] >> 2)
	bieżący.uruchomcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	bieżący.PartitionIdentyfikator = data[4]

	bieżący.koniechead = data[5]
	bieżący.koniecsector = (data[6] >> 2)
	bieżący.konieccylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	bieżący.Uruchomlba = Unsignedinteger32r(Tablicatounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	bieżący.długość = Unsignedinteger32r(Tablicatounsignedinteger32(buffer2))
}

type TGłówny_rekord_rozruchowy struct {
	bootloader	[440]byte
	signature	uint32
	wolne_2		uint16

	Primarypartition	[4]TPartitionTabelawpis

	magicnumber	uint16
}
type TmsdospartitionTabela struct {
	Mbr TGłówny_rekord_rozruchowy
}

func (bieżący *TmsdospartitionTabela) Odczytpartition(hd *TZaawansowaneTechnologiaattachment) {

	konsola_2 := TKonsola{}
	konsola_2.MWydrukuj(([]byte)("Reading MBR"))

	var partitionBajty [512]byte
	var buffer_2 = partitionBajty[:]
	hd.Odczyt28(0, &buffer_2, 512)

	bieżący.Mbr = TGłówny_rekord_rozruchowy{}
	var i int = 0
	for ; i < 440; i++ {
		bieżący.Mbr.bootloader[i] = partitionBajty[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBajty[i:i+4])
	bieżący.Mbr.signature = Unsignedinteger32r(Tablicatounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBajty[i:i+2])
	bieżący.Mbr.wolne_2 = Unsignedinteger16r(Tablicatounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBajty[i:i+16])
	bieżący.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajty[i:i+16])
	bieżący.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajty[i:i+16])
	bieżący.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajty[i:i+16])
	bieżący.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBajty[i:i+2])
	bieżący.Mbr.magicnumber = Unsignedinteger16r(Tablicatounsignedinteger16(buffer6))

	if bieżący.Mbr.magicnumber != 0xAA55 {
		konsola_2.MWydrukuj(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if bieżący.Mbr.Primarypartition[i].PartitionIdentyfikator == 0x00 {
			continue
		}

	}
}
