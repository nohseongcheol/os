/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalΜνήμη

import (
	. "κοινό"
	. "unsafe"
)

const (
	ΜπλοκΜέγεθος	uint32	= 4 * 1024
	Μπλοκperbyte	uint32	= 8
)

type multibootΜνήμηmap struct {
	μέγεθος			uint32
	baseaddressΧαμηλή	uint64
	baseaddressΥψηλή	uint64
	διάρκειαΧαμηλή		uint64
	διάρκειαΥψηλή		uint64
	Τύπος			uint32
}

func PhymemΔοκιμή() {
}

var μνήμηoper Μνήμηoper = Μνήμηoper{}

type PhysicalΜνήμηmanager struct {
	μνήμηΜέγεθος	uint32
	σεχρήσηΜπλοκ	uint32
	μέγιστοΜπλοκ	uint32
	μνήμηΔιάταξη	[]uint32
}

var (
	μέγιστοΜπλοκ		uint32	= 0
	μνήμηΔιάταξη		[]uint32
	grubmultibootΜνήμηmapt	multibootΜνήμηmap
)

func (self *PhysicalΜνήμηmanager) Σύνολοbit(bit uint32) uint32 {
	self.μνήμηΔιάταξη[bit/32] = self.μνήμηΔιάταξη[bit/32] | (1 << (bit % 32))
	return self.μνήμηΔιάταξη[bit/32]
}
func (self *PhysicalΜνήμηmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.μνήμηΔιάταξη[bit/32] = self.μνήμηΔιάταξη[bit/32] ^ (1 << (bit % 32))
	return self.μνήμηΔιάταξη[bit/32]
}
func (self *PhysicalΜνήμηmanager) Δοκιμήbit(bit uint32) uint32 {
	ret := self.μνήμηΔιάταξη[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalΜνήμηmanager) ΣύνολοΜπλοκ() uint32 {
	return self.μέγιστοΜπλοκ
}
func (self *PhysicalΜνήμηmanager) ΣεχρήσηΜπλοκ() uint32 {
	return self.σεχρήσηΜπλοκ
}
func (self *PhysicalΜνήμηmanager) ΠοσόαπόΜνήμη() uint32 {
	return self.μνήμηΜέγεθος
}
func (self *PhysicalΜνήμηmanager) GetbitmaspΜέγεθος() uint32 {
	return self.μνήμηΜέγεθος / ΜπλοκΜέγεθος / Μπλοκperbyte
}

func (self *PhysicalΜνήμηmanager) FirstΕλεύθερα() uint32 {
	for i := uint32(0); i < self.ΣύνολοΜπλοκ(); i++ {
		if self.μνήμηΔιάταξη[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (μνήμηΔιάταξη[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalΜνήμηmanager) FirstΕλεύθεραΜέγεθος(μέγεθος uint32) uint32 {
	if μέγεθος == 0 {
		return 0xffffffff
	}
	if μέγεθος == 1 {
		return self.FirstΕλεύθερα()
	}

	for i := uint32(0); i < self.ΣύνολοΜπλοκ(); i++ {
		if self.μνήμηΔιάταξη[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.μνήμηΔιάταξη[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var ελεύθερα uint32 = 0
					for count := uint32(0); count <= μέγεθος; count++ {
						if self.Δοκιμήbit(startingbit+count) == 0 {
							ελεύθερα++
						}

						if ελεύθερα == μέγεθος {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalΜνήμηmanager) Init(μέγεθος uint32, bitmap []uint32) {
	self.μνήμηΜέγεθος = μέγεθος
	self.μνήμηΔιάταξη = bitmap
	self.μέγιστοΜπλοκ = μέγεθος / ΜπλοκΜέγεθος
	self.σεχρήσηΜπλοκ = self.μέγιστοΜπλοκ
	μνήμηoper.Memσύνολο(uintptr(Pointer(&self.μνήμηΔιάταξη)), 0xFF, self.σεχρήσηΜπλοκ/Μπλοκperbyte)
}
func (self *PhysicalΜνήμηmanager) AllocateΜπλοκ() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalΜνήμηmanager) ΣελίδαΣτρογγυλοποίησηπροςτονπλησιέστεροακέραιοΠάνω(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalΜνήμηmanager) ΣελίδαΣτρογγυλοποίησηπροςτονπλησιέστεροακέραιοΚάτω(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
