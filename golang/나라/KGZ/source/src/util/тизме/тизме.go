/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package тизме

import . "unsafe"
import . "console"
import mem "эсиmanager"

type Node struct {
	көрсөткүч	uintptr
	previous	*Node
	кийинки		*Node
}

type LinkedТизме struct {
	head	*Node
	tail	*Node
	Өлчөм_2	int

	mem	*mem.TЭсиmanager
}

func (self *LinkedТизме) Init(mem *mem.TЭсиmanager) {
	self.head = nil
	self.tail = nil
	self.Өлчөм_2 = 0

	self.mem = mem
}
func (self *LinkedТизме) Prepend_to_list(көрсөткүч uintptr) {
	жаңыnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if жаңыnode == nil {
		return
	}
	жаңыnode.көрсөткүч = көрсөткүч
	жаңыnode.previous = nil
	жаңыnode.кийинки = self.head
	if self.head != nil {
		self.head.previous = жаңыnode
	}
	self.head = жаңыnode
	self.Өлчөм_2++

	if self.head.кийинки == nil {
		self.tail = self.head
	}

}
func (self *LinkedТизме) Append_to_list(көрсөткүч uintptr) {
	if self.Өлчөм_2 == 0 {
		self.Prepend_to_list(көрсөткүч)
	} else {
		жаңыnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if жаңыnode == nil {
			return
		}
		жаңыnode.көрсөткүч = көрсөткүч
		жаңыnode.previous = self.tail
		жаңыnode.кийинки = nil
		self.tail.кийинки = жаңыnode
		self.tail = жаңыnode
		self.Өлчөм_2++
	}
}
func (self *LinkedТизме) Insert_at_index(мазмун int, көрсөткүч uintptr) {
	if мазмун == 0 {
		self.Prepend_to_list(көрсөткүч)
	} else {
		previousnode := self.Getnodeat(мазмун - 1)
		кийинкиnode := previousnode.кийинки
		жаңыnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if жаңыnode == nil {
			return
		}
		жаңыnode.көрсөткүч = көрсөткүч

		previousnode.кийинки = жаңыnode
		жаңыnode.previous = previousnode
		жаңыnode.кийинки = кийинкиnode
		if кийинкиnode != nil {
			кийинкиnode.previous = жаңыnode
		}

		self.Өлчөм_2++

		if жаңыnode.кийинки == nil {
			self.tail = жаңыnode
		}
	}
}
func (self *LinkedТизме) Getnodeat(мазмун int) *Node {
	if мазмун < 0 || мазмун >= self.Өлчөм_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < мазмун; i++ {
		x = x.кийинки
	}
	return x
}

func (self *LinkedТизме) Setnodeat(мазмун int, көрсөткүч uintptr) {
	var x *Node = self.head
	for i := 0; i < мазмун; i++ {
		x = x.кийинки
	}
	if x != nil {
		x.көрсөткүч = көрсөткүч
	}
}
func (self *LinkedТизме) Getat(мазмун int) Pointer {
	node := self.Getnodeat(мазмун)
	if node == nil {
		return nil
	}
	var көрсөткүч uintptr = node.көрсөткүч
	return Pointer(көрсөткүч)
}
func (self *LinkedТизме) Мазмунof(көрсөткүч uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Өлчөм_2; i++ {
		if көрсөткүч == n.көрсөткүч {
			return i
		}
		n = n.кийинки
	}
	return -1
}
func (self *LinkedТизме) Өчүрүү_2(көрсөткүч uintptr) {
	мазмун := self.Мазмунof(көрсөткүч)
	if мазмун < 0 {
		return
	}
	self.Өчүрүүat(мазмун)
}
func (self *LinkedТизме) Өчүрүүat(мазмун int) {
	if мазмун < 0 || мазмун >= self.Өлчөм_2 {
		return
	}
	node := self.Getnodeat(мазмун)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.кийинки = node.кийинки
	} else {
		self.head = node.кийинки
	}
	if node.кийинки != nil {
		node.кийинки.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Өлчөм_2 = self.Өлчөм_2 - 1

	if self.mem != nil {
		self.mem.Бош(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *LinkedТизме) Басма() {
	console_2.MБасмаxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Басма(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Өлчөм_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32Басма(uint32(node.көрсөткүч))
		console_2.MБасма(":")
	}
}
