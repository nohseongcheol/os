/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package serie

import . "unsafe"
import . "console"

var nodoSerie [100]uintptr

type TSerie struct {
	Dimensione_2 int
}

func (séstesso *TSerie) Aggiungi(riferimento_di_memoria uintptr) {
	nodoSerie[séstesso.Dimensione_2] = riferimento_di_memoria
	séstesso.Dimensione_2++
}
func (séstesso *TSerie) Getat(indice int) Pointer {
	return Pointer(nodoSerie[indice])
}
func (séstesso *TSerie) Indicedi(riferimento_di_memoria uintptr) int {
	i := 0
	for ; i < séstesso.Dimensione_2; i++ {
		if riferimento_di_memoria == nodoSerie[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (séstesso *TSerie) Stampa() {
	console_2.MStampaxy("array:", 1, 1)

	for i := 0; i < séstesso.Dimensione_2; i++ {
		console_2.MUnsignedinteger32Stampa(uint32(nodoSerie[i]))
		console_2.MStampa(":")
	}
}
