/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMemória

import (
	. "közös"
	. "unsafe"
)

const (
	BlokkMéret	uint32	= 4 * 1024
	Blokkperbyte	uint32	= 8
)

type multibootMemóriamap struct {
	méret			uint32
	baseaddressAlacsony	uint64
	baseaddressMagas	uint64
	hosszAlacsony		uint64
	hosszMagas		uint64
	Típus			uint32
}

func PhymemTeszt() {
}

var memóriaoper Memóriaoper = Memóriaoper{}

type PhysicalMemóriamanager struct {
	memóriaMéret	uint32
	használtBlokk	uint32
	maximumBlokk	uint32
	memóriaTömb	[]uint32
}

var (
	maximumBlokk			uint32	= 0
	memóriaTömb			[]uint32
	grubmultibootMemóriamapt	multibootMemóriamap
)

func (self *PhysicalMemóriamanager) Halmazbit(bit uint32) uint32 {
	self.memóriaTömb[bit/32] = self.memóriaTömb[bit/32] | (1 << (bit % 32))
	return self.memóriaTömb[bit/32]
}
func (self *PhysicalMemóriamanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.memóriaTömb[bit/32] = self.memóriaTömb[bit/32] ^ (1 << (bit % 32))
	return self.memóriaTömb[bit/32]
}
func (self *PhysicalMemóriamanager) Tesztbit(bit uint32) uint32 {
	ret := self.memóriaTömb[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalMemóriamanager) ÖsszesenBlokk() uint32 {
	return self.maximumBlokk
}
func (self *PhysicalMemóriamanager) HasználtBlokk() uint32 {
	return self.használtBlokk
}
func (self *PhysicalMemóriamanager) MennyiségofMemória() uint32 {
	return self.memóriaMéret
}
func (self *PhysicalMemóriamanager) GetbitmaspMéret() uint32 {
	return self.memóriaMéret / BlokkMéret / Blokkperbyte
}

func (self *PhysicalMemóriamanager) FirstSzabad() uint32 {
	for i := uint32(0); i < self.ÖsszesenBlokk(); i++ {
		if self.memóriaTömb[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memóriaTömb[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalMemóriamanager) FirstSzabadMéret(méret uint32) uint32 {
	if méret == 0 {
		return 0xffffffff
	}
	if méret == 1 {
		return self.FirstSzabad()
	}

	for i := uint32(0); i < self.ÖsszesenBlokk(); i++ {
		if self.memóriaTömb[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.memóriaTömb[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var szabad uint32 = 0
					for számláló := uint32(0); számláló <= méret; számláló++ {
						if self.Tesztbit(startingbit+számláló) == 0 {
							szabad++
						}

						if szabad == méret {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalMemóriamanager) Init(méret uint32, bitmap []uint32) {
	self.memóriaMéret = méret
	self.memóriaTömb = bitmap
	self.maximumBlokk = méret / BlokkMéret
	self.használtBlokk = self.maximumBlokk
	memóriaoper.Memhalmaz(uintptr(Pointer(&self.memóriaTömb)), 0xFF, self.használtBlokk/Blokkperbyte)
}
func (self *PhysicalMemóriamanager) AllocateBlokk() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalMemóriamanager) OldalKerekítésFel(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalMemóriamanager) OldalKerekítésLe(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
