package list

import . "unsafe"
import . "console"
import mem "ഓർമ്മ"

type Node struct {
	വിലാസ_സൂചിക		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vവലുപ്പം	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vആരംഭിക്കുക(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vവലുപ്പം = 0

	self.mem = mem
}
func (self *LinkedList) Vപട്ടികയുടെ_തുടക്കത്തിൽ_ചേർക്കുക(വിലാസ_സൂചിക uintptr) {
	newNode := (*Node)(self.mem.Vഓർമ്മസ്ഥലം_അനുവദിക്കുക(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.വിലാസ_സൂചിക = വിലാസ_സൂചിക
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vവലുപ്പം++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) Vപട്ടികയുടെ_അവസാനം_ചേർക്കുക(വിലാസ_സൂചിക uintptr) {
	if self.Vവലുപ്പം == 0 {
		self.Vപട്ടികയുടെ_തുടക്കത്തിൽ_ചേർക്കുക(വിലാസ_സൂചിക)
	} else {
		newNode := (*Node)(self.mem.Vഓർമ്മസ്ഥലം_അനുവദിക്കുക(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.വിലാസ_സൂചിക = വിലാസ_സൂചിക
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vവലുപ്പം++
	}
}
func (self *LinkedList) PushAt(index int, വിലാസ_സൂചിക uintptr) {
	if index == 0 {
		self.Vപട്ടികയുടെ_തുടക്കത്തിൽ_ചേർക്കുക(വിലാസ_സൂചിക)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Vഓർമ്മസ്ഥലം_അനുവദിക്കുക(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.വിലാസ_സൂചിക = വിലാസ_സൂചിക

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vവലുപ്പം++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vവലുപ്പം {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, വിലാസ_സൂചിക uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.വിലാസ_സൂചിക = വിലാസ_സൂചിക
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var വിലാസ_സൂചിക uintptr = node.വിലാസ_സൂചിക
	return Pointer(വിലാസ_സൂചിക)
}
func (self *LinkedList) IndexOf(വിലാസ_സൂചിക uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vവലുപ്പം; i++ {
		if വിലാസ_സൂചിക == n.വിലാസ_സൂചിക {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(വിലാസ_സൂചിക uintptr) {
	index := self.IndexOf(വിലാസ_സൂചിക)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vവലുപ്പം {
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
	self.Vവലുപ്പം = self.Vവലുപ്പം - 1

	if self.mem != nil {
		self.mem.Vഓർമ്മസ്ഥലം_വിടുക(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vവലുപ്പം; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.വിലാസ_സൂചിക))
		콘솔.M출력(":")
	}
}
