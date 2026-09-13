package memorymananger

import . "unsafe"

const Maxqueueზომა uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type Tმეხსიერებაchunk struct {
	შემდეგი		*Tმეხსიერებაchunk
	previous	*Tმეხსიერებაchunk
	allocated	bool

	ზომა	uint32
}

type Tმეხსიერებაmanager struct {
}

var first *Tმეხსიერებაchunk
var Aაქტიურიმეხსიერებაmanager *Tმეხსიერებაmanager = nil
var მეხსიერებაchunkზომა uint32

func (self *Tმეხსიერებაmanager) Init(start uint32, ზომა uint32) {

	Aაქტიურიმეხსიერებაmanager = self

	მეხსიერებაchunkზომა = uint32(Sizeof(Tმეხსიერებაchunk{}))

	if ზომა < მეხსიერებაchunkზომა {
		first = nil
	} else {
		first = (*Tმეხსიერებაchunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.შემდეგი = nil
		first.ზომა = ზომა - მეხსიერებაchunkზომა
	}
}
func (self *Tმეხსიერებაmanager) Destroy() {
	if Aაქტიურიმეხსიერებაmanager == self {
		Aაქტიურიმეხსიერებაmanager = nil
	}
}
func (self *Tმეხსიერებაmanager) Malloc(ზომა uint32) Pointer {
	var result *Tმეხსიერებაchunk = nil

	var chunk *Tმეხსიერებაchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.შემდეგი {
		if chunk.ზომა > ზომა && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.ზომა >= (ზომა + მეხსიერებაchunkზომა + 1) {

		var temporary *Tმეხსიერებაchunk
		temporary = (*Tმეხსიერებაchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + მეხსიერებაchunkზომა + ზომა)))

		temporary.allocated = false
		temporary.ზომა = result.ზომა - ზომა - მეხსიერებაchunkზომა
		temporary.previous = result
		temporary.შემდეგი = result.შემდეგი

		if temporary.შემდეგი != nil {
			temporary.შემდეგი.previous = temporary
		}

		result.ზომა = ზომა
		result.შემდეგი = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(მეხსიერებაchunkზომა))
}
func (self *Tმეხსიერებაmanager) Alignedmalloc(ზომა uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if ზომა == 0 || ზომა > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *Tმეხსიერებაchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.შემდეგი {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(მეხსიერებაchunkზომა))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.ზომა && ზომა <= chunk.ზომა-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	ზომა += diff
	if result.ზომა-ზომა >= მეხსიერებაchunkზომა+1 {
		temporary := (*Tმეხსიერებაchunk)(Pointer(uintptr(Pointer(result)) + uintptr(მეხსიერებაchunkზომა) + uintptr(ზომა)))
		temporary.allocated = false
		temporary.ზომა = result.ზომა - ზომა - მეხსიერებაchunkზომა
		temporary.previous = result
		temporary.შემდეგი = result.შემდეგი
		if temporary.შემდეგი != nil {
			temporary.შემდეგი.previous = temporary
		}
		result.ზომა = ზომა
		result.შემდეგი = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(მეხსიერებაchunkზომა) + uintptr(diff)), diff
}
func (self *Tმეხსიერებაmanager) Fთავისუფალი(კურსორი_2 Pointer) {
	var chunk *Tმეხსიერებაchunk = (*Tმეხსიერებაchunk)(Pointer(uintptr(კურსორი_2) - uintptr(მეხსიერებაchunkზომა)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.შემდეგი = chunk.შემდეგი
		chunk.previous.ზომა += chunk.ზომა + მეხსიერებაchunkზომა
		if chunk.შემდეგი != nil {
			chunk.შემდეგი.previous = chunk.previous
		}
	}

	if chunk.შემდეგი != nil && !chunk.შემდეგი.allocated {
		chunk.ზომა += chunk.შემდეგი.ზომა + მეხსიერებაchunkზომა
		chunk.შემდეგი = chunk.შემდეგი.შემდეგი
		if chunk.შემდეგი != nil {
			chunk.შემდეგი.previous = chunk
		}
	}
}
func Nახალი(ზომა int) Pointer {
	if Aაქტიურიმეხსიერებაmanager == nil {
		return nil
	}
	return Aაქტიურიმეხსიერებაmanager.Malloc(uint32(ზომა))
}
func Dწაშლა(კურსორი_2 Pointer) {
	if Aაქტიურიმეხსიერებაmanager != nil {
		Aაქტიურიმეხსიერებაmanager.Fთავისუფალი(კურსორი_2)
	}
}
