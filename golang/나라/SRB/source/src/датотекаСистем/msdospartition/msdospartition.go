package msdospartition

import . "конзола"
import . "util"

import . "driver/ata"

type TPartitionТабелаунос struct {
	bootable	uint8

	покрениhead	uint8
	покрениsector	uint8
	покрениcylinder	uint16

	PartitionИБ	uint8

	krajhead	uint8
	krajsector	uint8
	krajcylinder	uint16

	Покрениlba	uint32
	дужина		uint32
}

func (исти *TPartitionТабелаунос) Init(data [16]byte) {
	исти.bootable = data[0]

	исти.покрениhead = data[1]
	исти.покрениsector = (data[2] >> 2)
	исти.покрениcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	исти.PartitionИБ = data[4]

	исти.krajhead = data[5]
	исти.krajsector = (data[6] >> 2)
	исти.krajcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	исти.Покрениlba = Unsignedinteger32r(Низtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	исти.дужина = Unsignedinteger32r(Низtounsignedinteger32(buffer2))
}

type TГлавниbootСнимање struct {
	bootloader	[440]byte
	signature	uint32
	неупотребљен	uint16

	Primarypartition	[4]TPartitionТабелаунос

	magicnumber	uint16
}
type TmsdospartitionТабела struct {
	Mbr TГлавниbootСнимање
}

func (исти *TmsdospartitionТабела) Читањеpartition(hd *TНапредноТехнологијаattachment) {

	конзола_2 := TКонзола{}
	конзола_2.MШтампај(([]byte)("Reading MBR"))

	var partitionБајтова [512]byte
	var buffer_2 = partitionБајтова[:]
	hd.Читање28(0, &buffer_2, 512)

	исти.Mbr = TГлавниbootСнимање{}
	var i int = 0
	for ; i < 440; i++ {
		исти.Mbr.bootloader[i] = partitionБајтова[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionБајтова[i:i+4])
	исти.Mbr.signature = Unsignedinteger32r(Низtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionБајтова[i:i+2])
	исти.Mbr.неупотребљен = Unsignedinteger16r(Низtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionБајтова[i:i+16])
	исти.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБајтова[i:i+16])
	исти.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБајтова[i:i+16])
	исти.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБајтова[i:i+16])
	исти.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionБајтова[i:i+2])
	исти.Mbr.magicnumber = Unsignedinteger16r(Низtounsignedinteger16(buffer6))

	if исти.Mbr.magicnumber != 0xAA55 {
		конзола_2.MШтампај(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if исти.Mbr.Primarypartition[i].PartitionИБ == 0x00 {
			continue
		}

	}
}
