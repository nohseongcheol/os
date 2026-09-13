package msdos分割區

import . "控制台"
import . "工具"

import . "驅動程式/ata"

type T分割區table項目 struct {
	bootable	uint8

	啟動head		uint8
	啟動sector	uint8
	啟動cylinder	uint16

	P分割區識別號	uint8

	結束head		uint8
	結束sector	uint8
	結束cylinder	uint16

	S啟動lba	uint32
	長度	uint32
}

func (self *T分割區table項目) Init(資料 [16]byte) {
	self.bootable = 資料[0]

	self.啟動head = 資料[1]
	self.啟動sector = (資料[2] >> 2)
	self.啟動cylinder = Unsignedinteger16r(uint16(資料[2]&0x03) | uint16(資料[3]))

	self.P分割區識別號 = 資料[4]

	self.結束head = 資料[5]
	self.結束sector = (資料[6] >> 2)
	self.結束cylinder = Unsignedinteger16r(uint16(資料[6]&0x03) | uint16(資料[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], 資料[8:12])
	self.S啟動lba = Unsignedinteger32r(A陣列tounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], 資料[12:16])
	self.長度 = Unsignedinteger32r(A陣列tounsignedinteger32(buffer2))
}

type T主開機紀錄 struct {
	bootloader	[440]byte
	signature	uint32
	未使用		uint16

	Primary分割區	[4]T分割區table項目

	magicnumber	uint16
}
type Tmsdos分割區table struct {
	Mbr T主開機紀錄
}

func (self *Tmsdos分割區table) R讀取分割區(hd *T進階科技attachment) {

	控制台_2 := T控制台{}
	控制台_2.M列印(([]byte)("Reading MBR"))

	var 分割區位元組 [512]byte
	var buffer_2 = 分割區位元組[:]
	hd.R讀取28(0, &buffer_2, 512)

	self.Mbr = T主開機紀錄{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = 分割區位元組[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], 分割區位元組[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(A陣列tounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], 分割區位元組[i:i+2])
	self.Mbr.未使用 = Unsignedinteger16r(A陣列tounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], 分割區位元組[i:i+16])
	self.Mbr.Primary分割區[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], 分割區位元組[i:i+16])
	self.Mbr.Primary分割區[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], 分割區位元組[i:i+16])
	self.Mbr.Primary分割區[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], 分割區位元組[i:i+16])
	self.Mbr.Primary分割區[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], 分割區位元組[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(A陣列tounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		控制台_2.M列印(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primary分割區[i].P分割區識別號 == 0x00 {
			continue
		}

	}
}
