package physicalAtmintis

import (
	. "bendrinis"
	. "unsafe"
)

const (
	BlokasDydis	uint32	= 4 * 1024
	Blokasperbyte	uint32	= 8
)

type multibootAtmintismap struct {
	dydis			uint32
	baseaddressŽemas	uint64
	baseaddressAukštas	uint64
	trukmėŽemas		uint64
	trukmėAukštas		uint64
	Tipas			uint32
}

func PhymemTestas() {
}

var atmintisoper Atmintisoper = Atmintisoper{}

type PhysicalAtmintismanager struct {
	atmintisDydis		uint32
	naudojamaBlokas		uint32
	maksimumasBlokas	uint32
	atmintisMasyvas		[]uint32
}

var (
	maksimumasBlokas		uint32	= 0
	atmintisMasyvas			[]uint32
	grubmultibootAtmintismapt	multibootAtmintismap
)

func (self *PhysicalAtmintismanager) Nustatytabit(bit uint32) uint32 {
	self.atmintisMasyvas[bit/32] = self.atmintisMasyvas[bit/32] | (1 << (bit % 32))
	return self.atmintisMasyvas[bit/32]
}
func (self *PhysicalAtmintismanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.atmintisMasyvas[bit/32] = self.atmintisMasyvas[bit/32] ^ (1 << (bit % 32))
	return self.atmintisMasyvas[bit/32]
}
func (self *PhysicalAtmintismanager) Testasbit(bit uint32) uint32 {
	ret := self.atmintisMasyvas[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalAtmintismanager) IšvisoBlokas() uint32 {
	return self.maksimumasBlokas
}
func (self *PhysicalAtmintismanager) NaudojamaBlokas() uint32 {
	return self.naudojamaBlokas
}
func (self *PhysicalAtmintismanager) KiekisišAtmintis() uint32 {
	return self.atmintisDydis
}
func (self *PhysicalAtmintismanager) GetbitmaspDydis() uint32 {
	return self.atmintisDydis / BlokasDydis / Blokasperbyte
}

func (self *PhysicalAtmintismanager) FirstLaisva() uint32 {
	for i := uint32(0); i < self.IšvisoBlokas(); i++ {
		if self.atmintisMasyvas[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (atmintisMasyvas[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalAtmintismanager) FirstLaisvaDydis(dydis uint32) uint32 {
	if dydis == 0 {
		return 0xffffffff
	}
	if dydis == 1 {
		return self.FirstLaisva()
	}

	for i := uint32(0); i < self.IšvisoBlokas(); i++ {
		if self.atmintisMasyvas[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.atmintisMasyvas[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var laisva uint32 = 0
					for count := uint32(0); count <= dydis; count++ {
						if self.Testasbit(startingbit+count) == 0 {
							laisva++
						}

						if laisva == dydis {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalAtmintismanager) Init(dydis uint32, bitmap []uint32) {
	self.atmintisDydis = dydis
	self.atmintisMasyvas = bitmap
	self.maksimumasBlokas = dydis / BlokasDydis
	self.naudojamaBlokas = self.maksimumasBlokas
	atmintisoper.Memnustatyta(uintptr(Pointer(&self.atmintisMasyvas)), 0xFF, self.naudojamaBlokas/Blokasperbyte)
}
func (self *PhysicalAtmintismanager) AllocateBlokas() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalAtmintismanager) PuslapisApvalintiAukštyn(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalAtmintismanager) PuslapisApvalintiŽemyn(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
