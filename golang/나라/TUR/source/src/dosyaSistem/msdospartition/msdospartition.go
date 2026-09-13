package msdospartition

import . "konsol"
import . "util"

import . "driver/ata"

type TPartitionTablogirdi struct {
	bootable	uint8

	başlathead	uint8
	başlatsector	uint8
	başlatcylinder	uint16

	PartitionNo	uint8

	sonhead		uint8
	sonsector	uint8
	soncylinder	uint16

	Başlatlba	uint32
	süre		uint32
}

func (self *TPartitionTablogirdi) Init(data [16]byte) {
	self.bootable = data[0]

	self.başlathead = data[1]
	self.başlatsector = (data[2] >> 2)
	self.başlatcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.PartitionNo = data[4]

	self.sonhead = data[5]
	self.sonsector = (data[6] >> 2)
	self.soncylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Başlatlba = Unsignedinteger32r(Dizitounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.süre = Unsignedinteger32r(Dizitounsignedinteger32(buffer2))
}

type TAna_önyükleme_kaydı struct {
	bootloader	[440]byte
	signature	uint32
	kullanılmamış	uint16

	Primarypartition	[4]TPartitionTablogirdi

	magicnumber	uint16
}
type TmsdospartitionTablo struct {
	Mbr TAna_önyükleme_kaydı
}

func (self *TmsdospartitionTablo) Okumapartition(hd *TGelişmişTeknolojiattachment) {

	konsol_2 := TKonsol{}
	konsol_2.MYazdır(([]byte)("Reading MBR"))

	var partitionBayt [512]byte
	var buffer_2 = partitionBayt[:]
	hd.Okuma28(0, &buffer_2, 512)

	self.Mbr = TAna_önyükleme_kaydı{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionBayt[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionBayt[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Dizitounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionBayt[i:i+2])
	self.Mbr.kullanılmamış = Unsignedinteger16r(Dizitounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionBayt[i:i+16])
	self.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBayt[i:i+16])
	self.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBayt[i:i+16])
	self.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionBayt[i:i+16])
	self.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionBayt[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Dizitounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		konsol_2.MYazdır(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].PartitionNo == 0x00 {
			continue
		}

	}
}
