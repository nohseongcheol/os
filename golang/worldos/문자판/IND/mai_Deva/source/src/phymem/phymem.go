/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package phymem

import (
	. "common"
	. "unsafe"
)

const (
	BLOCK_SIZE	uint32	= 4 * 1024
	BLOCKS_PER_BYTE	uint32	= 8
)

type multiboot_memory_map struct {
	आकार		uint32
	base_addr_low	uint64
	base_addr_high	uint64
	length_low	uint64
	length_high	uint64
	Type	uint32
}

func PhyMemTest() {
}

var memoryOper MemoryOper = MemoryOper{}

type PhysicalMemoryManager struct {
	memorySize	uint32
	usedBlocks	uint32
	maximumBlocks	uint32
	memoryArray	[]uint32
}

var (
	maximumBlocks		uint32	= 0
	memoryArray		[]uint32
	grub_multiboot_memory_map_t	multiboot_memory_map
)

func (self *PhysicalMemoryManager) SetBit(bit uint32) uint32 {
	self.memoryArray[bit/32] = self.memoryArray[bit/32] | (1 << (bit % 32))
	return self.memoryArray[bit/32]
}
func (self *PhysicalMemoryManager) UnsetBit(bit uint32) uint32 {
	self.memoryArray[bit/32] = self.memoryArray[bit/32] ^ (1 << (bit % 32))
	return self.memoryArray[bit/32]
}
func (self *PhysicalMemoryManager) TestBit(bit uint32) uint32 {
	ret := self.memoryArray[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *PhysicalMemoryManager) TotalBlocks() uint32 {
	return self.maximumBlocks
}
func (self *PhysicalMemoryManager) UsedBlocks() uint32 {
	return self.usedBlocks
}
func (self *PhysicalMemoryManager) AmountOfMemory() uint32 {
	return self.memorySize
}
func (self *PhysicalMemoryManager) GetBitmaspSize() uint32 {
	return self.memorySize / BLOCK_SIZE / BLOCKS_PER_BYTE
}

func (self *PhysicalMemoryManager) FirstFree() uint32 {
	for i := uint32(0); i < self.TotalBlocks(); i++ {
		if self.memoryArray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (memoryArray[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *PhysicalMemoryManager) FirstFreeSize(आकार uint32) uint32 {
	if आकार == 0 {
		return 0xffffffff
	}
	if आकार == 1 {
		return self.FirstFree()
	}

	for i := uint32(0); i < self.TotalBlocks(); i++ {
		if self.memoryArray[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.memoryArray[j]&bit == 0 {
					var startingBit uint32 = i * 32
					startingBit += j

					var free uint32 = 0
					for count := uint32(0); count <= आकार; count++ {
						if self.TestBit(startingBit+count) == 0 {
							free++
						}

						if free == आकार {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *PhysicalMemoryManager) Vआरंभ_करब(आकार uint32, bitmap []uint32) {
	self.memorySize = आकार
	self.memoryArray = bitmap
	self.maximumBlocks = आकार / BLOCK_SIZE
	self.usedBlocks = self.maximumBlocks
	memoryOper.MemSet(uintptr(Pointer(&self.memoryArray)), 0xFF, self.usedBlocks/BLOCKS_PER_BYTE)
}
func (self *PhysicalMemoryManager) AllocateBlock() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *PhysicalMemoryManager) PageRoundUp(address uint32) uint32 {
	if (address & 0xFFFFF000) != address {
		address = address & 0xFFFFF000
		address = address + 0x1000
	}
	return address
}
func (self *PhysicalMemoryManager) PageRoundDown(address uint32) uint32 {
	return address & 0xFFFFF000
}
