package physicalMälu

import (
	. "üldine"
	. "unsafe"
)

const (
	KastSuurus	uint32	= 4 * 1024
	Kastperbyte	uint32	= 8
)

type multibootMälumap struct {
	suurus			uint32
	baseaddressMadal	uint64
	baseaddressKõrge	uint64
	kestusMadal		uint64
	kestusKõrge		uint64
	Liik			uint32
}

func PhymemTesti() {
}

var mäluoper Mäluoper = Mäluoper{}

type PhysicalMälumanager struct {
	mäluSuurus	uint32
	kasutusesKast	uint32
	suurimKast	uint32
	mäluMassiiv	[]uint32
}

var (
	suurimKast		uint32	= 0
	mäluMassiiv		[]uint32
	grubmultibootMälumapt	multibootMälumap
)

func (ise *PhysicalMälumanager) Määrabiti(biti uint32) uint32 {
	ise.mäluMassiiv[biti/32] = ise.mäluMassiiv[biti/32] | (1 << (biti % 32))
	return ise.mäluMassiiv[biti/32]
}
func (ise *PhysicalMälumanager) Toggle_allocation_bit(biti uint32) uint32 {
	ise.mäluMassiiv[biti/32] = ise.mäluMassiiv[biti/32] ^ (1 << (biti % 32))
	return ise.mäluMassiiv[biti/32]
}
func (ise *PhysicalMälumanager) Testibiti(biti uint32) uint32 {
	ret := ise.mäluMassiiv[biti/32] & (1 << (biti % 32))
	return ret
}
func (ise *PhysicalMälumanager) KokkuKast() uint32 {
	return ise.suurimKast
}
func (ise *PhysicalMälumanager) KasutusesKast() uint32 {
	return ise.kasutusesKast
}
func (ise *PhysicalMälumanager) KogusofMälu() uint32 {
	return ise.mäluSuurus
}
func (ise *PhysicalMälumanager) GetbitmaspSuurus() uint32 {
	return ise.mäluSuurus / KastSuurus / Kastperbyte
}

func (ise *PhysicalMälumanager) FirstVaba() uint32 {
	for i := uint32(0); i < ise.KokkuKast(); i++ {
		if ise.mäluMassiiv[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				biti := uint32(1 << j)
				if (mäluMassiiv[i] & biti) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (ise *PhysicalMälumanager) FirstVabaSuurus(suurus uint32) uint32 {
	if suurus == 0 {
		return 0xffffffff
	}
	if suurus == 1 {
		return ise.FirstVaba()
	}

	for i := uint32(0); i < ise.KokkuKast(); i++ {
		if ise.mäluMassiiv[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var biti uint32 = 1 << j

				if ise.mäluMassiiv[j]&biti == 0 {
					var startingbiti uint32 = i * 32
					startingbiti += j

					var vaba uint32 = 0
					for count := uint32(0); count <= suurus; count++ {
						if ise.Testibiti(startingbiti+count) == 0 {
							vaba++
						}

						if vaba == suurus {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (ise *PhysicalMälumanager) Init(suurus uint32, bitmap []uint32) {
	ise.mäluSuurus = suurus
	ise.mäluMassiiv = bitmap
	ise.suurimKast = suurus / KastSuurus
	ise.kasutusesKast = ise.suurimKast
	mäluoper.MemMäära(uintptr(Pointer(&ise.mäluMassiiv)), 0xFF, ise.kasutusesKast/Kastperbyte)
}
func (ise *PhysicalMälumanager) AllocateKast() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (ise *PhysicalMälumanager) LehekülgÜmardamineÜles(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (ise *PhysicalMälumanager) LehekülgÜmardamineNoolalla(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
