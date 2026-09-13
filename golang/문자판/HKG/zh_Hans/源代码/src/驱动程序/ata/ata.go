package ata

import . "端口"
import . "控制台"

const B字节persector int = 512

type T高级技术attachment struct {
	主		bool
	数据端口		T端口16bit
	错误端口		T端口8bit
	sector计数端口	T端口8bit
	lba低端口		T端口8bit
	lbamid端口	T端口8bit
	lbahi端口	T端口8bit
	设备端口		T端口8bit
	命令端口		T端口8bit
	ctrl端口		T端口8bit
}

func (self *T高级技术attachment) Init(主 bool, 端口base uint16) {
	self.主 = 主
	self.数据端口.Init(端口base)
	self.错误端口.Init(端口base + 0x1)
	self.sector计数端口.Init(端口base + 0x2)
	self.lba低端口.Init(端口base + 0x3)
	self.lbamid端口.Init(端口base + 0x4)
	self.lbahi端口.Init(端口base + 0x5)
	self.设备端口.Init(端口base + 0x6)
	self.命令端口.Init(端口base + 0x7)
	self.ctrl端口.Init(端口base + 0x8)

}

func (self *T高级技术attachment) Identify() {

	var 控制台_2 = T控制台{}

	if self.主 {
		self.设备端口.W写入(0xA0)
	} else {
		self.设备端口.W写入(0xB0)
	}
	self.ctrl端口.W写入(0)
	self.设备端口.W写入(0xA0)

	var 状态 uint8 = self.命令端口.R读取()
	if 状态 == 0xFF {
		控制台_2.M打印(([]byte)("Invalid Status"))
		return
	}

	if self.主 {
		self.设备端口.W写入(0xA0)
	} else {
		self.设备端口.W写入(0xB0)
	}
	self.sector计数端口.W写入(0)
	self.lba低端口.W写入(0)
	self.lbamid端口.W写入(0)
	self.lbahi端口.W写入(0)
	self.命令端口.W写入(0xEC)

	状态 = self.命令端口.R读取()
	if 状态 == 0x00 {
		控制台_2.M打印(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (状态&0x80) == 0x80 && (状态&0x01) != 0x01 {
		状态 = self.命令端口.R读取()
	}

	if (状态 & 0x01) != 0 {
		控制台_2.M打印(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var 数据 = self.数据端口.R读取()
		文本 := []byte("  ")
		文本[0] = uint8((数据 >> 8) & 0xFF)
		文本[1] = uint8(数据 & 0xFF)

	}
	控制台_2.M打印xy(([]byte)("ata ok"), 10, 22)

}
func (self *T高级技术attachment) R读取28(sector uint32, 数据 *[]byte, 计数 int) {
	var 控制台_2 = T控制台{}
	if (sector & 0xF0000000) != 0 {
		控制台_2.M打印(([]byte)("ata read error "))
		return
	}
	if 计数 > B字节persector {
		控制台_2.M打印(([]byte)("ata read error "))
		return
	}

	if self.主 {
		self.设备端口.W写入(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.设备端口.W写入(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.错误端口.W写入(0)
	self.sector计数端口.W写入(1)

	self.lba低端口.W写入(uint8(sector & 0x000000FF))
	self.lbamid端口.W写入(uint8((sector & 0x0000FF00) >> 8))
	self.lbahi端口.W写入(uint8((sector & 0x00FF0000) >> 16))
	self.命令端口.W写入(0x20)

	var 状态 uint8 = self.命令端口.R读取()
	for ((状态 & 0x80) == 0x80) && ((状态 & 0x01) != 0x01) {
		状态 = self.命令端口.R读取()
	}

	if (状态 & 0x01) != 0 {
		控制台_2.M打印(([]byte)("ata read error "))
		return
	}

	控制台_2.M打印xy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < 计数; i += 2 {
		var wdata uint16 = self.数据端口.R读取()

		(*数据)[i] = uint8(wdata & 0x00FF)
		if i+1 < 计数 {

			(*数据)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (计数 + (计数 % 2)); i < B字节persector; i += 2 {
		self.数据端口.R读取()
	}
}
func (self *T高级技术attachment) W写入28(sector数字 uint32, 数据 []byte, 计数 uint32) {

	if sector数字 > 0x0FFFFFFF {
		return
	}

	if 计数 > 512 {
		return
	}

	if self.主 {
		self.设备端口.W写入(uint8(0xE0 | uint8((sector数字&0x0F000000)>>24)))
	} else {
		self.设备端口.W写入(uint8(0xF0 | uint8((sector数字&0x0F000000)>>24)))
	}

	self.错误端口.W写入(0)
	self.sector计数端口.W写入(1)
	self.lba低端口.W写入(uint8(sector数字 & 0x000000FF))
	self.lbamid端口.W写入(uint8((sector数字 & 0x0000FF00) >> 8))
	self.lbahi端口.W写入(uint8((sector数字 & 0x00FF0000) >> 16))
	self.命令端口.W写入(0x30)

	var 控制台_2 = T控制台{}
	控制台_2.M打印(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < 计数; i += 2 {

		var wdata uint16 = uint16(数据[i])

		if i+1 < 计数 {
			wdata = wdata | (uint16(数据[i+1]) << 8)
		}

		self.数据端口.W写入(wdata)

		文本 := []byte("  ")
		文本[0] = uint8((wdata >> 8) & 0xFF)
		文本[1] = uint8(wdata & 0xFF)

		控制台_2.M打印(文本)
	}

	for i := (计数 + (计数 % 2)); i < 512; i += 2 {
		self.数据端口.W写入(0x0000)
	}

}

func (self *T高级技术attachment) Flush() {
	if self.主 {
		self.设备端口.W写入(0xE0)
	} else {
		self.设备端口.W写入(0xF0)
	}
	self.命令端口.W写入(0xE7)

	var 控制台_2 = T控制台{}

	var 状态 uint8 = self.命令端口.R读取()
	if 状态 == 0x00 {
		return
	}

	for ((状态 & 0x80) == 0x80) && ((状态 & 0x01) != 0x01) {
		状态 = self.命令端口.R读取()
	}
	if (状态 & 0x01) != 0 {
		控制台_2.M打印(([]byte)(" ata flush error"))
		return
	}

}
