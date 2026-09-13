package listă

import . "unsafe"
import . "console"
import mem "memoriemanager"

type Node struct {
	indicator	uintptr
	previous	*Node
	înainte		*Node
}

type LinkedListă struct {
	head		*Node
	tail		*Node
	Mărime_2	int

	mem	*mem.TMemoriemanager
}

func (sine *LinkedListă) Init(mem *mem.TMemoriemanager) {
	sine.head = nil
	sine.tail = nil
	sine.Mărime_2 = 0

	sine.mem = mem
}
func (sine *LinkedListă) Prepend_to_list(indicator uintptr) {
	nounode := (*Node)(sine.mem.Malloc(uint32(Sizeof(Node{}))))
	if nounode == nil {
		return
	}
	nounode.indicator = indicator
	nounode.previous = nil
	nounode.înainte = sine.head
	if sine.head != nil {
		sine.head.previous = nounode
	}
	sine.head = nounode
	sine.Mărime_2++

	if sine.head.înainte == nil {
		sine.tail = sine.head
	}

}
func (sine *LinkedListă) Append_to_list(indicator uintptr) {
	if sine.Mărime_2 == 0 {
		sine.Prepend_to_list(indicator)
	} else {
		nounode := (*Node)(sine.mem.Malloc(uint32(Sizeof(Node{}))))
		if nounode == nil {
			return
		}
		nounode.indicator = indicator
		nounode.previous = sine.tail
		nounode.înainte = nil
		sine.tail.înainte = nounode
		sine.tail = nounode
		sine.Mărime_2++
	}
}
func (sine *LinkedListă) Insert_at_index(index int, indicator uintptr) {
	if index == 0 {
		sine.Prepend_to_list(indicator)
	} else {
		previousnode := sine.Getnodeat(index - 1)
		înaintenode := previousnode.înainte
		nounode := (*Node)(sine.mem.Malloc(uint32(Sizeof(Node{}))))
		if nounode == nil {
			return
		}
		nounode.indicator = indicator

		previousnode.înainte = nounode
		nounode.previous = previousnode
		nounode.înainte = înaintenode
		if înaintenode != nil {
			înaintenode.previous = nounode
		}

		sine.Mărime_2++

		if nounode.înainte == nil {
			sine.tail = nounode
		}
	}
}
func (sine *LinkedListă) Getnodeat(index int) *Node {
	if index < 0 || index >= sine.Mărime_2 {
		return nil
	}
	var x *Node = sine.head
	for i := 0; i < index; i++ {
		x = x.înainte
	}
	return x
}

func (sine *LinkedListă) Definitnodeat(index int, indicator uintptr) {
	var x *Node = sine.head
	for i := 0; i < index; i++ {
		x = x.înainte
	}
	if x != nil {
		x.indicator = indicator
	}
}
func (sine *LinkedListă) Getat(index int) Pointer {
	node := sine.Getnodeat(index)
	if node == nil {
		return nil
	}
	var indicator uintptr = node.indicator
	return Pointer(indicator)
}
func (sine *LinkedListă) Indexdin(indicator uintptr) int {
	var n *Node = sine.head
	i := 0
	for ; i < sine.Mărime_2; i++ {
		if indicator == n.indicator {
			return i
		}
		n = n.înainte
	}
	return -1
}
func (sine *LinkedListă) Elimină(indicator uintptr) {
	index := sine.Indexdin(indicator)
	if index < 0 {
		return
	}
	sine.Eliminăat(index)
}
func (sine *LinkedListă) Eliminăat(index int) {
	if index < 0 || index >= sine.Mărime_2 {
		return
	}
	node := sine.Getnodeat(index)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.înainte = node.înainte
	} else {
		sine.head = node.înainte
	}
	if node.înainte != nil {
		node.înainte.previous = node.previous
	} else {
		sine.tail = node.previous
	}
	sine.Mărime_2 = sine.Mărime_2 - 1

	if sine.mem != nil {
		sine.mem.Liber(Pointer(node))
	}
}

var console_2 = TConsole{}

func (sine *LinkedListă) Tipărește() {
	console_2.MTipăreștexy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Tipărește(uint32(uintptr(Pointer(sine))))
	for i := 0; i < sine.Mărime_2; i++ {
		node := (*Node)(sine.Getat(i))
		console_2.MUnsignedinteger32Tipărește(uint32(node.indicator))
		console_2.MTipărește(":")
	}
}
