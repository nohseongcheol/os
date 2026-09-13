package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "паметmanager"
import . "gdt"

var Тест uint8

func halt()

type TcpuСъстояние struct {
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

type TЗадача struct {
	stack			[4096]uint8
	процесорСъстояние	*TcpuСъстояние
}

func (себеси *TЗадача) Init(gdt *TShareddescriptorТаблица, mem *mem.TПаметmanager, записpoint_2 func()) {

	себеси.процесорСъстояние = (*TcpuСъстояние)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuСъстояние{})))

	себеси.процесорСъстояние.Eax = 0
	себеси.процесорСъстояние.Ebx = 0
	себеси.процесорСъстояние.Ecx = 0
	себеси.процесорСъстояние.Edx = 0

	себеси.процесорСъстояние.Esi = 0
	себеси.процесорСъстояние.Edi = 0

	себеси.процесорСъстояние.Gs = 0
	себеси.процесорСъстояние.Fs = 0
	себеси.процесорСъстояние.Es = 0
	себеси.процесорСъстояние.Ds = 0

	себеси.процесорСъстояние.Eip = uint32(ValueOf(записpoint_2).Pointer())
	себеси.процесорСъстояние.Cs = Segkernelcode
	себеси.процесорСъстояние.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(себеси.процесорСъстояние)))

	себеси.процесорСъстояние.Esp = stackaddress
	себеси.процесорСъстояние.Ebp = stackaddress
	себеси.процесорСъстояние.Ss = 0

}

type TЗадачаmanager struct {
}

var задачи [256]TЗадача
var числоЗадачи int
var текущадатаЗадача int

func (себеси *TЗадачаmanager) Init() {
	числоЗадачи = 0
	текущадатаЗадача = -1
}

func (себеси *TЗадачаmanager) ДобавянеЗадача(задача TЗадача) bool {
	if числоЗадачи >= 255 {
		return false
	}
	задачи[числоЗадачи] = задача
	числоЗадачи++
	return true
}

func (себеси *TЗадачаmanager) Schedule(процесорСъстояние *TcpuСъстояние) *TcpuСъстояние {

	console_2 := TConsole{}
	for i := 0; i < числоЗадачи; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(задачи[i].процесорСъстояние)))

		console_2.MUnsignedinteger32Печатxy(x, 10, uint16(15+i))
	}
	if числоЗадачи <= 0 {
		return процесорСъстояние
	}

	if текущадатаЗадача >= 0 {
		задачи[текущадатаЗадача].процесорСъстояние = процесорСъстояние
	}

	текущадатаЗадача++
	if текущадатаЗадача >= числоЗадачи {
		текущадатаЗадача %= числоЗадачи

	}

	return задачи[текущадатаЗадача].процесорСъстояние
}
