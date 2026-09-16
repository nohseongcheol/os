/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ぶつりめもり

import (
	. "きょうつう"
	. "unsafe"
)

const (
	Bぶろっくさいず	uint32	= 4 * 1024
	Bぶろっくperばいと	uint32	= 8
)

type multibootめもりたいおうひょう struct {
	さいず		uint32
	baseaddressひくい	uint64
	baseaddressたかい	uint64
	ながさひくい		uint64
	ながさたかい		uint64
	Tかた		uint32
}

func Phymemてすと() {
}

var めもりoper Mめもりoper = Mめもりoper{}

type Pぶつりめもりかんりしゃ struct {
	めもりさいず	uint32
	しようちゅうぶろっく	uint32
	さいだいぶろっく	uint32
	めもりはいれつ	[]uint32
}

var (
	さいだいぶろっく			uint32	= 0
	めもりはいれつ			[]uint32
	grubmultibootめもりたいおうひょうt	multibootめもりたいおうひょう
)

func (self *Pぶつりめもりかんりしゃ) Sありbit(bit uint32) uint32 {
	self.めもりはいれつ[bit/32] = self.めもりはいれつ[bit/32] | (1 << (bit % 32))
	return self.めもりはいれつ[bit/32]
}
func (self *Pぶつりめもりかんりしゃ) Mわりあてびっとをはんてん(bit uint32) uint32 {
	self.めもりはいれつ[bit/32] = self.めもりはいれつ[bit/32] ^ (1 << (bit % 32))
	return self.めもりはいれつ[bit/32]
}
func (self *Pぶつりめもりかんりしゃ) Tてすとbit(bit uint32) uint32 {
	ret := self.めもりはいれつ[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Pぶつりめもりかんりしゃ) Tごうけいぶろっく() uint32 {
	return self.さいだいぶろっく
}
func (self *Pぶつりめもりかんりしゃ) Uしようちゅうぶろっく() uint32 {
	return self.しようちゅうぶろっく
}
func (self *Pぶつりめもりかんりしゃ) Aかぶかずofめもり() uint32 {
	return self.めもりさいず
}
func (self *Pぶつりめもりかんりしゃ) Getbitmaspさいず() uint32 {
	return self.めもりさいず / Bぶろっくさいず / Bぶろっくperばいと
}

func (self *Pぶつりめもりかんりしゃ) Firstあき() uint32 {
	for i := uint32(0); i < self.Tごうけいぶろっく(); i++ {
		if self.めもりはいれつ[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (めもりはいれつ[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Pぶつりめもりかんりしゃ) Firstあきさいず(さいず uint32) uint32 {
	if さいず == 0 {
		return 0xffffffff
	}
	if さいず == 1 {
		return self.Firstあき()
	}

	for i := uint32(0); i < self.Tごうけいぶろっく(); i++ {
		if self.めもりはいれつ[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.めもりはいれつ[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var あき uint32 = 0
					for かうんと := uint32(0); かうんと <= さいず; かうんと++ {
						if self.Tてすとbit(startingbit+かうんと) == 0 {
							あき++
						}

						if あき == さいず {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Pぶつりめもりかんりしゃ) Init(さいず uint32, わりあてびっとおもて []uint32) {
	self.めもりさいず = さいず
	self.めもりはいれつ = わりあてびっとおもて
	self.さいだいぶろっく = さいず / Bぶろっくさいず
	self.しようちゅうぶろっく = self.さいだいぶろっく
	めもりoper.Memあり(uintptr(Pointer(&self.めもりはいれつ)), 0xFF, self.しようちゅうぶろっく/Bぶろっくperばいと)
}
func (self *Pぶつりめもりかんりしゃ) Allocateぶろっく() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Pぶつりめもりかんりしゃ) Pぺーじすうちのまるめこみうえへ(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Pぶつりめもりかんりしゃ) Pぺーじすうちのまるめこみした(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
