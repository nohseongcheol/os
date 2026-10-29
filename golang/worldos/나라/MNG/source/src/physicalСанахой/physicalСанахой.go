/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalСанахой

import (
	. "үндсэн"
	. "unsafe"
)

const (
	BlockХэмжээ	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootСанахойmap struct {
	хэмжээ				uint32
	baseaddressБага			uint64
	baseaddressБүрэнцэнэглэгдсэн	uint64
	lengthБага			uint64
	lengthБүрэнцэнэглэгдсэн		uint64
	Төрөл				uint32
}

func Phymemtest() {
}

var санахойoper Санахойoper = Санахойoper{}

type PhysicalСанахойЗохицуулагч struct {
	санахойХэмжээ		uint32
	хэрэглэгдсэнblock	uint32
	maximumblock		uint32
	санахойarray		[]uint32
}

var (
	maximumblock			uint32	= 0
	санахойarray			[]uint32
	grubmultibootСанахойmapt	multibootСанахойmap
)

func (self *PhysicalСанахойЗохицуулагч) Setbit(bit uint32) uint32 {
	self.санахойarray[bit/32] = self.санахойarray[bit/32] | (1 << (bit % 32))
	return self.санахойarray[bit/32]
}
func (self *PhysicalСанахойЗохицуулагч) Toggle_allocation_bit(bit uint32) uint32 {
	self.санахойarray[bit/32] = self.санахойarray[bit/32] ^ (1 << (bit % 32))
	return self.санахойarray[bit/32]
}
func (self *PhysicalСанахойЗохицуулагч) Testbit(bit uint32) uint32 {
	ret := self.санахойarray[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalСанахойЗохицуулагч) Нийтblock() uint32 {
	return self.maximumblock
}
func (self *PhysicalСанахойЗохицуулагч) Хэрэглэгдсэнblock() uint32 {
	return self.хэрэглэгдсэнblock
}
func (self *PhysicalСанахойЗохицуулагч) AmountofСанахой() uint32 {
	return self.санахойХэмжээ
}
func (self *PhysicalСанахойЗохицуулагч) GetbitmaspХэмжээ() uint32 {
	return self.санахойХэмжээ / BlockХэмжээ / Blockperbyte
}

func (self *PhysicalСанахойЗохицуулагч) FirstЧөлөөт() uint32 {
	for i := uint32(0); i < self.Нийтblock(); i++ {
		if self.санахойarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (санахойarray[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalСанахойЗохицуулагч) FirstЧөлөөтХэмжээ(хэмжээ uint32) uint32 {
	if хэмжээ == 0 {
		return 0xffffffff
	}
	if хэмжээ == 1 {
		return self.FirstЧөлөөт()
	}

	for i := uint32(0); i < self.Нийтblock(); i++ {
		if self.санахойarray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.санахойarray[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var чөлөөт uint32 = 0
					for count := uint32(0); count <= хэмжээ; count++ {
						if self.Testbit(startingbit+count) == 0 {
							чөлөөт++
						}

						if чөлөөт == хэмжээ {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalСанахойЗохицуулагч) Init(хэмжээ uint32, bitmap []uint32) {
	self.санахойХэмжээ = хэмжээ
	self.санахойarray = bitmap
	self.maximumblock = хэмжээ / BlockХэмжээ
	self.хэрэглэгдсэнblock = self.maximumblock
	санахойoper.Memset(uintptr(Pointer(&self.санахойarray)), 0xFF, self.хэрэглэгдсэнblock/Blockperbyte)
}
func (self *PhysicalСанахойЗохицуулагч) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalСанахойЗохицуулагч) ХУУДАСroundДээш(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *PhysicalСанахойЗохицуулагч) ХУУДАСrounddown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
