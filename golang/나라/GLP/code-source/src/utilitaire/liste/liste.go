package liste

import . "unsafe"
import . "console"
import mem "mémoiregestionnaire"

type TMaillon_de_liste struct {
	référence_mémoire	uintptr
	previous	*TMaillon_de_liste
	suivant		*TMaillon_de_liste
}

type Linkedliste struct {
	head		*TMaillon_de_liste
	tail		*TMaillon_de_liste
	Taille_2	int

	mem	*mem.TMémoiregestionnaire
}

func (self *Linkedliste) Init(mem *mem.TMémoiregestionnaire) {
	self.head = nil
	self.tail = nil
	self.Taille_2 = 0

	self.mem = mem
}
func (self *Linkedliste) Ajouter_en_tête_de_liste(référence_mémoire uintptr) {
	nouveauNœud := (*TMaillon_de_liste)(self.mem.Allouer_la_mémoire(uint32(Sizeof(TMaillon_de_liste{}))))
	if nouveauNœud == nil {
		return
	}
	nouveauNœud.référence_mémoire = référence_mémoire
	nouveauNœud.previous = nil
	nouveauNœud.suivant = self.head
	if self.head != nil {
		self.head.previous = nouveauNœud
	}
	self.head = nouveauNœud
	self.Taille_2++

	if self.head.suivant == nil {
		self.tail = self.head
	}

}
func (self *Linkedliste) Ajouter_en_fin_de_liste(référence_mémoire uintptr) {
	if self.Taille_2 == 0 {
		self.Ajouter_en_tête_de_liste(référence_mémoire)
	} else {
		nouveauNœud := (*TMaillon_de_liste)(self.mem.Allouer_la_mémoire(uint32(Sizeof(TMaillon_de_liste{}))))
		if nouveauNœud == nil {
			return
		}
		nouveauNœud.référence_mémoire = référence_mémoire
		nouveauNœud.previous = self.tail
		nouveauNœud.suivant = nil
		self.tail.suivant = nouveauNœud
		self.tail = nouveauNœud
		self.Taille_2++
	}
}
func (self *Linkedliste) Insérer_à_la_position(index int, référence_mémoire uintptr) {
	if index == 0 {
		self.Ajouter_en_tête_de_liste(référence_mémoire)
	} else {
		previousNœud := self.GetNœudat(index - 1)
		suivantNœud := previousNœud.suivant
		nouveauNœud := (*TMaillon_de_liste)(self.mem.Allouer_la_mémoire(uint32(Sizeof(TMaillon_de_liste{}))))
		if nouveauNœud == nil {
			return
		}
		nouveauNœud.référence_mémoire = référence_mémoire

		previousNœud.suivant = nouveauNœud
		nouveauNœud.previous = previousNœud
		nouveauNœud.suivant = suivantNœud
		if suivantNœud != nil {
			suivantNœud.previous = nouveauNœud
		}

		self.Taille_2++

		if nouveauNœud.suivant == nil {
			self.tail = nouveauNœud
		}
	}
}
func (self *Linkedliste) GetNœudat(index int) *TMaillon_de_liste {
	if index < 0 || index >= self.Taille_2 {
		return nil
	}
	var x *TMaillon_de_liste = self.head
	for i := 0; i < index; i++ {
		x = x.suivant
	}
	return x
}

func (self *Linkedliste) EnsembleNœudat(index int, référence_mémoire uintptr) {
	var x *TMaillon_de_liste = self.head
	for i := 0; i < index; i++ {
		x = x.suivant
	}
	if x != nil {
		x.référence_mémoire = référence_mémoire
	}
}
func (self *Linkedliste) Getat(index int) Pointer {
	maillon_de_liste := self.GetNœudat(index)
	if maillon_de_liste == nil {
		return nil
	}
	var référence_mémoire uintptr = maillon_de_liste.référence_mémoire
	return Pointer(référence_mémoire)
}
func (self *Linkedliste) Indexsur(référence_mémoire uintptr) int {
	var n *TMaillon_de_liste = self.head
	i := 0
	for ; i < self.Taille_2; i++ {
		if référence_mémoire == n.référence_mémoire {
			return i
		}
		n = n.suivant
	}
	return -1
}
func (self *Linkedliste) Supprimer_2(référence_mémoire uintptr) {
	index := self.Indexsur(référence_mémoire)
	if index < 0 {
		return
	}
	self.Supprimerat(index)
}
func (self *Linkedliste) Supprimerat(index int) {
	if index < 0 || index >= self.Taille_2 {
		return
	}
	maillon_de_liste := self.GetNœudat(index)
	if maillon_de_liste == nil {
		return
	}
	if maillon_de_liste.previous != nil {
		maillon_de_liste.previous.suivant = maillon_de_liste.suivant
	} else {
		self.head = maillon_de_liste.suivant
	}
	if maillon_de_liste.suivant != nil {
		maillon_de_liste.suivant.previous = maillon_de_liste.previous
	} else {
		self.tail = maillon_de_liste.previous
	}
	self.Taille_2 = self.Taille_2 - 1

	if self.mem != nil {
		self.mem.Libre(Pointer(maillon_de_liste))
	}
}

var console_2 = TConsole{}

func (self *Linkedliste) Imprimer() {
	console_2.MImprimerxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Imprimer(uint32(uintptr(Pointer(self))))
	for i := 0; i < self.Taille_2; i++ {
		maillon_de_liste := (*TMaillon_de_liste)(self.Getat(i))
		console_2.MUnsignedinteger32Imprimer(uint32(maillon_de_liste.référence_mémoire))
		console_2.MImprimer(":")
	}
}
