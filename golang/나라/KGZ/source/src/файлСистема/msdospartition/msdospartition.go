package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionЖадыбалentry struct {
	bootable	uint8

	жүргүзүүhead		uint8
	жүргүзүүsector		uint8
	жүргүзүүcylinder	uint16

	PartitionИДЕНТИФИКАТОР	uint8

	endhead		uint8
	endsector	uint8
	endcylinder	uint16

	Жүргүзүүlba	uint32
	узундук		uint32
}

func (self *TPartitionЖадыбалentry) Init(data [16]byte) {
	self.bootable = data[0]

	self.жүргүзүүhead = data[1]
	self.жүргүзүүsector = (data[2] >> 2)
	self.жүргүзүүcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	self.PartitionИДЕНТИФИКАТОР = data[4]

	self.endhead = data[5]
	self.endsector = (data[6] >> 2)
	self.endcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	self.Жүргүзүүlba = Unsignedinteger32r(Массивtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	self.узундук = Unsignedinteger32r(Массивtounsignedinteger32(buffer2))
}

type TMasterbootrecord struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionЖадыбалentry

	magicnumber	uint16
}
type TmsdospartitionЖадыбал struct {
	Mbr TMasterbootrecord
}

func (self *TmsdospartitionЖадыбал) Окууpartition(hd *TКеңейтилгенТехнологияattachment) {

	console_2 := TConsole{}
	console_2.MБасма(([]byte)("Reading MBR"))

	var partitionБайт [512]byte
	var buffer_2 = partitionБайт[:]
	hd.Окуу28(0, &buffer_2, 512)

	self.Mbr = TMasterbootrecord{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = partitionБайт[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionБайт[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Массивtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionБайт[i:i+2])
	self.Mbr.unused = Unsignedinteger16r(Массивtounsignedinteger16(buffer2))
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
	self.Mbr.magicnumber = Unsignedinteger16r(Массивtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		console_2.MБасма(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primarypartition[i].PartitionИДЕНТИФИКАТОР == 0x00 {
			continue
		}

	}
}
