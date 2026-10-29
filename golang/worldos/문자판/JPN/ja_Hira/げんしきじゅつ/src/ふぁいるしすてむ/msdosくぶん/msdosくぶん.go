/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdosくぶん

import . "こんそーる"
import . "はんよう"

import . "どらいばー/ata"

type Tくぶんtableentry struct {
	bootable	uint8

	かいしhead		uint8
	かいしsector	uint8
	かいしcylinder	uint16

	Pくぶんid	uint8

	ぶんまつhead		uint8
	ぶんまつsector	uint8
	ぶんまつcylinder	uint16

	Sかいしlba	uint32
	ながさ	uint32
}

func (self *Tくぶんtableentry) Init(でーた [16]byte) {
	self.bootable = でーた[0]

	self.かいしhead = でーた[1]
	self.かいしsector = (でーた[2] >> 2)
	self.かいしcylinder = Unsignedinteger16r(uint16(でーた[2]&0x03) | uint16(でーた[3]))

	self.Pくぶんid = でーた[4]

	self.ぶんまつhead = でーた[5]
	self.ぶんまつsector = (でーた[6] >> 2)
	self.ぶんまつcylinder = Unsignedinteger16r(uint16(でーた[6]&0x03) | uint16(でーた[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], でーた[8:12])
	self.Sかいしlba = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], でーた[12:16])
	self.ながさ = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer2))
}

type Tしゅきどうきろく struct {
	bootloader	[440]byte
	signature	uint32
	みしよう		uint16

	Primaryくぶん	[4]Tくぶんtableentry

	magicnumber	uint16
}
type Tmsdosくぶんtable struct {
	Mbr Tしゅきどうきろく
}

func (self *Tmsdosくぶんtable) Rよみこみくぶん(hd *Tしょうさいしようぎじゅつattachment) {

	こんそーる_2 := Tこんそーる{}
	こんそーる_2.Mいんさつ(([]byte)("Reading MBR"))

	var くぶんばいと [512]byte
	var buffer_2 = くぶんばいと[:]
	hd.Rよみこみ28(0, &buffer_2, 512)

	self.Mbr = Tしゅきどうきろく{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = くぶんばいと[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], くぶんばいと[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], くぶんばいと[i:i+2])
	self.Mbr.みしよう = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], くぶんばいと[i:i+16])
	self.Mbr.Primaryくぶん[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], くぶんばいと[i:i+16])
	self.Mbr.Primaryくぶん[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], くぶんばいと[i:i+16])
	self.Mbr.Primaryくぶん[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], くぶんばいと[i:i+16])
	self.Mbr.Primaryくぶん[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], くぶんばいと[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Aはいれつtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		こんそーる_2.Mいんさつ(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primaryくぶん[i].Pくぶんid == 0x00 {
			continue
		}

	}
}
