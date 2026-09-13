package msdosクブン

import . "コンソール"
import . "ハンヨウ"

import . "ドライバー/ata"

type Tクブンtableentry struct {
	bootable	uint8

	カイシhead		uint8
	カイシsector	uint8
	カイシcylinder	uint16

	Pクブンid	uint8

	ブンマツhead		uint8
	ブンマツsector	uint8
	ブンマツcylinder	uint16

	Sカイシlba	uint32
	ナガサ	uint32
}

func (self *Tクブンtableentry) Init(データ [16]byte) {
	self.bootable = データ[0]

	self.カイシhead = データ[1]
	self.カイシsector = (データ[2] >> 2)
	self.カイシcylinder = Unsignedinteger16r(uint16(データ[2]&0x03) | uint16(データ[3]))

	self.Pクブンid = データ[4]

	self.ブンマツhead = データ[5]
	self.ブンマツsector = (データ[6] >> 2)
	self.ブンマツcylinder = Unsignedinteger16r(uint16(データ[6]&0x03) | uint16(データ[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], データ[8:12])
	self.Sカイシlba = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], データ[12:16])
	self.ナガサ = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer2))
}

type Tシュキドウキロク struct {
	bootloader	[440]byte
	signature	uint32
	ミシヨウ		uint16

	Primaryクブン	[4]Tクブンtableentry

	magicnumber	uint16
}
type Tmsdosクブンtable struct {
	Mbr Tシュキドウキロク
}

func (self *Tmsdosクブンtable) Rヨミコミクブン(hd *Tショウサイシヨウギジュツattachment) {

	コンソール_2 := Tコンソール{}
	コンソール_2.Mインサツ(([]byte)("Reading MBR"))

	var クブンバイト [512]byte
	var buffer_2 = クブンバイト[:]
	hd.Rヨミコミ28(0, &buffer_2, 512)

	self.Mbr = Tシュキドウキロク{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = クブンバイト[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], クブンバイト[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], クブンバイト[i:i+2])
	self.Mbr.ミシヨウ = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], クブンバイト[i:i+16])
	self.Mbr.Primaryクブン[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], クブンバイト[i:i+16])
	self.Mbr.Primaryクブン[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], クブンバイト[i:i+16])
	self.Mbr.Primaryクブン[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], クブンバイト[i:i+16])
	self.Mbr.Primaryクブン[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], クブンバイト[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(Aハイレツtounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		コンソール_2.Mインサツ(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primaryクブン[i].Pクブンid == 0x00 {
			continue
		}

	}
}
