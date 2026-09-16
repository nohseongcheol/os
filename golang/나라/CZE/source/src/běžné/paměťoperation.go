/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package běžné

type Paměťoper struct {
}

func (self *Paměťoper) MemNastavit(bufferKurzor uintptr, hodnota byte, velikost uint32) uintptr {
	return bufferKurzor
}
func (self *Paměťoper) MemPřesunout(cílKurzor_2 uintptr, srcptr uintptr, velikost uint32) uintptr {
	return cílKurzor_2
}

func (self *Paměťoper) MemKopírovat(cílKurzor_2 uintptr, srcptr uintptr, velikost uint32) uintptr {
	return cílKurzor_2
}
func (self *Paměťoper) Memcmp(cílKurzor_2 uintptr, srcptr uintptr, velikost uint32) bool {
	return true
}
