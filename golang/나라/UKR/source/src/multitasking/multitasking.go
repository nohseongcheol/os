package multitasking

import . "unsafe"
import . "консоль"
import . "reflect"
import mem "памятьmanager"
import . "gdt"

var Тест uint8

func halt()

type TcpuСтан struct {
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
	стекова_памʼять		[4096]uint8
	процесорСтан	*TcpuСтан
}

func (поточний *TЗадача) Init(gdt *TShareddescriptorТаблиця, mem *mem.TПамятьmanager, записpoint_2 func()) {

	поточний.процесорСтан = (*TcpuСтан)(Pointer(uintptr(mem.Виділити_памʼять(1024*1024)) + 1024*1024 - Sizeof(TcpuСтан{})))

	поточний.процесорСтан.Eax = 0
	поточний.процесорСтан.Ebx = 0
	поточний.процесорСтан.Ecx = 0
	поточний.процесорСтан.Edx = 0

	поточний.процесорСтан.Esi = 0
	поточний.процесорСтан.Edi = 0

	поточний.процесорСтан.Gs = 0
	поточний.процесорСтан.Fs = 0
	поточний.процесорСтан.Es = 0
	поточний.процесорСтан.Ds = 0

	поточний.процесорСтан.Eip = uint32(ValueOf(записpoint_2).Pointer())
	поточний.процесорСтан.Cs = Segkernelcode
	поточний.процесорСтан.Eflags = 0x202

	var stackАдреса = uint32(uintptr(Pointer(поточний.процесорСтан)))

	поточний.процесорСтан.Esp = stackАдреса
	поточний.процесорСтан.Ebp = stackАдреса
	поточний.процесорСтан.Ss = 0

}

type TЗадачаmanager struct {
}

var завдання [256]TЗадача
var числоЗавдання int
var поточнаЗадача int

func (поточний *TЗадачаmanager) Init() {
	числоЗавдання = 0
	поточнаЗадача = -1
}

func (поточний *TЗадачаmanager) ДодатиЗадача(задача TЗадача) bool {
	if числоЗавдання >= 255 {
		return false
	}
	завдання[числоЗавдання] = задача
	числоЗавдання++
	return true
}

func (поточний *TЗадачаmanager) Schedule(процесорСтан *TcpuСтан) *TcpuСтан {

	консоль_2 := TКонсоль{}
	for i := 0; i < числоЗавдання; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(завдання[i].процесорСтан)))

		консоль_2.MUnsignedinteger32Друкxy(x, 10, uint16(15+i))
	}
	if числоЗавдання <= 0 {
		return процесорСтан
	}

	if поточнаЗадача >= 0 {
		завдання[поточнаЗадача].процесорСтан = процесорСтан
	}

	поточнаЗадача++
	if поточнаЗадача >= числоЗавдання {
		поточнаЗадача %= числоЗавдання

	}

	return завдання[поточнаЗадача].процесорСтан
}
