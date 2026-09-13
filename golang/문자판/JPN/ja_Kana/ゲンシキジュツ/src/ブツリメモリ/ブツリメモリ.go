package ブツリメモリ

import (
	. "キョウツウ"
	. "unsafe"
)

const (
	Bブロックサイズ	uint32	= 4 * 1024
	Bブロックperバイト	uint32	= 8
)

type multibootメモリタイオウヒョウ struct {
	サイズ		uint32
	baseaddressヒクイ	uint64
	baseaddressタカイ	uint64
	ナガサヒクイ		uint64
	ナガサタカイ		uint64
	Tカタ		uint32
}

func Phymemテスト() {
}

var メモリoper Mメモリoper = Mメモリoper{}

type Pブツリメモリカンリシャ struct {
	メモリサイズ	uint32
	シヨウチュウブロック	uint32
	サイダイブロック	uint32
	メモリハイレツ	[]uint32
}

var (
	サイダイブロック			uint32	= 0
	メモリハイレツ			[]uint32
	grubmultibootメモリタイオウヒョウt	multibootメモリタイオウヒョウ
)

func (self *Pブツリメモリカンリシャ) Sアリbit(bit uint32) uint32 {
	self.メモリハイレツ[bit/32] = self.メモリハイレツ[bit/32] | (1 << (bit % 32))
	return self.メモリハイレツ[bit/32]
}
func (self *Pブツリメモリカンリシャ) Mワリアテビットヲハンテン(bit uint32) uint32 {
	self.メモリハイレツ[bit/32] = self.メモリハイレツ[bit/32] ^ (1 << (bit % 32))
	return self.メモリハイレツ[bit/32]
}
func (self *Pブツリメモリカンリシャ) Tテストbit(bit uint32) uint32 {
	ret := self.メモリハイレツ[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Pブツリメモリカンリシャ) Tゴウケイブロック() uint32 {
	return self.サイダイブロック
}
func (self *Pブツリメモリカンリシャ) Uシヨウチュウブロック() uint32 {
	return self.シヨウチュウブロック
}
func (self *Pブツリメモリカンリシャ) Aカブカズofメモリ() uint32 {
	return self.メモリサイズ
}
func (self *Pブツリメモリカンリシャ) Getbitmaspサイズ() uint32 {
	return self.メモリサイズ / Bブロックサイズ / Bブロックperバイト
}

func (self *Pブツリメモリカンリシャ) Firstアキ() uint32 {
	for i := uint32(0); i < self.Tゴウケイブロック(); i++ {
		if self.メモリハイレツ[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (メモリハイレツ[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Pブツリメモリカンリシャ) Firstアキサイズ(サイズ uint32) uint32 {
	if サイズ == 0 {
		return 0xffffffff
	}
	if サイズ == 1 {
		return self.Firstアキ()
	}

	for i := uint32(0); i < self.Tゴウケイブロック(); i++ {
		if self.メモリハイレツ[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.メモリハイレツ[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var アキ uint32 = 0
					for カウント := uint32(0); カウント <= サイズ; カウント++ {
						if self.Tテストbit(startingbit+カウント) == 0 {
							アキ++
						}

						if アキ == サイズ {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Pブツリメモリカンリシャ) Init(サイズ uint32, ワリアテビットオモテ []uint32) {
	self.メモリサイズ = サイズ
	self.メモリハイレツ = ワリアテビットオモテ
	self.サイダイブロック = サイズ / Bブロックサイズ
	self.シヨウチュウブロック = self.サイダイブロック
	メモリoper.Memアリ(uintptr(Pointer(&self.メモリハイレツ)), 0xFF, self.シヨウチュウブロック/Bブロックperバイト)
}
func (self *Pブツリメモリカンリシャ) Allocateブロック() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Pブツリメモリカンリシャ) Pページスウチノマルメコミウエヘ(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Pブツリメモリカンリシャ) Pページスウチノマルメコミシタ(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
