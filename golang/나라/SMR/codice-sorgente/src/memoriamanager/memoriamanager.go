package memorymananger

import . "unsafe"

const MassimaqueueDimensione uint32 = 0x1FFFFFF
const QueueAvviaaddress uint32 = 0x1000000

type TMemoriachunk struct {
	successivo	*TMemoriachunk
	previous	*TMemoriachunk
	allocated	bool

	dimensione	uint32
}

type TMemoriamanager struct {
}

var first *TMemoriachunk
var AttivoMemoriamanager *TMemoriamanager = nil
var memoriachunkDimensione uint32

func (séstesso *TMemoriamanager) Init(avvia uint32, dimensione uint32) {

	AttivoMemoriamanager = séstesso

	memoriachunkDimensione = uint32(Sizeof(TMemoriachunk{}))

	if dimensione < memoriachunkDimensione {
		first = nil
	} else {
		first = (*TMemoriachunk)(Pointer(uintptr(QueueAvviaaddress) + uintptr(avvia)))
		first.allocated = false
		first.previous = nil
		first.successivo = nil
		first.dimensione = dimensione - memoriachunkDimensione
	}
}
func (séstesso *TMemoriamanager) Distruggi() {
	if AttivoMemoriamanager == séstesso {
		AttivoMemoriamanager = nil
	}
}
func (séstesso *TMemoriamanager) Alloca_memoria(dimensione uint32) Pointer {
	var rISULTATO *TMemoriachunk = nil

	var chunk *TMemoriachunk = first
	for ; chunk != nil && rISULTATO == nil; chunk = chunk.successivo {
		if chunk.dimensione > dimensione && !chunk.allocated {
			rISULTATO = chunk
		}
	}

	if rISULTATO == nil {
		return nil
	}

	if rISULTATO.dimensione >= (dimensione + memoriachunkDimensione + 1) {

		var temporary *TMemoriachunk
		temporary = (*TMemoriachunk)(Pointer(uintptr(uint32(uintptr(Pointer(rISULTATO))) + memoriachunkDimensione + dimensione)))

		temporary.allocated = false
		temporary.dimensione = rISULTATO.dimensione - dimensione - memoriachunkDimensione
		temporary.previous = rISULTATO
		temporary.successivo = rISULTATO.successivo

		if temporary.successivo != nil {
			temporary.successivo.previous = temporary
		}

		rISULTATO.dimensione = dimensione
		rISULTATO.successivo = temporary
	}
	rISULTATO.allocated = true

	return Pointer(uintptr(Pointer(rISULTATO)) + uintptr(memoriachunkDimensione))
}
func (séstesso *TMemoriamanager) Alignedmalloc(dimensione uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if dimensione == 0 || dimensione > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rISULTATO *TMemoriachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.successivo {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memoriachunkDimensione))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.dimensione && dimensione <= chunk.dimensione-diff {
			rISULTATO = chunk
			break
		}
	}
	if rISULTATO == nil {
		return nil, 0
	}
	dimensione += diff
	if rISULTATO.dimensione-dimensione >= memoriachunkDimensione+1 {
		temporary := (*TMemoriachunk)(Pointer(uintptr(Pointer(rISULTATO)) + uintptr(memoriachunkDimensione) + uintptr(dimensione)))
		temporary.allocated = false
		temporary.dimensione = rISULTATO.dimensione - dimensione - memoriachunkDimensione
		temporary.previous = rISULTATO
		temporary.successivo = rISULTATO.successivo
		if temporary.successivo != nil {
			temporary.successivo.previous = temporary
		}
		rISULTATO.dimensione = dimensione
		rISULTATO.successivo = temporary
	}
	rISULTATO.allocated = true
	return Pointer(uintptr(Pointer(rISULTATO)) + uintptr(memoriachunkDimensione) + uintptr(diff)), diff
}
func (séstesso *TMemoriamanager) Libero(riferimento_di_memoria_2 Pointer) {
	var chunk *TMemoriachunk = (*TMemoriachunk)(Pointer(uintptr(riferimento_di_memoria_2) - uintptr(memoriachunkDimensione)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.successivo = chunk.successivo
		chunk.previous.dimensione += chunk.dimensione + memoriachunkDimensione
		if chunk.successivo != nil {
			chunk.successivo.previous = chunk.previous
		}
	}

	if chunk.successivo != nil && !chunk.successivo.allocated {
		chunk.dimensione += chunk.successivo.dimensione + memoriachunkDimensione
		chunk.successivo = chunk.successivo.successivo
		if chunk.successivo != nil {
			chunk.successivo.previous = chunk
		}
	}
}
func Nuovo(dimensione int) Pointer {
	if AttivoMemoriamanager == nil {
		return nil
	}
	return AttivoMemoriamanager.Alloca_memoria(uint32(dimensione))
}
func Elimina(riferimento_di_memoria_2 Pointer) {
	if AttivoMemoriamanager != nil {
		AttivoMemoriamanager.Libero(riferimento_di_memoria_2)
	}
}
