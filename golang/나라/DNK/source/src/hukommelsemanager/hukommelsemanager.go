package memorymananger

import . "unsafe"

const MaxqueueStørrelse uint32 = 0x1FFFFFF
const QueueBegyndaddress uint32 = 0x1000000

type THukommelsechunk struct {
	næste		*THukommelsechunk
	previous	*THukommelsechunk
	allocated	bool

	størrelse	uint32
}

type THukommelsemanager struct {
}

var first *THukommelsechunk
var AktivHukommelsemanager *THukommelsemanager = nil
var hukommelsechunkStørrelse uint32

func (selv *THukommelsemanager) Init(begynd uint32, størrelse uint32) {

	AktivHukommelsemanager = selv

	hukommelsechunkStørrelse = uint32(Sizeof(THukommelsechunk{}))

	if størrelse < hukommelsechunkStørrelse {
		first = nil
	} else {
		first = (*THukommelsechunk)(Pointer(uintptr(QueueBegyndaddress) + uintptr(begynd)))
		first.allocated = false
		first.previous = nil
		first.næste = nil
		first.størrelse = størrelse - hukommelsechunkStørrelse
	}
}
func (selv *THukommelsemanager) Destruer() {
	if AktivHukommelsemanager == selv {
		AktivHukommelsemanager = nil
	}
}
func (selv *THukommelsemanager) Malloc(størrelse uint32) Pointer {
	var result *THukommelsechunk = nil

	var chunk *THukommelsechunk = first
	for ; chunk != nil && result == nil; chunk = chunk.næste {
		if chunk.størrelse > størrelse && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.størrelse >= (størrelse + hukommelsechunkStørrelse + 1) {

		var temporary *THukommelsechunk
		temporary = (*THukommelsechunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + hukommelsechunkStørrelse + størrelse)))

		temporary.allocated = false
		temporary.størrelse = result.størrelse - størrelse - hukommelsechunkStørrelse
		temporary.previous = result
		temporary.næste = result.næste

		if temporary.næste != nil {
			temporary.næste.previous = temporary
		}

		result.størrelse = størrelse
		result.næste = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(hukommelsechunkStørrelse))
}
func (selv *THukommelsemanager) Alignedmalloc(størrelse uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if størrelse == 0 || størrelse > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *THukommelsechunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.næste {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(hukommelsechunkStørrelse))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.størrelse && størrelse <= chunk.størrelse-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	størrelse += diff
	if result.størrelse-størrelse >= hukommelsechunkStørrelse+1 {
		temporary := (*THukommelsechunk)(Pointer(uintptr(Pointer(result)) + uintptr(hukommelsechunkStørrelse) + uintptr(størrelse)))
		temporary.allocated = false
		temporary.størrelse = result.størrelse - størrelse - hukommelsechunkStørrelse
		temporary.previous = result
		temporary.næste = result.næste
		if temporary.næste != nil {
			temporary.næste.previous = temporary
		}
		result.størrelse = størrelse
		result.næste = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(hukommelsechunkStørrelse) + uintptr(diff)), diff
}
func (selv *THukommelsemanager) Fri(markør_2 Pointer) {
	var chunk *THukommelsechunk = (*THukommelsechunk)(Pointer(uintptr(markør_2) - uintptr(hukommelsechunkStørrelse)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.næste = chunk.næste
		chunk.previous.størrelse += chunk.størrelse + hukommelsechunkStørrelse
		if chunk.næste != nil {
			chunk.næste.previous = chunk.previous
		}
	}

	if chunk.næste != nil && !chunk.næste.allocated {
		chunk.størrelse += chunk.næste.størrelse + hukommelsechunkStørrelse
		chunk.næste = chunk.næste.næste
		if chunk.næste != nil {
			chunk.næste.previous = chunk
		}
	}
}
func Ny(størrelse int) Pointer {
	if AktivHukommelsemanager == nil {
		return nil
	}
	return AktivHukommelsemanager.Malloc(uint32(størrelse))
}
func Slet(markør_2 Pointer) {
	if AktivHukommelsemanager != nil {
		AktivHukommelsemanager.Fri(markør_2)
	}
}
