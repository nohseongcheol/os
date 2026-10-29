/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMemorija

import (
	. "zajednički"
	. "unsafe"
)

const (
	BlokVeličina	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootMemorijamap struct {
	veličina	uint32
	baseaddresslow	uint64
	baseaddresshigh	uint64
	lengthlow	uint64
	lengthhigh	uint64
	Tip		uint32
}

func Phymemtest() {
}

var memorijaoper Memorijaoper = Memorijaoper{}

type PhysicalMemorijamanager struct {
	memorijaVeličina	uint32
	korištenoblok		uint32
	najvišeblok		uint32
	memorijaarray		[]uint32
}

var (
	najvišeblok			uint32	= 0
	memorijaarray			[]uint32
	grubmultibootMemorijamapt	multibootMemorijamap
)

func (self *PhysicalMemorijamanager) Skupbit(bit uint32) uint32 {
	self.memorijaarray[bit/32] = self.memorijaarray[bit/32] | (1 << (bit % 32))
	return self.memorijaarray[bit/32]
}
func (self *PhysicalMemorijamanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.memorijaarray[bit/32] = self.memorijaarray[bit/32] ^ (1 << (bit % 32))
	return self.memorijaarray[bit/32]
}
func (self *PhysicalMemorijamanager) Testbit(bit uint32) uint32 {
	ret := self.memorijaarray[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalMemorijamanager) Ukupnoblok() uint32 {
	return self.najvišeblok
}
func (self *PhysicalMemorijamanager) Korištenoblok() uint32 {
	return self.korištenoblok
}
func (self *PhysicalMemorijamanager) IznosofMemorija() uint32 {
	return self.memorijaVeličina
}
func (self *PhysicalMemorijamanager) GetbitmaspVeličina() uint32 {
	return self.memorijaVeličina / BlokVeličina / Blokperbyte
}

func (self *PhysicalMemorijamanager) FirstSlobodno() uint32 {
	for i := uint32(0); i < self.Ukupnoblok(); i++ {
		if self.memorijaarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memorijaarray[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalMemorijamanager) FirstSlobodnoVeličina(veličina uint32) uint32 {
	if veličina == 0 {
		return 0xffffffff
	}
	if veličina == 1 {
		return self.FirstSlobodno()
	}

	for i := uint32(0); i < self.Ukupnoblok(); i++ {
		if self.memorijaarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.memorijaarray[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var slobodno uint32 = 0
					for count := uint32(0); count <= veličina; count++ {
						if self.Testbit(startingbit+count) == 0 {
							slobodno++
						}

						if slobodno == veličina {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalMemorijamanager) Init(veličina uint32, bitmap []uint32) {
	self.memorijaVeličina = veličina
	self.memorijaarray = bitmap
	self.najvišeblok = veličina / BlokVeličina
	self.korištenoblok = self.najvišeblok
	memorijaoper.Memskup(uintptr(Pointer(&self.memorijaarray)), 0xFF, self.korištenoblok/Blokperbyte)
}
func (self *PhysicalMemorijamanager) Allocateblok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalMemorijamanager) StranicaroundGore(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalMemorijamanager) Stranicarounddown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
