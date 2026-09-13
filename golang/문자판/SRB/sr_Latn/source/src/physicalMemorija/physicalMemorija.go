package physicalMemorija

import (
	. "zajednički"
	. "unsafe"
)

const (
	BlokVeličina	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootMemorijamap struct {
	veličina		uint32
	baseaddressTiho		uint64
	baseaddressVisoka	uint64
	dužinaTiho		uint64
	dužinaVisoka		uint64
	Vrsta			uint32
}

func PhymemTest() {
}

var memorijaoper Memorijaoper = Memorijaoper{}

type PhysicalMemorijamanager struct {
	memorijaVeličina	uint32
	zauzetoBlok		uint32
	najvišeBlok		uint32
	memorijaNiz		[]uint32
}

var (
	najvišeBlok			uint32	= 0
	memorijaNiz			[]uint32
	grubmultibootMemorijamapt	multibootMemorijamap
)

func (isti *PhysicalMemorijamanager) Skupbit(bit uint32) uint32 {
	isti.memorijaNiz[bit/32] = isti.memorijaNiz[bit/32] | (1 << (bit % 32))
	return isti.memorijaNiz[bit/32]
}
func (isti *PhysicalMemorijamanager) Toggle_allocation_bit(bit uint32) uint32 {
	isti.memorijaNiz[bit/32] = isti.memorijaNiz[bit/32] ^ (1 << (bit % 32))
	return isti.memorijaNiz[bit/32]
}
func (isti *PhysicalMemorijamanager) Testbit(bit uint32) uint32 {
	ret := isti.memorijaNiz[bit/32] & (1 << (bit % 32))
	return ret
}
func (isti *PhysicalMemorijamanager) UkupnoBlok() uint32 {
	return isti.najvišeBlok
}
func (isti *PhysicalMemorijamanager) ZauzetoBlok() uint32 {
	return isti.zauzetoBlok
}
func (isti *PhysicalMemorijamanager) IznosodMemorija() uint32 {
	return isti.memorijaVeličina
}
func (isti *PhysicalMemorijamanager) GetbitmaspVeličina() uint32 {
	return isti.memorijaVeličina / BlokVeličina / Blokperbyte
}

func (isti *PhysicalMemorijamanager) FirstSlobodno() uint32 {
	for i := uint32(0); i < isti.UkupnoBlok(); i++ {
		if isti.memorijaNiz[i] != 0xffffffff {
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
func (isti *PhysicalMemorijamanager) FirstSlobodnoVeličina(veličina uint32) uint32 {
	if veličina == 0 {
		return 0xffffffff
	}
	if veličina == 1 {
		return isti.FirstSlobodno()
	}

	for i := uint32(0); i < isti.UkupnoBlok(); i++ {
		if isti.memorijaNiz[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if isti.memorijaNiz[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var slobodno uint32 = 0
					for count := uint32(0); count <= veličina; count++ {
						if isti.Testbit(startingbit+count) == 0 {
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

func (isti *PhysicalMemorijamanager) Init(veličina uint32, bitmap []uint32) {
	isti.memorijaVeličina = veličina
	isti.memorijaNiz = bitmap
	isti.najvišeBlok = veličina / BlokVeličina
	isti.zauzetoBlok = isti.najvišeBlok
	memorijaoper.Memskup(uintptr(Pointer(&isti.memorijaNiz)), 0xFF, isti.zauzetoBlok/Blokperbyte)
}
func (isti *PhysicalMemorijamanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (isti *PhysicalMemorijamanager) STRANAZaokružiGore(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (isti *PhysicalMemorijamanager) STRANAZaokružiNiže(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
