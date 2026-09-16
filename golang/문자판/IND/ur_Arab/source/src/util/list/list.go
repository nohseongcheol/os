/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "حافظہ"

type Node struct {
	پتے_کا_حوالہ		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vحجم	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vآغاز_کرنا(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vحجم = 0

	self.mem = mem
}
func (self *LinkedList) Vفہرست_کے_شروع_میں_شامل_کرنا(پتے_کا_حوالہ uintptr) {
	newNode := (*Node)(self.mem.Vحافظہ_مختص_کرنا(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.پتے_کا_حوالہ = پتے_کا_حوالہ
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vحجم++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) Vفہرست_کے_آخر_میں_شامل_کرنا(پتے_کا_حوالہ uintptr) {
	if self.Vحجم == 0 {
		self.Vفہرست_کے_شروع_میں_شامل_کرنا(پتے_کا_حوالہ)
	} else {
		newNode := (*Node)(self.mem.Vحافظہ_مختص_کرنا(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.پتے_کا_حوالہ = پتے_کا_حوالہ
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vحجم++
	}
}
func (self *LinkedList) PushAt(index int, پتے_کا_حوالہ uintptr) {
	if index == 0 {
		self.Vفہرست_کے_شروع_میں_شامل_کرنا(پتے_کا_حوالہ)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Vحافظہ_مختص_کرنا(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.پتے_کا_حوالہ = پتے_کا_حوالہ

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vحجم++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vحجم {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, پتے_کا_حوالہ uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.پتے_کا_حوالہ = پتے_کا_حوالہ
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var پتے_کا_حوالہ uintptr = node.پتے_کا_حوالہ
	return Pointer(پتے_کا_حوالہ)
}
func (self *LinkedList) IndexOf(پتے_کا_حوالہ uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vحجم; i++ {
		if پتے_کا_حوالہ == n.پتے_کا_حوالہ {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(پتے_کا_حوالہ uintptr) {
	index := self.IndexOf(پتے_کا_حوالہ)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vحجم {
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
	self.Vحجم = self.Vحجم - 1

	if self.mem != nil {
		self.mem.Vحافظہ_آزاد_کرنا(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vحجم; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.پتے_کا_حوالہ))
		콘솔.M출력(":")
	}
}
