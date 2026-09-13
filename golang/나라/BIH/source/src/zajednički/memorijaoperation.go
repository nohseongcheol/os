package zajednički

type Memorijaoper struct {
}

func (self *Memorijaoper) Memskup(bufferpointer uintptr, vrijednost byte, veličina uint32) uintptr {
	return bufferpointer
}
func (self *Memorijaoper) MemPremjesti(odredištepointer_2 uintptr, srcptr uintptr, veličina uint32) uintptr {
	return odredištepointer_2
}

func (self *Memorijaoper) MemKopiraj(odredištepointer_2 uintptr, srcptr uintptr, veličina uint32) uintptr {
	return odredištepointer_2
}
func (self *Memorijaoper) Memcmp(odredištepointer_2 uintptr, srcptr uintptr, veličina uint32) bool {
	return true
}
