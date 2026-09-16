/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdospartition

import . "console"
import . "util"

import . "driver/ata"

type TPartitionجدولentry struct {
	bootable	uint8

	starthead	uint8
	startsector	uint8
	startcylinder	uint16

	Partitionشناسه	uint8

	پایانhead	uint8
	پایانsector	uint8
	پایانcylinder	uint16

	Startlba	uint32
	طول		uint32
}

func (خود *TPartitionجدولentry) Init(data [16]byte) {
	خود.bootable = data[0]

	خود.starthead = data[1]
	خود.startsector = (data[2] >> 2)
	خود.startcylinder = Unsignedinteger16r(uint16(data[2]&0x03) | uint16(data[3]))

	خود.Partitionشناسه = data[4]

	خود.پایانhead = data[5]
	خود.پایانsector = (data[6] >> 2)
	خود.پایانcylinder = Unsignedinteger16r(uint16(data[6]&0x03) | uint16(data[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], data[8:12])
	خود.Startlba = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], data[12:16])
	خود.طول = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer2))
}

type Tاصلیbootضبط struct {
	bootloader	[440]byte
	signature	uint32
	unused		uint16

	Primarypartition	[4]TPartitionجدولentry

	magicnumber	uint16
}
type Tmsdospartitionجدول struct {
	Mbr Tاصلیbootضبط
}

func (خود *Tmsdospartitionجدول) Rخواندنpartition(hd *Tپیشرفتهtechnologyattachment) {

	console_2 := TConsole{}
	console_2.Mچاپ(([]byte)("Reading MBR"))

	var partitionبایت [512]byte
	var buffer_2 = partitionبایت[:]
	hd.Rخواندن28(0, &buffer_2, 512)

	خود.Mbr = Tاصلیbootضبط{}
	var i int = 0
	for ; i < 440; i++ {
		خود.Mbr.bootloader[i] = partitionبایت[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], partitionبایت[i:i+4])
	خود.Mbr.signature = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], partitionبایت[i:i+2])
	خود.Mbr.unused = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], partitionبایت[i:i+16])
	خود.Mbr.Primarypartition[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionبایت[i:i+16])
	خود.Mbr.Primarypartition[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionبایت[i:i+16])
	خود.Mbr.Primarypartition[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], partitionبایت[i:i+16])
	خود.Mbr.Primarypartition[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], partitionبایت[i:i+2])
	خود.Mbr.magicnumber = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer6))

	if خود.Mbr.magicnumber != 0xAA55 {
		console_2.Mچاپ(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if خود.Mbr.Primarypartition[i].Partitionشناسه == 0x00 {
			continue
		}

	}
}
