package list

import . "unsafe"
import . "console"
import mem "memorymanager"

type Node struct {
	pointer		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Size	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Init(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Size = 0

	self.mem = mem
}
func (self *LinkedList) PushFront(pointer uintptr) {
	newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.pointer = pointer
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Size++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) PushBack(pointer uintptr) {
	if self.Size == 0 {
		self.PushFront(pointer)
	} else {
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.pointer = pointer
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Size++
	}
}
func (self *LinkedList) PushAt(index int, pointer uintptr) {
	if index == 0 {
		self.PushFront(pointer)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.pointer = pointer

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Size++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Size {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, pointer uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.pointer = pointer
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var pointer uintptr = node.pointer
	return Pointer(pointer)
}
func (self *LinkedList) IndexOf(pointer uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Size; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(pointer uintptr) {
	index := self.IndexOf(pointer)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Size {
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
	self.Size = self.Size - 1

	if self.mem != nil {
		self.mem.Free(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Size; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.pointer))
		콘솔.M출력(":")
	}
}
