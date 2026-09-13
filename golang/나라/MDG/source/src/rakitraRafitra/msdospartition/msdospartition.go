package msdospartition

import . "konsoly"
import . "util"

import . "driver/ata"

type TPartitionFafanaentry struct {
	bootable	uint8

	atomboyhead	uint8
	atomboysector	uint8
	atomboycylinder	uint16

	Partitionid	uint8

	endhead		uint8
	endsector	uint8
	endcylinder	uint16

	Atomboylba	uint32
	length		uint32
}

func (nytena *TPartitionFafanaentry) Init(data [16]byte) {
	nytena.bootable = data[0]

	nytena.atomboyhead = data[1]
	nytena.atomboysector = (data[2] >> 2)
	nytena.atomboycylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	nytena.Partitionid = data[4]

	nytena.endhead = data[5]
	nytena.endsector = (data[6] >> 2)
	nytena.endcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	nytena.Atomboylba = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	nytena.length = Unsignedinteger32r(Arraytounsignedinteger32(buffer2))
}

type TMasterbootrecord struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionFafanaentry

	magicnumber	uint16
}
type TmsdospartitionFafana struct {
	Mbr TMasterbootrecord
}

func (nytena *TmsdospartitionFafana) Mamakypartition(hd *TAvolentatechnologyattachment) {

	konsoly_2 := TKonsoly{}
	konsoly_2.MAtontay(([]byte)("Reading MBR"))

	var partitionOctet [512]byte
	var buffer_2 = partitionOctet[:]
	hd.Mamaky28(0, &buffer_2, 512)

	nytena.Mbr = TMasterbootrecord{}
	var i int = 0
	for ; i < 440; i++ {
		nytena.Mbr.bootloader[i] = partitionOctet[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionOctet[i:i+4])
	nytena.Mbr.signature = Unsignedinteger32r(Arraytounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionOctet[i:i+2])
	nytena.Mbr.unused = Unsignedinteger16r(Arraytounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionOctet[i:i+16])
	nytena.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOctet[i:i+16])
	nytena.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOctet[i:i+16])
	nytena.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionOctet[i:i+16])
	nytena.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionOctet[i:i+2])
	nytena.Mbr.magicnumber = Unsignedinteger16r(Arraytounsignedinteger16(buffer6))

	if nytena.Mbr.magicnumber != 0xAA55 {
		konsoly_2.MAtontay(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if nytena.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
