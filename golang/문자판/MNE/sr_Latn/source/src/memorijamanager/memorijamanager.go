package memorymananger

import . "unsafe"

const MaksqueueVeličina uint32 = 0x1FFFFFF
const QueuePokreniaddress uint32 = 0x1000000

type TMemorijachunk struct {
	sledeće		*TMemorijachunk
	previous	*TMemorijachunk
	allocated	bool

	veličina	uint32
}

type TMemorijamanager struct {
}

var first *TMemorijachunk
var AktivnaMemorijamanager *TMemorijamanager = nil
var memorijachunkVeličina uint32

func (isti *TMemorijamanager) Init(pokreni uint32, veličina uint32) {

	AktivnaMemorijamanager = isti

	memorijachunkVeličina = uint32(Sizeof(TMemorijachunk{}))

	if veličina < memorijachunkVeličina {
		first = nil
	} else {
		first = (*TMemorijachunk)(Pointer(uintptr(QueuePokreniaddress) + uintptr(pokreni)))
		first.allocated = false
		first.previous = nil
		first.sledeće = nil
		first.veličina = veličina - memorijachunkVeličina
	}
}
func (isti *TMemorijamanager) Uništi() {
	if AktivnaMemorijamanager == isti {
		AktivnaMemorijamanager = nil
	}
}
func (isti *TMemorijamanager) Malloc(veličina uint32) Pointer {
	var iSHOD *TMemorijachunk = nil

	var chunk *TMemorijachunk = first
	for ; chunk != nil && iSHOD == nil; chunk = chunk.sledeće {
		if chunk.veličina > veličina && !chunk.allocated {
			iSHOD = chunk
		}
	}

	if iSHOD == nil {
		return nil
	}

	if iSHOD.veličina >= (veličina + memorijachunkVeličina + 1) {

		var temporary *TMemorijachunk
		temporary = (*TMemorijachunk)(Pointer(uintptr(uint32(uintptr(Pointer(iSHOD))) + memorijachunkVeličina + veličina)))

		temporary.allocated = false
		temporary.veličina = iSHOD.veličina - veličina - memorijachunkVeličina
		temporary.previous = iSHOD
		temporary.sledeće = iSHOD.sledeće

		if temporary.sledeće != nil {
			temporary.sledeće.previous = temporary
		}

		iSHOD.veličina = veličina
		iSHOD.sledeće = temporary
	}
	iSHOD.allocated = true

	return Pointer(uintptr(Pointer(iSHOD)) + uintptr(memorijachunkVeličina))
}
func (isti *TMemorijamanager) Alignedmalloc(veličina uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if veličina == 0 || veličina > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var iSHOD *TMemorijachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.sledeće {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorijachunkVeličina))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.veličina && veličina <= chunk.veličina-diff {
			iSHOD = chunk
			break
		}
	}
	if iSHOD == nil {
		return nil, 0
	}
	veličina += diff
	if iSHOD.veličina-veličina >= memorijachunkVeličina+1 {
		temporary := (*TMemorijachunk)(Pointer(uintptr(Pointer(iSHOD)) + uintptr(memorijachunkVeličina) + uintptr(veličina)))
		temporary.allocated = false
		temporary.veličina = iSHOD.veličina - veličina - memorijachunkVeličina
		temporary.previous = iSHOD
		temporary.sledeće = iSHOD.sledeće
		if temporary.sledeće != nil {
			temporary.sledeće.previous = temporary
		}
		iSHOD.veličina = veličina
		iSHOD.sledeće = temporary
	}
	iSHOD.allocated = true
	return Pointer(uintptr(Pointer(iSHOD)) + uintptr(memorijachunkVeličina) + uintptr(diff)), diff
}
func (isti *TMemorijamanager) Slobodno(pokazivač_2 Pointer) {
	var chunk *TMemorijachunk = (*TMemorijachunk)(Pointer(uintptr(pokazivač_2) - uintptr(memorijachunkVeličina)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.sledeće = chunk.sledeće
		chunk.previous.veličina += chunk.veličina + memorijachunkVeličina
		if chunk.sledeće != nil {
			chunk.sledeće.previous = chunk.previous
		}
	}

	if chunk.sledeće != nil && !chunk.sledeće.allocated {
		chunk.veličina += chunk.sledeće.veličina + memorijachunkVeličina
		chunk.sledeće = chunk.sledeće.sledeće
		if chunk.sledeće != nil {
			chunk.sledeće.previous = chunk
		}
	}
}
func Nova(veličina int) Pointer {
	if AktivnaMemorijamanager == nil {
		return nil
	}
	return AktivnaMemorijamanager.Malloc(uint32(veličina))
}
func Obriši(pokazivač_2 Pointer) {
	if AktivnaMemorijamanager != nil {
		AktivnaMemorijamanager.Slobodno(pokazivač_2)
	}
}
