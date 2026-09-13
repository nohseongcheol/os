package list

import . "unsafe"
import . "console"
import mem "স্মৃতি"

type Node struct {
	ঠিকানা_নির্দেশক		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vআকার	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vআরম্ভ_করা(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vআকার = 0

	self.mem = mem
}
func (self *LinkedList) Vতালিকার_শুরুতে_যোগ_করা(ঠিকানা_নির্দেশক uintptr) {
	newNode := (*Node)(self.mem.Vস্মৃতি_বরাদ্দ_করা(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.ঠিকানা_নির্দেশক = ঠিকানা_নির্দেশক
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vআকার++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) Vতালিকার_শেষে_যোগ_করা(ঠিকানা_নির্দেশক uintptr) {
	if self.Vআকার == 0 {
		self.Vতালিকার_শুরুতে_যোগ_করা(ঠিকানা_নির্দেশক)
	} else {
		newNode := (*Node)(self.mem.Vস্মৃতি_বরাদ্দ_করা(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ঠিকানা_নির্দেশক = ঠিকানা_নির্দেশক
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vআকার++
	}
}
func (self *LinkedList) PushAt(index int, ঠিকানা_নির্দেশক uintptr) {
	if index == 0 {
		self.Vতালিকার_শুরুতে_যোগ_করা(ঠিকানা_নির্দেশক)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Vস্মৃতি_বরাদ্দ_করা(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.ঠিকানা_নির্দেশক = ঠিকানা_নির্দেশক

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vআকার++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vআকার {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, ঠিকানা_নির্দেশক uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.ঠিকানা_নির্দেশক = ঠিকানা_নির্দেশক
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var ঠিকানা_নির্দেশক uintptr = node.ঠিকানা_নির্দেশক
	return Pointer(ঠিকানা_নির্দেশক)
}
func (self *LinkedList) IndexOf(ঠিকানা_নির্দেশক uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vআকার; i++ {
		if ঠিকানা_নির্দেশক == n.ঠিকানা_নির্দেশক {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(ঠিকানা_নির্দেশক uintptr) {
	index := self.IndexOf(ঠিকানা_নির্দেশক)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vআকার {
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
	self.Vআকার = self.Vআকার - 1

	if self.mem != nil {
		self.mem.Vস্মৃতি_মুক্ত_করা(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vআকার; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.ঠিকানা_নির্দেশক))
		콘솔.M출력(":")
	}
}
