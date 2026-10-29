/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "ਯਾਦਾਸ਼ਤ"

type Node struct {
	ਪਤੇ_ਦਾ_ਹਵਾਲਾ		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vਆਕਾਰ	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vਆਰੰਭ_ਕਰਨਾ(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vਆਕਾਰ = 0

	self.mem = mem
}
func (self *LinkedList) PushFront(ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr) {
	newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.ਪਤੇ_ਦਾ_ਹਵਾਲਾ = ਪਤੇ_ਦਾ_ਹਵਾਲਾ
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vਆਕਾਰ++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) PushBack(ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr) {
	if self.Vਆਕਾਰ == 0 {
		self.PushFront(ਪਤੇ_ਦਾ_ਹਵਾਲਾ)
	} else {
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ਪਤੇ_ਦਾ_ਹਵਾਲਾ = ਪਤੇ_ਦਾ_ਹਵਾਲਾ
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vਆਕਾਰ++
	}
}
func (self *LinkedList) PushAt(index int, ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr) {
	if index == 0 {
		self.PushFront(ਪਤੇ_ਦਾ_ਹਵਾਲਾ)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ਪਤੇ_ਦਾ_ਹਵਾਲਾ = ਪਤੇ_ਦਾ_ਹਵਾਲਾ

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vਆਕਾਰ++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vਆਕਾਰ {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.ਪਤੇ_ਦਾ_ਹਵਾਲਾ = ਪਤੇ_ਦਾ_ਹਵਾਲਾ
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr = node.ਪਤੇ_ਦਾ_ਹਵਾਲਾ
	return Pointer(ਪਤੇ_ਦਾ_ਹਵਾਲਾ)
}
func (self *LinkedList) IndexOf(ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vਆਕਾਰ; i++ {
		if ਪਤੇ_ਦਾ_ਹਵਾਲਾ == n.ਪਤੇ_ਦਾ_ਹਵਾਲਾ {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(ਪਤੇ_ਦਾ_ਹਵਾਲਾ uintptr) {
	index := self.IndexOf(ਪਤੇ_ਦਾ_ਹਵਾਲਾ)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vਆਕਾਰ {
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
	self.Vਆਕਾਰ = self.Vਆਕਾਰ - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vਆਕਾਰ; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.ਪਤੇ_ਦਾ_ਹਵਾਲਾ))
		콘솔.M출력(":")
	}
}
