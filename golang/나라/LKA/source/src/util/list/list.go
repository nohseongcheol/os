/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "මතකයmanager"

type Node struct {
	pointer		uintptr
	previous	*Node
	ඊලඟ		*Node
}

type Linkedlist struct {
	head	*Node
	tail	*Node
	Size_2	int

	mem	*mem.Tමතකයmanager
}

func (self *Linkedlist) Init(mem *mem.Tමතකයmanager) {
	self.head = nil
	self.tail = nil
	self.Size_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	නවnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if නවnode == nil {
		return
	}
	නවnode.pointer = pointer
	නවnode.previous = nil
	නවnode.ඊලඟ = self.head
	if self.head != nil {
		self.head.previous = නවnode
	}
	self.head = නවnode
	self.Size_2++

	if self.head.ඊලඟ == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Size_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		නවnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if නවnode == nil {
			return
		}
		නවnode.pointer = pointer
		නවnode.previous = self.tail
		නවnode.ඊලඟ = nil
		self.tail.ඊලඟ = නවnode
		self.tail = නවnode
		self.Size_2++
	}
}
func (self *Linkedlist) Insert_at_index(index int, pointer uintptr) {
	if index == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(index - 1)
		ඊලඟnode := previousnode.ඊලඟ
		නවnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if නවnode == nil {
			return
		}
		නවnode.pointer = pointer

		previousnode.ඊලඟ = නවnode
		නවnode.previous = previousnode
		නවnode.ඊලඟ = ඊලඟnode
		if ඊලඟnode != nil {
			ඊලඟnode.previous = නවnode
		}

		self.Size_2++

		if නවnode.ඊලඟ == nil {
			self.tail = නවnode
		}
	}
}
func (self *Linkedlist) Getnodeat(index int) *Node {
	if index < 0 || index >= self.Size_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.ඊලඟ
	}
	return x
}

func (self *Linkedlist) Setnodeat(index int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.ඊලඟ
	}
	if x != nil {
		x.pointer = pointer
	}
}
func (self *Linkedlist) Getat(index int) Pointer {
	node := self.Getnodeat(index)
	if node == nil {
		return nil
	}
	var pointer uintptr = node.pointer
	return Pointer(pointer)
}
func (self *Linkedlist) Indexof(pointer uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Size_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.ඊලඟ
	}
	return -1
}
func (self *Linkedlist) Remove(pointer uintptr) {
	index := self.Indexof(pointer)
	if index < 0 {
		return
	}
	self.Removeat(index)
}
func (self *Linkedlist) Removeat(index int) {
	if index < 0 || index >= self.Size_2 {
		return
	}
	node := self.Getnodeat(index)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.ඊලඟ = node.ඊලඟ
	} else {
		self.head = node.ඊලඟ
	}
	if node.ඊලඟ != nil {
		node.ඊලඟ.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Size_2 = self.Size_2 - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Print() {
	console_2.MPrintxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Size_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32print(uint32(node.pointer))
		console_2.MPrint(":")
	}
}
