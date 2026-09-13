package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionΠίνακαςκαταχώρηση struct {
	bootable	uint8

	έναρξηhead	uint8
	έναρξηsector	uint8
	έναρξηcylinder	uint16

	PartitionΤΑΥΤΌΤΗΤΑ	uint8

	τέλοςhead	uint8
	τέλοςsector	uint8
	τέλοςcylinder	uint16

	Έναρξηlba	uint32
	διάρκεια	uint32
}

func (self *TPartitionΠίνακαςκαταχώρηση) Init(data [16]byte) {
	self.bootable = data[0]

	self.έναρξηhead = data[1]
	self.έναρξηsector = (data[2] >> 2)
	self.έναρξηcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.PartitionΤΑΥΤΌΤΗΤΑ = data[4]

	self.τέλοςhead = data[5]
	self.τέλοςsector = (data[6] >> 2)
	self.τέλοςcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Έναρξηlba = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.διάρκεια = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer2))
}

type TΚύριαέξοδοςbootΗχογράφηση struct {
	bootloader	[440]byte
	signature	uint32
	αχρησιμοποίητο	uint16

	Primarypartition	[4]TPartitionΠίνακαςκαταχώρηση

	magicnumber	uint16
}
type TmsdospartitionΠίνακας struct {
	Mbr TΚύριαέξοδοςbootΗχογράφηση
}

func (self *TmsdospartitionΠίνακας) Ανάγνωσηpartition(hd *TΓιαπροχωρημένουςΤεχνολογίαattachment) {

	console_2 := TConsole{}
	console_2.MΕκτύπωση(([]byte)("Reading MBR"))

	var partitionbytes [512]byte
	var buffer_2 = partitionbytes[:]
	hd.Ανάγνωση28(0, &buffer_2, 512)

	self.Mbr = TΚύριαέξοδοςbootΗχογράφηση{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionbytes[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionbytes[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionbytes[i:i+2])
	self.Mbr.αχρησιμοποίητο = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer2))
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
	self.Mbr.magicnumber = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.MΕκτύπωση(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].PartitionΤΑΥΤΌΤΗΤΑ == 0x00 {
			continue
		}

	}
}
