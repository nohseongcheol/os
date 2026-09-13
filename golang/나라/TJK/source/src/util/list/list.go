package list

import . "unsafe"
import . "console"
import mem "memorymanager"

type Node struct {
	pointer		uintptr
	previous	*Node
	навбатӣ		*Node
}

type Linkedlist struct {
	head	*Node
	tail	*Node
	Size_2	int

	mem	*mem.TMemorymanager
}

func (self *Linkedlist) Init(mem *mem.TMemorymanager) {
	self.head = nil
	self.tail = nil
	self.Size_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	навnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if навnode == nil {
		return
	}
	навnode.pointer = pointer
	навnode.previous = nil
	навnode.навбатӣ = self.head
	if self.head != nil {
		self.head.previous = навnode
	}
	self.head = навnode
	self.Size_2++

	if self.head.навбатӣ == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Size_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		навnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if навnode == nil {
			return
		}
		навnode.pointer = pointer
		навnode.previous = self.tail
		навnode.навбатӣ = nil
		self.tail.навбатӣ = навnode
		self.tail = навnode
		self.Size_2++
	}
}
func (self *Linkedlist) Insert_at_index(index int, pointer uintptr) {
	if index == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(index - 1)
		навбатӣnode := previousnode.навбатӣ
		навnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if навnode == nil {
			return
		}
		навnode.pointer = pointer

		previousnode.навбатӣ = навnode
		навnode.previous = previousnode
		навnode.навбатӣ = навбатӣnode
		if навбатӣnode != nil {
			навбатӣnode.previous = навnode
		}

		self.Size_2++

		if навnode.навбатӣ == nil {
			self.tail = навnode
		}
	}
}
func (self *Linkedlist) Getnodeat(index int) *Node {
	if index < 0 || index >= self.Size_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.навбатӣ
	}
	return x
}

func (self *Linkedlist) Setnodeat(index int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.навбатӣ
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
		n = n.навбатӣ
	}
	return -1
}
func (self *Linkedlist) Нобудкардан(pointer uintptr) {
	index := self.Indexof(pointer)
	if index < 0 {
		return
	}
	self.Нобудкарданat(index)
}
func (self *Linkedlist) Нобудкарданat(index int) {
	if index < 0 || index >= self.Size_2 {
		return
	}
	node := self.Getnodeat(index)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.навбатӣ = node.навбатӣ
	} else {
		self.head = node.навбатӣ
	}
	if node.навбатӣ != nil {
		node.навбатӣ.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Size_2 = self.Size_2 - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Чопкардан() {
	console_2.MЧопкарданxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Чопкардан(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Size_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32Чопкардан(uint32(node.pointer))
		console_2.MЧопкардан(":")
	}
}
