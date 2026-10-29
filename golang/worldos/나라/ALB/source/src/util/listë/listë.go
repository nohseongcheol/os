/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package listë

import . "unsafe"
import . "konsolë"
import mem "memoriaManazhuesi"

type Nyje struct {
	kursori		uintptr
	previous	*Nyje
	pasuesen	*Nyje
}

type LinkedListë struct {
	head		*Nyje
	tail		*Nyje
	Madhësia_2	int

	mem	*mem.TMemoriaManazhuesi
}

func (vetvetja *LinkedListë) Init(mem *mem.TMemoriaManazhuesi) {
	vetvetja.head = nil
	vetvetja.tail = nil
	vetvetja.Madhësia_2 = 0

	vetvetja.mem = mem
}
func (vetvetja *LinkedListë) Prepend_to_list(kursori uintptr) {
	iRiNyje := (*Nyje)(vetvetja.mem.Malloc(uint32(Sizeof(Nyje{}))))
	if iRiNyje == nil {
		return
	}
	iRiNyje.kursori = kursori
	iRiNyje.previous = nil
	iRiNyje.pasuesen = vetvetja.head
	if vetvetja.head != nil {
		vetvetja.head.previous = iRiNyje
	}
	vetvetja.head = iRiNyje
	vetvetja.Madhësia_2++

	if vetvetja.head.pasuesen == nil {
		vetvetja.tail = vetvetja.head
	}

}
func (vetvetja *LinkedListë) Append_to_list(kursori uintptr) {
	if vetvetja.Madhësia_2 == 0 {
		vetvetja.Prepend_to_list(kursori)
	} else {
		iRiNyje := (*Nyje)(vetvetja.mem.Malloc(uint32(Sizeof(Nyje{}))))
		if iRiNyje == nil {
			return
		}
		iRiNyje.kursori = kursori
		iRiNyje.previous = vetvetja.tail
		iRiNyje.pasuesen = nil
		vetvetja.tail.pasuesen = iRiNyje
		vetvetja.tail = iRiNyje
		vetvetja.Madhësia_2++
	}
}
func (vetvetja *LinkedListë) Insert_at_index(treguesi int, kursori uintptr) {
	if treguesi == 0 {
		vetvetja.Prepend_to_list(kursori)
	} else {
		previousNyje := vetvetja.GetNyjeat(treguesi - 1)
		pasuesenNyje := previousNyje.pasuesen
		iRiNyje := (*Nyje)(vetvetja.mem.Malloc(uint32(Sizeof(Nyje{}))))
		if iRiNyje == nil {
			return
		}
		iRiNyje.kursori = kursori

		previousNyje.pasuesen = iRiNyje
		iRiNyje.previous = previousNyje
		iRiNyje.pasuesen = pasuesenNyje
		if pasuesenNyje != nil {
			pasuesenNyje.previous = iRiNyje
		}

		vetvetja.Madhësia_2++

		if iRiNyje.pasuesen == nil {
			vetvetja.tail = iRiNyje
		}
	}
}
func (vetvetja *LinkedListë) GetNyjeat(treguesi int) *Nyje {
	if treguesi < 0 || treguesi >= vetvetja.Madhësia_2 {
		return nil
	}
	var x *Nyje = vetvetja.head
	for i := 0; i < treguesi; i++ {
		x = x.pasuesen
	}
	return x
}

func (vetvetja *LinkedListë) CaktoniNyjeat(treguesi int, kursori uintptr) {
	var x *Nyje = vetvetja.head
	for i := 0; i < treguesi; i++ {
		x = x.pasuesen
	}
	if x != nil {
		x.kursori = kursori
	}
}
func (vetvetja *LinkedListë) Getat(treguesi int) Pointer {
	nyje := vetvetja.GetNyjeat(treguesi)
	if nyje == nil {
		return nil
	}
	var kursori uintptr = nyje.kursori
	return Pointer(kursori)
}
func (vetvetja *LinkedListë) Treguesinga(kursori uintptr) int {
	var n *Nyje = vetvetja.head
	i := 0
	for ; i < vetvetja.Madhësia_2; i++ {
		if kursori == n.kursori {
			return i
		}
		n = n.pasuesen
	}
	return -1
}
func (vetvetja *LinkedListë) Hiqe(kursori uintptr) {
	treguesi := vetvetja.Treguesinga(kursori)
	if treguesi < 0 {
		return
	}
	vetvetja.Hiqeat(treguesi)
}
func (vetvetja *LinkedListë) Hiqeat(treguesi int) {
	if treguesi < 0 || treguesi >= vetvetja.Madhësia_2 {
		return
	}
	nyje := vetvetja.GetNyjeat(treguesi)
	if nyje == nil {
		return
	}
	if nyje.previous != nil {
		nyje.previous.pasuesen = nyje.pasuesen
	} else {
		vetvetja.head = nyje.pasuesen
	}
	if nyje.pasuesen != nil {
		nyje.pasuesen.previous = nyje.previous
	} else {
		vetvetja.tail = nyje.previous
	}
	vetvetja.Madhësia_2 = vetvetja.Madhësia_2 - 1

	if vetvetja.mem != nil {
		vetvetja.mem.Elirë(Pointer(nyje))
	}
}

var konsolë_2 = TKonsolë{}

func (vetvetja *LinkedListë) Printo() {
	konsolë_2.MPrintoxy("LinkedList:", 1, 1)
	konsolë_2.MUnsignedinteger32Printo(uint32(uintptr(Pointer(vetvetja))))
	for i := 0; i < vetvetja.Madhësia_2; i++ {
		nyje := (*Nyje)(vetvetja.Getat(i))
		konsolë_2.MUnsignedinteger32Printo(uint32(nyje.kursori))
		konsolë_2.MPrinto(":")
	}
}
