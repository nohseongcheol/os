package memorymananger

import . "unsafe"

const MaxqueueBöyüklük uint32 = 0x1FFFFFF
const Queuestartaddress uint32 = 0x1000000

type TYaddaşchunk struct {
	sonrakı		*TYaddaşchunk
	previous	*TYaddaşchunk
	allocated	bool

	böyüklük	uint32
}

type TYaddaşmanager struct {
}

var first *TYaddaşchunk
var FəalYaddaşmanager *TYaddaşmanager = nil
var yaddaşchunkBöyüklük uint32

func (self *TYaddaşmanager) Init(start uint32, böyüklük uint32) {

	FəalYaddaşmanager = self

	yaddaşchunkBöyüklük = uint32(Sizeof(TYaddaşchunk{}))

	if böyüklük < yaddaşchunkBöyüklük {
		first = nil
	} else {
		first = (*TYaddaşchunk)(Pointer(uintptr(Queuestartaddress) + uintptr(start)))
		first.allocated = false
		first.previous = nil
		first.sonrakı = nil
		first.böyüklük = böyüklük - yaddaşchunkBöyüklük
	}
}
func (self *TYaddaşmanager) Destroy() {
	if FəalYaddaşmanager == self {
		FəalYaddaşmanager = nil
	}
}
func (self *TYaddaşmanager) Malloc(böyüklük uint32) Pointer {
	var result *TYaddaşchunk = nil

	var chunk *TYaddaşchunk = first
	for ; chunk != nil && result == nil; chunk = chunk.sonrakı {
		if chunk.böyüklük > böyüklük && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.böyüklük >= (böyüklük + yaddaşchunkBöyüklük + 1) {

		var temporary *TYaddaşchunk
		temporary = (*TYaddaşchunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + yaddaşchunkBöyüklük + böyüklük)))

		temporary.allocated = false
		temporary.böyüklük = result.böyüklük - böyüklük - yaddaşchunkBöyüklük
		temporary.previous = result
		temporary.sonrakı = result.sonrakı

		if temporary.sonrakı != nil {
			temporary.sonrakı.previous = temporary
		}

		result.böyüklük = böyüklük
		result.sonrakı = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(yaddaşchunkBöyüklük))
}
func (self *TYaddaşmanager) Alignedmalloc(böyüklük uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if böyüklük == 0 || böyüklük > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TYaddaşchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.sonrakı {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(yaddaşchunkBöyüklük))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.böyüklük && böyüklük <= chunk.böyüklük-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	böyüklük += diff
	if result.böyüklük-böyüklük >= yaddaşchunkBöyüklük+1 {
		temporary := (*TYaddaşchunk)(Pointer(uintptr(Pointer(result)) + uintptr(yaddaşchunkBöyüklük) + uintptr(böyüklük)))
		temporary.allocated = false
		temporary.böyüklük = result.böyüklük - böyüklük - yaddaşchunkBöyüklük
		temporary.previous = result
		temporary.sonrakı = result.sonrakı
		if temporary.sonrakı != nil {
			temporary.sonrakı.previous = temporary
		}
		result.böyüklük = böyüklük
		result.sonrakı = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(yaddaşchunkBöyüklük) + uintptr(diff)), diff
}
func (self *TYaddaşmanager) Boş(pointer_2 Pointer) {
	var chunk *TYaddaşchunk = (*TYaddaşchunk)(Pointer(uintptr(pointer_2) - uintptr(yaddaşchunkBöyüklük)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.sonrakı = chunk.sonrakı
		chunk.previous.böyüklük += chunk.böyüklük + yaddaşchunkBöyüklük
		if chunk.sonrakı != nil {
			chunk.sonrakı.previous = chunk.previous
		}
	}

	if chunk.sonrakı != nil && !chunk.sonrakı.allocated {
		chunk.böyüklük += chunk.sonrakı.böyüklük + yaddaşchunkBöyüklük
		chunk.sonrakı = chunk.sonrakı.sonrakı
		if chunk.sonrakı != nil {
			chunk.sonrakı.previous = chunk
		}
	}
}
func Yeni(böyüklük int) Pointer {
	if FəalYaddaşmanager == nil {
		return nil
	}
	return FəalYaddaşmanager.Malloc(uint32(böyüklük))
}
func Sil(pointer_2 Pointer) {
	if FəalYaddaşmanager != nil {
		FəalYaddaşmanager.Boş(pointer_2)
	}
}
