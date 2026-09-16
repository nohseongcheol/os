/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package lista

import . "unsafe"
import . "konsola"
import mem "pamięćmanager"

type TWęzeł_listy struct {
	odwołanie_do_adresu		uintptr
	previous	*TWęzeł_listy
	następny	*TWęzeł_listy
}

type LinkedLista struct {
	head		*TWęzeł_listy
	tail		*TWęzeł_listy
	Rozmiar_2	int

	mem	*mem.TPamięćmanager
}

func (bieżący *LinkedLista) Init(mem *mem.TPamięćmanager) {
	bieżący.head = nil
	bieżący.tail = nil
	bieżący.Rozmiar_2 = 0

	bieżący.mem = mem
}
func (bieżący *LinkedLista) Dodaj_na_początku_listy(odwołanie_do_adresu uintptr) {
	nowyWęzeł := (*TWęzeł_listy)(bieżący.mem.Przydziel_pamięć(uint32(Sizeof(TWęzeł_listy{}))))
	if nowyWęzeł == nil {
		return
	}
	nowyWęzeł.odwołanie_do_adresu = odwołanie_do_adresu
	nowyWęzeł.previous = nil
	nowyWęzeł.następny = bieżący.head
	if bieżący.head != nil {
		bieżący.head.previous = nowyWęzeł
	}
	bieżący.head = nowyWęzeł
	bieżący.Rozmiar_2++

	if bieżący.head.następny == nil {
		bieżący.tail = bieżący.head
	}

}
func (bieżący *LinkedLista) Dodaj_na_końcu_listy(odwołanie_do_adresu uintptr) {
	if bieżący.Rozmiar_2 == 0 {
		bieżący.Dodaj_na_początku_listy(odwołanie_do_adresu)
	} else {
		nowyWęzeł := (*TWęzeł_listy)(bieżący.mem.Przydziel_pamięć(uint32(Sizeof(TWęzeł_listy{}))))
		if nowyWęzeł == nil {
			return
		}
		nowyWęzeł.odwołanie_do_adresu = odwołanie_do_adresu
		nowyWęzeł.previous = bieżący.tail
		nowyWęzeł.następny = nil
		bieżący.tail.następny = nowyWęzeł
		bieżący.tail = nowyWęzeł
		bieżący.Rozmiar_2++
	}
}
func (bieżący *LinkedLista) Wstaw_pod_indeksem(indeks int, odwołanie_do_adresu uintptr) {
	if indeks == 0 {
		bieżący.Dodaj_na_początku_listy(odwołanie_do_adresu)
	} else {
		previousWęzeł := bieżący.GetWęzełat(indeks - 1)
		następnyWęzeł := previousWęzeł.następny
		nowyWęzeł := (*TWęzeł_listy)(bieżący.mem.Przydziel_pamięć(uint32(Sizeof(TWęzeł_listy{}))))
		if nowyWęzeł == nil {
			return
		}
		nowyWęzeł.odwołanie_do_adresu = odwołanie_do_adresu

		previousWęzeł.następny = nowyWęzeł
		nowyWęzeł.previous = previousWęzeł
		nowyWęzeł.następny = następnyWęzeł
		if następnyWęzeł != nil {
			następnyWęzeł.previous = nowyWęzeł
		}

		bieżący.Rozmiar_2++

		if nowyWęzeł.następny == nil {
			bieżący.tail = nowyWęzeł
		}
	}
}
func (bieżący *LinkedLista) GetWęzełat(indeks int) *TWęzeł_listy {
	if indeks < 0 || indeks >= bieżący.Rozmiar_2 {
		return nil
	}
	var x *TWęzeł_listy = bieżący.head
	for i := 0; i < indeks; i++ {
		x = x.następny
	}
	return x
}

func (bieżący *LinkedLista) ZbiórWęzełat(indeks int, odwołanie_do_adresu uintptr) {
	var x *TWęzeł_listy = bieżący.head
	for i := 0; i < indeks; i++ {
		x = x.następny
	}
	if x != nil {
		x.odwołanie_do_adresu = odwołanie_do_adresu
	}
}
func (bieżący *LinkedLista) Getat(indeks int) Pointer {
	węzeł_listy := bieżący.GetWęzełat(indeks)
	if węzeł_listy == nil {
		return nil
	}
	var odwołanie_do_adresu uintptr = węzeł_listy.odwołanie_do_adresu
	return Pointer(odwołanie_do_adresu)
}
func (bieżący *LinkedLista) Indeksz(odwołanie_do_adresu uintptr) int {
	var n *TWęzeł_listy = bieżący.head
	i := 0
	for ; i < bieżący.Rozmiar_2; i++ {
		if odwołanie_do_adresu == n.odwołanie_do_adresu {
			return i
		}
		n = n.następny
	}
	return -1
}
func (bieżący *LinkedLista) Usuń_2(odwołanie_do_adresu uintptr) {
	indeks := bieżący.Indeksz(odwołanie_do_adresu)
	if indeks < 0 {
		return
	}
	bieżący.Usuńat(indeks)
}
func (bieżący *LinkedLista) Usuńat(indeks int) {
	if indeks < 0 || indeks >= bieżący.Rozmiar_2 {
		return
	}
	węzeł_listy := bieżący.GetWęzełat(indeks)
	if węzeł_listy == nil {
		return
	}
	if węzeł_listy.previous != nil {
		węzeł_listy.previous.następny = węzeł_listy.następny
	} else {
		bieżący.head = węzeł_listy.następny
	}
	if węzeł_listy.następny != nil {
		węzeł_listy.następny.previous = węzeł_listy.previous
	} else {
		bieżący.tail = węzeł_listy.previous
	}
	bieżący.Rozmiar_2 = bieżący.Rozmiar_2 - 1

	if bieżący.mem != nil {
		bieżący.mem.Wolne(Pointer(węzeł_listy))
	}
}

var konsola_2 = TKonsola{}

func (bieżący *LinkedLista) Wydrukuj() {
	konsola_2.MWydrukujxy("LinkedList:", 1, 1)
	konsola_2.MUnsignedinteger32Wydrukuj(uint32(uintptr(Pointer(bieżący))))
	for i := 0; i < bieżący.Rozmiar_2; i++ {
		węzeł_listy := (*TWęzeł_listy)(bieżący.Getat(i))
		konsola_2.MUnsignedinteger32Wydrukuj(uint32(węzeł_listy.odwołanie_do_adresu))
		konsola_2.MWydrukuj(":")
	}
}
