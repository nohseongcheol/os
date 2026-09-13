package elenco

import . "unsafe"
import . "console"
import mem "memoriamanager"

type TNodo_della_lista struct {
	riferimento_di_memoria	uintptr
	previous	*TNodo_della_lista
	successivo	*TNodo_della_lista
}

type LinkedElenco struct {
	head		*TNodo_della_lista
	tail		*TNodo_della_lista
	Dimensione_2	int

	mem	*mem.TMemoriamanager
}

func (séstesso *LinkedElenco) Init(mem *mem.TMemoriamanager) {
	séstesso.head = nil
	séstesso.tail = nil
	séstesso.Dimensione_2 = 0

	séstesso.mem = mem
}
func (séstesso *LinkedElenco) Aggiungi_in_testa_alla_lista(riferimento_di_memoria uintptr) {
	nuovoNodo := (*TNodo_della_lista)(séstesso.mem.Alloca_memoria(uint32(Sizeof(TNodo_della_lista{}))))
	if nuovoNodo == nil {
		return
	}
	nuovoNodo.riferimento_di_memoria = riferimento_di_memoria
	nuovoNodo.previous = nil
	nuovoNodo.successivo = séstesso.head
	if séstesso.head != nil {
		séstesso.head.previous = nuovoNodo
	}
	séstesso.head = nuovoNodo
	séstesso.Dimensione_2++

	if séstesso.head.successivo == nil {
		séstesso.tail = séstesso.head
	}

}
func (séstesso *LinkedElenco) Aggiungi_in_fondo_alla_lista(riferimento_di_memoria uintptr) {
	if séstesso.Dimensione_2 == 0 {
		séstesso.Aggiungi_in_testa_alla_lista(riferimento_di_memoria)
	} else {
		nuovoNodo := (*TNodo_della_lista)(séstesso.mem.Alloca_memoria(uint32(Sizeof(TNodo_della_lista{}))))
		if nuovoNodo == nil {
			return
		}
		nuovoNodo.riferimento_di_memoria = riferimento_di_memoria
		nuovoNodo.previous = séstesso.tail
		nuovoNodo.successivo = nil
		séstesso.tail.successivo = nuovoNodo
		séstesso.tail = nuovoNodo
		séstesso.Dimensione_2++
	}
}
func (séstesso *LinkedElenco) Inserisci_alla_posizione(indice int, riferimento_di_memoria uintptr) {
	if indice == 0 {
		séstesso.Aggiungi_in_testa_alla_lista(riferimento_di_memoria)
	} else {
		previousNodo := séstesso.GetNodoat(indice - 1)
		successivoNodo := previousNodo.successivo
		nuovoNodo := (*TNodo_della_lista)(séstesso.mem.Alloca_memoria(uint32(Sizeof(TNodo_della_lista{}))))
		if nuovoNodo == nil {
			return
		}
		nuovoNodo.riferimento_di_memoria = riferimento_di_memoria

		previousNodo.successivo = nuovoNodo
		nuovoNodo.previous = previousNodo
		nuovoNodo.successivo = successivoNodo
		if successivoNodo != nil {
			successivoNodo.previous = nuovoNodo
		}

		séstesso.Dimensione_2++

		if nuovoNodo.successivo == nil {
			séstesso.tail = nuovoNodo
		}
	}
}
func (séstesso *LinkedElenco) GetNodoat(indice int) *TNodo_della_lista {
	if indice < 0 || indice >= séstesso.Dimensione_2 {
		return nil
	}
	var x *TNodo_della_lista = séstesso.head
	for i := 0; i < indice; i++ {
		x = x.successivo
	}
	return x
}

func (séstesso *LinkedElenco) ImpostaNodoat(indice int, riferimento_di_memoria uintptr) {
	var x *TNodo_della_lista = séstesso.head
	for i := 0; i < indice; i++ {
		x = x.successivo
	}
	if x != nil {
		x.riferimento_di_memoria = riferimento_di_memoria
	}
}
func (séstesso *LinkedElenco) Getat(indice int) Pointer {
	nodo_della_lista := séstesso.GetNodoat(indice)
	if nodo_della_lista == nil {
		return nil
	}
	var riferimento_di_memoria uintptr = nodo_della_lista.riferimento_di_memoria
	return Pointer(riferimento_di_memoria)
}
func (séstesso *LinkedElenco) Indicedi(riferimento_di_memoria uintptr) int {
	var n *TNodo_della_lista = séstesso.head
	i := 0
	for ; i < séstesso.Dimensione_2; i++ {
		if riferimento_di_memoria == n.riferimento_di_memoria {
			return i
		}
		n = n.successivo
	}
	return -1
}
func (séstesso *LinkedElenco) Rimuovi(riferimento_di_memoria uintptr) {
	indice := séstesso.Indicedi(riferimento_di_memoria)
	if indice < 0 {
		return
	}
	séstesso.Rimuoviat(indice)
}
func (séstesso *LinkedElenco) Rimuoviat(indice int) {
	if indice < 0 || indice >= séstesso.Dimensione_2 {
		return
	}
	nodo_della_lista := séstesso.GetNodoat(indice)
	if nodo_della_lista == nil {
		return
	}
	if nodo_della_lista.previous != nil {
		nodo_della_lista.previous.successivo = nodo_della_lista.successivo
	} else {
		séstesso.head = nodo_della_lista.successivo
	}
	if nodo_della_lista.successivo != nil {
		nodo_della_lista.successivo.previous = nodo_della_lista.previous
	} else {
		séstesso.tail = nodo_della_lista.previous
	}
	séstesso.Dimensione_2 = séstesso.Dimensione_2 - 1

	if séstesso.mem != nil {
		séstesso.mem.Libero(Pointer(nodo_della_lista))
	}
}

var console_2 = TConsole{}

func (séstesso *LinkedElenco) Stampa() {
	console_2.MStampaxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Stampa(uint32(uintptr(Pointer(séstesso))))
	for i := 0; i < séstesso.Dimensione_2; i++ {
		nodo_della_lista := (*TNodo_della_lista)(séstesso.Getat(i))
		console_2.MUnsignedinteger32Stampa(uint32(nodo_della_lista.riferimento_di_memoria))
		console_2.MStampa(":")
	}
}
