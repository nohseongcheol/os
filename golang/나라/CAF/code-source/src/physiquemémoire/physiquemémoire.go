package physiquemémoire

import (
	. "commun"
	. "unsafe"
)

const (
	BlocTaille	uint32	= 4 * 1024
	Blocperoctet	uint32	= 8
)

type multibootmémoirecarte struct {
	taille			uint32
	baseaddressBasse	uint64
	baseaddressÉlevée	uint64
	duréeBasse		uint64
	duréeÉlevée		uint64
	TypeValeur		uint32
}

func PhymemTester() {
}

var mémoireoper Mémoireoper = Mémoireoper{}

type Physiquemémoiregestionnaire struct {
	mémoireTaille	uint32
	utiliséBloc	uint32
	maximumBloc	uint32
	mémoiretableau	[]uint32
}

var (
	maximumBloc			uint32	= 0
	mémoiretableau			[]uint32
	grubmultibootmémoirecartet	multibootmémoirecarte
)

func (self *Physiquemémoiregestionnaire) Ensemblebit(bit uint32) uint32 {
	self.mémoiretableau[bit/32] = self.mémoiretableau[bit/32] | (1 << (bit % 32))
	return self.mémoiretableau[bit/32]
}
func (self *Physiquemémoiregestionnaire) Inverser_le_bit_de_réservation(bit uint32) uint32 {
	self.mémoiretableau[bit/32] = self.mémoiretableau[bit/32] ^ (1 << (bit % 32))
	return self.mémoiretableau[bit/32]
}
func (self *Physiquemémoiregestionnaire) Testerbit(bit uint32) uint32 {
	ret := self.mémoiretableau[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Physiquemémoiregestionnaire) TotalBloc() uint32 {
	return self.maximumBloc
}
func (self *Physiquemémoiregestionnaire) UtiliséBloc() uint32 {
	return self.utiliséBloc
}
func (self *Physiquemémoiregestionnaire) Quantitésurmémoire() uint32 {
	return self.mémoireTaille
}
func (self *Physiquemémoiregestionnaire) GetbitmaspTaille() uint32 {
	return self.mémoireTaille / BlocTaille / Blocperoctet
}

func (self *Physiquemémoiregestionnaire) FirstLibre() uint32 {
	for i := uint32(0); i < self.TotalBloc(); i++ {
		if self.mémoiretableau[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (mémoiretableau[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Physiquemémoiregestionnaire) FirstLibreTaille(taille uint32) uint32 {
	if taille == 0 {
		return 0xffffffff
	}
	if taille == 1 {
		return self.FirstLibre()
	}

	for i := uint32(0); i < self.TotalBloc(); i++ {
		if self.mémoiretableau[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.mémoiretableau[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var libre uint32 = 0
					for nombre := uint32(0); nombre <= taille; nombre++ {
						if self.Testerbit(startingbit+nombre) == 0 {
							libre++
						}

						if libre == taille {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Physiquemémoiregestionnaire) Init(taille uint32, carte_des_allocations []uint32) {
	self.mémoireTaille = taille
	self.mémoiretableau = carte_des_allocations
	self.maximumBloc = taille / BlocTaille
	self.utiliséBloc = self.maximumBloc
	mémoireoper.Memensemble(uintptr(Pointer(&self.mémoiretableau)), 0xFF, self.utiliséBloc/Blocperoctet)
}
func (self *Physiquemémoiregestionnaire) AllocateBloc() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Physiquemémoiregestionnaire) PageArrondiHaut(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Physiquemémoiregestionnaire) PageArrondiVerslebas(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
