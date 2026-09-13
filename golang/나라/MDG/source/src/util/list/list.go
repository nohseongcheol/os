package list

import . "unsafe"
import . "konsoly"
import mem "arikaMpandrindra"

type Node struct {
	pointer		uintptr
	previous	*Node
	manaraka	*Node
}

type Linkedlist struct {
	head	*Node
	tail	*Node
	Habe_2	int

	mem	*mem.TArikaMpandrindra
}

func (nytena *Linkedlist) Init(mem *mem.TArikaMpandrindra) {
	nytena.head = nil
	nytena.tail = nil
	nytena.Habe_2 = 0

	nytena.mem = mem
}
func (nytena *Linkedlist) Prepend_to_list(pointer uintptr) {
	vaovaonode := (*Node)(nytena.mem.Malloc(uint32(Sizeof(Node{}))))
	if vaovaonode == nil {
		return
	}
	vaovaonode.pointer = pointer
	vaovaonode.previous = nil
	vaovaonode.manaraka = nytena.head
	if nytena.head != nil {
		nytena.head.previous = vaovaonode
	}
	nytena.head = vaovaonode
	nytena.Habe_2++

	if nytena.head.manaraka == nil {
		nytena.tail = nytena.head
	}

}
func (nytena *Linkedlist) Append_to_list(pointer uintptr) {
	if nytena.Habe_2 == 0 {
		nytena.Prepend_to_list(pointer)
	} else {
		vaovaonode := (*Node)(nytena.mem.Malloc(uint32(Sizeof(Node{}))))
		if vaovaonode == nil {
			return
		}
		vaovaonode.pointer = pointer
		vaovaonode.previous = nytena.tail
		vaovaonode.manaraka = nil
		nytena.tail.manaraka = vaovaonode
		nytena.tail = vaovaonode
		nytena.Habe_2++
	}
}
func (nytena *Linkedlist) Insert_at_index(fizahantakila int, pointer uintptr) {
	if fizahantakila == 0 {
		nytena.Prepend_to_list(pointer)
	} else {
		previousnode := nytena.Getnodeat(fizahantakila - 1)
		manarakanode := previousnode.manaraka
		vaovaonode := (*Node)(nytena.mem.Malloc(uint32(Sizeof(Node{}))))
		if vaovaonode == nil {
			return
		}
		vaovaonode.pointer = pointer

		previousnode.manaraka = vaovaonode
		vaovaonode.previous = previousnode
		vaovaonode.manaraka = manarakanode
		if manarakanode != nil {
			manarakanode.previous = vaovaonode
		}

		nytena.Habe_2++

		if vaovaonode.manaraka == nil {
			nytena.tail = vaovaonode
		}
	}
}
func (nytena *Linkedlist) Getnodeat(fizahantakila int) *Node {
	if fizahantakila < 0 || fizahantakila >= nytena.Habe_2 {
		return nil
	}
	var x *Node = nytena.head
	for i := 0; i < fizahantakila; i++ {
		x = x.manaraka
	}
	return x
}

func (nytena *Linkedlist) Setnodeat(fizahantakila int, pointer uintptr) {
	var x *Node = nytena.head
	for i := 0; i < fizahantakila; i++ {
		x = x.manaraka
	}
	if x != nil {
		x.pointer = pointer
	}
}
func (nytena *Linkedlist) Getat(fizahantakila int) Pointer {
	node := nytena.Getnodeat(fizahantakila)
	if node == nil {
		return nil
	}
	var pointer uintptr = node.pointer
	return Pointer(pointer)
}
func (nytena *Linkedlist) Fizahantakilaaminny(pointer uintptr) int {
	var n *Node = nytena.head
	i := 0
	for ; i < nytena.Habe_2; i++ {
		if pointer == n.pointer {
			return i
		}
		n = n.manaraka
	}
	return -1
}
func (nytena *Linkedlist) Esory(pointer uintptr) {
	fizahantakila := nytena.Fizahantakilaaminny(pointer)
	if fizahantakila < 0 {
		return
	}
	nytena.Esoryat(fizahantakila)
}
func (nytena *Linkedlist) Esoryat(fizahantakila int) {
	if fizahantakila < 0 || fizahantakila >= nytena.Habe_2 {
		return
	}
	node := nytena.Getnodeat(fizahantakila)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.manaraka = node.manaraka
	} else {
		nytena.head = node.manaraka
	}
	if node.manaraka != nil {
		node.manaraka.previous = node.previous
	} else {
		nytena.tail = node.previous
	}
	nytena.Habe_2 = nytena.Habe_2 - 1

	if nytena.mem != nil {
		nytena.mem.Malalaka(Pointer(node))
	}
}

var konsoly_2 = TKonsoly{}

func (nytena *Linkedlist) Atontay() {
	konsoly_2.MAtontayxy("LinkedList:", 1, 1)
	konsoly_2.MUnsignedinteger32Atontay(uint32(uintptr(Pointer(nytena))))
	for i := 0; i < nytena.Habe_2; i++ {
		node := (*Node)(nytena.Getat(i))
		konsoly_2.MUnsignedinteger32Atontay(uint32(node.pointer))
		konsoly_2.MAtontay(":")
	}
}
