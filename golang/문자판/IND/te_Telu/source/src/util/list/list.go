package list

import . "unsafe"
import . "console"
import mem "జ్ఞాపకస్థలం"

type Node struct {
	చిరునామా_సూచిక		uintptr
	prev	*Node
	next		*Node
}

type LinkedList struct {
	head	*Node
	tail	*Node
	Vపరిమాణం	int

	mem	*mem.TMemoryManager
}

func (self *LinkedList) Vప్రారంభించు(mem *mem.TMemoryManager) {
	self.head = nil
	self.tail = nil
	self.Vపరిమాణం = 0

	self.mem = mem
}
func (self *LinkedList) Vజాబితా_మొదట_చేర్చు(చిరునామా_సూచిక uintptr) {
	newNode := (*Node)(self.mem.Vజ్ఞాపకస్థలాన్ని_కేటాయించు(uint32(Sizeof(Node{}))))
	if newNode == nil {
		return
	}
	newNode.చిరునామా_సూచిక = చిరునామా_సూచిక
	newNode.prev = nil
	newNode.next = self.head
	if self.head != nil {
		self.head.prev = newNode
	}
	self.head = newNode
	self.Vపరిమాణం++

	if self.head.next == nil {
		self.tail = self.head
	}

}
func (self *LinkedList) Vజాబితా_చివర_చేర్చు(చిరునామా_సూచిక uintptr) {
	if self.Vపరిమాణం == 0 {
		self.Vజాబితా_మొదట_చేర్చు(చిరునామా_సూచిక)
	} else {
		newNode := (*Node)(self.mem.Vజ్ఞాపకస్థలాన్ని_కేటాయించు(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.చిరునామా_సూచిక = చిరునామా_సూచిక
		newNode.prev = self.tail
		newNode.next = nil
		self.tail.next = newNode
		self.tail = newNode
		self.Vపరిమాణం++
	}
}
func (self *LinkedList) PushAt(index int, చిరునామా_సూచిక uintptr) {
	if index == 0 {
		self.Vజాబితా_మొదట_చేర్చు(చిరునామా_సూచిక)
	} else {
		prevNode := self.GetNodeAt(index - 1)
		nextNode := prevNode.next
		newNode := (*Node)(self.mem.Vజ్ఞాపకస్థలాన్ని_కేటాయించు(uint32(Sizeof(Node{}))))
		if newNode == nil {
			return
		}
		newNode.చిరునామా_సూచిక = చిరునామా_సూచిక

		prevNode.next = newNode
		newNode.prev = prevNode
		newNode.next = nextNode
		if nextNode != nil {
			nextNode.prev = newNode
		}

		self.Vపరిమాణం++

		if newNode.next == nil {
			self.tail = newNode
		}
	}
}
func (self *LinkedList) GetNodeAt(index int) *Node {
	if index < 0 || index >= self.Vపరిమాణం {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	return x
}

func (self *LinkedList) SetNodeAt(index int, చిరునామా_సూచిక uintptr) {
	var x *Node = self.head
	for i := 0; i < index; i++ {
		x = x.next
	}
	if x != nil {
		x.చిరునామా_సూచిక = చిరునామా_సూచిక
	}
}
func (self *LinkedList) GetAt(index int) Pointer {
	node := self.GetNodeAt(index)
	if node == nil {
		return nil
	}
	var చిరునామా_సూచిక uintptr = node.చిరునామా_సూచిక
	return Pointer(చిరునామా_సూచిక)
}
func (self *LinkedList) IndexOf(చిరునామా_సూచిక uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Vపరిమాణం; i++ {
		if చిరునామా_సూచిక == n.చిరునామా_సూచిక {
			return i
		}
		n = n.next
	}
	return -1
}
func (self *LinkedList) Remove(చిరునామా_సూచిక uintptr) {
	index := self.IndexOf(చిరునామా_సూచిక)
	if index < 0 {
		return
	}
	self.RemoveAt(index)
}
func (self *LinkedList) RemoveAt(index int) {
	if index < 0 || index >= self.Vపరిమాణం {
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
	self.Vపరిమాణం = self.Vపరిమాణం - 1

	if self.mem != nil {
		self.mem.Vజ్ఞాపకస్థలాన్ని_విడుదల_చేయి(Pointer(node))
	}
}

var 콘솔 = T콘솔{}

func (self *LinkedList) Print() {
	콘솔.M출력XY("LinkedList:", 1, 1)
	콘솔.MUint32출력(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Vపరిమాణం; i++ {
		node := (*Node)(self.GetAt(i))
		콘솔.MUint32출력(uint32(node.చిరునామా_సూచిక))
		콘솔.M출력(":")
	}
}
