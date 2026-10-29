/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalMinne

import (
	. "vanlig"
	. "unsafe"
)

const (
	BlokkStørrelse	uint32	= 4 * 1024
	Blokkperbyte	uint32	= 8
)

type multibootMinnemap struct {
	størrelse	uint32
	baseaddressLav	uint64
	baseaddressHøy	uint64
	lengdeLav	uint64
	lengdeHøy	uint64
	Filtype		uint32
}

func Phymemtest() {
}

var minneoper Minneoper = Minneoper{}

type PhysicalMinnemanager struct {
	minneStørrelse	uint32
	bruktBlokk	uint32
	maksimumBlokk	uint32
	minneTabell	[]uint32
}

var (
	maksimumBlokk		uint32	= 0
	minneTabell		[]uint32
	grubmultibootMinnemapt	multibootMinnemap
)

func (selv *PhysicalMinnemanager) Settbit(bit uint32) uint32 {
	selv.minneTabell[bit/32] = selv.minneTabell[bit/32] | (1 << (bit % 32))
	return selv.minneTabell[bit/32]
}
func (selv *PhysicalMinnemanager) Toggle_allocation_bit(bit uint32) uint32 {
	selv.minneTabell[bit/32] = selv.minneTabell[bit/32] ^ (1 << (bit % 32))
	return selv.minneTabell[bit/32]
}
func (selv *PhysicalMinnemanager) Testbit(bit uint32) uint32 {
	ret := selv.minneTabell[bit/32] & (1 << (bit % 32))
	return ret
}
func (selv *PhysicalMinnemanager) TotaltBlokk() uint32 {
	return selv.maksimumBlokk
}
func (selv *PhysicalMinnemanager) BruktBlokk() uint32 {
	return selv.bruktBlokk
}
func (selv *PhysicalMinnemanager) BeløpavMinne() uint32 {
	return selv.minneStørrelse
}
func (selv *PhysicalMinnemanager) GetbitmaspStørrelse() uint32 {
	return selv.minneStørrelse / BlokkStørrelse / Blokkperbyte
}

func (selv *PhysicalMinnemanager) FirstLedig() uint32 {
	for i := uint32(0); i < selv.TotaltBlokk(); i++ {
		if selv.minneTabell[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (minneTabell[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (selv *PhysicalMinnemanager) FirstLedigStørrelse(størrelse uint32) uint32 {
	if størrelse == 0 {
		return 0xffffffff
	}
	if størrelse == 1 {
		return selv.FirstLedig()
	}

	for i := uint32(0); i < selv.TotaltBlokk(); i++ {
		if selv.minneTabell[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if selv.minneTabell[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var ledig uint32 = 0
					for antall := uint32(0); antall <= størrelse; antall++ {
						if selv.Testbit(startingbit+antall) == 0 {
							ledig++
						}

						if ledig == størrelse {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (selv *PhysicalMinnemanager) Init(størrelse uint32, bitmap []uint32) {
	selv.minneStørrelse = størrelse
	selv.minneTabell = bitmap
	selv.maksimumBlokk = størrelse / BlokkStørrelse
	selv.bruktBlokk = selv.maksimumBlokk
	minneoper.MemSett(uintptr(Pointer(&selv.minneTabell)), 0xFF, selv.bruktBlokk/Blokkperbyte)
}
func (selv *PhysicalMinnemanager) AllocateBlokk() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (selv *PhysicalMinnemanager) SideRundavOpp(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (selv *PhysicalMinnemanager) SideRundavNed(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
