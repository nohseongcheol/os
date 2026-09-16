/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "konzola"
import . "reflect"
import mem "memorijamanager"
import . "gdt"

var Test uint8

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

func (isti *TZadatak) Init(gdt *TShareddescriptorTabela, mem *mem.TMemorijamanager, unospoint_2 func()) {

	isti.procesorStanje = (*TcpuStanje)(Pointer(uintptr(mem.Malloc(1024*1024)) + 1024*1024 - Sizeof(TcpuStanje{})))

	isti.procesorStanje.Eax = 0
	isti.procesorStanje.Ebx = 0
	isti.procesorStanje.Ecx = 0
	isti.procesorStanje.Edx = 0

	isti.procesorStanje.Esi = 0
	isti.procesorStanje.Edi = 0

	isti.procesorStanje.Gs = 0
	isti.procesorStanje.Fs = 0
	isti.procesorStanje.Es = 0
	isti.procesorStanje.Ds = 0

	isti.procesorStanje.Eip = uint32(ValueOf(unospoint_2).Pointer())
	isti.procesorStanje.Cs = Segkernelcode
	isti.procesorStanje.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(isti.procesorStanje)))

	isti.procesorStanje.Esp = stackaddress
	isti.procesorStanje.Ebp = stackaddress
	isti.procesorStanje.Ss = 0

}

type TZadatakmanager struct {
}

var zadaci [256]TZadatak
var brojzadaci int
var trenutnoZadatak int

func (isti *TZadatakmanager) Init() {
	brojzadaci = 0
	trenutnoZadatak = -1
}

func (isti *TZadatakmanager) DodajZadatak(zadatak TZadatak) bool {
	if brojzadaci >= 255 {
		return false
	}
	zadaci[brojzadaci] = zadatak
	brojzadaci++
	return true
}

func (isti *TZadatakmanager) Schedule(procesorStanje *TcpuStanje) *TcpuStanje {

	konzola_2 := TKonzola{}
	for i := 0; i < brojzadaci; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(zadaci[i].procesorStanje)))

		konzola_2.MUnsignedinteger32Štampajxy(x, 10, uint16(15+i))
	}
	if brojzadaci <= 0 {
		return procesorStanje
	}

	if trenutnoZadatak >= 0 {
		zadaci[trenutnoZadatak].procesorStanje = procesorStanje
	}

	trenutnoZadatak++
	if trenutnoZadatak >= brojzadaci {
		trenutnoZadatak %= brojzadaci

	}

	return zadaci[trenutnoZadatak].procesorStanje
}
