package commun

type Mémoireoper struct {
}

func (self *Mémoireoper) Memensemble(bufferPointeur uintptr, valeur byte, taille uint32) uintptr {
	return bufferPointeur
}
func (self *Mémoireoper) MemDéplacer(destinationPointeur_2 uintptr, srcptr uintptr, taille uint32) uintptr {
	return destinationPointeur_2
}

func (self *Mémoireoper) Memcopier(destinationPointeur_2 uintptr, srcptr uintptr, taille uint32) uintptr {
	return destinationPointeur_2
}
func (self *Mémoireoper) Memcmp(destinationPointeur_2 uintptr, srcptr uintptr, taille uint32) bool {
	return true
}
