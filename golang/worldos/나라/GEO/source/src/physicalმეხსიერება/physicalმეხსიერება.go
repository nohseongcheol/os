/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package physicalმეხსიერება

import (
	. "საერთო"
	. "unsafe"
)

const (
	Blockზომა	uint32	= 4 * 1024
	Blockperbyte	uint32	= 8
)

type multibootმეხსიერებაmap struct {
	ზომა		uint32
	baseaddresslow	uint64
	baseaddresshigh	uint64
	lengthlow	uint64
	lengthhigh	uint64
	Tტიპი		uint32
}

func Phymemtest() {
}

var მეხსიერებაoper Mმეხსიერებაoper = Mმეხსიერებაoper{}

type Physicalმეხსიერებაmanager struct {
	მეხსიერებაზომა		uint32
	გამოყეებულიაblock	uint32
	maximumblock		uint32
	მეხსიერებამასივი	[]uint32
}

var (
	maximumblock			uint32	= 0
	მეხსიერებამასივი		[]uint32
	grubmultibootმეხსიერებაmapt	multibootმეხსიერებაmap
)

func (self *Physicalმეხსიერებაmanager) Setbit(bit uint32) uint32 {
	self.მეხსიერებამასივი[bit/32] = self.მეხსიერებამასივი[bit/32] | (1 << (bit % 32))
	return self.მეხსიერებამასივი[bit/32]
}
func (self *Physicalმეხსიერებაmanager) Toggle_allocation_bit(bit uint32) uint32 {
	self.მეხსიერებამასივი[bit/32] = self.მეხსიერებამასივი[bit/32] ^ (1 << (bit % 32))
	return self.მეხსიერებამასივი[bit/32]
}
func (self *Physicalმეხსიერებაmanager) Testbit(bit uint32) uint32 {
	ret := self.მეხსიერებამასივი[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *Physicalმეხსიერებაmanager) Tსულblock() uint32 {
	return self.maximumblock
}
func (self *Physicalმეხსიერებაmanager) Uგამოყეებულიაblock() uint32 {
	return self.გამოყეებულიაblock
}
func (self *Physicalმეხსიერებაmanager) Aრაოდენობაofმეხსიერება() uint32 {
	return self.მეხსიერებაზომა
}
func (self *Physicalმეხსიერებაmanager) Getbitmaspზომა() uint32 {
	return self.მეხსიერებაზომა / Blockზომა / Blockperbyte
}

func (self *Physicalმეხსიერებაmanager) Firstთავისუფალი() uint32 {
	for i := uint32(0); i < self.Tსულblock(); i++ {
		if self.მეხსიერებამასივი[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (მეხსიერებამასივი[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *Physicalმეხსიერებაmanager) Firstთავისუფალიზომა(ზომა uint32) uint32 {
	if ზომა == 0 {
		return 0xffffffff
	}
	if ზომა == 1 {
		return self.Firstთავისუფალი()
	}

	for i := uint32(0); i < self.Tსულblock(); i++ {
		if self.მეხსიერებამასივი[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.მეხსიერებამასივი[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var თავისუფალი uint32 = 0
					for count := uint32(0); count <= ზომა; count++ {
						if self.Testbit(startingbit+count) == 0 {
							თავისუფალი++
						}

						if თავისუფალი == ზომა {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *Physicalმეხსიერებაmanager) Init(ზომა uint32, bitmap []uint32) {
	self.მეხსიერებაზომა = ზომა
	self.მეხსიერებამასივი = bitmap
	self.maximumblock = ზომა / Blockზომა
	self.გამოყეებულიაblock = self.maximumblock
	მეხსიერებაoper.Memset(uintptr(Pointer(&self.მეხსიერებამასივი)), 0xFF, self.გამოყეებულიაblock/Blockperbyte)
}
func (self *Physicalმეხსიერებაmanager) Allocateblock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *Physicalმეხსიერებაmanager) Pგვერდიroundზემოთ(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *Physicalმეხსიერებაmanager) Pგვერდიrounddown(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
