/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const Mزیادہqueueحجم uint32 = 0x1FFFFFF
const Queueچلائیںaddress uint32 = 0x1000000

type Tیادداشتchunk struct {
	اگلا		*Tیادداشتchunk
	previous	*Tیادداشتchunk
	allocated	bool

	حجم	uint32
}

type Tیادداشتmanager struct {
}

var first *Tیادداشتchunk
var Aفعالیادداشتmanager *Tیادداشتmanager = nil
var یادداشتchunkحجم uint32

func (self *Tیادداشتmanager) Init(چلائیں uint32, حجم uint32) {

	Aفعالیادداشتmanager = self

	یادداشتchunkحجم = uint32(Sizeof(Tیادداشتchunk{}))

	if حجم < یادداشتchunkحجم {
		first = nil
	} else {
		first = (*Tیادداشتchunk)(Pointer(uintptr(Queueچلائیںaddress) + uintptr(چلائیں)))
		first.allocated = false
		first.previous = nil
		first.اگلا = nil
		first.حجم = حجم - یادداشتchunkحجم
	}
}
func (self *Tیادداشتmanager) Dتباہکریں() {
	if Aفعالیادداشتmanager == self {
		Aفعالیادداشتmanager = nil
	}
}
func (self *Tیادداشتmanager) Malloc(حجم uint32) Pointer {
	var result *Tیادداشتchunk = nil

	var chunk *Tیادداشتchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.اگلا {
		if chunk.حجم > حجم && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.حجم >= (حجم + یادداشتchunkحجم + 1) {

		var temporary *Tیادداشتchunk
		temporary = (*Tیادداشتchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + یادداشتchunkحجم + حجم)))

		temporary.allocated = false
		temporary.حجم = result.حجم - حجم - یادداشتchunkحجم
		temporary.previous = result
		temporary.اگلا = result.اگلا

		if temporary.اگلا != nil {
			temporary.اگلا.previous = temporary
		}

		result.حجم = حجم
		result.اگلا = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(یادداشتchunkحجم))
}
func (self *Tیادداشتmanager) Alignedmalloc(حجم uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if حجم == 0 || حجم > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *Tیادداشتchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.اگلا {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(یادداشتchunkحجم))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.حجم && حجم <= chunk.حجم-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	حجم += diff
	if result.حجم-حجم >= یادداشتchunkحجم+1 {
		temporary := (*Tیادداشتchunk)(Pointer(uintptr(Pointer(result)) + uintptr(یادداشتchunkحجم) + uintptr(حجم)))
		temporary.allocated = false
		temporary.حجم = result.حجم - حجم - یادداشتchunkحجم
		temporary.previous = result
		temporary.اگلا = result.اگلا
		if temporary.اگلا != nil {
			temporary.اگلا.previous = temporary
		}
		result.حجم = حجم
		result.اگلا = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(یادداشتchunkحجم) + uintptr(diff)), diff
}
func (self *Tیادداشتmanager) Fخالی(پؤائنٹر_2 Pointer) {
	var chunk *Tیادداشتchunk = (*Tیادداشتchunk)(Pointer(uintptr(پؤائنٹر_2) - uintptr(یادداشتchunkحجم)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.اگلا = chunk.اگلا
		chunk.previous.حجم += chunk.حجم + یادداشتchunkحجم
		if chunk.اگلا != nil {
			chunk.اگلا.previous = chunk.previous
		}
	}

	if chunk.اگلا != nil && !chunk.اگلا.allocated {
		chunk.حجم += chunk.اگلا.حجم + یادداشتchunkحجم
		chunk.اگلا = chunk.اگلا.اگلا
		if chunk.اگلا != nil {
			chunk.اگلا.previous = chunk
		}
	}
}
func Nنیا(حجم int) Pointer {
	if Aفعالیادداشتmanager == nil {
		return nil
	}
	return Aفعالیادداشتmanager.Malloc(uint32(حجم))
}
func Dحذفکریں(پؤائنٹر_2 Pointer) {
	if Aفعالیادداشتmanager != nil {
		Aفعالیادداشتmanager.Fخالی(پؤائنٹر_2)
	}
}
