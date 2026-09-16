/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Hilo

import . "unsafe"
import . "reflect"
import . "gdt"
import . "consola"
import . "múltiplegestiónTareas"
import mem "memoriagestor"
import . "virtualmemoria"

const (
	Blocked		= 1
	Preparado	= 2
	Parado		= 3
	Iniciado	= 4
)

const HilostackTamaño = 32 * 1024

type THilo struct {
	CpuEstado		*TcpuEstado
	Stack			uint32
	Usuariostack_2		uint32
	UsuariostackTamaño_2	uint32
	Pid			uint32
	Padrepid		uint32

	Páginadirectorioentrada	uint32

	HiloEstado	uint8
	BlockedEstado	uint8

	horadelta	uint32

	TlsSegmentos		[Gdtentrada]TSegmentdescriptor
	FpuDesplazamiento	uintptr
	Fpubuffer		[512 + 16]byte
	Isnúcleo		bool
}

func (propio *THilo) Nuevo() {
}

type THilohelper struct {
	mem *mem.TMemoriagestor
}

var consola_2 = TConsola{}

func (propio *THilohelper) Init(mem *mem.TMemoriagestor) {
	propio.mem = mem
	consola_2.MImprimirxy(([]byte)("thread:"), 1, 14)
}
func (propio *THilohelper) CreardesdeFunción(entradapoint_2 func(), Páginadirectorioentrada uint32, isnúcleo bool) THilo {
	rESULTADO := THilo{}

	rESULTADO.Stack = uint32(uintptr(propio.mem.Asignar_memoria(HilostackTamaño)))
	if rESULTADO.Stack == 0 {
		return rESULTADO
	}
	consola_2.MImprimir(([]byte)("[mem:"))
	consola_2.MUnsignedinteger32Imprimir(rESULTADO.Stack)

	rESULTADO.CpuEstado = (*TcpuEstado)(Pointer(uintptr(rESULTADO.Stack) + HilostackTamaño - Sizeof(TcpuEstado{})))
	rESULTADO.CpuEstado.Esp = rESULTADO.Stack + HilostackTamaño
	rESULTADO.CpuEstado.Ebp = rESULTADO.CpuEstado.Esp
	rESULTADO.CpuEstado.Eip = uint32(ValueOf(entradapoint_2).Pointer())
	rESULTADO.Usuariostack_2 = Usuariostack
	rESULTADO.UsuariostackTamaño_2 = UsuariostackTamaño
	rESULTADO.Pid = 0
	rESULTADO.Padrepid = 0
	rESULTADO.Páginadirectorioentrada = Páginadirectorioentrada
	consola_2.MImprimir((([]byte)("cpu")))

	consola_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(rESULTADO.CpuEstado))))

	consola_2.MImprimir((([]byte)(":")))
	consola_2.MUnsignedinteger32Imprimir(rESULTADO.CpuEstado.Eip)

	consola_2.MImprimir("]")
	if isnúcleo == true {
		rESULTADO.CpuEstado.Cs = Segnúcleocode
		rESULTADO.CpuEstado.Ds = Segnúcleodatos
		rESULTADO.CpuEstado.Es = Segnúcleodatos
		rESULTADO.CpuEstado.Fs = Segnúcleodatos
		rESULTADO.CpuEstado.Gs = Segnúcleogs
		rESULTADO.CpuEstado.Ss = Segnúcleodatos
		rESULTADO.HiloEstado = Preparado
		rESULTADO.CpuEstado.Eflags = 0x202
	} else {
		rESULTADO.CpuEstado.Cs = Segusuariocode
		rESULTADO.CpuEstado.Ds = Segusuariodatos
		rESULTADO.CpuEstado.Es = Segusuariodatos
		rESULTADO.CpuEstado.Fs = Segusuariodatos
		rESULTADO.CpuEstado.Gs = Segusuariogs
		rESULTADO.CpuEstado.Ss = Segusuariodatos
		rESULTADO.HiloEstado = Iniciado
		rESULTADO.CpuEstado.Eflags = 0x222
	}
	rESULTADO.Isnúcleo = isnúcleo
	rESULTADO.FpuDesplazamiento = 0xffffffff

	return rESULTADO
}

func (propio *THilohelper) CrearPunterodesdeFunción(entradapoint_2 func(), Páginadirectorioentrada uint32, isnúcleo bool) *THilo {
	rESULTADO := (*THilo)(propio.mem.Asignar_memoria(uint32(Sizeof(THilo{}))))
	if rESULTADO == nil {
		return nil
	}
	*rESULTADO = propio.CreardesdeFunción(entradapoint_2, Páginadirectorioentrada, isnúcleo)
	if rESULTADO.CpuEstado == nil {
		propio.mem.Libre(Pointer(rESULTADO))
		return nil
	}
	return rESULTADO
}
