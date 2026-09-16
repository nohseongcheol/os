/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTabelItem struct {
	bootable	uint8

	startenhead	uint8
	startensector	uint8
	startencylinder	uint16

	Partitionid	uint8

	eindhead	uint8
	eindsector	uint8
	eindcylinder	uint16

	Startenlba	uint32
	lengte		uint32
}

func (zelf *TPartitionTabelItem) Init(data [16]byte) {
	zelf.bootable = data[0]

	zelf.startenhead = data[1]
	zelf.startensector = (data[2] >> 2)
	zelf.startencylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	zelf.Partitionid = data[4]

	zelf.eindhead = data[5]
	zelf.eindsector = (data[6] >> 2)
	zelf.eindcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	zelf.Startenlba = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	zelf.lengte = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer2))
}

type THoofdopstartrecord struct {
	bootloader	[440]byte
	signature	uint32
	ongebruikt	uint16

	Primarypartition	[4]TPartitionTabelItem

	magicnumber	uint16
}
type TmsdospartitionTabel struct {
	Mbr THoofdopstartrecord
}

func (zelf *TmsdospartitionTabel) Lezenpartition(hd *TGeavanceerdTechnologieattachment) {

	console_2 := TConsole{}
	console_2.MAfdrukken(([]byte)("Reading MBR"))

	var partitionbytes [512]byte
	var buffer_2 = partitionbytes[:]
	hd.Lezen28(0, &buffer_2, 512)

	zelf.Mbr = THoofdopstartrecord{}
	var i int = 0
	for ; i < 440; i++ {
		zelf.Mbr.bootloader[i] = partitionbytes[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionbytes[i:i+4])
	zelf.Mbr.signature = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionbytes[i:i+2])
	zelf.Mbr.ongebruikt = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionbytes[i:i+16])
	zelf.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	zelf.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	zelf.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	zelf.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionbytes[i:i+2])
	zelf.Mbr.magicnumber = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer6))

	if zelf.Mbr.magicnumber != 0xAA55 {
		console_2.MAfdrukken(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if zelf.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
