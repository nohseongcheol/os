/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tömb

import . "unsafe"
import . "konzol"

var csomópontTömb [100]uintptr

type TTömb struct {
	Méret_2 int
}

func (self *TTömb) Hozzáadás(mutató uintptr) {
	csomópontTömb[self.Méret_2] = mutató
	self.Méret_2++
}
func (self *TTömb) Getat(index int) Pointer {
	return Pointer(csomópontTömb[index])
}
func (self *TTömb) Indexof(mutató uintptr) int {
	i := 0
	for ; i < self.Méret_2; i++ {
		if mutató == csomópontTömb[i] {
			return i
		}
	}
	return -1
}

var konzol_2 = TKonzol{}

func (self *TTömb) Nyomtatás() {
	konzol_2.MNyomtatásxy("array:", 1, 1)

	for i := 0; i < self.Méret_2; i++ {
		konzol_2.MUnsignedinteger32Nyomtatás(uint32(csomópontTömb[i]))
		konzol_2.MNyomtatás(":")
	}
}
