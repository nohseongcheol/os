/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package multitasking

import . "unsafe"
import . "console"
import . "reflect"
import mem "memorimanager"
import . "gdt"

var Tes uint8

func halt()

type TcpuStatus struct {
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
	memori_tumpukan		[4096]uint8
	cpuStatus	*TcpuStatus
}

func (dirisendiri *TTugas) Init(gdt *TShareddescriptorTabel, mem *mem.TMemorimanager, entripoint_2 func()) {

	dirisendiri.cpuStatus = (*TcpuStatus)(Pointer(uintptr(mem.Alokasikan_memori(1024*1024)) + 1024*1024 - Sizeof(TcpuStatus{})))

	dirisendiri.cpuStatus.Eax = 0
	dirisendiri.cpuStatus.Ebx = 0
	dirisendiri.cpuStatus.Ecx = 0
	dirisendiri.cpuStatus.Edx = 0

	dirisendiri.cpuStatus.Esi = 0
	dirisendiri.cpuStatus.Edi = 0

	dirisendiri.cpuStatus.Gs = 0
	dirisendiri.cpuStatus.Fs = 0
	dirisendiri.cpuStatus.Es = 0
	dirisendiri.cpuStatus.Ds = 0

	dirisendiri.cpuStatus.Eip = uint32(ValueOf(entripoint_2).Pointer())
	dirisendiri.cpuStatus.Cs = Segkernelcode
	dirisendiri.cpuStatus.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(dirisendiri.cpuStatus)))

	dirisendiri.cpuStatus.Esp = stackaddress
	dirisendiri.cpuStatus.Ebp = stackaddress
	dirisendiri.cpuStatus.Ss = 0

}

type TTugasmanager struct {
}

var tugas_2 [256]TTugas
var nomorTugas int
var sekarangTugas int

func (dirisendiri *TTugasmanager) Init() {
	nomorTugas = 0
	sekarangTugas = -1
}

func (dirisendiri *TTugasmanager) TambahTugas(tugas TTugas) bool {
	if nomorTugas >= 255 {
		return false
	}
	tugas_2[nomorTugas] = tugas
	nomorTugas++
	return true
}

func (dirisendiri *TTugasmanager) Schedule(cpuStatus *TcpuStatus) *TcpuStatus {

	console_2 := TConsole{}
	for i := 0; i < nomorTugas; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tugas_2[i].cpuStatus)))

		console_2.MUnsignedinteger32Cetakxy(x, 10, uint16(15+i))
	}
	if nomorTugas <= 0 {
		return cpuStatus
	}

	if sekarangTugas >= 0 {
		tugas_2[sekarangTugas].cpuStatus = cpuStatus
	}

	sekarangTugas++
	if sekarangTugas >= nomorTugas {
		sekarangTugas %= nomorTugas

	}

	return tugas_2[sekarangTugas].cpuStatus
}
