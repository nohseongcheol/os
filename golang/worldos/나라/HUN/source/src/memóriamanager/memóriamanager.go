/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaximumqueueMéret uint32 = 0x1FFFFFF
const QueueIndításaddress uint32 = 0x1000000

type TMemóriachunk struct {
	következő	*TMemóriachunk
	previous	*TMemóriachunk
	allocated	bool

	méret	uint32
}

type TMemóriamanager struct {
}

var first *TMemóriachunk
var AktívMemóriamanager *TMemóriamanager = nil
var memóriachunkMéret uint32

func (self *TMemóriamanager) Init(indítás uint32, méret uint32) {

	AktívMemóriamanager = self

	memóriachunkMéret = uint32(Sizeof(TMemóriachunk{}))

	if méret < memóriachunkMéret {
		first = nil
	} else {
		first = (*TMemóriachunk)(Pointer(uintptr(QueueIndításaddress) + uintptr(indítás)))
		first.allocated = false
		first.previous = nil
		first.következő = nil
		first.méret = méret - memóriachunkMéret
	}
}
func (self *TMemóriamanager) Megsemmisítés() {
	if AktívMemóriamanager == self {
		AktívMemóriamanager = nil
	}
}
func (self *TMemóriamanager) Malloc(méret uint32) Pointer {
	var result *TMemóriachunk = nil

	var chunk *TMemóriachunk = first
	for ; chunk != nil && result == nil; chunk = chunk.következő {
		if chunk.méret > méret && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.méret >= (méret + memóriachunkMéret + 1) {

		var temporary *TMemóriachunk
		temporary = (*TMemóriachunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memóriachunkMéret + méret)))

		temporary.allocated = false
		temporary.méret = result.méret - méret - memóriachunkMéret
		temporary.previous = result
		temporary.következő = result.következő

		if temporary.következő != nil {
			temporary.következő.previous = temporary
		}

		result.méret = méret
		result.következő = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memóriachunkMéret))
}
func (self *TMemóriamanager) Alignedmalloc(méret uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if méret == 0 || méret > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemóriachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.következő {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memóriachunkMéret))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.méret && méret <= chunk.méret-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	méret += diff
	if result.méret-méret >= memóriachunkMéret+1 {
		temporary := (*TMemóriachunk)(Pointer(uintptr(Pointer(result)) + uintptr(memóriachunkMéret) + uintptr(méret)))
		temporary.allocated = false
		temporary.méret = result.méret - méret - memóriachunkMéret
		temporary.previous = result
		temporary.következő = result.következő
		if temporary.következő != nil {
			temporary.következő.previous = temporary
		}
		result.méret = méret
		result.következő = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memóriachunkMéret) + uintptr(diff)), diff
}
func (self *TMemóriamanager) Szabad(mutató_2 Pointer) {
	var chunk *TMemóriachunk = (*TMemóriachunk)(Pointer(uintptr(mutató_2) - uintptr(memóriachunkMéret)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.következő = chunk.következő
		chunk.previous.méret += chunk.méret + memóriachunkMéret
		if chunk.következő != nil {
			chunk.következő.previous = chunk.previous
		}
	}

	if chunk.következő != nil && !chunk.következő.allocated {
		chunk.méret += chunk.következő.méret + memóriachunkMéret
		chunk.következő = chunk.következő.következő
		if chunk.következő != nil {
			chunk.következő.previous = chunk
		}
	}
}
func Új(méret int) Pointer {
	if AktívMemóriamanager == nil {
		return nil
	}
	return AktívMemóriamanager.Malloc(uint32(méret))
}
func Törlés_2(mutató_2 Pointer) {
	if AktívMemóriamanager != nil {
		AktívMemóriamanager.Szabad(mutató_2)
	}
}
