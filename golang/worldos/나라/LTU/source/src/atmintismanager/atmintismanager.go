/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaksqueueDydis uint32 = 0x1FFFFFF
const QueuePaleistiaddress uint32 = 0x1000000

type TAtmintischunk struct {
	kitas		*TAtmintischunk
	previous	*TAtmintischunk
	allocated	bool

	dydis	uint32
}

type TAtmintismanager struct {
}

var first *TAtmintischunk
var AktyvusAtmintismanager *TAtmintismanager = nil
var atmintischunkDydis uint32

func (self *TAtmintismanager) Init(paleisti uint32, dydis uint32) {

	AktyvusAtmintismanager = self

	atmintischunkDydis = uint32(Sizeof(TAtmintischunk{}))

	if dydis < atmintischunkDydis {
		first = nil
	} else {
		first = (*TAtmintischunk)(Pointer(uintptr(QueuePaleistiaddress) + uintptr(paleisti)))
		first.allocated = false
		first.previous = nil
		first.kitas = nil
		first.dydis = dydis - atmintischunkDydis
	}
}
func (self *TAtmintismanager) Sunaikinti() {
	if AktyvusAtmintismanager == self {
		AktyvusAtmintismanager = nil
	}
}
func (self *TAtmintismanager) Malloc(dydis uint32) Pointer {
	var rEZULTATAS *TAtmintischunk = nil

	var chunk *TAtmintischunk = first
	for ; chunk != nil && rEZULTATAS == nil; chunk = chunk.kitas {
		if chunk.dydis > dydis && !chunk.allocated {
			rEZULTATAS = chunk
		}
	}

	if rEZULTATAS == nil {
		return nil
	}

	if rEZULTATAS.dydis >= (dydis + atmintischunkDydis + 1) {

		var temporary *TAtmintischunk
		temporary = (*TAtmintischunk)(Pointer(uintptr(uint32(uintptr(Pointer(rEZULTATAS))) + atmintischunkDydis + dydis)))

		temporary.allocated = false
		temporary.dydis = rEZULTATAS.dydis - dydis - atmintischunkDydis
		temporary.previous = rEZULTATAS
		temporary.kitas = rEZULTATAS.kitas

		if temporary.kitas != nil {
			temporary.kitas.previous = temporary
		}

		rEZULTATAS.dydis = dydis
		rEZULTATAS.kitas = temporary
	}
	rEZULTATAS.allocated = true

	return Pointer(uintptr(Pointer(rEZULTATAS)) + uintptr(atmintischunkDydis))
}
func (self *TAtmintismanager) Alignedmalloc(dydis uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if dydis == 0 || dydis > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rEZULTATAS *TAtmintischunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.kitas {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(atmintischunkDydis))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.dydis && dydis <= chunk.dydis-diff {
			rEZULTATAS = chunk
			break
		}
	}
	if rEZULTATAS == nil {
		return nil, 0
	}
	dydis += diff
	if rEZULTATAS.dydis-dydis >= atmintischunkDydis+1 {
		temporary := (*TAtmintischunk)(Pointer(uintptr(Pointer(rEZULTATAS)) + uintptr(atmintischunkDydis) + uintptr(dydis)))
		temporary.allocated = false
		temporary.dydis = rEZULTATAS.dydis - dydis - atmintischunkDydis
		temporary.previous = rEZULTATAS
		temporary.kitas = rEZULTATAS.kitas
		if temporary.kitas != nil {
			temporary.kitas.previous = temporary
		}
		rEZULTATAS.dydis = dydis
		rEZULTATAS.kitas = temporary
	}
	rEZULTATAS.allocated = true
	return Pointer(uintptr(Pointer(rEZULTATAS)) + uintptr(atmintischunkDydis) + uintptr(diff)), diff
}
func (self *TAtmintismanager) Laisva(rodyklė_3 Pointer) {
	var chunk *TAtmintischunk = (*TAtmintischunk)(Pointer(uintptr(rodyklė_3) - uintptr(atmintischunkDydis)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.kitas = chunk.kitas
		chunk.previous.dydis += chunk.dydis + atmintischunkDydis
		if chunk.kitas != nil {
			chunk.kitas.previous = chunk.previous
		}
	}

	if chunk.kitas != nil && !chunk.kitas.allocated {
		chunk.dydis += chunk.kitas.dydis + atmintischunkDydis
		chunk.kitas = chunk.kitas.kitas
		if chunk.kitas != nil {
			chunk.kitas.previous = chunk
		}
	}
}
func Naujas(dydis int) Pointer {
	if AktyvusAtmintismanager == nil {
		return nil
	}
	return AktyvusAtmintismanager.Malloc(uint32(dydis))
}
func Ištrinti(rodyklė_3 Pointer) {
	if AktyvusAtmintismanager != nil {
		AktyvusAtmintismanager.Laisva(rodyklė_3)
	}
}
