package skupno

type Pomnilnikoper struct {
}

func (sam *Pomnilnikoper) Memmnožica(bufferKazalnik uintptr, vrednost byte, velikost uint32) uintptr {
	return bufferKazalnik
}
func (sam *Pomnilnikoper) MemPremakni(ciljKazalnik_2 uintptr, srcptr uintptr, velikost uint32) uintptr {
	return ciljKazalnik_2
}

func (sam *Pomnilnikoper) MemKopiraj(ciljKazalnik_2 uintptr, srcptr uintptr, velikost uint32) uintptr {
	return ciljKazalnik_2
}
func (sam *Pomnilnikoper) Memcmp(ciljKazalnik_2 uintptr, srcptr uintptr, velikost uint32) bool {
	return true
}
