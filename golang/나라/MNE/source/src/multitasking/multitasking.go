package multitasking

import . "unsafe"
import . "конзола"
import . "reflect"
import mem "memorijamanager"
import . "gdt"

var Тест uint8

func halt()

type TcpuСтање struct {
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

type TЗадатак struct {
	stack		[4096]uint8
	процесорСтање	*TcpuСтање
}

func (isti *TЗадатак) Init(gdt *TShareddescriptorTabela, mem *mem.TMemorijamanager, уносpoint_2 func()) {

	isti.процесорСтање = (*TcpuСтање)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuСтање{})))

	isti.процесорСтање.Eax = 0
	isti.процесорСтање.Ebx = 0
	isti.процесорСтање.Ecx = 0
	isti.процесорСтање.Edx = 0

	isti.процесорСтање.Esi = 0
	isti.процесорСтање.Edi = 0

	isti.процесорСтање.Gs = 0
	isti.процесорСтање.Fs = 0
	isti.процесорСтање.Es = 0
	isti.процесорСтање.Ds = 0

	isti.процесорСтање.Eip = uint32(ValueOf(уносpoint_2).Pointer())
	isti.процесорСтање.Cs = Segkernelcode
	isti.процесорСтање.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(isti.процесорСтање)))

	isti.процесорСтање.Esp = stackaddress
	isti.процесорСтање.Ebp = stackaddress
	isti.процесорСтање.Ss = 0

}

type TЗадатакmanager struct {
}

var zadaci [256]TЗадатак
var бројzadaci int
var тренутноЗадатак int

func (isti *TЗадатакmanager) Init() {
	бројzadaci = 0
	тренутноЗадатак = -1
}

func (isti *TЗадатакmanager) ДодајЗадатак(задатак TЗадатак) bool {
	if бројzadaci >= 255 {
		return false
	}
	zadaci[бројzadaci] = задатак
	бројzadaci++
	return true
}

func (isti *TЗадатакmanager) Schedule(процесорСтање *TcpuСтање) *TcpuСтање {

	конзола_2 := TКонзола{}
	for i := 0; i < бројzadaci; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(zadaci[i].процесорСтање)))

		конзола_2.MUnsignedinteger32Štampajxy(x, 10, uint16(15+i))
	}
	if бројzadaci <= 0 {
		return процесорСтање
	}

	if тренутноЗадатак >= 0 {
		zadaci[тренутноЗадатак].процесорСтање = процесорСтање
	}

	тренутноЗадатак++
	if тренутноЗадатак >= бројzadaci {
		тренутноЗадатак %= бројzadaci

	}

	return zadaci[тренутноЗадатак].процесорСтање
}
