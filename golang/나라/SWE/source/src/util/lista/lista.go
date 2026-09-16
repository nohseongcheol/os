/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package lista

import . "unsafe"
import . "konsol"
import mem "minnemanager"

type TListnod struct {
	adressreferens	uintptr
	previous	*TListnod
	nästa		*TListnod
}

type LinkedLista struct {
	head		*TListnod
	tail		*TListnod
	Storlek_2	int

	mem	*mem.TMinnemanager
}

func (själv *LinkedLista) Init(mem *mem.TMinnemanager) {
	själv.head = nil
	själv.tail = nil
	själv.Storlek_2 = 0

	själv.mem = mem
}
func (själv *LinkedLista) Lägg_till_först_i_listan(adressreferens uintptr) {
	nyNod := (*TListnod)(själv.mem.Tilldela_minne(uint32(Sizeof(TListnod{}))))
	if nyNod == nil {
		return
	}
	nyNod.adressreferens = adressreferens
	nyNod.previous = nil
	nyNod.nästa = själv.head
	if själv.head != nil {
		själv.head.previous = nyNod
	}
	själv.head = nyNod
	själv.Storlek_2++

	if själv.head.nästa == nil {
		själv.tail = själv.head
	}

}
func (själv *LinkedLista) Lägg_till_sist_i_listan(adressreferens uintptr) {
	if själv.Storlek_2 == 0 {
		själv.Lägg_till_först_i_listan(adressreferens)
	} else {
		nyNod := (*TListnod)(själv.mem.Tilldela_minne(uint32(Sizeof(TListnod{}))))
		if nyNod == nil {
			return
		}
		nyNod.adressreferens = adressreferens
		nyNod.previous = själv.tail
		nyNod.nästa = nil
		själv.tail.nästa = nyNod
		själv.tail = nyNod
		själv.Storlek_2++
	}
}
func (själv *LinkedLista) Infoga_vid_index(index int, adressreferens uintptr) {
	if index == 0 {
		själv.Lägg_till_först_i_listan(adressreferens)
	} else {
		previousNod := själv.GetNodat(index - 1)
		nästaNod := previousNod.nästa
		nyNod := (*TListnod)(själv.mem.Tilldela_minne(uint32(Sizeof(TListnod{}))))
		if nyNod == nil {
			return
		}
		nyNod.adressreferens = adressreferens

		previousNod.nästa = nyNod
		nyNod.previous = previousNod
		nyNod.nästa = nästaNod
		if nästaNod != nil {
			nästaNod.previous = nyNod
		}

		själv.Storlek_2++

		if nyNod.nästa == nil {
			själv.tail = nyNod
		}
	}
}
func (själv *LinkedLista) GetNodat(index int) *TListnod {
	if index < 0 || index >= själv.Storlek_2 {
		return nil
	}
	var x *TListnod = själv.head
	for i := 0; i < index; i++ {
		x = x.nästa
	}
	return x
}

func (själv *LinkedLista) MängdNodat(index int, adressreferens uintptr) {
	var x *TListnod = själv.head
	for i := 0; i < index; i++ {
		x = x.nästa
	}
	if x != nil {
		x.adressreferens = adressreferens
	}
}
func (själv *LinkedLista) Getat(index int) Pointer {
	listnod := själv.GetNodat(index)
	if listnod == nil {
		return nil
	}
	var adressreferens uintptr = listnod.adressreferens
	return Pointer(adressreferens)
}
func (själv *LinkedLista) Indexav(adressreferens uintptr) int {
	var n *TListnod = själv.head
	i := 0
	for ; i < själv.Storlek_2; i++ {
		if adressreferens == n.adressreferens {
			return i
		}
		n = n.nästa
	}
	return -1
}
func (själv *LinkedLista) Tabort_2(adressreferens uintptr) {
	index := själv.Indexav(adressreferens)
	if index < 0 {
		return
	}
	själv.Tabortat(index)
}
func (själv *LinkedLista) Tabortat(index int) {
	if index < 0 || index >= själv.Storlek_2 {
		return
	}
	listnod := själv.GetNodat(index)
	if listnod == nil {
		return
	}
	if listnod.previous != nil {
		listnod.previous.nästa = listnod.nästa
	} else {
		själv.head = listnod.nästa
	}
	if listnod.nästa != nil {
		listnod.nästa.previous = listnod.previous
	} else {
		själv.tail = listnod.previous
	}
	själv.Storlek_2 = själv.Storlek_2 - 1

	if själv.mem != nil {
		själv.mem.Ledigt(Pointer(listnod))
	}
}

var konsol_2 = TKonsol{}

func (själv *LinkedLista) Skrivut() {
	konsol_2.MSkrivutxy("LinkedList:", 1, 1)
	konsol_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(själv))))
	for i := 0; i < själv.Storlek_2; i++ {
		listnod := (*TListnod)(själv.Getat(i))
		konsol_2.MUnsignedinteger32Skrivut(uint32(listnod.adressreferens))
		konsol_2.MSkrivut(":")
	}
}
