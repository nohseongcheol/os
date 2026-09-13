package multitasking

import . "unsafe"
import . "konzole"
import . "reflect"
import mem "paměťmanager"
import . "gdt"

var Otestovat uint8

func halt()

type TcpuStav struct {
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

type TÚloha struct {
	paměť_zásobníku	[4096]uint8
	cpuStav	*TcpuStav
}

func (self *TÚloha) Init(gdt *TShareddescriptorTabulka, mem *mem.TPaměťmanager, záznampoint_2 func()) {

	self.cpuStav = (*TcpuStav)(Pointer(uintptr(mem.Přidělit_paměť(1024*1024)) + 1024*1024 - Sizeof(TcpuStav{})))

	self.cpuStav.Eax = 0
	self.cpuStav.Ebx = 0
	self.cpuStav.Ecx = 0
	self.cpuStav.Edx = 0

	self.cpuStav.Esi = 0
	self.cpuStav.Edi = 0

	self.cpuStav.Gs = 0
	self.cpuStav.Fs = 0
	self.cpuStav.Es = 0
	self.cpuStav.Ds = 0

	self.cpuStav.Eip = uint32(ValueOf(záznampoint_2).Pointer())
	self.cpuStav.Cs = Segkernelcode
	self.cpuStav.Eflags = 0x202

	var stackAdresa = uint32(uintptr(Pointer(self.cpuStav)))

	self.cpuStav.Esp = stackAdresa
	self.cpuStav.Ebp = stackAdresa
	self.cpuStav.Ss = 0

}

type TÚlohamanager struct {
}

var úkoly [256]TÚloha
var čísloÚkoly int
var současnýÚloha int

func (self *TÚlohamanager) Init() {
	čísloÚkoly = 0
	současnýÚloha = -1
}

func (self *TÚlohamanager) PřidatÚloha(úloha TÚloha) bool {
	if čísloÚkoly >= 255 {
		return false
	}
	úkoly[čísloÚkoly] = úloha
	čísloÚkoly++
	return true
}

func (self *TÚlohamanager) Schedule(cpuStav *TcpuStav) *TcpuStav {

	konzole_2 := TKonzole{}
	for i := 0; i < čísloÚkoly; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(úkoly[i].cpuStav)))

		konzole_2.MUnsignedinteger32Tisknoutxy(x, 10, uint16(15+i))
	}
	if čísloÚkoly <= 0 {
		return cpuStav
	}

	if současnýÚloha >= 0 {
		úkoly[současnýÚloha].cpuStav = cpuStav
	}

	současnýÚloha++
	if současnýÚloha >= čísloÚkoly {
		současnýÚloha %= čísloÚkoly

	}

	return úkoly[současnýÚloha].cpuStav
}
