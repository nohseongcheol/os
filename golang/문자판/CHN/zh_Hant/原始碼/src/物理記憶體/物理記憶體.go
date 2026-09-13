package 物理記憶體

import (
	. "通用"
	. "unsafe"
)

const (
	B區塊大小	uint32	= 4 * 1024
	B區塊per位元組	uint32	= 8
)

type multiboot記憶體對映 struct {
	大小		uint32
	baseaddress低	uint64
	baseaddress高	uint64
	長度低		uint64
	長度高		uint64
	T類型		uint32
}

func Phymem測試() {
}

var 記憶體oper M記憶體oper = M記憶體oper{}

type P物理記憶體管理器 struct {
	記憶體大小	uint32
	已使用區塊	uint32
	最大值區塊	uint32
	記憶體陣列	[]uint32
}

var (
	最大值區塊			uint32	= 0
	記憶體陣列			[]uint32
	grubmultiboot記憶體對映t	multiboot記憶體對映
)

func (self *P物理記憶體管理器) S設定bit(bit uint32) uint32 {
	self.記憶體陣列[bit/32] = self.記憶體陣列[bit/32] | (1 << (bit % 32))
	return self.記憶體陣列[bit/32]
}
func (self *P物理記憶體管理器) M反轉配置位元(bit uint32) uint32 {
	self.記憶體陣列[bit/32] = self.記憶體陣列[bit/32] ^ (1 << (bit % 32))
	return self.記憶體陣列[bit/32]
}
func (self *P物理記憶體管理器) T測試bit(bit uint32) uint32 {
	ret := self.記憶體陣列[bit/32] & (1 << (bit % 32))
	return ret
}
func (self *P物理記憶體管理器) T總數區塊() uint32 {
	return self.最大值區塊
}
func (self *P物理記憶體管理器) U已使用區塊() uint32 {
	return self.已使用區塊
}
func (self *P物理記憶體管理器) A數量of記憶體() uint32 {
	return self.記憶體大小
}
func (self *P物理記憶體管理器) Getbitmasp大小() uint32 {
	return self.記憶體大小 / B區塊大小 / B區塊per位元組
}

func (self *P物理記憶體管理器) First剩餘() uint32 {
	for i := uint32(0); i < self.T總數區塊(); i++ {
		if self.記憶體陣列[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (記憶體陣列[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (self *P物理記憶體管理器) First剩餘大小(大小 uint32) uint32 {
	if 大小 == 0 {
		return 0xffffffff
	}
	if 大小 == 1 {
		return self.First剩餘()
	}

	for i := uint32(0); i < self.T總數區塊(); i++ {
		if self.記憶體陣列[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if self.記憶體陣列[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var 剩餘 uint32 = 0
					for 計數 := uint32(0); 計數 <= 大小; 計數++ {
						if self.T測試bit(startingbit+計數) == 0 {
							剩餘++
						}

						if 剩餘 == 大小 {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (self *P物理記憶體管理器) Init(大小 uint32, 配置位元圖 []uint32) {
	self.記憶體大小 = 大小
	self.記憶體陣列 = 配置位元圖
	self.最大值區塊 = 大小 / B區塊大小
	self.已使用區塊 = self.最大值區塊
	記憶體oper.Mem設定(uintptr(Pointer(&self.記憶體陣列)), 0xFF, self.已使用區塊/B區塊per位元組)
}
func (self *P物理記憶體管理器) Allocate區塊() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (self *P物理記憶體管理器) P頁四捨五入上(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (self *P物理記憶體管理器) P頁四捨五入下(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
