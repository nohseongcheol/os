package list

import . "unsafe"
import . "console"
import mem "স্মৃতি"

type Node struct {
	ঠিকনা_সূচক		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vআকাৰ	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vআৰম্ভ_কৰা(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vআকাৰ = 0

	self.mem = mem
}
func (self *LinkedList) PushFront(ঠিকনা_সূচক uintptr) {
	newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.ঠিকনা_সূচক = ঠিকনা_সূচক
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vআকাৰ++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) PushBack(ঠিকনা_সূচক uintptr) {
	if self.Vআকাৰ == 0 {
		self.PushFront(ঠিকনা_সূচক)
	} else {
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ঠিকনা_সূচক = ঠিকনা_সূচক
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vআকাৰ++
	}
}
func (self *LinkedList) PushAt(index int, ঠিকনা_সূচক uintptr) {
	if index == 0 {
		self.PushFront(ঠিকনা_সূচক)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ঠিকনা_সূচক = ঠিকনা_সূচক

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vআকাৰ++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vআকাৰ {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, ঠিকনা_সূচক uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.ঠিকনা_সূচক = ঠিকনা_সূচক
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var ঠিকনা_সূচক uintptr = node.ঠিকনা_সূচক
	return Pointer(ঠিকনা_সূচক)
}
func (self *LinkedList) IndexOf(ঠিকনা_সূচক uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vআকাৰ; i++ {
		if ঠিকনা_সূচক == n.ঠিকনা_সূচক {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(ঠিকনা_সূচক uintptr) {
	index := self.IndexOf(ঠিকনা_সূচক)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vআকাৰ {
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
	self.Vআকাৰ = self.Vআকাৰ - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vআকাৰ; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.ঠিকনা_সূচক))
		콘솔.M출력(":")
	}
}
