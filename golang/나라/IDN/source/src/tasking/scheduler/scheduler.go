/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/tabel"

import . "interupsi"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memorimanager"

const SchedulerFrekuensi = 1
const KernelheapMulai = 1024 * 1024
const schedulerdebug = false
const pitFrekuensi = 100

var tabel LinkedTabel

type Schedulerdata struct {
	frekuensi	uint32
	tickcount	uint32

	switchforced	bool

	Diaktifkan	bool

	sekarangthread	*TThread
	tss		*Tssentri
}

var schedata Schedulerdata = Schedulerdata{}

func (dirisendiri *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frekuensi = SchedulerFrekuensi
	schedata.sekarangthread = nil
	schedata.Diaktifkan = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var sekarangthreadIndeks int = 0
var berikutnyaProsesid uint32 = 1

func Allocatepid() uint32 {
	pid := berikutnyaProsesid
	berikutnyaProsesid++
	return pid
}

func (dirisendiri *Schedulerdata) GetBerikutnyaSiapthread() *TThread {
	if tabel.Ukuran_2 <= 0 {
		return nil
	}

	if schedata.sekarangthread != nil {
		sekarangthreadIndeks = tabel.Indeksdari(uintptr(Pointer(schedata.sekarangthread)))
		if sekarangthreadIndeks < 0 {
			sekarangthreadIndeks = 0
		}
	} else {
		sekarangthreadIndeks = -1
	}

	for checked := 0; checked < tabel.Ukuran_2; checked++ {
		sekarangthreadIndeks++
		if sekarangthreadIndeks >= tabel.Ukuran_2 {
			sekarangthreadIndeks = 0
		}
		thread := (*TThread)(tabel.Getat(sekarangthreadIndeks))
		if thread != nil && thread.ThreadStatus != Blocked && thread.ThreadStatus != Berhenti {
			if schedulerdebug {
				console_2.MCetak("ti:")
				console_2.MUnsignedinteger32Cetak(uint32(sekarangthreadIndeks))
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.sekarangthread

}
func (dirisendiri *Scheduler) Tambahthread(thread *TThread) {
	if thread == nil {
		return
	}
	tabel.Tambah_di_akhir_daftar(uintptr(Pointer(thread)))
}
func Tambahrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	tabel.Tambah_di_akhir_daftar(uintptr(Pointer(thread)))
}

func Sekarangpid() uint32 {
	if schedata.sekarangthread == nil || schedata.sekarangthread.Pid == 0 {
		return 1
	}
	return schedata.sekarangthread.Pid
}

func Sekarangorangtuapid() uint32 {
	if schedata.sekarangthread == nil {
		return 0
	}
	return schedata.sekarangthread.Orangtuapid
}
func (dirisendiri *Scheduler) Buangthread(thread *TThread) {
	tabel.Buang(uintptr(Pointer(thread)))
}

func (dirisendiri *Scheduler) Buangthreadat(indeks int) {
	tabel.Buangat(indeks)
}

type Scheduler struct {
	TInterupsihandler
}

func (dirisendiri *Scheduler) Init(manager *TInterupsimanager, mem *mem.TMemorimanager, tss *Tssentri) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitFrekuensi)

	tabel = LinkedTabel{}
	tabel.Init(mem)
	console_2.MCetak("list:")
	console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(&tabel))))

	interupsihandler = penangananInterupsi
	var address uintptr
	address = uintptr(Pointer(&interupsihandler))
	dirisendiri.TInterupsihandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (dirisendiri *Scheduler) Diaktifkan(diaktifkan bool) {
	schedata.Diaktifkan = diaktifkan
}

func initpit(frekuensi uint32) {
	if frekuensi == 0 {
		return
	}
	divisor := uint32(1193180) / frekuensi
	PortTulisbyte(0x43, 0x36)
	PortTulisbyte(0x40, uint8(divisor&0xFF))
	PortTulisbyte(0x40, uint8((divisor>>8)&0xFF))
}

func aturds(dssegment uint32)
func aturgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func kembalikanfpregs(buffer_2 uintptr)

var jmpPengguna uint32 = 0
var interupsihandler func(uint32) uint32

func schedulestack(fn func())
func aturcr3(address uint32)
func getcr3() uint32

func penangananInterupsi(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MCetakxy(([]byte)("sche1:"), 1, 17)

		console_2.MCetak(":")
		console_2.MUnsignedinteger32Cetak(esp)
		console_2.MCetak(":")

		console_2.MUnsignedinteger32Cetak(uint32(schedata.tickcount))
		console_2.MCetak(":")
		console_2.MUnsignedinteger32Cetak(KernelheapMulai)
	}

	if schedata.tickcount == schedata.frekuensi {
		schedata.tickcount = 0

		if tabel.Ukuran_2 > 0 && schedata.Diaktifkan == true {
			var berikutnyathread = schedata.GetBerikutnyaSiapthread()
			if berikutnyathread == nil {
				return esp
			}
			if schedata.sekarangthread == nil {
				MEmergencylogBenang("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogBenang(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(berikutnyathread))))
				MEmergencylogBenang(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(berikutnyathread.CpuStatus))))
				MEmergencylogBenang(" state=")
				MEmergencylogunsignedinteger32(uint32(berikutnyathread.ThreadStatus))
				MEmergencylogBenang(" eip=")
				MEmergencylogunsignedinteger32(berikutnyathread.CpuStatus.Eip)
				MEmergencylogBenang(" cs=")
				MEmergencylogunsignedinteger32(berikutnyathread.CpuStatus.Cs)
				MEmergencylogBenang("\n")
			}

			if esp >= KernelheapMulai && schedata.sekarangthread != nil {
				schedata.sekarangthread.CpuStatus = (*TcpuStatus)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.sekarangthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.sekarangthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MCetak(([]byte)("backup"))
					console_2.MUnsignedinteger32Cetak(esp)
				}
			}

			address := uintptr(Pointer(&(berikutnyathread.Fpubuffer)))
			offset := berikutnyathread.Fpuoffset
			if offset != 0xffffffff {
				kembalikanfpregs(address + offset)
				if schedulerdebug {
					console_2.MCetak(([]byte)("restore"))
				}
			}

			schedata.sekarangthread = berikutnyathread

			if schedata.sekarangthread.ThreadStatus == Dimulai {
				schedata.sekarangthread.ThreadStatus = Siap

				InitialthreadPenggunajump(schedata.sekarangthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(berikutnyathread.CpuStatus)))
			if berikutnyathread.Stack != 0 {
				schedata.tss.Aturstack(Segkerneldata, berikutnyathread.Stack+ThreadstackUkuran)
			}

			aturcr3(berikutnyathread.HalamanDirektorientri)
			aturgs(berikutnyathread.CpuStatus.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Nonaktifkanint()

func getesp() uint32
func threadKeluarloop()

func aturthreadKeluarloopStatus(cpuStatus *TcpuStatus) {
	cpuStatus.Eip = uint32(ValueOf(threadKeluarloop).Pointer())
	cpuStatus.Cs = Segkernelcode
	cpuStatus.Ds = Segkerneldata
	cpuStatus.Es = Segkerneldata
	cpuStatus.Fs = Segkerneldata
	cpuStatus.Gs = Segkernelgs
	cpuStatus.Ss = Segkerneldata
	cpuStatus.Eflags = 0x202
}

func HentikanSekarangthread(cpuStatus *TcpuStatus) *TcpuStatus {
	if schedata.sekarangthread == nil {
		aturthreadKeluarloopStatus(cpuStatus)
		return cpuStatus
	}

	berhentithread := schedata.sekarangthread
	for i := 0; i < tabel.Ukuran_2; i++ {
		thread := (*TThread)(tabel.Getat(i))
		if thread != nil && thread.CpuStatus == cpuStatus {
			berhentithread = thread
			break
		}
	}
	berhentithread.CpuStatus = cpuStatus
	berhentithread.ThreadStatus = Berhenti
	schedata.sekarangthread = berhentithread

	berikutnyathread := schedata.GetBerikutnyaSiapthread()
	if berikutnyathread == nil || berikutnyathread == berhentithread || berikutnyathread.CpuStatus == nil || berikutnyathread.CpuStatus == cpuStatus {
		aturthreadKeluarloopStatus(cpuStatus)
		return cpuStatus
	}

	schedata.sekarangthread = berikutnyathread
	if berikutnyathread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Aturstack(Segkerneldata, berikutnyathread.Stack+ThreadstackUkuran)
	}
	aturcr3(berikutnyathread.HalamanDirektorientri)
	aturgs(berikutnyathread.CpuStatus.Gs)
	return berikutnyathread.CpuStatus
}

func InitialthreadPenggunajump(thread *TThread) {

	Nonaktifkanint()

	schedata.tss.Aturstack(Segkerneldata, thread.Stack+ThreadstackUkuran)

	aturcr3(thread.HalamanDirektorientri)
	aturgs(thread.CpuStatus.Gs)

	schedata.sekarangthread = thread
	schedata.Diaktifkan = true

	eip := thread.CpuStatus.Eip
	penggunaesp := thread.Penggunastack_2 + thread.PenggunastackUkuran_2
	eflags := thread.CpuStatus.Eflags
	cs := thread.CpuStatus.Cs
	esp := schedata.tss.Getesp0()

	console_2.MCetak(([]byte)("jump["))
	console_2.MUnsignedinteger32Cetak(eip)
	console_2.MCetak(([]byte)(":"))
	console_2.MUnsignedinteger32Cetak(penggunaesp)
	console_2.MCetak(([]byte)(":"))
	console_2.MUnsignedinteger32Cetak(eflags)
	console_2.MCetak(([]byte)(":"))
	console_2.MUnsignedinteger32Cetak(cs)
	console_2.MCetak(([]byte)(":"))

	console_2.MUnsignedinteger32Cetak(esp)
	console_2.MCetak(([]byte)("]"))

	userprocentri := thread.CpuStatus.Ecx
	globaloffsetTabel_2 := thread.CpuStatus.Edx
	dinamis := thread.CpuStatus.Esi

	PortTulisbyte(0x20, 0x20)
	jumpusermodeiret(eip, penggunaesp, eflags, userprocentri, globaloffsetTabel_2, dinamis)
	console_2.MCetak(([]byte)("usermode end"))
}
func cetakesp(esp uint32) {
	console_2.MCetak(([]byte)("esp["))
	console_2.MUnsignedinteger32Cetak(esp)
}
