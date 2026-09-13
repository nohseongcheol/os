package memorymananger

import . "unsafe"

const MaksqueueIzmērs uint32 = 0x1FFFFFF
const QueueStartētaddress uint32 = 0x1000000

type TAtmiņachunk struct {
	nākamais	*TAtmiņachunk
	previous	*TAtmiņachunk
	allocated	bool

	izmērs	uint32
}

type TAtmiņamanager struct {
}

var pirmais *TAtmiņachunk
var AktīvsAtmiņamanager *TAtmiņamanager = nil
var atmiņachunkIzmērs uint32

func (pats *TAtmiņamanager) Init(startēt uint32, izmērs uint32) {

	AktīvsAtmiņamanager = pats

	atmiņachunkIzmērs = uint32(Sizeof(TAtmiņachunk{}))

	if izmērs < atmiņachunkIzmērs {
		pirmais = nil
	} else {
		pirmais = (*TAtmiņachunk)(Pointer(uintptr(QueueStartētaddress) + uintptr(startēt)))
		pirmais.allocated = false
		pirmais.previous = nil
		pirmais.nākamais = nil
		pirmais.izmērs = izmērs - atmiņachunkIzmērs
	}
}
func (pats *TAtmiņamanager) Iznīcināt() {
	if AktīvsAtmiņamanager == pats {
		AktīvsAtmiņamanager = nil
	}
}
func (pats *TAtmiņamanager) Malloc(izmērs uint32) Pointer {
	var result *TAtmiņachunk = nil

	var chunk *TAtmiņachunk = pirmais
	for ; chunk != nil && result == nil; chunk = chunk.nākamais {
		if chunk.izmērs > izmērs && !chunk.allocated {
			result = chunk
		}
	}

	if result == nil {
		return nil
	}

	if result.izmērs >= (izmērs + atmiņachunkIzmērs + 1) {

		var temporary *TAtmiņachunk
		temporary = (*TAtmiņachunk)(Pointer(uintptr(uint32(uintptr(Pointer(result))) + atmiņachunkIzmērs + izmērs)))

		temporary.allocated = false
		temporary.izmērs = result.izmērs - izmērs - atmiņachunkIzmērs
		temporary.previous = result
		temporary.nākamais = result.nākamais

		if temporary.nākamais != nil {
			temporary.nākamais.previous = temporary
		}

		result.izmērs = izmērs
		result.nākamais = temporary
	}
	result.allocated = true

	return Pointer(uintptr(Pointer(result)) + uintptr(atmiņachunkIzmērs))
}
func (pats *TAtmiņamanager) Alignedmalloc(izmērs uint32) (Pointer, uint32) {
	// Account for leading alignment padding before selecting a free chunk.
	// Otherwise the split header can overlap a live page or underflow its size.
	if izmērs == 0 || izmērs > ^uint32(0)-0x1000 {
		return nil, 0
	}
	var result *TAtmiņachunk
	var diff uint32
	for chunk := pirmais; chunk != nil; chunk = chunk.nākamais {
		if chunk.allocated {
			continue
		}
		address := uint32(uintptr(Pointer(chunk)) + uintptr(atmiņachunkIzmērs))
		diff = (0x1000 - (address & 0xFFF)) & 0xFFF
		if address+diff < address {
			continue
		}
		if diff <= chunk.izmērs && izmērs <= chunk.izmērs-diff {
			result = chunk
			break
		}
	}
	if result == nil {
		return nil, 0
	}
	izmērs += diff
	if result.izmērs-izmērs >= atmiņachunkIzmērs+1 {
		temporary := (*TAtmiņachunk)(Pointer(uintptr(Pointer(result)) + uintptr(atmiņachunkIzmērs) + uintptr(izmērs)))
		temporary.allocated = false
		temporary.izmērs = result.izmērs - izmērs - atmiņachunkIzmērs
		temporary.previous = result
		temporary.nākamais = result.nākamais
		if temporary.nākamais != nil {
			temporary.nākamais.previous = temporary
		}
		result.izmērs = izmērs
		result.nākamais = temporary
	}
	result.allocated = true
	return Pointer(uintptr(Pointer(result)) + uintptr(atmiņachunkIzmērs) + uintptr(diff)), diff
}
func (pats *TAtmiņamanager) Brīvs(kursors_2 Pointer) {
	var chunk *TAtmiņachunk = (*TAtmiņachunk)(Pointer(uintptr(kursors_2) - uintptr(atmiņachunkIzmērs)))
	chunk.allocated = false

	if chunk.previous != nil && !chunk.previous.allocated {
		chunk.previous.nākamais = chunk.nākamais
		chunk.previous.izmērs += chunk.izmērs + atmiņachunkIzmērs
		if chunk.nākamais != nil {
			chunk.nākamais.previous = chunk.previous
		}
	}

	if chunk.nākamais != nil && !chunk.nākamais.allocated {
		chunk.izmērs += chunk.nākamais.izmērs + atmiņachunkIzmērs
		chunk.nākamais = chunk.nākamais.nākamais
		if chunk.nākamais != nil {
			chunk.nākamais.previous = chunk
		}
	}
}
func Jauns(izmērs int) Pointer {
	if AktīvsAtmiņamanager == nil {
		return nil
	}
	return AktīvsAtmiņamanager.Malloc(uint32(izmērs))
}
func Dzēst(kursors_2 Pointer) {
	if AktīvsAtmiņamanager != nil {
		AktīvsAtmiņamanager.Brīvs(kursors_2)
	}
}
