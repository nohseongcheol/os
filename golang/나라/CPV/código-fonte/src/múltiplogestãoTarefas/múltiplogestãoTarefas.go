package múltiplogestãoTarefas

import . "unsafe"
import . "console"
import . "reflect"
import mem "memóriagestor"
import . "gdt"

var Testar uint8

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

type TTarefa struct {
	memória_de_pilha		[4096]uint8
	cpuEstado	*TcpuEstado
}

func (próprio *TTarefa) Init(gdt *TShareddescriptorTabela, mem *mem.TMemóriagestor, pontodeentradapoint_2 func()) {

	próprio.cpuEstado = (*TcpuEstado)(Pointer(uintptr(mem.Alocar_memória(1024*1024)) + 1024*1024 - Sizeof(TcpuEstado{})))

	próprio.cpuEstado.Eax = 0
	próprio.cpuEstado.Ebx = 0
	próprio.cpuEstado.Ecx = 0
	próprio.cpuEstado.Edx = 0

	próprio.cpuEstado.Esi = 0
	próprio.cpuEstado.Edi = 0

	próprio.cpuEstado.Gs = 0
	próprio.cpuEstado.Fs = 0
	próprio.cpuEstado.Es = 0
	próprio.cpuEstado.Ds = 0

	próprio.cpuEstado.Eip = uint32(ValueOf(pontodeentradapoint_2).Pointer())
	próprio.cpuEstado.Cs = Segnúcleocode
	próprio.cpuEstado.Eflags = 0x202

	var stackEndereço = uint32(uintptr(Pointer(próprio.cpuEstado)))

	próprio.cpuEstado.Esp = stackEndereço
	próprio.cpuEstado.Ebp = stackEndereço
	próprio.cpuEstado.Ss = 0

}

type TTarefagestor struct {
}

var tarefas [256]TTarefa
var númeroTarefas int
var atualtarefa int

func (próprio *TTarefagestor) Init() {
	númeroTarefas = 0
	atualtarefa = -1
}

func (próprio *TTarefagestor) Adicionartarefa(tarefa TTarefa) bool {
	if númeroTarefas >= 255 {
		return false
	}
	tarefas[númeroTarefas] = tarefa
	númeroTarefas++
	return true
}

func (próprio *TTarefagestor) Schedule(cpuEstado *TcpuEstado) *TcpuEstado {

	console_2 := TConsole{}
	for i := 0; i < númeroTarefas; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tarefas[i].cpuEstado)))

		console_2.MUnsignedinteger32Imprimirxy(x, 10, uint16(15+i))
	}
	if númeroTarefas <= 0 {
		return cpuEstado
	}

	if atualtarefa >= 0 {
		tarefas[atualtarefa].cpuEstado = cpuEstado
	}

	atualtarefa++
	if atualtarefa >= númeroTarefas {
		atualtarefa %= númeroTarefas

	}

	return tarefas[atualtarefa].cpuEstado
}
