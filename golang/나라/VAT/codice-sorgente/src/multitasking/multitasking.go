/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "memoriamanager"
import . "gdt"

var Prova uint8

func halt()

type TcpuStato struct {
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

type TProcesso struct {
	memoria_a_pila		[4096]uint8
	cpuStato	*TcpuStato
}

func (séstesso *TProcesso) Init(gdt *TShareddescriptorTabella, mem *mem.TMemoriamanager, vocepoint_2 func()) {

	séstesso.cpuStato = (*TcpuStato)(Pointer(uintptr(mem.Alloca_memoria(1024*1024)) + 1024*1024 - Sizeof(TcpuStato{})))

	séstesso.cpuStato.Eax = 0
	séstesso.cpuStato.Ebx = 0
	séstesso.cpuStato.Ecx = 0
	séstesso.cpuStato.Edx = 0

	séstesso.cpuStato.Esi = 0
	séstesso.cpuStato.Edi = 0

	séstesso.cpuStato.Gs = 0
	séstesso.cpuStato.Fs = 0
	séstesso.cpuStato.Es = 0
	séstesso.cpuStato.Ds = 0

	séstesso.cpuStato.Eip = uint32(ValueOf(vocepoint_2).Pointer())
	séstesso.cpuStato.Cs = Segkernelcode
	séstesso.cpuStato.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(séstesso.cpuStato)))

	séstesso.cpuStato.Esp = stackaddress
	séstesso.cpuStato.Ebp = stackaddress
	séstesso.cpuStato.Ss = 0

}

type TProcessomanager struct {
}

var attività [256]TProcesso
var numeroAttività int
var correnteProcesso int

func (séstesso *TProcessomanager) Init() {
	numeroAttività = 0
	correnteProcesso = -1
}

func (séstesso *TProcessomanager) AggiungiProcesso(processo TProcesso) bool {
	if numeroAttività >= 255 {
		return false
	}
	attività[numeroAttività] = processo
	numeroAttività++
	return true
}

func (séstesso *TProcessomanager) Schedule(cpuStato *TcpuStato) *TcpuStato {

	console_2 := TConsole{}
	for i := 0; i < numeroAttività; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(attività[i].cpuStato)))

		console_2.MUnsignedinteger32Stampaxy(x, 10, uint16(15+i))
	}
	if numeroAttività <= 0 {
		return cpuStato
	}

	if correnteProcesso >= 0 {
		attività[correnteProcesso].cpuStato = cpuStato
	}

	correnteProcesso++
	if correnteProcesso >= numeroAttività {
		correnteProcesso %= numeroAttività

	}

	return attività[correnteProcesso].cpuStato
}
