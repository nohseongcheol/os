/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalXotira

import (
	. "common"
	. "unsafe"
)

const (
	BlokHajmi	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootXotiramap struct {
	hajmi			uint32
	baseaddressPast		uint64
	baseaddressYuqori	uint64
	uzunlikPast		uint64
	uzunlikYuqori		uint64
	Turi			uint32
}

func PhymemSinash() {
}

var xotiraoper Xotiraoper = Xotiraoper{}

type PhysicalXotiramanager struct {
	xotiraHajmi	uint32
	ishlatilganBlok	uint32
	maksimumBlok	uint32
	xotiraarray	[]uint32
}

var (
	maksimumBlok		uint32	= 0
	xotiraarray		[]uint32
	grubmultibootXotiramapt	multibootXotiramap
)

func (self *PhysicalXotiramanager) Setbit(bit uint32) uint32 {
	self.xotiraarray[bit/32] = self.xotiraarray[bit/32] | (1 << (bit % 32))
	return self.xotiraarray[bit/32]
}
func (self *PhysicalXotiramanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.xotiraarray[bit/32] = self.xotiraarray[bit/32] ^ (1 << (bit % 32))
	return self.xotiraarray[bit/32]
}
func (self *PhysicalXotiramanager) Sinashbit(bit uint32) uint32 {
	ret := self.xotiraarray[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalXotiramanager) JamiBlok() uint32 {
	return self.maksimumBlok
}
func (self *PhysicalXotiramanager) IshlatilganBlok() uint32 {
	return self.ishlatilganBlok
}
func (self *PhysicalXotiramanager) AmountofXotira() uint32 {
	return self.xotiraHajmi
}
func (self *PhysicalXotiramanager) GetbitmaspHajmi() uint32 {
	return self.xotiraHajmi / BlokHajmi / Blokperbyte
}

func (self *PhysicalXotiramanager) FirstBosh() uint32 {
	for i := uint32(0); i < self.JamiBlok(); i++ {
		if self.xotiraarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (xotiraarray[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalXotiramanager) FirstBoshHajmi(hajmi uint32) uint32 {
	if hajmi == 0 {
		return 0xffffffff
	}
	if hajmi == 1 {
		return self.FirstBosh()
	}

	for i := uint32(0); i < self.JamiBlok(); i++ {
		if self.xotiraarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.xotiraarray[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var bosh uint32 = 0
					for count := uint32(0); count <= hajmi; count++ {
						if self.Sinashbit(startingbit+count) == 0 {
							bosh++
						}

						if bosh == hajmi {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalXotiramanager) Init(hajmi uint32, bitmap []uint32) {
	self.xotiraHajmi = hajmi
	self.xotiraarray = bitmap
	self.maksimumBlok = hajmi / BlokHajmi
	self.ishlatilganBlok = self.maksimumBlok
	xotiraoper.Memset(uintptr(Pointer(&self.xotiraarray)), 0xFF, self.ishlatilganBlok/Blokperbyte)
}
func (self *PhysicalXotiramanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalXotiramanager) SAHIFAroundYuqoriga(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalXotiramanager) SAHIFAroundPastga(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
