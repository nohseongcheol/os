/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalማስታወሻ

import (
	. "common"
	. "unsafe"
)

const (
	Bመከልከያመጠን	uint32	= 4 * 1024
	Bመከልከያperbyte	uint32	= 8
)

type multibootማስታወሻmap struct {
	መጠን		uint32
	baseaddressዝቅተኛ	uint64
	baseaddressከፍተኛ	uint64
	እርዝመትዝቅተኛ	uint64
	እርዝመትከፍተኛ	uint64
	Tአይነት		uint32
}

func Phymemመሞከሪያ() {
}

var ማስታወሻoper Mማስታወሻoper = Mማስታወሻoper{}

type Physicalማስታወሻmanager struct {
	ማስታወሻመጠን	uint32
	የተጠቀሙትመከልከያ	uint32
	ከፍተኛመከልከያ	uint32
	ማስታወሻማዘጋጃ	[]uint32
}

var (
	ከፍተኛመከልከያ		uint32	= 0
	ማስታወሻማዘጋጃ		[]uint32
	grubmultibootማስታወሻmapt	multibootማስታወሻmap
)

func (self *Physicalማስታወሻmanager) Setbit(bit uint32) uint32 {
	self.ማስታወሻማዘጋጃ[bit/32] = self.ማስታወሻማዘጋጃ[bit/32] | (1 << (bit % 32))
	return self.ማስታወሻማዘጋጃ[bit/32]
}
func (self *Physicalማስታወሻmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.ማስታወሻማዘጋጃ[bit/32] = self.ማስታወሻማዘጋጃ[bit/32] ^ (1 << (bit % 32))
	return self.ማስታወሻማዘጋጃ[bit/32]
}
func (self *Physicalማስታወሻmanager) Tመሞከሪያbit(bit uint32) uint32 {
	ret := self.ማስታወሻማዘጋጃ[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Physicalማስታወሻmanager) Tጠቅላላመከልከያ() uint32 {
	return self.ከፍተኛመከልከያ
}
func (self *Physicalማስታወሻmanager) Uየተጠቀሙትመከልከያ() uint32 {
	return self.የተጠቀሙትመከልከያ
}
func (self *Physicalማስታወሻmanager) Amountከማስታወሻ() uint32 {
	return self.ማስታወሻመጠን
}
func (self *Physicalማስታወሻmanager) Getbitmaspመጠን() uint32 {
	return self.ማስታወሻመጠን / Bመከልከያመጠን / Bመከልከያperbyte
}

func (self *Physicalማስታወሻmanager) Firstነፃ() uint32 {
	for i := uint32(0); i < self.Tጠቅላላመከልከያ(); i++ {
		if self.ማስታወሻማዘጋጃ[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (ማስታወሻማዘጋጃ[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Physicalማስታወሻmanager) Firstነፃመጠን(መጠን uint32) uint32 {
	if መጠን == 0 {
		return 0xffffffff
	}
	if መጠን == 1 {
		return self.Firstነፃ()
	}

	for i := uint32(0); i < self.Tጠቅላላመከልከያ(); i++ {
		if self.ማስታወሻማዘጋጃ[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.ማስታወሻማዘጋጃ[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var ነፃ uint32 = 0
					for count := uint32(0); count <= መጠን; count++ {
						if self.Tመሞከሪያbit(startingbit+count) == 0 {
							ነፃ++
						}

						if ነፃ == መጠን {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Physicalማስታወሻmanager) Init(መጠን uint32, bitmap []uint32) {
	self.ማስታወሻመጠን = መጠን
	self.ማስታወሻማዘጋጃ = bitmap
	self.ከፍተኛመከልከያ = መጠን / Bመከልከያመጠን
	self.የተጠቀሙትመከልከያ = self.ከፍተኛመከልከያ
	ማስታወሻoper.Memset(uintptr(Pointer(&self.ማስታወሻማዘጋጃ)), 0xFF, self.የተጠቀሙትመከልከያ/Bመከልከያperbyte)
}
func (self *Physicalማስታወሻmanager) Allocateመከልከያ() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Physicalማስታወሻmanager) Pገጽክብወደላይ(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Physicalማስታወሻmanager) Pገጽክብወደታች(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
