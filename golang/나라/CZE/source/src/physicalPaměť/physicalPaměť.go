package physicalPaměť

import (
	. "běžné"
	. "unsafe"
)

const (
	BlokovýVelikost	uint32	= 4 * 1024
	Blokovýperbyte	uint32	= 8
)

type multibootPaměťmap struct {
	velikost		uint32
	baseAdresaNízká		uint64
	baseAdresaVysoká	uint64
	délkaNízká		uint64
	délkaVysoká		uint64
	Typ			uint32
}

func PhymemOtestovat() {
}

var paměťoper Paměťoper = Paměťoper{}

type PhysicalPaměťmanager struct {
	paměťVelikost	uint32
	použitoBlokový	uint32
	maximumBlokový	uint32
	paměťPole	[]uint32
}

var (
	maximumBlokový		uint32	= 0
	paměťPole		[]uint32
	grubmultibootPaměťmapt	multibootPaměťmap
)

func (self *PhysicalPaměťmanager) Nastavitbit(bit uint32) uint32 {
	self.paměťPole[bit/32] = self.paměťPole[bit/32] | (1 << (bit % 32))
	return self.paměťPole[bit/32]
}
func (self *PhysicalPaměťmanager) Obrátit_bit_obsazení(bit uint32) uint32 {
	self.paměťPole[bit/32] = self.paměťPole[bit/32] ^ (1 << (bit % 32))
	return self.paměťPole[bit/32]
}
func (self *PhysicalPaměťmanager) Otestovatbit(bit uint32) uint32 {
	ret := self.paměťPole[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalPaměťmanager) CelkemBlokový() uint32 {
	return self.maximumBlokový
}
func (self *PhysicalPaměťmanager) PoužitoBlokový() uint32 {
	return self.použitoBlokový
}
func (self *PhysicalPaměťmanager) MnožstvízPaměť() uint32 {
	return self.paměťVelikost
}
func (self *PhysicalPaměťmanager) GetbitmaspVelikost() uint32 {
	return self.paměťVelikost / BlokovýVelikost / Blokovýperbyte
}

func (self *PhysicalPaměťmanager) FirstVolné() uint32 {
	for i := uint32(0); i < self.CelkemBlokový(); i++ {
		if self.paměťPole[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (paměťPole[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalPaměťmanager) FirstVolnéVelikost(velikost uint32) uint32 {
	if velikost == 0 {
		return 0xffffffff
	}
	if velikost == 1 {
		return self.FirstVolné()
	}

	for i := uint32(0); i < self.CelkemBlokový(); i++ {
		if self.paměťPole[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.paměťPole[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var volné uint32 = 0
					for počet := uint32(0); počet <= velikost; počet++ {
						if self.Otestovatbit(startingbit+počet) == 0 {
							volné++
						}

						if volné == velikost {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalPaměťmanager) Init(velikost uint32, mapa_obsazení []uint32) {
	self.paměťVelikost = velikost
	self.paměťPole = mapa_obsazení
	self.maximumBlokový = velikost / BlokovýVelikost
	self.použitoBlokový = self.maximumBlokový
	paměťoper.MemNastavit(uintptr(Pointer(&self.paměťPole)), 0xFF, self.použitoBlokový/Blokovýperbyte)
}
func (self *PhysicalPaměťmanager) AllocateBlokový() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalPaměťmanager) StránkaZaokrouhlitNahoru(adresa_2 uint32) uint32 {
	if (adresa_2 & 0xFFFFF000) != adresa_2 {
		adresa_2 = adresa_2 & 0xFFFFF000
		adresa_2 = adresa_2 + 0x1000
	}
	return adresa_2
}
func (self *PhysicalPaměťmanager) StránkaZaokrouhlitDolů(adresa_2 uint32) uint32 {
	return adresa_2 & 0xFFFFF000
}
