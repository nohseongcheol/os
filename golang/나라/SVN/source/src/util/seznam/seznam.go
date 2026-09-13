package seznam

import . "unsafe"
import . "console"
import mem "pomnilnikmanager"

type Node struct {
	kazalnik	uintptr
	previous	*Node
	naslednje	*Node
}

type LinkedSeznam struct {
	head		*Node
	tail		*Node
	Velikost_2	int

	mem	*mem.TPomnilnikmanager
}

func (sam *LinkedSeznam) Init(mem *mem.TPomnilnikmanager) {
	sam.head = nil
	sam.tail = nil
	sam.Velikost_2 = 0

	sam.mem = mem
}
func (sam *LinkedSeznam) Prepend_to_list(kazalnik uintptr) {
	novanode := (*Node)(sam.mem.Malloc(uint32(Sizeof(Node{}))))
	if novanode == nil {
		return
	}
	novanode.kazalnik = kazalnik
	novanode.previous = nil
	novanode.naslednje = sam.head
	if sam.head != nil {
		sam.head.previous = novanode
	}
	sam.head = novanode
	sam.Velikost_2++

	if sam.head.naslednje == nil {
		sam.tail = sam.head
	}

}
func (sam *LinkedSeznam) Append_to_list(kazalnik uintptr) {
	if sam.Velikost_2 == 0 {
		sam.Prepend_to_list(kazalnik)
	} else {
		novanode := (*Node)(sam.mem.Malloc(uint32(Sizeof(Node{}))))
		if novanode == nil {
			return
		}
		novanode.kazalnik = kazalnik
		novanode.previous = sam.tail
		novanode.naslednje = nil
		sam.tail.naslednje = novanode
		sam.tail = novanode
		sam.Velikost_2++
	}
}
func (sam *LinkedSeznam) Insert_at_index(kazalo int, kazalnik uintptr) {
	if kazalo == 0 {
		sam.Prepend_to_list(kazalnik)
	} else {
		previousnode := sam.Getnodeat(kazalo - 1)
		naslednjenode := previousnode.naslednje
		novanode := (*Node)(sam.mem.Malloc(uint32(Sizeof(Node{}))))
		if novanode == nil {
			return
		}
		novanode.kazalnik = kazalnik

		previousnode.naslednje = novanode
		novanode.previous = previousnode
		novanode.naslednje = naslednjenode
		if naslednjenode != nil {
			naslednjenode.previous = novanode
		}

		sam.Velikost_2++

		if novanode.naslednje == nil {
			sam.tail = novanode
		}
	}
}
func (sam *LinkedSeznam) Getnodeat(kazalo int) *Node {
	if kazalo < 0 || kazalo >= sam.Velikost_2 {
		return nil
	}
	var x *Node = sam.head
	for i := 0; i < kazalo; i++ {
		x = x.naslednje
	}
	return x
}

func (sam *LinkedSeznam) Množicanodeat(kazalo int, kazalnik uintptr) {
	var x *Node = sam.head
	for i := 0; i < kazalo; i++ {
		x = x.naslednje
	}
	if x != nil {
		x.kazalnik = kazalnik
	}
}
func (sam *LinkedSeznam) Getat(kazalo int) Pointer {
	node := sam.Getnodeat(kazalo)
	if node == nil {
		return nil
	}
	var kazalnik uintptr = node.kazalnik
	return Pointer(kazalnik)
}
func (sam *LinkedSeznam) Kazalood(kazalnik uintptr) int {
	var n *Node = sam.head
	i := 0
	for ; i < sam.Velikost_2; i++ {
		if kazalnik == n.kazalnik {
			return i
		}
		n = n.naslednje
	}
	return -1
}
func (sam *LinkedSeznam) Odstrani(kazalnik uintptr) {
	kazalo := sam.Kazalood(kazalnik)
	if kazalo < 0 {
		return
	}
	sam.Odstraniat(kazalo)
}
func (sam *LinkedSeznam) Odstraniat(kazalo int) {
	if kazalo < 0 || kazalo >= sam.Velikost_2 {
		return
	}
	node := sam.Getnodeat(kazalo)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.naslednje = node.naslednje
	} else {
		sam.head = node.naslednje
	}
	if node.naslednje != nil {
		node.naslednje.previous = node.previous
	} else {
		sam.tail = node.previous
	}
	sam.Velikost_2 = sam.Velikost_2 - 1

	if sam.mem != nil {
		sam.mem.Prosto(Pointer(node))
	}
}

var console_2 = TConsole{}

func (sam *LinkedSeznam) Natisni() {
	console_2.MNatisnixy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Natisni(uint32(uintptr(Pointer(sam))))
	for i := 0; i < sam.Velikost_2; i++ {
		node := (*Node)(sam.Getat(i))
		console_2.MUnsignedinteger32Natisni(uint32(node.kazalnik))
		console_2.MNatisni(":")
	}
}
