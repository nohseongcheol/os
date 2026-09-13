package physicalPamięć

import (
	. "zwykły"
	. "unsafe"
)

const (
	BlokRozmiar	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootPamięćmap struct {
	rozmiar		uint32
	baseAdresNiski	uint64
	baseAdresWysoki	uint64
	długośćNiski	uint64
	długośćWysoki	uint64
	Typ		uint32
}

func PhymemPrzetestuj() {
}

var pamięćoper Pamięćoper = Pamięćoper{}

type PhysicalPamięćmanager struct {
	pamięćRozmiar	uint32
	użytychBlok	uint32
	maksimumBlok	uint32
	pamięćTablica	[]uint32
}

var (
	maksimumBlok		uint32	= 0
	pamięćTablica		[]uint32
	grubmultibootPamięćmapt	multibootPamięćmap
)

func (bieżący *PhysicalPamięćmanager) Zbiórbit(bit uint32) uint32 {
	bieżący.pamięćTablica[bit/32] = bieżący.pamięćTablica[bit/32] | (1 << (bit % 32))
	return bieżący.pamięćTablica[bit/32]
}
func (bieżący *PhysicalPamięćmanager) Odwróć_bit_zajętości(bit uint32) uint32 {
	bieżący.pamięćTablica[bit/32] = bieżący.pamięćTablica[bit/32] ^ (1 << (bit % 32))
	return bieżący.pamięćTablica[bit/32]
}
func (bieżący *PhysicalPamięćmanager) Przetestujbit(bit uint32) uint32 {
	ret := bieżący.pamięćTablica[bit/32] & (1 << (bit % 32))
	return ret
}
func (bieżący *PhysicalPamięćmanager) ŁącznieBlok() uint32 {
	return bieżący.maksimumBlok
}
func (bieżący *PhysicalPamięćmanager) UżytychBlok() uint32 {
	return bieżący.użytychBlok
}
func (bieżący *PhysicalPamięćmanager) IlośćzPamięć() uint32 {
	return bieżący.pamięćRozmiar
}
func (bieżący *PhysicalPamięćmanager) GetbitmaspRozmiar() uint32 {
	return bieżący.pamięćRozmiar / BlokRozmiar / Blokperbyte
}

func (bieżący *PhysicalPamięćmanager) FirstWolne() uint32 {
	for i := uint32(0); i < bieżący.ŁącznieBlok(); i++ {
		if bieżący.pamięćTablica[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (pamięćTablica[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (bieżący *PhysicalPamięćmanager) FirstWolneRozmiar(rozmiar uint32) uint32 {
	if rozmiar == 0 {
		return 0xffffffff
	}
	if rozmiar == 1 {
		return bieżący.FirstWolne()
	}

	for i := uint32(0); i < bieżący.ŁącznieBlok(); i++ {
		if bieżący.pamięćTablica[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if bieżący.pamięćTablica[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var wolne uint32 = 0
					for liczba := uint32(0); liczba <= rozmiar; liczba++ {
						if bieżący.Przetestujbit(startingbit+liczba) == 0 {
							wolne++
						}

						if wolne == rozmiar {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (bieżący *PhysicalPamięćmanager) Init(rozmiar uint32, mapa_zajętości []uint32) {
	bieżący.pamięćRozmiar = rozmiar
	bieżący.pamięćTablica = mapa_zajętości
	bieżący.maksimumBlok = rozmiar / BlokRozmiar
	bieżący.użytychBlok = bieżący.maksimumBlok
	pamięćoper.Memzbiór(uintptr(Pointer(&bieżący.pamięćTablica)), 0xFF, bieżący.użytychBlok/Blokperbyte)
}
func (bieżący *PhysicalPamięćmanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (bieżący *PhysicalPamięćmanager) StronaZaokrąglaGóra(adres_2 uint32) uint32 {
	if (adres_2 & 0xFFFFF000) != adres_2 {
		adres_2 = adres_2 & 0xFFFFF000
		adres_2 = adres_2 + 0x1000
	}
	return adres_2
}
func (bieżący *PhysicalPamięćmanager) StronaZaokrąglaWdół(adres_2 uint32) uint32 {
	return adres_2 & 0xFFFFF000
}
