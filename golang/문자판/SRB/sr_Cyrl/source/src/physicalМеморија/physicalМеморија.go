package physicalМеморија

import (
	. "заједнички"
	. "unsafe"
)

const (
	БлокВеличина	uint32	= 4 * 1024
	Блокperbyte	uint32	= 8
)

type multibootМеморијаmap struct {
	величина		uint32
	baseaddressТихо		uint64
	baseaddressВисока	uint64
	дужинаТихо		uint64
	дужинаВисока		uint64
	Врста			uint32
}

func PhymemТест() {
}

var меморијаoper Меморијаoper = Меморијаoper{}

type PhysicalМеморијаmanager struct {
	меморијаВеличина	uint32
	заузетоБлок		uint32
	највишеБлок		uint32
	меморијаНиз		[]uint32
}

var (
	највишеБлок			uint32	= 0
	меморијаНиз			[]uint32
	grubmultibootМеморијаmapt	multibootМеморијаmap
)

func (исти *PhysicalМеморијаmanager) Скупbit(bit uint32) uint32 {
	исти.меморијаНиз[bit/32] = исти.меморијаНиз[bit/32] | (1 << (bit % 32))
	return исти.меморијаНиз[bit/32]
}
func (исти *PhysicalМеморијаmanager) Toggle_allocation_bit(bit uint32) uint32 {
	исти.меморијаНиз[bit/32] = исти.меморијаНиз[bit/32] ^ (1 << (bit % 32))
	return исти.меморијаНиз[bit/32]
}
func (исти *PhysicalМеморијаmanager) Тестbit(bit uint32) uint32 {
	ret := исти.меморијаНиз[bit/32] & (1 << (bit % 32))
	return ret
}
func (исти *PhysicalМеморијаmanager) УкупноБлок() uint32 {
	return исти.највишеБлок
}
func (исти *PhysicalМеморијаmanager) ЗаузетоБлок() uint32 {
	return исти.заузетоБлок
}
func (исти *PhysicalМеморијаmanager) ИзносодМеморија() uint32 {
	return исти.меморијаВеличина
}
func (исти *PhysicalМеморијаmanager) GetbitmaspВеличина() uint32 {
	return исти.меморијаВеличина / БлокВеличина / Блокperbyte
}

func (исти *PhysicalМеморијаmanager) FirstСлободно() uint32 {
	for i := uint32(0); i < исти.УкупноБлок(); i++ {
		if исти.меморијаНиз[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (меморијаНиз[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (исти *PhysicalМеморијаmanager) FirstСлободноВеличина(величина uint32) uint32 {
	if величина == 0 {
		return 0xffffffff
	}
	if величина == 1 {
		return исти.FirstСлободно()
	}

	for i := uint32(0); i < исти.УкупноБлок(); i++ {
		if исти.меморијаНиз[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if исти.меморијаНиз[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var слободно uint32 = 0
					for count := uint32(0); count <= величина; count++ {
						if исти.Тестbit(startingbit+count) == 0 {
							слободно++
						}

						if слободно == величина {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (исти *PhysicalМеморијаmanager) Init(величина uint32, bitmap []uint32) {
	исти.меморијаВеличина = величина
	исти.меморијаНиз = bitmap
	исти.највишеБлок = величина / БлокВеличина
	исти.заузетоБлок = исти.највишеБлок
	меморијаoper.Memскуп(uintptr(Pointer(&исти.меморијаНиз)), 0xFF, исти.заузетоБлок/Блокperbyte)
}
func (исти *PhysicalМеморијаmanager) AllocateБлок() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (исти *PhysicalМеморијаmanager) СТРАНАЗаокружиГоре(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (исти *PhysicalМеморијаmanager) СТРАНАЗаокружиНиже(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
