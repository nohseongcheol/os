/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 清單

import . "unsafe"
import . "控制台"
import mem "記憶體管理器"

type T鏈結串列節點 struct {
	位址參照		uintptr
	previous	*T鏈結串列節點
	下一個		*T鏈結串列節點
}

type Linked清單 struct {
	head	*T鏈結串列節點
	tail	*T鏈結串列節點
	S大小_2	int

	mem	*mem.T記憶體管理器
}

func (self *Linked清單) Init(mem *mem.T記憶體管理器) {
	self.head = nil
	self.tail = nil
	self.S大小_2 = 0

	self.mem = mem
}
func (self *Linked清單) M加入至串列開頭(位址參照 uintptr) {
	新增節點 := (*T鏈結串列節點)(self.mem.M配置記憶體(uint32(Sizeof(T鏈結串列節點{}))))
	if 新增節點 == nil {
		return
	}
	新增節點.位址參照 = 位址參照
	新增節點.previous = nil
	新增節點.下一個 = self.head
	if self.head != nil {
		self.head.previous = 新增節點
	}
	self.head = 新增節點
	self.S大小_2++

	if self.head.下一個 == nil {
		self.tail = self.head
	}

}
func (self *Linked清單) M附加至串列尾端(位址參照 uintptr) {
	if self.S大小_2 == 0 {
		self.M加入至串列開頭(位址參照)
	} else {
		新增節點 := (*T鏈結串列節點)(self.mem.M配置記憶體(uint32(Sizeof(T鏈結串列節點{}))))
		if 新增節點 == nil {
			return
		}
		新增節點.位址參照 = 位址參照
		新增節點.previous = self.tail
		新增節點.下一個 = nil
		self.tail.下一個 = 新增節點
		self.tail = 新增節點
		self.S大小_2++
	}
}
func (self *Linked清單) M在指定位置插入(索引 int, 位址參照 uintptr) {
	if 索引 == 0 {
		self.M加入至串列開頭(位址參照)
	} else {
		previous節點 := self.Get節點at(索引 - 1)
		下一個節點 := previous節點.下一個
		新增節點 := (*T鏈結串列節點)(self.mem.M配置記憶體(uint32(Sizeof(T鏈結串列節點{}))))
		if 新增節點 == nil {
			return
		}
		新增節點.位址參照 = 位址參照

		previous節點.下一個 = 新增節點
		新增節點.previous = previous節點
		新增節點.下一個 = 下一個節點
		if 下一個節點 != nil {
			下一個節點.previous = 新增節點
		}

		self.S大小_2++

		if 新增節點.下一個 == nil {
			self.tail = 新增節點
		}
	}
}
func (self *Linked清單) Get節點at(索引 int) *T鏈結串列節點 {
	if 索引 < 0 || 索引 >= self.S大小_2 {
		return nil
	}
	var x *T鏈結串列節點 = self.head
	for i := 0; i < 索引; i++ {
		x = x.下一個
	}
	return x
}

func (self *Linked清單) S設定節點at(索引 int, 位址參照 uintptr) {
	var x *T鏈結串列節點 = self.head
	for i := 0; i < 索引; i++ {
		x = x.下一個
	}
	if x != nil {
		x.位址參照 = 位址參照
	}
}
func (self *Linked清單) Getat(索引 int) Pointer {
	鏈結串列節點 := self.Get節點at(索引)
	if 鏈結串列節點 == nil {
		return nil
	}
	var 位址參照 uintptr = 鏈結串列節點.位址參照
	return Pointer(位址參照)
}
func (self *Linked清單) I索引of(位址參照 uintptr) int {
	var n *T鏈結串列節點 = self.head
	i := 0
	for ; i < self.S大小_2; i++ {
		if 位址參照 == n.位址參照 {
			return i
		}
		n = n.下一個
	}
	return -1
}
func (self *Linked清單) R移除(位址參照 uintptr) {
	索引 := self.I索引of(位址參照)
	if 索引 < 0 {
		return
	}
	self.R移除at(索引)
}
func (self *Linked清單) R移除at(索引 int) {
	if 索引 < 0 || 索引 >= self.S大小_2 {
		return
	}
	鏈結串列節點 := self.Get節點at(索引)
	if 鏈結串列節點 == nil {
		return
	}
	if 鏈結串列節點.previous != nil {
		鏈結串列節點.previous.下一個 = 鏈結串列節點.下一個
	} else {
		self.head = 鏈結串列節點.下一個
	}
	if 鏈結串列節點.下一個 != nil {
		鏈結串列節點.下一個.previous = 鏈結串列節點.previous
	} else {
		self.tail = 鏈結串列節點.previous
	}
	self.S大小_2 = self.S大小_2 - 1

	if self.mem != nil {
		self.mem.F剩餘(Pointer(鏈結串列節點))
	}
}

var 控制台_2 = T控制台{}

func (self *Linked清單) P列印() {
	控制台_2.M列印xy("LinkedList:", 1, 1)
	控制台_2.MUnsignedinteger32列印(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.S大小_2; i++ {
		鏈結串列節點 := (*T鏈結串列節點)(self.Getat(i))
		控制台_2.MUnsignedinteger32列印(uint32(鏈結串列節點.位址參照))
		控制台_2.M列印(":")
	}
}
