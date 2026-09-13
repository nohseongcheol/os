package многоуправлениеЗадачами

import . "unsafe"
import . "консоль"
import . "reflect"
import mem "памятьдиспетчер"
import . "gdt"

var Проверить uint8

func halt()

type TcpuСостояние struct {
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
	стековая_память		[4096]uint8
	цПСостояние	*TcpuСостояние
}

func (текущий *TЗадача) Init(gdt *TShareddescriptorТаблица, mem *mem.TПамятьдиспетчер, записьpoint_2 func()) {

	текущий.цПСостояние = (*TcpuСостояние)(Pointer(uintptr(mem.Выделить_память(1024*1024)) + 1024*1024 - Sizeof(TcpuСостояние{})))

	текущий.цПСостояние.Eax = 0
	текущий.цПСостояние.Ebx = 0
	текущий.цПСостояние.Ecx = 0
	текущий.цПСостояние.Edx = 0

	текущий.цПСостояние.Esi = 0
	текущий.цПСостояние.Edi = 0

	текущий.цПСостояние.Gs = 0
	текущий.цПСостояние.Fs = 0
	текущий.цПСостояние.Es = 0
	текущий.цПСостояние.Ds = 0

	текущий.цПСостояние.Eip = uint32(ValueOf(записьpoint_2).Pointer())
	текущий.цПСостояние.Cs = Segядроcode
	текущий.цПСостояние.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(текущий.цПСостояние)))

	текущий.цПСостояние.Esp = stackaddress
	текущий.цПСостояние.Ebp = stackaddress
	текущий.цПСостояние.Ss = 0

}

type TЗадачадиспетчер struct {
}

var задачи [256]TЗадача
var числоЗадачи int
var текущаядатазадача int

func (текущий *TЗадачадиспетчер) Init() {
	числоЗадачи = 0
	текущаядатазадача = -1
}

func (текущий *TЗадачадиспетчер) Добавитьзадача(задача TЗадача) bool {
	if числоЗадачи >= 255 {
		return false
	}
	задачи[числоЗадачи] = задача
	числоЗадачи++
	return true
}

func (текущий *TЗадачадиспетчер) Schedule(цПСостояние *TcpuСостояние) *TcpuСостояние {

	консоль_2 := TКонсоль{}
	for i := 0; i < числоЗадачи; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(задачи[i].цПСостояние)))

		консоль_2.MUnsignedinteger32Печатьxy(x, 10, uint16(15+i))
	}
	if числоЗадачи <= 0 {
		return цПСостояние
	}

	if текущаядатазадача >= 0 {
		задачи[текущаядатазадача].цПСостояние = цПСостояние
	}

	текущаядатазадача++
	if текущаядатазадача >= числоЗадачи {
		текущаядатазадача %= числоЗадачи

	}

	return задачи[текущаядатазадача].цПСостояние
}
