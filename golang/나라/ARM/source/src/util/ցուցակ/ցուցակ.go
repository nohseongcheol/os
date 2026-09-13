package ցուցակ

import . "unsafe"
import . "console"
import mem "հիշողությունmanager"

type Node struct {
	ցուցիչ		uintptr
	previous	*Node
	հաջորդ		*Node
}

type LinkedՑուցակ struct {
	head	*Node
	tail	*Node
	Չափս_2	int

	mem	*mem.TՀիշողությունmanager
}

func (ինքնուրույն *LinkedՑուցակ) Init(mem *mem.TՀիշողությունmanager) {
	ինքնուրույն.head = nil
	ինքնուրույն.tail = nil
	ինքնուրույն.Չափս_2 = 0

	ինքնուրույն.mem = mem
}
func (ինքնուրույն *LinkedՑուցակ) Prepend_to_list(ցուցիչ uintptr) {
	նորnode := (*Node)(ինքնուրույն.mem.Malloc(uint32(Sizeof(Node{}))))
	if նորnode == nil {
		return
	}
	նորnode.ցուցիչ = ցուցիչ
	նորnode.previous = nil
	նորnode.հաջորդ = ինքնուրույն.head
	if ինքնուրույն.head != nil {
		ինքնուրույն.head.previous = նորnode
	}
	ինքնուրույն.head = նորnode
	ինքնուրույն.Չափս_2++

	if ինքնուրույն.head.հաջորդ == nil {
		ինքնուրույն.tail = ինքնուրույն.head
	}

}
func (ինքնուրույն *LinkedՑուցակ) Append_to_list(ցուցիչ uintptr) {
	if ինքնուրույն.Չափս_2 == 0 {
		ինքնուրույն.Prepend_to_list(ցուցիչ)
	} else {
		նորnode := (*Node)(ինքնուրույն.mem.Malloc(uint32(Sizeof(Node{}))))
		if նորnode == nil {
			return
		}
		նորnode.ցուցիչ = ցուցիչ
		նորnode.previous = ինքնուրույն.tail
		նորnode.հաջորդ = nil
		ինքնուրույն.tail.հաջորդ = նորnode
		ինքնուրույն.tail = նորnode
		ինքնուրույն.Չափս_2++
	}
}
func (ինքնուրույն *LinkedՑուցակ) Insert_at_index(ինդեքս int, ցուցիչ uintptr) {
	if ինդեքս == 0 {
		ինքնուրույն.Prepend_to_list(ցուցիչ)
	} else {
		previousnode := ինքնուրույն.Getnodeat(ինդեքս - 1)
		հաջորդnode := previousnode.հաջորդ
		նորnode := (*Node)(ինքնուրույն.mem.Malloc(uint32(Sizeof(Node{}))))
		if նորnode == nil {
			return
		}
		նորnode.ցուցիչ = ցուցիչ

		previousnode.հաջորդ = նորnode
		նորnode.previous = previousnode
		նորnode.հաջորդ = հաջորդnode
		if հաջորդnode != nil {
			հաջորդnode.previous = նորnode
		}

		ինքնուրույն.Չափս_2++

		if նորnode.հաջորդ == nil {
			ինքնուրույն.tail = նորnode
		}
	}
}
func (ինքնուրույն *LinkedՑուցակ) Getnodeat(ինդեքս int) *Node {
	if ինդեքս < 0 || ինդեքս >= ինքնուրույն.Չափս_2 {
		return nil
	}
	var x *Node = ինքնուրույն.head
	for i := 0; i < ինդեքս; i++ {
		x = x.հաջորդ
	}
	return x
}

func (ինքնուրույն *LinkedՑուցակ) Setnodeat(ինդեքս int, ցուցիչ uintptr) {
	var x *Node = ինքնուրույն.head
	for i := 0; i < ինդեքս; i++ {
		x = x.հաջորդ
	}
	if x != nil {
		x.ցուցիչ = ցուցիչ
	}
}
func (ինքնուրույն *LinkedՑուցակ) Getat(ինդեքս int) Pointer {
	node := ինքնուրույն.Getnodeat(ինդեքս)
	if node == nil {
		return nil
	}
	var ցուցիչ uintptr = node.ցուցիչ
	return Pointer(ցուցիչ)
}
func (ինքնուրույն *LinkedՑուցակ) Ինդեքսof(ցուցիչ uintptr) int {
	var n *Node = ինքնուրույն.head
	i := 0
	for ; i < ինքնուրույն.Չափս_2; i++ {
		if ցուցիչ == n.ցուցիչ {
			return i
		}
		n = n.հաջորդ
	}
	return -1
}
func (ինքնուրույն *LinkedՑուցակ) Հեռացնել_2(ցուցիչ uintptr) {
	ինդեքս := ինքնուրույն.Ինդեքսof(ցուցիչ)
	if ինդեքս < 0 {
		return
	}
	ինքնուրույն.Հեռացնելat(ինդեքս)
}
func (ինքնուրույն *LinkedՑուցակ) Հեռացնելat(ինդեքս int) {
	if ինդեքս < 0 || ինդեքս >= ինքնուրույն.Չափս_2 {
		return
	}
	node := ինքնուրույն.Getnodeat(ինդեքս)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.հաջորդ = node.հաջորդ
	} else {
		ինքնուրույն.head = node.հաջորդ
	}
	if node.հաջորդ != nil {
		node.հաջորդ.previous = node.previous
	} else {
		ինքնուրույն.tail = node.previous
	}
	ինքնուրույն.Չափս_2 = ինքնուրույն.Չափս_2 - 1

	if ինքնուրույն.mem != nil {
		ինքնուրույն.mem.Ազատ(Pointer(node))
	}
}

var console_2 = TConsole{}

func (ինքնուրույն *LinkedՑուցակ) Տպել() {
	console_2.MՏպելxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Տպել(uint32(uintptr(Pointer(ինքնուրույն))))
	for i := 0; i < ինքնուրույն.Չափս_2; i++ {
		node := (*Node)(ինքնուրույն.Getat(i))
		console_2.MUnsignedinteger32Տպել(uint32(node.ցուցիչ))
		console_2.MՏպել(":")
	}
}
