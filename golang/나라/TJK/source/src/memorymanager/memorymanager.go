/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const Maxqueuesize uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TMemorychunk struct {
	навбатӣ		*TMemorychunk
	previous	*TMemorychunk
	allocated	bool

	size	uint32
}

type TMemorymanager struct {
}

var first *TMemorychunk
var Activememorymanager *TMemorymanager = nil
var memorychunksize uint32

func (self *TMemorymanager) Init(start uint32, size uint32) {

	Activememorymanager = self

	memorychunksize = uint32(Sizeof(TMemorychunk{}))

	if size < memorychunksize {
		first = nil
	} else {
		first = (*TMemorychunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.навбатӣ = nil
		first.size = size - memorychunksize
	}
}
func (self *TMemorymanager) Destroy() {
	if Activememorymanager == self {
		Activememorymanager = nil
	}
}
func (self *TMemorymanager) Malloc(size uint32) Pointer {
	var result *TMemorychunk = nil

	var chunk *TMemorychunk = first
	for ; chunk != nil && result == nil; chunk = chunk.навбатӣ {
		if chunk.size > size && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.size >= (size + memorychunksize + 1) {

		var temporary *TMemorychunk
		temporary = (*TMemorychunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + memorychunksize + size)))

		temporary.allocated = false
		temporary.size = result.size - size - memorychunksize
		temporary.previous = result
		temporary.навбатӣ = result.навбатӣ

		if temporary.навбатӣ != nil {
			temporary.навбатӣ.previous = temporary
		}

		result.size = size
		result.навбатӣ = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunksize))
}
func (self *TMemorymanager) Alignedmalloc(size uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if size == 0 || size > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TMemorychunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.навбатӣ {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorychunksize))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.size && size <= chunk.size-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	size += diff
	if result.size-size >= memorychunksize+1 {
		temporary := (*TMemorychunk)(Pointer(uintptr(Pointer(result)) + uintptr(memorychunksize) + uintptr(size)))
		temporary.allocated = false
		temporary.size = result.size - size - memorychunksize
		temporary.previous = result
		temporary.навбатӣ = result.навбатӣ
		if temporary.навбатӣ != nil {
			temporary.навбатӣ.previous = temporary
		}
		result.size = size
		result.навбатӣ = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(memorychunksize) + uintptr(diff)), diff
}
func (self *TMemorymanager) Free(pointer_2 Pointer) {
	var chunk *TMemorychunk = (*TMemorychunk)(Pointer(uintptr(pointer_2) - uintptr(memorychunksize)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.навбатӣ = chunk.навбатӣ
		chunk.previous.size += chunk.size + memorychunksize
		if chunk.навбатӣ != nil {
			chunk.навбатӣ.previous = chunk.previous
		}
	}

	if chunk.навбатӣ != nil && !chunk.навбатӣ.allocated {
		chunk.size += chunk.навбатӣ.size + memorychunksize
		chunk.навбатӣ = chunk.навбатӣ.навбатӣ
		if chunk.навбатӣ != nil {
			chunk.навбатӣ.previous = chunk
		}
	}
}
func Нав(size int) Pointer {
	if Activememorymanager == nil {
		return nil
	}
	return Activememorymanager.Malloc(uint32(size))
}
func Несткардан(pointer_2 Pointer) {
	if Activememorymanager != nil {
		Activememorymanager.Free(pointer_2)
	}
}
