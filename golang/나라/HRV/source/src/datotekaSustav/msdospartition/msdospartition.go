package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTablicaentry struct {
	bootable	uint8

	pokrenihead	uint8
	pokrenisector	uint8
	pokrenicylinder	uint16

	PartitionIdentifikacija	uint8

	krajhead	uint8
	krajsector	uint8
	krajcylinder	uint16

	Pokrenilba	uint32
	dužina		uint32
}

func (sam *TPartitionTablicaentry) Init(data [16]byte) {
	sam.bootable = data[0]

	sam.pokrenihead = data[1]
	sam.pokrenisector = (data[2] >> 2)
	sam.pokrenicylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	sam.PartitionIdentifikacija = data[4]

	sam.krajhead = data[5]
	sam.krajsector = (data[6] >> 2)
	sam.krajcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	sam.Pokrenilba = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	sam.dužina = Unsignedinteger32r(Niztounsignedinteger32(buffer2))
}

type TMasterbootSnimaj struct {
	bootloader	[440]byte
	signature	uint32
	nekorišteno	uint16

	Primarypartition	[4]TPartitionTablicaentry

	magicnumber	uint16
}
type TmsdospartitionTablica struct {
	Mbr TMasterbootSnimaj
}

func (sam *TmsdospartitionTablica) Čitajpartition(hd *TNaprednoTehnologijaattachment) {

	console_2 := TConsole{}
	console_2.MIspis(([]byte)("Reading MBR"))

	var partitionBajtova [512]byte
	var buffer_2 = partitionBajtova[:]
	hd.Čitaj28(0, &buffer_2, 512)

	sam.Mbr = TMasterbootSnimaj{}
	var i int = 0
	for ; i < 440; i++ {
		sam.Mbr.bootloader[i] = partitionBajtova[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBajtova[i:i+4])
	sam.Mbr.signature = Unsignedinteger32r(Niztounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBajtova[i:i+2])
	sam.Mbr.nekorišteno = Unsignedinteger16r(Niztounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBajtova[i:i+16])
	sam.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtova[i:i+16])
	sam.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtova[i:i+16])
	sam.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtova[i:i+16])
	sam.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBajtova[i:i+2])
	sam.Mbr.magicnumber = Unsignedinteger16r(Niztounsignedinteger16(buffer6))

	if sam.Mbr.magicnumber != 0xAA55 {
		console_2.MIspis(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if sam.Mbr.Primarypartition[i].PartitionIdentifikacija == 0x00 {
			continue
		}

	}
}
