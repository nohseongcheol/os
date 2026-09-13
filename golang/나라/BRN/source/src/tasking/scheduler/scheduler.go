package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/senarai"

import . "sampuk"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "ingatanmanager"

const SchedulerKekerapan = 1
const KernelheapMula = 1024 * 1024
const schedulerNyahpepijat = false
const pitKekerapan = 100

var senarai LinkedSenarai

type Schedulerdata struct {
	kekerapan	uint32
	tickcount	uint32

	switchforced	bool

	Dibenarkan	bool

	semasathread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (diri *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.kekerapan = SchedulerKekerapan
	schedata.semasathread = nil
	schedata.Dibenarkan = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var semasathreadIndeks int = 0
var berikutnyaProsesid uint32 = 1

func AllocateIDP() uint32 {
	iDP := berikutnyaProsesid
	berikutnyaProsesid++
	return iDP
}

func (diri *Schedulerdata) GetBerikutnyaSediathread() *TThread {
	if senarai.Saiz_2 <= 0 {
		return nil
	}

	if schedata.semasathread != nil {
		semasathreadIndeks = senarai.Indeksdari(uintptr(Pointer(schedata.semasathread)))
		if semasathreadIndeks < 0 {
			semasathreadIndeks = 0
		}
	} else {
		semasathreadIndeks = -1
	}

	for checked := 0; checked < senarai.Saiz_2; checked++ {
		semasathreadIndeks++
		if semasathreadIndeks >= senarai.Saiz_2 {
			semasathreadIndeks = 0
		}
		thread := (*TThread)(senarai.Getat(semasathreadIndeks))
		if thread != nil && thread.ThreadKeadaan != Blocked && thread.ThreadKeadaan != Berhenti {
			if schedulerNyahpepijat {
				console_2.MCetak("ti:")
				console_2.MUnsignedinteger32Cetak(uint32(semasathreadIndeks))
				console_2.MCetak(":")
				console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.semasathread

}
func (diri *Scheduler) Tambahthread(thread *TThread) {
	if thread == nil {
		return
	}
	senarai.Tambah_di_hujung_senarai(uintptr(Pointer(thread)))
}
func Tambahrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	senarai.Tambah_di_hujung_senarai(uintptr(Pointer(thread)))
}

func SemasaIDP() uint32 {
	if schedata.semasathread == nil || schedata.semasathread.IDP == 0 {
		return 1
	}
	return schedata.semasathread.IDP
}

func SemasaindukIDP() uint32 {
	if schedata.semasathread == nil {
		return 0
	}
	return schedata.semasathread.IndukIDP
}
func (diri *Scheduler) Buangthread(thread *TThread) {
	senarai.Buang(uintptr(Pointer(thread)))
}

func (diri *Scheduler) Buangthreadat(indeks int) {
	senarai.Buangat(indeks)
}

type Scheduler struct {
	TSampukhandler
}

func (diri *Scheduler) Init(manager *TSampukmanager, mem *mem.TIngatanmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitKekerapan)

	senarai = LinkedSenarai{}
	senarai.Init(mem)
	console_2.MCetak("list:")
	console_2.MUnsignedinteger32Cetak(uint32(uintptr(Pointer(&senarai))))

	sampukhandler = kendaliSampuk
	var address uintptr
	address = uintptr(Pointer(&sampukhandler))
	diri.TSampukhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (diri *Scheduler) Dibenarkan(dibenarkan bool) {
	schedata.Dibenarkan = dibenarkan
}

func initpit(kekerapan uint32) {
	if kekerapan == 0 {
		return
	}
	divisor := uint32(1193180) / kekerapan
	PortTulisbyte(0x43, 0x36)
	PortTulisbyte(0x40, uint8(divisor&0xFF))
	PortTulisbyte(0x40, uint8((divisor>>8)&0xFF))
}

func tetapkands(dssegment uint32)
func tetapkangs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func pulihfpregs(buffer_2 uintptr)

var jmpPengguna uint32 = 0
var sampukhandler func(uint32) uint32

func schedulestack(fn func())
func tetapkancr3(address uint32)
func getcr3() uint32

func kendaliSampuk(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerNyahpepijat {
		console_2.MCetakxy(([]byte)("sche1:"), 1, 17)

		console_2.MCetak(":")
		console_2.MUnsignedinteger32Cetak(esp)
		console_2.MCetak(":")

		console_2.MUnsignedinteger32Cetak(uint32(schedata.tickcount))
		console_2.MCetak(":")
		console_2.MUnsignedinteger32Cetak(KernelheapMula)
	}

	if schedata.tickcount == schedata.kekerapan {
		schedata.tickcount = 0

		if senarai.Saiz_2 > 0 && schedata.Dibenarkan == true {
			var berikutnyathread = schedata.GetBerikutnyaSediathread()
			if berikutnyathread == nil {
				return esp
			}
			if schedata.semasathread == nil {
				MEmergencylogRentetan("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogRentetan(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(berikutnyathread))))
				MEmergencylogRentetan(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(berikutnyathread.CpuKeadaan))))
				MEmergencylogRentetan(" state=")
				MEmergencylogunsignedinteger32(uint32(berikutnyathread.ThreadKeadaan))
				MEmergencylogRentetan(" eip=")
				MEmergencylogunsignedinteger32(berikutnyathread.CpuKeadaan.Eip)
				MEmergencylogRentetan(" cs=")
				MEmergencylogunsignedinteger32(berikutnyathread.CpuKeadaan.Cs)
				MEmergencylogRentetan("\n")
			}

			if esp >= KernelheapMula && schedata.semasathread != nil {
				schedata.semasathread.CpuKeadaan = (*TcpuKeadaan)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.semasathread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.semasathread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerNyahpepijat {
					console_2.MCetak(([]byte)("backup"))
					console_2.MUnsignedinteger32Cetak(esp)
				}
			}

			address := uintptr(Pointer(&(berikutnyathread.Fpubuffer)))
			offset := berikutnyathread.Fpuoffset
			if offset != 0xffffffff {
				pulihfpregs(address + offset)
				if schedulerNyahpepijat {
					console_2.MCetak(([]byte)("restore"))
				}
			}

			schedata.semasathread = berikutnyathread

			if schedata.semasathread.ThreadKeadaan == Bermula {
				schedata.semasathread.ThreadKeadaan = Sedia

				InitialthreadPenggunajump(schedata.semasathread)
				return esp
			}

			esp = uint32(uintptr(Pointer(berikutnyathread.CpuKeadaan)))
			if berikutnyathread.Stack != 0 {
				schedata.tss.Tetapkanstack(Segkerneldata, berikutnyathread.Stack+ThreadstackSaiz)
			}

			tetapkancr3(berikutnyathread.Halamandirektorientry)
			tetapkangs(berikutnyathread.CpuKeadaan.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Lumpuhint()

func getesp() uint32
func threadKeluarloop()

func tetapkanthreadKeluarloopKeadaan(cpuKeadaan *TcpuKeadaan) {
	cpuKeadaan.Eip = uint32(ValueOf(threadKeluarloop).Pointer())
	cpuKeadaan.Cs = Segkernelcode
	cpuKeadaan.Ds = Segkerneldata
	cpuKeadaan.Es = Segkerneldata
	cpuKeadaan.Fs = Segkerneldata
	cpuKeadaan.Gs = Segkernelgs
	cpuKeadaan.Ss = Segkerneldata
	cpuKeadaan.Eflags = 0x202
}

func HentiSemasathread(cpuKeadaan *TcpuKeadaan) *TcpuKeadaan {
	if schedata.semasathread == nil {
		tetapkanthreadKeluarloopKeadaan(cpuKeadaan)
		return cpuKeadaan
	}

	berhentithread := schedata.semasathread
	for i := 0; i < senarai.Saiz_2; i++ {
		thread := (*TThread)(senarai.Getat(i))
		if thread != nil && thread.CpuKeadaan == cpuKeadaan {
			berhentithread = thread
			break
		}
	}
	berhentithread.CpuKeadaan = cpuKeadaan
	berhentithread.ThreadKeadaan = Berhenti
	schedata.semasathread = berhentithread

	berikutnyathread := schedata.GetBerikutnyaSediathread()
	if berikutnyathread == nil || berikutnyathread == berhentithread || berikutnyathread.CpuKeadaan == nil || berikutnyathread.CpuKeadaan == cpuKeadaan {
		tetapkanthreadKeluarloopKeadaan(cpuKeadaan)
		return cpuKeadaan
	}

	schedata.semasathread = berikutnyathread
	if berikutnyathread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Tetapkanstack(Segkerneldata, berikutnyathread.Stack+ThreadstackSaiz)
	}
	tetapkancr3(berikutnyathread.Halamandirektorientry)
	tetapkangs(berikutnyathread.CpuKeadaan.Gs)
	return berikutnyathread.CpuKeadaan
}

func InitialthreadPenggunajump(thread *TThread) {

	Lumpuhint()

	schedata.tss.Tetapkanstack(Segkerneldata, thread.Stack+ThreadstackSaiz)

	tetapkancr3(thread.Halamandirektorientry)
	tetapkangs(thread.CpuKeadaan.Gs)

	schedata.semasathread = thread
	schedata.Dibenarkan = true

	eip := thread.CpuKeadaan.Eip
	penggunaesp := thread.Penggunastack_2 + thread.PenggunastackSaiz_2
	eflags := thread.CpuKeadaan.Eflags
	cs := thread.CpuKeadaan.Cs
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

	userprocentry := thread.CpuKeadaan.Ecx
	sejagatoffsetJadual_2 := thread.CpuKeadaan.Edx
	dynamic := thread.CpuKeadaan.Esi

	PortTulisbyte(0x20, 0x20)
	jumpusermodeiret(eip, penggunaesp, eflags, userprocentry, sejagatoffsetJadual_2, dynamic)
	console_2.MCetak(([]byte)("usermode end"))
}
func cetakesp(esp uint32) {
	console_2.MCetak(([]byte)("esp["))
	console_2.MUnsignedinteger32Cetak(esp)
}
