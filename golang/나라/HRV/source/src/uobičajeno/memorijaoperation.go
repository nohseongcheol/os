package uobičajeno

type Memorijaoper struct {
}

func (sam *Memorijaoper) MemPostavi(bufferPokazivač uintptr, vrijednost byte, veličina uint32) uintptr {
	return bufferPokazivač
}
func (sam *Memorijaoper) MemPremjesti(odredištePokazivač_2 uintptr, srcptr uintptr, veličina uint32) uintptr {
	return odredištePokazivač_2
}

func (sam *Memorijaoper) MemKopiraj(odredištePokazivač_2 uintptr, srcptr uintptr, veličina uint32) uintptr {
	return odredištePokazivač_2
}
func (sam *Memorijaoper) Memcmp(odredištePokazivač_2 uintptr, srcptr uintptr, veličina uint32) bool {
	return true
}
