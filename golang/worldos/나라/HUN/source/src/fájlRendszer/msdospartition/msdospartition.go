/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "konzol"
import . "util"

import . "driver/ata"

type TPartitionTáblázatbejegyzés struct {
	bootable	uint8

	indításhead	uint8
	indítássector	uint8
	indításcylinder	uint16

	PartitionAzonosító	uint8

	végénhead	uint8
	végénsector	uint8
	végéncylinder	uint16

	Indításlba	uint32
	hossz		uint32
}

func (self *TPartitionTáblázatbejegyzés) Init(data [16]byte) {
	self.bootable = data[0]

	self.indításhead = data[1]
	self.indítássector = (data[2] >> 2)
	self.indításcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.PartitionAzonosító = data[4]

	self.végénhead = data[5]
	self.végénsector = (data[6] >> 2)
	self.végéncylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Indításlba = Unsignedinteger32r(Tömbtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.hossz = Unsignedinteger32r(Tömbtounsignedinteger32(buffer2))
}

type TFőbootFelvétel struct {
	bootloader	[440]byte
	signature	uint32
	szabad_2	uint16

	Primarypartition	[4]TPartitionTáblázatbejegyzés

	magicnumber	uint16
}
type TmsdospartitionTáblázat struct {
	Mbr TFőbootFelvétel
}

func (self *TmsdospartitionTáblázat) Olvasáspartition(hd *THaladóTechnológiaattachment) {

	konzol_2 := TKonzol{}
	konzol_2.MNyomtatás(([]byte)("Reading MBR"))

	var partitionBájt [512]byte
	var buffer_2 = partitionBájt[:]
	hd.Olvasás28(0, &buffer_2, 512)

	self.Mbr = TFőbootFelvétel{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionBájt[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBájt[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Tömbtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBájt[i:i+2])
	self.Mbr.szabad_2 = Unsignedinteger16r(Tömbtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBájt[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBájt[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBájt[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBájt[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBájt[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Tömbtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		konzol_2.MNyomtatás(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].PartitionAzonosító == 0x00 {
			continue
		}

	}
}
