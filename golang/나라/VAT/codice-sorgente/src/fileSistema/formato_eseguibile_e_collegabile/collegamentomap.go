package formato_eseguibile_e_collegabile

import . "unsafe"
import . "console"

import mem "memoriamanager"

type Collegamento struct {
	Dinamico	uintptr
	Previous	*Collegamento
	Successivo	*Collegamento
}
type Collegamentomap struct {
	First	*Collegamento
	Ultima	*Collegamento

	Dimensione_2	int

	mem	*mem.TMemoriamanager
}

func (séstesso *Collegamentomap) Init(mem *mem.TMemoriamanager) {
	séstesso.mem = mem
}
func (séstesso *Collegamentomap) Clone() Collegamentomap {
	var collegamentomap Collegamentomap

	collegamentomap.Init(séstesso.mem)

	Collegamento := séstesso.First

	for ; Collegamento != nil; Collegamento = Collegamento.Successivo {
		collegamentomap.Aggiungi_in_fondo_alla_lista(Collegamento.Dinamico)
	}
	return collegamentomap
}
func (séstesso *Collegamentomap) Aggiungi_in_testa_alla_lista(Dinamico uintptr) {
	nuovoCollegamento := (*Collegamento)(séstesso.mem.Alloca_memoria(uint32(Sizeof(Collegamento{}))))
	nuovoCollegamento.Dinamico = Dinamico
	nuovoCollegamento.Successivo = séstesso.First
	séstesso.First = nuovoCollegamento
	séstesso.Dimensione_2++

	if séstesso.First.Successivo == nil {
		séstesso.Ultima = séstesso.First
	}
}
func (séstesso *Collegamentomap) Aggiungi_in_fondo_alla_lista(Dinamico uintptr) {
	if Dinamico == 0 {
		return
	}

	if séstesso.Dimensione_2 == 0 {
		séstesso.Aggiungi_in_testa_alla_lista(Dinamico)
	} else {
		nuovoCollegamento := (*Collegamento)(séstesso.mem.Alloca_memoria(uint32(Sizeof(Collegamento{}))))
		nuovoCollegamento.Dinamico = Dinamico
		nuovoCollegamento.Successivo = nil
		séstesso.Ultima.Successivo = nuovoCollegamento
		séstesso.Ultima = nuovoCollegamento
		séstesso.Dimensione_2++
	}
}
func (séstesso *Collegamentomap) Stampa(x uint16, y uint16) {
	Collegamento := séstesso.First
	console_2 := TConsole{}
	console_2.MStampaxy("linkmap : ", x, y)
	for ; Collegamento != nil; Collegamento = Collegamento.Successivo {
		console_2.MUnsignedinteger32Stampa(uint32(Collegamento.Dinamico))
		console_2.MStampa("+")

	}
}
