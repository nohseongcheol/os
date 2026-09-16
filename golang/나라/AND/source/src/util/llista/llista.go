/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package llista

import . "unsafe"
import . "consola"
import mem "memòriamanager"

type Node struct {
	punter		uintptr
	previous	*Node
	següent		*Node
}

type LinkedLlista struct {
	head	*Node
	tail	*Node
	Mida_2	int

	mem	*mem.TMemòriamanager
}

func (unmateix *LinkedLlista) Init(mem *mem.TMemòriamanager) {
	unmateix.head = nil
	unmateix.tail = nil
	unmateix.Mida_2 = 0

	unmateix.mem = mem
}
func (unmateix *LinkedLlista) Prepend_to_list(punter uintptr) {
	nounode := (*Node)(unmateix.mem.Malloc(uint32(Sizeof(Node{}))))
	if nounode == nil {
		return
	}
	nounode.punter = punter
	nounode.previous = nil
	nounode.següent = unmateix.head
	if unmateix.head != nil {
		unmateix.head.previous = nounode
	}
	unmateix.head = nounode
	unmateix.Mida_2++

	if unmateix.head.següent == nil {
		unmateix.tail = unmateix.head
	}

}
func (unmateix *LinkedLlista) Append_to_list(punter uintptr) {
	if unmateix.Mida_2 == 0 {
		unmateix.Prepend_to_list(punter)
	} else {
		nounode := (*Node)(unmateix.mem.Malloc(uint32(Sizeof(Node{}))))
		if nounode == nil {
			return
		}
		nounode.punter = punter
		nounode.previous = unmateix.tail
		nounode.següent = nil
		unmateix.tail.següent = nounode
		unmateix.tail = nounode
		unmateix.Mida_2++
	}
}
func (unmateix *LinkedLlista) Insert_at_index(índex int, punter uintptr) {
	if índex == 0 {
		unmateix.Prepend_to_list(punter)
	} else {
		previousnode := unmateix.Getnodeat(índex - 1)
		següentnode := previousnode.següent
		nounode := (*Node)(unmateix.mem.Malloc(uint32(Sizeof(Node{}))))
		if nounode == nil {
			return
		}
		nounode.punter = punter

		previousnode.següent = nounode
		nounode.previous = previousnode
		nounode.següent = següentnode
		if següentnode != nil {
			següentnode.previous = nounode
		}

		unmateix.Mida_2++

		if nounode.següent == nil {
			unmateix.tail = nounode
		}
	}
}
func (unmateix *LinkedLlista) Getnodeat(índex int) *Node {
	if índex < 0 || índex >= unmateix.Mida_2 {
		return nil
	}
	var x *Node = unmateix.head
	for i := 0; i < índex; i++ {
		x = x.següent
	}
	return x
}

func (unmateix *LinkedLlista) Estableixnodeat(índex int, punter uintptr) {
	var x *Node = unmateix.head
	for i := 0; i < índex; i++ {
		x = x.següent
	}
	if x != nil {
		x.punter = punter
	}
}
func (unmateix *LinkedLlista) Getat(índex int) Pointer {
	node := unmateix.Getnodeat(índex)
	if node == nil {
		return nil
	}
	var punter uintptr = node.punter
	return Pointer(punter)
}
func (unmateix *LinkedLlista) Índexde(punter uintptr) int {
	var n *Node = unmateix.head
	i := 0
	for ; i < unmateix.Mida_2; i++ {
		if punter == n.punter {
			return i
		}
		n = n.següent
	}
	return -1
}
func (unmateix *LinkedLlista) Elimina(punter uintptr) {
	índex := unmateix.Índexde(punter)
	if índex < 0 {
		return
	}
	unmateix.Eliminaat(índex)
}
func (unmateix *LinkedLlista) Eliminaat(índex int) {
	if índex < 0 || índex >= unmateix.Mida_2 {
		return
	}
	node := unmateix.Getnodeat(índex)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.següent = node.següent
	} else {
		unmateix.head = node.següent
	}
	if node.següent != nil {
		node.següent.previous = node.previous
	} else {
		unmateix.tail = node.previous
	}
	unmateix.Mida_2 = unmateix.Mida_2 - 1

	if unmateix.mem != nil {
		unmateix.mem.Lliure(Pointer(node))
	}
}

var consola_2 = TConsola{}

func (unmateix *LinkedLlista) Imprimeix() {
	consola_2.MImprimeixxy("LinkedList:", 1, 1)
	consola_2.MUnsignedinteger32Imprimeix(uint32(uintptr(Pointer(unmateix))))
	for i := 0; i < unmateix.Mida_2; i++ {
		node := (*Node)(unmateix.Getat(i))
		consola_2.MUnsignedinteger32Imprimeix(uint32(node.punter))
		consola_2.MImprimeix(":")
	}
}
