package memorymananger

import . "unsafe"

const MaxqueueПамер uint32 = 0x1FFFFFF
const QueueУключыцьaddress uint32 = 0x1000000

type TПамяцьchunk struct {
	наступны	*TПамяцьchunk
	previous	*TПамяцьchunk
	allocated	bool

	памер	uint32
}

type TПамяцьmanager struct {
}

var first *TПамяцьchunk
var АктыўнаПамяцьmanager *TПамяцьmanager = nil
var памяцьchunkПамер uint32

func (self *TПамяцьmanager) Init(уключыць uint32, памер uint32) {

	АктыўнаПамяцьmanager = self

	памяцьchunkПамер = uint32(Sizeof(TПамяцьchunk{}))

	if памер < памяцьchunkПамер {
		first = nil
	} else {
		first = (*TПамяцьchunk)(Pointer(uintptr(QueueУключыцьaddress) + uintptr(уключыць)))
		first.allocated = false
		first.previous = nil
		first.наступны = nil
		first.памер = памер - памяцьchunkПамер
	}
}
func (self *TПамяцьmanager) Зьнішчыць() {
	if АктыўнаПамяцьmanager == self {
		АктыўнаПамяцьmanager = nil
	}
}
func (self *TПамяцьmanager) Malloc(памер uint32) Pointer {
	var result *TПамяцьchunk = nil

	var chunk *TПамяцьchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.наступны {
		if chunk.памер > памер && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.памер >= (памер + памяцьchunkПамер + 1) {

		var temporary *TПамяцьchunk
		temporary = (*TПамяцьchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + памяцьchunkПамер + памер)))

		temporary.allocated = false
		temporary.памер = result.памер - памер - памяцьchunkПамер
		temporary.previous = result
		temporary.наступны = result.наступны

		if temporary.наступны != nil {
			temporary.наступны.previous = temporary
		}

		result.памер = памер
		result.наступны = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(памяцьchunkПамер))
}
func (self *TПамяцьmanager) Alignedmalloc(памер uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if памер == 0 || памер > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TПамяцьchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.наступны {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(памяцьchunkПамер))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.памер && памер <= chunk.памер-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	памер += diff
	if result.памер-памер >= памяцьchunkПамер+1 {
		temporary := (*TПамяцьchunk)(Pointer(uintptr(Pointer(result)) + uintptr(памяцьchunkПамер) + uintptr(памер)))
		temporary.allocated = false
		temporary.памер = result.памер - памер - памяцьchunkПамер
		temporary.previous = result
		temporary.наступны = result.наступны
		if temporary.наступны != nil {
			temporary.наступны.previous = temporary
		}
		result.памер = памер
		result.наступны = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(памяцьchunkПамер) + uintptr(diff)), diff
}
func (self *TПамяцьmanager) Вольна(паказальнік_2 Pointer) {
	var chunk *TПамяцьchunk = (*TПамяцьchunk)(Pointer(uintptr(паказальнік_2) - uintptr(памяцьchunkПамер)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.наступны = chunk.наступны
		chunk.previous.памер += chunk.памер + памяцьchunkПамер
		if chunk.наступны != nil {
			chunk.наступны.previous = chunk.previous
		}
	}

	if chunk.наступны != nil && !chunk.наступны.allocated {
		chunk.памер += chunk.наступны.памер + памяцьchunkПамер
		chunk.наступны = chunk.наступны.наступны
		if chunk.наступны != nil {
			chunk.наступны.previous = chunk
		}
	}
}
func Новы(памер int) Pointer {
	if АктыўнаПамяцьmanager == nil {
		return nil
	}
	return АктыўнаПамяцьmanager.Malloc(uint32(памер))
}
func Выдаліць(паказальнік_2 Pointer) {
	if АктыўнаПамяцьmanager != nil {
		АктыўнаПамяцьmanager.Вольна(паказальнік_2)
	}
}
