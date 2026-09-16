/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const Mأقصىطابورالحجم uint32 = 0x1FFFFFF
const Qطابورابدأaddress uint32 = 0x1000000

type Tذاكرةchunk struct {
	التالي		*Tذاكرةchunk
	previous	*Tذاكرةchunk
	allocated	bool

	الحجم	uint32
}

type Tذاكرةمدير struct {
}

var first *Tذاكرةchunk
var Aنشطذاكرةمدير *Tذاكرةمدير = nil
var ذاكرةchunkالحجم uint32

func (نفسه *Tذاكرةمدير) Init(ابدأ uint32, الحجم uint32) {

	Aنشطذاكرةمدير = نفسه

	ذاكرةchunkالحجم = uint32(Sizeof(Tذاكرةchunk{}))

	if الحجم < ذاكرةchunkالحجم {
		first = nil
	} else {
		first = (*Tذاكرةchunk)(Pointer(uintptr(Qطابورابدأaddress) + uintptr(ابدأ)))
		first.allocated = false
		first.previous = nil
		first.التالي = nil
		first.الحجم = الحجم - ذاكرةchunkالحجم
	}
}
func (نفسه *Tذاكرةمدير) Destroy() {
	if Aنشطذاكرةمدير == نفسه {
		Aنشطذاكرةمدير = nil
	}
}
func (نفسه *Tذاكرةمدير) Mتخصيص_الذاكرة(الحجم uint32) Pointer {
	var result *Tذاكرةchunk = nil

	var chunk *Tذاكرةchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.التالي {
		if chunk.الحجم > الحجم && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.الحجم >= (الحجم + ذاكرةchunkالحجم + 1) {

		var temporary *Tذاكرةchunk
		temporary = (*Tذاكرةchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + ذاكرةchunkالحجم + الحجم)))

		temporary.allocated = false
		temporary.الحجم = result.الحجم - الحجم - ذاكرةchunkالحجم
		temporary.previous = result
		temporary.التالي = result.التالي

		if temporary.التالي != nil {
			temporary.التالي.previous = temporary
		}

		result.الحجم = الحجم
		result.التالي = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(ذاكرةchunkالحجم))
}
func (نفسه *Tذاكرةمدير) Alignedmalloc(الحجم uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if الحجم == 0 || الحجم > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *Tذاكرةchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.التالي {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(ذاكرةchunkالحجم))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.الحجم && الحجم <= chunk.الحجم-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	الحجم += diff
	if result.الحجم-الحجم >= ذاكرةchunkالحجم+1 {
		temporary := (*Tذاكرةchunk)(Pointer(uintptr(Pointer(result)) + uintptr(ذاكرةchunkالحجم) + uintptr(الحجم)))
		temporary.allocated = false
		temporary.الحجم = result.الحجم - الحجم - ذاكرةchunkالحجم
		temporary.previous = result
		temporary.التالي = result.التالي
		if temporary.التالي != nil {
			temporary.التالي.previous = temporary
		}
		result.الحجم = الحجم
		result.التالي = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(ذاكرةchunkالحجم) + uintptr(diff)), diff
}
func (نفسه *Tذاكرةمدير) Fخالي(مرجع_عنوان_2 Pointer) {
	var chunk *Tذاكرةchunk = (*Tذاكرةchunk)(Pointer(uintptr(مرجع_عنوان_2) - uintptr(ذاكرةchunkالحجم)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.التالي = chunk.التالي
		chunk.previous.الحجم += chunk.الحجم + ذاكرةchunkالحجم
		if chunk.التالي != nil {
			chunk.التالي.previous = chunk.previous
		}
	}

	if chunk.التالي != nil && !chunk.التالي.allocated {
		chunk.الحجم += chunk.التالي.الحجم + ذاكرةchunkالحجم
		chunk.التالي = chunk.التالي.التالي
		if chunk.التالي != nil {
			chunk.التالي.previous = chunk
		}
	}
}
func Nجديد(الحجم int) Pointer {
	if Aنشطذاكرةمدير == nil {
		return nil
	}
	return Aنشطذاكرةمدير.Mتخصيص_الذاكرة(uint32(الحجم))
}
func Dحذف(مرجع_عنوان_2 Pointer) {
	if Aنشطذاكرةمدير != nil {
		Aنشطذاكرةمدير.Fخالي(مرجع_عنوان_2)
	}
}
