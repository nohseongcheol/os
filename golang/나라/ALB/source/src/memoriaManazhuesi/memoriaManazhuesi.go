package memorymananger

import . "unsafe"

const MaxqueueMadhësia uint32 = 0x1FFFFFF
const QueueFilloaddress uint32 = 0x1000000

type TMemoriachunk struct {
	pasuesen	*TMemoriachunk
	previous	*TMemoriachunk
	allocated	bool

	madhësia	uint32
}

type TMemoriaManazhuesi struct {
}

var first *TMemoriachunk
var AktivMemoriaManazhuesi *TMemoriaManazhuesi = nil
var memoriachunkMadhësia uint32

func (vetvetja *TMemoriaManazhuesi) Init(fillo uint32, madhësia uint32) {

	AktivMemoriaManazhuesi = vetvetja

	memoriachunkMadhësia = uint32(Sizeof(TMemoriachunk{}))

	if madhësia < memoriachunkMadhësia {
		first = nil
	} else {
		first = (*TMemoriachunk)(Pointer(uintptr(QueueFilloaddress) + uintptr(fillo)))
		first.allocated = false
		first.previous = nil
		first.pasuesen = nil
		first.madhësia = madhësia - memoriachunkMadhësia
	}
}
func (vetvetja *TMemoriaManazhuesi) Shkatërroje() {
	if AktivMemoriaManazhuesi == vetvetja {
		AktivMemoriaManazhuesi = nil
	}
}
func (vetvetja *TMemoriaManazhuesi) Malloc(madhësia uint32) Pointer {
	var result *TMemoriachunk = nil

	var chunk *TMemoriachunk = first
	for ; chunk != nil && result == nil; chunk = chunk.pasuesen {
		if chunk.madhësia > madhësia && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.madhësia >= (madhësia + memoriachunkMadhësia + 1) {

		var temporary *TMemoriachunk
		temporary = (*TMemoriachunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memoriachunkMadhësia + madhësia)))

		temporary.allocated = false
		temporary.madhësia = result.madhësia - madhësia - memoriachunkMadhësia
		temporary.previous = result
		temporary.pasuesen = result.pasuesen

		if temporary.pasuesen != nil {
			temporary.pasuesen.previous = temporary
		}

		result.madhësia = madhësia
		result.pasuesen = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memoriachunkMadhësia))
}
func (vetvetja *TMemoriaManazhuesi) Alignedmalloc(madhësia uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if madhësia == 0 || madhësia > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemoriachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.pasuesen {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memoriachunkMadhësia))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.madhësia && madhësia <= chunk.madhësia-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	madhësia += diff
	if result.madhësia-madhësia >= memoriachunkMadhësia+1 {
		temporary := (*TMemoriachunk)(Pointer(uintptr(Pointer(result)) + uintptr(memoriachunkMadhësia) + uintptr(madhësia)))
		temporary.allocated = false
		temporary.madhësia = result.madhësia - madhësia - memoriachunkMadhësia
		temporary.previous = result
		temporary.pasuesen = result.pasuesen
		if temporary.pasuesen != nil {
			temporary.pasuesen.previous = temporary
		}
		result.madhësia = madhësia
		result.pasuesen = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memoriachunkMadhësia) + uintptr(diff)), diff
}
func (vetvetja *TMemoriaManazhuesi) Elirë(kursori_2 Pointer) {
	var chunk *TMemoriachunk = (*TMemoriachunk)(Pointer(uintptr(kursori_2) - uintptr(memoriachunkMadhësia)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.pasuesen = chunk.pasuesen
		chunk.previous.madhësia += chunk.madhësia + memoriachunkMadhësia
		if chunk.pasuesen != nil {
			chunk.pasuesen.previous = chunk.previous
		}
	}

	if chunk.pasuesen != nil && !chunk.pasuesen.allocated {
		chunk.madhësia += chunk.pasuesen.madhësia + memoriachunkMadhësia
		chunk.pasuesen = chunk.pasuesen.pasuesen
		if chunk.pasuesen != nil {
			chunk.pasuesen.previous = chunk
		}
	}
}
func IRi(madhësia int) Pointer {
	if AktivMemoriaManazhuesi == nil {
		return nil
	}
	return AktivMemoriaManazhuesi.Malloc(uint32(madhësia))
}
func Elemino(kursori_2 Pointer) {
	if AktivMemoriaManazhuesi != nil {
		AktivMemoriaManazhuesi.Elirë(kursori_2)
	}
}
