/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "konsolë"
import . "util"

import . "driver/ata"

type TPartitionTabelaentry struct {
	bootable	uint8

	fillohead	uint8
	fillosector	uint8
	fillocylinder	uint16

	Partitionid	uint8

	fundhead	uint8
	fundsector	uint8
	fundcylinder	uint16

	Fillolba	uint32
	gjatësi		uint32
}

func (vetvetja *TPartitionTabelaentry) Init(data [16]byte) {
	vetvetja.bootable = data[0]

	vetvetja.fillohead = data[1]
	vetvetja.fillosector = (data[2] >> 2)
	vetvetja.fillocylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	vetvetja.Partitionid = data[4]

	vetvetja.fundhead = data[5]
	vetvetja.fundsector = (data[6] >> 2)
	vetvetja.fundcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	vetvetja.Fillolba = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	vetvetja.gjatësi = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer2))
}

type TMasterNisjarecord struct {
	nisjaloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionTabelaentry

	magicnumber	uint16
}
type TmsdospartitionTabela struct {
	Mbr TMasterNisjarecord
}

func (vetvetja *TmsdospartitionTabela) Leximipartition(hd *TTëmëtejshmetechnologyattachment) {

	konsolë_2 := TKonsolë{}
	konsolë_2.MPrinto(([]byte)("Reading MBR"))

	var partitionbytes [512]byte
	var buffer_2 = partitionbytes[:]
	hd.Leximi28(0, &buffer_2, 512)

	vetvetja.Mbr = TMasterNisjarecord{}
	var i int = 0
	for ; i < 440; i++ {
		vetvetja.Mbr.nisjaloader[i] = partitionbytes[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionbytes[i:i+4])
	vetvetja.Mbr.signature = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionbytes[i:i+2])
	vetvetja.Mbr.unused = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionbytes[i:i+16])
	vetvetja.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	vetvetja.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	vetvetja.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionbytes[i:i+16])
	vetvetja.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionbytes[i:i+2])
	vetvetja.Mbr.magicnumber = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer6))

	if vetvetja.Mbr.magicnumber != 0xAA55 {
		konsolë_2.MPrinto(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if vetvetja.Mbr.Primarypartition[i].Partitionid == 0x00 {
			continue
		}

	}
}
