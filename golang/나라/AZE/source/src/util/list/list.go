package list

import . "unsafe"
import . "console"
import mem "yaddaşmanager"

type Node struct {
	pointer		uintptr
	previous	*Node
	sonrakı		*Node
}

type Linkedlist struct {
	head		*Node
	tail		*Node
	Böyüklük_2	int

	mem	*mem.TYaddaşmanager
}

func (self *Linkedlist) Init(mem *mem.TYaddaşmanager) {
	self.head = nil
	self.tail = nil
	self.Böyüklük_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	yeninode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if yeninode == nil {
		return
	}
	yeninode.pointer = pointer
	yeninode.previous = nil
	yeninode.sonrakı = self.head
	if self.head != nil {
		self.head.previous = yeninode
	}
	self.head = yeninode
	self.Böyüklük_2++

	if self.head.sonrakı == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Böyüklük_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		yeninode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if yeninode == nil {
			return
		}
		yeninode.pointer = pointer
		yeninode.previous = self.tail
		yeninode.sonrakı = nil
		self.tail.sonrakı = yeninode
		self.tail = yeninode
		self.Böyüklük_2++
	}
}
func (self *Linkedlist) Insert_at_index(index int, pointer uintptr) {
	if index == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(index - 1)
		sonrakınode := previousnode.sonrakı
		yeninode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if yeninode == nil {
			return
		}
		yeninode.pointer = pointer

		previousnode.sonrakı = yeninode
		yeninode.previous = previousnode
		yeninode.sonrakı = sonrakınode
		if sonrakınode != nil {
			sonrakınode.previous = yeninode
		}

		self.Böyüklük_2++

		if yeninode.sonrakı == nil {
			self.tail = yeninode
		}
	}
}
func (self *Linkedlist) Getnodeat(index int) *Node {
	if index < 0 || index >= self.Böyüklük_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.sonrakı
	}
	return x
}

func (self *Linkedlist) Setnodeat(index int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.sonrakı
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
	for ; i < self.Böyüklük_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.sonrakı
	}
	return -1
}
func (self *Linkedlist) Çıxart(pointer uintptr) {
	index := self.Indexof(pointer)
	if index < 0 {
		return
	}
	self.Çıxartat(index)
}
func (self *Linkedlist) Çıxartat(index int) {
	if index < 0 || index >= self.Böyüklük_2 {
		return
	}
	node := self.Getnodeat(index)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.sonrakı = node.sonrakı
	} else {
		self.head = node.sonrakı
	}
	if node.sonrakı != nil {
		node.sonrakı.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Böyüklük_2 = self.Böyüklük_2 - 1

	if self.mem != nil {
		self.mem.Boş(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) ÇapEt() {
	console_2.MÇapEtxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32ÇapEt(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Böyüklük_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32ÇapEt(uint32(node.pointer))
		console_2.MÇapEt(":")
	}
}
