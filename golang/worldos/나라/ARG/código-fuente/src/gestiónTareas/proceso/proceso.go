/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proceso

import . "unsafe"
import . "utilidad/lista"
import mem "memoriagestor"
import . "gestiónTareas/hilo"
import . "gestiónTareas/planificador"
import . "utilidad"

const ProcusuarioheapTamaño = 1 * 1024 * 1024

type Proceso struct {
	id			uint32
	syscallid		int
	IsusuarioEspacio	bool
	argumentos		*[]byte

	Hilolista	Linkedlista
	Threads		*Linkedlista
	ArchivoNombre	[]byte

	Páginadirectorioentrada	uintptr
}

func (propio *Proceso) Init(mem *mem.TMemoriagestor) {
	propio.Hilolista = Linkedlista{}
	propio.Threads = &propio.Hilolista
	propio.Threads.Init(mem)
}

type Procesohelper struct {
	procesos			Linkedlista
	mem				*mem.TMemoriagestor
	núcleopáginadirectorioentrada	uintptr
}

func (propio *Procesohelper) Init(mem *mem.TMemoriagestor, núcleopáginadirectorioentrada uintptr) {
	propio.mem = mem
	propio.procesos = Linkedlista{}
	propio.procesos.Init(propio.mem)
	propio.núcleopáginadirectorioentrada = núcleopáginadirectorioentrada
}

func (propio *Procesohelper) Crear(entradapoint func(), hilohelper *THilohelper, Páginadirectorioentrada uint32, isnúcleo bool) Proceso {
	proceso := (*Proceso)(propio.mem.Asignar_memoria(uint32(Sizeof(Proceso{}))))
	if proceso == nil {
		return Proceso{}
	}
	proceso.Init(propio.mem)
	proceso.id = Allocatepid()
	proceso.Páginadirectorioentrada = uintptr(Páginadirectorioentrada)
	principalhilo := hilohelper.CrearPunterodesdeFunción(entradapoint, Páginadirectorioentrada, isnúcleo)
	if principalhilo != nil {
		principalhilo.Pid = proceso.id
		principalhilo.Padrepid = 0
		proceso.Threads.Añadir_al_final_de_la_lista(uintptr(Pointer(principalhilo)))
	}

	propio.procesos.Añadir_al_final_de_la_lista(uintptr(Pointer(proceso)))

	return *proceso
}

func (propio *Procesohelper) Spawn(entradapoint func(), hilohelper *THilohelper, planificador *Planificador, Páginadirectorioentrada uint32, isnúcleo bool) Proceso {
	proceso := propio.Crear(entradapoint, hilohelper, Páginadirectorioentrada, isnúcleo)
	if proceso.Threads != nil && proceso.Threads.Tamaño_2 > 0 {
		hilo := (*THilo)(proceso.Threads.Getat(0))
		if hilo != nil && planificador != nil {
			planificador.Añadirhilo(hilo)
		}
	}
	return proceso
}

func (propio *Procesohelper) copiarpáginadirectorio(origenentrada uintptr, destinoentrada uintptr) {
	origen_2 := Getunsignedinteger32matrizdesdePuntero(origenentrada, 1024, 1024)
	destino_2 := Getunsignedinteger32matrizdesdePuntero(destinoentrada, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destino_2[i] = origen_2[i]
	}
}
func (propio *Procesohelper) Creardesdedatos() Proceso {
	proceso := Proceso{}
	return proceso
}
