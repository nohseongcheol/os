/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package matriz

import . "unsafe"
import . "console"

var nómatriz [100]uintptr

type TMatriz struct {
	Tamanho_2 int
}

func (próprio *TMatriz) Adicionar(referência_de_memória uintptr) {
	nómatriz[próprio.Tamanho_2] = referência_de_memória
	próprio.Tamanho_2++
}
func (próprio *TMatriz) Getat(índice int) Pointer {
	return Pointer(nómatriz[índice])
}
func (próprio *TMatriz) Índicede(referência_de_memória uintptr) int {
	i := 0
	for ; i < próprio.Tamanho_2; i++ {
		if referência_de_memória == nómatriz[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (próprio *TMatriz) Imprimir() {
	console_2.MImprimirxy("array:", 1, 1)

	for i := 0; i < próprio.Tamanho_2; i++ {
		console_2.MUnsignedinteger32Imprimir(uint32(nómatriz[i]))
		console_2.MImprimir(":")
	}
}
