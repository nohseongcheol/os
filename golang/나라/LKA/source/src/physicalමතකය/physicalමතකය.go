/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalමතකය

import (
	. "common"
	. "unsafe"
)

const (
	Blocksize	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootමතකයmap struct {
	size		uint32
	baseaddresslow	uint64
	baseaddresshigh	uint64
	lengthlow	uint64
	lengthhigh	uint64
	Typeඅගය		uint32
}

func Phymemtest() {
}

var මතකයoper Mමතකයoper = Mමතකයoper{}

type Physicalමතකයmanager struct {
	මතකයsize	uint32
	usedblock	uint32
	maximumblock	uint32
	මතකයarray	[]uint32
}

var (
	maximumblock		uint32	= 0
	මතකයarray		[]uint32
	grubmultibootමතකයmapt	multibootමතකයmap
)

func (self *Physicalමතකයmanager) Setbit(bit uint32) uint32 {
	self.මතකයarray[bit/32] = self.මතකයarray[bit/32] | (1 << (bit % 32))
	return self.මතකයarray[bit/32]
}
func (self *Physicalමතකයmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.මතකයarray[bit/32] = self.මතකයarray[bit/32] ^ (1 << (bit % 32))
	return self.මතකයarray[bit/32]
}
func (self *Physicalමතකයmanager) Testbit(bit uint32) uint32 {
	ret := self.මතකයarray[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Physicalමතකයmanager) Totalblock() uint32 {
	return self.maximumblock
}
func (self *Physicalමතකයmanager) Usedblock() uint32 {
	return self.usedblock
}
func (self *Physicalමතකයmanager) Amountofමතකය() uint32 {
	return self.මතකයsize
}
func (self *Physicalමතකයmanager) Getbitmaspsize() uint32 {
	return self.මතකයsize / Blocksize / Blockperbyte
}

func (self *Physicalමතකයmanager) Firstfree() uint32 {
	for i := uint32(0); i < self.Totalblock(); i++ {
		if self.මතකයarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (මතකයarray[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Physicalමතකයmanager) Firstfreesize(size uint32) uint32 {
	if size == 0 {
		return 0xffffffff
	}
	if size == 1 {
		return self.Firstfree()
	}

	for i := uint32(0); i < self.Totalblock(); i++ {
		if self.මතකයarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.මතකයarray[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var free uint32 = 0
					for count := uint32(0); count <= size; count++ {
						if self.Testbit(startingbit+count) == 0 {
							free++
						}

						if free == size {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Physicalමතකයmanager) Init(size uint32, bitmap []uint32) {
	self.මතකයsize = size
	self.මතකයarray = bitmap
	self.maximumblock = size / Blocksize
	self.usedblock = self.maximumblock
	මතකයoper.Memset(uintptr(Pointer(&self.මතකයarray)), 0xFF, self.usedblock/Blockperbyte)
}
func (self *Physicalමතකයmanager) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Physicalමතකයmanager) Pageroundඉහළ(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Physicalමතකයmanager) Pageroundපහළ(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
