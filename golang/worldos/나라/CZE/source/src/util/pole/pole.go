/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pole

import . "unsafe"
import . "konzole"

var uzelPole [100]uintptr

type TPole struct {
	Velikost_2 int
}

func (self *TPole) Přidat(odkaz_na_adresu uintptr) {
	uzelPole[self.Velikost_2] = odkaz_na_adresu
	self.Velikost_2++
}
func (self *TPole) Getat(rejstřík int) Pointer {
	return Pointer(uzelPole[rejstřík])
}
func (self *TPole) Rejstříkz(odkaz_na_adresu uintptr) int {
	i := 0
	for ; i < self.Velikost_2; i++ {
		if odkaz_na_adresu == uzelPole[i] {
			return i
		}
	}
	return -1
}

var konzole_2 = TKonzole{}

func (self *TPole) Tisknout() {
	konzole_2.MTisknoutxy("array:", 1, 1)

	for i := 0; i < self.Velikost_2; i++ {
		konzole_2.MUnsignedinteger32Tisknout(uint32(uzelPole[i]))
		konzole_2.MTisknout(":")
	}
}
