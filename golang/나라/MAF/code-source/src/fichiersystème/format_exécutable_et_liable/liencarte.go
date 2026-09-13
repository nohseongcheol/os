package format_exécutable_et_liable

import . "unsafe"
import . "console"

import mem "mémoiregestionnaire"

type Lien struct {
	Dynamique	uintptr
	Previous	*Lien
	Suivant		*Lien
}
type Liencarte struct {
	First		*Lien
	Dernière	*Lien

	Taille_2	int

	mem	*mem.TMémoiregestionnaire
}

func (self *Liencarte) Init(mem *mem.TMémoiregestionnaire) {
	self.mem = mem
}
func (self *Liencarte) Clone() Liencarte {
	var liencarte Liencarte

	liencarte.Init(self.mem)

	Lien := self.First

	for ; Lien != nil; Lien = Lien.Suivant {
		liencarte.Ajouter_en_fin_de_liste(Lien.Dynamique)
	}
	return liencarte
}
func (self *Liencarte) Ajouter_en_tête_de_liste(Dynamique uintptr) {
	nouveaulien := (*Lien)(self.mem.Allouer_la_mémoire(uint32(Sizeof(Lien{}))))
	nouveaulien.Dynamique = Dynamique
	nouveaulien.Suivant = self.First
	self.First = nouveaulien
	self.Taille_2++

	if self.First.Suivant == nil {
		self.Dernière = self.First
	}
}
func (self *Liencarte) Ajouter_en_fin_de_liste(Dynamique uintptr) {
	if Dynamique == 0 {
		return
	}

	if self.Taille_2 == 0 {
		self.Ajouter_en_tête_de_liste(Dynamique)
	} else {
		nouveaulien := (*Lien)(self.mem.Allouer_la_mémoire(uint32(Sizeof(Lien{}))))
		nouveaulien.Dynamique = Dynamique
		nouveaulien.Suivant = nil
		self.Dernière.Suivant = nouveaulien
		self.Dernière = nouveaulien
		self.Taille_2++
	}
}
func (self *Liencarte) Imprimer(x uint16, y uint16) {
	Lien := self.First
	console_2 := TConsole{}
	console_2.MImprimerxy("linkmap : ", x, y)
	for ; Lien != nil; Lien = Lien.Suivant {
		console_2.MUnsignedinteger32Imprimer(uint32(Lien.Dynamique))
		console_2.MImprimer("+")

	}
}
