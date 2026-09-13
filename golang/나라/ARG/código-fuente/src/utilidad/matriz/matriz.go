package matriz

import . "unsafe"
import . "consola"

var nodomatriz [100]uintptr

type TMatriz struct {
	Tamaño_2 int
}

func (propio *TMatriz) Añadir(referencia_de_memoria uintptr) {
	nodomatriz[propio.Tamaño_2] = referencia_de_memoria
	propio.Tamaño_2++
}
func (propio *TMatriz) Getat(índice int) Pointer {
	return Pointer(nodomatriz[índice])
}
func (propio *TMatriz) Índicede(referencia_de_memoria uintptr) int {
	i := 0
	for ; i < propio.Tamaño_2; i++ {
		if referencia_de_memoria == nodomatriz[i] {
			return i
		}
	}
	return -1
}

var consola_2 = TConsola{}

func (propio *TMatriz) Imprimir() {
	consola_2.MImprimirxy("array:", 1, 1)

	for i := 0; i < propio.Tamaño_2; i++ {
		consola_2.MUnsignedinteger32Imprimir(uint32(nodomatriz[i]))
		consola_2.MImprimir(":")
	}
}
