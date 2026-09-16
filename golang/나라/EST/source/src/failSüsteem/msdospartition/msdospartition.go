/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionTabelkirje struct {
	bootable	uint8

	käivitahead	uint8
	käivitasector	uint8
	käivitacylinder	uint16

	Partitionid	uint8

	lõpphead	uint8
	lõppsector	uint8
	lõppcylinder	uint16

	Käivitalba	uint32
	kestus		uint32
}

func (ise *TPartitionTabelkirje) Init(data [16]byte) {
	ise.bootable = data[0]

	ise.käivitahead = data[1]
	ise.käivitasector = (data[2] >> 2)
	ise.käivitacylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	ise.Partitionid = data[4]

	ise.lõpphead = data[5]
	ise.lõppsector = (data[6] >> 2)
	ise.lõppcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	ise.Käivitalba = Unsignedinteger32r(Massiivtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	ise.kestus = Unsignedinteger32r(Massiivtounsignedinteger32(buffer2))
}

type TValjusbootSalvesta struct {
	bootloader	[440]byte
	signature	uint32
	kasutamata	uint16

	Primarypartition	[4]TPartitionTabelkirje

	magicnumber	uint16
}
type TmsdospartitionTabel struct {
	Mbr TValjusbootSalvesta
}

func (ise *TmsdospartitionTabel) Lugeminepartition(hd *TLaiendatudTehnoloogiaattachment) {

	console_2 := TConsole{}
	console_2.MPrindi(([]byte)("Reading MBR"))

	var partitionbaiti [512]byte
	var buffer_2 = partitionbaiti[:]
	hd.Lugemine28(0, &buffer_2, 512)

	ise.Mbr = TValjusbootSalvesta{}
	var i int = 0
	for ; i < 440; i++ {
		ise.Mbr.bootloader[i] = partitionbaiti[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionbaiti[i:i+4])
	ise.Mbr.signature = Unsignedinteger32r(Massiivtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionbaiti[i:i+2])
	ise.Mbr.kasutamata = Unsignedinteger16r(Massiivtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionbaiti[i:i+16])
	ise.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbaiti[i:i+16])
	ise.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbaiti[i:i+16])
	ise.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbaiti[i:i+16])
	ise.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionbaiti[i:i+2])
	ise.Mbr.magicnumber = Unsignedinteger16r(Massiivtounsignedinteger16(buffer6))

	if ise.Mbr.magicnumber != 0xAA55 {
		console_2.MPrindi(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if ise.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
