package bežné

type Pamäťoper struct {
}

func (vlastný *Pamäťoper) Memsada(bufferKurzor uintptr, hodnota byte, veľkosť uint32) uintptr {
	return bufferKurzor
}
func (vlastný *Pamäťoper) MemPresunúť(cieľKurzor_2 uintptr, srcptr uintptr, veľkosť uint32) uintptr {
	return cieľKurzor_2
}

func (vlastný *Pamäťoper) MemKopírovať(cieľKurzor_2 uintptr, srcptr uintptr, veľkosť uint32) uintptr {
	return cieľKurzor_2
}
func (vlastný *Pamäťoper) Memcmp(cieľKurzor_2 uintptr, srcptr uintptr, veľkosť uint32) bool {
	return true
}
