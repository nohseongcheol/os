package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "памяцьmanager"
import . "gdt"

var Праверка uint8

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
	stack	[4096]uint8
	цПСтан	*TcpuСтан
}

func (self *TЗадача) Init(gdt *TShareddescriptorТабліца, mem *mem.TПамяцьmanager, entrypoint_2 func()) {

	self.цПСтан = (*TcpuСтан)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuСтан{})))

	self.цПСтан.Eax = 0
	self.цПСтан.Ebx = 0
	self.цПСтан.Ecx = 0
	self.цПСтан.Edx = 0

	self.цПСтан.Esi = 0
	self.цПСтан.Edi = 0

	self.цПСтан.Gs = 0
	self.цПСтан.Fs = 0
	self.цПСтан.Es = 0
	self.цПСтан.Ds = 0

	self.цПСтан.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	self.цПСтан.Cs = Segkernelcode
	self.цПСтан.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.цПСтан)))

	self.цПСтан.Esp = stackaddress
	self.цПСтан.Ebp = stackaddress
	self.цПСтан.Ss = 0

}

type TЗадачаmanager struct {
}

var заданні [256]TЗадача
var нУМАРЗаданні int
var дзейныЗадача int

func (self *TЗадачаmanager) Init() {
	нУМАРЗаданні = 0
	дзейныЗадача = -1
}

func (self *TЗадачаmanager) ДадацьЗадача(задача TЗадача) bool {
	if нУМАРЗаданні >= 255 {
		return false
	}
	заданні[нУМАРЗаданні] = задача
	нУМАРЗаданні++
	return true
}

func (self *TЗадачаmanager) Schedule(цПСтан *TcpuСтан) *TcpuСтан {

	console_2 := TConsole{}
	for i := 0; i < нУМАРЗаданні; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(заданні[i].цПСтан)))

		console_2.MUnsignedinteger32Друкавацьxy(x, 10, uint16(15+i))
	}
	if нУМАРЗаданні <= 0 {
		return цПСтан
	}

	if дзейныЗадача >= 0 {
		заданні[дзейныЗадача].цПСтан = цПСтан
	}

	дзейныЗадача++
	if дзейныЗадача >= нУМАРЗаданні {
		дзейныЗадача %= нУМАРЗаданні

	}

	return заданні[дзейныЗадача].цПСтан
}
