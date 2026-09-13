package memorymananger

import . "unsafe"

const MaxqueueГолемина uint32 = 0x1FFFFFF
const QueueПуштиaddress uint32 = 0x1000000

type TМеморијаchunk struct {
	следна		*TМеморијаchunk
	previous	*TМеморијаchunk
	allocated	bool

	големина	uint32
}

type TМеморијаmanager struct {
}

var first *TМеморијаchunk
var АктивноМеморијаmanager *TМеморијаmanager = nil
var меморијаchunkГолемина uint32

func (само *TМеморијаmanager) Init(пушти uint32, големина uint32) {

	АктивноМеморијаmanager = само

	меморијаchunkГолемина = uint32(Sizeof(TМеморијаchunk{}))

	if големина < меморијаchunkГолемина {
		first = nil
	} else {
		first = (*TМеморијаchunk)(Pointer(uintptr(QueueПуштиaddress) + uintptr(пушти)))
		first.allocated = false
		first.previous = nil
		first.следна = nil
		first.големина = големина - меморијаchunkГолемина
	}
}
func (само *TМеморијаmanager) Destroy() {
	if АктивноМеморијаmanager == само {
		АктивноМеморијаmanager = nil
	}
}
func (само *TМеморијаmanager) Malloc(големина uint32) Pointer {
	var result *TМеморијаchunk = nil

	var chunk *TМеморијаchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.следна {
		if chunk.големина > големина && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.големина >= (големина + меморијаchunkГолемина + 1) {

		var temporary *TМеморијаchunk
		temporary = (*TМеморијаchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + меморијаchunkГолемина + големина)))

		temporary.allocated = false
		temporary.големина = result.големина - големина - меморијаchunkГолемина
		temporary.previous = result
		temporary.следна = result.следна

		if temporary.следна != nil {
			temporary.следна.previous = temporary
		}

		result.големина = големина
		result.следна = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(меморијаchunkГолемина))
}
func (само *TМеморијаmanager) Alignedmalloc(големина uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if големина == 0 || големина > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TМеморијаchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.следна {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(меморијаchunkГолемина))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.големина && големина <= chunk.големина-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	големина += diff
	if result.големина-големина >= меморијаchunkГолемина+1 {
		temporary := (*TМеморијаchunk)(Pointer(uintptr(Pointer(result)) + uintptr(меморијаchunkГолемина) + uintptr(големина)))
		temporary.allocated = false
		temporary.големина = result.големина - големина - меморијаchunkГолемина
		temporary.previous = result
		temporary.следна = result.следна
		if temporary.следна != nil {
			temporary.следна.previous = temporary
		}
		result.големина = големина
		result.следна = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(меморијаchunkГолемина) + uintptr(diff)), diff
}
func (само *TМеморијаmanager) Слободни(стрелка_2 Pointer) {
	var chunk *TМеморијаchunk = (*TМеморијаchunk)(Pointer(uintptr(стрелка_2) - uintptr(меморијаchunkГолемина)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.следна = chunk.следна
		chunk.previous.големина += chunk.големина + меморијаchunkГолемина
		if chunk.следна != nil {
			chunk.следна.previous = chunk.previous
		}
	}

	if chunk.следна != nil && !chunk.следна.allocated {
		chunk.големина += chunk.следна.големина + меморијаchunkГолемина
		chunk.следна = chunk.следна.следна
		if chunk.следна != nil {
			chunk.следна.previous = chunk
		}
	}
}
func Нов(големина int) Pointer {
	if АктивноМеморијаmanager == nil {
		return nil
	}
	return АктивноМеморијаmanager.Malloc(uint32(големина))
}
func Избриши(стрелка_2 Pointer) {
	if АктивноМеморијаmanager != nil {
		АктивноМеморијаmanager.Слободни(стрелка_2)
	}
}
