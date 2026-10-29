/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueХэмжээ uint32 = 0x1FFFFFF
const QueueЭхлэлaddress uint32 = 0x1000000

type TСанахойchunk struct {
	дараах		*TСанахойchunk
	previous	*TСанахойchunk
	allocated	bool

	хэмжээ	uint32
}

type TСанахойЗохицуулагч struct {
}

var first *TСанахойchunk
var ИдэвхтэйСанахойЗохицуулагч *TСанахойЗохицуулагч = nil
var санахойchunkХэмжээ uint32

func (self *TСанахойЗохицуулагч) Init(эхлэл uint32, хэмжээ uint32) {

	ИдэвхтэйСанахойЗохицуулагч = self

	санахойchunkХэмжээ = uint32(Sizeof(TСанахойchunk{}))

	if хэмжээ < санахойchunkХэмжээ {
		first = nil
	} else {
		first = (*TСанахойchunk)(Pointer(uintptr(QueueЭхлэлaddress) + uintptr(эхлэл)))
		first.allocated = false
		first.previous = nil
		first.дараах = nil
		first.хэмжээ = хэмжээ - санахойchunkХэмжээ
	}
}
func (self *TСанахойЗохицуулагч) Destroy() {
	if ИдэвхтэйСанахойЗохицуулагч == self {
		ИдэвхтэйСанахойЗохицуулагч = nil
	}
}
func (self *TСанахойЗохицуулагч) Malloc(хэмжээ uint32) Pointer {
	var result *TСанахойchunk = nil

	var chunk *TСанахойchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.дараах {
		if chunk.хэмжээ > хэмжээ && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.хэмжээ >= (хэмжээ + санахойchunkХэмжээ + 1) {

		var temporary *TСанахойchunk
		temporary = (*TСанахойchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + санахойchunkХэмжээ + хэмжээ)))

		temporary.allocated = false
		temporary.хэмжээ = result.хэмжээ - хэмжээ - санахойchunkХэмжээ
		temporary.previous = result
		temporary.дараах = result.дараах

		if temporary.дараах != nil {
			temporary.дараах.previous = temporary
		}

		result.хэмжээ = хэмжээ
		result.дараах = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(санахойchunkХэмжээ))
}
func (self *TСанахойЗохицуулагч) Alignedmalloc(хэмжээ uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if хэмжээ == 0 || хэмжээ > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TСанахойchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.дараах {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(санахойchunkХэмжээ))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.хэмжээ && хэмжээ <= chunk.хэмжээ-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	хэмжээ += diff
	if result.хэмжээ-хэмжээ >= санахойchunkХэмжээ+1 {
		temporary := (*TСанахойchunk)(Pointer(uintptr(Pointer(result)) + uintptr(санахойchunkХэмжээ) + uintptr(хэмжээ)))
		temporary.allocated = false
		temporary.хэмжээ = result.хэмжээ - хэмжээ - санахойchunkХэмжээ
		temporary.previous = result
		temporary.дараах = result.дараах
		if temporary.дараах != nil {
			temporary.дараах.previous = temporary
		}
		result.хэмжээ = хэмжээ
		result.дараах = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(санахойchunkХэмжээ) + uintptr(diff)), diff
}
func (self *TСанахойЗохицуулагч) Чөлөөт(pointer_2 Pointer) {
	var chunk *TСанахойchunk = (*TСанахойchunk)(Pointer(uintptr(pointer_2) - uintptr(санахойchunkХэмжээ)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.дараах = chunk.дараах
		chunk.previous.хэмжээ += chunk.хэмжээ + санахойchunkХэмжээ
		if chunk.дараах != nil {
			chunk.дараах.previous = chunk.previous
		}
	}

	if chunk.дараах != nil && !chunk.дараах.allocated {
		chunk.хэмжээ += chunk.дараах.хэмжээ + санахойchunkХэмжээ
		chunk.дараах = chunk.дараах.дараах
		if chunk.дараах != nil {
			chunk.дараах.previous = chunk
		}
	}
}
func Шинэ(хэмжээ int) Pointer {
	if ИдэвхтэйСанахойЗохицуулагч == nil {
		return nil
	}
	return ИдэвхтэйСанахойЗохицуулагч.Malloc(uint32(хэмжээ))
}
func Устгах(pointer_2 Pointer) {
	if ИдэвхтэйСанахойЗохицуулагч != nil {
		ИдэвхтэйСанахойЗохицуулагч.Чөлөөт(pointer_2)
	}
}
