/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package proses

import . "unsafe"
import . "util/senarai"
import mem "ingatanmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcPenggunaheapSaiz = 1 * 1024 * 1024

type Proses struct {
	id		uint32
	syscallid	int
	IsPenggunaRuang	bool
	arguments	*[]byte

	ThreadSenarai	LinkedSenarai
	Threads		*LinkedSenarai
	FailNama	[]byte

	Halamandirektorientry	uintptr
}

func (diri *Proses) Init(mem *mem.TIngatanmanager) {
	diri.ThreadSenarai = LinkedSenarai{}
	diri.Threads = &diri.ThreadSenarai
	diri.Threads.Init(mem)
}

type Proseshelper struct {
	proses_2			LinkedSenarai
	mem				*mem.TIngatanmanager
	kernelHalamandirektorientry	uintptr
}

func (diri *Proseshelper) Init(mem *mem.TIngatanmanager, kernelHalamandirektorientry uintptr) {
	diri.mem = mem
	diri.proses_2 = LinkedSenarai{}
	diri.proses_2.Init(diri.mem)
	diri.kernelHalamandirektorientry = kernelHalamandirektorientry
}

func (diri *Proseshelper) Create(entrypoint func(), threadhelper *TThreadhelper, Halamandirektorientry uint32, iskernel bool) Proses {
	proses := (*Proses)(diri.mem.Peruntukkan_ingatan(uint32(Sizeof(Proses{}))))
	if proses == nil {
		return Proses{}
	}
	proses.Init(diri.mem)
	proses.id = AllocateIDP()
	proses.Halamandirektorientry = uintptr(Halamandirektorientry)
	utamathread := threadhelper.CreatePenudingfromFungsi(entrypoint, Halamandirektorientry, iskernel)
	if utamathread != nil {
		utamathread.IDP = proses.id
		utamathread.IndukIDP = 0
		proses.Threads.Tambah_di_hujung_senarai(uintptr(Pointer(utamathread)))
	}

	diri.proses_2.Tambah_di_hujung_senarai(uintptr(Pointer(proses)))

	return *proses
}

func (diri *Proseshelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Halamandirektorientry uint32, iskernel bool) Proses {
	proses := diri.Create(entrypoint, threadhelper, Halamandirektorientry, iskernel)
	if proses.Threads != nil && proses.Threads.Saiz_2 > 0 {
		thread := (*TThread)(proses.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Tambahthread(thread)
		}
	}
	return proses
}

func (diri *Proseshelper) salinHalamandirektori(sumberentry uintptr, destinationentry uintptr) {
	sumber_2 := Getunsignedinteger32TatasusunanfromPenuding(sumberentry, 1024, 1024)
	destination_2 := Getunsignedinteger32TatasusunanfromPenuding(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = sumber_2[i]
	}
}
func (diri *Proseshelper) Createfromdata() Proses {
	proses := Proses{}
	return proses
}
