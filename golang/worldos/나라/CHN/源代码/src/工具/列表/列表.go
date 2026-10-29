/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 列表

import . "unsafe"
import . "控制台"
import mem "内存管理器"

type T链表节点 struct {
	地址引用		uintptr
	previous	*T链表节点
	下一个		*T链表节点
}

type Linked列表 struct {
	head	*T链表节点
	tail	*T链表节点
	S大小_2	int

	mem	*mem.T内存管理器
}

func (self *Linked列表) Init(mem *mem.T内存管理器) {
	self.head = nil
	self.tail = nil
	self.S大小_2 = 0

	self.mem = mem
}
func (self *Linked列表) M添加到表头(地址引用 uintptr) {
	新建节点 := (*T链表节点)(self.mem.M分配内存(uint32(Sizeof(T链表节点{}))))
	if 新建节点 == nil {
		return
	}
	新建节点.地址引用 = 地址引用
	新建节点.previous = nil
	新建节点.下一个 = self.head
	if self.head != nil {
		self.head.previous = 新建节点
	}
	self.head = 新建节点
	self.S大小_2++

	if self.head.下一个 == nil {
		self.tail = self.head
	}

}
func (self *Linked列表) M追加到表尾(地址引用 uintptr) {
	if self.S大小_2 == 0 {
		self.M添加到表头(地址引用)
	} else {
		新建节点 := (*T链表节点)(self.mem.M分配内存(uint32(Sizeof(T链表节点{}))))
		if 新建节点 == nil {
			return
		}
		新建节点.地址引用 = 地址引用
		新建节点.previous = self.tail
		新建节点.下一个 = nil
		self.tail.下一个 = 新建节点
		self.tail = 新建节点
		self.S大小_2++
	}
}
func (self *Linked列表) M在指定位置插入(索引 int, 地址引用 uintptr) {
	if 索引 == 0 {
		self.M添加到表头(地址引用)
	} else {
		previous节点 := self.Get节点at(索引 - 1)
		下一个节点 := previous节点.下一个
		新建节点 := (*T链表节点)(self.mem.M分配内存(uint32(Sizeof(T链表节点{}))))
		if 新建节点 == nil {
			return
		}
		新建节点.地址引用 = 地址引用

		previous节点.下一个 = 新建节点
		新建节点.previous = previous节点
		新建节点.下一个 = 下一个节点
		if 下一个节点 != nil {
			下一个节点.previous = 新建节点
		}

		self.S大小_2++

		if 新建节点.下一个 == nil {
			self.tail = 新建节点
		}
	}
}
func (self *Linked列表) Get节点at(索引 int) *T链表节点 {
	if 索引 < 0 || 索引 >= self.S大小_2 {
		return nil
	}
	var x *T链表节点 = self.head
	for i := 0; i < 索引; i++ {
		x = x.下一个
	}
	return x
}

func (self *Linked列表) S集合节点at(索引 int, 地址引用 uintptr) {
	var x *T链表节点 = self.head
	for i := 0; i < 索引; i++ {
		x = x.下一个
	}
	if x != nil {
		x.地址引用 = 地址引用
	}
}
func (self *Linked列表) Getat(索引 int) Pointer {
	链表节点 := self.Get节点at(索引)
	if 链表节点 == nil {
		return nil
	}
	var 地址引用 uintptr = 链表节点.地址引用
	return Pointer(地址引用)
}
func (self *Linked列表) I索引of(地址引用 uintptr) int {
	var n *T链表节点 = self.head
	i := 0
	for ; i < self.S大小_2; i++ {
		if 地址引用 == n.地址引用 {
			return i
		}
		n = n.下一个
	}
	return -1
}
func (self *Linked列表) R删除(地址引用 uintptr) {
	索引 := self.I索引of(地址引用)
	if 索引 < 0 {
		return
	}
	self.R删除at(索引)
}
func (self *Linked列表) R删除at(索引 int) {
	if 索引 < 0 || 索引 >= self.S大小_2 {
		return
	}
	链表节点 := self.Get节点at(索引)
	if 链表节点 == nil {
		return
	}
	if 链表节点.previous != nil {
		链表节点.previous.下一个 = 链表节点.下一个
	} else {
		self.head = 链表节点.下一个
	}
	if 链表节点.下一个 != nil {
		链表节点.下一个.previous = 链表节点.previous
	} else {
		self.tail = 链表节点.previous
	}
	self.S大小_2 = self.S大小_2 - 1

	if self.mem != nil {
		self.mem.F空闲(Pointer(链表节点))
	}
}

var 控制台_2 = T控制台{}

func (self *Linked列表) P打印() {
	控制台_2.M打印xy("LinkedList:", 1, 1)
	控制台_2.MUnsignedinteger32打印(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.S大小_2; i++ {
		链表节点 := (*T链表节点)(self.Getat(i))
		控制台_2.MUnsignedinteger32打印(uint32(链表节点.地址引用))
		控制台_2.M打印(":")
	}
}
