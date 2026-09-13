package tëpërbashkët

type Memoriaoper struct {
}

func (vetvetja *Memoriaoper) MemCaktoni(bufferKursori uintptr, vlera byte, madhësia uint32) uintptr {
	return bufferKursori
}
func (vetvetja *Memoriaoper) MemLëviz(destinacioniKursori_2 uintptr, srcptr uintptr, madhësia uint32) uintptr {
	return destinacioniKursori_2
}

func (vetvetja *Memoriaoper) MemKopjo(destinacioniKursori_2 uintptr, srcptr uintptr, madhësia uint32) uintptr {
	return destinacioniKursori_2
}
func (vetvetja *Memoriaoper) Memcmp(destinacioniKursori_2 uintptr, srcptr uintptr, madhësia uint32) bool {
	return true
}
