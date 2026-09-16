/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package სია

import . "unsafe"
import . "console"
import mem "მეხსიერებაmanager"

type Node struct {
	კურსორი		uintptr
	previous	*Node
	შემდეგი		*Node
}

type Linkedსია struct {
	head	*Node
	tail	*Node
	Sზომა_2	int

	mem	*mem.Tმეხსიერებაmanager
}

func (self *Linkedსია) Init(mem *mem.Tმეხსიერებაmanager) {
	self.head = nil
	self.tail = nil
	self.Sზომა_2 = 0

	self.mem = mem
}
func (self *Linkedსია) Prepend_to_list(კურსორი uintptr) {
	ახალიnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
	if ახალიnode == nil {
		return
	}
	ახალიnode.კურსორი = კურსორი
	ახალიnode.previous = nil
	ახალიnode.შემდეგი = self.head
	if self.head != nil {
		self.head.previous = ახალიnode
	}
	self.head = ახალიnode
	self.Sზომა_2++

	if self.head.შემდეგი == nil {
		self.tail = self.head
	}

}
func (self *Linkedსია) Append_to_list(კურსორი uintptr) {
	if self.Sზომა_2 == 0 {
		self.Prepend_to_list(კურსორი)
	} else {
		ახალიnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if ახალიnode == nil {
			return
		}
		ახალიnode.კურსორი = კურსორი
		ახალიnode.previous = self.tail
		ახალიnode.შემდეგი = nil
		self.tail.შემდეგი = ახალიnode
		self.tail = ახალიnode
		self.Sზომა_2++
	}
}
func (self *Linkedსია) Insert_at_index(ინდექსი int, კურსორი uintptr) {
	if ინდექსი == 0 {
		self.Prepend_to_list(კურსორი)
	} else {
		previousnode := self.Getnodeat(ინდექსი - 1)
		შემდეგიnode := previousnode.შემდეგი
		ახალიnode := (*Node)(self.mem.Malloc(uint32(Sizeof(Node{}))))
		if ახალიnode == nil {
			return
		}
		ახალიnode.კურსორი = კურსორი

		previousnode.შემდეგი = ახალიnode
		ახალიnode.previous = previousnode
		ახალიnode.შემდეგი = შემდეგიnode
		if შემდეგიnode != nil {
			შემდეგიnode.previous = ახალიnode
		}

		self.Sზომა_2++

		if ახალიnode.შემდეგი == nil {
			self.tail = ახალიnode
		}
	}
}
func (self *Linkedსია) Getnodeat(ინდექსი int) *Node {
	if ინდექსი < 0 || ინდექსი >= self.Sზომა_2 {
		return nil
	}
	var x *Node = self.head
	for i := 0; i < ინდექსი; i++ {
		x = x.შემდეგი
	}
	return x
}

func (self *Linkedსია) Setnodeat(ინდექსი int, კურსორი uintptr) {
	var x *Node = self.head
	for i := 0; i < ინდექსი; i++ {
		x = x.შემდეგი
	}
	if x != nil {
		x.კურსორი = კურსორი
	}
}
func (self *Linkedსია) Getat(ინდექსი int) Pointer {
	node := self.Getnodeat(ინდექსი)
	if node == nil {
		return nil
	}
	var კურსორი uintptr = node.კურსორი
	return Pointer(კურსორი)
}
func (self *Linkedსია) Iინდექსიof(კურსორი uintptr) int {
	var n *Node = self.head
	i := 0
	for ; i < self.Sზომა_2; i++ {
		if კურსორი == n.კურსორი {
			return i
		}
		n = n.შემდეგი
	}
	return -1
}
func (self *Linkedსია) Rწაშლა(კურსორი uintptr) {
	ინდექსი := self.Iინდექსიof(კურსორი)
	if ინდექსი < 0 {
		return
	}
	self.Rწაშლაat(ინდექსი)
}
func (self *Linkedსია) Rწაშლაat(ინდექსი int) {
	if ინდექსი < 0 || ინდექსი >= self.Sზომა_2 {
		return
	}
	node := self.Getnodeat(ინდექსი)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.შემდეგი = node.შემდეგი
	} else {
		self.head = node.შემდეგი
	}
	if node.შემდეგი != nil {
		node.შემდეგი.previous = node.previous
	} else {
		self.tail = node.previous
	}
	self.Sზომა_2 = self.Sზომა_2 - 1

	if self.mem != nil {
		self.mem.Fთავისუფალი(Pointer(node))
	}
}

var console_2 = TConsole{}

func (self *Linkedსია) Pბეჭდვა() {
	console_2.Mბეჭდვაxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32ბეჭდვა(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Sზომა_2; i++ {
		node := (*Node)(self.Getat(i))
		console_2.MUnsignedinteger32ბეჭდვა(uint32(node.კურსორი))
		console_2.Mბეჭდვა(":")
	}
}
