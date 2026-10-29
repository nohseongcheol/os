/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const Maxqueueاندازه uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type Tحافظهchunk struct {
	بعدی		*Tحافظهchunk
	previous	*Tحافظهchunk
	allocated	bool

	اندازه	uint32
}

type Tحافظهmanager struct {
}

var first *Tحافظهchunk
var Aفعالحافظهmanager *Tحافظهmanager = nil
var حافظهchunkاندازه uint32

func (خود *Tحافظهmanager) Init(start uint32, اندازه uint32) {

	Aفعالحافظهmanager = خود

	حافظهchunkاندازه = uint32(Sizeof(Tحافظهchunk{}))

	if اندازه < حافظهchunkاندازه {
		first = nil
	} else {
		first = (*Tحافظهchunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.بعدی = nil
		first.اندازه = اندازه - حافظهchunkاندازه
	}
}
func (خود *Tحافظهmanager) Destroy() {
	if Aفعالحافظهmanager == خود {
		Aفعالحافظهmanager = nil
	}
}
func (خود *Tحافظهmanager) Malloc(اندازه uint32) Pointer {
	var result *Tحافظهchunk = nil

	var chunk *Tحافظهchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.بعدی {
		if chunk.اندازه > اندازه && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.اندازه >= (اندازه + حافظهchunkاندازه + 1) {

		var temporary *Tحافظهchunk
		temporary = (*Tحافظهchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + حافظهchunkاندازه + اندازه)))

		temporary.allocated = false
		temporary.اندازه = result.اندازه - اندازه - حافظهchunkاندازه
		temporary.previous = result
		temporary.بعدی = result.بعدی

		if temporary.بعدی != nil {
			temporary.بعدی.previous = temporary
		}

		result.اندازه = اندازه
		result.بعدی = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(حافظهchunkاندازه))
}
func (خود *Tحافظهmanager) Alignedmalloc(اندازه uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if اندازه == 0 || اندازه > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *Tحافظهchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.بعدی {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(حافظهchunkاندازه))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.اندازه && اندازه <= chunk.اندازه-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	اندازه += diff
	if result.اندازه-اندازه >= حافظهchunkاندازه+1 {
		temporary := (*Tحافظهchunk)(Pointer(uintptr(Pointer(result)) + uintptr(حافظهchunkاندازه) + uintptr(اندازه)))
		temporary.allocated = false
		temporary.اندازه = result.اندازه - اندازه - حافظهchunkاندازه
		temporary.previous = result
		temporary.بعدی = result.بعدی
		if temporary.بعدی != nil {
			temporary.بعدی.previous = temporary
		}
		result.اندازه = اندازه
		result.بعدی = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(حافظهchunkاندازه) + uintptr(diff)), diff
}
func (خود *Tحافظهmanager) Fآزاد(pointer_2 Pointer) {
	var chunk *Tحافظهchunk = (*Tحافظهchunk)(Pointer(uintptr(pointer_2) - uintptr(حافظهchunkاندازه)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.بعدی = chunk.بعدی
		chunk.previous.اندازه += chunk.اندازه + حافظهchunkاندازه
		if chunk.بعدی != nil {
			chunk.بعدی.previous = chunk.previous
		}
	}

	if chunk.بعدی != nil && !chunk.بعدی.allocated {
		chunk.اندازه += chunk.بعدی.اندازه + حافظهchunkاندازه
		chunk.بعدی = chunk.بعدی.بعدی
		if chunk.بعدی != nil {
			chunk.بعدی.previous = chunk
		}
	}
}
func Nجدید(اندازه int) Pointer {
	if Aفعالحافظهmanager == nil {
		return nil
	}
	return Aفعالحافظهmanager.Malloc(uint32(اندازه))
}
func Dحذف(pointer_2 Pointer) {
	if Aفعالحافظهmanager != nil {
		Aفعالحافظهmanager.Fآزاد(pointer_2)
	}
}
