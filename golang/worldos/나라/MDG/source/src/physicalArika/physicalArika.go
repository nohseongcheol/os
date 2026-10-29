/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalArika

import (
	. "common"
	. "unsafe"
)

const (
	BlockHabe	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootArikamap struct {
	habe		uint32
	baseaddresslow	uint64
	baseaddresshigh	uint64
	lengthlow	uint64
	lengthhigh	uint64
	Karazana	uint32
}

func Phymemtest() {
}

var arikaoper Arikaoper = Arikaoper{}

type PhysicalArikaMpandrindra struct {
	arikaHabe	uint32
	ampiasainablock	uint32
	maximumblock	uint32
	arikaarray	[]uint32
}

var (
	maximumblock		uint32	= 0
	arikaarray		[]uint32
	grubmultibootArikamapt	multibootArikamap
)

func (nytena *PhysicalArikaMpandrindra) Setbit(bit uint32) uint32 {
	nytena.arikaarray[bit/32] = nytena.arikaarray[bit/32] | (1 << (bit % 32))
	return nytena.arikaarray[bit/32]
}
func (nytena *PhysicalArikaMpandrindra) Toggle_allocation_bit(bit uint32) uint32 {
	nytena.arikaarray[bit/32] = nytena.arikaarray[bit/32] ^ (1 << (bit % 32))
	return nytena.arikaarray[bit/32]
}
func (nytena *PhysicalArikaMpandrindra) Testbit(bit uint32) uint32 {
	ret := nytena.arikaarray[bit/32] & (1 << (bit % 32))
	return ret
}
func (nytena *PhysicalArikaMpandrindra) Tontalinyblock() uint32 {
	return nytena.maximumblock
}
func (nytena *PhysicalArikaMpandrindra) Ampiasainablock() uint32 {
	return nytena.ampiasainablock
}
func (nytena *PhysicalArikaMpandrindra) HabetsakaaminnyArika() uint32 {
	return nytena.arikaHabe
}
func (nytena *PhysicalArikaMpandrindra) GetbitmaspHabe() uint32 {
	return nytena.arikaHabe / BlockHabe / Blockperbyte
}

func (nytena *PhysicalArikaMpandrindra) FirstMalalaka() uint32 {
	for i := uint32(0); i < nytena.Tontalinyblock(); i++ {
		if nytena.arikaarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (arikaarray[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (nytena *PhysicalArikaMpandrindra) FirstMalalakaHabe(habe uint32) uint32 {
	if habe == 0 {
		return 0xffffffff
	}
	if habe == 1 {
		return nytena.FirstMalalaka()
	}

	for i := uint32(0); i < nytena.Tontalinyblock(); i++ {
		if nytena.arikaarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if nytena.arikaarray[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var malalaka uint32 = 0
					for count := uint32(0); count <= habe; count++ {
						if nytena.Testbit(startingbit+count) == 0 {
							malalaka++
						}

						if malalaka == habe {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (nytena *PhysicalArikaMpandrindra) Init(habe uint32, bitmap []uint32) {
	nytena.arikaHabe = habe
	nytena.arikaarray = bitmap
	nytena.maximumblock = habe / BlockHabe
	nytena.ampiasainablock = nytena.maximumblock
	arikaoper.Memset(uintptr(Pointer(&nytena.arikaarray)), 0xFF, nytena.ampiasainablock/Blockperbyte)
}
func (nytena *PhysicalArikaMpandrindra) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (nytena *PhysicalArikaMpandrindra) PEJYroundAmbony(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (nytena *PhysicalArikaMpandrindra) PEJYrounddown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
