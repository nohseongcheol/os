/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package memorymananger

import . "unsafe"

const MaxqueueGrootte uint32 = 0x1FFFFFF
const QueueStartenaddress uint32 = 0x1000000

type TGeheugenchunk struct {
	volgende	*TGeheugenchunk
	previous	*TGeheugenchunk
	allocated	bool

	grootte	uint32
}

type TGeheugenmanager struct {
}

var first *TGeheugenchunk
var ActiefGeheugenmanager *TGeheugenmanager = nil
var geheugenchunkGrootte uint32

func (zelf *TGeheugenmanager) Init(starten uint32, grootte uint32) {

	ActiefGeheugenmanager = zelf

	geheugenchunkGrootte = uint32(Sizeof(TGeheugenchunk{}))

	if grootte < geheugenchunkGrootte {
		first = nil
	} else {
		first = (*TGeheugenchunk)(Pointer(uintptr(QueueStartenaddress) + uintptr(starten)))
		first.allocated = false
		first.previous = nil
		first.volgende = nil
		first.grootte = grootte - geheugenchunkGrootte
	}
}
func (zelf *TGeheugenmanager) Vernietigen() {
	if ActiefGeheugenmanager == zelf {
		ActiefGeheugenmanager = nil
	}
}
func (zelf *TGeheugenmanager) Geheugen_toewijzen(grootte uint32) Pointer {
	var rESULTAAT *TGeheugenchunk = nil

	var chunk *TGeheugenchunk = first
	for ; chunk != nil && rESULTAAT == nil; chunk = chunk.volgende {
		if chunk.grootte > grootte && !chunk.allocated {
			rESULTAAT = chunk
		}
	}

	if rESULTAAT == nil {
		return nil
	}

	if rESULTAAT.grootte >= (grootte + geheugenchunkGrootte + 1) {

		var temporary *TGeheugenchunk
		temporary = (*TGeheugenchunk)(Pointer(uintptr(uint32(uintptr(Pointer(rESULTAAT))) + geheugenchunkGrootte + grootte)))

		temporary.allocated = false
		temporary.grootte = rESULTAAT.grootte - grootte - geheugenchunkGrootte
		temporary.previous = rESULTAAT
		temporary.volgende = rESULTAAT.volgende

		if temporary.volgende != nil {
			temporary.volgende.previous = temporary
		}

		rESULTAAT.grootte = grootte
		rESULTAAT.volgende = temporary
	}
	rESULTAAT.allocated = true

	return Pointer(uintptr(Pointer(rESULTAAT)) + uintptr(geheugenchunkGrootte))
}
func (zelf *TGeheugenmanager) Alignedmalloc(grootte uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if grootte == 0 || grootte > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var rESULTAAT *TGeheugenchunk
	var diff uint32
	for chunk := first; chunk != nil; chunk = chunk.volgende {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(geheugenchunkGrootte))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.grootte && grootte <= chunk.grootte-diff {
			rESULTAAT = chunk
			break
		}
	}
	if rESULTAAT == nil {
		return nil, 0
	}
	grootte += diff
	if rESULTAAT.grootte-grootte >= geheugenchunkGrootte+1 {
		temporary := (*TGeheugenchunk)(Pointer(uintptr(Pointer(rESULTAAT)) + uintptr(geheugenchunkGrootte) + uintptr(grootte)))
		temporary.allocated = false
		temporary.grootte = rESULTAAT.grootte - grootte - geheugenchunkGrootte
		temporary.previous = rESULTAAT
		temporary.volgende = rESULTAAT.volgende
		if temporary.volgende != nil {
			temporary.volgende.previous = temporary
		}
		rESULTAAT.grootte = grootte
		rESULTAAT.volgende = temporary
	}
	rESULTAAT.allocated = true
	return Pointer(uintptr(Pointer(rESULTAAT)) + uintptr(geheugenchunkGrootte) + uintptr(diff)), diff
}
func (zelf *TGeheugenmanager) Vrij(adresverwijzing_2 Pointer) {
	var chunk *TGeheugenchunk = (*TGeheugenchunk)(Pointer(uintptr(adresverwijzing_2) - uintptr(geheugenchunkGrootte)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.volgende = chunk.volgende
		chunk.previous.grootte += chunk.grootte + geheugenchunkGrootte
		if chunk.volgende != nil {
			chunk.volgende.previous = chunk.previous
		}
	}

	if chunk.volgende != nil && !chunk.volgende.allocated {
		chunk.grootte += chunk.volgende.grootte + geheugenchunkGrootte
		chunk.volgende = chunk.volgende.volgende
		if chunk.volgende != nil {
			chunk.volgende.previous = chunk
		}
	}
}
func Nieuw(grootte int) Pointer {
	if ActiefGeheugenmanager == nil {
		return nil
	}
	return ActiefGeheugenmanager.Geheugen_toewijzen(uint32(grootte))
}
func Verwijderen(adresverwijzing_2 Pointer) {
	if ActiefGeheugenmanager != nil {
		ActiefGeheugenmanager.Vrij(adresverwijzing_2)
	}
}
