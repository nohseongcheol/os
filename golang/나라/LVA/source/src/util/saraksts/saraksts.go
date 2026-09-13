package saraksts

import . "unsafe"
import . "console"
import mem "atmiņamanager"

type Node struct {
	kursors		uintptr
	previous	*Node
	nākamais	*Node
}

type LinkedSaraksts struct {
	head		*Node
	tail		*Node
	Izmērs_2	int

	mem	*mem.TAtmiņamanager
}

func (pats *LinkedSaraksts) Init(mem *mem.TAtmiņamanager) {
	pats.head = nil
	pats.tail = nil
	pats.Izmērs_2 = 0

	pats.mem = mem
}
func (pats *LinkedSaraksts) Prepend_to_list(kursors uintptr) {
	jaunsnode := (*Node)(pats.mem.Malloc(uint32(Sizeof(Node{}))))
	if jaunsnode == nil {
		return
	}
	jaunsnode.kursors = kursors
	jaunsnode.previous = nil
	jaunsnode.nākamais = pats.head
	if pats.head != nil {
		pats.head.previous = jaunsnode
	}
	pats.head = jaunsnode
	pats.Izmērs_2++

	if pats.head.nākamais == nil {
		pats.tail = pats.head
	}

}
func (pats *LinkedSaraksts) Append_to_list(kursors uintptr) {
	if pats.Izmērs_2 == 0 {
		pats.Prepend_to_list(kursors)
	} else {
		jaunsnode := (*Node)(pats.mem.Malloc(uint32(Sizeof(Node{}))))
		if jaunsnode == nil {
			return
		}
		jaunsnode.kursors = kursors
		jaunsnode.previous = pats.tail
		jaunsnode.nākamais = nil
		pats.tail.nākamais = jaunsnode
		pats.tail = jaunsnode
		pats.Izmērs_2++
	}
}
func (pats *LinkedSaraksts) Insert_at_index(saturs int, kursors uintptr) {
	if saturs == 0 {
		pats.Prepend_to_list(kursors)
	} else {
		previousnode := pats.Getnodeat(saturs - 1)
		nākamaisnode := previousnode.nākamais
		jaunsnode := (*Node)(pats.mem.Malloc(uint32(Sizeof(Node{}))))
		if jaunsnode == nil {
			return
		}
		jaunsnode.kursors = kursors

		previousnode.nākamais = jaunsnode
		jaunsnode.previous = previousnode
		jaunsnode.nākamais = nākamaisnode
		if nākamaisnode != nil {
			nākamaisnode.previous = jaunsnode
		}

		pats.Izmērs_2++

		if jaunsnode.nākamais == nil {
			pats.tail = jaunsnode
		}
	}
}
func (pats *LinkedSaraksts) Getnodeat(saturs int) *Node {
	if saturs < 0 || saturs >= pats.Izmērs_2 {
		return nil
	}
	var x *Node = pats.head
	for i := 0; i < saturs; i++ {
		x = x.nākamais
	}
	return x
}

func (pats *LinkedSaraksts) Kopanodeat(saturs int, kursors uintptr) {
	var x *Node = pats.head
	for i := 0; i < saturs; i++ {
		x = x.nākamais
	}
	if x != nil {
		x.kursors = kursors
	}
}
func (pats *LinkedSaraksts) Getat(saturs int) Pointer {
	node := pats.Getnodeat(saturs)
	if node == nil {
		return nil
	}
	var kursors uintptr = node.kursors
	return Pointer(kursors)
}
func (pats *LinkedSaraksts) Satursno(kursors uintptr) int {
	var n *Node = pats.head
	i := 0
	for ; i < pats.Izmērs_2; i++ {
		if kursors == n.kursors {
			return i
		}
		n = n.nākamais
	}
	return -1
}
func (pats *LinkedSaraksts) Izņemt(kursors uintptr) {
	saturs := pats.Satursno(kursors)
	if saturs < 0 {
		return
	}
	pats.Izņemtat(saturs)
}
func (pats *LinkedSaraksts) Izņemtat(saturs int) {
	if saturs < 0 || saturs >= pats.Izmērs_2 {
		return
	}
	node := pats.Getnodeat(saturs)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.nākamais = node.nākamais
	} else {
		pats.head = node.nākamais
	}
	if node.nākamais != nil {
		node.nākamais.previous = node.previous
	} else {
		pats.tail = node.previous
	}
	pats.Izmērs_2 = pats.Izmērs_2 - 1

	if pats.mem != nil {
		pats.mem.Brīvs(Pointer(node))
	}
}

var console_2 = TConsole{}

func (pats *LinkedSaraksts) Drukāt() {
	console_2.MDrukātxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Drukāt(uint32(uintptr(Pointer(pats))))
	for i := 0; i < pats.Izmērs_2; i++ {
		node := (*Node)(pats.Getat(i))
		console_2.MUnsignedinteger32Drukāt(uint32(node.kursors))
		console_2.MDrukāt(":")
	}
}
