/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxfilaTamanho uint32 = 0x1FFFFFF
const FilaIniciarEndereço uint32 = 0x1000000

type TMemóriachunk struct {
	seguinte	*TMemóriachunk
	previous	*TMemóriachunk
	allocated	bool

	tamanho	uint32
}

type TMemóriagestor struct {
}

var first *TMemóriachunk
var Ativomemóriagestor *TMemóriagestor = nil
var memóriachunkTamanho uint32

func (próprio *TMemóriagestor) Init(iniciar uint32, tamanho uint32) {

	Ativomemóriagestor = próprio

	memóriachunkTamanho = uint32(Sizeof(TMemóriachunk{}))

	if tamanho < memóriachunkTamanho {
		first = nil
	} else {
		first = (*TMemóriachunk)(Pointer(uintptr(FilaIniciarEndereço) + uintptr(iniciar)))
		first.allocated = false
		first.previous = nil
		first.seguinte = nil
		first.tamanho = tamanho - memóriachunkTamanho
	}
}
func (próprio *TMemóriagestor) Destruir() {
	if Ativomemóriagestor == próprio {
		Ativomemóriagestor = nil
	}
}
func (próprio *TMemóriagestor) Alocar_memória(tamanho uint32) Pointer {
	var destino_3 *TMemóriachunk = nil

	var chunk *TMemóriachunk = first
	for ; chunk != nil && destino_3 == nil; chunk = chunk.seguinte {
		if chunk.tamanho > tamanho && !chunk.allocated {
			destino_3 = chunk
		}
	}

	if destino_3 == nil {
		return nil
	}

	if destino_3.tamanho >= (tamanho + memóriachunkTamanho + 1) {

		var temporary *TMemóriachunk
		temporary = (*TMemóriachunk)(Pointer(uintptr(uint32(uintptr(Pointer(destino_3))) + memóriachunkTamanho + tamanho)))

		temporary.allocated = false
		temporary.tamanho = destino_3.tamanho - tamanho - memóriachunkTamanho
		temporary.previous = destino_3
		temporary.seguinte = destino_3.seguinte

		if temporary.seguinte != nil {
			temporary.seguinte.previous = temporary
		}

		destino_3.tamanho = tamanho
		destino_3.seguinte = temporary
	}
	destino_3.allocated = true

	return Pointer(uintptr(Pointer(destino_3)) + uintptr(memóriachunkTamanho))
}
func (próprio *TMemóriagestor) Alignedmalloc(tamanho uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if tamanho == 0 || tamanho > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var destino_3 *TMemóriachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.seguinte {
		if chunk.allocated {
			continue
		}
		endereço := uint32(uintptr(Pointer(chunk)) + uintptr(memóriachunkTamanho))
		diff = (0x1000 - (endereço & 0xFFF)) & 0xFFF
		if endereço+diff < endereço {
			continue
		}
		if diff <= chunk.tamanho && tamanho <= chunk.tamanho-diff {
			destino_3 = chunk
			break
		}
	}
	if destino_3 == nil {
		return nil, 0
	}
	tamanho += diff
	if destino_3.tamanho-tamanho >= memóriachunkTamanho+1 {
		temporary := (*TMemóriachunk)(Pointer(uintptr(Pointer(destino_3)) + uintptr(memóriachunkTamanho) + uintptr(tamanho)))
		temporary.allocated = false
		temporary.tamanho = destino_3.tamanho - tamanho - memóriachunkTamanho
		temporary.previous = destino_3
		temporary.seguinte = destino_3.seguinte
		if temporary.seguinte != nil {
			temporary.seguinte.previous = temporary
		}
		destino_3.tamanho = tamanho
		destino_3.seguinte = temporary
	}
	destino_3.allocated = true
	return Pointer(uintptr(Pointer(destino_3)) + uintptr(memóriachunkTamanho) + uintptr(diff)), diff
}
func (próprio *TMemóriagestor) Livre(referência_de_memória_2 Pointer) {
	var chunk *TMemóriachunk = (*TMemóriachunk)(Pointer(uintptr(referência_de_memória_2) - uintptr(memóriachunkTamanho)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.seguinte = chunk.seguinte
		chunk.previous.tamanho += chunk.tamanho + memóriachunkTamanho
		if chunk.seguinte != nil {
			chunk.seguinte.previous = chunk.previous
		}
	}

	if chunk.seguinte != nil && !chunk.seguinte.allocated {
		chunk.tamanho += chunk.seguinte.tamanho + memóriachunkTamanho
		chunk.seguinte = chunk.seguinte.seguinte
		if chunk.seguinte != nil {
			chunk.seguinte.previous = chunk
		}
	}
}
func Novo(tamanho int) Pointer {
	if Ativomemóriagestor == nil {
		return nil
	}
	return Ativomemóriagestor.Alocar_memória(uint32(tamanho))
}
func Eliminar(referência_de_memória_2 Pointer) {
	if Ativomemóriagestor != nil {
		Ativomemóriagestor.Livre(referência_de_memória_2)
	}
}
