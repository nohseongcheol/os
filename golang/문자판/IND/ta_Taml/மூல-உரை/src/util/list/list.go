package list

import . "unsafe"
import . "console"
import mem "நினைவகம்"

type Node struct {
	முகவரிச்_சுட்டி		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vஅளவு	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vதொடங்கு(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vஅளவு = 0

	self.mem = mem
}
func (self *LinkedList) Vபட்டியலின்_தொடக்கத்தில்_சேர்(முகவரிச்_சுட்டி uintptr) {
	newNode := (*Node)(self.mem.Vநினைவகத்தை_ஒதுக்கு(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.முகவரிச்_சுட்டி = முகவரிச்_சுட்டி
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vஅளவு++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) Vபட்டியலின்_முடிவில்_சேர்(முகவரிச்_சுட்டி uintptr) {
	if self.Vஅளவு == 0 {
		self.Vபட்டியலின்_தொடக்கத்தில்_சேர்(முகவரிச்_சுட்டி)
	} else {
		newNode := (*Node)(self.mem.Vநினைவகத்தை_ஒதுக்கு(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.முகவரிச்_சுட்டி = முகவரிச்_சுட்டி
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vஅளவு++
	}
}
func (self *LinkedList) PushAt(index int, முகவரிச்_சுட்டி uintptr) {
	if index == 0 {
		self.Vபட்டியலின்_தொடக்கத்தில்_சேர்(முகவரிச்_சுட்டி)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Vநினைவகத்தை_ஒதுக்கு(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.முகவரிச்_சுட்டி = முகவரிச்_சுட்டி

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vஅளவு++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vஅளவு {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, முகவரிச்_சுட்டி uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.முகவரிச்_சுட்டி = முகவரிச்_சுட்டி
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var முகவரிச்_சுட்டி uintptr = node.முகவரிச்_சுட்டி
	return Pointer(முகவரிச்_சுட்டி)
}
func (self *LinkedList) IndexOf(முகவரிச்_சுட்டி uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vஅளவு; i++ {
		if முகவரிச்_சுட்டி == n.முகவரிச்_சுட்டி {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(முகவரிச்_சுட்டி uintptr) {
	index := self.IndexOf(முகவரிச்_சுட்டி)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vஅளவு {
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
	self.Vஅளவு = self.Vஅளவு - 1

	if self.mem != nil {
		self.mem.Vநினைவகத்தை_விடுவி(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vஅளவு; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.முகவரிச்_சுட்டி))
		콘솔.M출력(":")
	}
}
