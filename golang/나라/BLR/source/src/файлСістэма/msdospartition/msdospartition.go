package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionТабліцаentry struct {
	bootable	uint8

	уключыцьhead		uint8
	уключыцьsector		uint8
	уключыцьcylinder	uint16

	PartitionІДЭНТЫФІКАТАР	uint8

	канецhead	uint8
	канецsector	uint8
	канецcylinder	uint16

	Уключыцьlba	uint32
	даўжыня		uint32
}

func (self *TPartitionТабліцаentry) Init(data [16]byte) {
	self.bootable = data[0]

	self.уключыцьhead = data[1]
	self.уключыцьsector = (data[2] >> 2)
	self.уключыцьcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.PartitionІДЭНТЫФІКАТАР = data[4]

	self.канецhead = data[5]
	self.канецsector = (data[6] >> 2)
	self.канецcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Уключыцьlba = Unsignedinteger32r(Масіўtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.даўжыня = Unsignedinteger32r(Масіўtounsignedinteger32(buffer2))
}

type TАгульныbootЗапіс struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionТабліцаentry

	magicnumber	uint16
}
type TmsdospartitionТабліца struct {
	Mbr TАгульныbootЗапіс
}

func (self *TmsdospartitionТабліца) Чытаннеpartition(hd *TДадатковаТэхналогіяattachment) {

	console_2 := TConsole{}
	console_2.MДрукаваць(([]byte)("Reading MBR"))

	var partitionБайтаў [512]byte
	var buffer_2 = partitionБайтаў[:]
	hd.Чытанне28(0, &buffer_2, 512)

	self.Mbr = TАгульныbootЗапіс{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionБайтаў[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionБайтаў[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Масіўtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionБайтаў[i:i+2])
	self.Mbr.unused = Unsignedinteger16r(Масіўtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionБайтаў[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайтаў[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайтаў[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайтаў[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionБайтаў[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Масіўtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.MДрукаваць(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].PartitionІДЭНТЫФІКАТАР == 0x00 {
			continue
		}

	}
}
