package physicalGeheugen

import (
	. "veelvoorkomend"
	. "unsafe"
)

const (
	BlokGrootte	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootGeheugenmap struct {
	grootte		uint32
	baseaddressLaag	uint64
	baseaddressHoog	uint64
	lengteLaag	uint64
	lengteHoog	uint64
	Soort		uint32
}

func PhymemProef() {
}

var geheugenoper Geheugenoper = Geheugenoper{}

type PhysicalGeheugenmanager struct {
	geheugenGrootte	uint32
	gebruiktBlok	uint32
	maximumBlok	uint32
	geheugenReeks	[]uint32
}

var (
	maximumBlok			uint32	= 0
	geheugenReeks			[]uint32
	grubmultibootGeheugenmapt	multibootGeheugenmap
)

func (zelf *PhysicalGeheugenmanager) Instellenbit(bit uint32) uint32 {
	zelf.geheugenReeks[bit/32] = zelf.geheugenReeks[bit/32] | (1 << (bit % 32))
	return zelf.geheugenReeks[bit/32]
}
func (zelf *PhysicalGeheugenmanager) Toewijzingsbit_omkeren(bit uint32) uint32 {
	zelf.geheugenReeks[bit/32] = zelf.geheugenReeks[bit/32] ^ (1 << (bit % 32))
	return zelf.geheugenReeks[bit/32]
}
func (zelf *PhysicalGeheugenmanager) Proefbit(bit uint32) uint32 {
	ret := zelf.geheugenReeks[bit/32] & (1 << (bit % 32))
	return ret
}
func (zelf *PhysicalGeheugenmanager) TotaalBlok() uint32 {
	return zelf.maximumBlok
}
func (zelf *PhysicalGeheugenmanager) GebruiktBlok() uint32 {
	return zelf.gebruiktBlok
}
func (zelf *PhysicalGeheugenmanager) HoeveelheidvanGeheugen() uint32 {
	return zelf.geheugenGrootte
}
func (zelf *PhysicalGeheugenmanager) GetbitmaspGrootte() uint32 {
	return zelf.geheugenGrootte / BlokGrootte / Blokperbyte
}

func (zelf *PhysicalGeheugenmanager) FirstVrij() uint32 {
	for i := uint32(0); i < zelf.TotaalBlok(); i++ {
		if zelf.geheugenReeks[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (geheugenReeks[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (zelf *PhysicalGeheugenmanager) FirstVrijGrootte(grootte uint32) uint32 {
	if grootte == 0 {
		return 0xffffffff
	}
	if grootte == 1 {
		return zelf.FirstVrij()
	}

	for i := uint32(0); i < zelf.TotaalBlok(); i++ {
		if zelf.geheugenReeks[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if zelf.geheugenReeks[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var vrij uint32 = 0
					for aantal := uint32(0); aantal <= grootte; aantal++ {
						if zelf.Proefbit(startingbit+aantal) == 0 {
							vrij++
						}

						if vrij == grootte {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (zelf *PhysicalGeheugenmanager) Init(grootte uint32, toewijzingskaart []uint32) {
	zelf.geheugenGrootte = grootte
	zelf.geheugenReeks = toewijzingskaart
	zelf.maximumBlok = grootte / BlokGrootte
	zelf.gebruiktBlok = zelf.maximumBlok
	geheugenoper.MemInstellen(uintptr(Pointer(&zelf.geheugenReeks)), 0xFF, zelf.gebruiktBlok/Blokperbyte)
}
func (zelf *PhysicalGeheugenmanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (zelf *PhysicalGeheugenmanager) PaginaAfrondenOmhoog(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (zelf *PhysicalGeheugenmanager) PaginaAfrondenOmlaag(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
