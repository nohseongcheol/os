/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package msdos分区

import . "控制台"
import . "工具"

import . "驱动程序/ata"

type T分区表格条目 struct {
	bootable	uint8

	开始head		uint8
	开始sector	uint8
	开始cylinder	uint16

	P分区id	uint8

	结尾head		uint8
	结尾sector	uint8
	结尾cylinder	uint16

	S开始lba	uint32
	长度	uint32
}

func (self *T分区表格条目) Init(数据 [16]byte) {
	self.bootable = 数据[0]

	self.开始head = 数据[1]
	self.开始sector = (数据[2] >> 2)
	self.开始cylinder = Unsignedinteger16r(uint16(数据[2]&0x03) | uint16(数据[3]))

	self.P分区id = 数据[4]

	self.结尾head = 数据[5]
	self.结尾sector = (数据[6] >> 2)
	self.结尾cylinder = Unsignedinteger16r(uint16(数据[6]&0x03) | uint16(数据[7]))

	var buffer1 [4]byte
	copy(buffer1[:4], 数据[8:12])
	self.S开始lba = Unsignedinteger32r(A数组tounsignedinteger32(buffer1))

	var buffer2 [4]byte
	copy(buffer2[:4], 数据[12:16])
	self.长度 = Unsignedinteger32r(A数组tounsignedinteger32(buffer2))
}

type T主引导记录 struct {
	bootloader	[440]byte
	signature	uint32
	未使用		uint16

	Primary分区	[4]T分区表格条目

	magicnumber	uint16
}
type Tmsdos分区表格 struct {
	Mbr T主引导记录
}

func (self *Tmsdos分区表格) R读取分区(hd *T高级技术attachment) {

	控制台_2 := T控制台{}
	控制台_2.M打印(([]byte)("Reading MBR"))

	var 分区字节 [512]byte
	var buffer_2 = 分区字节[:]
	hd.R读取28(0, &buffer_2, 512)

	self.Mbr = T主引导记录{}
	var i int = 0
	for ; i < 440; i++ {
		self.Mbr.bootloader[i] = 分区字节[i]
	}

	var buffer1 [4]byte
	copy(buffer1[:4], 分区字节[i:i+4])
	self.Mbr.signature = Unsignedinteger32r(A数组tounsignedinteger32(buffer1))
	i += 4

	var buffer2 [2]byte
	copy(buffer2[:2], 分区字节[i:i+2])
	self.Mbr.未使用 = Unsignedinteger16r(A数组tounsignedinteger16(buffer2))
	i += 2

	var buffer3 [16]byte
	copy(buffer3[:16], 分区字节[i:i+16])
	self.Mbr.Primary分区[0].Init(buffer3)
	i += 16

	copy(buffer3[:16], 分区字节[i:i+16])
	self.Mbr.Primary分区[1].Init(buffer3)
	i += 16

	copy(buffer3[:16], 分区字节[i:i+16])
	self.Mbr.Primary分区[2].Init(buffer3)
	i += 16

	copy(buffer3[:16], 分区字节[i:i+16])
	self.Mbr.Primary分区[3].Init(buffer3)
	i += 16

	var buffer6 [2]byte
	copy(buffer6[:2], 分区字节[i:i+2])
	self.Mbr.magicnumber = Unsignedinteger16r(A数组tounsignedinteger16(buffer6))

	if self.Mbr.magicnumber != 0xAA55 {
		控制台_2.M打印(([]byte)("illegal MBR"))
		return
	}

	for i := 0; i < 4; i++ {

		if self.Mbr.Primary分区[i].P分区id == 0x00 {
			continue
		}

	}
}
