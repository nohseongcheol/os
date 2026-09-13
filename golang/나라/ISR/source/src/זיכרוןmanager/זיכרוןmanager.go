package memorymananger

import . "unsafe"

const Mמקסימוםqueueגודל uint32 = 0x1FFFFFF
const Queueהתחלהaddress uint32 = 0x1000000

type Tזיכרוןchunk struct {
	הבא		*Tזיכרוןchunk
	previous	*Tזיכרוןchunk
	allocated	bool

	גודל	uint32
}

type Tזיכרוןmanager struct {
}

var first *Tזיכרוןchunk
var Aפעילזיכרוןmanager *Tזיכרוןmanager = nil
var זיכרוןchunkגודל uint32

func (self *Tזיכרוןmanager) Init(התחלה uint32, גודל uint32) {

	Aפעילזיכרוןmanager = self

	זיכרוןchunkגודל = uint32(Sizeof(Tזיכרוןchunk{}))

	if גודל < זיכרוןchunkגודל {
		first = nil
	} else {
		first = (*Tזיכרוןchunk)(Pointer(uintptr(Queueהתחלהaddress) + uintptr(התחלה)))
		first.allocated = false
		first.previous = nil
		first.הבא = nil
		first.גודל = גודל - זיכרוןchunkגודל
	}
}
func (self *Tזיכרוןmanager) Dהשמד() {
	if Aפעילזיכרוןmanager == self {
		Aפעילזיכרוןmanager = nil
	}
}
func (self *Tזיכרוןmanager) Malloc(גודל uint32) Pointer {
	var result *Tזיכרוןchunk = nil

	var chunk *Tזיכרוןchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.הבא {
		if chunk.גודל > גודל && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.גודל >= (גודל + זיכרוןchunkגודל + 1) {

		var temporary *Tזיכרוןchunk
		temporary = (*Tזיכרוןchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + זיכרוןchunkגודל + גודל)))

		temporary.allocated = false
		temporary.גודל = result.גודל - גודל - זיכרוןchunkגודל
		temporary.previous = result
		temporary.הבא = result.הבא

		if temporary.הבא != nil {
			temporary.הבא.previous = temporary
		}

		result.גודל = גודל
		result.הבא = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(זיכרוןchunkגודל))
}
func (self *Tזיכרוןmanager) Alignedmalloc(גודל uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if גודל == 0 || גודל > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *Tזיכרוןchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.הבא {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(זיכרוןchunkגודל))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.גודל && גודל <= chunk.גודל-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	גודל += diff
	if result.גודל-גודל >= זיכרוןchunkגודל+1 {
		temporary := (*Tזיכרוןchunk)(Pointer(uintptr(Pointer(result)) + uintptr(זיכרוןchunkגודל) + uintptr(גודל)))
		temporary.allocated = false
		temporary.גודל = result.גודל - גודל - זיכרוןchunkגודל
		temporary.previous = result
		temporary.הבא = result.הבא
		if temporary.הבא != nil {
			temporary.הבא.previous = temporary
		}
		result.גודל = גודל
		result.הבא = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(זיכרוןchunkגודל) + uintptr(diff)), diff
}
func (self *Tזיכרוןmanager) Fפנוי(סמן_2 Pointer) {
	var chunk *Tזיכרוןchunk = (*Tזיכרוןchunk)(Pointer(uintptr(סמן_2) - uintptr(זיכרוןchunkגודל)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.הבא = chunk.הבא
		chunk.previous.גודל += chunk.גודל + זיכרוןchunkגודל
		if chunk.הבא != nil {
			chunk.הבא.previous = chunk.previous
		}
	}

	if chunk.הבא != nil && !chunk.הבא.allocated {
		chunk.גודל += chunk.הבא.גודל + זיכרוןchunkגודל
		chunk.הבא = chunk.הבא.הבא
		if chunk.הבא != nil {
			chunk.הבא.previous = chunk
		}
	}
}
func Nחדש(גודל int) Pointer {
	if Aפעילזיכרוןmanager == nil {
		return nil
	}
	return Aפעילזיכרוןmanager.Malloc(uint32(גודל))
}
func Dמחיקה(סמן_2 Pointer) {
	if Aפעילזיכרוןmanager != nil {
		Aפעילזיכרוןmanager.Fפנוי(סמן_2)
	}
}
