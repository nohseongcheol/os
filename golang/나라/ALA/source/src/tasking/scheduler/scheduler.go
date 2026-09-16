/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "konsol"
import . "gdt"
import . "port"
import . "util/lista"

import . "avbrott"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "minnemanager"

const SchedulerFrekvens = 1
const KernelheapStarta = 1024 * 1024
const schedulerAvlusa = false
const pitFrekvens = 100

var lista LinkedLista

type Schedulerdata struct {
	frekvens	uint32
	tickAntal	uint32

	switchforced	bool

	Aktiverad	bool

	aktuellthread	*TThread
	tss		*Tsspost
}

var schedata Schedulerdata = Schedulerdata{}

func (själv *Schedulerdata) Init() {
	schedata.tickAntal = 0
	schedata.frekvens = SchedulerFrekvens
	schedata.aktuellthread = nil
	schedata.Aktiverad = false
	schedata.switchforced = false

}

var konsol_2 = TKonsol{}
var aktuellthreadindex int = 0
var nästaprocessid uint32 = 1

func Allocateprocessid() uint32 {
	processid := nästaprocessid
	nästaprocessid++
	return processid
}

func (själv *Schedulerdata) GetNästaRedothread() *TThread {
	if lista.Storlek_2 <= 0 {
		return nil
	}

	if schedata.aktuellthread != nil {
		aktuellthreadindex = lista.Indexav(uintptr(Pointer(schedata.aktuellthread)))
		if aktuellthreadindex < 0 {
			aktuellthreadindex = 0
		}
	} else {
		aktuellthreadindex = -1
	}

	for checked := 0; checked < lista.Storlek_2; checked++ {
		aktuellthreadindex++
		if aktuellthreadindex >= lista.Storlek_2 {
			aktuellthreadindex = 0
		}
		thread := (*TThread)(lista.Getat(aktuellthreadindex))
		if thread != nil && thread.ThreadTillstånd != Blocked && thread.ThreadTillstånd != Stoppad {
			if schedulerAvlusa {
				konsol_2.MSkrivut("ti:")
				konsol_2.MUnsignedinteger32Skrivut(uint32(aktuellthreadindex))
				konsol_2.MSkrivut(":")
				konsol_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.aktuellthread

}
func (själv *Scheduler) Läggtillthread(thread *TThread) {
	if thread == nil {
		return
	}
	lista.Lägg_till_sist_i_listan(uintptr(Pointer(thread)))
}
func Läggtillrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	lista.Lägg_till_sist_i_listan(uintptr(Pointer(thread)))
}

func Aktuellprocessid() uint32 {
	if schedata.aktuellthread == nil || schedata.aktuellthread.Processid == 0 {
		return 1
	}
	return schedata.aktuellthread.Processid
}

func Aktuellförälderprocessid() uint32 {
	if schedata.aktuellthread == nil {
		return 0
	}
	return schedata.aktuellthread.Förälderprocessid
}
func (själv *Scheduler) Tabortthread(thread *TThread) {
	lista.Tabort_2(uintptr(Pointer(thread)))
}

func (själv *Scheduler) Tabortthreadat(index int) {
	lista.Tabortat(index)
}

type Scheduler struct {
	TAvbrotthandler
}

func (själv *Scheduler) Init(manager *TAvbrottmanager, mem *mem.TMinnemanager, tss *Tsspost) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitFrekvens)

	lista = LinkedLista{}
	lista.Init(mem)
	konsol_2.MSkrivut("list:")
	konsol_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(&lista))))

	avbrotthandler = handtagAvbrott
	var adress uintptr
	adress = uintptr(Pointer(&avbrotthandler))
	själv.TAvbrotthandler.Init(0x20, uintptr(Pointer(manager)), adress)
}

func (själv *Scheduler) Aktiverad(aktiverad bool) {
	schedata.Aktiverad = aktiverad
}

func initpit(frekvens uint32) {
	if frekvens == 0 {
		return
	}
	divisor := uint32(1193180) / frekvens
	PortSkrivbyte(0x43, 0x36)
	PortSkrivbyte(0x40, uint8(divisor&0xFF))
	PortSkrivbyte(0x40, uint8((divisor>>8)&0xFF))
}

func mängdds(dssegment uint32)
func mängdgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func återställfpregs(buffer_2 uintptr)

var jmpAnvändare uint32 = 0
var avbrotthandler func(uint32) uint32

func schedulestack(fn func())
func mängdcr3(adress uint32)
func getcr3() uint32

func handtagAvbrott(esp uint32) uint32 {

	schedata.tickAntal++

	if schedulerAvlusa {
		konsol_2.MSkrivutxy(([]byte)("sche1:"), 1, 17)

		konsol_2.MSkrivut(":")
		konsol_2.MUnsignedinteger32Skrivut(esp)
		konsol_2.MSkrivut(":")

		konsol_2.MUnsignedinteger32Skrivut(uint32(schedata.tickAntal))
		konsol_2.MSkrivut(":")
		konsol_2.MUnsignedinteger32Skrivut(KernelheapStarta)
	}

	if schedata.tickAntal == schedata.frekvens {
		schedata.tickAntal = 0

		if lista.Storlek_2 > 0 && schedata.Aktiverad == true {
			var nästathread = schedata.GetNästaRedothread()
			if nästathread == nil {
				return esp
			}
			if schedata.aktuellthread == nil {
				MEmergencyLoggsträng("\nSCHED first esp=")
				MEmergencyLoggunsignedinteger32(esp)
				MEmergencyLoggsträng(" thread=")
				MEmergencyLoggunsignedinteger32(uint32(uintptr(Pointer(nästathread))))
				MEmergencyLoggsträng(" cpu=")
				MEmergencyLoggunsignedinteger32(uint32(uintptr(Pointer(nästathread.ProcessorTillstånd))))
				MEmergencyLoggsträng(" state=")
				MEmergencyLoggunsignedinteger32(uint32(nästathread.ThreadTillstånd))
				MEmergencyLoggsträng(" eip=")
				MEmergencyLoggunsignedinteger32(nästathread.ProcessorTillstånd.Eip)
				MEmergencyLoggsträng(" cs=")
				MEmergencyLoggunsignedinteger32(nästathread.ProcessorTillstånd.Cs)
				MEmergencyLoggsträng("\n")
			}

			if esp >= KernelheapStarta && schedata.aktuellthread != nil {
				schedata.aktuellthread.ProcessorTillstånd = (*TcpuTillstånd)(Pointer(uintptr(esp)))

				adress := uintptr(Pointer(&(schedata.aktuellthread.Fpubuffer)))
				förskjutning := (16 - (adress % 16)) & 0xF
				schedata.aktuellthread.FpuFörskjutning = förskjutning
				backupfpregs(adress + förskjutning)
				if schedulerAvlusa {
					konsol_2.MSkrivut(([]byte)("backup"))
					konsol_2.MUnsignedinteger32Skrivut(esp)
				}
			}

			adress := uintptr(Pointer(&(nästathread.Fpubuffer)))
			förskjutning := nästathread.FpuFörskjutning
			if förskjutning != 0xffffffff {
				återställfpregs(adress + förskjutning)
				if schedulerAvlusa {
					konsol_2.MSkrivut(([]byte)("restore"))
				}
			}

			schedata.aktuellthread = nästathread

			if schedata.aktuellthread.ThreadTillstånd == Startad {
				schedata.aktuellthread.ThreadTillstånd = Redo

				InitialthreadAnvändarejump(schedata.aktuellthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(nästathread.ProcessorTillstånd)))
			if nästathread.Stack != 0 {
				schedata.tss.Mängdstack(Segkerneldata, nästathread.Stack+ThreadstackStorlek)
			}

			mängdcr3(nästathread.SidaKatalogpost)
			mängdgs(nästathread.ProcessorTillstånd.Gs)

		}

	}

	return esp
}

func jumpAnvändarlägeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Avaktiveraint()

func getesp() uint32
func threadAvslutaSlinga()

func mängdthreadAvslutaSlingaTillstånd(processorTillstånd *TcpuTillstånd) {
	processorTillstånd.Eip = uint32(ValueOf(threadAvslutaSlinga).Pointer())
	processorTillstånd.Cs = Segkernelcode
	processorTillstånd.Ds = Segkerneldata
	processorTillstånd.Es = Segkerneldata
	processorTillstånd.Fs = Segkerneldata
	processorTillstånd.Gs = Segkernelgs
	processorTillstånd.Ss = Segkerneldata
	processorTillstånd.Eflags = 0x202
}

func StoppaAktuellthread(processorTillstånd *TcpuTillstånd) *TcpuTillstånd {
	if schedata.aktuellthread == nil {
		mängdthreadAvslutaSlingaTillstånd(processorTillstånd)
		return processorTillstånd
	}

	stoppadthread := schedata.aktuellthread
	for i := 0; i < lista.Storlek_2; i++ {
		thread := (*TThread)(lista.Getat(i))
		if thread != nil && thread.ProcessorTillstånd == processorTillstånd {
			stoppadthread = thread
			break
		}
	}
	stoppadthread.ProcessorTillstånd = processorTillstånd
	stoppadthread.ThreadTillstånd = Stoppad
	schedata.aktuellthread = stoppadthread

	nästathread := schedata.GetNästaRedothread()
	if nästathread == nil || nästathread == stoppadthread || nästathread.ProcessorTillstånd == nil || nästathread.ProcessorTillstånd == processorTillstånd {
		mängdthreadAvslutaSlingaTillstånd(processorTillstånd)
		return processorTillstånd
	}

	schedata.aktuellthread = nästathread
	if nästathread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Mängdstack(Segkerneldata, nästathread.Stack+ThreadstackStorlek)
	}
	mängdcr3(nästathread.SidaKatalogpost)
	mängdgs(nästathread.ProcessorTillstånd.Gs)
	return nästathread.ProcessorTillstånd
}

func InitialthreadAnvändarejump(thread *TThread) {

	Avaktiveraint()

	schedata.tss.Mängdstack(Segkerneldata, thread.Stack+ThreadstackStorlek)

	mängdcr3(thread.SidaKatalogpost)
	mängdgs(thread.ProcessorTillstånd.Gs)

	schedata.aktuellthread = thread
	schedata.Aktiverad = true

	eip := thread.ProcessorTillstånd.Eip
	användareesp := thread.Användarestack_2 + thread.AnvändarestackStorlek_2
	eflags := thread.ProcessorTillstånd.Eflags
	cs := thread.ProcessorTillstånd.Cs
	esp := schedata.tss.Getesp0()

	konsol_2.MSkrivut(([]byte)("jump["))
	konsol_2.MUnsignedinteger32Skrivut(eip)
	konsol_2.MSkrivut(([]byte)(":"))
	konsol_2.MUnsignedinteger32Skrivut(användareesp)
	konsol_2.MSkrivut(([]byte)(":"))
	konsol_2.MUnsignedinteger32Skrivut(eflags)
	konsol_2.MSkrivut(([]byte)(":"))
	konsol_2.MUnsignedinteger32Skrivut(cs)
	konsol_2.MSkrivut(([]byte)(":"))

	konsol_2.MUnsignedinteger32Skrivut(esp)
	konsol_2.MSkrivut(([]byte)("]"))

	userprocpost := thread.ProcessorTillstånd.Ecx
	globalFörskjutningTabell_2 := thread.ProcessorTillstånd.Edx
	dynamisk := thread.ProcessorTillstånd.Esi

	PortSkrivbyte(0x20, 0x20)
	jumpAnvändarlägeiret(eip, användareesp, eflags, userprocpost, globalFörskjutningTabell_2, dynamisk)
	konsol_2.MSkrivut(([]byte)("usermode end"))
}
func skrivutesp(esp uint32) {
	konsol_2.MSkrivut(([]byte)("esp["))
	konsol_2.MUnsignedinteger32Skrivut(esp)
}
