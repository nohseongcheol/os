package list

import . "unsafe"
import . "console"
import mem "ububikomanager"

type Node struct {
	pointer		uintptr
	previous	*Node
	ikurikira	*Node
}

type Linkedlist struct {
	head		*Node
	tail		*Node
	Ingano_2	int

	mem	*mem.TUbubikomanager
}

func (self *Linkedlist) Init(mem *mem.TUbubikomanager) {
	self.head = nil
	self.tail = nil
	self.Ingano_2 = 0

	self.mem = mem
}
func (self *Linkedlist) Prepend_to_list(pointer uintptr) {
	newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if newnode == nil {
		return
	}
	newnode.pointer = pointer
	newnode.previous = nil
	newnode.ikurikira = self.head
	if self.head != nil {
		self.head.previous = newnode
	}
	self.head = newnode
	self.Ingano_2++

	if self.head.ikurikira == nil {
		self.tail = self.head
	}

}
func (self *Linkedlist) Append_to_list(pointer uintptr) {
	if self.Ingano_2 == 0 {
		self.Prepend_to_list(pointer)
	} else {
		newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newnode == nil {
			return
		}
		newnode.pointer = pointer
		newnode.previous = self.tail
		newnode.ikurikira = nil
		self.tail.ikurikira = newnode
		self.tail = newnode
		self.Ingano_2++
	}
}
func (self *Linkedlist) Insert_at_index(umubarendanga int, pointer uintptr) {
	if umubarendanga == 0 {
		self.Prepend_to_list(pointer)
	} else {
		previousnode := self.Getnodeat(umubarendanga - 1)
		ikurikiranode := previousnode.ikurikira
		newnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newnode == nil {
			return
		}
		newnode.pointer = pointer

		previousnode.ikurikira = newnode
		newnode.previous = previousnode
		newnode.ikurikira = ikurikiranode
		if ikurikiranode != nil {
			ikurikiranode.previous = newnode
		}

		self.Ingano_2++

		if newnode.ikurikira == nil {
			self.tail = newnode
		}
	}
}
func (self *Linkedlist) Getnodeat(umubarendanga int) *Node {
	if umubarendanga < 0 || umubarendanga >= self.Ingano_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < umubarendanga; i++ {
		x = x.ikurikira
	}
	return x
}

func (self *Linkedlist) Setnodeat(umubarendanga int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < umubarendanga; i++ {
		x = x.ikurikira
	}
	if x != nil {
		x.pointer = pointer
	}
}
func (self *Linkedlist) Getat(umubarendanga int) Pointer {
	node := self.Getnodeat(umubarendanga)
	if node == nil {
		return nil
	}
	var pointer uintptr = node.pointer
	return Pointer(pointer)
}
func (self *Linkedlist) Umubarendangaof(pointer uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Ingano_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.ikurikira
	}
	return -1
}
func (self *Linkedlist) Gukuraho(pointer uintptr) {
	umubarendanga := self.Umubarendangaof(pointer)
	if umubarendanga < 0 {
		return
	}
	self.Gukurahoat(umubarendanga)
}
func (self *Linkedlist) Gukurahoat(umubarendanga int) {
	if umubarendanga < 0 || umubarendanga >= self.Ingano_2 {
		return
	}
	node := self.Getnodeat(umubarendanga)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.ikurikira = node.ikurikira
	} else {
		self.head = node.ikurikira
	}
	if node.ikurikira != nil {
		node.ikurikira.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Ingano_2 = self.Ingano_2 - 1

	if self.mem != nil {
		self.mem.Kigenga(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedlist) Gucapa() {
	console_2.MGucapaxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Gucapa(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Ingano_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32Gucapa(uint32(node.pointer))
		console_2.MGucapa(":")
	}
}
