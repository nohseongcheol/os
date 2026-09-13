package ዝርዝር

import . "unsafe"
import . "console"
import mem "ማስታወሻmanager"

type Node struct {
	ጠቋሚ		uintptr
	previous	*Node
	የሚቀጥለው		*Node
}

type Linkedዝርዝር struct {
	head	*Node
	tail	*Node
	Sመጠን_2	int

	mem	*mem.Tማስታወሻmanager
}

func (self *Linkedዝርዝር) Init(mem *mem.Tማስታወሻmanager) {
	self.head = nil
	self.tail = nil
	self.Sመጠን_2 = 0

	self.mem = mem
}
func (self *Linkedዝርዝር) Prepend_to_list(ጠቋሚ uintptr) {
	አዲስnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if አዲስnode == nil {
		return
	}
	አዲስnode.ጠቋሚ = ጠቋሚ
	አዲስnode.previous = nil
	አዲስnode.የሚቀጥለው = self.head
	if self.head != nil {
		self.head.previous = አዲስnode
	}
	self.head = አዲስnode
	self.Sመጠን_2++

	if self.head.የሚቀጥለው == nil {
		self.tail = self.head
	}

}
func (self *Linkedዝርዝር) Append_to_list(ጠቋሚ uintptr) {
	if self.Sመጠን_2 == 0 {
		self.Prepend_to_list(ጠቋሚ)
	} else {
		አዲስnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if አዲስnode == nil {
			return
		}
		አዲስnode.ጠቋሚ = ጠቋሚ
		አዲስnode.previous = self.tail
		አዲስnode.የሚቀጥለው = nil
		self.tail.የሚቀጥለው = አዲስnode
		self.tail = አዲስnode
		self.Sመጠን_2++
	}
}
func (self *Linkedዝርዝር) Insert_at_index(ማውጫ int, ጠቋሚ uintptr) {
	if ማውጫ == 0 {
		self.Prepend_to_list(ጠቋሚ)
	} else {
		previousnode := self.Getnodeat(ማውጫ - 1)
		የሚቀጥለውnode := previousnode.የሚቀጥለው
		አዲስnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if አዲስnode == nil {
			return
		}
		አዲስnode.ጠቋሚ = ጠቋሚ

		previousnode.የሚቀጥለው = አዲስnode
		አዲስnode.previous = previousnode
		አዲስnode.የሚቀጥለው = የሚቀጥለውnode
		if የሚቀጥለውnode != nil {
			የሚቀጥለውnode.previous = አዲስnode
		}

		self.Sመጠን_2++

		if አዲስnode.የሚቀጥለው == nil {
			self.tail = አዲስnode
		}
	}
}
func (self *Linkedዝርዝር) Getnodeat(ማውጫ int) *Node {
	if ማውጫ < 0 || ማውጫ >= self.Sመጠን_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < ማውጫ; i++ {
		x = x.የሚቀጥለው
	}
	return x
}

func (self *Linkedዝርዝር) Setnodeat(ማውጫ int, ጠቋሚ uintptr) {
	var x *Node = self.head
	for i := 0; i < ማውጫ; i++ {
		x = x.የሚቀጥለው
	}
	if x != nil {
		x.ጠቋሚ = ጠቋሚ
	}
}
func (self *Linkedዝርዝር) Getat(ማውጫ int) Pointer {
	node := self.Getnodeat(ማውጫ)
	if node == nil {
		return nil
	}
	var ጠቋሚ uintptr = node.ጠቋሚ
	return Pointer(ጠቋሚ)
}
func (self *Linkedዝርዝር) Iማውጫከ(ጠቋሚ uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Sመጠን_2; i++ {
		if ጠቋሚ == n.ጠቋሚ {
			return i
		}
		n = n.የሚቀጥለው
	}
	return -1
}
func (self *Linkedዝርዝር) Rአስወግድ(ጠቋሚ uintptr) {
	ማውጫ := self.Iማውጫከ(ጠቋሚ)
	if ማውጫ < 0 {
		return
	}
	self.Rአስወግድat(ማውጫ)
}
func (self *Linkedዝርዝር) Rአስወግድat(ማውጫ int) {
	if ማውጫ < 0 || ማውጫ >= self.Sመጠን_2 {
		return
	}
	node := self.Getnodeat(ማውጫ)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.የሚቀጥለው = node.የሚቀጥለው
	} else {
		self.head = node.የሚቀጥለው
	}
	if node.የሚቀጥለው != nil {
		node.የሚቀጥለው.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Sመጠን_2 = self.Sመጠን_2 - 1

	if self.mem != nil {
		self.mem.Fነፃ(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedዝርዝር) Pማተሚያ() {
	console_2.Mማተሚያxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32ማተሚያ(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sመጠን_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32ማተሚያ(uint32(node.ጠቋሚ))
		console_2.Mማተሚያ(":")
	}
}
