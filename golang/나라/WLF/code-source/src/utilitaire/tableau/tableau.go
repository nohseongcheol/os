package tableau

import . "unsafe"
import . "console"

var nœudtableau [100]uintptr

type TTableau struct {
	Taille_2 int
}

func (self *TTableau) Ajouter(référence_mémoire uintptr) {
	nœudtableau[self.Taille_2] = référence_mémoire
	self.Taille_2++
}
func (self *TTableau) Getat(index int) Pointer {
	return Pointer(nœudtableau[index])
}
func (self *TTableau) Indexsur(référence_mémoire uintptr) int {
	i := 0
	for ; i < self.Taille_2; i++ {
		if référence_mémoire == nœudtableau[i] {
			return i
		}
	}
	return -1
}

var console_2 = TConsole{}

func (self *TTableau) Imprimer() {
	console_2.MImprimerxy("array:", 1, 1)

	for i := 0; i < self.Taille_2; i++ {
		console_2.MUnsignedinteger32Imprimer(uint32(nœudtableau[i]))
		console_2.MImprimer(":")
	}
}
