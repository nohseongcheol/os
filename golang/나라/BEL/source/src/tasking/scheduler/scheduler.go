package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "poort"
import . "util/lijst"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "geheugenmanager"

const SchedulerFrequentie = 1
const KernelheapStarten = 1024 * 1024
const schedulerDebuggen = false
const pitFrequentie = 100

var lijst LinkedLijst

type Schedulerdata struct {
	frequentie	uint32
	tickAantal	uint32

	switchforced	bool

	Ingeschakeld	bool

	huidigthread	*TThread
	tss		*TssItem
}

var schedata Schedulerdata = Schedulerdata{}

func (zelf *Schedulerdata) Init() {
	schedata.tickAantal = 0
	schedata.frequentie = SchedulerFrequentie
	schedata.huidigthread = nil
	schedata.Ingeschakeld = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var huidigthreadindex int = 0
var volgendeProcesid uint32 = 1

func Allocatepid() uint32 {
	pid := volgendeProcesid
	volgendeProcesid++
	return pid
}

func (zelf *Schedulerdata) GetVolgendeKlaarthread() *TThread {
	if lijst.Grootte_2 <= 0 {
		return nil
	}

	if schedata.huidigthread != nil {
		huidigthreadindex = lijst.Indexvan(uintptr(Pointer(schedata.huidigthread)))
		if huidigthreadindex < 0 {
			huidigthreadindex = 0
		}
	} else {
		huidigthreadindex = -1
	}

	for checked := 0; checked < lijst.Grootte_2; checked++ {
		huidigthreadindex++
		if huidigthreadindex >= lijst.Grootte_2 {
			huidigthreadindex = 0
		}
		thread := (*TThread)(lijst.Getat(huidigthreadindex))
		if thread != nil && thread.ThreadStatus != Blocked && thread.ThreadStatus != Gestaakt {
			if schedulerDebuggen {
				console_2.MAfdrukken("ti:")
				console_2.MUnsignedinteger32Afdrukken(uint32(huidigthreadindex))
				console_2.MAfdrukken(":")
				console_2.MUnsignedinteger32Afdrukken(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.huidigthread

}
func (zelf *Scheduler) Toevoegenthread(thread *TThread) {
	if thread == nil {
		return
	}
	lijst.Achteraan_toevoegen(uintptr(Pointer(thread)))
}
func Toevoegenrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	lijst.Achteraan_toevoegen(uintptr(Pointer(thread)))
}

func Huidigpid() uint32 {
	if schedata.huidigthread == nil || schedata.huidigthread.Pid == 0 {
		return 1
	}
	return schedata.huidigthread.Pid
}

func Huidigouderpid() uint32 {
	if schedata.huidigthread == nil {
		return 0
	}
	return schedata.huidigthread.Ouderpid
}
func (zelf *Scheduler) Verwijderenthread(thread *TThread) {
	lijst.Verwijderen_2(uintptr(Pointer(thread)))
}

func (zelf *Scheduler) Verwijderenthreadat(index int) {
	lijst.Verwijderenat(index)
}

type Scheduler struct {
	TInterrupthandler
}

func (zelf *Scheduler) Init(manager *TInterruptmanager, mem *mem.TGeheugenmanager, tss *TssItem) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitFrequentie)

	lijst = LinkedLijst{}
	lijst.Init(mem)
	console_2.MAfdrukken("list:")
	console_2.MUnsignedinteger32Afdrukken(uint32(uintptr(Pointer(&lijst))))

	interrupthandler = handgreepinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	zelf.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (zelf *Scheduler) Ingeschakeld(ingeschakeld bool) {
	schedata.Ingeschakeld = ingeschakeld
}

func initpit(frequentie uint32) {
	if frequentie == 0 {
		return
	}
	divisor := uint32(1193180) / frequentie
	PoortSchrijvenbyte(0x43, 0x36)
	PoortSchrijvenbyte(0x40, uint8(divisor&0xFF))
	PoortSchrijvenbyte(0x40, uint8((divisor>>8)&0xFF))
}

func instellends(dssegment uint32)
func instellengs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func herstellenfpregs(buffer_2 uintptr)

var jmpGebruiker uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func instellencr3(address uint32)
func getcr3() uint32

func handgreepinterrupt(esp uint32) uint32 {

	schedata.tickAantal++

	if schedulerDebuggen {
		console_2.MAfdrukkenxy(([]byte)("sche1:"), 1, 17)

		console_2.MAfdrukken(":")
		console_2.MUnsignedinteger32Afdrukken(esp)
		console_2.MAfdrukken(":")

		console_2.MUnsignedinteger32Afdrukken(uint32(schedata.tickAantal))
		console_2.MAfdrukken(":")
		console_2.MUnsignedinteger32Afdrukken(KernelheapStarten)
	}

	if schedata.tickAantal == schedata.frequentie {
		schedata.tickAantal = 0

		if lijst.Grootte_2 > 0 && schedata.Ingeschakeld == true {
			var volgendethread = schedata.GetVolgendeKlaarthread()
			if volgendethread == nil {
				return esp
			}
			if schedata.huidigthread == nil {
				MEmergencyLogboekTekstsnoer("\nSCHED first esp=")
				MEmergencyLogboekunsignedinteger32(esp)
				MEmergencyLogboekTekstsnoer(" thread=")
				MEmergencyLogboekunsignedinteger32(uint32(uintptr(Pointer(volgendethread))))
				MEmergencyLogboekTekstsnoer(" cpu=")
				MEmergencyLogboekunsignedinteger32(uint32(uintptr(Pointer(volgendethread.CpuStatus))))
				MEmergencyLogboekTekstsnoer(" state=")
				MEmergencyLogboekunsignedinteger32(uint32(volgendethread.ThreadStatus))
				MEmergencyLogboekTekstsnoer(" eip=")
				MEmergencyLogboekunsignedinteger32(volgendethread.CpuStatus.Eip)
				MEmergencyLogboekTekstsnoer(" cs=")
				MEmergencyLogboekunsignedinteger32(volgendethread.CpuStatus.Cs)
				MEmergencyLogboekTekstsnoer("\n")
			}

			if esp >= KernelheapStarten && schedata.huidigthread != nil {
				schedata.huidigthread.CpuStatus = (*TcpuStatus)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.huidigthread.Fpubuffer)))
				verschuiving := (16 - (address % 16)) & 0xF
				schedata.huidigthread.FpuVerschuiving = verschuiving
				backupfpregs(address + verschuiving)
				if schedulerDebuggen {
					console_2.MAfdrukken(([]byte)("backup"))
					console_2.MUnsignedinteger32Afdrukken(esp)
				}
			}

			address := uintptr(Pointer(&(volgendethread.Fpubuffer)))
			verschuiving := volgendethread.FpuVerschuiving
			if verschuiving != 0xffffffff {
				herstellenfpregs(address + verschuiving)
				if schedulerDebuggen {
					console_2.MAfdrukken(([]byte)("restore"))
				}
			}

			schedata.huidigthread = volgendethread

			if schedata.huidigthread.ThreadStatus == Gestart {
				schedata.huidigthread.ThreadStatus = Klaar

				InitialthreadGebruikerjump(schedata.huidigthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(volgendethread.CpuStatus)))
			if volgendethread.Stack != 0 {
				schedata.tss.Instellenstack(Segkerneldata, volgendethread.Stack+ThreadstackGrootte)
			}

			instellencr3(volgendethread.PaginaMapItem)
			instellengs(volgendethread.CpuStatus.Gs)

		}

	}

	return esp
}

func jumpGebruikermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Uitschakelenint()

func getesp() uint32
func threadAfsluitenloop()

func instellenthreadAfsluitenloopStatus(cpuStatus *TcpuStatus) {
	cpuStatus.Eip = uint32(ValueOf(threadAfsluitenloop).Pointer())
	cpuStatus.Cs = Segkernelcode
	cpuStatus.Ds = Segkerneldata
	cpuStatus.Es = Segkerneldata
	cpuStatus.Fs = Segkerneldata
	cpuStatus.Gs = Segkernelgs
	cpuStatus.Ss = Segkerneldata
	cpuStatus.Eflags = 0x202
}

func StoppenHuidigthread(cpuStatus *TcpuStatus) *TcpuStatus {
	if schedata.huidigthread == nil {
		instellenthreadAfsluitenloopStatus(cpuStatus)
		return cpuStatus
	}

	gestaaktthread := schedata.huidigthread
	for i := 0; i < lijst.Grootte_2; i++ {
		thread := (*TThread)(lijst.Getat(i))
		if thread != nil && thread.CpuStatus == cpuStatus {
			gestaaktthread = thread
			break
		}
	}
	gestaaktthread.CpuStatus = cpuStatus
	gestaaktthread.ThreadStatus = Gestaakt
	schedata.huidigthread = gestaaktthread

	volgendethread := schedata.GetVolgendeKlaarthread()
	if volgendethread == nil || volgendethread == gestaaktthread || volgendethread.CpuStatus == nil || volgendethread.CpuStatus == cpuStatus {
		instellenthreadAfsluitenloopStatus(cpuStatus)
		return cpuStatus
	}

	schedata.huidigthread = volgendethread
	if volgendethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Instellenstack(Segkerneldata, volgendethread.Stack+ThreadstackGrootte)
	}
	instellencr3(volgendethread.PaginaMapItem)
	instellengs(volgendethread.CpuStatus.Gs)
	return volgendethread.CpuStatus
}

func InitialthreadGebruikerjump(thread *TThread) {

	Uitschakelenint()

	schedata.tss.Instellenstack(Segkerneldata, thread.Stack+ThreadstackGrootte)

	instellencr3(thread.PaginaMapItem)
	instellengs(thread.CpuStatus.Gs)

	schedata.huidigthread = thread
	schedata.Ingeschakeld = true

	eip := thread.CpuStatus.Eip
	gebruikeresp := thread.Gebruikerstack_2 + thread.GebruikerstackGrootte_2
	eflags := thread.CpuStatus.Eflags
	cs := thread.CpuStatus.Cs
	esp := schedata.tss.Getesp0()

	console_2.MAfdrukken(([]byte)("jump["))
	console_2.MUnsignedinteger32Afdrukken(eip)
	console_2.MAfdrukken(([]byte)(":"))
	console_2.MUnsignedinteger32Afdrukken(gebruikeresp)
	console_2.MAfdrukken(([]byte)(":"))
	console_2.MUnsignedinteger32Afdrukken(eflags)
	console_2.MAfdrukken(([]byte)(":"))
	console_2.MUnsignedinteger32Afdrukken(cs)
	console_2.MAfdrukken(([]byte)(":"))

	console_2.MUnsignedinteger32Afdrukken(esp)
	console_2.MAfdrukken(([]byte)("]"))

	userprocItem := thread.CpuStatus.Ecx
	algemeenVerschuivingTabel_2 := thread.CpuStatus.Edx
	dynamisch := thread.CpuStatus.Esi

	PoortSchrijvenbyte(0x20, 0x20)
	jumpGebruikermodeiret(eip, gebruikeresp, eflags, userprocItem, algemeenVerschuivingTabel_2, dynamisch)
	console_2.MAfdrukken(([]byte)("usermode end"))
}
func afdrukkenesp(esp uint32) {
	console_2.MAfdrukken(([]byte)("esp["))
	console_2.MUnsignedinteger32Afdrukken(esp)
}
