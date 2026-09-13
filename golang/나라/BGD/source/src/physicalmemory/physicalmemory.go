package physicalmemory

import (
	. "common"
	. "unsafe"
)

const (
	Blocksize	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootmemorymap struct {
	size		uint32
	baseaddresslow	uint64
	baseaddresshigh	uint64
	lengthlow	uint64
	lengthhigh	uint64
	Tধরণ		uint32
}

func Phymemtest() {
}

var memoryoper Memoryoper = Memoryoper{}

type Physicalmemorymanager struct {
	memorysize	uint32
	usedblock	uint32
	maximumblock	uint32
	memoryarray	[]uint32
}

var (
	maximumblock		uint32	= 0
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
func (self *Physicalmemorymanager) Totalblock() uint32 {
	return self.maximumblock
}
func (self *Physicalmemorymanager) Usedblock() uint32 {
	return self.usedblock
}
func (self *Physicalmemorymanager) Amountofmemory() uint32 {
	return self.memorysize
}
func (self *Physicalmemorymanager) Getbitmaspsize() uint32 {
	return self.memorysize / Blocksize / Blockperbyte
}

func (self *Physicalmemorymanager) Firstfree() uint32 {
	for i := uint32(0); i < self.Totalblock(); i++ {
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
func (self *Physicalmemorymanager) Firstfreesize(size uint32) uint32 {
	if size == 0 {
		return 0xffffffff
	}
	if size == 1 {
		return self.Firstfree()
	}

	for i := uint32(0); i < self.Totalblock(); i++ {
		if self.memoryarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.memoryarray[j]&bit == 0 {
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

func (self *Physicalmemorymanager) Init(size uint32, bitmap []uint32) {
	self.memorysize = size
	self.memoryarray = bitmap
	self.maximumblock = size / Blocksize
	self.usedblock = self.maximumblock
	memoryoper.Memset(uintptr(Pointer(&self.memoryarray)), 0xFF, self.usedblock/Blockperbyte)
}
func (self *Physicalmemorymanager) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Physicalmemorymanager) Pageroundউপর(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Physicalmemorymanager) Pagerounddown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
