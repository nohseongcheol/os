package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "prievadas"
import . "util/sąrašas"

import . "pertraukimas"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "atmintismanager"

const SchedulerDažnumas = 1
const KernelheapPaleisti = 1024 * 1024
const schedulerDerinti = false
const pitDažnumas = 100

var sąrašas LinkedSąrašas

type Schedulerdata struct {
	dažnumas	uint32
	tickcount	uint32

	switchforced	bool

	Įjungta	bool

	dabartinisthread	*TThread
	tss			*Tssįrašas
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.dažnumas = SchedulerDažnumas
	schedata.dabartinisthread = nil
	schedata.Įjungta = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var dabartinisthreadRodyklė int = 0
var kitasProcesasid uint32 = 1

func Allocatepid() uint32 {
	pid := kitasProcesasid
	kitasProcesasid++
	return pid
}

func (self *Schedulerdata) GetKitasPasiruošęsthread() *TThread {
	if sąrašas.Dydis_2 <= 0 {
		return nil
	}

	if schedata.dabartinisthread != nil {
		dabartinisthreadRodyklė = sąrašas.Rodyklėiš(uintptr(Pointer(schedata.dabartinisthread)))
		if dabartinisthreadRodyklė < 0 {
			dabartinisthreadRodyklė = 0
		}
	} else {
		dabartinisthreadRodyklė = -1
	}

	for checked := 0; checked < sąrašas.Dydis_2; checked++ {
		dabartinisthreadRodyklė++
		if dabartinisthreadRodyklė >= sąrašas.Dydis_2 {
			dabartinisthreadRodyklė = 0
		}
		thread := (*TThread)(sąrašas.Getat(dabartinisthreadRodyklė))
		if thread != nil && thread.ThreadBūsena != Blocked && thread.ThreadBūsena != Sustabdyta {
			if schedulerDerinti {
				console_2.MSpausdinti("ti:")
				console_2.MUnsignedinteger32Spausdinti(uint32(dabartinisthreadRodyklė))
				console_2.MSpausdinti(":")
				console_2.MUnsignedinteger32Spausdinti(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.dabartinisthread

}
func (self *Scheduler) Pridėtithread(thread *TThread) {
	if thread == nil {
		return
	}
	sąrašas.Append_to_list(uintptr(Pointer(thread)))
}
func Pridėtirunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	sąrašas.Append_to_list(uintptr(Pointer(thread)))
}

func Dabartinispid() uint32 {
	if schedata.dabartinisthread == nil || schedata.dabartinisthread.Pid == 0 {
		return 1
	}
	return schedata.dabartinisthread.Pid
}

func Dabartinisparentpid() uint32 {
	if schedata.dabartinisthread == nil {
		return 0
	}
	return schedata.dabartinisthread.Parentpid
}
func (self *Scheduler) Pašalintithread(thread *TThread) {
	sąrašas.Pašalinti(uintptr(Pointer(thread)))
}

func (self *Scheduler) Pašalintithreadat(rodyklė int) {
	sąrašas.Pašalintiat(rodyklė)
}

type Scheduler struct {
	TPertraukimashandler
}

func (self *Scheduler) Init(manager *TPertraukimasmanager, mem *mem.TAtmintismanager, tss *Tssįrašas) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitDažnumas)

	sąrašas = LinkedSąrašas{}
	sąrašas.Init(mem)
	console_2.MSpausdinti("list:")
	console_2.MUnsignedinteger32Spausdinti(uint32(uintptr(Pointer(&sąrašas))))

	pertraukimashandler = pozicijaPertraukimas
	var address uintptr
	address = uintptr(Pointer(&pertraukimashandler))
	self.TPertraukimashandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Įjungta(įjungta bool) {
	schedata.Įjungta = įjungta
}

func initpit(dažnumas uint32) {
	if dažnumas == 0 {
		return
	}
	divisor := uint32(1193180) / dažnumas
	PrievadasRašymasbyte(0x43, 0x36)
	PrievadasRašymasbyte(0x40, uint8(divisor&0xFF))
	PrievadasRašymasbyte(0x40, uint8((divisor>>8)&0xFF))
}

func nustatytads(dssegment uint32)
func nustatytags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func atstatytifpregs(buffer_2 uintptr)

var jmpNaudotojas uint32 = 0
var pertraukimashandler func(uint32) uint32

func schedulestack(fn func())
func nustatytacr3(address uint32)
func getcr3() uint32

func pozicijaPertraukimas(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerDerinti {
		console_2.MSpausdintixy(([]byte)("sche1:"), 1, 17)

		console_2.MSpausdinti(":")
		console_2.MUnsignedinteger32Spausdinti(esp)
		console_2.MSpausdinti(":")

		console_2.MUnsignedinteger32Spausdinti(uint32(schedata.tickcount))
		console_2.MSpausdinti(":")
		console_2.MUnsignedinteger32Spausdinti(KernelheapPaleisti)
	}

	if schedata.tickcount == schedata.dažnumas {
		schedata.tickcount = 0

		if sąrašas.Dydis_2 > 0 && schedata.Įjungta == true {
			var kitasthread = schedata.GetKitasPasiruošęsthread()
			if kitasthread == nil {
				return esp
			}
			if schedata.dabartinisthread == nil {
				MEmergencyŽurnalasEilutė("\nSCHED first esp=")
				MEmergencyŽurnalasunsignedinteger32(esp)
				MEmergencyŽurnalasEilutė(" thread=")
				MEmergencyŽurnalasunsignedinteger32(uint32(uintptr(Pointer(kitasthread))))
				MEmergencyŽurnalasEilutė(" cpu=")
				MEmergencyŽurnalasunsignedinteger32(uint32(uintptr(Pointer(kitasthread.CpuBūsena))))
				MEmergencyŽurnalasEilutė(" state=")
				MEmergencyŽurnalasunsignedinteger32(uint32(kitasthread.ThreadBūsena))
				MEmergencyŽurnalasEilutė(" eip=")
				MEmergencyŽurnalasunsignedinteger32(kitasthread.CpuBūsena.Eip)
				MEmergencyŽurnalasEilutė(" cs=")
				MEmergencyŽurnalasunsignedinteger32(kitasthread.CpuBūsena.Cs)
				MEmergencyŽurnalasEilutė("\n")
			}

			if esp >= KernelheapPaleisti && schedata.dabartinisthread != nil {
				schedata.dabartinisthread.CpuBūsena = (*TcpuBūsena)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.dabartinisthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.dabartinisthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerDerinti {
					console_2.MSpausdinti(([]byte)("backup"))
					console_2.MUnsignedinteger32Spausdinti(esp)
				}
			}

			address := uintptr(Pointer(&(kitasthread.Fpubuffer)))
			offset := kitasthread.Fpuoffset
			if offset != 0xffffffff {
				atstatytifpregs(address + offset)
				if schedulerDerinti {
					console_2.MSpausdinti(([]byte)("restore"))
				}
			}

			schedata.dabartinisthread = kitasthread

			if schedata.dabartinisthread.ThreadBūsena == Paleista {
				schedata.dabartinisthread.ThreadBūsena = Pasiruošęs

				InitialthreadNaudotojasjump(schedata.dabartinisthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(kitasthread.CpuBūsena)))
			if kitasthread.Stack != 0 {
				schedata.tss.Nustatytastack(Segkerneldata, kitasthread.Stack+ThreadstackDydis)
			}

			nustatytacr3(kitasthread.Puslapiskatalogasįrašas)
			nustatytags(kitasthread.CpuBūsena.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Išjungtiint()

func getesp() uint32
func threadIšeitiloop()

func nustatytathreadIšeitiloopBūsena(cpuBūsena *TcpuBūsena) {
	cpuBūsena.Eip = uint32(ValueOf(threadIšeitiloop).Pointer())
	cpuBūsena.Cs = Segkernelcode
	cpuBūsena.Ds = Segkerneldata
	cpuBūsena.Es = Segkerneldata
	cpuBūsena.Fs = Segkerneldata
	cpuBūsena.Gs = Segkernelgs
	cpuBūsena.Ss = Segkerneldata
	cpuBūsena.Eflags = 0x202
}

func SustabdytiDabartinisthread(cpuBūsena *TcpuBūsena) *TcpuBūsena {
	if schedata.dabartinisthread == nil {
		nustatytathreadIšeitiloopBūsena(cpuBūsena)
		return cpuBūsena
	}

	sustabdytathread := schedata.dabartinisthread
	for i := 0; i < sąrašas.Dydis_2; i++ {
		thread := (*TThread)(sąrašas.Getat(i))
		if thread != nil && thread.CpuBūsena == cpuBūsena {
			sustabdytathread = thread
			break
		}
	}
	sustabdytathread.CpuBūsena = cpuBūsena
	sustabdytathread.ThreadBūsena = Sustabdyta
	schedata.dabartinisthread = sustabdytathread

	kitasthread := schedata.GetKitasPasiruošęsthread()
	if kitasthread == nil || kitasthread == sustabdytathread || kitasthread.CpuBūsena == nil || kitasthread.CpuBūsena == cpuBūsena {
		nustatytathreadIšeitiloopBūsena(cpuBūsena)
		return cpuBūsena
	}

	schedata.dabartinisthread = kitasthread
	if kitasthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Nustatytastack(Segkerneldata, kitasthread.Stack+ThreadstackDydis)
	}
	nustatytacr3(kitasthread.Puslapiskatalogasįrašas)
	nustatytags(kitasthread.CpuBūsena.Gs)
	return kitasthread.CpuBūsena
}

func InitialthreadNaudotojasjump(thread *TThread) {

	Išjungtiint()

	schedata.tss.Nustatytastack(Segkerneldata, thread.Stack+ThreadstackDydis)

	nustatytacr3(thread.Puslapiskatalogasįrašas)
	nustatytags(thread.CpuBūsena.Gs)

	schedata.dabartinisthread = thread
	schedata.Įjungta = true

	eip := thread.CpuBūsena.Eip
	naudotojasesp := thread.Naudotojasstack_2 + thread.NaudotojasstackDydis_2
	eflags := thread.CpuBūsena.Eflags
	cs := thread.CpuBūsena.Cs
	esp := schedata.tss.Getesp0()

	console_2.MSpausdinti(([]byte)("jump["))
	console_2.MUnsignedinteger32Spausdinti(eip)
	console_2.MSpausdinti(([]byte)(":"))
	console_2.MUnsignedinteger32Spausdinti(naudotojasesp)
	console_2.MSpausdinti(([]byte)(":"))
	console_2.MUnsignedinteger32Spausdinti(eflags)
	console_2.MSpausdinti(([]byte)(":"))
	console_2.MUnsignedinteger32Spausdinti(cs)
	console_2.MSpausdinti(([]byte)(":"))

	console_2.MUnsignedinteger32Spausdinti(esp)
	console_2.MSpausdinti(([]byte)("]"))

	userprocįrašas := thread.CpuBūsena.Ecx
	visuotinėoffsetLentelė_2 := thread.CpuBūsena.Edx
	dinaminis := thread.CpuBūsena.Esi

	PrievadasRašymasbyte(0x20, 0x20)
	jumpusermodeiret(eip, naudotojasesp, eflags, userprocįrašas, visuotinėoffsetLentelė_2, dinaminis)
	console_2.MSpausdinti(([]byte)("usermode end"))
}
func spausdintiesp(esp uint32) {
	console_2.MSpausdinti(([]byte)("esp["))
	console_2.MUnsignedinteger32Spausdinti(esp)
}
