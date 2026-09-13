package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "memorijamanager"
import . "gdt"

var Provjeri uint8

func halt()

type TcpuStanje struct {
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

type TZadatak struct {
	stack		[4096]uint8
	procesorStanje	*TcpuStanje
}

func (sam *TZadatak) Init(gdt *TShareddescriptorTablica, mem *mem.TMemorijamanager, entrypoint_2 func()) {

	sam.procesorStanje = (*TcpuStanje)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStanje{})))

	sam.procesorStanje.Eax = 0
	sam.procesorStanje.Ebx = 0
	sam.procesorStanje.Ecx = 0
	sam.procesorStanje.Edx = 0

	sam.procesorStanje.Esi = 0
	sam.procesorStanje.Edi = 0

	sam.procesorStanje.Gs = 0
	sam.procesorStanje.Fs = 0
	sam.procesorStanje.Es = 0
	sam.procesorStanje.Ds = 0

	sam.procesorStanje.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	sam.procesorStanje.Cs = Segkernelcode
	sam.procesorStanje.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(sam.procesorStanje)))

	sam.procesorStanje.Esp = stackaddress
	sam.procesorStanje.Ebp = stackaddress
	sam.procesorStanje.Ss = 0

}

type TZadatakmanager struct {
}

var zadaci [256]TZadatak
var bROJZadaci int
var trenutnoZadatak int

func (sam *TZadatakmanager) Init() {
	bROJZadaci = 0
	trenutnoZadatak = -1
}

func (sam *TZadatakmanager) DodajZadatak(zadatak TZadatak) bool {
	if bROJZadaci >= 255 {
		return false
	}
	zadaci[bROJZadaci] = zadatak
	bROJZadaci++
	return true
}

func (sam *TZadatakmanager) Schedule(procesorStanje *TcpuStanje) *TcpuStanje {

	console_2 := TConsole{}
	for i := 0; i < bROJZadaci; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(zadaci[i].procesorStanje)))

		console_2.MUnsignedinteger32Ispisxy(x, 10, uint16(15+i))
	}
	if bROJZadaci <= 0 {
		return procesorStanje
	}

	if trenutnoZadatak >= 0 {
		zadaci[trenutnoZadatak].procesorStanje = procesorStanje
	}

	trenutnoZadatak++
	if trenutnoZadatak >= bROJZadaci {
		trenutnoZadatak %= bROJZadaci

	}

	return zadaci[trenutnoZadatak].procesorStanje
}
