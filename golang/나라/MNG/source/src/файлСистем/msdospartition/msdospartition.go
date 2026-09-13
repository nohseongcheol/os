package msdospartition

import . "консол"
import . "util"

import . "driver/ata"

type TPartitiontableentry struct {
	bootable	uint8

	эхлэлhead	uint8
	эхлэлsector	uint8
	эхлэлcylinder	uint16

	PartitionДугаар	uint8

	endhead		uint8
	endsector	uint8
	endcylinder	uint16

	Эхлэлlba	uint32
	length		uint32
}

func (self *TPartitiontableentry) Init(data [16]byte) {
	self.bootable = data[0]

	self.эхлэлhead = data[1]
	self.эхлэлsector = (data[2] >> 2)
	self.эхлэлcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.PartitionДугаар = data[4]

	self.endhead = data[5]
	self.endsector = (data[6] >> 2)
	self.endcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Эхлэлlba = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.length = Unsignedinteger32r(Arraytounsignedinteger32(buffer2))
}

type TMasterЭхлүүлэлrecord struct {
	эхлүүлэлloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitiontableentry

	magicnumber	uint16
}
type Tmsdospartitiontable struct {
	Mbr TMasterЭхлүүлэлrecord
}

func (self *Tmsdospartitiontable) Уншихpartition(hd *TӨргөтгөсөнtechnologyattachment) {

	консол_2 := TКонсол{}
	консол_2.MХэвлэх(([]byte)("Reading MBR"))

	var partitionБайт [512]byte
	var buffer_2 = partitionБайт[:]
	hd.Унших28(0, &buffer_2, 512)

	self.Mbr = TMasterЭхлүүлэлrecord{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.эхлүүлэлloader[i] = partitionБайт[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionБайт[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionБайт[i:i+2])
	self.Mbr.unused = Unsignedinteger16r(Arraytounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionБайт[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайт[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайт[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайт[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionБайт[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Arraytounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		консол_2.MХэвлэх(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].PartitionДугаар == 0x00 {
			continue
		}

	}
}
