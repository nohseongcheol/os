/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const Maxqueuesize uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type Tමතකයchunk struct {
	ඊලඟ		*Tමතකයchunk
	previous	*Tමතකයchunk
	allocated	bool

	size	uint32
}

type Tමතකයmanager struct {
}

var first *Tමතකයchunk
var Activeමතකයmanager *Tමතකයmanager = nil
var මතකයchunksize uint32

func (self *Tමතකයmanager) Init(start uint32, size uint32) {

	Activeමතකයmanager = self

	මතකයchunksize = uint32(Sizeof(Tමතකයchunk{}))

	if size < මතකයchunksize {
		first = nil
	} else {
		first = (*Tමතකයchunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.ඊලඟ = nil
		first.size = size - මතකයchunksize
	}
}
func (self *Tමතකයmanager) Destroy() {
	if Activeමතකයmanager == self {
		Activeමතකයmanager = nil
	}
}
func (self *Tමතකයmanager) Malloc(size uint32) Pointer {
	var result *Tමතකයchunk = nil

	var chunk *Tමතකයchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.ඊලඟ {
		if chunk.size > size && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.size >= (size + මතකයchunksize + 1) {

		var temporary *Tමතකයchunk
		temporary = (*Tමතකයchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + මතකයchunksize + size)))

		temporary.allocated = false
		temporary.size = result.size - size - මතකයchunksize
		temporary.previous = result
		temporary.ඊලඟ = result.ඊලඟ

		if temporary.ඊලඟ != nil {
			temporary.ඊලඟ.previous = temporary
		}

		result.size = size
		result.ඊලඟ = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(මතකයchunksize))
}
func (self *Tමතකයmanager) Alignedmalloc(size uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if size == 0 || size > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *Tමතකයchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.ඊලඟ {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(මතකයchunksize))
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
	if result.size-size >= මතකයchunksize+1 {
		temporary := (*Tමතකයchunk)(Pointer(uintptr(Pointer(result)) + uintptr(මතකයchunksize) + uintptr(size)))
		temporary.allocated = false
		temporary.size = result.size - size - මතකයchunksize
		temporary.previous = result
		temporary.ඊලඟ = result.ඊලඟ
		if temporary.ඊලඟ != nil {
			temporary.ඊලඟ.previous = temporary
		}
		result.size = size
		result.ඊලඟ = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(මතකයchunksize) + uintptr(diff)), diff
}
func (self *Tමතකයmanager) Free(pointer_2 Pointer) {
	var chunk *Tමතකයchunk = (*Tමතකයchunk)(Pointer(uintptr(pointer_2) - uintptr(මතකයchunksize)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.ඊලඟ = chunk.ඊලඟ
		chunk.previous.size += chunk.size + මතකයchunksize
		if chunk.ඊලඟ != nil {
			chunk.ඊලඟ.previous = chunk.previous
		}
	}

	if chunk.ඊලඟ != nil && !chunk.ඊලඟ.allocated {
		chunk.size += chunk.ඊලඟ.size + මතකයchunksize
		chunk.ඊලඟ = chunk.ඊලඟ.ඊලඟ
		if chunk.ඊලඟ != nil {
			chunk.ඊලඟ.previous = chunk
		}
	}
}
func Nනව(size int) Pointer {
	if Activeමතකයmanager == nil {
		return nil
	}
	return Activeමතකයmanager.Malloc(uint32(size))
}
func Delete(pointer_2 Pointer) {
	if Activeමතකයmanager != nil {
		Activeමතකයmanager.Free(pointer_2)
	}
}
