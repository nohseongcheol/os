package matriu

import . "unsafe"
import . "consola"

var nodeMatriu [100]uintptr

type TMatriu struct {
	Mida_2 int
}

func (unmateix *TMatriu) Afegeix(punter uintptr) {
	nodeMatriu[unmateix.Mida_2] = punter
	unmateix.Mida_2++
}
func (unmateix *TMatriu) Getat(índex int) Pointer {
	return Pointer(nodeMatriu[índex])
}
func (unmateix *TMatriu) Índexde(punter uintptr) int {
	i := 0
	for ; i < unmateix.Mida_2; i++ {
		if punter == nodeMatriu[i] {
			return i
		}
	}
	return -1
}

var consola_2 = TConsola{}

func (unmateix *TMatriu) Imprimeix() {
	consola_2.MImprimeixxy("array:", 1, 1)

	for i := 0; i < unmateix.Mida_2; i++ {
		consola_2.MUnsignedinteger32Imprimeix(uint32(nodeMatriu[i]))
		consola_2.MImprimeix(":")
	}
}
