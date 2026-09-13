package memorymananger

import . "unsafe"

const МаксимумqueueРозмір uint32 = 0x1FFFFFF
const QueueЗапуститиАдреса uint32 = 0x1000000

type TПамятьchunk struct {
	наступне	*TПамятьchunk
	previous	*TПамятьchunk
	allocated	bool

	розмір	uint32
}

type TПамятьmanager struct {
}

var first *TПамятьchunk
var АктивнийПамятьmanager *TПамятьmanager = nil
var памятьchunkРозмір uint32

func (поточний *TПамятьmanager) Init(запустити uint32, розмір uint32) {

	АктивнийПамятьmanager = поточний

	памятьchunkРозмір = uint32(Sizeof(TПамятьchunk{}))

	if розмір < памятьchunkРозмір {
		first = nil
	} else {
		first = (*TПамятьchunk)(Pointer(uintptr(QueueЗапуститиАдреса) + uintptr(запустити)))
		first.allocated = false
		first.previous = nil
		first.наступне = nil
		first.розмір = розмір - памятьchunkРозмір
	}
}
func (поточний *TПамятьmanager) Знищити() {
	if АктивнийПамятьmanager == поточний {
		АктивнийПамятьmanager = nil
	}
}
func (поточний *TПамятьmanager) Виділити_памʼять(розмір uint32) Pointer {
	var яРЛИК *TПамятьchunk = nil

	var chunk *TПамятьchunk = first
	for ; chunk != nil && яРЛИК == nil; chunk = chunk.наступне {
		if chunk.розмір > розмір && !chunk.allocated {
			яРЛИК = chunk
		}
	}

	if яРЛИК == nil {
		return nil
	}

	if яРЛИК.розмір >= (розмір + памятьchunkРозмір + 1) {

		var temporary *TПамятьchunk
		temporary = (*TПамятьchunk)(Pointer(uintptr(uint32(uintptr(Pointer(яРЛИК))) + памятьchunkРозмір + розмір)))

		temporary.allocated = false
		temporary.розмір = яРЛИК.розмір - розмір - памятьchunkРозмір
		temporary.previous = яРЛИК
		temporary.наступне = яРЛИК.наступне

		if temporary.наступне != nil {
			temporary.наступне.previous = temporary
		}

		яРЛИК.розмір = розмір
		яРЛИК.наступне = temporary
	}
	яРЛИК.allocated = true

	return Pointer(uintptr(Pointer(яРЛИК)) + uintptr(памятьchunkРозмір))
}
func (поточний *TПамятьmanager) Alignedmalloc(розмір uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if розмір == 0 || розмір > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var яРЛИК *TПамятьchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.наступне {
		if chunk.allocated {
			continue
		}
		адреса := uint32(uintptr(Pointer(chunk)) + uintptr(памятьchunkРозмір))
		diff = (0x1000 - (адреса & 0xFFF)) & 0xFFF
		if адреса+diff < адреса {
			continue
		}
		if diff <= chunk.розмір && розмір <= chunk.розмір-diff {
			яРЛИК = chunk
			break
		}
	}
	if яРЛИК == nil {
		return nil, 0
	}
	розмір += diff
	if яРЛИК.розмір-розмір >= памятьchunkРозмір+1 {
		temporary := (*TПамятьchunk)(Pointer(uintptr(Pointer(яРЛИК)) + uintptr(памятьchunkРозмір) + uintptr(розмір)))
		temporary.allocated = false
		temporary.розмір = яРЛИК.розмір - розмір - памятьchunkРозмір
		temporary.previous = яРЛИК
		temporary.наступне = яРЛИК.наступне
		if temporary.наступне != nil {
			temporary.наступне.previous = temporary
		}
		яРЛИК.розмір = розмір
		яРЛИК.наступне = temporary
	}
	яРЛИК.allocated = true
	return Pointer(uintptr(Pointer(яРЛИК)) + uintptr(памятьchunkРозмір) + uintptr(diff)), diff
}
func (поточний *TПамятьmanager) Вільно(посилання_на_адресу_2 Pointer) {
	var chunk *TПамятьchunk = (*TПамятьchunk)(Pointer(uintptr(посилання_на_адресу_2) - uintptr(памятьchunkРозмір)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.наступне = chunk.наступне
		chunk.previous.розмір += chunk.розмір + памятьchunkРозмір
		if chunk.наступне != nil {
			chunk.наступне.previous = chunk.previous
		}
	}

	if chunk.наступне != nil && !chunk.наступне.allocated {
		chunk.розмір += chunk.наступне.розмір + памятьchunkРозмір
		chunk.наступне = chunk.наступне.наступне
		if chunk.наступне != nil {
			chunk.наступне.previous = chunk
		}
	}
}
func Новий(розмір int) Pointer {
	if АктивнийПамятьmanager == nil {
		return nil
	}
	return АктивнийПамятьmanager.Виділити_памʼять(uint32(розмір))
}
func Вилучити(посилання_на_адресу_2 Pointer) {
	if АктивнийПамятьmanager != nil {
		АктивнийПамятьmanager.Вільно(посилання_на_адресу_2)
	}
}
