package royxat

import . "unsafe"
import . "console"
import mem "xotiramanager"

type Node struct {
	korsatgich	uintptr
	previous	*Node
	keyingi		*Node
}

type Linkedroyxat struct {
	head	*Node
	tail	*Node
	Hajmi_2	int

	mem	*mem.TXotiramanager
}

func (self *Linkedroyxat) Init(mem *mem.TXotiramanager) {
	self.head = nil
	self.tail = nil
	self.Hajmi_2 = 0

	self.mem = mem
}
func (self *Linkedroyxat) Prepend_to_list(korsatgich uintptr) {
	yanginode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if yanginode == nil {
		return
	}
	yanginode.korsatgich = korsatgich
	yanginode.previous = nil
	yanginode.keyingi = self.head
	if self.head != nil {
		self.head.previous = yanginode
	}
	self.head = yanginode
	self.Hajmi_2++

	if self.head.keyingi == nil {
		self.tail = self.head
	}

}
func (self *Linkedroyxat) Append_to_list(korsatgich uintptr) {
	if self.Hajmi_2 == 0 {
		self.Prepend_to_list(korsatgich)
	} else {
		yanginode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if yanginode == nil {
			return
		}
		yanginode.korsatgich = korsatgich
		yanginode.previous = self.tail
		yanginode.keyingi = nil
		self.tail.keyingi = yanginode
		self.tail = yanginode
		self.Hajmi_2++
	}
}
func (self *Linkedroyxat) Insert_at_index(index int, korsatgich uintptr) {
	if index == 0 {
		self.Prepend_to_list(korsatgich)
	} else {
		previousnode := self.Getnodeat(index - 1)
		keyinginode := previousnode.keyingi
		yanginode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if yanginode == nil {
			return
		}
		yanginode.korsatgich = korsatgich

		previousnode.keyingi = yanginode
		yanginode.previous = previousnode
		yanginode.keyingi = keyinginode
		if keyinginode != nil {
			keyinginode.previous = yanginode
		}

		self.Hajmi_2++

		if yanginode.keyingi == nil {
			self.tail = yanginode
		}
	}
}
func (self *Linkedroyxat) Getnodeat(index int) *Node {
	if index < 0 || index >= self.Hajmi_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.keyingi
	}
	return x
}

func (self *Linkedroyxat) Setnodeat(index int, korsatgich uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.keyingi
	}
	if x != nil {
		x.korsatgich = korsatgich
	}
}
func (self *Linkedroyxat) Getat(index int) Pointer {
	node := self.Getnodeat(index)
	if node == nil {
		return nil
	}
	var korsatgich uintptr = node.korsatgich
	return Pointer(korsatgich)
}
func (self *Linkedroyxat) Indexof(korsatgich uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Hajmi_2; i++ {
		if korsatgich == n.korsatgich {
			return i
		}
		n = n.keyingi
	}
	return -1
}
func (self *Linkedroyxat) Olibtashlash_2(korsatgich uintptr) {
	index := self.Indexof(korsatgich)
	if index < 0 {
		return
	}
	self.Olibtashlashat(index)
}
func (self *Linkedroyxat) Olibtashlashat(index int) {
	if index < 0 || index >= self.Hajmi_2 {
		return
	}
	node := self.Getnodeat(index)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.keyingi = node.keyingi
	} else {
		self.head = node.keyingi
	}
	if node.keyingi != nil {
		node.keyingi.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Hajmi_2 = self.Hajmi_2 - 1

	if self.mem != nil {
		self.mem.Bosh(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedroyxat) Chopetish() {
	console_2.MChopetishxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Chopetish(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Hajmi_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32Chopetish(uint32(node.korsatgich))
		console_2.MChopetish(":")
	}
}
