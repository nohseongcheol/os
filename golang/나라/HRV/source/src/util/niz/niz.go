/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package niz

import . "unsafe"
import . "console"

var čvorNiz [100]uintptr

type TNiz struct {
	Veličina_2 int
}

func (sam *TNiz) Dodaj(pokazivač uintptr) {
	čvorNiz[sam.Veličina_2] = pokazivač
	sam.Veličina_2++
}
func (sam *TNiz) Getat(kazalo int) Pointer {
	return Pointer(čvorNiz[kazalo])
}
func (sam *TNiz) Kazalood(pokazivač uintptr) int {
	i := 0
	for ; i < sam.Veličina_2; i++ {
		if pokazivač == čvorNiz[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (sam *TNiz) Ispis() {
	console_2.MIspisxy("array:", 1, 1)

	for i := 0; i < sam.Veličina_2; i++ {
		console_2.MUnsignedinteger32Ispis(uint32(čvorNiz[i]))
		console_2.MIspis(":")
	}
}
