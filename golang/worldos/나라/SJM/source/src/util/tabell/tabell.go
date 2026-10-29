/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tabell

import . "unsafe"
import . "console"

var nodeTabell [100]uintptr

type TTabell struct {
	Størrelse_2 int
}

func (selv *TTabell) Leggtil(peker uintptr) {
	nodeTabell[selv.Størrelse_2] = peker
	selv.Størrelse_2++
}
func (selv *TTabell) Getat(indeks int) Pointer {
	return Pointer(nodeTabell[indeks])
}
func (selv *TTabell) Indeksav(peker uintptr) int {
	i := 0
	for ; i < selv.Størrelse_2; i++ {
		if peker == nodeTabell[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (selv *TTabell) Skrivut() {
	console_2.MSkrivutxy("array:", 1, 1)

	for i := 0; i < selv.Størrelse_2; i++ {
		console_2.MUnsignedinteger32Skrivut(uint32(nodeTabell[i]))
		console_2.MSkrivut(":")
	}
}
