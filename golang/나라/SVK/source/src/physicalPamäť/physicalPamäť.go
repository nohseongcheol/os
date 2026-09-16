/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalPamäť

import (
	. "bežné"
	. "unsafe"
)

const (
	BlokVeľkosť	uint32	= 4 * 1024
	Blokperbyte	uint32	= 8
)

type multibootPamäťmap struct {
	veľkosť			uint32
	baseaddressNízka	uint64
	baseaddressVysoká	uint64
	dĺžkaNízka		uint64
	dĺžkaVysoká		uint64
	Typ			uint32
}

func PhymemOtestovať() {
}

var pamäťoper Pamäťoper = Pamäťoper{}

type PhysicalPamäťmanager struct {
	pamäťVeľkosť	uint32
	využitéBlok	uint32
	maximumBlok	uint32
	pamäťPole	[]uint32
}

var (
	maximumBlok		uint32	= 0
	pamäťPole		[]uint32
	grubmultibootPamäťmapt	multibootPamäťmap
)

func (vlastný *PhysicalPamäťmanager) Sadabit(bit uint32) uint32 {
	vlastný.pamäťPole[bit/32] = vlastný.pamäťPole[bit/32] | (1 << (bit % 32))
	return vlastný.pamäťPole[bit/32]
}
func (vlastný *PhysicalPamäťmanager) Toggle_allocation_bit(bit uint32) uint32 {
	vlastný.pamäťPole[bit/32] = vlastný.pamäťPole[bit/32] ^ (1 << (bit % 32))
	return vlastný.pamäťPole[bit/32]
}
func (vlastný *PhysicalPamäťmanager) Otestovaťbit(bit uint32) uint32 {
	ret := vlastný.pamäťPole[bit/32] & (1 << (bit % 32))
	return ret
}
func (vlastný *PhysicalPamäťmanager) CelkomBlok() uint32 {
	return vlastný.maximumBlok
}
func (vlastný *PhysicalPamäťmanager) VyužitéBlok() uint32 {
	return vlastný.využitéBlok
}
func (vlastný *PhysicalPamäťmanager) MnožstvozPamäť() uint32 {
	return vlastný.pamäťVeľkosť
}
func (vlastný *PhysicalPamäťmanager) GetbitmaspVeľkosť() uint32 {
	return vlastný.pamäťVeľkosť / BlokVeľkosť / Blokperbyte
}

func (vlastný *PhysicalPamäťmanager) FirstVoľné() uint32 {
	for i := uint32(0); i < vlastný.CelkomBlok(); i++ {
		if vlastný.pamäťPole[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (pamäťPole[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (vlastný *PhysicalPamäťmanager) FirstVoľnéVeľkosť(veľkosť uint32) uint32 {
	if veľkosť == 0 {
		return 0xffffffff
	}
	if veľkosť == 1 {
		return vlastný.FirstVoľné()
	}

	for i := uint32(0); i < vlastný.CelkomBlok(); i++ {
		if vlastný.pamäťPole[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if vlastný.pamäťPole[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var voľné uint32 = 0
					for count := uint32(0); count <= veľkosť; count++ {
						if vlastný.Otestovaťbit(startingbit+count) == 0 {
							voľné++
						}

						if voľné == veľkosť {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (vlastný *PhysicalPamäťmanager) Init(veľkosť uint32, bitmap []uint32) {
	vlastný.pamäťVeľkosť = veľkosť
	vlastný.pamäťPole = bitmap
	vlastný.maximumBlok = veľkosť / BlokVeľkosť
	vlastný.využitéBlok = vlastný.maximumBlok
	pamäťoper.Memsada(uintptr(Pointer(&vlastný.pamäťPole)), 0xFF, vlastný.využitéBlok/Blokperbyte)
}
func (vlastný *PhysicalPamäťmanager) AllocateBlok() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (vlastný *PhysicalPamäťmanager) STRANAZaokrúhlenieHore(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (vlastný *PhysicalPamäťmanager) STRANAZaokrúhlenieDole(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
