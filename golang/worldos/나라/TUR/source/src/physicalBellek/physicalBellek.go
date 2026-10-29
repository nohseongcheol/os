/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalBellek

import (
	. "genel"
	. "unsafe"
)

const (
	BlokBoyut	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootBellekmap struct {
	boyut			uint32
	baseaddressDüşük	uint64
	baseaddressYüksek	uint64
	süreDüşük		uint64
	süreYüksek		uint64
	Tür			uint32
}

func PhymemDene() {
}

var bellekoper Bellekoper = Bellekoper{}

type PhysicalBellekmanager struct {
	bellekBoyut	uint32
	kullanılanBlok	uint32
	enÇokBlok	uint32
	bellekDizi	[]uint32
}

var (
	enÇokBlok		uint32	= 0
	bellekDizi		[]uint32
	grubmultibootBellekmapt	multibootBellekmap
)

func (self *PhysicalBellekmanager) Ayarlabit(bit uint32) uint32 {
	self.bellekDizi[bit/32] = self.bellekDizi[bit/32] | (1 << (bit % 32))
	return self.bellekDizi[bit/32]
}
func (self *PhysicalBellekmanager) Ayırma_bitini_tersle(bit uint32) uint32 {
	self.bellekDizi[bit/32] = self.bellekDizi[bit/32] ^ (1 << (bit % 32))
	return self.bellekDizi[bit/32]
}
func (self *PhysicalBellekmanager) Denebit(bit uint32) uint32 {
	ret := self.bellekDizi[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalBellekmanager) ToplamBlok() uint32 {
	return self.enÇokBlok
}
func (self *PhysicalBellekmanager) KullanılanBlok() uint32 {
	return self.kullanılanBlok
}
func (self *PhysicalBellekmanager) MiktarofBellek() uint32 {
	return self.bellekBoyut
}
func (self *PhysicalBellekmanager) GetbitmaspBoyut() uint32 {
	return self.bellekBoyut / BlokBoyut / Blokperbyte
}

func (self *PhysicalBellekmanager) FirstBoş() uint32 {
	for i := uint32(0); i < self.ToplamBlok(); i++ {
		if self.bellekDizi[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (bellekDizi[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalBellekmanager) FirstBoşBoyut(boyut uint32) uint32 {
	if boyut == 0 {
		return 0xffffffff
	}
	if boyut == 1 {
		return self.FirstBoş()
	}

	for i := uint32(0); i < self.ToplamBlok(); i++ {
		if self.bellekDizi[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.bellekDizi[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var boş uint32 = 0
					for count := uint32(0); count <= boyut; count++ {
						if self.Denebit(startingbit+count) == 0 {
							boş++
						}

						if boş == boyut {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalBellekmanager) Init(boyut uint32, ayırma_bit_eşlemi []uint32) {
	self.bellekBoyut = boyut
	self.bellekDizi = ayırma_bit_eşlemi
	self.enÇokBlok = boyut / BlokBoyut
	self.kullanılanBlok = self.enÇokBlok
	bellekoper.Memayarla(uintptr(Pointer(&self.bellekDizi)), 0xFF, self.kullanılanBlok/Blokperbyte)
}
func (self *PhysicalBellekmanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalBellekmanager) SayfaYuvarlaYukarı(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalBellekmanager) SayfaYuvarlaAşağı(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
