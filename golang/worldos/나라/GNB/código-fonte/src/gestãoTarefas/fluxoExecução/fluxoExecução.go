/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package FluxoExecução

import . "unsafe"
import . "reflect"
import . "gdt"
import . "console"
import . "múltiplogestãoTarefas"
import mem "memóriagestor"
import . "virtualmemória"

const (
	Blocked		= 1
	Pronto		= 2
	Parado		= 3
	Iniciado	= 4
)

const FluxoExecuçãostackTamanho = 32 * 1024

type TFluxoExecução struct {
	CpuEstado			*TcpuEstado
	Stack				uint32
	Utilizadorstack_2		uint32
	UtilizadorstackTamanho_2	uint32
	Pid				uint32
	Superiorpid			uint32

	Páginadiretóriopontodeentrada	uint32

	FluxoExecuçãoEstado	uint8
	BlockedEstado		uint8

	horadelta	uint32

	TlsSegmentos	[Gdtpontodeentrada]TSegmentdescriptor
	FpuDeslocamento	uintptr
	Fpubuffer	[512 + 16]byte
	Isnúcleo	bool
}

func (próprio *TFluxoExecução) Novo() {
}

type TFluxoExecuçãohelper struct {
	mem *mem.TMemóriagestor
}

var console_2 = TConsole{}

func (próprio *TFluxoExecuçãohelper) Init(mem *mem.TMemóriagestor) {
	próprio.mem = mem
	console_2.MImprimirxy(([]byte)("thread:"), 1, 14)
}
func (próprio *TFluxoExecuçãohelper) CriardeFunção(pontodeentradapoint_2 func(), Páginadiretóriopontodeentrada uint32, isnúcleo bool) TFluxoExecução {
	destino_3 := TFluxoExecução{}

	destino_3.Stack = uint32(uintptr(próprio.mem.Alocar_memória(FluxoExecuçãostackTamanho)))
	if destino_3.Stack == 0 {
		return destino_3
	}
	console_2.MImprimir(([]byte)("[mem:"))
	console_2.MUnsignedinteger32Imprimir(destino_3.Stack)

	destino_3.CpuEstado = (*TcpuEstado)(Pointer(uintptr(destino_3.Stack) + FluxoExecuçãostackTamanho - Sizeof(TcpuEstado{})))
	destino_3.CpuEstado.Esp = destino_3.Stack + FluxoExecuçãostackTamanho
	destino_3.CpuEstado.Ebp = destino_3.CpuEstado.Esp
	destino_3.CpuEstado.Eip = uint32(ValueOf(pontodeentradapoint_2).Pointer())
	destino_3.Utilizadorstack_2 = Utilizadorstack
	destino_3.UtilizadorstackTamanho_2 = UtilizadorstackTamanho
	destino_3.Pid = 0
	destino_3.Superiorpid = 0
	destino_3.Páginadiretóriopontodeentrada = Páginadiretóriopontodeentrada
	console_2.MImprimir((([]byte)("cpu")))

	console_2.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(destino_3.CpuEstado))))

	console_2.MImprimir((([]byte)(":")))
	console_2.MUnsignedinteger32Imprimir(destino_3.CpuEstado.Eip)

	console_2.MImprimir("]")
	if isnúcleo == true {
		destino_3.CpuEstado.Cs = Segnúcleocode
		destino_3.CpuEstado.Ds = Segnúcleodados
		destino_3.CpuEstado.Es = Segnúcleodados
		destino_3.CpuEstado.Fs = Segnúcleodados
		destino_3.CpuEstado.Gs = Segnúcleogs
		destino_3.CpuEstado.Ss = Segnúcleodados
		destino_3.FluxoExecuçãoEstado = Pronto
		destino_3.CpuEstado.Eflags = 0x202
	} else {
		destino_3.CpuEstado.Cs = Segutilizadorcode
		destino_3.CpuEstado.Ds = Segutilizadordados
		destino_3.CpuEstado.Es = Segutilizadordados
		destino_3.CpuEstado.Fs = Segutilizadordados
		destino_3.CpuEstado.Gs = Segutilizadorgs
		destino_3.CpuEstado.Ss = Segutilizadordados
		destino_3.FluxoExecuçãoEstado = Iniciado
		destino_3.CpuEstado.Eflags = 0x222
	}
	destino_3.Isnúcleo = isnúcleo
	destino_3.FpuDeslocamento = 0xffffffff

	return destino_3
}

func (próprio *TFluxoExecuçãohelper) CriarPonteirodeFunção(pontodeentradapoint_2 func(), Páginadiretóriopontodeentrada uint32, isnúcleo bool) *TFluxoExecução {
	destino_3 := (*TFluxoExecução)(próprio.mem.Alocar_memória(uint32(Sizeof(TFluxoExecução{}))))
	if destino_3 == nil {
		return nil
	}
	*destino_3 = próprio.CriardeFunção(pontodeentradapoint_2, Páginadiretóriopontodeentrada, isnúcleo)
	if destino_3.CpuEstado == nil {
		próprio.mem.Livre(Pointer(destino_3))
		return nil
	}
	return destino_3
}
