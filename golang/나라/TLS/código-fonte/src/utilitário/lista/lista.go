/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package lista

import . "unsafe"
import . "console"
import mem "memóriagestor"

type TNó_da_lista struct {
	referência_de_memória	uintptr
	previous	*TNó_da_lista
	seguinte	*TNó_da_lista
}

type Linkedlista struct {
	head		*TNó_da_lista
	tail		*TNó_da_lista
	Tamanho_2	int

	mem	*mem.TMemóriagestor
}

func (próprio *Linkedlista) Init(mem *mem.TMemóriagestor) {
	próprio.head = nil
	próprio.tail = nil
	próprio.Tamanho_2 = 0

	próprio.mem = mem
}
func (próprio *Linkedlista) Adicionar_ao_início_da_lista(referência_de_memória uintptr) {
	novoNó := (*TNó_da_lista)(próprio.mem.Alocar_memória(uint32(Sizeof(TNó_da_lista{}))))
	if novoNó == nil {
		return
	}
	novoNó.referência_de_memória = referência_de_memória
	novoNó.previous = nil
	novoNó.seguinte = próprio.head
	if próprio.head != nil {
		próprio.head.previous = novoNó
	}
	próprio.head = novoNó
	próprio.Tamanho_2++

	if próprio.head.seguinte == nil {
		próprio.tail = próprio.head
	}

}
func (próprio *Linkedlista) Adicionar_ao_fim_da_lista(referência_de_memória uintptr) {
	if próprio.Tamanho_2 == 0 {
		próprio.Adicionar_ao_início_da_lista(referência_de_memória)
	} else {
		novoNó := (*TNó_da_lista)(próprio.mem.Alocar_memória(uint32(Sizeof(TNó_da_lista{}))))
		if novoNó == nil {
			return
		}
		novoNó.referência_de_memória = referência_de_memória
		novoNó.previous = próprio.tail
		novoNó.seguinte = nil
		próprio.tail.seguinte = novoNó
		próprio.tail = novoNó
		próprio.Tamanho_2++
	}
}
func (próprio *Linkedlista) Inserir_na_posição(índice int, referência_de_memória uintptr) {
	if índice == 0 {
		próprio.Adicionar_ao_início_da_lista(referência_de_memória)
	} else {
		previousNó := próprio.GetNóat(índice - 1)
		seguinteNó := previousNó.seguinte
		novoNó := (*TNó_da_lista)(próprio.mem.Alocar_memória(uint32(Sizeof(TNó_da_lista{}))))
		if novoNó == nil {
			return
		}
		novoNó.referência_de_memória = referência_de_memória

		previousNó.seguinte = novoNó
		novoNó.previous = previousNó
		novoNó.seguinte = seguinteNó
		if seguinteNó != nil {
			seguinteNó.previous = novoNó
		}

		próprio.Tamanho_2++

		if novoNó.seguinte == nil {
			próprio.tail = novoNó
		}
	}
}
func (próprio *Linkedlista) GetNóat(índice int) *TNó_da_lista {
	if índice < 0 || índice >= próprio.Tamanho_2 {
		return nil
	}
	var x *TNó_da_lista = próprio.head
	for i := 0; i < índice; i++ {
		x = x.seguinte
	}
	return x
}

func (próprio *Linkedlista) ConjuntoNóat(índice int, referência_de_memória uintptr) {
	var x *TNó_da_lista = próprio.head
	for i := 0; i < índice; i++ {
		x = x.seguinte
	}
	if x != nil {
		x.referência_de_memória = referência_de_memória
	}
}
func (próprio *Linkedlista) Getat(índice int) Pointer {
	nó_da_lista := próprio.GetNóat(índice)
	if nó_da_lista == nil {
		return nil
	}
	var referência_de_memória uintptr = nó_da_lista.referência_de_memória
	return Pointer(referência_de_memória)
}
func (próprio *Linkedlista) Índicede(referência_de_memória uintptr) int {
	var n *TNó_da_lista = próprio.head
	i := 0
	for ; i < próprio.Tamanho_2; i++ {
		if referência_de_memória == n.referência_de_memória {
			return i
		}
		n = n.seguinte
	}
	return -1
}
func (próprio *Linkedlista) Remover(referência_de_memória uintptr) {
	índice := próprio.Índicede(referência_de_memória)
	if índice < 0 {
		return
	}
	próprio.Removerat(índice)
}
func (próprio *Linkedlista) Removerat(índice int) {
	if índice < 0 || índice >= próprio.Tamanho_2 {
		return
	}
	nó_da_lista := próprio.GetNóat(índice)
	if nó_da_lista == nil {
		return
	}
	if nó_da_lista.previous != nil {
		nó_da_lista.previous.seguinte = nó_da_lista.seguinte
	} else {
		próprio.head = nó_da_lista.seguinte
	}
	if nó_da_lista.seguinte != nil {
		nó_da_lista.seguinte.previous = nó_da_lista.previous
	} else {
		próprio.tail = nó_da_lista.previous
	}
	próprio.Tamanho_2 = próprio.Tamanho_2 - 1

	if próprio.mem != nil {
		próprio.mem.Livre(Pointer(nó_da_lista))
	}
}

var console_2 = TConsole{}

func (próprio *Linkedlista) Imprimir() {
	console_2.MImprimirxy("LinkedList:", 1, 1)
	console_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(próprio))))
	for i := 0; i < próprio.Tamanho_2; i++ {
		nó_da_lista := (*TNó_da_lista)(próprio.Getat(i))
		console_2.MUnsignedinteger32Imprimir(uint32(nó_da_lista.referência_de_memória))
		console_2.MImprimir(":")
	}
}
