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
	head	*Node
	tail	*Node
	Sཚད_2	int

	mem	*mem.TMemorymanager
}

func (self *Linkedlist) Init(mem *mem.TMemorymanager) {
	self.head = nil
	self.tail = nil
	self.Sཚད_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if newnode == nil {
		return
	}
	newnode.pointer = pointer
	newnode.previous = nil
	newnode.next = self.head
	if self.head != nil {
		self.head.previous = newnode
	}
	self.head = newnode
	self.Sཚད_2++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Sཚད_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newnode == nil {
			return
		}
		newnode.pointer = pointer
		newnode.previous = self.tail
		newnode.next = nil
		self.tail.next = newnode
		self.tail = newnode
		self.Sཚད_2++
	}
}
func (self *Linkedlist) Insert_at_index(index int, pointer uintptr) {
	if index == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(index - 1)
		nextnode := previousnode.next
		newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newnode == nil {
			return
		}
		newnode.pointer = pointer

		previousnode.next = newnode
		newnode.previous = previousnode
		newnode.next = nextnode
		if nextnode != nil {
			nextnode.previous = newnode
		}

		self.Sཚད_2++

		if newnode.next == nil {
			self.tail = newnode
		}
	}
}
func (self *Linkedlist) Getnodeat(index int) *Node {
	if index < 0 || index >= self.Sཚད_2 {
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
	for ; i < self.Sཚད_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.next
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
	if index < 0 || index >= self.Sཚད_2 {
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
	self.Sཚད_2 = self.Sཚད_2 - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Print() {
	console_2.MPrintxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sཚད_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32print(uint32(node.pointer))
		console_2.MPrint(":")
	}
}
