package physicalHukommelse

import (
	. "almen"
	. "unsafe"
)

const (
	BlokStørrelse	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootHukommelsemap struct {
	størrelse	uint32
	baseaddressLav	uint64
	baseaddressHøj	uint64
	længdeLav	uint64
	længdeHøj	uint64
	TypeVærdi	uint32
}

func PhymemPrøv() {
}

var hukommelseoper Hukommelseoper = Hukommelseoper{}

type PhysicalHukommelsemanager struct {
	hukommelseStørrelse	uint32
	brugtBlok		uint32
	maksimumBlok		uint32
	hukommelseTabel		[]uint32
}

var (
	maksimumBlok			uint32	= 0
	hukommelseTabel			[]uint32
	grubmultibootHukommelsemapt	multibootHukommelsemap
)

func (selv *PhysicalHukommelsemanager) Satbit(bit uint32) uint32 {
	selv.hukommelseTabel[bit/32] = selv.hukommelseTabel[bit/32] | (1 << (bit % 32))
	return selv.hukommelseTabel[bit/32]
}
func (selv *PhysicalHukommelsemanager) Toggle_allocation_bit(bit uint32) uint32 {
	selv.hukommelseTabel[bit/32] = selv.hukommelseTabel[bit/32] ^ (1 << (bit % 32))
	return selv.hukommelseTabel[bit/32]
}
func (selv *PhysicalHukommelsemanager) Prøvbit(bit uint32) uint32 {
	ret := selv.hukommelseTabel[bit/32] & (1 << (bit % 32))
	return ret
}
func (selv *PhysicalHukommelsemanager) TotalBlok() uint32 {
	return selv.maksimumBlok
}
func (selv *PhysicalHukommelsemanager) BrugtBlok() uint32 {
	return selv.brugtBlok
}
func (selv *PhysicalHukommelsemanager) BeløbafHukommelse() uint32 {
	return selv.hukommelseStørrelse
}
func (selv *PhysicalHukommelsemanager) GetbitmaspStørrelse() uint32 {
	return selv.hukommelseStørrelse / BlokStørrelse / Blokperbyte
}

func (selv *PhysicalHukommelsemanager) FirstFri() uint32 {
	for i := uint32(0); i < selv.TotalBlok(); i++ {
		if selv.hukommelseTabel[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (hukommelseTabel[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (selv *PhysicalHukommelsemanager) FirstFriStørrelse(størrelse uint32) uint32 {
	if størrelse == 0 {
		return 0xffffffff
	}
	if størrelse == 1 {
		return selv.FirstFri()
	}

	for i := uint32(0); i < selv.TotalBlok(); i++ {
		if selv.hukommelseTabel[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if selv.hukommelseTabel[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var fri uint32 = 0
					for antal := uint32(0); antal <= størrelse; antal++ {
						if selv.Prøvbit(startingbit+antal) == 0 {
							fri++
						}

						if fri == størrelse {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (selv *PhysicalHukommelsemanager) Init(størrelse uint32, bitmap []uint32) {
	selv.hukommelseStørrelse = størrelse
	selv.hukommelseTabel = bitmap
	selv.maksimumBlok = størrelse / BlokStørrelse
	selv.brugtBlok = selv.maksimumBlok
	hukommelseoper.Memsat(uintptr(Pointer(&selv.hukommelseTabel)), 0xFF, selv.brugtBlok/Blokperbyte)
}
func (selv *PhysicalHukommelsemanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (selv *PhysicalHukommelsemanager) SideAfrundOp(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (selv *PhysicalHukommelsemanager) SideAfrundNed(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
