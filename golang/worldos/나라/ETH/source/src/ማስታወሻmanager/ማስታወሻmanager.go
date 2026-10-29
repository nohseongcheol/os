/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const Maxqueueመጠን uint32 = 0x1FFFFFF
const Queueማስጀመሪያaddress uint32 = 0x1000000

type Tማስታወሻchunk struct {
	የሚቀጥለው		*Tማስታወሻchunk
	previous	*Tማስታወሻchunk
	allocated	bool

	መጠን	uint32
}

type Tማስታወሻmanager struct {
}

var first *Tማስታወሻchunk
var Aአሰራማስታወሻmanager *Tማስታወሻmanager = nil
var ማስታወሻchunkመጠን uint32

func (self *Tማስታወሻmanager) Init(ማስጀመሪያ uint32, መጠን uint32) {

	Aአሰራማስታወሻmanager = self

	ማስታወሻchunkመጠን = uint32(Sizeof(Tማስታወሻchunk{}))

	if መጠን < ማስታወሻchunkመጠን {
		first = nil
	} else {
		first = (*Tማስታወሻchunk)(Pointer(uintptr(Queueማስጀመሪያaddress) + uintptr(ማስጀመሪያ)))
		first.allocated = false
		first.previous = nil
		first.የሚቀጥለው = nil
		first.መጠን = መጠን - ማስታወሻchunkመጠን
	}
}
func (self *Tማስታወሻmanager) Dአጥፋ() {
	if Aአሰራማስታወሻmanager == self {
		Aአሰራማስታወሻmanager = nil
	}
}
func (self *Tማስታወሻmanager) Malloc(መጠን uint32) Pointer {
	var result *Tማስታወሻchunk = nil

	var chunk *Tማስታወሻchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.የሚቀጥለው {
		if chunk.መጠን > መጠን && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.መጠን >= (መጠን + ማስታወሻchunkመጠን + 1) {

		var temporary *Tማስታወሻchunk
		temporary = (*Tማስታወሻchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + ማስታወሻchunkመጠን + መጠን)))

		temporary.allocated = false
		temporary.መጠን = result.መጠን - መጠን - ማስታወሻchunkመጠን
		temporary.previous = result
		temporary.የሚቀጥለው = result.የሚቀጥለው

		if temporary.የሚቀጥለው != nil {
			temporary.የሚቀጥለው.previous = temporary
		}

		result.መጠን = መጠን
		result.የሚቀጥለው = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(ማስታወሻchunkመጠን))
}
func (self *Tማስታወሻmanager) Alignedmalloc(መጠን uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if መጠን == 0 || መጠን > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *Tማስታወሻchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.የሚቀጥለው {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(ማስታወሻchunkመጠን))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.መጠን && መጠን <= chunk.መጠን-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	መጠን += diff
	if result.መጠን-መጠን >= ማስታወሻchunkመጠን+1 {
		temporary := (*Tማስታወሻchunk)(Pointer(uintptr(Pointer(result)) + uintptr(ማስታወሻchunkመጠን) + uintptr(መጠን)))
		temporary.allocated = false
		temporary.መጠን = result.መጠን - መጠን - ማስታወሻchunkመጠን
		temporary.previous = result
		temporary.የሚቀጥለው = result.የሚቀጥለው
		if temporary.የሚቀጥለው != nil {
			temporary.የሚቀጥለው.previous = temporary
		}
		result.መጠን = መጠን
		result.የሚቀጥለው = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(ማስታወሻchunkመጠን) + uintptr(diff)), diff
}
func (self *Tማስታወሻmanager) Fነፃ(ጠቋሚ_2 Pointer) {
	var chunk *Tማስታወሻchunk = (*Tማስታወሻchunk)(Pointer(uintptr(ጠቋሚ_2) - uintptr(ማስታወሻchunkመጠን)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.የሚቀጥለው = chunk.የሚቀጥለው
		chunk.previous.መጠን += chunk.መጠን + ማስታወሻchunkመጠን
		if chunk.የሚቀጥለው != nil {
			chunk.የሚቀጥለው.previous = chunk.previous
		}
	}

	if chunk.የሚቀጥለው != nil && !chunk.የሚቀጥለው.allocated {
		chunk.መጠን += chunk.የሚቀጥለው.መጠን + ማስታወሻchunkመጠን
		chunk.የሚቀጥለው = chunk.የሚቀጥለው.የሚቀጥለው
		if chunk.የሚቀጥለው != nil {
			chunk.የሚቀጥለው.previous = chunk
		}
	}
}
func Nአዲስ(መጠን int) Pointer {
	if Aአሰራማስታወሻmanager == nil {
		return nil
	}
	return Aአሰራማስታወሻmanager.Malloc(uint32(መጠን))
}
func Dማጥፊያ(ጠቋሚ_2 Pointer) {
	if Aአሰራማስታወሻmanager != nil {
		Aአሰራማስታወሻmanager.Fነፃ(ጠቋሚ_2)
	}
}
