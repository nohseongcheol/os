/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tabel

import . "unsafe"
import . "console"

var knudepunktTabel [100]uintptr

type TTabel struct {
	Størrelse_2 int
}

func (selv *TTabel) Tilføj(markør uintptr) {
	knudepunktTabel[selv.Størrelse_2] = markør
	selv.Størrelse_2++
}
func (selv *TTabel) Getat(indeks int) Pointer {
	return Pointer(knudepunktTabel[indeks])
}
func (selv *TTabel) Indeksaf(markør uintptr) int {
	i := 0
	for ; i < selv.Størrelse_2; i++ {
		if markør == knudepunktTabel[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (selv *TTabel) Udskriv() {
	console_2.MUdskrivxy("array:", 1, 1)

	for i := 0; i < selv.Størrelse_2; i++ {
		console_2.MUnsignedinteger32Udskriv(uint32(knudepunktTabel[i]))
		console_2.MUdskriv(":")
	}
}
