/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 物理メモリ

import (
	. "共通"
	. "unsafe"
)

const (
	Bブロックサイズ	uint32	= 4 * 1024
	Bブロックperバイト	uint32	= 8
)

type multibootメモリ対応表 struct {
	サイズ		uint32
	baseaddress低い	uint64
	baseaddress高い	uint64
	長さ低い		uint64
	長さ高い		uint64
	T型		uint32
}

func Phymemテスト() {
}

var メモリoper Mメモリoper = Mメモリoper{}

type P物理メモリ管理者 struct {
	メモリサイズ	uint32
	使用中ブロック	uint32
	最大ブロック	uint32
	メモリ配列	[]uint32
}

var (
	最大ブロック			uint32	= 0
	メモリ配列			[]uint32
	grubmultibootメモリ対応表t	multibootメモリ対応表
)

func (self *P物理メモリ管理者) Sありbit(bit uint32) uint32 {
	self.メモリ配列[bit/32] = self.メモリ配列[bit/32] | (1 << (bit % 32))
	return self.メモリ配列[bit/32]
}
func (self *P物理メモリ管理者) M割当ビットを反転(bit uint32) uint32 {
	self.メモリ配列[bit/32] = self.メモリ配列[bit/32] ^ (1 << (bit % 32))
	return self.メモリ配列[bit/32]
}
func (self *P物理メモリ管理者) Tテストbit(bit uint32) uint32 {
	ret := self.メモリ配列[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *P物理メモリ管理者) T合計ブロック() uint32 {
	return self.最大ブロック
}
func (self *P物理メモリ管理者) U使用中ブロック() uint32 {
	return self.使用中ブロック
}
func (self *P物理メモリ管理者) A株数ofメモリ() uint32 {
	return self.メモリサイズ
}
func (self *P物理メモリ管理者) Getbitmaspサイズ() uint32 {
	return self.メモリサイズ / Bブロックサイズ / Bブロックperバイト
}

func (self *P物理メモリ管理者) First空き() uint32 {
	for i := uint32(0); i < self.T合計ブロック(); i++ {
		if self.メモリ配列[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (メモリ配列[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *P物理メモリ管理者) First空きサイズ(サイズ uint32) uint32 {
	if サイズ == 0 {
		return 0xffffffff
	}
	if サイズ == 1 {
		return self.First空き()
	}

	for i := uint32(0); i < self.T合計ブロック(); i++ {
		if self.メモリ配列[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.メモリ配列[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var 空き uint32 = 0
					for カウント := uint32(0); カウント <= サイズ; カウント++ {
						if self.Tテストbit(startingbit+カウント) == 0 {
							空き++
						}

						if 空き == サイズ {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *P物理メモリ管理者) Init(サイズ uint32, 割当ビット表 []uint32) {
	self.メモリサイズ = サイズ
	self.メモリ配列 = 割当ビット表
	self.最大ブロック = サイズ / Bブロックサイズ
	self.使用中ブロック = self.最大ブロック
	メモリoper.Memあり(uintptr(Pointer(&self.メモリ配列)), 0xFF, self.使用中ブロック/Bブロックperバイト)
}
func (self *P物理メモリ管理者) Allocateブロック() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *P物理メモリ管理者) Pページ数値の丸め込み上へ(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *P物理メモリ管理者) Pページ数値の丸め込み下(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
