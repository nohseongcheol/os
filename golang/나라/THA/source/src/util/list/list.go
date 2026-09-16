/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "memorymanager"

type Nโหนด struct {
	pointer		uintptr
	previous	*Nโหนด
	next		*Nโหนด
}

type Linkedlist struct {
	head	*Nโหนด
	tail	*Nโหนด
	Sขนาด_2	int

	mem	*mem.TMemorymanager
}

func (self *Linkedlist) Init(mem *mem.TMemorymanager) {
	self.head = nil
	self.tail = nil
	self.Sขนาด_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	newโหนด := (*Nโหนด)(self.mem.Malloc(uint32(Sizeof(Nโหนด{}))))
	if newโหนด == nil {
		return
	}
	newโหนด.pointer = pointer
	newโหนด.previous = nil
	newโหนด.next = self.head
	if self.head != nil {
		self.head.previous = newโหนด
	}
	self.head = newโหนด
	self.Sขนาด_2++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Sขนาด_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		newโหนด := (*Nโหนด)(self.mem.Malloc(uint32(Sizeof(Nโหนด{}))))
		if newโหนด == nil {
			return
		}
		newโหนด.pointer = pointer
		newโหนด.previous = self.tail
		newโหนด.next = nil
		self.tail.next = newโหนด
		self.tail = newโหนด
		self.Sขนาด_2++
	}
}
func (self *Linkedlist) Insert_at_index(index int, pointer uintptr) {
	if index == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousโหนด := self.Getโหนดat(index - 1)
		nextโหนด := previousโหนด.next
		newโหนด := (*Nโหนด)(self.mem.Malloc(uint32(Sizeof(Nโหนด{}))))
		if newโหนด == nil {
			return
		}
		newโหนด.pointer = pointer

		previousโหนด.next = newโหนด
		newโหนด.previous = previousโหนด
		newโหนด.next = nextโหนด
		if nextโหนด != nil {
			nextโหนด.previous = newโหนด
		}

		self.Sขนาด_2++

		if newโหนด.next == nil {
			self.tail = newโหนด
		}
	}
}
func (self *Linkedlist) Getโหนดat(index int) *Nโหนด {
	if index < 0 || index >= self.Sขนาด_2 {
		return nil
	}
	var x *Nโหนด = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *Linkedlist) Sกำหนดโหนดat(index int, pointer uintptr) {
	var x *Nโหนด = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.pointer = pointer
	}
}
func (self *Linkedlist) Getat(index int) Pointer {
	โหนด := self.Getโหนดat(index)
	if โหนด == nil {
		return nil
	}
	var pointer uintptr = โหนด.pointer
	return Pointer(pointer)
}
func (self *Linkedlist) Indexจาก(pointer uintptr) int {
	var n *Nโหนด = self.head
	i := 0
	for ; i < self.Sขนาด_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *Linkedlist) Rลบ(pointer uintptr) {
	index := self.Indexจาก(pointer)
	if index < 0 {
		return
	}
	self.Rลบat(index)
}
func (self *Linkedlist) Rลบat(index int) {
	if index < 0 || index >= self.Sขนาด_2 {
		return
	}
	โหนด := self.Getโหนดat(index)
	if โหนด == nil {
		return
	}
	if โหนด.previous != nil {
		โหนด.previous.next = โหนด.next
	} else {
		self.head = โหนด.next
	}
	if โหนด.next != nil {
		โหนด.next.previous = โหนด.previous
	} else {
		self.tail = โหนด.previous
	}
	self.Sขนาด_2 = self.Sขนาด_2 - 1

	if self.mem != nil {
		self.mem.Free(Pointer(โหนด))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Print() {
	console_2.MPrintxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sขนาด_2; i++ {
		โหนด := (*Nโหนด)(self.Getat(i))
		console_2.MUnsignedinteger32print(uint32(โหนด.pointer))
		console_2.MPrint(":")
	}
}
