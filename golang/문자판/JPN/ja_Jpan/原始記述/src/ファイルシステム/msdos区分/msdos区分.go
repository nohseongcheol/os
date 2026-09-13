package msdos区分

import . "コンソール"
import . "汎用"

import . "ドライバー/ata"

type T区分tableentry struct {
	bootable	uint8

	開始head		uint8
	開始sector	uint8
	開始cylinder	uint16

	P区分id	uint8

	文末head		uint8
	文末sector	uint8
	文末cylinder	uint16

	S開始lba	uint32
	長さ	uint32
}

func (self *T区分tableentry) Init(データ [16]byte) {
	self.bootable = データ[0]

	self.開始head = データ[1]
	self.開始sector = (データ[2] >> 2)
	self.開始cylinder = Unsignedinteger16r(uint16(データ[2]&0x03) | uint16(データ[3]))

	self.P区分id = データ[4]

	self.文末head = データ[5]
	self.文末sector = (データ[6] >> 2)
	self.文末cylinder = Unsignedinteger16r(uint16(データ[6]&0x03) | uint16(データ[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], データ[8:12])
	self.S開始lba = Unsignedinteger32r(A配列tounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], データ[12:16])
	self.長さ = Unsignedinteger32r(A配列tounsignedinteger32(buffer2))
}

type T主起動記録 struct {
	bootloader	[440]byte
	signature	uint32
	未使用		uint16

	Primary区分	[4]T区分tableentry

	magicnumber	uint16
}
type Tmsdos区分table struct {
	Mbr T主起動記録
}

func (self *Tmsdos区分table) R読込み区分(hd *T詳細使用技術attachment) {

	コンソール_2 := Tコンソール{}
	コンソール_2.M印刷(([]byte)("Reading MBR"))

	var 区分バイト [512]byte
	var buffer_2 = 区分バイト[:]
	hd.R読込み28(0, &buffer_2, 512)

	self.Mbr = T主起動記録{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = 区分バイト[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], 区分バイト[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(A配列tounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], 区分バイト[i:i+2])
	self.Mbr.未使用 = Unsignedinteger16r(A配列tounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], 区分バイト[i:i+16])
	self.Mbr.Primary区分[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], 区分バイト[i:i+16])
	self.Mbr.Primary区分[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], 区分バイト[i:i+16])
	self.Mbr.Primary区分[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], 区分バイト[i:i+16])
	self.Mbr.Primary区分[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], 区分バイト[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(A配列tounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		コンソール_2.M印刷(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primary区分[i].P区分id == 0x00 {
			continue
		}

	}
}
