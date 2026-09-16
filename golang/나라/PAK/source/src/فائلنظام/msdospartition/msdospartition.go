/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionجدولentry struct {
	bootable	uint8

	چلائیںhead	uint8
	چلائیںsector	uint8
	چلائیںcylinder	uint16

	Partitionآئیڈی	uint8

	آخرhead		uint8
	آخرsector	uint8
	آخرcylinder	uint16

	Sچلائیںlba	uint32
	طول		uint32
}

func (self *TPartitionجدولentry) Init(data [16]byte) {
	self.bootable = data[0]

	self.چلائیںhead = data[1]
	self.چلائیںsector = (data[2] >> 2)
	self.چلائیںcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.Partitionآئیڈی = data[4]

	self.آخرhead = data[5]
	self.آخرsector = (data[6] >> 2)
	self.آخرcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Sچلائیںlba = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.طول = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer2))
}

type TMasterbootrecord struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionجدولentry

	magicnumber	uint16
}
type Tmsdospartitionجدول struct {
	Mbr TMasterbootrecord
}

func (self *Tmsdospartitionجدول) Rپڑھیںpartition(hd *Tاعلیٹیکنالوجیattachment) {

	console_2 := TConsole{}
	console_2.Mچھاپیں(([]byte)("Reading MBR"))

	var partitionبائٹس [512]byte
	var buffer_2 = partitionبائٹس[:]
	hd.Rپڑھیں28(0, &buffer_2, 512)

	self.Mbr = TMasterbootrecord{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionبائٹس[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionبائٹس[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionبائٹس[i:i+2])
	self.Mbr.unused = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionبائٹس[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionبائٹس[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionبائٹس[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionبائٹس[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionبائٹس[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.Mچھاپیں(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].Partitionآئیڈی == 0x00 {
			continue
		}

	}
}
