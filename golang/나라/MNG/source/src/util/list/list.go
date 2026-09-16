/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "консол"
import mem "санахойЗохицуулагч"

type Node struct {
	pointer		uintptr
	previous	*Node
	дараах		*Node
}

type Linkedlist struct {
	head		*Node
	tail		*Node
	Хэмжээ_2	int

	mem	*mem.TСанахойЗохицуулагч
}

func (self *Linkedlist) Init(mem *mem.TСанахойЗохицуулагч) {
	self.head = nil
	self.tail = nil
	self.Хэмжээ_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	шинэnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if шинэnode == nil {
		return
	}
	шинэnode.pointer = pointer
	шинэnode.previous = nil
	шинэnode.дараах = self.head
	if self.head != nil {
		self.head.previous = шинэnode
	}
	self.head = шинэnode
	self.Хэмжээ_2++

	if self.head.дараах == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Хэмжээ_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		шинэnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if шинэnode == nil {
			return
		}
		шинэnode.pointer = pointer
		шинэnode.previous = self.tail
		шинэnode.дараах = nil
		self.tail.дараах = шинэnode
		self.tail = шинэnode
		self.Хэмжээ_2++
	}
}
func (self *Linkedlist) Insert_at_index(үзүүлэлт int, pointer uintptr) {
	if үзүүлэлт == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(үзүүлэлт - 1)
		дараахnode := previousnode.дараах
		шинэnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if шинэnode == nil {
			return
		}
		шинэnode.pointer = pointer

		previousnode.дараах = шинэnode
		шинэnode.previous = previousnode
		шинэnode.дараах = дараахnode
		if дараахnode != nil {
			дараахnode.previous = шинэnode
		}

		self.Хэмжээ_2++

		if шинэnode.дараах == nil {
			self.tail = шинэnode
		}
	}
}
func (self *Linkedlist) Getnodeat(үзүүлэлт int) *Node {
	if үзүүлэлт < 0 || үзүүлэлт >= self.Хэмжээ_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < үзүүлэлт; i++ {
		x = x.дараах
	}
	return x
}

func (self *Linkedlist) Setnodeat(үзүүлэлт int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < үзүүлэлт; i++ {
		x = x.дараах
	}
	if x != nil {
		x.pointer = pointer
	}
}
func (self *Linkedlist) Getat(үзүүлэлт int) Pointer {
	node := self.Getnodeat(үзүүлэлт)
	if node == nil {
		return nil
	}
	var pointer uintptr = node.pointer
	return Pointer(pointer)
}
func (self *Linkedlist) Үзүүлэлтof(pointer uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Хэмжээ_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.дараах
	}
	return -1
}
func (self *Linkedlist) Устгах_2(pointer uintptr) {
	үзүүлэлт := self.Үзүүлэлтof(pointer)
	if үзүүлэлт < 0 {
		return
	}
	self.Устгахat(үзүүлэлт)
}
func (self *Linkedlist) Устгахat(үзүүлэлт int) {
	if үзүүлэлт < 0 || үзүүлэлт >= self.Хэмжээ_2 {
		return
	}
	node := self.Getnodeat(үзүүлэлт)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.дараах = node.дараах
	} else {
		self.head = node.дараах
	}
	if node.дараах != nil {
		node.дараах.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Хэмжээ_2 = self.Хэмжээ_2 - 1

	if self.mem != nil {
		self.mem.Чөлөөт(Pointer(node))
	}
}

var консол_2 = TКонсол{}

func (self *Linkedlist) Хэвлэх() {
	консол_2.MХэвлэхxy("LinkedList:", 1, 1)
	консол_2.MUnsignedinteger32Хэвлэх(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Хэмжээ_2; i++ {
		node := (*Node)(self.Getat(i))
		консол_2.MUnsignedinteger32Хэвлэх(uint32(node.pointer))
		консол_2.MХэвлэх(":")
	}
}
