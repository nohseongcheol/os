/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/liste"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "hukommelsemanager"

const Schedulerfrequency = 1
const KernelheapBegynd = 1024 * 1024
const schedulerFejlsøgning = false
const pitfrequency = 100

var liste LinkedListe

type Schedulerdata struct {
	frequency	uint32
	tickAntal	uint32

	switchforced	bool

	Aktiveret	bool

	aktivethread	*TThread
	tss		*Tssemne
}

var schedata Schedulerdata = Schedulerdata{}

func (selv *Schedulerdata) Init() {
	schedata.tickAntal = 0
	schedata.frequency = Schedulerfrequency
	schedata.aktivethread = nil
	schedata.Aktiveret = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var aktivethreadIndeks int = 0
var næsteProcesid uint32 = 1

func Allocatepid() uint32 {
	pid := næsteProcesid
	næsteProcesid++
	return pid
}

func (selv *Schedulerdata) GetNæsteKlarthread() *TThread {
	if liste.Størrelse_2 <= 0 {
		return nil
	}

	if schedata.aktivethread != nil {
		aktivethreadIndeks = liste.Indeksaf(uintptr(Pointer(schedata.aktivethread)))
		if aktivethreadIndeks < 0 {
			aktivethreadIndeks = 0
		}
	} else {
		aktivethreadIndeks = -1
	}

	for checked := 0; checked < liste.Størrelse_2; checked++ {
		aktivethreadIndeks++
		if aktivethreadIndeks >= liste.Størrelse_2 {
			aktivethreadIndeks = 0
		}
		thread := (*TThread)(liste.Getat(aktivethreadIndeks))
		if thread != nil && thread.ThreadStatus != Blocked && thread.ThreadStatus != Stoppet {
			if schedulerFejlsøgning {
				console_2.MUdskriv("ti:")
				console_2.MUnsignedinteger32Udskriv(uint32(aktivethreadIndeks))
				console_2.MUdskriv(":")
				console_2.MUnsignedinteger32Udskriv(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.aktivethread

}
func (selv *Scheduler) Tilføjthread(thread *TThread) {
	if thread == nil {
		return
	}
	liste.Append_to_list(uintptr(Pointer(thread)))
}
func Tilføjrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	liste.Append_to_list(uintptr(Pointer(thread)))
}

func Aktivepid() uint32 {
	if schedata.aktivethread == nil || schedata.aktivethread.Pid == 0 {
		return 1
	}
	return schedata.aktivethread.Pid
}

func Aktiveforælderpid() uint32 {
	if schedata.aktivethread == nil {
		return 0
	}
	return schedata.aktivethread.Forælderpid
}
func (selv *Scheduler) Fjernthread(thread *TThread) {
	liste.Fjern(uintptr(Pointer(thread)))
}

func (selv *Scheduler) Fjernthreadat(indeks int) {
	liste.Fjernat(indeks)
}

type Scheduler struct {
	TInterrupthandler
}

func (selv *Scheduler) Init(manager *TInterruptmanager, mem *mem.THukommelsemanager, tss *Tssemne) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	liste = LinkedListe{}
	liste.Init(mem)
	console_2.MUdskriv("list:")
	console_2.MUnsignedinteger32Udskriv(uint32(uintptr(Pointer(&liste))))

	interrupthandler = håndtaginterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	selv.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (selv *Scheduler) Aktiveret(aktiveret bool) {
	schedata.Aktiveret = aktiveret
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	PortSkrivebyte(0x43, 0x36)
	PortSkrivebyte(0x40, uint8(divisor&0xFF))
	PortSkrivebyte(0x40, uint8((divisor>>8)&0xFF))
}

func satds(dssegment uint32)
func satgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func gendanfpregs(buffer_2 uintptr)

var jmpBruger uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func satcr3(address uint32)
func getcr3() uint32

func håndtaginterrupt(esp uint32) uint32 {

	schedata.tickAntal++

	if schedulerFejlsøgning {
		console_2.MUdskrivxy(([]byte)("sche1:"), 1, 17)

		console_2.MUdskriv(":")
		console_2.MUnsignedinteger32Udskriv(esp)
		console_2.MUdskriv(":")

		console_2.MUnsignedinteger32Udskriv(uint32(schedata.tickAntal))
		console_2.MUdskriv(":")
		console_2.MUnsignedinteger32Udskriv(KernelheapBegynd)
	}

	if schedata.tickAntal == schedata.frequency {
		schedata.tickAntal = 0

		if liste.Størrelse_2 > 0 && schedata.Aktiveret == true {
			var næstethread = schedata.GetNæsteKlarthread()
			if næstethread == nil {
				return esp
			}
			if schedata.aktivethread == nil {
				MEmergencylogStreng("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogStreng(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(næstethread))))
				MEmergencylogStreng(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(næstethread.CpuStatus))))
				MEmergencylogStreng(" state=")
				MEmergencylogunsignedinteger32(uint32(næstethread.ThreadStatus))
				MEmergencylogStreng(" eip=")
				MEmergencylogunsignedinteger32(næstethread.CpuStatus.Eip)
				MEmergencylogStreng(" cs=")
				MEmergencylogunsignedinteger32(næstethread.CpuStatus.Cs)
				MEmergencylogStreng("\n")
			}

			if esp >= KernelheapBegynd && schedata.aktivethread != nil {
				schedata.aktivethread.CpuStatus = (*TcpuStatus)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.aktivethread.Fpubuffer)))
				forskydning := (16 - (address % 16)) & 0xF
				schedata.aktivethread.FpuForskydning = forskydning
				backupfpregs(address + forskydning)
				if schedulerFejlsøgning {
					console_2.MUdskriv(([]byte)("backup"))
					console_2.MUnsignedinteger32Udskriv(esp)
				}
			}

			address := uintptr(Pointer(&(næstethread.Fpubuffer)))
			forskydning := næstethread.FpuForskydning
			if forskydning != 0xffffffff {
				gendanfpregs(address + forskydning)
				if schedulerFejlsøgning {
					console_2.MUdskriv(([]byte)("restore"))
				}
			}

			schedata.aktivethread = næstethread

			if schedata.aktivethread.ThreadStatus == Startet {
				schedata.aktivethread.ThreadStatus = Klar

				InitialthreadBrugerjump(schedata.aktivethread)
				return esp
			}

			esp = uint32(uintptr(Pointer(næstethread.CpuStatus)))
			if næstethread.Stack != 0 {
				schedata.tss.Satstack(Segkerneldata, næstethread.Stack+ThreadstackStørrelse)
			}

			satcr3(næstethread.SideMappeemne)
			satgs(næstethread.CpuStatus.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func SlåfraHeltal()

func getesp() uint32
func threadAfslutLøkkekolonier()

func satthreadAfslutLøkkekolonierStatus(cpuStatus *TcpuStatus) {
	cpuStatus.Eip = uint32(ValueOf(threadAfslutLøkkekolonier).Pointer())
	cpuStatus.Cs = Segkernelcode
	cpuStatus.Ds = Segkerneldata
	cpuStatus.Es = Segkerneldata
	cpuStatus.Fs = Segkerneldata
	cpuStatus.Gs = Segkernelgs
	cpuStatus.Ss = Segkerneldata
	cpuStatus.Eflags = 0x202
}

func StopAktivethread(cpuStatus *TcpuStatus) *TcpuStatus {
	if schedata.aktivethread == nil {
		satthreadAfslutLøkkekolonierStatus(cpuStatus)
		return cpuStatus
	}

	stoppetthread := schedata.aktivethread
	for i := 0; i < liste.Størrelse_2; i++ {
		thread := (*TThread)(liste.Getat(i))
		if thread != nil && thread.CpuStatus == cpuStatus {
			stoppetthread = thread
			break
		}
	}
	stoppetthread.CpuStatus = cpuStatus
	stoppetthread.ThreadStatus = Stoppet
	schedata.aktivethread = stoppetthread

	næstethread := schedata.GetNæsteKlarthread()
	if næstethread == nil || næstethread == stoppetthread || næstethread.CpuStatus == nil || næstethread.CpuStatus == cpuStatus {
		satthreadAfslutLøkkekolonierStatus(cpuStatus)
		return cpuStatus
	}

	schedata.aktivethread = næstethread
	if næstethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Satstack(Segkerneldata, næstethread.Stack+ThreadstackStørrelse)
	}
	satcr3(næstethread.SideMappeemne)
	satgs(næstethread.CpuStatus.Gs)
	return næstethread.CpuStatus
}

func InitialthreadBrugerjump(thread *TThread) {

	SlåfraHeltal()

	schedata.tss.Satstack(Segkerneldata, thread.Stack+ThreadstackStørrelse)

	satcr3(thread.SideMappeemne)
	satgs(thread.CpuStatus.Gs)

	schedata.aktivethread = thread
	schedata.Aktiveret = true

	eip := thread.CpuStatus.Eip
	brugeresp := thread.Brugerstack_2 + thread.BrugerstackStørrelse_2
	eflags := thread.CpuStatus.Eflags
	cs := thread.CpuStatus.Cs
	esp := schedata.tss.Getesp0()

	console_2.MUdskriv(([]byte)("jump["))
	console_2.MUnsignedinteger32Udskriv(eip)
	console_2.MUdskriv(([]byte)(":"))
	console_2.MUnsignedinteger32Udskriv(brugeresp)
	console_2.MUdskriv(([]byte)(":"))
	console_2.MUnsignedinteger32Udskriv(eflags)
	console_2.MUdskriv(([]byte)(":"))
	console_2.MUnsignedinteger32Udskriv(cs)
	console_2.MUdskriv(([]byte)(":"))

	console_2.MUnsignedinteger32Udskriv(esp)
	console_2.MUdskriv(([]byte)("]"))

	userprocemne := thread.CpuStatus.Ecx
	globaltForskydningTabel_2 := thread.CpuStatus.Edx
	dynamisk := thread.CpuStatus.Esi

	PortSkrivebyte(0x20, 0x20)
	jumpusermodeiret(eip, brugeresp, eflags, userprocemne, globaltForskydningTabel_2, dynamisk)
	console_2.MUdskriv(([]byte)("usermode end"))
}
func udskrivesp(esp uint32) {
	console_2.MUdskriv(([]byte)("esp["))
	console_2.MUnsignedinteger32Udskriv(esp)
}
