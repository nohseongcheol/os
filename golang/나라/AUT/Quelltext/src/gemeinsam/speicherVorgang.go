package gemeinsam

type Speicheroper struct {
}

func (selbst *Speicheroper) MemSetzen(bufferZeiger uintptr, wert byte, größe uint32) uintptr {
	return bufferZeiger
}
func (selbst *Speicheroper) MemVerschieben(zielZeiger_2 uintptr, srcptr uintptr, größe uint32) uintptr {
	return zielZeiger_2
}

func (selbst *Speicheroper) MemKopieren(zielZeiger_2 uintptr, srcptr uintptr, größe uint32) uintptr {
	return zielZeiger_2
}
func (selbst *Speicheroper) Memcmp(zielZeiger_2 uintptr, srcptr uintptr, größe uint32) bool {
	return true
}
