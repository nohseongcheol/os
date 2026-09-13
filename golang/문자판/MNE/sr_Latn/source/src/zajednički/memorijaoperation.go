package zajednički

type Memorijaoper struct {
}

func (isti *Memorijaoper) Memskup(bufferPokazivač uintptr, vrednost byte, veličina uint32) uintptr {
	return bufferPokazivač
}
func (isti *Memorijaoper) MemPremesti(odredištePokazivač_2 uintptr, srcptr uintptr, veličina uint32) uintptr {
	return odredištePokazivač_2
}

func (isti *Memorijaoper) MemUmnoži(odredištePokazivač_2 uintptr, srcptr uintptr, veličina uint32) uintptr {
	return odredištePokazivač_2
}
func (isti *Memorijaoper) Memcmp(odredištePokazivač_2 uintptr, srcptr uintptr, veličina uint32) bool {
	return true
}
