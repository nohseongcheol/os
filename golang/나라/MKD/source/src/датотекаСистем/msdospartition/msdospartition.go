package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionТабелаentry struct {
	bootable	uint8

	пуштиhead	uint8
	пуштиsector	uint8
	пуштиcylinder	uint16

	PartitionИд	uint8

	endhead		uint8
	endsector	uint8
	endcylinder	uint16

	Пуштиlba	uint32
	должина		uint32
}

func (само *TPartitionТабелаentry) Init(data [16]byte) {
	само.bootable = data[0]

	само.пуштиhead = data[1]
	само.пуштиsector = (data[2] >> 2)
	само.пуштиcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	само.PartitionИд = data[4]

	само.endhead = data[5]
	само.endsector = (data[6] >> 2)
	само.endcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	само.Пуштиlba = Unsignedinteger32r(Построиtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	само.должина = Unsignedinteger32r(Построиtounsignedinteger32(buffer2))
}

type TMasterbootrecord struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionТабелаentry

	magicnumber	uint16
}
type TmsdospartitionТабела struct {
	Mbr TMasterbootrecord
}

func (само *TmsdospartitionТабела) Читајpartition(hd *TНапредноtechnologyattachment) {

	console_2 := TConsole{}
	console_2.MПечати(([]byte)("Reading MBR"))

	var partitionбајти [512]byte
	var buffer_2 = partitionбајти[:]
	hd.Читај28(0, &buffer_2, 512)

	само.Mbr = TMasterbootrecord{}
	var i int = 0
	for ; i < 440; i++ {
		само.Mbr.bootloader[i] = partitionбајти[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionбајти[i:i+4])
	само.Mbr.signature = Unsignedinteger32r(Построиtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionбајти[i:i+2])
	само.Mbr.unused = Unsignedinteger16r(Построиtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionбајти[i:i+16])
	само.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionбајти[i:i+16])
	само.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionбајти[i:i+16])
	само.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionбајти[i:i+16])
	само.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionбајти[i:i+2])
	само.Mbr.magicnumber = Unsignedinteger16r(Построиtounsignedinteger16(buffer6))

	if само.Mbr.magicnumber != 0xAA55 {
		console_2.MПечати(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if само.Mbr.Primarypartition[i].PartitionИд == 0x00 {
			continue
		}

	}
}
