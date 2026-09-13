package спіс

import . "unsafe"
import . "console"
import mem "памяцьmanager"

type Node struct {
	паказальнік	uintptr
	previous	*Node
	наступны	*Node
}

type LinkedСпіс struct {
	head	*Node
	tail	*Node
	Памер_2	int

	mem	*mem.TПамяцьmanager
}

func (self *LinkedСпіс) Init(mem *mem.TПамяцьmanager) {
	self.head = nil
	self.tail = nil
	self.Памер_2 = 0

	self.mem = mem
}
func (self *LinkedСпіс) Prepend_to_list(паказальнік uintptr) {
	новыnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if новыnode == nil {
		return
	}
	новыnode.паказальнік = паказальнік
	новыnode.previous = nil
	новыnode.наступны = self.head
	if self.head != nil {
		self.head.previous = новыnode
	}
	self.head = новыnode
	self.Памер_2++

	if self.head.наступны == nil {
		self.tail = self.head
	}

}
func (self *LinkedСпіс) Append_to_list(паказальнік uintptr) {
	if self.Памер_2 == 0 {
		self.Prepend_to_list(паказальнік)
	} else {
		новыnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if новыnode == nil {
			return
		}
		новыnode.паказальнік = паказальнік
		новыnode.previous = self.tail
		новыnode.наступны = nil
		self.tail.наступны = новыnode
		self.tail = новыnode
		self.Памер_2++
	}
}
func (self *LinkedСпіс) Insert_at_index(змест int, паказальнік uintptr) {
	if змест == 0 {
		self.Prepend_to_list(паказальнік)
	} else {
		previousnode := self.Getnodeat(змест - 1)
		наступныnode := previousnode.наступны
		новыnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if новыnode == nil {
			return
		}
		новыnode.паказальнік = паказальнік

		previousnode.наступны = новыnode
		новыnode.previous = previousnode
		новыnode.наступны = наступныnode
		if наступныnode != nil {
			наступныnode.previous = новыnode
		}

		self.Памер_2++

		if новыnode.наступны == nil {
			self.tail = новыnode
		}
	}
}
func (self *LinkedСпіс) Getnodeat(змест int) *Node {
	if змест < 0 || змест >= self.Памер_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < змест; i++ {
		x = x.наступны
	}
	return x
}

func (self *LinkedСпіс) Вызначанаnodeat(змест int, паказальнік uintptr) {
	var x *Node = self.head
	for i := 0; i < змест; i++ {
		x = x.наступны
	}
	if x != nil {
		x.паказальнік = паказальнік
	}
}
func (self *LinkedСпіс) Getat(змест int) Pointer {
	node := self.Getnodeat(змест)
	if node == nil {
		return nil
	}
	var паказальнік uintptr = node.паказальнік
	return Pointer(паказальнік)
}
func (self *LinkedСпіс) Зместз(паказальнік uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Памер_2; i++ {
		if паказальнік == n.паказальнік {
			return i
		}
		n = n.наступны
	}
	return -1
}
func (self *LinkedСпіс) Выдаліць_2(паказальнік uintptr) {
	змест := self.Зместз(паказальнік)
	if змест < 0 {
		return
	}
	self.Выдаліцьat(змест)
}
func (self *LinkedСпіс) Выдаліцьat(змест int) {
	if змест < 0 || змест >= self.Памер_2 {
		return
	}
	node := self.Getnodeat(змест)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.наступны = node.наступны
	} else {
		self.head = node.наступны
	}
	if node.наступны != nil {
		node.наступны.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Памер_2 = self.Памер_2 - 1

	if self.mem != nil {
		self.mem.Вольна(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *LinkedСпіс) Друкаваць() {
	console_2.MДрукавацьxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Друкаваць(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Памер_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32Друкаваць(uint32(node.паказальнік))
		console_2.MДрукаваць(":")
	}
}
