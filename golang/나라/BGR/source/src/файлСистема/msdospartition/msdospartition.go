package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionТаблицазапис struct {
	bootable	uint8

	стартиранеhead		uint8
	стартиранеsector	uint8
	стартиранеcylinder	uint16

	PartitionИДЕНТИФИКАТОР	uint8

	крайhead	uint8
	крайsector	uint8
	крайcylinder	uint16

	Стартиранеlba	uint32
	дължина		uint32
}

func (себеси *TPartitionТаблицазапис) Init(data [16]byte) {
	себеси.bootable = data[0]

	себеси.стартиранеhead = data[1]
	себеси.стартиранеsector = (data[2] >> 2)
	себеси.стартиранеcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	себеси.PartitionИДЕНТИФИКАТОР = data[4]

	себеси.крайhead = data[5]
	себеси.крайsector = (data[6] >> 2)
	себеси.крайcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	себеси.Стартиранеlba = Unsignedinteger32r(Масивtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	себеси.дължина = Unsignedinteger32r(Масивtounsignedinteger32(buffer2))
}

type TГлавенbootЗапис struct {
	bootloader	[440]byte
	signature	uint32
	неизползван	uint16

	Primarypartition	[4]TPartitionТаблицазапис

	magicnumber	uint16
}
type TmsdospartitionТаблица struct {
	Mbr TГлавенbootЗапис
}

func (себеси *TmsdospartitionТаблица) Четенеpartition(hd *TДопълнителниТехнологияattachment) {

	console_2 := TConsole{}
	console_2.MПечат(([]byte)("Reading MBR"))

	var partitionБайтове [512]byte
	var buffer_2 = partitionБайтове[:]
	hd.Четене28(0, &buffer_2, 512)

	себеси.Mbr = TГлавенbootЗапис{}
	var i int = 0
	for ; i < 440; i++ {
		себеси.Mbr.bootloader[i] = partitionБайтове[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionБайтове[i:i+4])
	себеси.Mbr.signature = Unsignedinteger32r(Масивtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionБайтове[i:i+2])
	себеси.Mbr.неизползван = Unsignedinteger16r(Масивtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionБайтове[i:i+16])
	себеси.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайтове[i:i+16])
	себеси.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайтове[i:i+16])
	себеси.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionБайтове[i:i+16])
	себеси.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionБайтове[i:i+2])
	себеси.Mbr.magicnumber = Unsignedinteger16r(Масивtounsignedinteger16(buffer6))

	if себеси.Mbr.magicnumber != 0xAA55 {
		console_2.MПечат(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if себеси.Mbr.Primarypartition[i].PartitionИДЕНТИФИКАТОР == 0x00 {
			continue
		}

	}
}
