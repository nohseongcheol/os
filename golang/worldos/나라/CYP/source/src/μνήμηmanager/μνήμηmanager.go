/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const ΜεγqueueΜέγεθος uint32 = 0x1FFFFFF
const QueueΈναρξηaddress uint32 = 0x1000000

type TΜνήμηchunk struct {
	επόμενο		*TΜνήμηchunk
	previous	*TΜνήμηchunk
	allocated	bool

	μέγεθος	uint32
}

type TΜνήμηmanager struct {
}

var first *TΜνήμηchunk
var ΕνεργόΜνήμηmanager *TΜνήμηmanager = nil
var μνήμηchunkΜέγεθος uint32

func (self *TΜνήμηmanager) Init(έναρξη uint32, μέγεθος uint32) {

	ΕνεργόΜνήμηmanager = self

	μνήμηchunkΜέγεθος = uint32(Sizeof(TΜνήμηchunk{}))

	if μέγεθος < μνήμηchunkΜέγεθος {
		first = nil
	} else {
		first = (*TΜνήμηchunk)(Pointer(uintptr(QueueΈναρξηaddress) + uintptr(έναρξη)))
		first.allocated = false
		first.previous = nil
		first.επόμενο = nil
		first.μέγεθος = μέγεθος - μνήμηchunkΜέγεθος
	}
}
func (self *TΜνήμηmanager) Καταστροφή() {
	if ΕνεργόΜνήμηmanager == self {
		ΕνεργόΜνήμηmanager = nil
	}
}
func (self *TΜνήμηmanager) Malloc(μέγεθος uint32) Pointer {
	var result *TΜνήμηchunk = nil

	var chunk *TΜνήμηchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.επόμενο {
		if chunk.μέγεθος > μέγεθος && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.μέγεθος >= (μέγεθος + μνήμηchunkΜέγεθος + 1) {

		var temporary *TΜνήμηchunk
		temporary = (*TΜνήμηchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + μνήμηchunkΜέγεθος + μέγεθος)))

		temporary.allocated = false
		temporary.μέγεθος = result.μέγεθος - μέγεθος - μνήμηchunkΜέγεθος
		temporary.previous = result
		temporary.επόμενο = result.επόμενο

		if temporary.επόμενο != nil {
			temporary.επόμενο.previous = temporary
		}

		result.μέγεθος = μέγεθος
		result.επόμενο = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(μνήμηchunkΜέγεθος))
}
func (self *TΜνήμηmanager) Alignedmalloc(μέγεθος uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if μέγεθος == 0 || μέγεθος > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TΜνήμηchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.επόμενο {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(μνήμηchunkΜέγεθος))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.μέγεθος && μέγεθος <= chunk.μέγεθος-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	μέγεθος += diff
	if result.μέγεθος-μέγεθος >= μνήμηchunkΜέγεθος+1 {
		temporary := (*TΜνήμηchunk)(Pointer(uintptr(Pointer(result)) + uintptr(μνήμηchunkΜέγεθος) + uintptr(μέγεθος)))
		temporary.allocated = false
		temporary.μέγεθος = result.μέγεθος - μέγεθος - μνήμηchunkΜέγεθος
		temporary.previous = result
		temporary.επόμενο = result.επόμενο
		if temporary.επόμενο != nil {
			temporary.επόμενο.previous = temporary
		}
		result.μέγεθος = μέγεθος
		result.επόμενο = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(μνήμηchunkΜέγεθος) + uintptr(diff)), diff
}
func (self *TΜνήμηmanager) Ελεύθερα(δείκτης_2 Pointer) {
	var chunk *TΜνήμηchunk = (*TΜνήμηchunk)(Pointer(uintptr(δείκτης_2) - uintptr(μνήμηchunkΜέγεθος)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.επόμενο = chunk.επόμενο
		chunk.previous.μέγεθος += chunk.μέγεθος + μνήμηchunkΜέγεθος
		if chunk.επόμενο != nil {
			chunk.επόμενο.previous = chunk.previous
		}
	}

	if chunk.επόμενο != nil && !chunk.επόμενο.allocated {
		chunk.μέγεθος += chunk.επόμενο.μέγεθος + μνήμηchunkΜέγεθος
		chunk.επόμενο = chunk.επόμενο.επόμενο
		if chunk.επόμενο != nil {
			chunk.επόμενο.previous = chunk
		}
	}
}
func Νέο(μέγεθος int) Pointer {
	if ΕνεργόΜνήμηmanager == nil {
		return nil
	}
	return ΕνεργόΜνήμηmanager.Malloc(uint32(μέγεθος))
}
func Διαγραφή(δείκτης_2 Pointer) {
	if ΕνεργόΜνήμηmanager != nil {
		ΕνεργόΜνήμηmanager.Ελεύθερα(δείκτης_2)
	}
}
