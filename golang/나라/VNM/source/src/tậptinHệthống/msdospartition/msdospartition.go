/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionBảngentry struct {
	bootable	uint8

	chạyhead	uint8
	chạysector	uint8
	chạycylinder	uint16

	PartitionMãsố	uint8

	kếtthúchead	uint8
	kếtthúcsector	uint8
	kếtthúccylinder	uint16

	Chạylba	uint32
	độdài	uint32
}

func (mình *TPartitionBảngentry) Init(data [16]byte) {
	mình.bootable = data[0]

	mình.chạyhead = data[1]
	mình.chạysector = (data[2] >> 2)
	mình.chạycylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	mình.PartitionMãsố = data[4]

	mình.kếtthúchead = data[5]
	mình.kếtthúcsector = (data[6] >> 2)
	mình.kếtthúccylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	mình.Chạylba = Unsignedinteger32r(Mảngtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	mình.độdài = Unsignedinteger32r(Mảngtounsignedinteger32(buffer2))
}

type TBản_ghi_khởi_động_chính struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionBảngentry

	magicnumber	uint16
}
type TmsdospartitionBảng struct {
	Mbr TBản_ghi_khởi_động_chính
}

func (mình *TmsdospartitionBảng) Đọcpartition(hd *TNângcaoCôngnghệattachment) {

	console_2 := TConsole{}
	console_2.MIn(([]byte)("Reading MBR"))

	var partitionByte [512]byte
	var buffer_2 = partitionByte[:]
	hd.Đọc28(0, &buffer_2, 512)

	mình.Mbr = TBản_ghi_khởi_động_chính{}
	var i int = 0
	for ; i < 440; i++ {
		mình.Mbr.bootloader[i] = partitionByte[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionByte[i:i+4])
	mình.Mbr.signature = Unsignedinteger32r(Mảngtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionByte[i:i+2])
	mình.Mbr.unused = Unsignedinteger16r(Mảngtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionByte[i:i+16])
	mình.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	mình.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	mình.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionByte[i:i+16])
	mình.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionByte[i:i+2])
	mình.Mbr.magicnumber = Unsignedinteger16r(Mảngtounsignedinteger16(buffer6))

	if mình.Mbr.magicnumber != 0xAA55 {
		console_2.MIn(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if mình.Mbr.Primarypartition[i].PartitionMãsố == 0x00 {
			continue
		}

	}
}
