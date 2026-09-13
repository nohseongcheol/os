package msdospartition

import . "konsol"
import . "util"

import . "driver/ata"

type TPartitionTabellpost struct {
	bootable	uint8

	startahead	uint8
	startasector	uint8
	startacylinder	uint16

	Partitionid	uint8

	sluthead	uint8
	slutsector	uint8
	slutcylinder	uint16

	Startalba	uint32
	längd		uint32
}

func (själv *TPartitionTabellpost) Init(data [16]byte) {
	själv.bootable = data[0]

	själv.startahead = data[1]
	själv.startasector = (data[2] >> 2)
	själv.startacylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	själv.Partitionid = data[4]

	själv.sluthead = data[5]
	själv.slutsector = (data[6] >> 2)
	själv.slutcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	själv.Startalba = Unsignedinteger32r(Vektortounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	själv.längd = Unsignedinteger32r(Vektortounsignedinteger32(buffer2))
}

type THuvudstartpost struct {
	bootloader	[440]byte
	signature	uint32
	oanvänt		uint16

	Primarypartition	[4]TPartitionTabellpost

	magicnumber	uint16
}
type TmsdospartitionTabell struct {
	Mbr THuvudstartpost
}

func (själv *TmsdospartitionTabell) Läspartition(hd *TAvanceratTeknikattachment) {

	konsol_2 := TKonsol{}
	konsol_2.MSkrivut(([]byte)("Reading MBR"))

	var partitionByte [512]byte
	var buffer_2 = partitionByte[:]
	hd.Läs28(0, &buffer_2, 512)

	själv.Mbr = THuvudstartpost{}
	var i int = 0
	for ; i < 440; i++ {
		själv.Mbr.bootloader[i] = partitionByte[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionByte[i:i+4])
	själv.Mbr.signature = Unsignedinteger32r(Vektortounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionByte[i:i+2])
	själv.Mbr.oanvänt = Unsignedinteger16r(Vektortounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionByte[i:i+16])
	själv.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	själv.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	själv.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	själv.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionByte[i:i+2])
	själv.Mbr.magicnumber = Unsignedinteger16r(Vektortounsignedinteger16(buffer6))

	if själv.Mbr.magicnumber != 0xAA55 {
		konsol_2.MSkrivut(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if själv.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
