/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package polje

import . "unsafe"
import . "console"

var nodePolje [100]uintptr

type TPolje struct {
	Velikost_2 int
}

func (sam *TPolje) Dodaj(kazalnik uintptr) {
	nodePolje[sam.Velikost_2] = kazalnik
	sam.Velikost_2++
}
func (sam *TPolje) Getat(kazalo int) Pointer {
	return Pointer(nodePolje[kazalo])
}
func (sam *TPolje) Kazalood(kazalnik uintptr) int {
	i := 0
	for ; i < sam.Velikost_2; i++ {
		if kazalnik == nodePolje[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (sam *TPolje) Natisni() {
	console_2.MNatisnixy("array:", 1, 1)

	for i := 0; i < sam.Velikost_2; i++ {
		console_2.MUnsignedinteger32Natisni(uint32(nodePolje[i]))
		console_2.MNatisni(":")
	}
}
