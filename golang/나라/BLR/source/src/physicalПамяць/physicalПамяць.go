/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalПамяць

import (
	. "агульныязнакі"
	. "unsafe"
)

const (
	БлокПамер	uint32	= 4 * 1024
	Блокperbyte	uint32	= 8
)

type multibootПамяцьmap struct {
	памер			uint32
	baseaddressНізкі	uint64
	baseaddressВысокі	uint64
	даўжыняНізкі		uint64
	даўжыняВысокі		uint64
	Тып			uint32
}

func PhymemПраверка() {
}

var памяцьoper Памяцьoper = Памяцьoper{}

type PhysicalПамяцьmanager struct {
	памяцьПамер	uint32
	выкарыстанаБлок	uint32
	максімумБлок	uint32
	памяцьМасіў	[]uint32
}

var (
	максімумБлок		uint32	= 0
	памяцьМасіў		[]uint32
	grubmultibootПамяцьmapt	multibootПамяцьmap
)

func (self *PhysicalПамяцьmanager) Вызначанаbit(bit uint32) uint32 {
	self.памяцьМасіў[bit/32] = self.памяцьМасіў[bit/32] | (1 << (bit % 32))
	return self.памяцьМасіў[bit/32]
}
func (self *PhysicalПамяцьmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.памяцьМасіў[bit/32] = self.памяцьМасіў[bit/32] ^ (1 << (bit % 32))
	return self.памяцьМасіў[bit/32]
}
func (self *PhysicalПамяцьmanager) Праверкаbit(bit uint32) uint32 {
	ret := self.памяцьМасіў[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalПамяцьmanager) АгуламБлок() uint32 {
	return self.максімумБлок
}
func (self *PhysicalПамяцьmanager) ВыкарыстанаБлок() uint32 {
	return self.выкарыстанаБлок
}
func (self *PhysicalПамяцьmanager) АгуламзПамяць() uint32 {
	return self.памяцьПамер
}
func (self *PhysicalПамяцьmanager) GetbitmaspПамер() uint32 {
	return self.памяцьПамер / БлокПамер / Блокperbyte
}

func (self *PhysicalПамяцьmanager) FirstВольна() uint32 {
	for i := uint32(0); i < self.АгуламБлок(); i++ {
		if self.памяцьМасіў[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (памяцьМасіў[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalПамяцьmanager) FirstВольнаПамер(памер uint32) uint32 {
	if памер == 0 {
		return 0xffffffff
	}
	if памер == 1 {
		return self.FirstВольна()
	}

	for i := uint32(0); i < self.АгуламБлок(); i++ {
		if self.памяцьМасіў[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.памяцьМасіў[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var вольна uint32 = 0
					for count := uint32(0); count <= памер; count++ {
						if self.Праверкаbit(startingbit+count) == 0 {
							вольна++
						}

						if вольна == памер {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalПамяцьmanager) Init(памер uint32, bitmap []uint32) {
	self.памяцьПамер = памер
	self.памяцьМасіў = bitmap
	self.максімумБлок = памер / БлокПамер
	self.выкарыстанаБлок = self.максімумБлок
	памяцьoper.Memвызначана(uintptr(Pointer(&self.памяцьМасіў)), 0xFF, self.выкарыстанаБлок/Блокperbyte)
}
func (self *PhysicalПамяцьmanager) AllocateБлок() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalПамяцьmanager) СтаронкаАкругленнеВышэй(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalПамяцьmanager) СтаронкаАкругленнеУніз(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
