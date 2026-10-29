/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "連接埠"
import . "控制台"

const B位元組persector int = 512

type T進階科技attachment struct {
	主音量		bool
	資料連接埠		T連接埠16bit
	錯誤連接埠		T連接埠8bit
	sector計數連接埠	T連接埠8bit
	lba低連接埠		T連接埠8bit
	lbamid連接埠	T連接埠8bit
	lbahi連接埠		T連接埠8bit
	裝置連接埠		T連接埠8bit
	指令連接埠		T連接埠8bit
	控制連接埠		T連接埠8bit
}

func (self *T進階科技attachment) Init(主音量 bool, 連接埠base uint16) {
	self.主音量 = 主音量
	self.資料連接埠.Init(連接埠base)
	self.錯誤連接埠.Init(連接埠base + 0x1)
	self.sector計數連接埠.Init(連接埠base + 0x2)
	self.lba低連接埠.Init(連接埠base + 0x3)
	self.lbamid連接埠.Init(連接埠base + 0x4)
	self.lbahi連接埠.Init(連接埠base + 0x5)
	self.裝置連接埠.Init(連接埠base + 0x6)
	self.指令連接埠.Init(連接埠base + 0x7)
	self.控制連接埠.Init(連接埠base + 0x8)

}

func (self *T進階科技attachment) Identify() {

	var 控制台_2 = T控制台{}

	if self.主音量 {
		self.裝置連接埠.W寫入(0xA0)
	} else {
		self.裝置連接埠.W寫入(0xB0)
	}
	self.控制連接埠.W寫入(0)
	self.裝置連接埠.W寫入(0xA0)

	var 狀態 uint8 = self.指令連接埠.R讀取()
	if 狀態 == 0xFF {
		控制台_2.M列印(([]byte)("Invalid Status"))
		return
	}

	if self.主音量 {
		self.裝置連接埠.W寫入(0xA0)
	} else {
		self.裝置連接埠.W寫入(0xB0)
	}
	self.sector計數連接埠.W寫入(0)
	self.lba低連接埠.W寫入(0)
	self.lbamid連接埠.W寫入(0)
	self.lbahi連接埠.W寫入(0)
	self.指令連接埠.W寫入(0xEC)

	狀態 = self.指令連接埠.R讀取()
	if 狀態 == 0x00 {
		控制台_2.M列印(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (狀態&0x80) == 0x80 && (狀態&0x01) != 0x01 {
		狀態 = self.指令連接埠.R讀取()
	}

	if (狀態 & 0x01) != 0 {
		控制台_2.M列印(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var 資料 = self.資料連接埠.R讀取()
		文字 := []byte("  ")
		文字[0] = uint8((資料 >> 8) & 0xFF)
		文字[1] = uint8(資料 & 0xFF)

	}
	控制台_2.M列印xy(([]byte)("ata ok"), 10, 22)

}
func (self *T進階科技attachment) R讀取28(sector uint32, 資料 *[]byte, 計數 int) {
	var 控制台_2 = T控制台{}
	if (sector & 0xF0000000) != 0 {
		控制台_2.M列印(([]byte)("ata read error "))
		return
	}
	if 計數 > B位元組persector {
		控制台_2.M列印(([]byte)("ata read error "))
		return
	}

	if self.主音量 {
		self.裝置連接埠.W寫入(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.裝置連接埠.W寫入(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.錯誤連接埠.W寫入(0)
	self.sector計數連接埠.W寫入(1)

	self.lba低連接埠.W寫入(uint8(sector & 0x000000FF))
	self.lbamid連接埠.W寫入(uint8((sector & 0x0000FF00) >> 8))
	self.lbahi連接埠.W寫入(uint8((sector & 0x00FF0000) >> 16))
	self.指令連接埠.W寫入(0x20)

	var 狀態 uint8 = self.指令連接埠.R讀取()
	for ((狀態 & 0x80) == 0x80) && ((狀態 & 0x01) != 0x01) {
		狀態 = self.指令連接埠.R讀取()
	}

	if (狀態 & 0x01) != 0 {
		控制台_2.M列印(([]byte)("ata read error "))
		return
	}

	控制台_2.M列印xy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < 計數; i += 2 {
		var wdata uint16 = self.資料連接埠.R讀取()

		(*資料)[i] = uint8(wdata & 0x00FF)
		if i+1 < 計數 {

			(*資料)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (計數 + (計數 % 2)); i < B位元組persector; i += 2 {
		self.資料連接埠.R讀取()
	}
}
func (self *T進階科技attachment) W寫入28(sector數字 uint32, 資料 []byte, 計數 uint32) {

	if sector數字 > 0x0FFFFFFF {
		return
	}

	if 計數 > 512 {
		return
	}

	if self.主音量 {
		self.裝置連接埠.W寫入(uint8(0xE0 | uint8((sector數字&0x0F000000)>>24)))
	} else {
		self.裝置連接埠.W寫入(uint8(0xF0 | uint8((sector數字&0x0F000000)>>24)))
	}

	self.錯誤連接埠.W寫入(0)
	self.sector計數連接埠.W寫入(1)
	self.lba低連接埠.W寫入(uint8(sector數字 & 0x000000FF))
	self.lbamid連接埠.W寫入(uint8((sector數字 & 0x0000FF00) >> 8))
	self.lbahi連接埠.W寫入(uint8((sector數字 & 0x00FF0000) >> 16))
	self.指令連接埠.W寫入(0x30)

	var 控制台_2 = T控制台{}
	控制台_2.M列印(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < 計數; i += 2 {

		var wdata uint16 = uint16(資料[i])

		if i+1 < 計數 {
			wdata = wdata | (uint16(資料[i+1]) << 8)
		}

		self.資料連接埠.W寫入(wdata)

		文字 := []byte("  ")
		文字[0] = uint8((wdata >> 8) & 0xFF)
		文字[1] = uint8(wdata & 0xFF)

		控制台_2.M列印(文字)
	}

	for i := (計數 + (計數 % 2)); i < 512; i += 2 {
		self.資料連接埠.W寫入(0x0000)
	}

}

func (self *T進階科技attachment) Flush() {
	if self.主音量 {
		self.裝置連接埠.W寫入(0xE0)
	} else {
		self.裝置連接埠.W寫入(0xF0)
	}
	self.指令連接埠.W寫入(0xE7)

	var 控制台_2 = T控制台{}

	var 狀態 uint8 = self.指令連接埠.R讀取()
	if 狀態 == 0x00 {
		return
	}

	for ((狀態 & 0x80) == 0x80) && ((狀態 & 0x01) != 0x01) {
		狀態 = self.指令連接埠.R讀取()
	}
	if (狀態 & 0x01) != 0 {
		控制台_2.M列印(([]byte)(" ata flush error"))
		return
	}

}
