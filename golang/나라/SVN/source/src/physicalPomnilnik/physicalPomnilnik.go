package physicalPomnilnik

import (
	. "skupno"
	. "unsafe"
)

const (
	BlokVelikost	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootPomnilnikmap struct {
	velikost		uint32
	baseaddressNizko	uint64
	baseaddressVisoko	uint64
	dolžinaNizko		uint64
	dolžinaVisoko		uint64
	Vrsta			uint32
}

func PhymemPreizkus() {
}

var pomnilnikoper Pomnilnikoper = Pomnilnikoper{}

type PhysicalPomnilnikmanager struct {
	pomnilnikVelikost	uint32
	uporabljenoBlok		uint32
	največBlok		uint32
	pomnilnikPolje		[]uint32
}

var (
	največBlok			uint32	= 0
	pomnilnikPolje			[]uint32
	grubmultibootPomnilnikmapt	multibootPomnilnikmap
)

func (sam *PhysicalPomnilnikmanager) Množicabit(bit uint32) uint32 {
	sam.pomnilnikPolje[bit/32] = sam.pomnilnikPolje[bit/32] | (1 << (bit % 32))
	return sam.pomnilnikPolje[bit/32]
}
func (sam *PhysicalPomnilnikmanager) Toggle_allocation_bit(bit uint32) uint32 {
	sam.pomnilnikPolje[bit/32] = sam.pomnilnikPolje[bit/32] ^ (1 << (bit % 32))
	return sam.pomnilnikPolje[bit/32]
}
func (sam *PhysicalPomnilnikmanager) Preizkusbit(bit uint32) uint32 {
	ret := sam.pomnilnikPolje[bit/32] & (1 << (bit % 32))
	return ret
}
func (sam *PhysicalPomnilnikmanager) SkupnoBlok() uint32 {
	return sam.največBlok
}
func (sam *PhysicalPomnilnikmanager) UporabljenoBlok() uint32 {
	return sam.uporabljenoBlok
}
func (sam *PhysicalPomnilnikmanager) KoličinaodPomnilnik() uint32 {
	return sam.pomnilnikVelikost
}
func (sam *PhysicalPomnilnikmanager) GetbitmaspVelikost() uint32 {
	return sam.pomnilnikVelikost / BlokVelikost / Blokperbyte
}

func (sam *PhysicalPomnilnikmanager) PrviProsto() uint32 {
	for i := uint32(0); i < sam.SkupnoBlok(); i++ {
		if sam.pomnilnikPolje[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (pomnilnikPolje[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (sam *PhysicalPomnilnikmanager) PrviProstoVelikost(velikost uint32) uint32 {
	if velikost == 0 {
		return 0xffffffff
	}
	if velikost == 1 {
		return sam.PrviProsto()
	}

	for i := uint32(0); i < sam.SkupnoBlok(); i++ {
		if sam.pomnilnikPolje[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if sam.pomnilnikPolje[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var prosto uint32 = 0
					for count := uint32(0); count <= velikost; count++ {
						if sam.Preizkusbit(startingbit+count) == 0 {
							prosto++
						}

						if prosto == velikost {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (sam *PhysicalPomnilnikmanager) Init(velikost uint32, bitmap []uint32) {
	sam.pomnilnikVelikost = velikost
	sam.pomnilnikPolje = bitmap
	sam.največBlok = velikost / BlokVelikost
	sam.uporabljenoBlok = sam.največBlok
	pomnilnikoper.Memmnožica(uintptr(Pointer(&sam.pomnilnikPolje)), 0xFF, sam.uporabljenoBlok/Blokperbyte)
}
func (sam *PhysicalPomnilnikmanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (sam *PhysicalPomnilnikmanager) StranNajbližjecelošteviloštevilaxGor(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (sam *PhysicalPomnilnikmanager) StranNajbližjecelošteviloštevilaxDol(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
