package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionLentelėįrašas struct {
	bootable	uint8

	paleistihead		uint8
	paleistisector		uint8
	paleisticylinder	uint16

	Partitionid	uint8

	pabhead		uint8
	pabsector	uint8
	pabcylinder	uint16

	Paleistilba	uint32
	trukmė		uint32
}

func (self *TPartitionLentelėįrašas) Init(data [16]byte) {
	self.bootable = data[0]

	self.paleistihead = data[1]
	self.paleistisector = (data[2] >> 2)
	self.paleisticylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.Partitionid = data[4]

	self.pabhead = data[5]
	self.pabsector = (data[6] >> 2)
	self.pabcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Paleistilba = Unsignedinteger32r(Masyvastounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.trukmė = Unsignedinteger32r(Masyvastounsignedinteger32(buffer2))
}

type TPagrindinisbootĮrašinėti struct {
	bootloader	[440]byte
	signature	uint32
	nenaudojama	uint16

	Primarypartition	[4]TPartitionLentelėįrašas

	magicnumber	uint16
}
type TmsdospartitionLentelė struct {
	Mbr TPagrindinisbootĮrašinėti
}

func (self *TmsdospartitionLentelė) Skaitymaspartition(hd *TIšsamiauTechnologijaattachment) {

	console_2 := TConsole{}
	console_2.MSpausdinti(([]byte)("Reading MBR"))

	var partitionBaitų [512]byte
	var buffer_2 = partitionBaitų[:]
	hd.Skaitymas28(0, &buffer_2, 512)

	self.Mbr = TPagrindinisbootĮrašinėti{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionBaitų[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBaitų[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Masyvastounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBaitų[i:i+2])
	self.Mbr.nenaudojama = Unsignedinteger16r(Masyvastounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBaitų[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBaitų[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBaitų[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBaitų[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBaitų[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Masyvastounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.MSpausdinti(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
