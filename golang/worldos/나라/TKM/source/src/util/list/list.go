/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "memorymanager"

type Node struct {
	pointer		uintptr
	previous	*Node
	next		*Node
}

type Linkedlist struct {
	head		*Node
	tail		*Node
	Ululyk_2	int

	mem	*mem.TMemorymanager
}

func (self *Linkedlist) Init(mem *mem.TMemorymanager) {
	self.head = nil
	self.tail = nil
	self.Ululyk_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	täzenode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if täzenode == nil {
		return
	}
	täzenode.pointer = pointer
	täzenode.previous = nil
	täzenode.next = self.head
	if self.head != nil {
		self.head.previous = täzenode
	}
	self.head = täzenode
	self.Ululyk_2++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Ululyk_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		täzenode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if täzenode == nil {
			return
		}
		täzenode.pointer = pointer
		täzenode.previous = self.tail
		täzenode.next = nil
		self.tail.next = täzenode
		self.tail = täzenode
		self.Ululyk_2++
	}
}
func (self *Linkedlist) Insert_at_index(index int, pointer uintptr) {
	if index == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(index - 1)
		nextnode := previousnode.next
		täzenode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if täzenode == nil {
			return
		}
		täzenode.pointer = pointer

		previousnode.next = täzenode
		täzenode.previous = previousnode
		täzenode.next = nextnode
		if nextnode != nil {
			nextnode.previous = täzenode
		}

		self.Ululyk_2++

		if täzenode.next == nil {
			self.tail = täzenode
		}
	}
}
func (self *Linkedlist) Getnodeat(index int) *Node {
	if index < 0 || index >= self.Ululyk_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *Linkedlist) Setnodeat(index int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
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
	for ; i < self.Ululyk_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *Linkedlist) Çykar(pointer uintptr) {
	index := self.Indexof(pointer)
	if index < 0 {
		return
	}
	self.Çykarat(index)
}
func (self *Linkedlist) Çykarat(index int) {
	if index < 0 || index >= self.Ululyk_2 {
		return
	}
	node := self.Getnodeat(index)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.next = node.next
	} else {
		self.head = node.next
	}
	if node.next != nil {
		node.next.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Ululyk_2 = self.Ululyk_2 - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Çap() {
	console_2.MÇapxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Çap(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Ululyk_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32Çap(uint32(node.pointer))
		console_2.MÇap(":")
	}
}
