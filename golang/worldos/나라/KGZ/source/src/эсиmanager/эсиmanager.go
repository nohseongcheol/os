/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueӨлчөм uint32 = 0x1FFFFFF
const QueueЖүргүзүүaddress uint32 = 0x1000000

type TЭсиchunk struct {
	кийинки		*TЭсиchunk
	previous	*TЭсиchunk
	allocated	bool

	өлчөм	uint32
}

type TЭсиmanager struct {
}

var first *TЭсиchunk
var АктивдүүЭсиmanager *TЭсиmanager = nil
var эсиchunkӨлчөм uint32

func (self *TЭсиmanager) Init(жүргүзүү uint32, өлчөм uint32) {

	АктивдүүЭсиmanager = self

	эсиchunkӨлчөм = uint32(Sizeof(TЭсиchunk{}))

	if өлчөм < эсиchunkӨлчөм {
		first = nil
	} else {
		first = (*TЭсиchunk)(Pointer(uintptr(QueueЖүргүзүүaddress) + uintptr(жүргүзүү)))
		first.allocated = false
		first.previous = nil
		first.кийинки = nil
		first.өлчөм = өлчөм - эсиchunkӨлчөм
	}
}
func (self *TЭсиmanager) Destroy() {
	if АктивдүүЭсиmanager == self {
		АктивдүүЭсиmanager = nil
	}
}
func (self *TЭсиmanager) Malloc(өлчөм uint32) Pointer {
	var result *TЭсиchunk = nil

	var chunk *TЭсиchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.кийинки {
		if chunk.өлчөм > өлчөм && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.өлчөм >= (өлчөм + эсиchunkӨлчөм + 1) {

		var temporary *TЭсиchunk
		temporary = (*TЭсиchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + эсиchunkӨлчөм + өлчөм)))

		temporary.allocated = false
		temporary.өлчөм = result.өлчөм - өлчөм - эсиchunkӨлчөм
		temporary.previous = result
		temporary.кийинки = result.кийинки

		if temporary.кийинки != nil {
			temporary.кийинки.previous = temporary
		}

		result.өлчөм = өлчөм
		result.кийинки = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(эсиchunkӨлчөм))
}
func (self *TЭсиmanager) Alignedmalloc(өлчөм uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if өлчөм == 0 || өлчөм > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TЭсиchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.кийинки {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(эсиchunkӨлчөм))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.өлчөм && өлчөм <= chunk.өлчөм-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	өлчөм += diff
	if result.өлчөм-өлчөм >= эсиchunkӨлчөм+1 {
		temporary := (*TЭсиchunk)(Pointer(uintptr(Pointer(result)) + uintptr(эсиchunkӨлчөм) + uintptr(өлчөм)))
		temporary.allocated = false
		temporary.өлчөм = result.өлчөм - өлчөм - эсиchunkӨлчөм
		temporary.previous = result
		temporary.кийинки = result.кийинки
		if temporary.кийинки != nil {
			temporary.кийинки.previous = temporary
		}
		result.өлчөм = өлчөм
		result.кийинки = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(эсиchunkӨлчөм) + uintptr(diff)), diff
}
func (self *TЭсиmanager) Бош(көрсөткүч_2 Pointer) {
	var chunk *TЭсиchunk = (*TЭсиchunk)(Pointer(uintptr(көрсөткүч_2) - uintptr(эсиchunkӨлчөм)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.кийинки = chunk.кийинки
		chunk.previous.өлчөм += chunk.өлчөм + эсиchunkӨлчөм
		if chunk.кийинки != nil {
			chunk.кийинки.previous = chunk.previous
		}
	}

	if chunk.кийинки != nil && !chunk.кийинки.allocated {
		chunk.өлчөм += chunk.кийинки.өлчөм + эсиchunkӨлчөм
		chunk.кийинки = chunk.кийинки.кийинки
		if chunk.кийинки != nil {
			chunk.кийинки.previous = chunk
		}
	}
}
func Жаңы(өлчөм int) Pointer {
	if АктивдүүЭсиmanager == nil {
		return nil
	}
	return АктивдүүЭсиmanager.Malloc(uint32(өлчөм))
}
func Өчүрүү(көрсөткүч_2 Pointer) {
	if АктивдүүЭсиmanager != nil {
		АктивдүүЭсиmanager.Бош(көрсөткүч_2)
	}
}
