/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package list

import . "unsafe"
import . "console"
import mem "حافظهmanager"

type Node struct {
	pointer		uintptr
	previous	*Node
	بعدی		*Node
}

type Linkedlist struct {
	head		*Node
	tail		*Node
	Sاندازه_2	int

	mem	*mem.Tحافظهmanager
}

func (خود *Linkedlist) Init(mem *mem.Tحافظهmanager) {
	خود.head = nil
	خود.tail = nil
	خود.Sاندازه_2 = 0

	خود.mem = mem
}
func (خود *Linkedlist) Prepend_to_list(pointer uintptr) {
	جدیدnode := (*Node)(خود.mem.Malloc(uint32(Sizeof(Node{}))))
	if جدیدnode == nil {
		return
	}
	جدیدnode.pointer = pointer
	جدیدnode.previous = nil
	جدیدnode.بعدی = خود.head
	if خود.head != nil {
		خود.head.previous = جدیدnode
	}
	خود.head = جدیدnode
	خود.Sاندازه_2++

	if خود.head.بعدی == nil {
		خود.tail = خود.head
	}

}
func (خود *Linkedlist) Append_to_list(pointer uintptr) {
	if خود.Sاندازه_2 == 0 {
		خود.Prepend_to_list(pointer)
	} else {
		جدیدnode := (*Node)(خود.mem.Malloc(uint32(Sizeof(Node{}))))
		if جدیدnode == nil {
			return
		}
		جدیدnode.pointer = pointer
		جدیدnode.previous = خود.tail
		جدیدnode.بعدی = nil
		خود.tail.بعدی = جدیدnode
		خود.tail = جدیدnode
		خود.Sاندازه_2++
	}
}
func (خود *Linkedlist) Insert_at_index(نمایه int, pointer uintptr) {
	if نمایه == 0 {
		خود.Prepend_to_list(pointer)
	} else {
		previousnode := خود.Getnodeat(نمایه - 1)
		بعدیnode := previousnode.بعدی
		جدیدnode := (*Node)(خود.mem.Malloc(uint32(Sizeof(Node{}))))
		if جدیدnode == nil {
			return
		}
		جدیدnode.pointer = pointer

		previousnode.بعدی = جدیدnode
		جدیدnode.previous = previousnode
		جدیدnode.بعدی = بعدیnode
		if بعدیnode != nil {
			بعدیnode.previous = جدیدnode
		}

		خود.Sاندازه_2++

		if جدیدnode.بعدی == nil {
			خود.tail = جدیدnode
		}
	}
}
func (خود *Linkedlist) Getnodeat(نمایه int) *Node {
	if نمایه < 0 || نمایه >= خود.Sاندازه_2 {
		return nil
	}
	var x *Node = خود.head
	for i := 0; i < نمایه; i++ {
		x = x.بعدی
	}
	return x
}

func (خود *Linkedlist) Setnodeat(نمایه int, pointer uintptr) {
	var x *Node = خود.head
	for i := 0; i < نمایه; i++ {
		x = x.بعدی
	}
	if x != nil {
		x.pointer = pointer
	}
}
func (خود *Linkedlist) Getat(نمایه int) Pointer {
	node := خود.Getnodeat(نمایه)
	if node == nil {
		return nil
	}
	var pointer uintptr = node.pointer
	return Pointer(pointer)
}
func (خود *Linkedlist) Iنمایهof(pointer uintptr) int {
	var n *Node = خود.head
	i := 0
	for ; i < خود.Sاندازه_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.بعدی
	}
	return -1
}
func (خود *Linkedlist) Rحذف(pointer uintptr) {
	نمایه := خود.Iنمایهof(pointer)
	if نمایه < 0 {
		return
	}
	خود.Rحذفat(نمایه)
}
func (خود *Linkedlist) Rحذفat(نمایه int) {
	if نمایه < 0 || نمایه >= خود.Sاندازه_2 {
		return
	}
	node := خود.Getnodeat(نمایه)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.بعدی = node.بعدی
	} else {
		خود.head = node.بعدی
	}
	if node.بعدی != nil {
		node.بعدی.previous = node.previous
	} else {
		خود.tail = node.previous
	}
	خود.Sاندازه_2 = خود.Sاندازه_2 - 1

	if خود.mem != nil {
		خود.mem.Fآزاد(Pointer(node))
	}
}

var console_2 = TConsole{}

func (خود *Linkedlist) Pچاپ() {
	console_2.Mچاپxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32چاپ(uint32(uintptr(Pointer(خود))))
	for i := 0; i < خود.Sاندازه_2; i++ {
		node := (*Node)(خود.Getat(i))
		console_2.MUnsignedinteger32چاپ(uint32(node.pointer))
		console_2.Mچاپ(":")
	}
}
