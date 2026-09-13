package list

import . "unsafe"
import . "console"
import mem "સ્મૃતિ"

type Node struct {
	સરનામા_નિર્દેશક		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vકદ	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vઆરંભ_કરવો(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vકદ = 0

	self.mem = mem
}
func (self *LinkedList) Vસૂચિની_શરૂઆતમાં_ઉમેરવું(સરનામા_નિર્દેશક uintptr) {
	newNode := (*Node)(self.mem.Vસ્મૃતિ_ફાળવવી(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.સરનામા_નિર્દેશક = સરનામા_નિર્દેશક
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vકદ++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) Vસૂચિના_અંતે_ઉમેરવું(સરનામા_નિર્દેશક uintptr) {
	if self.Vકદ == 0 {
		self.Vસૂચિની_શરૂઆતમાં_ઉમેરવું(સરનામા_નિર્દેશક)
	} else {
		newNode := (*Node)(self.mem.Vસ્મૃતિ_ફાળવવી(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.સરનામા_નિર્દેશક = સરનામા_નિર્દેશક
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vકદ++
	}
}
func (self *LinkedList) PushAt(index int, સરનામા_નિર્દેશક uintptr) {
	if index == 0 {
		self.Vસૂચિની_શરૂઆતમાં_ઉમેરવું(સરનામા_નિર્દેશક)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Vસ્મૃતિ_ફાળવવી(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.સરનામા_નિર્દેશક = સરનામા_નિર્દેશક

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vકદ++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vકદ {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, સરનામા_નિર્દેશક uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.સરનામા_નિર્દેશક = સરનામા_નિર્દેશક
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var સરનામા_નિર્દેશક uintptr = node.સરનામા_નિર્દેશક
	return Pointer(સરનામા_નિર્દેશક)
}
func (self *LinkedList) IndexOf(સરનામા_નિર્દેશક uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vકદ; i++ {
		if સરનામા_નિર્દેશક == n.સરનામા_નિર્દેશક {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(સરનામા_નિર્દેશક uintptr) {
	index := self.IndexOf(સરનામા_નિર્દેશક)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vકદ {
		return
	}
	node := self.GetNodeAt(index)
	if node == nil {
		return
	}
	if node.prev != nil {
		node.prev.next = node.next
	} else {
		self.head = node.next
	}
	if node.next != nil {
		node.next.prev = node.prev
	} else {
		self.tail = node.prev
	}
	self.Vકદ = self.Vકદ - 1

	if self.mem != nil {
		self.mem.Vસ્મૃતિ_મુક્ત_કરવી(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vકદ; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.સરનામા_નિર્દેશક))
		콘솔.M출력(":")
	}
}
