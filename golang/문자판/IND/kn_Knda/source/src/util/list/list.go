package list

import . "unsafe"
import . "console"
import mem "ಸ್ಮೃತಿ"

type Node struct {
	ವಿಳಾಸ_ಸೂಚಕ		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vಗಾತ್ರ	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vಆರಂಭಿಸು(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vಗಾತ್ರ = 0

	self.mem = mem
}
func (self *LinkedList) Vಪಟ್ಟಿಯ_ಆರಂಭದಲ್ಲಿ_ಸೇರಿಸು(ವಿಳಾಸ_ಸೂಚಕ uintptr) {
	newNode := (*Node)(self.mem.Vಸ್ಮೃತಿಯನ್ನು_ಹಂಚು(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.ವಿಳಾಸ_ಸೂಚಕ = ವಿಳಾಸ_ಸೂಚಕ
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vಗಾತ್ರ++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) Vಪಟ್ಟಿಯ_ಕೊನೆಯಲ್ಲಿ_ಸೇರಿಸು(ವಿಳಾಸ_ಸೂಚಕ uintptr) {
	if self.Vಗಾತ್ರ == 0 {
		self.Vಪಟ್ಟಿಯ_ಆರಂಭದಲ್ಲಿ_ಸೇರಿಸು(ವಿಳಾಸ_ಸೂಚಕ)
	} else {
		newNode := (*Node)(self.mem.Vಸ್ಮೃತಿಯನ್ನು_ಹಂಚು(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ವಿಳಾಸ_ಸೂಚಕ = ವಿಳಾಸ_ಸೂಚಕ
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vಗಾತ್ರ++
	}
}
func (self *LinkedList) PushAt(index int, ವಿಳಾಸ_ಸೂಚಕ uintptr) {
	if index == 0 {
		self.Vಪಟ್ಟಿಯ_ಆರಂಭದಲ್ಲಿ_ಸೇರಿಸು(ವಿಳಾಸ_ಸೂಚಕ)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Vಸ್ಮೃತಿಯನ್ನು_ಹಂಚು(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ವಿಳಾಸ_ಸೂಚಕ = ವಿಳಾಸ_ಸೂಚಕ

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vಗಾತ್ರ++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vಗಾತ್ರ {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, ವಿಳಾಸ_ಸೂಚಕ uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.ವಿಳಾಸ_ಸೂಚಕ = ವಿಳಾಸ_ಸೂಚಕ
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var ವಿಳಾಸ_ಸೂಚಕ uintptr = node.ವಿಳಾಸ_ಸೂಚಕ
	return Pointer(ವಿಳಾಸ_ಸೂಚಕ)
}
func (self *LinkedList) IndexOf(ವಿಳಾಸ_ಸೂಚಕ uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vಗಾತ್ರ; i++ {
		if ವಿಳಾಸ_ಸೂಚಕ == n.ವಿಳಾಸ_ಸೂಚಕ {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(ವಿಳಾಸ_ಸೂಚಕ uintptr) {
	index := self.IndexOf(ವಿಳಾಸ_ಸೂಚಕ)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vಗಾತ್ರ {
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
	self.Vಗಾತ್ರ = self.Vಗಾತ್ರ - 1

	if self.mem != nil {
		self.mem.Vಸ್ಮೃತಿಯನ್ನು_ಬಿಡುಗಡೆಮಾಡು(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vಗಾತ್ರ; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.ವಿಳಾಸ_ಸೂಚಕ))
		콘솔.M출력(":")
	}
}
