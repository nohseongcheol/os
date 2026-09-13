package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "ingatanmanager"
import . "gdt"

var Uji uint8

func halt()

type TcpuKeadaan struct {
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

type TTugas struct {
	ingatan_tindanan		[4096]uint8
	cpuKeadaan	*TcpuKeadaan
}

func (diri *TTugas) Init(gdt *TShareddescriptorJadual, mem *mem.TIngatanmanager, entrypoint_2 func()) {

	diri.cpuKeadaan = (*TcpuKeadaan)(Pointer(uintptr(mem.Peruntukkan_ingatan(1024*1024)) + 1024*1024 - Sizeof(TcpuKeadaan{})))

	diri.cpuKeadaan.Eax = 0
	diri.cpuKeadaan.Ebx = 0
	diri.cpuKeadaan.Ecx = 0
	diri.cpuKeadaan.Edx = 0

	diri.cpuKeadaan.Esi = 0
	diri.cpuKeadaan.Edi = 0

	diri.cpuKeadaan.Gs = 0
	diri.cpuKeadaan.Fs = 0
	diri.cpuKeadaan.Es = 0
	diri.cpuKeadaan.Ds = 0

	diri.cpuKeadaan.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	diri.cpuKeadaan.Cs = Segkernelcode
	diri.cpuKeadaan.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(diri.cpuKeadaan)))

	diri.cpuKeadaan.Esp = stackaddress
	diri.cpuKeadaan.Ebp = stackaddress
	diri.cpuKeadaan.Ss = 0

}

type TTugasmanager struct {
}

var tugas_2 [256]TTugas
var nOMBORTugas int
var semasaTugas int

func (diri *TTugasmanager) Init() {
	nOMBORTugas = 0
	semasaTugas = -1
}

func (diri *TTugasmanager) TambahTugas(tugas TTugas) bool {
	if nOMBORTugas >= 255 {
		return false
	}
	tugas_2[nOMBORTugas] = tugas
	nOMBORTugas++
	return true
}

func (diri *TTugasmanager) Schedule(cpuKeadaan *TcpuKeadaan) *TcpuKeadaan {

	console_2 := TConsole{}
	for i := 0; i < nOMBORTugas; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tugas_2[i].cpuKeadaan)))

		console_2.MUnsignedinteger32Cetakxy(x, 10, uint16(15+i))
	}
	if nOMBORTugas <= 0 {
		return cpuKeadaan
	}

	if semasaTugas >= 0 {
		tugas_2[semasaTugas].cpuKeadaan = cpuKeadaan
	}

	semasaTugas++
	if semasaTugas >= nOMBORTugas {
		semasaTugas %= nOMBORTugas

	}

	return tugas_2[semasaTugas].cpuKeadaan
}
