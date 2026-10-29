/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalmemory

import (
	. "common"
	. "unsafe"
)

const (
	BlokkurStødd	uint32	= 4 * 1024
	Blokkurperbyte	uint32	= 8
)

type multibootmemorymap struct {
	stødd			uint32
	baseaddressLágur	uint64
	baseaddressHøgt		uint64
	longdLágur		uint64
	longdHøgt		uint64
	TypeValue		uint32
}

func Phymemtest() {
}

var memoryoper Memoryoper = Memoryoper{}

type Physicalmemorymanager struct {
	memoryStødd	uint32
	usedBlokkur	uint32
	maximumBlokkur	uint32
	memoryarray	[]uint32
}

var (
	maximumBlokkur		uint32	= 0
	memoryarray		[]uint32
	grubmultibootmemorymapt	multibootmemorymap
)

func (self *Physicalmemorymanager) Setbit(bit uint32) uint32 {
	self.memoryarray[bit/32] = self.memoryarray[bit/32] | (1 << (bit % 32))
	return self.memoryarray[bit/32]
}
func (self *Physicalmemorymanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.memoryarray[bit/32] = self.memoryarray[bit/32] ^ (1 << (bit % 32))
	return self.memoryarray[bit/32]
}
func (self *Physicalmemorymanager) Testbit(bit uint32) uint32 {
	ret := self.memoryarray[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Physicalmemorymanager) TotalBlokkur() uint32 {
	return self.maximumBlokkur
}
func (self *Physicalmemorymanager) UsedBlokkur() uint32 {
	return self.usedBlokkur
}
func (self *Physicalmemorymanager) Amountofmemory() uint32 {
	return self.memoryStødd
}
func (self *Physicalmemorymanager) GetbitmaspStødd() uint32 {
	return self.memoryStødd / BlokkurStødd / Blokkurperbyte
}

func (self *Physicalmemorymanager) Firstfree() uint32 {
	for i := uint32(0); i < self.TotalBlokkur(); i++ {
		if self.memoryarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memoryarray[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Physicalmemorymanager) FirstfreeStødd(stødd uint32) uint32 {
	if stødd == 0 {
		return 0xffffffff
	}
	if stødd == 1 {
		return self.Firstfree()
	}

	for i := uint32(0); i < self.TotalBlokkur(); i++ {
		if self.memoryarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.memoryarray[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var free uint32 = 0
					for count := uint32(0); count <= stødd; count++ {
						if self.Testbit(startingbit+count) == 0 {
							free++
						}

						if free == stødd {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Physicalmemorymanager) Init(stødd uint32, bitmap []uint32) {
	self.memoryStødd = stødd
	self.memoryarray = bitmap
	self.maximumBlokkur = stødd / BlokkurStødd
	self.usedBlokkur = self.maximumBlokkur
	memoryoper.Memset(uintptr(Pointer(&self.memoryarray)), 0xFF, self.usedBlokkur/Blokkurperbyte)
}
func (self *Physicalmemorymanager) AllocateBlokkur() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Physicalmemorymanager) Pageroundup(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Physicalmemorymanager) Pagerounddown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
