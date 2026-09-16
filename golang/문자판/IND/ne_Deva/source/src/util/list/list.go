/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "स्मृति"

type Node struct {
	ठेगाना_सूचक		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vआकार	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vआरम्भ_गर्नु(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vआकार = 0

	self.mem = mem
}
func (self *LinkedList) Vसूचीको_सुरुमा_थप्नु(ठेगाना_सूचक uintptr) {
	newNode := (*Node)(self.mem.Vस्मृति_छुट्याउनु(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.ठेगाना_सूचक = ठेगाना_सूचक
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vआकार++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) Vसूचीको_अन्त्यमा_थप्नु(ठेगाना_सूचक uintptr) {
	if self.Vआकार == 0 {
		self.Vसूचीको_सुरुमा_थप्नु(ठेगाना_सूचक)
	} else {
		newNode := (*Node)(self.mem.Vस्मृति_छुट्याउनु(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ठेगाना_सूचक = ठेगाना_सूचक
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vआकार++
	}
}
func (self *LinkedList) PushAt(index int, ठेगाना_सूचक uintptr) {
	if index == 0 {
		self.Vसूचीको_सुरुमा_थप्नु(ठेगाना_सूचक)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Vस्मृति_छुट्याउनु(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ठेगाना_सूचक = ठेगाना_सूचक

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vआकार++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vआकार {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, ठेगाना_सूचक uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.ठेगाना_सूचक = ठेगाना_सूचक
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var ठेगाना_सूचक uintptr = node.ठेगाना_सूचक
	return Pointer(ठेगाना_सूचक)
}
func (self *LinkedList) IndexOf(ठेगाना_सूचक uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vआकार; i++ {
		if ठेगाना_सूचक == n.ठेगाना_सूचक {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(ठेगाना_सूचक uintptr) {
	index := self.IndexOf(ठेगाना_सूचक)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vआकार {
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
	self.Vआकार = self.Vआकार - 1

	if self.mem != nil {
		self.mem.Vस्मृति_मुक्त_गर्नु(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vआकार; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.ठेगाना_सूचक))
		콘솔.M출력(":")
	}
}
