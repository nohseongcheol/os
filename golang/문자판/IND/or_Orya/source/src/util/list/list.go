/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "ସ୍ମୃତି"

type Node struct {
	ଠିକଣା_ସୂଚକ		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vଆକାର	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vଆରମ୍ଭ_କରିବା(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vଆକାର = 0

	self.mem = mem
}
func (self *LinkedList) PushFront(ଠିକଣା_ସୂଚକ uintptr) {
	newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.ଠିକଣା_ସୂଚକ = ଠିକଣା_ସୂଚକ
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vଆକାର++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) PushBack(ଠିକଣା_ସୂଚକ uintptr) {
	if self.Vଆକାର == 0 {
		self.PushFront(ଠିକଣା_ସୂଚକ)
	} else {
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ଠିକଣା_ସୂଚକ = ଠିକଣା_ସୂଚକ
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vଆକାର++
	}
}
func (self *LinkedList) PushAt(index int, ଠିକଣା_ସୂଚକ uintptr) {
	if index == 0 {
		self.PushFront(ଠିକଣା_ସୂଚକ)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ଠିକଣା_ସୂଚକ = ଠିକଣା_ସୂଚକ

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vଆକାର++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vଆକାର {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, ଠିକଣା_ସୂଚକ uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.ଠିକଣା_ସୂଚକ = ଠିକଣା_ସୂଚକ
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var ଠିକଣା_ସୂଚକ uintptr = node.ଠିକଣା_ସୂଚକ
	return Pointer(ଠିକଣା_ସୂଚକ)
}
func (self *LinkedList) IndexOf(ଠିକଣା_ସୂଚକ uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vଆକାର; i++ {
		if ଠିକଣା_ସୂଚକ == n.ଠିକଣା_ସୂଚକ {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(ଠିକଣା_ସୂଚକ uintptr) {
	index := self.IndexOf(ଠିକଣା_ସୂଚକ)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vଆକାର {
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
	self.Vଆକାର = self.Vଆକାର - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vଆକାର; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.ଠିକଣା_ସୂଚକ))
		콘솔.M출력(":")
	}
}
