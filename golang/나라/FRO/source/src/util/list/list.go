package list

import . "unsafe"
import . "console"
import mem "memorymanager"

type Node struct {
	pointer		uintptr
	previous	*Node
	næsta		*Node
}

type Linkedlist struct {
	head	*Node
	tail	*Node
	Stødd_2	int

	mem	*mem.TMemorymanager
}

func (self *Linkedlist) Init(mem *mem.TMemorymanager) {
	self.head = nil
	self.tail = nil
	self.Stødd_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if newnode == nil {
		return
	}
	newnode.pointer = pointer
	newnode.previous = nil
	newnode.næsta = self.head
	if self.head != nil {
		self.head.previous = newnode
	}
	self.head = newnode
	self.Stødd_2++

	if self.head.næsta == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Stødd_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newnode == nil {
			return
		}
		newnode.pointer = pointer
		newnode.previous = self.tail
		newnode.næsta = nil
		self.tail.næsta = newnode
		self.tail = newnode
		self.Stødd_2++
	}
}
func (self *Linkedlist) Insert_at_index(index int, pointer uintptr) {
	if index == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(index - 1)
		næstanode := previousnode.næsta
		newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newnode == nil {
			return
		}
		newnode.pointer = pointer

		previousnode.næsta = newnode
		newnode.previous = previousnode
		newnode.næsta = næstanode
		if næstanode != nil {
			næstanode.previous = newnode
		}

		self.Stødd_2++

		if newnode.næsta == nil {
			self.tail = newnode
		}
	}
}
func (self *Linkedlist) Getnodeat(index int) *Node {
	if index < 0 || index >= self.Stødd_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.næsta
	}
	return x
}

func (self *Linkedlist) Setnodeat(index int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.næsta
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
	for ; i < self.Stødd_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.næsta
	}
	return -1
}
func (self *Linkedlist) Takburtur(pointer uintptr) {
	index := self.Indexof(pointer)
	if index < 0 {
		return
	}
	self.Takburturat(index)
}
func (self *Linkedlist) Takburturat(index int) {
	if index < 0 || index >= self.Stødd_2 {
		return
	}
	node := self.Getnodeat(index)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.næsta = node.næsta
	} else {
		self.head = node.næsta
	}
	if node.næsta != nil {
		node.næsta.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Stødd_2 = self.Stødd_2 - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Print() {
	console_2.MPrintxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Stødd_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32print(uint32(node.pointer))
		console_2.MPrint(":")
	}
}
