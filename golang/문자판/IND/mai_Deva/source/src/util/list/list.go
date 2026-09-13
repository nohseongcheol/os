package list

import . "unsafe"
import . "console"
import mem "स्मृति"

type Node struct {
	पता_संदर्भ		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vआकार	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vआरंभ_करब(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vआकार = 0

	self.mem = mem
}
func (self *LinkedList) PushFront(पता_संदर्भ uintptr) {
	newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.पता_संदर्भ = पता_संदर्भ
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
func (self *LinkedList) PushBack(पता_संदर्भ uintptr) {
	if self.Vआकार == 0 {
		self.PushFront(पता_संदर्भ)
	} else {
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.पता_संदर्भ = पता_संदर्भ
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vआकार++
	}
}
func (self *LinkedList) PushAt(index int, पता_संदर्भ uintptr) {
	if index == 0 {
		self.PushFront(पता_संदर्भ)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.पता_संदर्भ = पता_संदर्भ

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

func (self *LinkedList) SetNodeAt(index int, पता_संदर्भ uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.पता_संदर्भ = पता_संदर्भ
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var पता_संदर्भ uintptr = node.पता_संदर्भ
	return Pointer(पता_संदर्भ)
}
func (self *LinkedList) IndexOf(पता_संदर्भ uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vआकार; i++ {
		if पता_संदर्भ == n.पता_संदर्भ {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(पता_संदर्भ uintptr) {
	index := self.IndexOf(पता_संदर्भ)
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
		self.mem.Free(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vआकार; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.पता_संदर्भ))
		콘솔.M출력(":")
	}
}
