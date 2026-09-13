package memorymananger

import . "unsafe"

const MaximumWarteschlangeGröße uint32 = 0x1FFFFFF
const WarteschlangeStartenaddress uint32 = 0x1000000

type TSpeicherchunk struct {
	weiter		*TSpeicherchunk
	previous	*TSpeicherchunk
	allocated	bool

	größe	uint32
}

type TSpeicherVerwalter struct {
}

var first *TSpeicherchunk
var AktivSpeicherVerwalter *TSpeicherVerwalter = nil
var speicherchunkGröße uint32

func (selbst *TSpeicherVerwalter) Init(starten uint32, größe uint32) {

	AktivSpeicherVerwalter = selbst

	speicherchunkGröße = uint32(Sizeof(TSpeicherchunk{}))

	if größe < speicherchunkGröße {
		first = nil
	} else {
		first = (*TSpeicherchunk)(Pointer(uintptr(WarteschlangeStartenaddress) + uintptr(starten)))
		first.allocated = false
		first.previous = nil
		first.weiter = nil
		first.größe = größe - speicherchunkGröße
	}
}
func (selbst *TSpeicherVerwalter) Zerstören() {
	if AktivSpeicherVerwalter == selbst {
		AktivSpeicherVerwalter = nil
	}
}
func (selbst *TSpeicherVerwalter) Speicher_reservieren(größe uint32) Pointer {
	var ergebnis *TSpeicherchunk = nil

	var chunk *TSpeicherchunk = first
	for ; chunk != nil && ergebnis == nil; chunk = chunk.weiter {
		if chunk.größe > größe && !chunk.allocated {
			ergebnis = chunk
		}
	}

	if ergebnis == nil {
		return nil
	}

	if ergebnis.größe >= (größe + speicherchunkGröße + 1) {

		var temporary *TSpeicherchunk
		temporary = (*TSpeicherchunk)(Pointer(uintptr(uint32(uintptr(Pointer(ergebnis))) + speicherchunkGröße + größe)))

		temporary.allocated = false
		temporary.größe = ergebnis.größe - größe - speicherchunkGröße
		temporary.previous = ergebnis
		temporary.weiter = ergebnis.weiter

		if temporary.weiter != nil {
			temporary.weiter.previous = temporary
		}

		ergebnis.größe = größe
		ergebnis.weiter = temporary
	}
	ergebnis.allocated = true

	return Pointer(uintptr(Pointer(ergebnis)) + uintptr(speicherchunkGröße))
}
func (selbst *TSpeicherVerwalter) Alignedmalloc(größe uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if größe == 0 || größe > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var ergebnis *TSpeicherchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.weiter {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(speicherchunkGröße))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.größe && größe <= chunk.größe-diff {
			ergebnis = chunk
			break
		}
	}
	if ergebnis == nil {
		return nil, 0
	}
	größe += diff
	if ergebnis.größe-größe >= speicherchunkGröße+1 {
		temporary := (*TSpeicherchunk)(Pointer(uintptr(Pointer(ergebnis)) + uintptr(speicherchunkGröße) + uintptr(größe)))
		temporary.allocated = false
		temporary.größe = ergebnis.größe - größe - speicherchunkGröße
		temporary.previous = ergebnis
		temporary.weiter = ergebnis.weiter
		if temporary.weiter != nil {
			temporary.weiter.previous = temporary
		}
		ergebnis.größe = größe
		ergebnis.weiter = temporary
	}
	ergebnis.allocated = true
	return Pointer(uintptr(Pointer(ergebnis)) + uintptr(speicherchunkGröße) + uintptr(diff)), diff
}
func (selbst *TSpeicherVerwalter) Frei(adressverweis_2 Pointer) {
	var chunk *TSpeicherchunk = (*TSpeicherchunk)(Pointer(uintptr(adressverweis_2) - uintptr(speicherchunkGröße)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.weiter = chunk.weiter
		chunk.previous.größe += chunk.größe + speicherchunkGröße
		if chunk.weiter != nil {
			chunk.weiter.previous = chunk.previous
		}
	}

	if chunk.weiter != nil && !chunk.weiter.allocated {
		chunk.größe += chunk.weiter.größe + speicherchunkGröße
		chunk.weiter = chunk.weiter.weiter
		if chunk.weiter != nil {
			chunk.weiter.previous = chunk
		}
	}
}
func Neu(größe int) Pointer {
	if AktivSpeicherVerwalter == nil {
		return nil
	}
	return AktivSpeicherVerwalter.Speicher_reservieren(uint32(größe))
}
func Löschen(adressverweis_2 Pointer) {
	if AktivSpeicherVerwalter != nil {
		AktivSpeicherVerwalter.Frei(adressverweis_2)
	}
}
