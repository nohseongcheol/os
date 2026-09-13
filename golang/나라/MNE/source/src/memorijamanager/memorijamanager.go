package memorymananger

import . "unsafe"

const МаксqueueВеличина uint32 = 0x1FFFFFF
const QueuePokreniaddress uint32 = 0x1000000

type TMemorijachunk struct {
	следеће		*TMemorijachunk
	previous	*TMemorijachunk
	allocated	bool

	величина	uint32
}

type TMemorijamanager struct {
}

var first *TMemorijachunk
var AktivnaMemorijamanager *TMemorijamanager = nil
var memorijachunkВеличина uint32

func (isti *TMemorijamanager) Init(pokreni uint32, величина uint32) {

	AktivnaMemorijamanager = isti

	memorijachunkВеличина = uint32(Sizeof(TMemorijachunk{}))

	if величина < memorijachunkВеличина {
		first = nil
	} else {
		first = (*TMemorijachunk)(Pointer(uintptr(QueuePokreniaddress) + uintptr(pokreni)))
		first.allocated = false
		first.previous = nil
		first.следеће = nil
		first.величина = величина - memorijachunkВеличина
	}
}
func (isti *TMemorijamanager) Уништи() {
	if AktivnaMemorijamanager == isti {
		AktivnaMemorijamanager = nil
	}
}
func (isti *TMemorijamanager) Malloc(величина uint32) Pointer {
	var иСХОД *TMemorijachunk = nil

	var chunk *TMemorijachunk = first
	for ; chunk != nil && иСХОД == nil; chunk = chunk.следеће {
		if chunk.величина > величина && !chunk.allocated {
			иСХОД = chunk
		}
	}

	if иСХОД == nil {
		return nil
	}

	if иСХОД.величина >= (величина + memorijachunkВеличина + 1) {

		var temporary *TMemorijachunk
		temporary = (*TMemorijachunk)(Pointer(uintptr(uint32(uintptr(Pointer(иСХОД))) + memorijachunkВеличина + величина)))

		temporary.allocated = false
		temporary.величина = иСХОД.величина - величина - memorijachunkВеличина
		temporary.previous = иСХОД
		temporary.следеће = иСХОД.следеће

		if temporary.следеће != nil {
			temporary.следеће.previous = temporary
		}

		иСХОД.величина = величина
		иСХОД.следеће = temporary
	}
	иСХОД.allocated = true

	return Pointer(uintptr(Pointer(иСХОД)) + uintptr(memorijachunkВеличина))
}
func (isti *TMemorijamanager) Alignedmalloc(величина uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if величина == 0 || величина > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var иСХОД *TMemorijachunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.следеће {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(memorijachunkВеличина))
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
	if иСХОД.величина-величина >= memorijachunkВеличина+1 {
		temporary := (*TMemorijachunk)(Pointer(uintptr(Pointer(иСХОД)) + uintptr(memorijachunkВеличина) + uintptr(величина)))
		temporary.allocated = false
		temporary.величина = иСХОД.величина - величина - memorijachunkВеличина
		temporary.previous = иСХОД
		temporary.следеће = иСХОД.следеће
		if temporary.следеће != nil {
			temporary.следеће.previous = temporary
		}
		иСХОД.величина = величина
		иСХОД.следеће = temporary
	}
	иСХОД.allocated = true
	return Pointer(uintptr(Pointer(иСХОД)) + uintptr(memorijachunkВеличина) + uintptr(diff)), diff
}
func (isti *TMemorijamanager) Slobodno(pokazivač_2 Pointer) {
	var chunk *TMemorijachunk = (*TMemorijachunk)(Pointer(uintptr(pokazivač_2) - uintptr(memorijachunkВеличина)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.следеће = chunk.следеће
		chunk.previous.величина += chunk.величина + memorijachunkВеличина
		if chunk.следеће != nil {
			chunk.следеће.previous = chunk.previous
		}
	}

	if chunk.следеће != nil && !chunk.следеће.allocated {
		chunk.величина += chunk.следеће.величина + memorijachunkВеличина
		chunk.следеће = chunk.следеће.следеће
		if chunk.следеће != nil {
			chunk.следеће.previous = chunk
		}
	}
}
func Нова(величина int) Pointer {
	if AktivnaMemorijamanager == nil {
		return nil
	}
	return AktivnaMemorijamanager.Malloc(uint32(величина))
}
func Обриши(pokazivač_2 Pointer) {
	if AktivnaMemorijamanager != nil {
		AktivnaMemorijamanager.Slobodno(pokazivač_2)
	}
}
