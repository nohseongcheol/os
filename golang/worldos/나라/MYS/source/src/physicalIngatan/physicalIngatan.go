/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalIngatan

import (
	. "biasa"
	. "unsafe"
)

const (
	BlokSaiz	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootIngatanmap struct {
	saiz			uint32
	baseaddressRendah	uint64
	baseaddressTinggi	uint64
	jarakRendah		uint64
	jarakTinggi		uint64
	Jenis			uint32
}

func PhymemUji() {
}

var ingatanoper Ingatanoper = Ingatanoper{}

type PhysicalIngatanmanager struct {
	ingatanSaiz		uint32
	digunakanBlok		uint32
	maksimumBlok		uint32
	ingatanTatasusunan	[]uint32
}

var (
	maksimumBlok			uint32	= 0
	ingatanTatasusunan		[]uint32
	grubmultibootIngatanmapt	multibootIngatanmap
)

func (diri *PhysicalIngatanmanager) Tetapkanbit(bit uint32) uint32 {
	diri.ingatanTatasusunan[bit/32] = diri.ingatanTatasusunan[bit/32] | (1 << (bit % 32))
	return diri.ingatanTatasusunan[bit/32]
}
func (diri *PhysicalIngatanmanager) Songsangkan_bit_peruntukan(bit uint32) uint32 {
	diri.ingatanTatasusunan[bit/32] = diri.ingatanTatasusunan[bit/32] ^ (1 << (bit % 32))
	return diri.ingatanTatasusunan[bit/32]
}
func (diri *PhysicalIngatanmanager) Ujibit(bit uint32) uint32 {
	ret := diri.ingatanTatasusunan[bit/32] & (1 << (bit % 32))
	return ret
}
func (diri *PhysicalIngatanmanager) JumlahBlok() uint32 {
	return diri.maksimumBlok
}
func (diri *PhysicalIngatanmanager) DigunakanBlok() uint32 {
	return diri.digunakanBlok
}
func (diri *PhysicalIngatanmanager) AmountdariIngatan() uint32 {
	return diri.ingatanSaiz
}
func (diri *PhysicalIngatanmanager) GetbitmaspSaiz() uint32 {
	return diri.ingatanSaiz / BlokSaiz / Blokperbyte
}

func (diri *PhysicalIngatanmanager) FirstBebas() uint32 {
	for i := uint32(0); i < diri.JumlahBlok(); i++ {
		if diri.ingatanTatasusunan[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (ingatanTatasusunan[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (diri *PhysicalIngatanmanager) FirstBebasSaiz(saiz uint32) uint32 {
	if saiz == 0 {
		return 0xffffffff
	}
	if saiz == 1 {
		return diri.FirstBebas()
	}

	for i := uint32(0); i < diri.JumlahBlok(); i++ {
		if diri.ingatanTatasusunan[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if diri.ingatanTatasusunan[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var bebas uint32 = 0
					for count := uint32(0); count <= saiz; count++ {
						if diri.Ujibit(startingbit+count) == 0 {
							bebas++
						}

						if bebas == saiz {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (diri *PhysicalIngatanmanager) Init(saiz uint32, peta_peruntukan []uint32) {
	diri.ingatanSaiz = saiz
	diri.ingatanTatasusunan = peta_peruntukan
	diri.maksimumBlok = saiz / BlokSaiz
	diri.digunakanBlok = diri.maksimumBlok
	ingatanoper.MemTetapkan(uintptr(Pointer(&diri.ingatanTatasusunan)), 0xFF, diri.digunakanBlok/Blokperbyte)
}
func (diri *PhysicalIngatanmanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (diri *PhysicalIngatanmanager) HalamanBulatNaik(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (diri *PhysicalIngatanmanager) HalamanBulatTurun(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
