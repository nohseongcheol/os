/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physischSpeicher

import (
	. "gemeinsam"
	. "unsafe"
)

const (
	RechteckGröße	uint32	= 4 * 1024
	RechteckperByte	uint32	= 8
)

type multibootSpeicherAbbildung struct {
	größe			uint32
	baseaddressNiedrig	uint64
	baseaddressHoch		uint64
	längeNiedrig		uint64
	längeHoch		uint64
	Typ			uint32
}

func PhymemTesten() {
}

var speicheroper Speicheroper = Speicheroper{}

type PhysischSpeicherVerwalter struct {
	speicherGröße	uint32
	belegtRechteck	uint32
	maximumRechteck	uint32
	speicherFeld	[]uint32
}

var (
	maximumRechteck			uint32	= 0
	speicherFeld			[]uint32
	grubmultibootSpeicherAbbildungt	multibootSpeicherAbbildung
)

func (selbst *PhysischSpeicherVerwalter) Setzenbit(bit uint32) uint32 {
	selbst.speicherFeld[bit/32] = selbst.speicherFeld[bit/32] | (1 << (bit % 32))
	return selbst.speicherFeld[bit/32]
}
func (selbst *PhysischSpeicherVerwalter) Belegungsbit_umkehren(bit uint32) uint32 {
	selbst.speicherFeld[bit/32] = selbst.speicherFeld[bit/32] ^ (1 << (bit % 32))
	return selbst.speicherFeld[bit/32]
}
func (selbst *PhysischSpeicherVerwalter) Testenbit(bit uint32) uint32 {
	ret := selbst.speicherFeld[bit/32] & (1 << (bit % 32))
	return ret
}
func (selbst *PhysischSpeicherVerwalter) GesamtRechteck() uint32 {
	return selbst.maximumRechteck
}
func (selbst *PhysischSpeicherVerwalter) BelegtRechteck() uint32 {
	return selbst.belegtRechteck
}
func (selbst *PhysischSpeicherVerwalter) MengevonSpeicher() uint32 {
	return selbst.speicherGröße
}
func (selbst *PhysischSpeicherVerwalter) GetbitmaspGröße() uint32 {
	return selbst.speicherGröße / RechteckGröße / RechteckperByte
}

func (selbst *PhysischSpeicherVerwalter) FirstFrei() uint32 {
	for i := uint32(0); i < selbst.GesamtRechteck(); i++ {
		if selbst.speicherFeld[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (speicherFeld[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (selbst *PhysischSpeicherVerwalter) FirstFreiGröße(größe uint32) uint32 {
	if größe == 0 {
		return 0xffffffff
	}
	if größe == 1 {
		return selbst.FirstFrei()
	}

	for i := uint32(0); i < selbst.GesamtRechteck(); i++ {
		if selbst.speicherFeld[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if selbst.speicherFeld[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var frei uint32 = 0
					for anzahl := uint32(0); anzahl <= größe; anzahl++ {
						if selbst.Testenbit(startingbit+anzahl) == 0 {
							frei++
						}

						if frei == größe {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (selbst *PhysischSpeicherVerwalter) Init(größe uint32, belegungsbitkarte []uint32) {
	selbst.speicherGröße = größe
	selbst.speicherFeld = belegungsbitkarte
	selbst.maximumRechteck = größe / RechteckGröße
	selbst.belegtRechteck = selbst.maximumRechteck
	speicheroper.MemSetzen(uintptr(Pointer(&selbst.speicherFeld)), 0xFF, selbst.belegtRechteck/RechteckperByte)
}
func (selbst *PhysischSpeicherVerwalter) AllocateRechteck() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (selbst *PhysischSpeicherVerwalter) SeiteRundenAufwärts(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (selbst *PhysischSpeicherVerwalter) SeiteRundenAbwärts(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
