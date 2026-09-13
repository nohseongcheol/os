package memorymananger

import . "unsafe"

const MaxqueueIngano uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TUbubikochunk struct {
	ikurikira	*TUbubikochunk
	previous	*TUbubikochunk
	allocated	bool

	ingano	uint32
}

type TUbubikomanager struct {
}

var first *TUbubikochunk
var GikoraUbubikomanager *TUbubikomanager = nil
var ububikochunkIngano uint32

func (self *TUbubikomanager) Init(start uint32, ingano uint32) {

	GikoraUbubikomanager = self

	ububikochunkIngano = uint32(Sizeof(TUbubikochunk{}))

	if ingano < ububikochunkIngano {
		first = nil
	} else {
		first = (*TUbubikochunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.ikurikira = nil
		first.ingano = ingano - ububikochunkIngano
	}
}
func (self *TUbubikomanager) Destroy() {
	if GikoraUbubikomanager == self {
		GikoraUbubikomanager = nil
	}
}
func (self *TUbubikomanager) Malloc(ingano uint32) Pointer {
	var result *TUbubikochunk = nil

	var chunk *TUbubikochunk = first
	for ; chunk != nil && result == nil; chunk = chunk.ikurikira {
		if chunk.ingano > ingano && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.ingano >= (ingano + ububikochunkIngano + 1) {

		var temporary *TUbubikochunk
		temporary = (*TUbubikochunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + ububikochunkIngano + ingano)))

		temporary.allocated = false
		temporary.ingano = result.ingano - ingano - ububikochunkIngano
		temporary.previous = result
		temporary.ikurikira = result.ikurikira

		if temporary.ikurikira != nil {
			temporary.ikurikira.previous = temporary
		}

		result.ingano = ingano
		result.ikurikira = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(ububikochunkIngano))
}
func (self *TUbubikomanager) Alignedmalloc(ingano uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if ingano == 0 || ingano > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TUbubikochunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.ikurikira {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(ububikochunkIngano))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.ingano && ingano <= chunk.ingano-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	ingano += diff
	if result.ingano-ingano >= ububikochunkIngano+1 {
		temporary := (*TUbubikochunk)(Pointer(uintptr(Pointer(result)) + uintptr(ububikochunkIngano) + uintptr(ingano)))
		temporary.allocated = false
		temporary.ingano = result.ingano - ingano - ububikochunkIngano
		temporary.previous = result
		temporary.ikurikira = result.ikurikira
		if temporary.ikurikira != nil {
			temporary.ikurikira.previous = temporary
		}
		result.ingano = ingano
		result.ikurikira = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(ububikochunkIngano) + uintptr(diff)), diff
}
func (self *TUbubikomanager) Kigenga(pointer_2 Pointer) {
	var chunk *TUbubikochunk = (*TUbubikochunk)(Pointer(uintptr(pointer_2) - uintptr(ububikochunkIngano)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.ikurikira = chunk.ikurikira
		chunk.previous.ingano += chunk.ingano + ububikochunkIngano
		if chunk.ikurikira != nil {
			chunk.ikurikira.previous = chunk.previous
		}
	}

	if chunk.ikurikira != nil && !chunk.ikurikira.allocated {
		chunk.ingano += chunk.ikurikira.ingano + ububikochunkIngano
		chunk.ikurikira = chunk.ikurikira.ikurikira
		if chunk.ikurikira != nil {
			chunk.ikurikira.previous = chunk
		}
	}
}
func New(ingano int) Pointer {
	if GikoraUbubikomanager == nil {
		return nil
	}
	return GikoraUbubikomanager.Malloc(uint32(ingano))
}
func Gusiba_2(pointer_2 Pointer) {
	if GikoraUbubikomanager != nil {
		GikoraUbubikomanager.Kigenga(pointer_2)
	}
}
