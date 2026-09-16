/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTabellavoce struct {
	bootable	uint8

	avviahead	uint8
	avviasector	uint8
	avviacylinder	uint16

	Partitionid	uint8

	finehead	uint8
	finesector	uint8
	finecylinder	uint16

	Avvialba	uint32
	durata		uint32
}

func (séstesso *TPartitionTabellavoce) Init(data [16]byte) {
	séstesso.bootable = data[0]

	séstesso.avviahead = data[1]
	séstesso.avviasector = (data[2] >> 2)
	séstesso.avviacylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	séstesso.Partitionid = data[4]

	séstesso.finehead = data[5]
	séstesso.finesector = (data[6] >> 2)
	séstesso.finecylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	séstesso.Avvialba = Unsignedinteger32r(Serietounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	séstesso.durata = Unsignedinteger32r(Serietounsignedinteger32(buffer2))
}

type TRecord_principale_di_avvio struct {
	bootloader	[440]byte
	signature	uint32
	inutilizzato	uint16

	Primarypartition	[4]TPartitionTabellavoce

	magicnumber	uint16
}
type TmsdospartitionTabella struct {
	Mbr TRecord_principale_di_avvio
}

func (séstesso *TmsdospartitionTabella) Letturapartition(hd *TAvanzateTecnologiaattachment) {

	console_2 := TConsole{}
	console_2.MStampa(([]byte)("Reading MBR"))

	var partitionByte [512]byte
	var buffer_2 = partitionByte[:]
	hd.Lettura28(0, &buffer_2, 512)

	séstesso.Mbr = TRecord_principale_di_avvio{}
	var i int = 0
	for ; i < 440; i++ {
		séstesso.Mbr.bootloader[i] = partitionByte[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionByte[i:i+4])
	séstesso.Mbr.signature = Unsignedinteger32r(Serietounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionByte[i:i+2])
	séstesso.Mbr.inutilizzato = Unsignedinteger16r(Serietounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionByte[i:i+16])
	séstesso.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	séstesso.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	séstesso.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	séstesso.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionByte[i:i+2])
	séstesso.Mbr.magicnumber = Unsignedinteger16r(Serietounsignedinteger16(buffer6))

	if séstesso.Mbr.magicnumber != 0xAA55 {
		console_2.MStampa(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if séstesso.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
