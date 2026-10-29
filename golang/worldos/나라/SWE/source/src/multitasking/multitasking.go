/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "konsol"
import . "reflect"
import mem "minnemanager"
import . "gdt"

var Testa uint8

func halt()

type TcpuTillstånd struct {
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

type TAktivitet struct {
	stackminne			[4096]uint8
	processorTillstånd	*TcpuTillstånd
}

func (själv *TAktivitet) Init(gdt *TShareddescriptorTabell, mem *mem.TMinnemanager, postpoint_2 func()) {

	själv.processorTillstånd = (*TcpuTillstånd)(Pointer(uintptr(mem.Tilldela_minne(1024*1024)) + 1024*1024 - Sizeof(TcpuTillstånd{})))

	själv.processorTillstånd.Eax = 0
	själv.processorTillstånd.Ebx = 0
	själv.processorTillstånd.Ecx = 0
	själv.processorTillstånd.Edx = 0

	själv.processorTillstånd.Esi = 0
	själv.processorTillstånd.Edi = 0

	själv.processorTillstånd.Gs = 0
	själv.processorTillstånd.Fs = 0
	själv.processorTillstånd.Es = 0
	själv.processorTillstånd.Ds = 0

	själv.processorTillstånd.Eip = uint32(ValueOf(postpoint_2).Pointer())
	själv.processorTillstånd.Cs = Segkernelcode
	själv.processorTillstånd.Eflags = 0x202

	var stackAdress = uint32(uintptr(Pointer(själv.processorTillstånd)))

	själv.processorTillstånd.Esp = stackAdress
	själv.processorTillstånd.Ebp = stackAdress
	själv.processorTillstånd.Ss = 0

}

type TAktivitetmanager struct {
}

var uppgifter [256]TAktivitet
var nummerUppgifter int
var aktuellAktivitet int

func (själv *TAktivitetmanager) Init() {
	nummerUppgifter = 0
	aktuellAktivitet = -1
}

func (själv *TAktivitetmanager) LäggtillAktivitet(aktivitet TAktivitet) bool {
	if nummerUppgifter >= 255 {
		return false
	}
	uppgifter[nummerUppgifter] = aktivitet
	nummerUppgifter++
	return true
}

func (själv *TAktivitetmanager) Schedule(processorTillstånd *TcpuTillstånd) *TcpuTillstånd {

	konsol_2 := TKonsol{}
	for i := 0; i < nummerUppgifter; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(uppgifter[i].processorTillstånd)))

		konsol_2.MUnsignedinteger32Skrivutxy(x, 10, uint16(15+i))
	}
	if nummerUppgifter <= 0 {
		return processorTillstånd
	}

	if aktuellAktivitet >= 0 {
		uppgifter[aktuellAktivitet].processorTillstånd = processorTillstånd
	}

	aktuellAktivitet++
	if aktuellAktivitet >= nummerUppgifter {
		aktuellAktivitet %= nummerUppgifter

	}

	return uppgifter[aktuellAktivitet].processorTillstånd
}
