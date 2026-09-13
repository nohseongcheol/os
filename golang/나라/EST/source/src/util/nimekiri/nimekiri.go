package nimekiri

import . "unsafe"
import . "console"
import mem "mälumanager"

type Sõlm struct {
	kursor		uintptr
	previous	*Sõlm
	järgmine	*Sõlm
}

type LinkedNimekiri struct {
	head		*Sõlm
	tail		*Sõlm
	Suurus_2	int

	mem	*mem.TMälumanager
}

func (ise *LinkedNimekiri) Init(mem *mem.TMälumanager) {
	ise.head = nil
	ise.tail = nil
	ise.Suurus_2 = 0

	ise.mem = mem
}
func (ise *LinkedNimekiri) Prepend_to_list(kursor uintptr) {
	uusSõlm := (*Sõlm)(ise.mem.Malloc(uint32(Sizeof(Sõlm{}))))
	if uusSõlm == nil {
		return
	}
	uusSõlm.kursor = kursor
	uusSõlm.previous = nil
	uusSõlm.järgmine = ise.head
	if ise.head != nil {
		ise.head.previous = uusSõlm
	}
	ise.head = uusSõlm
	ise.Suurus_2++

	if ise.head.järgmine == nil {
		ise.tail = ise.head
	}

}
func (ise *LinkedNimekiri) Append_to_list(kursor uintptr) {
	if ise.Suurus_2 == 0 {
		ise.Prepend_to_list(kursor)
	} else {
		uusSõlm := (*Sõlm)(ise.mem.Malloc(uint32(Sizeof(Sõlm{}))))
		if uusSõlm == nil {
			return
		}
		uusSõlm.kursor = kursor
		uusSõlm.previous = ise.tail
		uusSõlm.järgmine = nil
		ise.tail.järgmine = uusSõlm
		ise.tail = uusSõlm
		ise.Suurus_2++
	}
}
func (ise *LinkedNimekiri) Insert_at_index(sisukord int, kursor uintptr) {
	if sisukord == 0 {
		ise.Prepend_to_list(kursor)
	} else {
		previousSõlm := ise.GetSõlmat(sisukord - 1)
		järgmineSõlm := previousSõlm.järgmine
		uusSõlm := (*Sõlm)(ise.mem.Malloc(uint32(Sizeof(Sõlm{}))))
		if uusSõlm == nil {
			return
		}
		uusSõlm.kursor = kursor

		previousSõlm.järgmine = uusSõlm
		uusSõlm.previous = previousSõlm
		uusSõlm.järgmine = järgmineSõlm
		if järgmineSõlm != nil {
			järgmineSõlm.previous = uusSõlm
		}

		ise.Suurus_2++

		if uusSõlm.järgmine == nil {
			ise.tail = uusSõlm
		}
	}
}
func (ise *LinkedNimekiri) GetSõlmat(sisukord int) *Sõlm {
	if sisukord < 0 || sisukord >= ise.Suurus_2 {
		return nil
	}
	var x *Sõlm = ise.head
	for i := 0; i < sisukord; i++ {
		x = x.järgmine
	}
	return x
}

func (ise *LinkedNimekiri) MääraSõlmat(sisukord int, kursor uintptr) {
	var x *Sõlm = ise.head
	for i := 0; i < sisukord; i++ {
		x = x.järgmine
	}
	if x != nil {
		x.kursor = kursor
	}
}
func (ise *LinkedNimekiri) Getat(sisukord int) Pointer {
	sõlm := ise.GetSõlmat(sisukord)
	if sõlm == nil {
		return nil
	}
	var kursor uintptr = sõlm.kursor
	return Pointer(kursor)
}
func (ise *LinkedNimekiri) Sisukordof(kursor uintptr) int {
	var n *Sõlm = ise.head
	i := 0
	for ; i < ise.Suurus_2; i++ {
		if kursor == n.kursor {
			return i
		}
		n = n.järgmine
	}
	return -1
}
func (ise *LinkedNimekiri) Eemalda(kursor uintptr) {
	sisukord := ise.Sisukordof(kursor)
	if sisukord < 0 {
		return
	}
	ise.Eemaldaat(sisukord)
}
func (ise *LinkedNimekiri) Eemaldaat(sisukord int) {
	if sisukord < 0 || sisukord >= ise.Suurus_2 {
		return
	}
	sõlm := ise.GetSõlmat(sisukord)
	if sõlm == nil {
		return
	}
	if sõlm.previous != nil {
		sõlm.previous.järgmine = sõlm.järgmine
	} else {
		ise.head = sõlm.järgmine
	}
	if sõlm.järgmine != nil {
		sõlm.järgmine.previous = sõlm.previous
	} else {
		ise.tail = sõlm.previous
	}
	ise.Suurus_2 = ise.Suurus_2 - 1

	if ise.mem != nil {
		ise.mem.Vaba(Pointer(sõlm))
	}
}

var console_2 = TConsole{}

func (ise *LinkedNimekiri) Prindi() {
	console_2.MPrindixy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Prindi(uint32(uintptr(Pointer(ise))))
	for i := 0; i < ise.Suurus_2; i++ {
		sõlm := (*Sõlm)(ise.Getat(i))
		console_2.MUnsignedinteger32Prindi(uint32(sõlm.kursor))
		console_2.MPrindi(":")
	}
}
