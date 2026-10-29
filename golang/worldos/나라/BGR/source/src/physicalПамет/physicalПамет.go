/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalПамет

import (
	. "честосрещани"
	. "unsafe"
)

const (
	БлокРазмер	uint32	= 4 * 1024
	Блокperbyte	uint32	= 8
)

type multibootПаметmap struct {
	размер			uint32
	baseaddressНисък	uint64
	baseaddressВисок	uint64
	дължинаНисък		uint64
	дължинаВисок		uint64
	Тип			uint32
}

func PhymemТест() {
}

var паметoper Паметoper = Паметoper{}

type PhysicalПаметmanager struct {
	паметРазмер	uint32
	използваноБлок	uint32
	максимумБлок	uint32
	паметМасив	[]uint32
}

var (
	максимумБлок		uint32	= 0
	паметМасив		[]uint32
	grubmultibootПаметmapt	multibootПаметmap
)

func (себеси *PhysicalПаметmanager) Задайbit(bit uint32) uint32 {
	себеси.паметМасив[bit/32] = себеси.паметМасив[bit/32] | (1 << (bit % 32))
	return себеси.паметМасив[bit/32]
}
func (себеси *PhysicalПаметmanager) Toggle_allocation_bit(bit uint32) uint32 {
	себеси.паметМасив[bit/32] = себеси.паметМасив[bit/32] ^ (1 << (bit % 32))
	return себеси.паметМасив[bit/32]
}
func (себеси *PhysicalПаметmanager) Тестbit(bit uint32) uint32 {
	ret := себеси.паметМасив[bit/32] & (1 << (bit % 32))
	return ret
}
func (себеси *PhysicalПаметmanager) ОбщоБлок() uint32 {
	return себеси.максимумБлок
}
func (себеси *PhysicalПаметmanager) ИзползваноБлок() uint32 {
	return себеси.използваноБлок
}
func (себеси *PhysicalПаметmanager) КоличествоотПамет() uint32 {
	return себеси.паметРазмер
}
func (себеси *PhysicalПаметmanager) GetbitmaspРазмер() uint32 {
	return себеси.паметРазмер / БлокРазмер / Блокperbyte
}

func (себеси *PhysicalПаметmanager) FirstСвободно() uint32 {
	for i := uint32(0); i < себеси.ОбщоБлок(); i++ {
		if себеси.паметМасив[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (паметМасив[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (себеси *PhysicalПаметmanager) FirstСвободноРазмер(размер uint32) uint32 {
	if размер == 0 {
		return 0xffffffff
	}
	if размер == 1 {
		return себеси.FirstСвободно()
	}

	for i := uint32(0); i < себеси.ОбщоБлок(); i++ {
		if себеси.паметМасив[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if себеси.паметМасив[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var свободно uint32 = 0
					for count := uint32(0); count <= размер; count++ {
						if себеси.Тестbit(startingbit+count) == 0 {
							свободно++
						}

						if свободно == размер {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (себеси *PhysicalПаметmanager) Init(размер uint32, bitmap []uint32) {
	себеси.паметРазмер = размер
	себеси.паметМасив = bitmap
	себеси.максимумБлок = размер / БлокРазмер
	себеси.използваноБлок = себеси.максимумБлок
	паметoper.MemЗадай(uintptr(Pointer(&себеси.паметМасив)), 0xFF, себеси.използваноБлок/Блокperbyte)
}
func (себеси *PhysicalПаметmanager) AllocateБлок() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (себеси *PhysicalПаметmanager) СтраницаЗакръглянедоцелочисленоНагоре(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (себеси *PhysicalПаметmanager) СтраницаЗакръглянедоцелочисленоНадолу(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
