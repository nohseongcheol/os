/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTabulaieraksts struct {
	bootable	uint8

	startēthead	uint8
	startētsector	uint8
	startētcylinder	uint16

	Partitionid	uint8

	beigashead	uint8
	beigassector	uint8
	beigascylinder	uint16

	Startētlba	uint32
	garums		uint32
}

func (pats *TPartitionTabulaieraksts) Init(data [16]byte) {
	pats.bootable = data[0]

	pats.startēthead = data[1]
	pats.startētsector = (data[2] >> 2)
	pats.startētcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	pats.Partitionid = data[4]

	pats.beigashead = data[5]
	pats.beigassector = (data[6] >> 2)
	pats.beigascylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	pats.Startētlba = Unsignedinteger32r(Masīvstounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	pats.garums = Unsignedinteger32r(Masīvstounsignedinteger32(buffer2))
}

type TMasterbootrecord struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionTabulaieraksts

	magicnumber	uint16
}
type TmsdospartitionTabula struct {
	Mbr TMasterbootrecord
}

func (pats *TmsdospartitionTabula) Lasītpartition(hd *TPaplašinātiTehnoloģijaattachment) {

	console_2 := TConsole{}
	console_2.MDrukāt(([]byte)("Reading MBR"))

	var partitionBaiti [512]byte
	var buffer_2 = partitionBaiti[:]
	hd.Lasīt28(0, &buffer_2, 512)

	pats.Mbr = TMasterbootrecord{}
	var i int = 0
	for ; i < 440; i++ {
		pats.Mbr.bootloader[i] = partitionBaiti[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBaiti[i:i+4])
	pats.Mbr.signature = Unsignedinteger32r(Masīvstounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBaiti[i:i+2])
	pats.Mbr.unused = Unsignedinteger16r(Masīvstounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBaiti[i:i+16])
	pats.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBaiti[i:i+16])
	pats.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBaiti[i:i+16])
	pats.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBaiti[i:i+16])
	pats.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBaiti[i:i+2])
	pats.Mbr.magicnumber = Unsignedinteger16r(Masīvstounsignedinteger16(buffer6))

	if pats.Mbr.magicnumber != 0xAA55 {
		console_2.MDrukāt(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if pats.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
