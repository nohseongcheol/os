/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/list"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memorijamanager"

const Schedulerfrequency = 1
const Kernelheapstart = 1024 * 1024
const schedulerIspravljanje = false
const pitfrequency = 100

var list Linkedlist

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Enabled	bool

	currentthread	*TThread
	tss		*Tssunos
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Enabled = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadIndeks int = 0
var sljedećeprocessid uint32 = 1

func Allocatepid() uint32 {
	pid := sljedećeprocessid
	sljedećeprocessid++
	return pid
}

func (self *Schedulerdata) GetSljedećereadythread() *TThread {
	if list.Veličina_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadIndeks = list.Indeksof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadIndeks < 0 {
			currentthreadIndeks = 0
		}
	} else {
		currentthreadIndeks = -1
	}

	for checked := 0; checked < list.Veličina_2; checked++ {
		currentthreadIndeks++
		if currentthreadIndeks >= list.Veličina_2 {
			currentthreadIndeks = 0
		}
		thread := (*TThread)(list.Getat(currentthreadIndeks))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Zaustavljeno {
			if schedulerIspravljanje {
				console_2.MŠtampaj("ti:")
				console_2.MUnsignedinteger32Štampaj(uint32(currentthreadIndeks))
				console_2.MŠtampaj(":")
				console_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) Dodajthread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}
func Dodajrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}

func Currentpid() uint32 {
	if schedata.currentthread == nil || schedata.currentthread.Pid == 0 {
		return 1
	}
	return schedata.currentthread.Pid
}

func Currentparentpid() uint32 {
	if schedata.currentthread == nil {
		return 0
	}
	return schedata.currentthread.Parentpid
}
func (self *Scheduler) Uklonithread(thread *TThread) {
	list.Ukloni(uintptr(Pointer(thread)))
}

func (self *Scheduler) Uklonithreadat(indeks int) {
	list.Ukloniat(indeks)
}

type Scheduler struct {
	TInterrupthandler
}

func (self *Scheduler) Init(manager *TInterruptmanager, mem *mem.TMemorijamanager, tss *Tssunos) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	list = Linkedlist{}
	list.Init(mem)
	console_2.MŠtampaj("list:")
	console_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&list))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Enabled(enabled bool) {
	schedata.Enabled = enabled
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	PortPišibyte(0x43, 0x36)
	PortPišibyte(0x40, uint8(divisor&0xFF))
	PortPišibyte(0x40, uint8((divisor>>8)&0xFF))
}

func skupds(dssegment uint32)
func skupgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restorefpregs(buffer_2 uintptr)

var jmpKorisnik uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func skupcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerIspravljanje {
		console_2.MŠtampajxy(([]byte)("sche1:"), 1, 17)

		console_2.MŠtampaj(":")
		console_2.MUnsignedinteger32Štampaj(esp)
		console_2.MŠtampaj(":")

		console_2.MUnsignedinteger32Štampaj(uint32(schedata.tickcount))
		console_2.MŠtampaj(":")
		console_2.MUnsignedinteger32Štampaj(Kernelheapstart)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if list.Veličina_2 > 0 && schedata.Enabled == true {
			var sljedećethread = schedata.GetSljedećereadythread()
			if sljedećethread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogNIZ("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogNIZ(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(sljedećethread))))
				MEmergencylogNIZ(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(sljedećethread.Cpustate))))
				MEmergencylogNIZ(" state=")
				MEmergencylogunsignedinteger32(uint32(sljedećethread.Threadstate))
				MEmergencylogNIZ(" eip=")
				MEmergencylogunsignedinteger32(sljedećethread.Cpustate.Eip)
				MEmergencylogNIZ(" cs=")
				MEmergencylogunsignedinteger32(sljedećethread.Cpustate.Cs)
				MEmergencylogNIZ("\n")
			}

			if esp >= Kernelheapstart && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerIspravljanje {
					console_2.MŠtampaj(([]byte)("backup"))
					console_2.MUnsignedinteger32Štampaj(esp)
				}
			}

			address := uintptr(Pointer(&(sljedećethread.Fpubuffer)))
			offset := sljedećethread.Fpuoffset
			if offset != 0xffffffff {
				restorefpregs(address + offset)
				if schedulerIspravljanje {
					console_2.MŠtampaj(([]byte)("restore"))
				}
			}

			schedata.currentthread = sljedećethread

			if schedata.currentthread.Threadstate == Started {
				schedata.currentthread.Threadstate = Ready

				InitialthreadKorisnikjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(sljedećethread.Cpustate)))
			if sljedećethread.Stack != 0 {
				schedata.tss.Skupstack(Segkerneldata, sljedećethread.Stack+ThreadstackVeličina)
			}

			skupcr3(sljedećethread.StranicaDirektorijunos)
			skupgs(sljedećethread.Cpustate.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadIzlazloop()

func skupthreadIzlazloopstate(cpustate *Tcpustate) {
	cpustate.Eip = uint32(ValueOf(threadIzlazloop).Pointer())
	cpustate.Cs = Segkernelcode
	cpustate.Ds = Segkerneldata
	cpustate.Es = Segkerneldata
	cpustate.Fs = Segkerneldata
	cpustate.Gs = Segkernelgs
	cpustate.Ss = Segkerneldata
	cpustate.Eflags = 0x202
}

func Zaustavicurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		skupthreadIzlazloopstate(cpustate)
		return cpustate
	}

	zaustavljenothread := schedata.currentthread
	for i := 0; i < list.Veličina_2; i++ {
		thread := (*TThread)(list.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			zaustavljenothread = thread
			break
		}
	}
	zaustavljenothread.Cpustate = cpustate
	zaustavljenothread.Threadstate = Zaustavljeno
	schedata.currentthread = zaustavljenothread

	sljedećethread := schedata.GetSljedećereadythread()
	if sljedećethread == nil || sljedećethread == zaustavljenothread || sljedećethread.Cpustate == nil || sljedećethread.Cpustate == cpustate {
		skupthreadIzlazloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = sljedećethread
	if sljedećethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Skupstack(Segkerneldata, sljedećethread.Stack+ThreadstackVeličina)
	}
	skupcr3(sljedećethread.StranicaDirektorijunos)
	skupgs(sljedećethread.Cpustate.Gs)
	return sljedećethread.Cpustate
}

func InitialthreadKorisnikjump(thread *TThread) {

	Disableint()

	schedata.tss.Skupstack(Segkerneldata, thread.Stack+ThreadstackVeličina)

	skupcr3(thread.StranicaDirektorijunos)
	skupgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Enabled = true

	eip := thread.Cpustate.Eip
	korisnikesp := thread.Korisnikstack_2 + thread.KorisnikstackVeličina_2
	eflags := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	console_2.MŠtampaj(([]byte)("jump["))
	console_2.MUnsignedinteger32Štampaj(eip)
	console_2.MŠtampaj(([]byte)(":"))
	console_2.MUnsignedinteger32Štampaj(korisnikesp)
	console_2.MŠtampaj(([]byte)(":"))
	console_2.MUnsignedinteger32Štampaj(eflags)
	console_2.MŠtampaj(([]byte)(":"))
	console_2.MUnsignedinteger32Štampaj(cs)
	console_2.MŠtampaj(([]byte)(":"))

	console_2.MUnsignedinteger32Štampaj(esp)
	console_2.MŠtampaj(([]byte)("]"))

	userprocunos := thread.Cpustate.Ecx
	globalnaoffsettable_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	PortPišibyte(0x20, 0x20)
	jumpusermodeiret(eip, korisnikesp, eflags, userprocunos, globalnaoffsettable_2, dynamic)
	console_2.MŠtampaj(([]byte)("usermode end"))
}
func štampajesp(esp uint32) {
	console_2.MŠtampaj(([]byte)("esp["))
	console_2.MUnsignedinteger32Štampaj(esp)
}
