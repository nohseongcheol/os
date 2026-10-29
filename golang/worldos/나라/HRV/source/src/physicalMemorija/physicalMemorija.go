/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMemorija

import (
	. "uobičajeno"
	. "unsafe"
)

const (
	BlokirajVeličina	uint32	= 4 * 1024
	Blokirajperbyte		uint32	= 8
)

type multibootMemorijamap struct {
	veličina		uint32
	baseaddressNIsko	uint64
	baseaddressVisoko	uint64
	dužinaNIsko		uint64
	dužinaVisoko		uint64
	Vrsta			uint32
}

func PhymemProvjeri() {
}

var memorijaoper Memorijaoper = Memorijaoper{}

type PhysicalMemorijamanager struct {
	memorijaVeličina	uint32
	iskorištenoBlokiraj	uint32
	najvišeBlokiraj		uint32
	memorijaNiz		[]uint32
}

var (
	najvišeBlokiraj			uint32	= 0
	memorijaNiz			[]uint32
	grubmultibootMemorijamapt	multibootMemorijamap
)

func (sam *PhysicalMemorijamanager) Postavibit(bit uint32) uint32 {
	sam.memorijaNiz[bit/32] = sam.memorijaNiz[bit/32] | (1 << (bit % 32))
	return sam.memorijaNiz[bit/32]
}
func (sam *PhysicalMemorijamanager) Toggle_allocation_bit(bit uint32) uint32 {
	sam.memorijaNiz[bit/32] = sam.memorijaNiz[bit/32] ^ (1 << (bit % 32))
	return sam.memorijaNiz[bit/32]
}
func (sam *PhysicalMemorijamanager) Provjeribit(bit uint32) uint32 {
	ret := sam.memorijaNiz[bit/32] & (1 << (bit % 32))
	return ret
}
func (sam *PhysicalMemorijamanager) UkupnoBlokiraj() uint32 {
	return sam.najvišeBlokiraj
}
func (sam *PhysicalMemorijamanager) IskorištenoBlokiraj() uint32 {
	return sam.iskorištenoBlokiraj
}
func (sam *PhysicalMemorijamanager) IznosodMemorija() uint32 {
	return sam.memorijaVeličina
}
func (sam *PhysicalMemorijamanager) GetbitmaspVeličina() uint32 {
	return sam.memorijaVeličina / BlokirajVeličina / Blokirajperbyte
}

func (sam *PhysicalMemorijamanager) FirstSlobodno() uint32 {
	for i := uint32(0); i < sam.UkupnoBlokiraj(); i++ {
		if sam.memorijaNiz[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memorijaNiz[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (sam *PhysicalMemorijamanager) FirstSlobodnoVeličina(veličina uint32) uint32 {
	if veličina == 0 {
		return 0xffffffff
	}
	if veličina == 1 {
		return sam.FirstSlobodno()
	}

	for i := uint32(0); i < sam.UkupnoBlokiraj(); i++ {
		if sam.memorijaNiz[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if sam.memorijaNiz[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var slobodno uint32 = 0
					for count := uint32(0); count <= veličina; count++ {
						if sam.Provjeribit(startingbit+count) == 0 {
							slobodno++
						}

						if slobodno == veličina {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (sam *PhysicalMemorijamanager) Init(veličina uint32, bitmap []uint32) {
	sam.memorijaVeličina = veličina
	sam.memorijaNiz = bitmap
	sam.najvišeBlokiraj = veličina / BlokirajVeličina
	sam.iskorištenoBlokiraj = sam.najvišeBlokiraj
	memorijaoper.MemPostavi(uintptr(Pointer(&sam.memorijaNiz)), 0xFF, sam.iskorištenoBlokiraj/Blokirajperbyte)
}
func (sam *PhysicalMemorijamanager) AllocateBlokiraj() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (sam *PhysicalMemorijamanager) StranicaroundGore(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (sam *PhysicalMemorijamanager) StranicaroundDolje(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
