package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitiontableentry struct {
	bootable	uint8

	starthead	uint8
	startsector	uint8
	startcylinder	uint16

	Partitionid	uint8

	endhead		uint8
	endsector	uint8
	endcylinder	uint16

	Startlba	uint32
	length		uint32
}

func (self *TPartitiontableentry) Init(data [16]byte) {
	self.bootable = data[0]

	self.starthead = data[1]
	self.startsector = (data[2] >> 2)
	self.startcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.Partitionid = data[4]

	self.endhead = data[5]
	self.endsector = (data[6] >> 2)
	self.endcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Startlba = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.length = Unsignedinteger32r(Arraytounsignedinteger32(buffer2))
}

type TMasterbootrecord struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitiontableentry

	magicnumber	uint16
}
type Tmsdospartitiontable struct {
	Mbr TMasterbootrecord
}

func (self *Tmsdospartitiontable) Aqrapartition(hd *TAdvancedtechnologyattachment) {

	console_2 := TConsole{}
	console_2.MPrint(([]byte)("Reading MBR"))

	var partitionbytes [512]byte
	var buffer_2 = partitionbytes[:]
	hd.Aqra28(0, &buffer_2, 512)

	self.Mbr = TMasterbootrecord{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionbytes[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionbytes[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionbytes[i:i+2])
	self.Mbr.unused = Unsignedinteger16r(Arraytounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionbytes[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionbytes[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Arraytounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.MPrint(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
