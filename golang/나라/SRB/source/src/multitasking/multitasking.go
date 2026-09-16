/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "конзола"
import . "reflect"
import mem "меморијаmanager"
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

func (исти *TЗадатак) Init(gdt *TShareddescriptorТабела, mem *mem.TМеморијаmanager, уносpoint_2 func()) {

	исти.процесорСтање = (*TcpuСтање)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuСтање{})))

	исти.процесорСтање.Eax = 0
	исти.процесорСтање.Ebx = 0
	исти.процесорСтање.Ecx = 0
	исти.процесорСтање.Edx = 0

	исти.процесорСтање.Esi = 0
	исти.процесорСтање.Edi = 0

	исти.процесорСтање.Gs = 0
	исти.процесорСтање.Fs = 0
	исти.процесорСтање.Es = 0
	исти.процесорСтање.Ds = 0

	исти.процесорСтање.Eip = uint32(ValueOf(уносpoint_2).Pointer())
	исти.процесорСтање.Cs = Segkernelcode
	исти.процесорСтање.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(исти.процесорСтање)))

	исти.процесорСтање.Esp = stackaddress
	исти.процесорСтање.Ebp = stackaddress
	исти.процесорСтање.Ss = 0

}

type TЗадатакmanager struct {
}

var задаци [256]TЗадатак
var бројзадаци int
var тренутноЗадатак int

func (исти *TЗадатакmanager) Init() {
	бројзадаци = 0
	тренутноЗадатак = -1
}

func (исти *TЗадатакmanager) ДодајЗадатак(задатак TЗадатак) bool {
	if бројзадаци >= 255 {
		return false
	}
	задаци[бројзадаци] = задатак
	бројзадаци++
	return true
}

func (исти *TЗадатакmanager) Schedule(процесорСтање *TcpuСтање) *TcpuСтање {

	конзола_2 := TКонзола{}
	for i := 0; i < бројзадаци; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(задаци[i].процесорСтање)))

		конзола_2.MUnsignedinteger32Штампајxy(x, 10, uint16(15+i))
	}
	if бројзадаци <= 0 {
		return процесорСтање
	}

	if тренутноЗадатак >= 0 {
		задаци[тренутноЗадатак].процесорСтање = процесорСтање
	}

	тренутноЗадатак++
	if тренутноЗадатак >= бројзадаци {
		тренутноЗадатак %= бројзадаци

	}

	return задаци[тренутноЗадатак].процесорСтање
}
