/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalЭси

import (
	. "common"
	. "unsafe"
)

const (
	БлокӨлчөм	uint32	= 4 * 1024
	Блокperbyte	uint32	= 8
)

type multibootЭсиmap struct {
	өлчөм		uint32
	baseaddresslow	uint64
	baseaddresshigh	uint64
	узундукlow	uint64
	узундукhigh	uint64
	Түрү		uint32
}

func PhymemТекшерүү() {
}

var эсиoper Эсиoper = Эсиoper{}

type PhysicalЭсиmanager struct {
	эсиӨлчөм		uint32
	колдонулганыБлок	uint32
	жогоркучегиБлок		uint32
	эсиМассив		[]uint32
}

var (
	жогоркучегиБлок		uint32	= 0
	эсиМассив		[]uint32
	grubmultibootЭсиmapt	multibootЭсиmap
)

func (self *PhysicalЭсиmanager) Setbit(bit uint32) uint32 {
	self.эсиМассив[bit/32] = self.эсиМассив[bit/32] | (1 << (bit % 32))
	return self.эсиМассив[bit/32]
}
func (self *PhysicalЭсиmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.эсиМассив[bit/32] = self.эсиМассив[bit/32] ^ (1 << (bit % 32))
	return self.эсиМассив[bit/32]
}
func (self *PhysicalЭсиmanager) Текшерүүbit(bit uint32) uint32 {
	ret := self.эсиМассив[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalЭсиmanager) БардыгыБлок() uint32 {
	return self.жогоркучегиБлок
}
func (self *PhysicalЭсиmanager) КолдонулганыБлок() uint32 {
	return self.колдонулганыБлок
}
func (self *PhysicalЭсиmanager) AmountofЭси() uint32 {
	return self.эсиӨлчөм
}
func (self *PhysicalЭсиmanager) GetbitmaspӨлчөм() uint32 {
	return self.эсиӨлчөм / БлокӨлчөм / Блокperbyte
}

func (self *PhysicalЭсиmanager) Firstбош() uint32 {
	for i := uint32(0); i < self.БардыгыБлок(); i++ {
		if self.эсиМассив[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (эсиМассив[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalЭсиmanager) FirstбошӨлчөм(өлчөм uint32) uint32 {
	if өлчөм == 0 {
		return 0xffffffff
	}
	if өлчөм == 1 {
		return self.Firstбош()
	}

	for i := uint32(0); i < self.БардыгыБлок(); i++ {
		if self.эсиМассив[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.эсиМассив[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var бош uint32 = 0
					for count := uint32(0); count <= өлчөм; count++ {
						if self.Текшерүүbit(startingbit+count) == 0 {
							бош++
						}

						if бош == өлчөм {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalЭсиmanager) Init(өлчөм uint32, bitmap []uint32) {
	self.эсиӨлчөм = өлчөм
	self.эсиМассив = bitmap
	self.жогоркучегиБлок = өлчөм / БлокӨлчөм
	self.колдонулганыБлок = self.жогоркучегиБлок
	эсиoper.Memset(uintptr(Pointer(&self.эсиМассив)), 0xFF, self.колдонулганыБлок/Блокperbyte)
}
func (self *PhysicalЭсиmanager) AllocateБлок() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalЭсиmanager) БАРАКТегеректөөӨйдө(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalЭсиmanager) БАРАКТегеректөөdown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
