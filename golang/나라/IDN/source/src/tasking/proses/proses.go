/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proses

import . "unsafe"
import . "util/tabel"
import mem "memorimanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcPenggunaheapUkuran = 1 * 1024 * 1024

type Proses struct {
	id		uint32
	syscallid	int
	IsPenggunaSpasi	bool
	arguments	*[]byte

	ThreadTabel	LinkedTabel
	Threads		*LinkedTabel
	BerkasNama	[]byte

	HalamanDirektorientri	uintptr
}

func (dirisendiri *Proses) Init(mem *mem.TMemorimanager) {
	dirisendiri.ThreadTabel = LinkedTabel{}
	dirisendiri.Threads = &dirisendiri.ThreadTabel
	dirisendiri.Threads.Init(mem)
}

type Proseshelper struct {
	proses_2			LinkedTabel
	mem				*mem.TMemorimanager
	kernelHalamanDirektorientri	uintptr
}

func (dirisendiri *Proseshelper) Init(mem *mem.TMemorimanager, kernelHalamanDirektorientri uintptr) {
	dirisendiri.mem = mem
	dirisendiri.proses_2 = LinkedTabel{}
	dirisendiri.proses_2.Init(dirisendiri.mem)
	dirisendiri.kernelHalamanDirektorientri = kernelHalamanDirektorientri
}

func (dirisendiri *Proseshelper) Create(entripoint func(), threadhelper *TThreadhelper, HalamanDirektorientri uint32, iskernel bool) Proses {
	proses := (*Proses)(dirisendiri.mem.Alokasikan_memori(uint32(Sizeof(Proses{}))))
	if proses == nil {
		return Proses{}
	}
	proses.Init(dirisendiri.mem)
	proses.id = Allocatepid()
	proses.HalamanDirektorientri = uintptr(HalamanDirektorientri)
	utamathread := threadhelper.CreatePenunjukfromFungsi(entripoint, HalamanDirektorientri, iskernel)
	if utamathread != nil {
		utamathread.Pid = proses.id
		utamathread.Orangtuapid = 0
		proses.Threads.Tambah_di_akhir_daftar(uintptr(Pointer(utamathread)))
	}

	dirisendiri.proses_2.Tambah_di_akhir_daftar(uintptr(Pointer(proses)))

	return *proses
}

func (dirisendiri *Proseshelper) Spawn(entripoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, HalamanDirektorientri uint32, iskernel bool) Proses {
	proses := dirisendiri.Create(entripoint, threadhelper, HalamanDirektorientri, iskernel)
	if proses.Threads != nil && proses.Threads.Ukuran_2 > 0 {
		thread := (*TThread)(proses.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Tambahthread(thread)
		}
	}
	return proses
}

func (dirisendiri *Proseshelper) salinHalamanDirektori(sumberentri uintptr, tujuanentri uintptr) {
	sumber_2 := Getunsignedinteger32JajaranfromPenunjuk(sumberentri, 1024, 1024)
	tujuan_2 := Getunsignedinteger32JajaranfromPenunjuk(tujuanentri, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		tujuan_2[i] = sumber_2[i]
	}
}
func (dirisendiri *Proseshelper) Createfromdata() Proses {
	proses := Proses{}
	return proses
}
