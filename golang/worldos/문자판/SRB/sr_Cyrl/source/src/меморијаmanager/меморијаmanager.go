/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const МаксqueueВеличина uint32 = 0x1FFFFFF
const QueueПокрениaddress uint32 = 0x1000000

type TМеморијаchunk struct {
	следеће		*TМеморијаchunk
	previous	*TМеморијаchunk
	allocated	bool

	величина	uint32
}

type TМеморијаmanager struct {
}

var first *TМеморијаchunk
var АктивнаМеморијаmanager *TМеморијаmanager = nil
var меморијаchunkВеличина uint32

func (исти *TМеморијаmanager) Init(покрени uint32, величина uint32) {

	АктивнаМеморијаmanager = исти

	меморијаchunkВеличина = uint32(Sizeof(TМеморијаchunk{}))

	if величина < меморијаchunkВеличина {
		first = nil
	} else {
		first = (*TМеморијаchunk)(Pointer(uintptr(QueueПокрениaddress) + uintptr(покрени)))
		first.allocated = false
		first.previous = nil
		first.следеће = nil
		first.величина = величина - меморијаchunkВеличина
	}
}
func (исти *TМеморијаmanager) Уништи() {
	if АктивнаМеморијаmanager == исти {
		АктивнаМеморијаmanager = nil
	}
}
func (исти *TМеморијаmanager) Malloc(величина uint32) Pointer {
	var иСХОД *TМеморијаchunk = nil

	var chunk *TМеморијаchunk = first
	for ; chunk != nil && иСХОД == nil; chunk = chunk.следеће {
		if chunk.величина > величина && !chunk.allocated {
			иСХОД = chunk
		}
	}

	if иСХОД == nil {
		return nil
	}

	if иСХОД.величина >= (величина + меморијаchunkВеличина + 1) {

		var temporary *TМеморијаchunk
		temporary = (*TМеморијаchunk)(Pointer(uintptr(uint32(uintptr(Pointer(иСХОД))) + меморијаchunkВеличина + величина)))

		temporary.allocated = false
		temporary.величина = иСХОД.величина - величина - меморијаchunkВеличина
		temporary.previous = иСХОД
		temporary.следеће = иСХОД.следеће

		if temporary.следеће != nil {
			temporary.следеће.previous = temporary
		}

		иСХОД.величина = величина
		иСХОД.следеће = temporary
	}
	иСХОД.allocated = true

	return Pointer(uintptr(Pointer(иСХОД)) + uintptr(меморијаchunkВеличина))
}
func (исти *TМеморијаmanager) Alignedmalloc(величина uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if величина == 0 || величина > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var иСХОД *TМеморијаchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.следеће {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(меморијаchunkВеличина))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.величина && величина <= chunk.величина-diff {
			иСХОД = chunk
			break
		}
	}
	if иСХОД == nil {
		return nil, 0
	}
	величина += diff
	if иСХОД.величина-величина >= меморијаchunkВеличина+1 {
		temporary := (*TМеморијаchunk)(Pointer(uintptr(Pointer(иСХОД)) + uintptr(меморијаchunkВеличина) + uintptr(величина)))
		temporary.allocated = false
		temporary.величина = иСХОД.величина - величина - меморијаchunkВеличина
		temporary.previous = иСХОД
		temporary.следеће = иСХОД.следеће
		if temporary.следеће != nil {
			temporary.следеће.previous = temporary
		}
		иСХОД.величина = величина
		иСХОД.следеће = temporary
	}
	иСХОД.allocated = true
	return Pointer(uintptr(Pointer(иСХОД)) + uintptr(меморијаchunkВеличина) + uintptr(diff)), diff
}
func (исти *TМеморијаmanager) Слободно(показивач_2 Pointer) {
	var chunk *TМеморијаchunk = (*TМеморијаchunk)(Pointer(uintptr(показивач_2) - uintptr(меморијаchunkВеличина)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.следеће = chunk.следеће
		chunk.previous.величина += chunk.величина + меморијаchunkВеличина
		if chunk.следеће != nil {
			chunk.следеће.previous = chunk.previous
		}
	}

	if chunk.следеће != nil && !chunk.следеће.allocated {
		chunk.величина += chunk.следеће.величина + меморијаchunkВеличина
		chunk.следеће = chunk.следеће.следеће
		if chunk.следеће != nil {
			chunk.следеће.previous = chunk
		}
	}
}
func Нова(величина int) Pointer {
	if АктивнаМеморијаmanager == nil {
		return nil
	}
	return АктивнаМеморијаmanager.Malloc(uint32(величина))
}
func Обриши(показивач_2 Pointer) {
	if АктивнаМеморијаmanager != nil {
		АктивнаМеморијаmanager.Слободно(показивач_2)
	}
}
