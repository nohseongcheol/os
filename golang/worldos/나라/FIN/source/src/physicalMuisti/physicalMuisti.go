/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMuisti

import (
	. "yhteinen"
	. "unsafe"
)

const (
	LohkoKoko	uint32	= 4 * 1024
	Lohkoperbyte	uint32	= 8
)

type multibootMuistimap struct {
	koko			uint32
	baseaddressMatala	uint64
	baseaddressKorkea	uint64
	kestoMatala		uint64
	kestoKorkea		uint64
	Tyyppi			uint32
}

func PhymemKokeile() {
}

var muistioper Muistioper = Muistioper{}

type PhysicalMuistimanager struct {
	muistiKoko	uint32
	käyttöLohko	uint32
	suurinLohko	uint32
	muistiTaulukko	[]uint32
}

var (
	suurinLohko		uint32	= 0
	muistiTaulukko		[]uint32
	grubmultibootMuistimapt	multibootMuistimap
)

func (itse *PhysicalMuistimanager) Asetabit(bit uint32) uint32 {
	itse.muistiTaulukko[bit/32] = itse.muistiTaulukko[bit/32] | (1 << (bit % 32))
	return itse.muistiTaulukko[bit/32]
}
func (itse *PhysicalMuistimanager) Käännä_varausbitti(bit uint32) uint32 {
	itse.muistiTaulukko[bit/32] = itse.muistiTaulukko[bit/32] ^ (1 << (bit % 32))
	return itse.muistiTaulukko[bit/32]
}
func (itse *PhysicalMuistimanager) Kokeilebit(bit uint32) uint32 {
	ret := itse.muistiTaulukko[bit/32] & (1 << (bit % 32))
	return ret
}
func (itse *PhysicalMuistimanager) YhteensäLohko() uint32 {
	return itse.suurinLohko
}
func (itse *PhysicalMuistimanager) KäyttöLohko() uint32 {
	return itse.käyttöLohko
}
func (itse *PhysicalMuistimanager) MääräofMuisti() uint32 {
	return itse.muistiKoko
}
func (itse *PhysicalMuistimanager) GetbitmaspKoko() uint32 {
	return itse.muistiKoko / LohkoKoko / Lohkoperbyte
}

func (itse *PhysicalMuistimanager) FirstVapaana() uint32 {
	for i := uint32(0); i < itse.YhteensäLohko(); i++ {
		if itse.muistiTaulukko[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (muistiTaulukko[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (itse *PhysicalMuistimanager) FirstVapaanaKoko(koko uint32) uint32 {
	if koko == 0 {
		return 0xffffffff
	}
	if koko == 1 {
		return itse.FirstVapaana()
	}

	for i := uint32(0); i < itse.YhteensäLohko(); i++ {
		if itse.muistiTaulukko[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if itse.muistiTaulukko[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var vapaana uint32 = 0
					for count := uint32(0); count <= koko; count++ {
						if itse.Kokeilebit(startingbit+count) == 0 {
							vapaana++
						}

						if vapaana == koko {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (itse *PhysicalMuistimanager) Init(koko uint32, varausbittikartta []uint32) {
	itse.muistiKoko = koko
	itse.muistiTaulukko = varausbittikartta
	itse.suurinLohko = koko / LohkoKoko
	itse.käyttöLohko = itse.suurinLohko
	muistioper.Memaseta(uintptr(Pointer(&itse.muistiTaulukko)), 0xFF, itse.käyttöLohko/Lohkoperbyte)
}
func (itse *PhysicalMuistimanager) AllocateLohko() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (itse *PhysicalMuistimanager) SivuroundYlös(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (itse *PhysicalMuistimanager) SivuroundAlas(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
