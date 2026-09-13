package physicalAtmiņa

import (
	. "kopējie"
	. "unsafe"
)

const (
	BloksIzmērs	uint32	= 4 * 1024
	Bloksperbyte	uint32	= 8
)

type multibootAtmiņamap struct {
	izmērs			uint32
	baseaddressKlusi	uint64
	baseaddressAugsta	uint64
	garumsKlusi		uint64
	garumsAugsta		uint64
	Tips			uint32
}

func PhymemPārbaudīt() {
}

var atmiņaoper Atmiņaoper = Atmiņaoper{}

type PhysicalAtmiņamanager struct {
	atmiņaIzmērs	uint32
	izmantotsBloks	uint32
	maksimumsBloks	uint32
	atmiņaMasīvs	[]uint32
}

var (
	maksimumsBloks		uint32	= 0
	atmiņaMasīvs		[]uint32
	grubmultibootAtmiņamapt	multibootAtmiņamap
)

func (pats *PhysicalAtmiņamanager) Kopabit(bit uint32) uint32 {
	pats.atmiņaMasīvs[bit/32] = pats.atmiņaMasīvs[bit/32] | (1 << (bit % 32))
	return pats.atmiņaMasīvs[bit/32]
}
func (pats *PhysicalAtmiņamanager) Toggle_allocation_bit(bit uint32) uint32 {
	pats.atmiņaMasīvs[bit/32] = pats.atmiņaMasīvs[bit/32] ^ (1 << (bit % 32))
	return pats.atmiņaMasīvs[bit/32]
}
func (pats *PhysicalAtmiņamanager) Pārbaudītbit(bit uint32) uint32 {
	ret := pats.atmiņaMasīvs[bit/32] & (1 << (bit % 32))
	return ret
}
func (pats *PhysicalAtmiņamanager) KopāBloks() uint32 {
	return pats.maksimumsBloks
}
func (pats *PhysicalAtmiņamanager) IzmantotsBloks() uint32 {
	return pats.izmantotsBloks
}
func (pats *PhysicalAtmiņamanager) ApjomsnoAtmiņa() uint32 {
	return pats.atmiņaIzmērs
}
func (pats *PhysicalAtmiņamanager) GetbitmaspIzmērs() uint32 {
	return pats.atmiņaIzmērs / BloksIzmērs / Bloksperbyte
}

func (pats *PhysicalAtmiņamanager) PirmaisBrīvs() uint32 {
	for i := uint32(0); i < pats.KopāBloks(); i++ {
		if pats.atmiņaMasīvs[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (atmiņaMasīvs[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (pats *PhysicalAtmiņamanager) PirmaisBrīvsIzmērs(izmērs uint32) uint32 {
	if izmērs == 0 {
		return 0xffffffff
	}
	if izmērs == 1 {
		return pats.PirmaisBrīvs()
	}

	for i := uint32(0); i < pats.KopāBloks(); i++ {
		if pats.atmiņaMasīvs[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if pats.atmiņaMasīvs[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var brīvs uint32 = 0
					for count := uint32(0); count <= izmērs; count++ {
						if pats.Pārbaudītbit(startingbit+count) == 0 {
							brīvs++
						}

						if brīvs == izmērs {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (pats *PhysicalAtmiņamanager) Init(izmērs uint32, bitmap []uint32) {
	pats.atmiņaIzmērs = izmērs
	pats.atmiņaMasīvs = bitmap
	pats.maksimumsBloks = izmērs / BloksIzmērs
	pats.izmantotsBloks = pats.maksimumsBloks
	atmiņaoper.Memkopa(uintptr(Pointer(&pats.atmiņaMasīvs)), 0xFF, pats.izmantotsBloks/Bloksperbyte)
}
func (pats *PhysicalAtmiņamanager) AllocateBloks() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (pats *PhysicalAtmiņamanager) LapaApaļotAugšup(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (pats *PhysicalAtmiņamanager) LapaApaļotLejup(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
