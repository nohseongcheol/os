/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package formato_ejecutable_y_enlazable

import . "unsafe"
import . "consola"

import mem "memoriagestor"

type Enlace struct {
	Dinámico	uintptr
	Previous	*Enlace
	Siguiente	*Enlace
}
type Enlacemapa struct {
	First	*Enlace
	Última	*Enlace

	Tamaño_2	int

	mem	*mem.TMemoriagestor
}

func (propio *Enlacemapa) Init(mem *mem.TMemoriagestor) {
	propio.mem = mem
}
func (propio *Enlacemapa) Clone() Enlacemapa {
	var enlacemapa Enlacemapa

	enlacemapa.Init(propio.mem)

	Enlace := propio.First

	for ; Enlace != nil; Enlace = Enlace.Siguiente {
		enlacemapa.Añadir_al_final_de_la_lista(Enlace.Dinámico)
	}
	return enlacemapa
}
func (propio *Enlacemapa) Añadir_al_inicio_de_la_lista(Dinámico uintptr) {
	nuevoenlace := (*Enlace)(propio.mem.Asignar_memoria(uint32(Sizeof(Enlace{}))))
	nuevoenlace.Dinámico = Dinámico
	nuevoenlace.Siguiente = propio.First
	propio.First = nuevoenlace
	propio.Tamaño_2++

	if propio.First.Siguiente == nil {
		propio.Última = propio.First
	}
}
func (propio *Enlacemapa) Añadir_al_final_de_la_lista(Dinámico uintptr) {
	if Dinámico == 0 {
		return
	}

	if propio.Tamaño_2 == 0 {
		propio.Añadir_al_inicio_de_la_lista(Dinámico)
	} else {
		nuevoenlace := (*Enlace)(propio.mem.Asignar_memoria(uint32(Sizeof(Enlace{}))))
		nuevoenlace.Dinámico = Dinámico
		nuevoenlace.Siguiente = nil
		propio.Última.Siguiente = nuevoenlace
		propio.Última = nuevoenlace
		propio.Tamaño_2++
	}
}
func (propio *Enlacemapa) Imprimir(x uint16, y uint16) {
	Enlace := propio.First
	consola_2 := TConsola{}
	consola_2.MImprimirxy("linkmap : ", x, y)
	for ; Enlace != nil; Enlace = Enlace.Siguiente {
		consola_2.MUnsignedinteger32Imprimir(uint32(Enlace.Dinámico))
		consola_2.MImprimir("+")

	}
}
