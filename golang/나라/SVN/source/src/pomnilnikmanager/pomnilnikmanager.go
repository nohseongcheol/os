package memorymananger

import . "unsafe"

const MaxqueueVelikost uint32 = 0x1FFFFFF
const QueueZačniaddress uint32 = 0x1000000

type TPomnilnikchunk struct {
	naslednje	*TPomnilnikchunk
	previous	*TPomnilnikchunk
	allocated	bool

	velikost	uint32
}

type TPomnilnikmanager struct {
}

var prvi *TPomnilnikchunk
var DejavenPomnilnikmanager *TPomnilnikmanager = nil
var pomnilnikchunkVelikost uint32

func (sam *TPomnilnikmanager) Init(začni uint32, velikost uint32) {

	DejavenPomnilnikmanager = sam

	pomnilnikchunkVelikost = uint32(Sizeof(TPomnilnikchunk{}))

	if velikost < pomnilnikchunkVelikost {
		prvi = nil
	} else {
		prvi = (*TPomnilnikchunk)(Pointer(uintptr(QueueZačniaddress) + uintptr(začni)))
		prvi.allocated = false
		prvi.previous = nil
		prvi.naslednje = nil
		prvi.velikost = velikost - pomnilnikchunkVelikost
	}
}
func (sam *TPomnilnikmanager) Uniči() {
	if DejavenPomnilnikmanager == sam {
		DejavenPomnilnikmanager = nil
	}
}
func (sam *TPomnilnikmanager) Malloc(velikost uint32) Pointer {
	var rEZULTAT *TPomnilnikchunk = nil

	var chunk *TPomnilnikchunk = prvi
	for ; chunk != nil && rEZULTAT == nil; chunk = chunk.naslednje {
		if chunk.velikost > velikost && !chunk.allocated {
			rEZULTAT = chunk
		}
	}

	if rEZULTAT == nil {
		return nil
	}

	if rEZULTAT.velikost >= (velikost + pomnilnikchunkVelikost + 1) {

		var temporary *TPomnilnikchunk
		temporary = (*TPomnilnikchunk)(Pointer(uintptr(uint32(uintptr(Pointer(rEZULTAT))) + pomnilnikchunkVelikost + velikost)))

		temporary.allocated = false
		temporary.velikost = rEZULTAT.velikost - velikost - pomnilnikchunkVelikost
		temporary.previous = rEZULTAT
		temporary.naslednje = rEZULTAT.naslednje

		if temporary.naslednje != nil {
			temporary.naslednje.previous = temporary
		}

		rEZULTAT.velikost = velikost
		rEZULTAT.naslednje = temporary
	}
	rEZULTAT.allocated = true

	return Pointer(uintptr(Pointer(rEZULTAT)) + uintptr(pomnilnikchunkVelikost))
}
func (sam *TPomnilnikmanager) Alignedmalloc(velikost uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if velikost == 0 || velikost > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rEZULTAT *TPomnilnikchunk
	var diff uint32
	for chunk := prvi; chunk != nil; chunk = chunk.naslednje {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(pomnilnikchunkVelikost))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.velikost && velikost <= chunk.velikost-diff {
			rEZULTAT = chunk
			break
		}
	}
	if rEZULTAT == nil {
		return nil, 0
	}
	velikost += diff
	if rEZULTAT.velikost-velikost >= pomnilnikchunkVelikost+1 {
		temporary := (*TPomnilnikchunk)(Pointer(uintptr(Pointer(rEZULTAT)) + uintptr(pomnilnikchunkVelikost) + uintptr(velikost)))
		temporary.allocated = false
		temporary.velikost = rEZULTAT.velikost - velikost - pomnilnikchunkVelikost
		temporary.previous = rEZULTAT
		temporary.naslednje = rEZULTAT.naslednje
		if temporary.naslednje != nil {
			temporary.naslednje.previous = temporary
		}
		rEZULTAT.velikost = velikost
		rEZULTAT.naslednje = temporary
	}
	rEZULTAT.allocated = true
	return Pointer(uintptr(Pointer(rEZULTAT)) + uintptr(pomnilnikchunkVelikost) + uintptr(diff)), diff
}
func (sam *TPomnilnikmanager) Prosto(kazalnik_2 Pointer) {
	var chunk *TPomnilnikchunk = (*TPomnilnikchunk)(Pointer(uintptr(kazalnik_2) - uintptr(pomnilnikchunkVelikost)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.naslednje = chunk.naslednje
		chunk.previous.velikost += chunk.velikost + pomnilnikchunkVelikost
		if chunk.naslednje != nil {
			chunk.naslednje.previous = chunk.previous
		}
	}

	if chunk.naslednje != nil && !chunk.naslednje.allocated {
		chunk.velikost += chunk.naslednje.velikost + pomnilnikchunkVelikost
		chunk.naslednje = chunk.naslednje.naslednje
		if chunk.naslednje != nil {
			chunk.naslednje.previous = chunk
		}
	}
}
func Nova(velikost int) Pointer {
	if DejavenPomnilnikmanager == nil {
		return nil
	}
	return DejavenPomnilnikmanager.Malloc(uint32(velikost))
}
func Izbriši(kazalnik_2 Pointer) {
	if DejavenPomnilnikmanager != nil {
		DejavenPomnilnikmanager.Prosto(kazalnik_2)
	}
}
