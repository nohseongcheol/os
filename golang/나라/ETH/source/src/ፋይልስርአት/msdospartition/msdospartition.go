package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionሰንጠረዥentry struct {
	bootable	uint8

	ማስጀመሪያhead	uint8
	ማስጀመሪያsector	uint8
	ማስጀመሪያcylinder	uint16

	Partitionመለያ	uint8

	መጨረሻhead	uint8
	መጨረሻsector	uint8
	መጨረሻcylinder	uint16

	Sማስጀመሪያlba	uint32
	እርዝመት_2		uint32
}

func (self *TPartitionሰንጠረዥentry) Init(data [16]byte) {
	self.bootable = data[0]

	self.ማስጀመሪያhead = data[1]
	self.ማስጀመሪያsector = (data[2] >> 2)
	self.ማስጀመሪያcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.Partitionመለያ = data[4]

	self.መጨረሻhead = data[5]
	self.መጨረሻsector = (data[6] >> 2)
	self.መጨረሻcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Sማስጀመሪያlba = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.እርዝመት_2 = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer2))
}

type Tዋናውbootመቅረጫ struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionሰንጠረዥentry

	magicnumber	uint16
}
type Tmsdospartitionሰንጠረዥ struct {
	Mbr Tዋናውbootመቅረጫ
}

func (self *Tmsdospartitionሰንጠረዥ) Rማንበቢያpartition(hd *Tጠለቅቴክኖሎጂattachment) {

	console_2 := TConsole{}
	console_2.Mማተሚያ(([]byte)("Reading MBR"))

	var partitionባይትስ [512]byte
	var buffer_2 = partitionባይትስ[:]
	hd.Rማንበቢያ28(0, &buffer_2, 512)

	self.Mbr = Tዋናውbootመቅረጫ{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionባይትስ[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionባይትስ[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionባይትስ[i:i+2])
	self.Mbr.unused = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionባይትስ[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionባይትስ[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionባይትስ[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionባይትስ[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionባይትስ[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.Mማተሚያ(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].Partitionመለያ == 0x00 {
			continue
		}

	}
}
