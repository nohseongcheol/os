package physicalUbubiko

import (
	. "common"
	. "unsafe"
)

const (
	BlockIngano	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootUbubikomap struct {
	ingano		uint32
	baseaddresslow	uint64
	baseaddresshigh	uint64
	lengthlow	uint64
	lengthhigh	uint64
	Ubwoko_2	uint32
}

func Phymemtest() {
}

var ububikooper Ububikooper = Ububikooper{}

type PhysicalUbubikomanager struct {
	ububikoIngano		uint32
	usedblock		uint32
	maximumblock		uint32
	ububikoImbonerahamwe	[]uint32
}

var (
	maximumblock			uint32	= 0
	ububikoImbonerahamwe		[]uint32
	grubmultibootUbubikomapt	multibootUbubikomap
)

func (self *PhysicalUbubikomanager) Setbit(bit uint32) uint32 {
	self.ububikoImbonerahamwe[bit/32] = self.ububikoImbonerahamwe[bit/32] | (1 << (bit % 32))
	return self.ububikoImbonerahamwe[bit/32]
}
func (self *PhysicalUbubikomanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.ububikoImbonerahamwe[bit/32] = self.ububikoImbonerahamwe[bit/32] ^ (1 << (bit % 32))
	return self.ububikoImbonerahamwe[bit/32]
}
func (self *PhysicalUbubikomanager) Testbit(bit uint32) uint32 {
	ret := self.ububikoImbonerahamwe[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalUbubikomanager) Igiteranyoblock() uint32 {
	return self.maximumblock
}
func (self *PhysicalUbubikomanager) Usedblock() uint32 {
	return self.usedblock
}
func (self *PhysicalUbubikomanager) AmountofUbubiko() uint32 {
	return self.ububikoIngano
}
func (self *PhysicalUbubikomanager) GetbitmaspIngano() uint32 {
	return self.ububikoIngano / BlockIngano / Blockperbyte
}

func (self *PhysicalUbubikomanager) FirstKigenga() uint32 {
	for i := uint32(0); i < self.Igiteranyoblock(); i++ {
		if self.ububikoImbonerahamwe[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (ububikoImbonerahamwe[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalUbubikomanager) FirstKigengaIngano(ingano uint32) uint32 {
	if ingano == 0 {
		return 0xffffffff
	}
	if ingano == 1 {
		return self.FirstKigenga()
	}

	for i := uint32(0); i < self.Igiteranyoblock(); i++ {
		if self.ububikoImbonerahamwe[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.ububikoImbonerahamwe[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var kigenga uint32 = 0
					for count := uint32(0); count <= ingano; count++ {
						if self.Testbit(startingbit+count) == 0 {
							kigenga++
						}

						if kigenga == ingano {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalUbubikomanager) Init(ingano uint32, bitmap []uint32) {
	self.ububikoIngano = ingano
	self.ububikoImbonerahamwe = bitmap
	self.maximumblock = ingano / BlockIngano
	self.usedblock = self.maximumblock
	ububikooper.Memset(uintptr(Pointer(&self.ububikoImbonerahamwe)), 0xFF, self.usedblock/Blockperbyte)
}
func (self *PhysicalUbubikomanager) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalUbubikomanager) Ipajiroundup(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalUbubikomanager) Ipajirounddown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
