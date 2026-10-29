/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTabelentri struct {
	bootable	uint8

	mulaihead	uint8
	mulaisector	uint8
	mulaicylinder	uint16

	Partitionid	uint8

	akhirhead	uint8
	akhirsector	uint8
	akhircylinder	uint16

	Mulailba	uint32
	panjang		uint32
}

func (dirisendiri *TPartitionTabelentri) Init(data [16]byte) {
	dirisendiri.bootable = data[0]

	dirisendiri.mulaihead = data[1]
	dirisendiri.mulaisector = (data[2] >> 2)
	dirisendiri.mulaicylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	dirisendiri.Partitionid = data[4]

	dirisendiri.akhirhead = data[5]
	dirisendiri.akhirsector = (data[6] >> 2)
	dirisendiri.akhircylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	dirisendiri.Mulailba = Unsignedinteger32r(Jajarantounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	dirisendiri.panjang = Unsignedinteger32r(Jajarantounsignedinteger32(buffer2))
}

type TRekaman_awal_utama struct {
	bootloader	[440]byte
	signature	uint32
	takberguna	uint16

	Primarypartition	[4]TPartitionTabelentri

	magicnumber	uint16
}
type TmsdospartitionTabel struct {
	Mbr TRekaman_awal_utama
}

func (dirisendiri *TmsdospartitionTabel) Bacapartition(hd *TLanjutanTeknologiattachment) {

	console_2 := TConsole{}
	console_2.MCetak(([]byte)("Reading MBR"))

	var partitionByte [512]byte
	var buffer_2 = partitionByte[:]
	hd.Baca28(0, &buffer_2, 512)

	dirisendiri.Mbr = TRekaman_awal_utama{}
	var i int = 0
	for ; i < 440; i++ {
		dirisendiri.Mbr.bootloader[i] = partitionByte[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionByte[i:i+4])
	dirisendiri.Mbr.signature = Unsignedinteger32r(Jajarantounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionByte[i:i+2])
	dirisendiri.Mbr.takberguna = Unsignedinteger16r(Jajarantounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionByte[i:i+16])
	dirisendiri.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	dirisendiri.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	dirisendiri.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	dirisendiri.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionByte[i:i+2])
	dirisendiri.Mbr.magicnumber = Unsignedinteger16r(Jajarantounsignedinteger16(buffer6))

	if dirisendiri.Mbr.magicnumber != 0xAA55 {
		console_2.MCetak(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if dirisendiri.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
