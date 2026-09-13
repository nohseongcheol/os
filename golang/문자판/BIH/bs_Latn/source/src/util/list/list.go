package list

import . "unsafe"
import . "console"
import mem "memorijamanager"

type Node struct {
	pointer		uintptr
	previous	*Node
	sljedeće	*Node
}

type Linkedlist struct {
	head		*Node
	tail		*Node
	Veličina_2	int

	mem	*mem.TMemorijamanager
}

func (self *Linkedlist) Init(mem *mem.TMemorijamanager) {
	self.head = nil
	self.tail = nil
	self.Veličina_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	novanode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if novanode == nil {
		return
	}
	novanode.pointer = pointer
	novanode.previous = nil
	novanode.sljedeće = self.head
	if self.head != nil {
		self.head.previous = novanode
	}
	self.head = novanode
	self.Veličina_2++

	if self.head.sljedeće == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Veličina_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		novanode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if novanode == nil {
			return
		}
		novanode.pointer = pointer
		novanode.previous = self.tail
		novanode.sljedeće = nil
		self.tail.sljedeće = novanode
		self.tail = novanode
		self.Veličina_2++
	}
}
func (self *Linkedlist) Insert_at_index(indeks int, pointer uintptr) {
	if indeks == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(indeks - 1)
		sljedećenode := previousnode.sljedeće
		novanode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if novanode == nil {
			return
		}
		novanode.pointer = pointer

		previousnode.sljedeće = novanode
		novanode.previous = previousnode
		novanode.sljedeće = sljedećenode
		if sljedećenode != nil {
			sljedećenode.previous = novanode
		}

		self.Veličina_2++

		if novanode.sljedeće == nil {
			self.tail = novanode
		}
	}
}
func (self *Linkedlist) Getnodeat(indeks int) *Node {
	if indeks < 0 || indeks >= self.Veličina_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < indeks; i++ {
		x = x.sljedeće
	}
	return x
}

func (self *Linkedlist) Skupnodeat(indeks int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < indeks; i++ {
		x = x.sljedeće
	}
	if x != nil {
		x.pointer = pointer
	}
}
func (self *Linkedlist) Getat(indeks int) Pointer {
	node := self.Getnodeat(indeks)
	if node == nil {
		return nil
	}
	var pointer uintptr = node.pointer
	return Pointer(pointer)
}
func (self *Linkedlist) Indeksof(pointer uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Veličina_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.sljedeće
	}
	return -1
}
func (self *Linkedlist) Ukloni(pointer uintptr) {
	indeks := self.Indeksof(pointer)
	if indeks < 0 {
		return
	}
	self.Ukloniat(indeks)
}
func (self *Linkedlist) Ukloniat(indeks int) {
	if indeks < 0 || indeks >= self.Veličina_2 {
		return
	}
	node := self.Getnodeat(indeks)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.sljedeće = node.sljedeće
	} else {
		self.head = node.sljedeće
	}
	if node.sljedeće != nil {
		node.sljedeće.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Veličina_2 = self.Veličina_2 - 1

	if self.mem != nil {
		self.mem.Slobodno(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Štampaj() {
	console_2.MŠtampajxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Veličina_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32Štampaj(uint32(node.pointer))
		console_2.MŠtampaj(":")
	}
}
