package memorymananger

import . "unsafe"

const MáxcolaTamaño uint32 = 0x1FFFFFF
const ColaIniciarDirección uint32 = 0x1000000

type TMemoriachunk struct {
	siguiente	*TMemoriachunk
	previous	*TMemoriachunk
	allocated	bool

	tamaño	uint32
}

type TMemoriagestor struct {
}

var first *TMemoriachunk
var Activomemoriagestor *TMemoriagestor = nil
var memoriachunkTamaño uint32

func (propio *TMemoriagestor) Init(iniciar uint32, tamaño uint32) {

	Activomemoriagestor = propio

	memoriachunkTamaño = uint32(Sizeof(TMemoriachunk{}))

	if tamaño < memoriachunkTamaño {
		first = nil
	} else {
		first = (*TMemoriachunk)(Pointer(uintptr(ColaIniciarDirección) + uintptr(iniciar)))
		first.allocated = false
		first.previous = nil
		first.siguiente = nil
		first.tamaño = tamaño - memoriachunkTamaño
	}
}
func (propio *TMemoriagestor) Destruir() {
	if Activomemoriagestor == propio {
		Activomemoriagestor = nil
	}
}
func (propio *TMemoriagestor) Asignar_memoria(tamaño uint32) Pointer {
	var rESULTADO *TMemoriachunk = nil

	var chunk *TMemoriachunk = first
	for ; chunk != nil && rESULTADO == nil; chunk = chunk.siguiente {
		if chunk.tamaño > tamaño && !chunk.allocated {
			rESULTADO = chunk
		}
	}

	if rESULTADO == nil {
		return nil
	}

	if rESULTADO.tamaño >= (tamaño + memoriachunkTamaño + 1) {

		var temporary *TMemoriachunk
		temporary = (*TMemoriachunk)(Pointer(uintptr(uint32(uintptr(Pointer(rESULTADO))) + memoriachunkTamaño + tamaño)))

		temporary.allocated = false
		temporary.tamaño = rESULTADO.tamaño - tamaño - memoriachunkTamaño
		temporary.previous = rESULTADO
		temporary.siguiente = rESULTADO.siguiente

		if temporary.siguiente != nil {
			temporary.siguiente.previous = temporary
		}

		rESULTADO.tamaño = tamaño
		rESULTADO.siguiente = temporary
	}
	rESULTADO.allocated = true

	return Pointer(uintptr(Pointer(rESULTADO)) + uintptr(memoriachunkTamaño))
}
func (propio *TMemoriagestor) Alignedmalloc(tamaño uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if tamaño == 0 || tamaño > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rESULTADO *TMemoriachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.siguiente {
		if chunk.allocated {
			continue
		}
		dirección := uint32(uintptr(Pointer(chunk)) + uintptr(memoriachunkTamaño))
		diff = (0x1000 - (dirección & 0xFFF)) & 0xFFF
		if dirección+diff < dirección {
			continue
		}
		if diff <= chunk.tamaño && tamaño <= chunk.tamaño-diff {
			rESULTADO = chunk
			break
		}
	}
	if rESULTADO == nil {
		return nil, 0
	}
	tamaño += diff
	if rESULTADO.tamaño-tamaño >= memoriachunkTamaño+1 {
		temporary := (*TMemoriachunk)(Pointer(uintptr(Pointer(rESULTADO)) + uintptr(memoriachunkTamaño) + uintptr(tamaño)))
		temporary.allocated = false
		temporary.tamaño = rESULTADO.tamaño - tamaño - memoriachunkTamaño
		temporary.previous = rESULTADO
		temporary.siguiente = rESULTADO.siguiente
		if temporary.siguiente != nil {
			temporary.siguiente.previous = temporary
		}
		rESULTADO.tamaño = tamaño
		rESULTADO.siguiente = temporary
	}
	rESULTADO.allocated = true
	return Pointer(uintptr(Pointer(rESULTADO)) + uintptr(memoriachunkTamaño) + uintptr(diff)), diff
}
func (propio *TMemoriagestor) Libre(referencia_de_memoria_2 Pointer) {
	var chunk *TMemoriachunk = (*TMemoriachunk)(Pointer(uintptr(referencia_de_memoria_2) - uintptr(memoriachunkTamaño)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.siguiente = chunk.siguiente
		chunk.previous.tamaño += chunk.tamaño + memoriachunkTamaño
		if chunk.siguiente != nil {
			chunk.siguiente.previous = chunk.previous
		}
	}

	if chunk.siguiente != nil && !chunk.siguiente.allocated {
		chunk.tamaño += chunk.siguiente.tamaño + memoriachunkTamaño
		chunk.siguiente = chunk.siguiente.siguiente
		if chunk.siguiente != nil {
			chunk.siguiente.previous = chunk
		}
	}
}
func Nuevo(tamaño int) Pointer {
	if Activomemoriagestor == nil {
		return nil
	}
	return Activomemoriagestor.Asignar_memoria(uint32(tamaño))
}
func Eliminar(referencia_de_memoria_2 Pointer) {
	if Activomemoriagestor != nil {
		Activomemoriagestor.Libre(referencia_de_memoria_2)
	}
}
