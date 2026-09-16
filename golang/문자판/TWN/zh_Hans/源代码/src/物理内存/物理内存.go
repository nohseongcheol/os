/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 物理内存

import (
	. "通用"
	. "unsafe"
)

const (
	B块大小		uint32	= 4 * 1024
	B块per字节	uint32	= 8
)

type multiboot内存映射 struct {
	大小		uint32
	baseaddress低	uint64
	baseaddress高	uint64
	长度低		uint64
	长度高		uint64
	T类型		uint32
}

func Phymem测试() {
}

var 内存oper M内存oper = M内存oper{}

type P物理内存管理器 struct {
	内存大小	uint32
	已用块	uint32
	最大块	uint32
	内存数组	[]uint32
}

var (
	最大块			uint32	= 0
	内存数组			[]uint32
	grubmultiboot内存映射t	multiboot内存映射
)

func (self *P物理内存管理器) S集合bit(bit uint32) uint32 {
	self.内存数组[bit/32] = self.内存数组[bit/32] | (1 << (bit % 32))
	return self.内存数组[bit/32]
}
func (self *P物理内存管理器) M反转分配位(bit uint32) uint32 {
	self.内存数组[bit/32] = self.内存数组[bit/32] ^ (1 << (bit % 32))
	return self.内存数组[bit/32]
}
func (self *P物理内存管理器) T测试bit(bit uint32) uint32 {
	ret := self.内存数组[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *P物理内存管理器) T总数块() uint32 {
	return self.最大块
}
func (self *P物理内存管理器) U已用块() uint32 {
	return self.已用块
}
func (self *P物理内存管理器) A总量of内存() uint32 {
	return self.内存大小
}
func (self *P物理内存管理器) Getbitmasp大小() uint32 {
	return self.内存大小 / B块大小 / B块per字节
}

func (self *P物理内存管理器) First空闲() uint32 {
	for i := uint32(0); i < self.T总数块(); i++ {
		if self.内存数组[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (内存数组[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *P物理内存管理器) First空闲大小(大小 uint32) uint32 {
	if 大小 == 0 {
		return 0xffffffff
	}
	if 大小 == 1 {
		return self.First空闲()
	}

	for i := uint32(0); i < self.T总数块(); i++ {
		if self.内存数组[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.内存数组[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var 空闲 uint32 = 0
					for 计数 := uint32(0); 计数 <= 大小; 计数++ {
						if self.T测试bit(startingbit+计数) == 0 {
							空闲++
						}

						if 空闲 == 大小 {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *P物理内存管理器) Init(大小 uint32, 分配位图 []uint32) {
	self.内存大小 = 大小
	self.内存数组 = 分配位图
	self.最大块 = 大小 / B块大小
	self.已用块 = self.最大块
	内存oper.Mem集合(uintptr(Pointer(&self.内存数组)), 0xFF, self.已用块/B块per字节)
}
func (self *P物理内存管理器) Allocate块() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *P物理内存管理器) P页舍入向上(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *P物理内存管理器) P页舍入下(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
