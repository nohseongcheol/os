/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueHabe uint32 = 0x1FFFFFF
const QueueAtomboyaddress uint32 = 0x1000000

type TArikachunk struct {
	manaraka	*TArikachunk
	previous	*TArikachunk
	allocated	bool

	habe	uint32
}

type TArikaMpandrindra struct {
}

var first *TArikachunk
var MiasaArikaMpandrindra *TArikaMpandrindra = nil
var arikachunkHabe uint32

func (nytena *TArikaMpandrindra) Init(atomboy uint32, habe uint32) {

	MiasaArikaMpandrindra = nytena

	arikachunkHabe = uint32(Sizeof(TArikachunk{}))

	if habe < arikachunkHabe {
		first = nil
	} else {
		first = (*TArikachunk)(Pointer(uintptr(QueueAtomboyaddress) + uintptr(atomboy)))
		first.allocated = false
		first.previous = nil
		first.manaraka = nil
		first.habe = habe - arikachunkHabe
	}
}
func (nytena *TArikaMpandrindra) Destroy() {
	if MiasaArikaMpandrindra == nytena {
		MiasaArikaMpandrindra = nil
	}
}
func (nytena *TArikaMpandrindra) Malloc(habe uint32) Pointer {
	var result *TArikachunk = nil

	var chunk *TArikachunk = first
	for ; chunk != nil && result == nil; chunk = chunk.manaraka {
		if chunk.habe > habe && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.habe >= (habe + arikachunkHabe + 1) {

		var temporary *TArikachunk
		temporary = (*TArikachunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + arikachunkHabe + habe)))

		temporary.allocated = false
		temporary.habe = result.habe - habe - arikachunkHabe
		temporary.previous = result
		temporary.manaraka = result.manaraka

		if temporary.manaraka != nil {
			temporary.manaraka.previous = temporary
		}

		result.habe = habe
		result.manaraka = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(arikachunkHabe))
}
func (nytena *TArikaMpandrindra) Alignedmalloc(habe uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if habe == 0 || habe > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TArikachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.manaraka {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(arikachunkHabe))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.habe && habe <= chunk.habe-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	habe += diff
	if result.habe-habe >= arikachunkHabe+1 {
		temporary := (*TArikachunk)(Pointer(uintptr(Pointer(result)) + uintptr(arikachunkHabe) + uintptr(habe)))
		temporary.allocated = false
		temporary.habe = result.habe - habe - arikachunkHabe
		temporary.previous = result
		temporary.manaraka = result.manaraka
		if temporary.manaraka != nil {
			temporary.manaraka.previous = temporary
		}
		result.habe = habe
		result.manaraka = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(arikachunkHabe) + uintptr(diff)), diff
}
func (nytena *TArikaMpandrindra) Malalaka(pointer_2 Pointer) {
	var chunk *TArikachunk = (*TArikachunk)(Pointer(uintptr(pointer_2) - uintptr(arikachunkHabe)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.manaraka = chunk.manaraka
		chunk.previous.habe += chunk.habe + arikachunkHabe
		if chunk.manaraka != nil {
			chunk.manaraka.previous = chunk.previous
		}
	}

	if chunk.manaraka != nil && !chunk.manaraka.allocated {
		chunk.habe += chunk.manaraka.habe + arikachunkHabe
		chunk.manaraka = chunk.manaraka.manaraka
		if chunk.manaraka != nil {
			chunk.manaraka.previous = chunk
		}
	}
}
func Vaovao(habe int) Pointer {
	if MiasaArikaMpandrindra == nil {
		return nil
	}
	return MiasaArikaMpandrindra.Malloc(uint32(habe))
}
func Fafao(pointer_2 Pointer) {
	if MiasaArikaMpandrindra != nil {
		MiasaArikaMpandrindra.Malalaka(pointer_2)
	}
}
