/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ata

import . "ポート"
import . "コンソール"

const Bバイトpersector int = 512

type Tショウサイシヨウギジュツattachment struct {
	マスター		bool
	データポート		Tポート16bit
	エラーポート		Tポート8bit
	sectorカウントポート	Tポート8bit
	lbaヒクイポート	Tポート8bit
	lbamidポート	Tポート8bit
	lbahiポート	Tポート8bit
	デバイスポート		Tポート8bit
	コマンドポート		Tポート8bit
	セイギョポート		Tポート8bit
}

func (self *Tショウサイシヨウギジュツattachment) Init(マスター bool, ポートbase uint16) {
	self.マスター = マスター
	self.データポート.Init(ポートbase)
	self.エラーポート.Init(ポートbase + 0x1)
	self.sectorカウントポート.Init(ポートbase + 0x2)
	self.lbaヒクイポート.Init(ポートbase + 0x3)
	self.lbamidポート.Init(ポートbase + 0x4)
	self.lbahiポート.Init(ポートbase + 0x5)
	self.デバイスポート.Init(ポートbase + 0x6)
	self.コマンドポート.Init(ポートbase + 0x7)
	self.セイギョポート.Init(ポートbase + 0x8)

}

func (self *Tショウサイシヨウギジュツattachment) Identify() {

	var コンソール_2 = Tコンソール{}

	if self.マスター {
		self.デバイスポート.Wカキコミ(0xA0)
	} else {
		self.デバイスポート.Wカキコミ(0xB0)
	}
	self.セイギョポート.Wカキコミ(0)
	self.デバイスポート.Wカキコミ(0xA0)

	var ジョウタイ uint8 = self.コマンドポート.Rヨミコミ()
	if ジョウタイ == 0xFF {
		コンソール_2.Mインサツ(([]byte)("Invalid Status"))
		return
	}

	if self.マスター {
		self.デバイスポート.Wカキコミ(0xA0)
	} else {
		self.デバイスポート.Wカキコミ(0xB0)
	}
	self.sectorカウントポート.Wカキコミ(0)
	self.lbaヒクイポート.Wカキコミ(0)
	self.lbamidポート.Wカキコミ(0)
	self.lbahiポート.Wカキコミ(0)
	self.コマンドポート.Wカキコミ(0xEC)

	ジョウタイ = self.コマンドポート.Rヨミコミ()
	if ジョウタイ == 0x00 {
		コンソール_2.Mインサツ(([]byte)("HDD Does not exist, ignoreign "))
		return
	}
	for (ジョウタイ&0x80) == 0x80 && (ジョウタイ&0x01) != 0x01 {
		ジョウタイ = self.コマンドポート.Rヨミコミ()
	}

	if (ジョウタイ & 0x01) != 0 {
		コンソール_2.Mインサツ(([]byte)("error reading ATA"))
		return
	}

	for i := 0; i < 256; i++ {
		var データ = self.データポート.Rヨミコミ()
		テキスト := []byte("  ")
		テキスト[0] = uint8((データ >> 8) & 0xFF)
		テキスト[1] = uint8(データ & 0xFF)

	}
	コンソール_2.Mインサツxy(([]byte)("ata ok"), 10, 22)

}
func (self *Tショウサイシヨウギジュツattachment) Rヨミコミ28(sector uint32, データ *[]byte, カウント int) {
	var コンソール_2 = Tコンソール{}
	if (sector & 0xF0000000) != 0 {
		コンソール_2.Mインサツ(([]byte)("ata read error "))
		return
	}
	if カウント > Bバイトpersector {
		コンソール_2.Mインサツ(([]byte)("ata read error "))
		return
	}

	if self.マスター {
		self.デバイスポート.Wカキコミ(uint8(0xE0 | uint8((sector&0x0F000000)>>24)))
	} else {
		self.デバイスポート.Wカキコミ(uint8(0xF0 | uint8((sector&0x0F000000)>>24)))
	}
	self.エラーポート.Wカキコミ(0)
	self.sectorカウントポート.Wカキコミ(1)

	self.lbaヒクイポート.Wカキコミ(uint8(sector & 0x000000FF))
	self.lbamidポート.Wカキコミ(uint8((sector & 0x0000FF00) >> 8))
	self.lbahiポート.Wカキコミ(uint8((sector & 0x00FF0000) >> 16))
	self.コマンドポート.Wカキコミ(0x20)

	var ジョウタイ uint8 = self.コマンドポート.Rヨミコミ()
	for ((ジョウタイ & 0x80) == 0x80) && ((ジョウタイ & 0x01) != 0x01) {
		ジョウタイ = self.コマンドポート.Rヨミコミ()
	}

	if (ジョウタイ & 0x01) != 0 {
		コンソール_2.Mインサツ(([]byte)("ata read error "))
		return
	}

	コンソール_2.Mインサツxy(([]byte)("Reading ATA Drive:"), 1, 24)

	var i int = 0
	for ; i < カウント; i += 2 {
		var wdata uint16 = self.データポート.Rヨミコミ()

		(*データ)[i] = uint8(wdata & 0x00FF)
		if i+1 < カウント {

			(*データ)[i+1] = uint8((wdata >> 8) & 0x00FF)
		}
	}

	for i := (カウント + (カウント % 2)); i < Bバイトpersector; i += 2 {
		self.データポート.Rヨミコミ()
	}
}
func (self *Tショウサイシヨウギジュツattachment) Wカキコミ28(sectornumber uint32, データ []byte, カウント uint32) {

	if sectornumber > 0x0FFFFFFF {
		return
	}

	if カウント > 512 {
		return
	}

	if self.マスター {
		self.デバイスポート.Wカキコミ(uint8(0xE0 | uint8((sectornumber&0x0F000000)>>24)))
	} else {
		self.デバイスポート.Wカキコミ(uint8(0xF0 | uint8((sectornumber&0x0F000000)>>24)))
	}

	self.エラーポート.Wカキコミ(0)
	self.sectorカウントポート.Wカキコミ(1)
	self.lbaヒクイポート.Wカキコミ(uint8(sectornumber & 0x000000FF))
	self.lbamidポート.Wカキコミ(uint8((sectornumber & 0x0000FF00) >> 8))
	self.lbahiポート.Wカキコミ(uint8((sectornumber & 0x00FF0000) >> 16))
	self.コマンドポート.Wカキコミ(0x30)

	var コンソール_2 = Tコンソール{}
	コンソール_2.Mインサツ(([]byte)("Writing to ATA Drive:"))

	for i := uint32(0); i < カウント; i += 2 {

		var wdata uint16 = uint16(データ[i])

		if i+1 < カウント {
			wdata = wdata | (uint16(データ[i+1]) << 8)
		}

		self.データポート.Wカキコミ(wdata)

		テキスト := []byte("  ")
		テキスト[0] = uint8((wdata >> 8) & 0xFF)
		テキスト[1] = uint8(wdata & 0xFF)

		コンソール_2.Mインサツ(テキスト)
	}

	for i := (カウント + (カウント % 2)); i < 512; i += 2 {
		self.データポート.Wカキコミ(0x0000)
	}

}

func (self *Tショウサイシヨウギジュツattachment) Flush() {
	if self.マスター {
		self.デバイスポート.Wカキコミ(0xE0)
	} else {
		self.デバイスポート.Wカキコミ(0xF0)
	}
	self.コマンドポート.Wカキコミ(0xE7)

	var コンソール_2 = Tコンソール{}

	var ジョウタイ uint8 = self.コマンドポート.Rヨミコミ()
	if ジョウタイ == 0x00 {
		return
	}

	for ((ジョウタイ & 0x80) == 0x80) && ((ジョウタイ & 0x01) != 0x01) {
		ジョウタイ = self.コマンドポート.Rヨミコミ()
	}
	if (ジョウタイ & 0x01) != 0 {
		コンソール_2.Mインサツ(([]byte)(" ata flush error"))
		return
	}

}
