/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalیادداشت

import (
	. "common"
	. "unsafe"
)

const (
	Blockحجم	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootیادداشتmap struct {
	حجم			uint32
	baseaddressکم		uint64
	baseaddressاونچا	uint64
	طولکم			uint64
	طولاونچا		uint64
	Tنوعیت			uint32
}

func Phymemٹیسٹ() {
}

var یادداشتoper Mیادداشتoper = Mیادداشتoper{}

type Physicalیادداشتmanager struct {
	یادداشتحجم		uint32
	استعمالشدہblock		uint32
	زیادہسےزیادہblock	uint32
	یادداشتلڑی		[]uint32
}

var (
	زیادہسےزیادہblock		uint32	= 0
	یادداشتلڑی			[]uint32
	grubmultibootیادداشتmapt	multibootیادداشتmap
)

func (self *Physicalیادداشتmanager) Sسیٹbit(bit uint32) uint32 {
	self.یادداشتلڑی[bit/32] = self.یادداشتلڑی[bit/32] | (1 << (bit % 32))
	return self.یادداشتلڑی[bit/32]
}
func (self *Physicalیادداشتmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.یادداشتلڑی[bit/32] = self.یادداشتلڑی[bit/32] ^ (1 << (bit % 32))
	return self.یادداشتلڑی[bit/32]
}
func (self *Physicalیادداشتmanager) Tٹیسٹbit(bit uint32) uint32 {
	ret := self.یادداشتلڑی[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Physicalیادداشتmanager) Tمیزانblock() uint32 {
	return self.زیادہسےزیادہblock
}
func (self *Physicalیادداشتmanager) Uاستعمالشدہblock() uint32 {
	return self.استعمالشدہblock
}
func (self *Physicalیادداشتmanager) Amountبرائےیادداشت() uint32 {
	return self.یادداشتحجم
}
func (self *Physicalیادداشتmanager) Getbitmaspحجم() uint32 {
	return self.یادداشتحجم / Blockحجم / Blockperbyte
}

func (self *Physicalیادداشتmanager) Firstخالی() uint32 {
	for i := uint32(0); i < self.Tمیزانblock(); i++ {
		if self.یادداشتلڑی[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (یادداشتلڑی[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Physicalیادداشتmanager) Firstخالیحجم(حجم uint32) uint32 {
	if حجم == 0 {
		return 0xffffffff
	}
	if حجم == 1 {
		return self.Firstخالی()
	}

	for i := uint32(0); i < self.Tمیزانblock(); i++ {
		if self.یادداشتلڑی[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.یادداشتلڑی[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var خالی uint32 = 0
					for count := uint32(0); count <= حجم; count++ {
						if self.Tٹیسٹbit(startingbit+count) == 0 {
							خالی++
						}

						if خالی == حجم {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Physicalیادداشتmanager) Init(حجم uint32, bitmap []uint32) {
	self.یادداشتحجم = حجم
	self.یادداشتلڑی = bitmap
	self.زیادہسےزیادہblock = حجم / Blockحجم
	self.استعمالشدہblock = self.زیادہسےزیادہblock
	یادداشتoper.Memسیٹ(uintptr(Pointer(&self.یادداشتلڑی)), 0xFF, self.استعمالشدہblock/Blockperbyte)
}
func (self *Physicalیادداشتmanager) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Physicalیادداشتmanager) Pصفحہroundاوپر(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Physicalیادداشتmanager) Pصفحہroundنیچے(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
