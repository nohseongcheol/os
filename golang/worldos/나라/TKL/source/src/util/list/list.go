/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "memorymanager"

type TList_node struct {
	address_reference		uintptr
	previous	*TList_node
	next		*TList_node
}

type Linkedlist struct {
	head	*TList_node
	tail	*TList_node
	Size_2	int

	mem	*mem.TMemorymanager
}

func (self *Linkedlist) Init(mem *mem.TMemorymanager) {
	self.head = nil
	self.tail = nil
	self.Size_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(address_reference uintptr) {
	newnode := (*TList_node)(self.mem.Allocate_memory(uint32(Sizeof(TList_node{}))))
	if newnode == nil {
		return
	}
	newnode.address_reference = address_reference
	newnode.previous = nil
	newnode.next = self.head
	if self.head != nil {
		self.head.previous = newnode
	}
	self.head = newnode
	self.Size_2++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(address_reference uintptr) {
	if self.Size_2 == 0 {
		self.Prepend_to_list(address_reference)
	} else {
		newnode := (*TList_node)(self.mem.Allocate_memory(uint32(Sizeof(TList_node{}))))
		if newnode == nil {
			return
		}
		newnode.address_reference = address_reference
		newnode.previous = self.tail
		newnode.next = nil
		self.tail.next = newnode
		self.tail = newnode
		self.Size_2++
	}
}
func (self *Linkedlist) Insert_at_index(index int, address_reference uintptr) {
	if index == 0 {
		self.Prepend_to_list(address_reference)
	} else {
		previousnode := self.Getnodeat(index - 1)
		nextnode := previousnode.next
		newnode := (*TList_node)(self.mem.Allocate_memory(uint32(Sizeof(TList_node{}))))
		if newnode == nil {
			return
		}
		newnode.address_reference = address_reference

		previousnode.next = newnode
		newnode.previous = previousnode
		newnode.next = nextnode
		if nextnode != nil {
			nextnode.previous = newnode
		}

		self.Size_2++

		if newnode.next == nil {
			self.tail = newnode
		}
	}
}
func (self *Linkedlist) Getnodeat(index int) *TList_node {
	if index < 0 || index >= self.Size_2 {
		return nil
	}
	var x *TList_node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *Linkedlist) Setnodeat(index int, address_reference uintptr) {
	var x *TList_node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.address_reference = address_reference
	}
}
func (self *Linkedlist) Getat(index int) Pointer {
	list_node := self.Getnodeat(index)
	if list_node == nil {
		return nil
	}
	var address_reference uintptr = list_node.address_reference
	return Pointer(address_reference)
}
func (self *Linkedlist) Indexof(address_reference uintptr) int {
	var n *TList_node = self.head
	i := 0
	for ; i < self.Size_2; i++ {
		if address_reference == n.address_reference {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *Linkedlist) Remove(address_reference uintptr) {
	index := self.Indexof(address_reference)
	if index < 0 {
		return
	}
	self.Removeat(index)
}
func (self *Linkedlist) Removeat(index int) {
	if index < 0 || index >= self.Size_2 {
		return
	}
	list_node := self.Getnodeat(index)
	if list_node == nil {
		return
	}
	if list_node.previous != nil {
		list_node.previous.next = list_node.next
	} else {
		self.head = list_node.next
	}
	if list_node.next != nil {
		list_node.next.previous = list_node.previous
	} else {
		self.tail = list_node.previous
	}
	self.Size_2 = self.Size_2 - 1

	if self.mem != nil {
		self.mem.Free(Pointer(list_node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Print() {
	console_2.MPrintxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Size_2; i++ {
		list_node := (*TList_node)(self.Getat(i))
		console_2.MUnsignedinteger32print(uint32(list_node.address_reference))
		console_2.MPrint(":")
	}
}
