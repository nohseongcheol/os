package msdospartition

import . "konzola"
import . "util"

import . "driver/ata"

type TPartitionTabelaunos struct {
	bootable	uint8

	pokrenihead	uint8
	pokrenisector	uint8
	pokrenicylinder	uint16

	PartitionIB	uint8

	krajhead	uint8
	krajsector	uint8
	krajcylinder	uint16

	Pokrenilba	uint32
	dužina		uint32
}

func (isti *TPartitionTabelaunos) Init(data [16]byte) {
	isti.bootable = data[0]

	isti.pokrenihead = data[1]
	isti.pokrenisector = (data[2] >> 2)
	isti.pokrenicylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	isti.PartitionIB = data[4]

	isti.krajhead = data[5]
	isti.krajsector = (data[6] >> 2)
	isti.krajcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	isti.Pokrenilba = Unsignedinteger32r(Niztounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	isti.dužina = Unsignedinteger32r(Niztounsignedinteger32(buffer2))
}

type TGlavnibootSnimanje struct {
	bootloader	[440]byte
	signature	uint32
	neupotrebljen	uint16

	Primarypartition	[4]TPartitionTabelaunos

	magicnumber	uint16
}
type TmsdospartitionTabela struct {
	Mbr TGlavnibootSnimanje
}

func (isti *TmsdospartitionTabela) Čitanjepartition(hd *TNaprednoTehnologijaattachment) {

	konzola_2 := TKonzola{}
	konzola_2.MŠtampaj(([]byte)("Reading MBR"))

	var partitionBajtova [512]byte
	var buffer_2 = partitionBajtova[:]
	hd.Čitanje28(0, &buffer_2, 512)

	isti.Mbr = TGlavnibootSnimanje{}
	var i int = 0
	for ; i < 440; i++ {
		isti.Mbr.bootloader[i] = partitionBajtova[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBajtova[i:i+4])
	isti.Mbr.signature = Unsignedinteger32r(Niztounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBajtova[i:i+2])
	isti.Mbr.neupotrebljen = Unsignedinteger16r(Niztounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBajtova[i:i+16])
	isti.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtova[i:i+16])
	isti.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtova[i:i+16])
	isti.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBajtova[i:i+16])
	isti.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBajtova[i:i+2])
	isti.Mbr.magicnumber = Unsignedinteger16r(Niztounsignedinteger16(buffer6))

	if isti.Mbr.magicnumber != 0xAA55 {
		konzola_2.MŠtampaj(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if isti.Mbr.Primarypartition[i].PartitionIB == 0x00 {
			continue
		}

	}
}
