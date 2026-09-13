package pole

import . "unsafe"
import . "konzola"

var uzolPole [100]uintptr

type TPole struct {
	Veľkosť_2 int
}

func (vlastný *TPole) Pridať(kurzor uintptr) {
	uzolPole[vlastný.Veľkosť_2] = kurzor
	vlastný.Veľkosť_2++
}
func (vlastný *TPole) Getat(index int) Pointer {
	return Pointer(uzolPole[index])
}
func (vlastný *TPole) Indexz(kurzor uintptr) int {
	i := 0
	for ; i < vlastný.Veľkosť_2; i++ {
		if kurzor == uzolPole[i] {
			return i
		}
	}
	return -1
}

var konzola_2 = TKonzola{}

func (vlastný *TPole) Tlačiť() {
	konzola_2.MTlačiťxy("array:", 1, 1)

	for i := 0; i < vlastný.Veľkosť_2; i++ {
		konzola_2.MUnsignedinteger32Tlačiť(uint32(uzolPole[i]))
		konzola_2.MTlačiť(":")
	}
}
