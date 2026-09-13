package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "atmintismanager"
import . "gdt"

var Testas uint8

func halt()

type TcpuBūsena struct {
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

type TUžduotis struct {
	stack		[4096]uint8
	cpuBūsena	*TcpuBūsena
}

func (self *TUžduotis) Init(gdt *TShareddescriptorLentelė, mem *mem.TAtmintismanager, įrašaspoint_2 func()) {

	self.cpuBūsena = (*TcpuBūsena)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuBūsena{})))

	self.cpuBūsena.Eax = 0
	self.cpuBūsena.Ebx = 0
	self.cpuBūsena.Ecx = 0
	self.cpuBūsena.Edx = 0

	self.cpuBūsena.Esi = 0
	self.cpuBūsena.Edi = 0

	self.cpuBūsena.Gs = 0
	self.cpuBūsena.Fs = 0
	self.cpuBūsena.Es = 0
	self.cpuBūsena.Ds = 0

	self.cpuBūsena.Eip = uint32(ValueOf(įrašaspoint_2).Pointer())
	self.cpuBūsena.Cs = Segkernelcode
	self.cpuBūsena.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.cpuBūsena)))

	self.cpuBūsena.Esp = stackaddress
	self.cpuBūsena.Ebp = stackaddress
	self.cpuBūsena.Ss = 0

}

type TUžduotismanager struct {
}

var užduotys [256]TUžduotis
var skaičiusUžduotys int
var dabartinisUžduotis int

func (self *TUžduotismanager) Init() {
	skaičiusUžduotys = 0
	dabartinisUžduotis = -1
}

func (self *TUžduotismanager) PridėtiUžduotis(užduotis TUžduotis) bool {
	if skaičiusUžduotys >= 255 {
		return false
	}
	užduotys[skaičiusUžduotys] = užduotis
	skaičiusUžduotys++
	return true
}

func (self *TUžduotismanager) Schedule(cpuBūsena *TcpuBūsena) *TcpuBūsena {

	console_2 := TConsole{}
	for i := 0; i < skaičiusUžduotys; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(užduotys[i].cpuBūsena)))

		console_2.MUnsignedinteger32Spausdintixy(x, 10, uint16(15+i))
	}
	if skaičiusUžduotys <= 0 {
		return cpuBūsena
	}

	if dabartinisUžduotis >= 0 {
		užduotys[dabartinisUžduotis].cpuBūsena = cpuBūsena
	}

	dabartinisUžduotis++
	if dabartinisUžduotis >= skaičiusUžduotys {
		dabartinisUžduotis %= skaičiusUžduotys

	}

	return užduotys[dabartinisUžduotis].cpuBūsena
}
