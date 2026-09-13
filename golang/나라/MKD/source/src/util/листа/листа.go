package листа

import . "unsafe"
import . "console"
import mem "меморијаmanager"

type Node struct {
	стрелка		uintptr
	previous	*Node
	следна		*Node
}

type LinkedЛиста struct {
	head		*Node
	tail		*Node
	Големина_2	int

	mem	*mem.TМеморијаmanager
}

func (само *LinkedЛиста) Init(mem *mem.TМеморијаmanager) {
	само.head = nil
	само.tail = nil
	само.Големина_2 = 0

	само.mem = mem
}
func (само *LinkedЛиста) Prepend_to_list(стрелка uintptr) {
	новnode := (*Node)(само.mem.Malloc(uint32(Sizeof(Node{}))))
	if новnode == nil {
		return
	}
	новnode.стрелка = стрелка
	новnode.previous = nil
	новnode.следна = само.head
	if само.head != nil {
		само.head.previous = новnode
	}
	само.head = новnode
	само.Големина_2++

	if само.head.следна == nil {
		само.tail = само.head
	}

}
func (само *LinkedЛиста) Append_to_list(стрелка uintptr) {
	if само.Големина_2 == 0 {
		само.Prepend_to_list(стрелка)
	} else {
		новnode := (*Node)(само.mem.Malloc(uint32(Sizeof(Node{}))))
		if новnode == nil {
			return
		}
		новnode.стрелка = стрелка
		новnode.previous = само.tail
		новnode.следна = nil
		само.tail.следна = новnode
		само.tail = новnode
		само.Големина_2++
	}
}
func (само *LinkedЛиста) Insert_at_index(индекс int, стрелка uintptr) {
	if индекс == 0 {
		само.Prepend_to_list(стрелка)
	} else {
		previousnode := само.Getnodeat(индекс - 1)
		следнаnode := previousnode.следна
		новnode := (*Node)(само.mem.Malloc(uint32(Sizeof(Node{}))))
		if новnode == nil {
			return
		}
		новnode.стрелка = стрелка

		previousnode.следна = новnode
		новnode.previous = previousnode
		новnode.следна = следнаnode
		if следнаnode != nil {
			следнаnode.previous = новnode
		}

		само.Големина_2++

		if новnode.следна == nil {
			само.tail = новnode
		}
	}
}
func (само *LinkedЛиста) Getnodeat(индекс int) *Node {
	if индекс < 0 || индекс >= само.Големина_2 {
		return nil
	}
	var x *Node = само.head
	for i := 0; i < индекс; i++ {
		x = x.следна
	}
	return x
}

func (само *LinkedЛиста) Поставиnodeat(индекс int, стрелка uintptr) {
	var x *Node = само.head
	for i := 0; i < индекс; i++ {
		x = x.следна
	}
	if x != nil {
		x.стрелка = стрелка
	}
}
func (само *LinkedЛиста) Getat(индекс int) Pointer {
	node := само.Getnodeat(индекс)
	if node == nil {
		return nil
	}
	var стрелка uintptr = node.стрелка
	return Pointer(стрелка)
}
func (само *LinkedЛиста) Индексна(стрелка uintptr) int {
	var n *Node = само.head
	i := 0
	for ; i < само.Големина_2; i++ {
		if стрелка == n.стрелка {
			return i
		}
		n = n.следна
	}
	return -1
}
func (само *LinkedЛиста) Отстрани(стрелка uintptr) {
	индекс := само.Индексна(стрелка)
	if индекс < 0 {
		return
	}
	само.Отстраниat(индекс)
}
func (само *LinkedЛиста) Отстраниat(индекс int) {
	if индекс < 0 || индекс >= само.Големина_2 {
		return
	}
	node := само.Getnodeat(индекс)
	if node == nil {
		return
	}
	if node.previous != nil {
		node.previous.следна = node.следна
	} else {
		само.head = node.следна
	}
	if node.следна != nil {
		node.следна.previous = node.previous
	} else {
		само.tail = node.previous
	}
	само.Големина_2 = само.Големина_2 - 1

	if само.mem != nil {
		само.mem.Слободни(Pointer(node))
	}
}

var console_2 = TConsole{}

func (само *LinkedЛиста) Печати() {
	console_2.MПечатиxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Печати(uint32(uintptr(Pointer(само))))
	for i := 0; i < само.Големина_2; i++ {
		node := (*Node)(само.Getat(i))
		console_2.MUnsignedinteger32Печати(uint32(node.стрелка))
		console_2.MПечати(":")
	}
}
