package memorymananger

import . "unsafe"

const MaxqueueVelikost uint32 = 0x1FFFFFF
const QueueSpustitAdresa uint32 = 0x1000000

type TPaměťchunk struct {
	následující	*TPaměťchunk
	previous	*TPaměťchunk
	allocated	bool

	velikost	uint32
}

type TPaměťmanager struct {
}

var first *TPaměťchunk
var AktivníPaměťmanager *TPaměťmanager = nil
var paměťchunkVelikost uint32

func (self *TPaměťmanager) Init(spustit uint32, velikost uint32) {

	AktivníPaměťmanager = self

	paměťchunkVelikost = uint32(Sizeof(TPaměťchunk{}))

	if velikost < paměťchunkVelikost {
		first = nil
	} else {
		first = (*TPaměťchunk)(Pointer(uintptr(QueueSpustitAdresa) + uintptr(spustit)))
		first.allocated = false
		first.previous = nil
		first.následující = nil
		first.velikost = velikost - paměťchunkVelikost
	}
}
func (self *TPaměťmanager) Zničit() {
	if AktivníPaměťmanager == self {
		AktivníPaměťmanager = nil
	}
}
func (self *TPaměťmanager) Přidělit_paměť(velikost uint32) Pointer {
	var vÝSLEDEK *TPaměťchunk = nil

	var chunk *TPaměťchunk = first
	for ; chunk != nil && vÝSLEDEK == nil; chunk = chunk.následující {
		if chunk.velikost > velikost && !chunk.allocated {
			vÝSLEDEK = chunk
		}
	}

	if vÝSLEDEK == nil {
		return nil
	}

	if vÝSLEDEK.velikost >= (velikost + paměťchunkVelikost + 1) {

		var temporary *TPaměťchunk
		temporary = (*TPaměťchunk)(Pointer(uintptr(uint32(uintptr(Pointer(vÝSLEDEK))) + paměťchunkVelikost + velikost)))

		temporary.allocated = false
		temporary.velikost = vÝSLEDEK.velikost - velikost - paměťchunkVelikost
		temporary.previous = vÝSLEDEK
		temporary.následující = vÝSLEDEK.následující

		if temporary.následující != nil {
			temporary.následující.previous = temporary
		}

		vÝSLEDEK.velikost = velikost
		vÝSLEDEK.následující = temporary
	}
	vÝSLEDEK.allocated = true

	return Pointer(uintptr(Pointer(vÝSLEDEK)) + uintptr(paměťchunkVelikost))
}
func (self *TPaměťmanager) Alignedmalloc(velikost uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if velikost == 0 || velikost > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var vÝSLEDEK *TPaměťchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.následující {
		if chunk.allocated {
			continue
		}
		adresa := uint32(uintptr(Pointer(chunk)) + uintptr(paměťchunkVelikost))
		diff = (0x1000 - (adresa & 0xFFF)) & 0xFFF
		if adresa+diff < adresa {
			continue
		}
		if diff <= chunk.velikost && velikost <= chunk.velikost-diff {
			vÝSLEDEK = chunk
			break
		}
	}
	if vÝSLEDEK == nil {
		return nil, 0
	}
	velikost += diff
	if vÝSLEDEK.velikost-velikost >= paměťchunkVelikost+1 {
		temporary := (*TPaměťchunk)(Pointer(uintptr(Pointer(vÝSLEDEK)) + uintptr(paměťchunkVelikost) + uintptr(velikost)))
		temporary.allocated = false
		temporary.velikost = vÝSLEDEK.velikost - velikost - paměťchunkVelikost
		temporary.previous = vÝSLEDEK
		temporary.následující = vÝSLEDEK.následující
		if temporary.následující != nil {
			temporary.následující.previous = temporary
		}
		vÝSLEDEK.velikost = velikost
		vÝSLEDEK.následující = temporary
	}
	vÝSLEDEK.allocated = true
	return Pointer(uintptr(Pointer(vÝSLEDEK)) + uintptr(paměťchunkVelikost) + uintptr(diff)), diff
}
func (self *TPaměťmanager) Volné(odkaz_na_adresu_2 Pointer) {
	var chunk *TPaměťchunk = (*TPaměťchunk)(Pointer(uintptr(odkaz_na_adresu_2) - uintptr(paměťchunkVelikost)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.následující = chunk.následující
		chunk.previous.velikost += chunk.velikost + paměťchunkVelikost
		if chunk.následující != nil {
			chunk.následující.previous = chunk.previous
		}
	}

	if chunk.následující != nil && !chunk.následující.allocated {
		chunk.velikost += chunk.následující.velikost + paměťchunkVelikost
		chunk.následující = chunk.následující.následující
		if chunk.následující != nil {
			chunk.následující.previous = chunk
		}
	}
}
func Nový(velikost int) Pointer {
	if AktivníPaměťmanager == nil {
		return nil
	}
	return AktivníPaměťmanager.Přidělit_paměť(uint32(velikost))
}
func Smazat(odkaz_na_adresu_2 Pointer) {
	if AktivníPaměťmanager != nil {
		AktivníPaměťmanager.Volné(odkaz_na_adresu_2)
	}
}
