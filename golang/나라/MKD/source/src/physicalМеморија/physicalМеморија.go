/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalМеморија

import (
	. "вообичаено"
	. "unsafe"
)

const (
	BlockГолемина	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootМеморијаmap struct {
	големина	uint32
	baseaddresslow	uint64
	baseaddresshigh	uint64
	должинаlow	uint64
	должинаhigh	uint64
	Тип		uint32
}

func Phymemtest() {
}

var меморијаoper Меморијаoper = Меморијаoper{}

type PhysicalМеморијаmanager struct {
	меморијаГолемина	uint32
	искористеноblock	uint32
	maximumblock		uint32
	меморијаПострои		[]uint32
}

var (
	maximumblock			uint32	= 0
	меморијаПострои			[]uint32
	grubmultibootМеморијаmapt	multibootМеморијаmap
)

func (само *PhysicalМеморијаmanager) Поставиbit(bit uint32) uint32 {
	само.меморијаПострои[bit/32] = само.меморијаПострои[bit/32] | (1 << (bit % 32))
	return само.меморијаПострои[bit/32]
}
func (само *PhysicalМеморијаmanager) Toggle_allocation_bit(bit uint32) uint32 {
	само.меморијаПострои[bit/32] = само.меморијаПострои[bit/32] ^ (1 << (bit % 32))
	return само.меморијаПострои[bit/32]
}
func (само *PhysicalМеморијаmanager) Testbit(bit uint32) uint32 {
	ret := само.меморијаПострои[bit/32] & (1 << (bit % 32))
	return ret
}
func (само *PhysicalМеморијаmanager) Вкупноblock() uint32 {
	return само.maximumblock
}
func (само *PhysicalМеморијаmanager) Искористеноblock() uint32 {
	return само.искористеноblock
}
func (само *PhysicalМеморијаmanager) СуманаМеморија() uint32 {
	return само.меморијаГолемина
}
func (само *PhysicalМеморијаmanager) GetbitmaspГолемина() uint32 {
	return само.меморијаГолемина / BlockГолемина / Blockperbyte
}

func (само *PhysicalМеморијаmanager) FirstСлободни() uint32 {
	for i := uint32(0); i < само.Вкупноblock(); i++ {
		if само.меморијаПострои[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (меморијаПострои[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (само *PhysicalМеморијаmanager) FirstСлободниГолемина(големина uint32) uint32 {
	if големина == 0 {
		return 0xffffffff
	}
	if големина == 1 {
		return само.FirstСлободни()
	}

	for i := uint32(0); i < само.Вкупноblock(); i++ {
		if само.меморијаПострои[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if само.меморијаПострои[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var слободни uint32 = 0
					for count := uint32(0); count <= големина; count++ {
						if само.Testbit(startingbit+count) == 0 {
							слободни++
						}

						if слободни == големина {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (само *PhysicalМеморијаmanager) Init(големина uint32, bitmap []uint32) {
	само.меморијаГолемина = големина
	само.меморијаПострои = bitmap
	само.maximumblock = големина / BlockГолемина
	само.искористеноblock = само.maximumblock
	меморијаoper.Memпостави(uintptr(Pointer(&само.меморијаПострои)), 0xFF, само.искористеноblock/Blockperbyte)
}
func (само *PhysicalМеморијаmanager) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (само *PhysicalМеморијаmanager) СтраницаЗаокружиГоре(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (само *PhysicalМеморијаmanager) СтраницаЗаокружиДолу(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
