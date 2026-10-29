/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalזיכרון

import (
	. "נפוצים"
	. "unsafe"
)

const (
	Bבלוקגודל	uint32	= 4 * 1024
	Bבלוקperbyte	uint32	= 8
)

type multibootזיכרוןmap struct {
	גודל			uint32
	baseaddressנמוך		uint64
	baseaddressגבוהה	uint64
	אורךנמוך		uint64
	אורךגבוהה		uint64
	Tסוג			uint32
}

func Phymemבדיקה() {
}

var זיכרוןoper Mזיכרוןoper = Mזיכרוןoper{}

type Physicalזיכרוןmanager struct {
	זיכרוןגודל	uint32
	בשימושבלוק	uint32
	מרביבלוק	uint32
	זיכרוןמערך	[]uint32
}

var (
	מרביבלוק		uint32	= 0
	זיכרוןמערך		[]uint32
	grubmultibootזיכרוןmapt	multibootזיכרוןmap
)

func (self *Physicalזיכרוןmanager) Sקבעbit(bit uint32) uint32 {
	self.זיכרוןמערך[bit/32] = self.זיכרוןמערך[bit/32] | (1 << (bit % 32))
	return self.זיכרוןמערך[bit/32]
}
func (self *Physicalזיכרוןmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.זיכרוןמערך[bit/32] = self.זיכרוןמערך[bit/32] ^ (1 << (bit % 32))
	return self.זיכרוןמערך[bit/32]
}
func (self *Physicalזיכרוןmanager) Tבדיקהbit(bit uint32) uint32 {
	ret := self.זיכרוןמערך[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Physicalזיכרוןmanager) Totalבלוק() uint32 {
	return self.מרביבלוק
}
func (self *Physicalזיכרוןmanager) Uבשימושבלוק() uint32 {
	return self.בשימושבלוק
}
func (self *Physicalזיכרוןmanager) Aכמותמתוךזיכרון() uint32 {
	return self.זיכרוןגודל
}
func (self *Physicalזיכרוןmanager) Getbitmaspגודל() uint32 {
	return self.זיכרוןגודל / Bבלוקגודל / Bבלוקperbyte
}

func (self *Physicalזיכרוןmanager) Firstפנוי() uint32 {
	for i := uint32(0); i < self.Totalבלוק(); i++ {
		if self.זיכרוןמערך[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (זיכרוןמערך[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Physicalזיכרוןmanager) Firstפנויגודל(גודל uint32) uint32 {
	if גודל == 0 {
		return 0xffffffff
	}
	if גודל == 1 {
		return self.Firstפנוי()
	}

	for i := uint32(0); i < self.Totalבלוק(); i++ {
		if self.זיכרוןמערך[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.זיכרוןמערך[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var פנוי_2 uint32 = 0
					for count := uint32(0); count <= גודל; count++ {
						if self.Tבדיקהbit(startingbit+count) == 0 {
							פנוי_2++
						}

						if פנוי_2 == גודל {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Physicalזיכרוןmanager) Init(גודל uint32, bitmap []uint32) {
	self.זיכרוןגודל = גודל
	self.זיכרוןמערך = bitmap
	self.מרביבלוק = גודל / Bבלוקגודל
	self.בשימושבלוק = self.מרביבלוק
	זיכרוןoper.Memקבע(uintptr(Pointer(&self.זיכרוןמערך)), 0xFF, self.בשימושבלוק/Bבלוקperbyte)
}
func (self *Physicalזיכרוןmanager) Allocateבלוק() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Physicalזיכרוןmanager) Pעמודעיגולמעלה(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Physicalזיכרוןmanager) Pעמודעיגוללמטה(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
