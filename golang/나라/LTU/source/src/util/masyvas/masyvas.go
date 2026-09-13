package masyvas

import . "unsafe"
import . "console"

var mazgasMasyvas [100]uintptr

type TMasyvas struct {
	Dydis_2 int
}

func (self *TMasyvas) Pridėti(rodyklė_2 uintptr) {
	mazgasMasyvas[self.Dydis_2] = rodyklė_2
	self.Dydis_2++
}
func (self *TMasyvas) Getat(rodyklė int) Pointer {
	return Pointer(mazgasMasyvas[rodyklė])
}
func (self *TMasyvas) Rodyklėiš(rodyklė_2 uintptr) int {
	i := 0
	for ; i < self.Dydis_2; i++ {
		if rodyklė_2 == mazgasMasyvas[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TMasyvas) Spausdinti() {
	console_2.MSpausdintixy("array:", 1, 1)

	for i := 0; i < self.Dydis_2; i++ {
		console_2.MUnsignedinteger32Spausdinti(uint32(mazgasMasyvas[i]))
		console_2.MSpausdinti(":")
	}
}
