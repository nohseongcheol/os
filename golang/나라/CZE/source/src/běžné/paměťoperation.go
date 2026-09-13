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
