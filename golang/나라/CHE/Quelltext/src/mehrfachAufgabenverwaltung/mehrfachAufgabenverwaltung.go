package mehrfachAufgabenverwaltung

import . "unsafe"
import . "konsole"
import . "reflect"
import mem "speicherVerwalter"
import . "gdt"

var Testen uint8

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

type TAufgabe struct {
	stapelspeicher		[4096]uint8
	cpuStatus	*TcpuStatus
}

func (selbst *TAufgabe) Init(gdt *TShareddescriptorTabelle, mem *mem.TSpeicherVerwalter, eintragpoint_2 func()) {

	selbst.cpuStatus = (*TcpuStatus)(Pointer(uintptr(mem.Speicher_reservieren(1024*1024)) + 1024*1024 - Sizeof(TcpuStatus{})))

	selbst.cpuStatus.Eax = 0
	selbst.cpuStatus.Ebx = 0
	selbst.cpuStatus.Ecx = 0
	selbst.cpuStatus.Edx = 0

	selbst.cpuStatus.Esi = 0
	selbst.cpuStatus.Edi = 0

	selbst.cpuStatus.Gs = 0
	selbst.cpuStatus.Fs = 0
	selbst.cpuStatus.Es = 0
	selbst.cpuStatus.Ds = 0

	selbst.cpuStatus.Eip = uint32(ValueOf(eintragpoint_2).Pointer())
	selbst.cpuStatus.Cs = SegKerncode
	selbst.cpuStatus.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(selbst.cpuStatus)))

	selbst.cpuStatus.Esp = stackaddress
	selbst.cpuStatus.Ebp = stackaddress
	selbst.cpuStatus.Ss = 0

}

type TAufgabeVerwalter struct {
}

var aufgaben [256]TAufgabe
var nummerAufgaben int
var systemzeitAufgabe int

func (selbst *TAufgabeVerwalter) Init() {
	nummerAufgaben = 0
	systemzeitAufgabe = -1
}

func (selbst *TAufgabeVerwalter) HinzufügenAufgabe(aufgabe TAufgabe) bool {
	if nummerAufgaben >= 255 {
		return false
	}
	aufgaben[nummerAufgaben] = aufgabe
	nummerAufgaben++
	return true
}

func (selbst *TAufgabeVerwalter) Schedule(cpuStatus *TcpuStatus) *TcpuStatus {

	konsole_2 := TKonsole{}
	for i := 0; i < nummerAufgaben; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(aufgaben[i].cpuStatus)))

		konsole_2.MUnsignedinteger32Druckenxy(x, 10, uint16(15+i))
	}
	if nummerAufgaben <= 0 {
		return cpuStatus
	}

	if systemzeitAufgabe >= 0 {
		aufgaben[systemzeitAufgabe].cpuStatus = cpuStatus
	}

	systemzeitAufgabe++
	if systemzeitAufgabe >= nummerAufgaben {
		systemzeitAufgabe %= nummerAufgaben

	}

	return aufgaben[systemzeitAufgabe].cpuStatus
}
