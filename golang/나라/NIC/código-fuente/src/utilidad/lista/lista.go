package lista

import . "unsafe"
import . "consola"
import mem "memoriagestor"

type TNodo_de_lista struct {
	referencia_de_memoria		uintptr
	previous	*TNodo_de_lista
	siguiente	*TNodo_de_lista
}

type Linkedlista struct {
	head		*TNodo_de_lista
	tail		*TNodo_de_lista
	Tamaño_2	int

	mem	*mem.TMemoriagestor
}

func (propio *Linkedlista) Init(mem *mem.TMemoriagestor) {
	propio.head = nil
	propio.tail = nil
	propio.Tamaño_2 = 0

	propio.mem = mem
}
func (propio *Linkedlista) Añadir_al_inicio_de_la_lista(referencia_de_memoria uintptr) {
	nuevoNodo := (*TNodo_de_lista)(propio.mem.Asignar_memoria(uint32(Sizeof(TNodo_de_lista{}))))
	if nuevoNodo == nil {
		return
	}
	nuevoNodo.referencia_de_memoria = referencia_de_memoria
	nuevoNodo.previous = nil
	nuevoNodo.siguiente = propio.head
	if propio.head != nil {
		propio.head.previous = nuevoNodo
	}
	propio.head = nuevoNodo
	propio.Tamaño_2++

	if propio.head.siguiente == nil {
		propio.tail = propio.head
	}

}
func (propio *Linkedlista) Añadir_al_final_de_la_lista(referencia_de_memoria uintptr) {
	if propio.Tamaño_2 == 0 {
		propio.Añadir_al_inicio_de_la_lista(referencia_de_memoria)
	} else {
		nuevoNodo := (*TNodo_de_lista)(propio.mem.Asignar_memoria(uint32(Sizeof(TNodo_de_lista{}))))
		if nuevoNodo == nil {
			return
		}
		nuevoNodo.referencia_de_memoria = referencia_de_memoria
		nuevoNodo.previous = propio.tail
		nuevoNodo.siguiente = nil
		propio.tail.siguiente = nuevoNodo
		propio.tail = nuevoNodo
		propio.Tamaño_2++
	}
}
func (propio *Linkedlista) Insertar_en_la_posición(índice int, referencia_de_memoria uintptr) {
	if índice == 0 {
		propio.Añadir_al_inicio_de_la_lista(referencia_de_memoria)
	} else {
		previousNodo := propio.GetNodoat(índice - 1)
		siguienteNodo := previousNodo.siguiente
		nuevoNodo := (*TNodo_de_lista)(propio.mem.Asignar_memoria(uint32(Sizeof(TNodo_de_lista{}))))
		if nuevoNodo == nil {
			return
		}
		nuevoNodo.referencia_de_memoria = referencia_de_memoria

		previousNodo.siguiente = nuevoNodo
		nuevoNodo.previous = previousNodo
		nuevoNodo.siguiente = siguienteNodo
		if siguienteNodo != nil {
			siguienteNodo.previous = nuevoNodo
		}

		propio.Tamaño_2++

		if nuevoNodo.siguiente == nil {
			propio.tail = nuevoNodo
		}
	}
}
func (propio *Linkedlista) GetNodoat(índice int) *TNodo_de_lista {
	if índice < 0 || índice >= propio.Tamaño_2 {
		return nil
	}
	var x *TNodo_de_lista = propio.head
	for i := 0; i < índice; i++ {
		x = x.siguiente
	}
	return x
}

func (propio *Linkedlista) EstablecerNodoat(índice int, referencia_de_memoria uintptr) {
	var x *TNodo_de_lista = propio.head
	for i := 0; i < índice; i++ {
		x = x.siguiente
	}
	if x != nil {
		x.referencia_de_memoria = referencia_de_memoria
	}
}
func (propio *Linkedlista) Getat(índice int) Pointer {
	nodo_de_lista := propio.GetNodoat(índice)
	if nodo_de_lista == nil {
		return nil
	}
	var referencia_de_memoria uintptr = nodo_de_lista.referencia_de_memoria
	return Pointer(referencia_de_memoria)
}
func (propio *Linkedlista) Índicede(referencia_de_memoria uintptr) int {
	var n *TNodo_de_lista = propio.head
	i := 0
	for ; i < propio.Tamaño_2; i++ {
		if referencia_de_memoria == n.referencia_de_memoria {
			return i
		}
		n = n.siguiente
	}
	return -1
}
func (propio *Linkedlista) Eliminar_2(referencia_de_memoria uintptr) {
	índice := propio.Índicede(referencia_de_memoria)
	if índice < 0 {
		return
	}
	propio.Eliminarat(índice)
}
func (propio *Linkedlista) Eliminarat(índice int) {
	if índice < 0 || índice >= propio.Tamaño_2 {
		return
	}
	nodo_de_lista := propio.GetNodoat(índice)
	if nodo_de_lista == nil {
		return
	}
	if nodo_de_lista.previous != nil {
		nodo_de_lista.previous.siguiente = nodo_de_lista.siguiente
	} else {
		propio.head = nodo_de_lista.siguiente
	}
	if nodo_de_lista.siguiente != nil {
		nodo_de_lista.siguiente.previous = nodo_de_lista.previous
	} else {
		propio.tail = nodo_de_lista.previous
	}
	propio.Tamaño_2 = propio.Tamaño_2 - 1

	if propio.mem != nil {
		propio.mem.Libre(Pointer(nodo_de_lista))
	}
}

var consola_2 = TConsola{}

func (propio *Linkedlista) Imprimir() {
	consola_2.MImprimirxy("LinkedList:", 1, 1)
	consola_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(propio))))
	for i := 0; i < propio.Tamaño_2; i++ {
		nodo_de_lista := (*TNodo_de_lista)(propio.Getat(i))
		consola_2.MUnsignedinteger32Imprimir(uint32(nodo_de_lista.referencia_de_memoria))
		consola_2.MImprimir(":")
	}
}
