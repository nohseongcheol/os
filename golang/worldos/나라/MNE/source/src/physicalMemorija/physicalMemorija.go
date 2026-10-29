/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMemorija

import (
	. "заједнички"
	. "unsafe"
)

const (
	BlokВеличина	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootMemorijamap struct {
	величина		uint32
	baseaddressTiho		uint64
	baseaddressВисока	uint64
	dužinaTiho		uint64
	dužinaВисока		uint64
	Врста			uint32
}

func PhymemТест() {
}

var memorijaoper Memorijaoper = Memorijaoper{}

type PhysicalMemorijamanager struct {
	memorijaВеличина	uint32
	zauzetoBlok		uint32
	najvišeBlok		uint32
	memorijaНиз		[]uint32
}

var (
	najvišeBlok			uint32	= 0
	memorijaНиз			[]uint32
	grubmultibootMemorijamapt	multibootMemorijamap
)

func (isti *PhysicalMemorijamanager) Скупbit(bit uint32) uint32 {
	isti.memorijaНиз[bit/32] = isti.memorijaНиз[bit/32] | (1 << (bit % 32))
	return isti.memorijaНиз[bit/32]
}
func (isti *PhysicalMemorijamanager) Toggle_allocation_bit(bit uint32) uint32 {
	isti.memorijaНиз[bit/32] = isti.memorijaНиз[bit/32] ^ (1 << (bit % 32))
	return isti.memorijaНиз[bit/32]
}
func (isti *PhysicalMemorijamanager) Тестbit(bit uint32) uint32 {
	ret := isti.memorijaНиз[bit/32] & (1 << (bit % 32))
	return ret
}
func (isti *PhysicalMemorijamanager) UkupnoBlok() uint32 {
	return isti.najvišeBlok
}
func (isti *PhysicalMemorijamanager) ZauzetoBlok() uint32 {
	return isti.zauzetoBlok
}
func (isti *PhysicalMemorijamanager) IznosodMemorija() uint32 {
	return isti.memorijaВеличина
}
func (isti *PhysicalMemorijamanager) GetbitmaspВеличина() uint32 {
	return isti.memorijaВеличина / BlokВеличина / Blokperbyte
}

func (isti *PhysicalMemorijamanager) FirstSlobodno() uint32 {
	for i := uint32(0); i < isti.UkupnoBlok(); i++ {
		if isti.memorijaНиз[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memorijaНиз[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (isti *PhysicalMemorijamanager) FirstSlobodnoВеличина(величина uint32) uint32 {
	if величина == 0 {
		return 0xffffffff
	}
	if величина == 1 {
		return isti.FirstSlobodno()
	}

	for i := uint32(0); i < isti.UkupnoBlok(); i++ {
		if isti.memorijaНиз[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if isti.memorijaНиз[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var slobodno uint32 = 0
					for count := uint32(0); count <= величина; count++ {
						if isti.Тестbit(startingbit+count) == 0 {
							slobodno++
						}

						if slobodno == величина {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (isti *PhysicalMemorijamanager) Init(величина uint32, bitmap []uint32) {
	isti.memorijaВеличина = величина
	isti.memorijaНиз = bitmap
	isti.najvišeBlok = величина / BlokВеличина
	isti.zauzetoBlok = isti.najvišeBlok
	memorijaoper.Memскуп(uintptr(Pointer(&isti.memorijaНиз)), 0xFF, isti.zauzetoBlok/Blokperbyte)
}
func (isti *PhysicalMemorijamanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (isti *PhysicalMemorijamanager) ListZaokružiGore(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (isti *PhysicalMemorijamanager) ListZaokružiНиже(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
