/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMemòria

import (
	. "comú"
	. "unsafe"
)

const (
	BlocMida	uint32	= 4 * 1024
	Blocperbyte	uint32	= 8
)

type multibootMemòriamap struct {
	mida		uint32
	baseAdreçaBaixa	uint64
	baseAdreçaAlta	uint64
	duradaBaixa	uint64
	duradaAlta	uint64
	Tipus		uint32
}

func PhymemProva() {
}

var memòriaoper Memòriaoper = Memòriaoper{}

type PhysicalMemòriamanager struct {
	memòriaMida	uint32
	utilitzatBloc	uint32
	màximBloc	uint32
	memòriaMatriu	[]uint32
}

var (
	màximBloc			uint32	= 0
	memòriaMatriu			[]uint32
	grubmultibootMemòriamapt	multibootMemòriamap
)

func (unmateix *PhysicalMemòriamanager) Estableixbit(bit uint32) uint32 {
	unmateix.memòriaMatriu[bit/32] = unmateix.memòriaMatriu[bit/32] | (1 << (bit % 32))
	return unmateix.memòriaMatriu[bit/32]
}
func (unmateix *PhysicalMemòriamanager) Toggle_allocation_bit(bit uint32) uint32 {
	unmateix.memòriaMatriu[bit/32] = unmateix.memòriaMatriu[bit/32] ^ (1 << (bit % 32))
	return unmateix.memòriaMatriu[bit/32]
}
func (unmateix *PhysicalMemòriamanager) Provabit(bit uint32) uint32 {
	ret := unmateix.memòriaMatriu[bit/32] & (1 << (bit % 32))
	return ret
}
func (unmateix *PhysicalMemòriamanager) TotalBloc() uint32 {
	return unmateix.màximBloc
}
func (unmateix *PhysicalMemòriamanager) UtilitzatBloc() uint32 {
	return unmateix.utilitzatBloc
}
func (unmateix *PhysicalMemòriamanager) QuantitatdeMemòria() uint32 {
	return unmateix.memòriaMida
}
func (unmateix *PhysicalMemòriamanager) GetbitmaspMida() uint32 {
	return unmateix.memòriaMida / BlocMida / Blocperbyte
}

func (unmateix *PhysicalMemòriamanager) FirstLliure() uint32 {
	for i := uint32(0); i < unmateix.TotalBloc(); i++ {
		if unmateix.memòriaMatriu[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memòriaMatriu[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (unmateix *PhysicalMemòriamanager) FirstLliureMida(mida uint32) uint32 {
	if mida == 0 {
		return 0xffffffff
	}
	if mida == 1 {
		return unmateix.FirstLliure()
	}

	for i := uint32(0); i < unmateix.TotalBloc(); i++ {
		if unmateix.memòriaMatriu[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if unmateix.memòriaMatriu[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var lliure uint32 = 0
					for recompte := uint32(0); recompte <= mida; recompte++ {
						if unmateix.Provabit(startingbit+recompte) == 0 {
							lliure++
						}

						if lliure == mida {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (unmateix *PhysicalMemòriamanager) Init(mida uint32, bitmap []uint32) {
	unmateix.memòriaMida = mida
	unmateix.memòriaMatriu = bitmap
	unmateix.màximBloc = mida / BlocMida
	unmateix.utilitzatBloc = unmateix.màximBloc
	memòriaoper.Memestableix(uintptr(Pointer(&unmateix.memòriaMatriu)), 0xFF, unmateix.utilitzatBloc/Blocperbyte)
}
func (unmateix *PhysicalMemòriamanager) AllocateBloc() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (unmateix *PhysicalMemòriamanager) PàginaArrodoneixAmunt(adreça_2 uint32) uint32 {
	if (adreça_2 & 0xFFFFF000) != adreça_2 {
		adreça_2 = adreça_2 & 0xFFFFF000
		adreça_2 = adreça_2 + 0x1000
	}
	return adreça_2
}
func (unmateix *PhysicalMemòriamanager) PàginaArrodoneixAvall(adreça_2 uint32) uint32 {
	return adreça_2 & 0xFFFFF000
}
