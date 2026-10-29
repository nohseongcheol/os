/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package comune

type Memoriaoper struct {
}

func (séstesso *Memoriaoper) MemImposta(bufferPuntatore uintptr, valore byte, dimensione uint32) uintptr {
	return bufferPuntatore
}
func (séstesso *Memoriaoper) MemSposta(destinazionePuntatore_2 uintptr, srcptr uintptr, dimensione uint32) uintptr {
	return destinazionePuntatore_2
}

func (séstesso *Memoriaoper) MemCopia(destinazionePuntatore_2 uintptr, srcptr uintptr, dimensione uint32) uintptr {
	return destinazionePuntatore_2
}
func (séstesso *Memoriaoper) Memcmp(destinazionePuntatore_2 uintptr, srcptr uintptr, dimensione uint32) bool {
	return true
}
