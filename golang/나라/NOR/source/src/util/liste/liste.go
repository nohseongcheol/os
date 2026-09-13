package liste

import . "unsafe"
import . "console"
import mem "minnemanager"

type Node struct {
	peker		uintptr
	previous	*Node
	neste		*Node
}

type LinkedListe struct {
	head		*Node
	tail		*Node
	Størrelse_2	int

	mem	*mem.TMinnemanager
}

func (selv *LinkedListe) Init(mem *mem.TMinnemanager) {
	selv.head = nil
	selv.tail = nil
	selv.Størrelse_2 = 0

	selv.mem = mem
}
func (selv *LinkedListe) Prepend_to_list(peker uintptr) {
	nynode := (*Node)(selv.mem.Malloc(uint32(Sizeof(Node{}))))
	if nynode == nil {
		return
	}
	nynode.peker = peker
	nynode.previous = nil
	nynode.neste = selv.head
	if selv.head != nil {
		selv.head.previous = nynode
	}
	selv.head = nynode
	selv.Størrelse_2++

	if selv.head.neste == nil {
		selv.tail = selv.head
	}

}
func (selv *LinkedListe) Append_to_list(peker uintptr) {
	if selv.Størrelse_2 == 0 {
		selv.Prepend_to_list(peker)
	} else {
		nynode := (*Node)(selv.mem.Malloc(uint32(Sizeof(Node{}))))
		if nynode == nil {
			return
		}
		nynode.peker = peker
		nynode.previous = selv.tail
		nynode.neste = nil
		selv.tail.neste = nynode
		selv.tail = nynode
		selv.Størrelse_2++
	}
}
func (selv *LinkedListe) Insert_at_index(indeks int, peker uintptr) {
	if indeks == 0 {
		selv.Prepend_to_list(peker)
	} else {
		previousnode := selv.Getnodeat(indeks - 1)
		nestenode := previousnode.neste
		nynode := (*Node)(selv.mem.Malloc(uint32(Sizeof(Node{}))))
		if nynode == nil {
			return
		}
		nynode.peker = peker

		previousnode.neste = nynode
		nynode.previous = previousnode
		nynode.neste = nestenode
		if nestenode != nil {
			nestenode.previous = nynode
		}

		selv.Størrelse_2++

		if nynode.neste == nil {
			selv.tail = nynode
		}
	}
}
func (selv *LinkedListe) Getnodeat(indeks int) *Node {
	if indeks < 0 || indeks >= selv.Størrelse_2 {
		return nil
	}
	var x *Node = selv.head
	for i := 0; i < indeks; i++ {
		x = x.neste
	}
	return x
}

func (selv *LinkedListe) Settnodeat(indeks int, peker uintptr) {
	var x *Node = selv.head
	for i := 0; i < indeks; i++ {
		x = x.neste
	}
	if x != nil {
		x.peker = peker
	}
}
func (selv *LinkedListe) Getat(indeks int) Pointer {
	node := selv.Getnodeat(indeks)
	if node == nil {
		return nil
	}
	var peker uintptr = node.peker
	return Pointer(peker)
}
func (selv *LinkedListe) Indeksav(peker uintptr) int {
	var n *Node = selv.head
	i := 0
	for ; i < selv.Størrelse_2; i++ {
		if peker == n.peker {
			return i
		}
		n = n.neste
	}
	return -1
}
func (selv *LinkedListe) Fjern(peker uintptr) {
	indeks := selv.Indeksav(peker)
	if indeks < 0 {
		return
	}
	selv.Fjernat(indeks)
}
func (selv *LinkedListe) Fjernat(indeks int) {
	if indeks < 0 || indeks >= selv.Størrelse_2 {
		return
	}
	node := selv.Getnodeat(indeks)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.neste = node.neste
	} else {
		selv.head = node.neste
	}
	if node.neste != nil {
		node.neste.previous = node.previous
	} else {
		selv.tail = node.previous
	}
	selv.Størrelse_2 = selv.Størrelse_2 - 1

	if selv.mem != nil {
		selv.mem.Ledig(Pointer(node))
	}
}

var console_2 = TConsole{}

func (selv *LinkedListe) Skrivut() {
	console_2.MSkrivutxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(selv))))
	for i := 0; i < selv.Størrelse_2; i++ {
		node := (*Node)(selv.Getat(i))
		console_2.MUnsignedinteger32Skrivut(uint32(node.peker))
		console_2.MSkrivut(":")
	}
}
