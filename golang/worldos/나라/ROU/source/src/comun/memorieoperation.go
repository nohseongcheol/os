/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package comun

type Memorieoper struct {
}

func (sine *Memorieoper) Memdefinit(bufferIndicator uintptr, valoare byte, mărime uint32) uintptr {
	return bufferIndicator
}
func (sine *Memorieoper) MemMutare(destinațieIndicator_2 uintptr, srcptr uintptr, mărime uint32) uintptr {
	return destinațieIndicator_2
}

func (sine *Memorieoper) MemCopiază(destinațieIndicator_2 uintptr, srcptr uintptr, mărime uint32) uintptr {
	return destinațieIndicator_2
}
func (sine *Memorieoper) Memcmp(destinațieIndicator_2 uintptr, srcptr uintptr, mărime uint32) bool {
	return true
}
