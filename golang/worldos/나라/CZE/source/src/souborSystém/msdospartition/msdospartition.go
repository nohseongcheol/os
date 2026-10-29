/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "konzole"
import . "util"

import . "driver/ata"

type TPartitionTabulkaZáznam struct {
	bootable	uint8

	spustithead	uint8
	spustitsector	uint8
	spustitcylinder	uint16

	Partitionid	uint8

	konechead	uint8
	konecsector	uint8
	koneccylinder	uint16

	Spustitlba	uint32
	délka		uint32
}

func (self *TPartitionTabulkaZáznam) Init(data [16]byte) {
	self.bootable = data[0]

	self.spustithead = data[1]
	self.spustitsector = (data[2] >> 2)
	self.spustitcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.Partitionid = data[4]

	self.konechead = data[5]
	self.konecsector = (data[6] >> 2)
	self.koneccylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Spustitlba = Unsignedinteger32r(Poledounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.délka = Unsignedinteger32r(Poledounsignedinteger32(buffer2))
}

type THlavní_spouštěcí_záznam struct {
	bootloader	[440]byte
	signature	uint32
	nepoužito	uint16

	Primarypartition	[4]TPartitionTabulkaZáznam

	magicnumber	uint16
}
type TmsdospartitionTabulka struct {
	Mbr THlavní_spouštěcí_záznam
}

func (self *TmsdospartitionTabulka) Čtenípartition(hd *TPokročiléTechnologieattachment) {

	konzole_2 := TKonzole{}
	konzole_2.MTisknout(([]byte)("Reading MBR"))

	var partitionBytů [512]byte
	var buffer_2 = partitionBytů[:]
	hd.Čtení28(0, &buffer_2, 512)

	self.Mbr = THlavní_spouštěcí_záznam{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionBytů[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBytů[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Poledounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBytů[i:i+2])
	self.Mbr.nepoužito = Unsignedinteger16r(Poledounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBytů[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBytů[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBytů[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBytů[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBytů[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Poledounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		konzole_2.MTisknout(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
