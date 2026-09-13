package physicalПамять

import (
	. "звичайний"
	. "unsafe"
)

const (
	БлокРозмір	uint32	= 4 * 1024
	Блокperbyte	uint32	= 8
)

type multibootПамятьmap struct {
	розмір			uint32
	baseАдресаНизька	uint64
	baseАдресаВисокий	uint64
	довжинаНизька		uint64
	довжинаВисокий		uint64
	Тип			uint32
}

func PhymemТест() {
}

var памятьoper Памятьoper = Памятьoper{}

type PhysicalПамятьmanager struct {
	памятьРозмір	uint32
	використаноБлок	uint32
	максимумБлок	uint32
	памятьМасив	[]uint32
}

var (
	максимумБлок		uint32	= 0
	памятьМасив		[]uint32
	grubmultibootПамятьmapt	multibootПамятьmap
)

func (поточний *PhysicalПамятьmanager) Множинабіт(біт uint32) uint32 {
	поточний.памятьМасив[біт/32] = поточний.памятьМасив[біт/32] | (1 << (біт % 32))
	return поточний.памятьМасив[біт/32]
}
func (поточний *PhysicalПамятьmanager) Інвертувати_біт_зайнятості(біт uint32) uint32 {
	поточний.памятьМасив[біт/32] = поточний.памятьМасив[біт/32] ^ (1 << (біт % 32))
	return поточний.памятьМасив[біт/32]
}
func (поточний *PhysicalПамятьmanager) Тестбіт(біт uint32) uint32 {
	ret := поточний.памятьМасив[біт/32] & (1 << (біт % 32))
	return ret
}
func (поточний *PhysicalПамятьmanager) УсьогоБлок() uint32 {
	return поточний.максимумБлок
}
func (поточний *PhysicalПамятьmanager) ВикористаноБлок() uint32 {
	return поточний.використаноБлок
}
func (поточний *PhysicalПамятьmanager) КількістьзПамять() uint32 {
	return поточний.памятьРозмір
}
func (поточний *PhysicalПамятьmanager) GetbitmaspРозмір() uint32 {
	return поточний.памятьРозмір / БлокРозмір / Блокperbyte
}

func (поточний *PhysicalПамятьmanager) FirstВільно() uint32 {
	for i := uint32(0); i < поточний.УсьогоБлок(); i++ {
		if поточний.памятьМасив[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				біт := uint32(1 << j)
				if (памятьМасив[i] & біт) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (поточний *PhysicalПамятьmanager) FirstВільноРозмір(розмір uint32) uint32 {
	if розмір == 0 {
		return 0xffffffff
	}
	if розмір == 1 {
		return поточний.FirstВільно()
	}

	for i := uint32(0); i < поточний.УсьогоБлок(); i++ {
		if поточний.памятьМасив[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var біт uint32 = 1 << j

				if поточний.памятьМасив[j]&біт == 0 {
					var startingбіт uint32 = i * 32
					startingбіт += j

					var вільно uint32 = 0
					for відлік := uint32(0); відлік <= розмір; відлік++ {
						if поточний.Тестбіт(startingбіт+відлік) == 0 {
							вільно++
						}

						if вільно == розмір {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (поточний *PhysicalПамятьmanager) Init(розмір uint32, карта_зайнятості []uint32) {
	поточний.памятьРозмір = розмір
	поточний.памятьМасив = карта_зайнятості
	поточний.максимумБлок = розмір / БлокРозмір
	поточний.використаноБлок = поточний.максимумБлок
	памятьoper.Memмножина(uintptr(Pointer(&поточний.памятьМасив)), 0xFF, поточний.використаноБлок/Блокperbyte)
}
func (поточний *PhysicalПамятьmanager) AllocateБлок() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (поточний *PhysicalПамятьmanager) СторінкаКолоВгору(адреса_2 uint32) uint32 {
	if (адреса_2 & 0xFFFFF000) != адреса_2 {
		адреса_2 = адреса_2 & 0xFFFFF000
		адреса_2 = адреса_2 + 0x1000
	}
	return адреса_2
}
func (поточний *PhysicalПамятьmanager) СторінкаКолоВниз(адреса_2 uint32) uint32 {
	return адреса_2 & 0xFFFFF000
}
