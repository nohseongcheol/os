/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package niz

import . "unsafe"
import . "konzola"

var čvorNiz [100]uintptr

type TNiz struct {
	Veličina_2 int
}

func (isti *TNiz) Dodaj(pokazivač uintptr) {
	čvorNiz[isti.Veličina_2] = pokazivač
	isti.Veličina_2++
}
func (isti *TNiz) Getat(popis int) Pointer {
	return Pointer(čvorNiz[popis])
}
func (isti *TNiz) Popisod(pokazivač uintptr) int {
	i := 0
	for ; i < isti.Veličina_2; i++ {
		if pokazivač == čvorNiz[i] {
			return i
		}
	}
	return -1
}

var konzola_2 = TKonzola{}

func (isti *TNiz) Štampaj() {
	konzola_2.MŠtampajxy("array:", 1, 1)

	for i := 0; i < isti.Veličina_2; i++ {
		konzola_2.MUnsignedinteger32Štampaj(uint32(čvorNiz[i]))
		konzola_2.MŠtampaj(":")
	}
}
