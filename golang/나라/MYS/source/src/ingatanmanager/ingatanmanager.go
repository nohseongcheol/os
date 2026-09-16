/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaksqueueSaiz uint32 = 0x1FFFFFF
const QueueMulaaddress uint32 = 0x1000000

type TIngatanchunk struct {
	berikutnya	*TIngatanchunk
	previous	*TIngatanchunk
	allocated	bool

	saiz	uint32
}

type TIngatanmanager struct {
}

var first *TIngatanchunk
var AktifIngatanmanager *TIngatanmanager = nil
var ingatanchunkSaiz uint32

func (diri *TIngatanmanager) Init(mula uint32, saiz uint32) {

	AktifIngatanmanager = diri

	ingatanchunkSaiz = uint32(Sizeof(TIngatanchunk{}))

	if saiz < ingatanchunkSaiz {
		first = nil
	} else {
		first = (*TIngatanchunk)(Pointer(uintptr(QueueMulaaddress) + uintptr(mula)))
		first.allocated = false
		first.previous = nil
		first.berikutnya = nil
		first.saiz = saiz - ingatanchunkSaiz
	}
}
func (diri *TIngatanmanager) Musnah() {
	if AktifIngatanmanager == diri {
		AktifIngatanmanager = nil
	}
}
func (diri *TIngatanmanager) Peruntukkan_ingatan(saiz uint32) Pointer {
	var result *TIngatanchunk = nil

	var chunk *TIngatanchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.berikutnya {
		if chunk.saiz > saiz && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.saiz >= (saiz + ingatanchunkSaiz + 1) {

		var temporary *TIngatanchunk
		temporary = (*TIngatanchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + ingatanchunkSaiz + saiz)))

		temporary.allocated = false
		temporary.saiz = result.saiz - saiz - ingatanchunkSaiz
		temporary.previous = result
		temporary.berikutnya = result.berikutnya

		if temporary.berikutnya != nil {
			temporary.berikutnya.previous = temporary
		}

		result.saiz = saiz
		result.berikutnya = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(ingatanchunkSaiz))
}
func (diri *TIngatanmanager) Alignedmalloc(saiz uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if saiz == 0 || saiz > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TIngatanchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.berikutnya {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(ingatanchunkSaiz))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.saiz && saiz <= chunk.saiz-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	saiz += diff
	if result.saiz-saiz >= ingatanchunkSaiz+1 {
		temporary := (*TIngatanchunk)(Pointer(uintptr(Pointer(result)) + uintptr(ingatanchunkSaiz) + uintptr(saiz)))
		temporary.allocated = false
		temporary.saiz = result.saiz - saiz - ingatanchunkSaiz
		temporary.previous = result
		temporary.berikutnya = result.berikutnya
		if temporary.berikutnya != nil {
			temporary.berikutnya.previous = temporary
		}
		result.saiz = saiz
		result.berikutnya = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(ingatanchunkSaiz) + uintptr(diff)), diff
}
func (diri *TIngatanmanager) Bebas(rujukan_alamat_2 Pointer) {
	var chunk *TIngatanchunk = (*TIngatanchunk)(Pointer(uintptr(rujukan_alamat_2) - uintptr(ingatanchunkSaiz)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.berikutnya = chunk.berikutnya
		chunk.previous.saiz += chunk.saiz + ingatanchunkSaiz
		if chunk.berikutnya != nil {
			chunk.berikutnya.previous = chunk.previous
		}
	}

	if chunk.berikutnya != nil && !chunk.berikutnya.allocated {
		chunk.saiz += chunk.berikutnya.saiz + ingatanchunkSaiz
		chunk.berikutnya = chunk.berikutnya.berikutnya
		if chunk.berikutnya != nil {
			chunk.berikutnya.previous = chunk
		}
	}
}
func Baharu(saiz int) Pointer {
	if AktifIngatanmanager == nil {
		return nil
	}
	return AktifIngatanmanager.Peruntukkan_ingatan(uint32(saiz))
}
func Padam(rujukan_alamat_2 Pointer) {
	if AktifIngatanmanager != nil {
		AktifIngatanmanager.Bebas(rujukan_alamat_2)
	}
}
