package ata

import . "ポート"
import . "コンソール"

const Bバイトpersector int = 512

type T詳細使用技術attachment struct {
	マスター		bool
	データポート		Tポート16bit
	エラーポート		Tポート8bit
	sectorカウントポート	Tポート8bit
	lba低いポート	Tポート8bit
	lbamidポート	Tポート8bit
	lbahiポート	Tポート8bit
	デバイスポート		Tポート8bit
	コマンドポート		Tポート8bit
	制御ポート		Tポート8bit
}

func (self *T詳細使用技術attachment) Init(マスター bool, ポートbase uint16) {
	self.マスター = マスター
	self.データポート.Init(ポートbase)
	self.エラーポート.Init(ポートbase + 0x1)
	self.sectorカウントポート.Init(ポートbase + 0x2)
	self.lba低いポート.Init(ポートbase + 0x3)
	self.lbamidポート.Init(ポートbase + 0x4)
	self.lbahiポート.Init(ポートbase + 0x5)
	self.デバイスポート.Init(ポートbase + 0x6)
	self.コマンドポート.Init(ポートbase + 0x7)
	self.制御ポート.Init(ポートbase + 0x8)

}

func (self *T詳細使用技術attachment) Identify() {

	var コンソール_2 = Tコンソール{}

	if self.マスター {
		self.デバイスポート.W書込み(0xA0)
	} else {
		self.デバイスポート.W書込み(0xB0)
	}
	self.制御ポート.W書込み(0)
	self.デバイスポート.W書込み(0xA0)

	var 状態 uint8 = self.コマンドポート.R読込み()
	if 状態 == 0xFF {
		コンソール_2.M印刷(([]byte)("Invalid Status"))
		return
	}

	if self.マスター {
		self.デバイスポート.W書込み(0xA0)
	} else {
		self.デバイスポート.W書込み(0xB0)
	}
	self.sectorカウントポート.W書込み(0)
	self.lba低いポート.W書込み(0)
	self.lbamidポート.W書込み(0)
	self.lbahiポート.W書込み(0)
	self.コマンドポート.W書込み(0xEC)

	状態 = self.コマンドポート.R読込み()
	if 状態 == 0x00 {
		コンソール_2.M印刷(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (状態&0x80) == 0x80 && (状態&0x01) != 0x01 {
		状態 = self.コマンドポート.R読込み()
	}

	if (状態 & 0x01) != 0 {
		コンソール_2.M印刷(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var データ = self.データポート.R読込み()
		テキスト := []byte("  ")
		テキスト[0] = uint8((データ >> 8) & 0xFF)
		テキスト[1] = uint8(データ & 0xFF)

	}
	コンソール_2.M印刷xy(([]byte)("ata ok"), 10, 22)

}
func (self *T詳細使用技術attachment) R読込み28(sector uint32, データ *[]byte, カウント int) {
	var コンソール_2 = Tコンソール{}
	if (sector & 0xF0000000) != 0 {
		コンソール_2.M印刷(([]byte)("ata read error "))
		return
	}
	if カウント > Bバイトpersector {
		コンソール_2.M印刷(([]byte)("ata read error "))
		return
	}

	if self.マスター {
		self.デバイスポート.W書込み(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.デバイスポート.W書込み(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.エラーポート.W書込み(0)
	self.sectorカウントポート.W書込み(1)

	self.lba低いポート.W書込み(uint8(sector & 0x000000FF))
	self.lbamidポート.W書込み(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiポート.W書込み(uint8((sector & 0x00FF0000) >> 16))
	self.コマンドポート.W書込み(0x20)

	var 状態 uint8 = self.コマンドポート.R読込み()
	for ((状態 & 0x80) == 0x80) && ((状態 & 0x01) != 0x01) {
		状態 = self.コマンドポート.R読込み()
	}

	if (状態 & 0x01) != 0 {
		コンソール_2.M印刷(([]byte)("ata read error "))
		return
	}

	コンソール_2.M印刷xy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < カウント; i += 2 {
		var wdata uint16 = self.データポート.R読込み()

		(*データ)[i] = uint8(wdata & 0x00FF)
		if i+1 < カウント {

			(*データ)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (カウント + (カウント % 2)); i < Bバイトpersector; i += 2 {
		self.データポート.R読込み()
	}
}
func (self *T詳細使用技術attachment) W書込み28(sectornumber uint32, データ []byte, カウント uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if カウント > 512 {
		return
	}

	if self.マスター {
		self.デバイスポート.W書込み(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.デバイスポート.W書込み(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.エラーポート.W書込み(0)
	self.sectorカウントポート.W書込み(1)
	self.lba低いポート.W書込み(uint8(sectornumber & 0x000000FF))
	self.lbamidポート.W書込み(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiポート.W書込み(uint8((sectornumber & 0x00FF0000) >> 16))
	self.コマンドポート.W書込み(0x30)

	var コンソール_2 = Tコンソール{}
	コンソール_2.M印刷(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < カウント; i += 2 {

		var wdata uint16 = uint16(データ[i])

		if i+1 < カウント {
			wdata = wdata | (uint16(データ[i+1]) << 8)
		}

		self.データポート.W書込み(wdata)

		テキスト := []byte("  ")
		テキスト[0] = uint8((wdata >> 8) & 0xFF)
		テキスト[1] = uint8(wdata & 0xFF)

		コンソール_2.M印刷(テキスト)
	}

	for i := (カウント + (カウント % 2)); i < 512; i += 2 {
		self.データポート.W書込み(0x0000)
	}

}

func (self *T詳細使用技術attachment) Flush() {
	if self.マスター {
		self.デバイスポート.W書込み(0xE0)
	} else {
		self.デバイスポート.W書込み(0xF0)
	}
	self.コマンドポート.W書込み(0xE7)

	var コンソール_2 = Tコンソール{}

	var 状態 uint8 = self.コマンドポート.R読込み()
	if 状態 == 0x00 {
		return
	}

	for ((状態 & 0x80) == 0x80) && ((状態 & 0x01) != 0x01) {
		状態 = self.コマンドポート.R読込み()
	}
	if (状態 & 0x01) != 0 {
		コンソール_2.M印刷(([]byte)(" ata flush error"))
		return
	}

}
