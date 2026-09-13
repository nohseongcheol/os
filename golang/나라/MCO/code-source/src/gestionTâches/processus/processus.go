package processus

import . "unsafe"
import . "utilitaire/liste"
import mem "mémoiregestionnaire"
import . "gestionTâches/filExécution"
import . "gestionTâches/ordonnanceur"
import . "utilitaire"

const ProcutilisateurheapTaille = 1 * 1024 * 1024

type Processus struct {
	identifiant		uint32
	syscallIdentifiant	int
	IsutilisateurEspace	bool
	arguments		*[]byte

	FilExécutionliste	Linkedliste
	Threads			*Linkedliste
	FichierNom		[]byte

	Pagerépertoireélément	uintptr
}

func (self *Processus) Init(mem *mem.TMémoiregestionnaire) {
	self.FilExécutionliste = Linkedliste{}
	self.Threads = &self.FilExécutionliste
	self.Threads.Init(mem)
}

type Processushelper struct {
	processus_2			Linkedliste
	mem				*mem.TMémoiregestionnaire
	noyaupagerépertoireélément	uintptr
}

func (self *Processushelper) Init(mem *mem.TMémoiregestionnaire, noyaupagerépertoireélément uintptr) {
	self.mem = mem
	self.processus_2 = Linkedliste{}
	self.processus_2.Init(self.mem)
	self.noyaupagerépertoireélément = noyaupagerépertoireélément
}

func (self *Processushelper) Créer(élémentpoint func(), filExécutionhelper *TFilExécutionhelper, Pagerépertoireélément uint32, isnoyau bool) Processus {
	processus := (*Processus)(self.mem.Allouer_la_mémoire(uint32(Sizeof(Processus{}))))
	if processus == nil {
		return Processus{}
	}
	processus.Init(self.mem)
	processus.identifiant = Allocatepid()
	processus.Pagerépertoireélément = uintptr(Pagerépertoireélément)
	principalfilExécution := filExécutionhelper.CréerPointeurdeFonction(élémentpoint, Pagerépertoireélément, isnoyau)
	if principalfilExécution != nil {
		principalfilExécution.Pid = processus.identifiant
		principalfilExécution.Parentpid = 0
		processus.Threads.Ajouter_en_fin_de_liste(uintptr(Pointer(principalfilExécution)))
	}

	self.processus_2.Ajouter_en_fin_de_liste(uintptr(Pointer(processus)))

	return *processus
}

func (self *Processushelper) Spawn(élémentpoint func(), filExécutionhelper *TFilExécutionhelper, ordonnanceur *Ordonnanceur, Pagerépertoireélément uint32, isnoyau bool) Processus {
	processus := self.Créer(élémentpoint, filExécutionhelper, Pagerépertoireélément, isnoyau)
	if processus.Threads != nil && processus.Threads.Taille_2 > 0 {
		filExécution := (*TFilExécution)(processus.Threads.Getat(0))
		if filExécution != nil && ordonnanceur != nil {
			ordonnanceur.AjouterfilExécution(filExécution)
		}
	}
	return processus
}

func (self *Processushelper) copierpagerépertoire(sourceélément uintptr, destinationélément uintptr) {
	source_2 := Getunsignedinteger32tableaudePointeur(sourceélément, 1024, 1024)
	destination_2 := Getunsignedinteger32tableaudePointeur(destinationélément, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = source_2[i]
	}
}
func (self *Processushelper) Créerdedonnées() Processus {
	processus := Processus{}
	return processus
}
