/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "geheugenmanager"
import . "gdt"

var Proef uint8

func halt()

type TcpuStatus struct {
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

type TTaak struct {
	stapelgeheugen		[4096]uint8
	cpuStatus	*TcpuStatus
}

func (zelf *TTaak) Init(gdt *TShareddescriptorTabel, mem *mem.TGeheugenmanager, itempoint_2 func()) {

	zelf.cpuStatus = (*TcpuStatus)(Pointer(uintptr(mem.Geheugen_toewijzen(1024*1024)) + 1024*1024 - Sizeof(TcpuStatus{})))

	zelf.cpuStatus.Eax = 0
	zelf.cpuStatus.Ebx = 0
	zelf.cpuStatus.Ecx = 0
	zelf.cpuStatus.Edx = 0

	zelf.cpuStatus.Esi = 0
	zelf.cpuStatus.Edi = 0

	zelf.cpuStatus.Gs = 0
	zelf.cpuStatus.Fs = 0
	zelf.cpuStatus.Es = 0
	zelf.cpuStatus.Ds = 0

	zelf.cpuStatus.Eip = uint32(ValueOf(itempoint_2).Pointer())
	zelf.cpuStatus.Cs = Segkernelcode
	zelf.cpuStatus.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(zelf.cpuStatus)))

	zelf.cpuStatus.Esp = stackaddress
	zelf.cpuStatus.Ebp = stackaddress
	zelf.cpuStatus.Ss = 0

}

type TTaakmanager struct {
}

var taken [256]TTaak
var getalTaken int
var huidigTaak int

func (zelf *TTaakmanager) Init() {
	getalTaken = 0
	huidigTaak = -1
}

func (zelf *TTaakmanager) ToevoegenTaak(taak TTaak) bool {
	if getalTaken >= 255 {
		return false
	}
	taken[getalTaken] = taak
	getalTaken++
	return true
}

func (zelf *TTaakmanager) Schedule(cpuStatus *TcpuStatus) *TcpuStatus {

	console_2 := TConsole{}
	for i := 0; i < getalTaken; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(taken[i].cpuStatus)))

		console_2.MUnsignedinteger32Afdrukkenxy(x, 10, uint16(15+i))
	}
	if getalTaken <= 0 {
		return cpuStatus
	}

	if huidigTaak >= 0 {
		taken[huidigTaak].cpuStatus = cpuStatus
	}

	huidigTaak++
	if huidigTaak >= getalTaken {
		huidigTaak %= getalTaken

	}

	return taken[huidigTaak].cpuStatus
}
