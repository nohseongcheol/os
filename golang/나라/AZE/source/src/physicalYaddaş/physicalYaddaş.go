package physicalYaddaş

import (
	. "ümumi"
	. "unsafe"
)

const (
	BlockBöyüklük	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootYaddaşmap struct {
	böyüklük		uint32
	baseaddressAlçaq	uint64
	baseaddresshigh		uint64
	lengthAlçaq		uint64
	lengthhigh		uint64
	Növ			uint32
}

func Phymemtest() {
}

var yaddaşoper Yaddaşoper = Yaddaşoper{}

type PhysicalYaddaşmanager struct {
	yaddaşBöyüklük	uint32
	istifadədəblock	uint32
	maximumblock	uint32
	yaddaşarray	[]uint32
}

var (
	maximumblock		uint32	= 0
	yaddaşarray		[]uint32
	grubmultibootYaddaşmapt	multibootYaddaşmap
)

func (self *PhysicalYaddaşmanager) Setbit(bit uint32) uint32 {
	self.yaddaşarray[bit/32] = self.yaddaşarray[bit/32] | (1 << (bit % 32))
	return self.yaddaşarray[bit/32]
}
func (self *PhysicalYaddaşmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.yaddaşarray[bit/32] = self.yaddaşarray[bit/32] ^ (1 << (bit % 32))
	return self.yaddaşarray[bit/32]
}
func (self *PhysicalYaddaşmanager) Testbit(bit uint32) uint32 {
	ret := self.yaddaşarray[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalYaddaşmanager) Cəmiblock() uint32 {
	return self.maximumblock
}
func (self *PhysicalYaddaşmanager) İstifadədəblock() uint32 {
	return self.istifadədəblock
}
func (self *PhysicalYaddaşmanager) AmountofYaddaş() uint32 {
	return self.yaddaşBöyüklük
}
func (self *PhysicalYaddaşmanager) GetbitmaspBöyüklük() uint32 {
	return self.yaddaşBöyüklük / BlockBöyüklük / Blockperbyte
}

func (self *PhysicalYaddaşmanager) FirstBoş() uint32 {
	for i := uint32(0); i < self.Cəmiblock(); i++ {
		if self.yaddaşarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (yaddaşarray[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalYaddaşmanager) FirstBoşBöyüklük(böyüklük uint32) uint32 {
	if böyüklük == 0 {
		return 0xffffffff
	}
	if böyüklük == 1 {
		return self.FirstBoş()
	}

	for i := uint32(0); i < self.Cəmiblock(); i++ {
		if self.yaddaşarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.yaddaşarray[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var boş uint32 = 0
					for count := uint32(0); count <= böyüklük; count++ {
						if self.Testbit(startingbit+count) == 0 {
							boş++
						}

						if boş == böyüklük {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalYaddaşmanager) Init(böyüklük uint32, bitmap []uint32) {
	self.yaddaşBöyüklük = böyüklük
	self.yaddaşarray = bitmap
	self.maximumblock = böyüklük / BlockBöyüklük
	self.istifadədəblock = self.maximumblock
	yaddaşoper.Memset(uintptr(Pointer(&self.yaddaşarray)), 0xFF, self.istifadədəblock/Blockperbyte)
}
func (self *PhysicalYaddaşmanager) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalYaddaşmanager) SəhifəroundYuxarı(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalYaddaşmanager) Səhifərounddown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
