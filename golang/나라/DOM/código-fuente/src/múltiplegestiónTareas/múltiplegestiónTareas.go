package múltiplegestiónTareas

import . "unsafe"
import . "consola"
import . "reflect"
import mem "memoriagestor"
import . "gdt"

var Probar uint8

func halt()

type TcpuEstado struct {
	p1	uint32
	p2	uint32

	Eax	uint32
	Ebx	uint32
	Ecx	uint32
	Edx	uint32

	Esi	uint32
	Edi	uint32
	Ebp	uint32

	Gs	uint32
	Fs	uint32
	Es	uint32
	Ds	uint32

	Eip	uint32

	Cs	uint32
	Eflags	uint32

	Esp	uint32
	Ss	uint32
}

type TTarea struct {
	memoria_de_pila		[4096]uint8
	cpuEstado	*TcpuEstado
}

func (propio *TTarea) Init(gdt *TShareddescriptorTabla, mem *mem.TMemoriagestor, entradapoint_2 func()) {

	propio.cpuEstado = (*TcpuEstado)(Pointer(uintptr(mem.Asignar_memoria(1024*1024)) + 1024*1024 - Sizeof(TcpuEstado{})))

	propio.cpuEstado.Eax = 0
	propio.cpuEstado.Ebx = 0
	propio.cpuEstado.Ecx = 0
	propio.cpuEstado.Edx = 0

	propio.cpuEstado.Esi = 0
	propio.cpuEstado.Edi = 0

	propio.cpuEstado.Gs = 0
	propio.cpuEstado.Fs = 0
	propio.cpuEstado.Es = 0
	propio.cpuEstado.Ds = 0

	propio.cpuEstado.Eip = uint32(ValueOf(entradapoint_2).Pointer())
	propio.cpuEstado.Cs = Segnúcleocode
	propio.cpuEstado.Eflags = 0x202

	var stackDirección = uint32(uintptr(Pointer(propio.cpuEstado)))

	propio.cpuEstado.Esp = stackDirección
	propio.cpuEstado.Ebp = stackDirección
	propio.cpuEstado.Ss = 0

}

type TTareagestor struct {
}

var tareas [256]TTarea
var númeroTareas int
var actualtarea int

func (propio *TTareagestor) Init() {
	númeroTareas = 0
	actualtarea = -1
}

func (propio *TTareagestor) Añadirtarea(tarea TTarea) bool {
	if númeroTareas >= 255 {
		return false
	}
	tareas[númeroTareas] = tarea
	númeroTareas++
	return true
}

func (propio *TTareagestor) Schedule(cpuEstado *TcpuEstado) *TcpuEstado {

	consola_2 := TConsola{}
	for i := 0; i < númeroTareas; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tareas[i].cpuEstado)))

		consola_2.MUnsignedinteger32Imprimirxy(x, 10, uint16(15+i))
	}
	if númeroTareas <= 0 {
		return cpuEstado
	}

	if actualtarea >= 0 {
		tareas[actualtarea].cpuEstado = cpuEstado
	}

	actualtarea++
	if actualtarea >= númeroTareas {
		actualtarea %= númeroTareas

	}

	return tareas[actualtarea].cpuEstado
}
