/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/listă"

import . "intrerupere"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memoriemanager"

const SchedulerFrecvență = 1
const KernelheapPornește = 1024 * 1024
const schedulerDepanează = false
const pitFrecvență = 100

var listă LinkedListă

type Schedulerdata struct {
	frecvență	uint32
	tickcount	uint32

	switchforced	bool

	Activat	bool

	curentăthread	*TThread
	tss		*Tssînregistrare
}

var schedata Schedulerdata = Schedulerdata{}

func (sine *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frecvență = SchedulerFrecvență
	schedata.curentăthread = nil
	schedata.Activat = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var curentăthreadindex int = 0
var înainteProcesid uint32 = 1

func Allocatepid() uint32 {
	pid := înainteProcesid
	înainteProcesid++
	return pid
}

func (sine *Schedulerdata) GetÎnaintePregătitthread() *TThread {
	if listă.Mărime_2 <= 0 {
		return nil
	}

	if schedata.curentăthread != nil {
		curentăthreadindex = listă.Indexdin(uintptr(Pointer(schedata.curentăthread)))
		if curentăthreadindex < 0 {
			curentăthreadindex = 0
		}
	} else {
		curentăthreadindex = -1
	}

	for checked := 0; checked < listă.Mărime_2; checked++ {
		curentăthreadindex++
		if curentăthreadindex >= listă.Mărime_2 {
			curentăthreadindex = 0
		}
		thread := (*TThread)(listă.Getat(curentăthreadindex))
		if thread != nil && thread.ThreadStare != Blocked && thread.ThreadStare != Oprit {
			if schedulerDepanează {
				console_2.MTipărește("ti:")
				console_2.MUnsignedinteger32Tipărește(uint32(curentăthreadindex))
				console_2.MTipărește(":")
				console_2.MUnsignedinteger32Tipărește(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.curentăthread

}
func (sine *Scheduler) Adaugăthread(thread *TThread) {
	if thread == nil {
		return
	}
	listă.Append_to_list(uintptr(Pointer(thread)))
}
func Adaugărunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	listă.Append_to_list(uintptr(Pointer(thread)))
}

func Curentăpid() uint32 {
	if schedata.curentăthread == nil || schedata.curentăthread.Pid == 0 {
		return 1
	}
	return schedata.curentăthread.Pid
}

func Curentăpărintepid() uint32 {
	if schedata.curentăthread == nil {
		return 0
	}
	return schedata.curentăthread.Părintepid
}
func (sine *Scheduler) Eliminăthread(thread *TThread) {
	listă.Elimină(uintptr(Pointer(thread)))
}

func (sine *Scheduler) Eliminăthreadat(index int) {
	listă.Eliminăat(index)
}

type Scheduler struct {
	TIntreruperehandler
}

func (sine *Scheduler) Init(manager *TIntreruperemanager, mem *mem.TMemoriemanager, tss *Tssînregistrare) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitFrecvență)

	listă = LinkedListă{}
	listă.Init(mem)
	console_2.MTipărește("list:")
	console_2.MUnsignedinteger32Tipărește(uint32(uintptr(Pointer(&listă))))

	intreruperehandler = mânerIntrerupere
	var address uintptr
	address = uintptr(Pointer(&intreruperehandler))
	sine.TIntreruperehandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (sine *Scheduler) Activat(activat bool) {
	schedata.Activat = activat
}

func initpit(frecvență uint32) {
	if frecvență == 0 {
		return
	}
	divisor := uint32(1193180) / frecvență
	PortScrierebyte(0x43, 0x36)
	PortScrierebyte(0x40, uint8(divisor&0xFF))
	PortScrierebyte(0x40, uint8((divisor>>8)&0xFF))
}

func definitds(dssegment uint32)
func definitgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restaureazăfpregs(buffer_2 uintptr)

var jmpUtilizator uint32 = 0
var intreruperehandler func(uint32) uint32

func schedulestack(fn func())
func definitcr3(address uint32)
func getcr3() uint32

func mânerIntrerupere(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerDepanează {
		console_2.MTipăreștexy(([]byte)("sche1:"), 1, 17)

		console_2.MTipărește(":")
		console_2.MUnsignedinteger32Tipărește(esp)
		console_2.MTipărește(":")

		console_2.MUnsignedinteger32Tipărește(uint32(schedata.tickcount))
		console_2.MTipărește(":")
		console_2.MUnsignedinteger32Tipărește(KernelheapPornește)
	}

	if schedata.tickcount == schedata.frecvență {
		schedata.tickcount = 0

		if listă.Mărime_2 > 0 && schedata.Activat == true {
			var înaintethread = schedata.GetÎnaintePregătitthread()
			if înaintethread == nil {
				return esp
			}
			if schedata.curentăthread == nil {
				MEmergencylogȘir("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogȘir(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(înaintethread))))
				MEmergencylogȘir(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(înaintethread.CpuStare))))
				MEmergencylogȘir(" state=")
				MEmergencylogunsignedinteger32(uint32(înaintethread.ThreadStare))
				MEmergencylogȘir(" eip=")
				MEmergencylogunsignedinteger32(înaintethread.CpuStare.Eip)
				MEmergencylogȘir(" cs=")
				MEmergencylogunsignedinteger32(înaintethread.CpuStare.Cs)
				MEmergencylogȘir("\n")
			}

			if esp >= KernelheapPornește && schedata.curentăthread != nil {
				schedata.curentăthread.CpuStare = (*TcpuStare)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.curentăthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.curentăthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerDepanează {
					console_2.MTipărește(([]byte)("backup"))
					console_2.MUnsignedinteger32Tipărește(esp)
				}
			}

			address := uintptr(Pointer(&(înaintethread.Fpubuffer)))
			offset := înaintethread.Fpuoffset
			if offset != 0xffffffff {
				restaureazăfpregs(address + offset)
				if schedulerDepanează {
					console_2.MTipărește(([]byte)("restore"))
				}
			}

			schedata.curentăthread = înaintethread

			if schedata.curentăthread.ThreadStare == Pornit {
				schedata.curentăthread.ThreadStare = Pregătit

				InitialthreadUtilizatorjump(schedata.curentăthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(înaintethread.CpuStare)))
			if înaintethread.Stack != 0 {
				schedata.tss.Definitstack(Segkerneldata, înaintethread.Stack+ThreadstackMărime)
			}

			definitcr3(înaintethread.PAGINĂDirectorînregistrare)
			definitgs(înaintethread.CpuStare.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Dezactiveazăint()

func getesp() uint32
func threadIeșireloop()

func definitthreadIeșireloopStare(cpuStare *TcpuStare) {
	cpuStare.Eip = uint32(ValueOf(threadIeșireloop).Pointer())
	cpuStare.Cs = Segkernelcode
	cpuStare.Ds = Segkerneldata
	cpuStare.Es = Segkerneldata
	cpuStare.Fs = Segkerneldata
	cpuStare.Gs = Segkernelgs
	cpuStare.Ss = Segkerneldata
	cpuStare.Eflags = 0x202
}

func OpreșteCurentăthread(cpuStare *TcpuStare) *TcpuStare {
	if schedata.curentăthread == nil {
		definitthreadIeșireloopStare(cpuStare)
		return cpuStare
	}

	opritthread := schedata.curentăthread
	for i := 0; i < listă.Mărime_2; i++ {
		thread := (*TThread)(listă.Getat(i))
		if thread != nil && thread.CpuStare == cpuStare {
			opritthread = thread
			break
		}
	}
	opritthread.CpuStare = cpuStare
	opritthread.ThreadStare = Oprit
	schedata.curentăthread = opritthread

	înaintethread := schedata.GetÎnaintePregătitthread()
	if înaintethread == nil || înaintethread == opritthread || înaintethread.CpuStare == nil || înaintethread.CpuStare == cpuStare {
		definitthreadIeșireloopStare(cpuStare)
		return cpuStare
	}

	schedata.curentăthread = înaintethread
	if înaintethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Definitstack(Segkerneldata, înaintethread.Stack+ThreadstackMărime)
	}
	definitcr3(înaintethread.PAGINĂDirectorînregistrare)
	definitgs(înaintethread.CpuStare.Gs)
	return înaintethread.CpuStare
}

func InitialthreadUtilizatorjump(thread *TThread) {

	Dezactiveazăint()

	schedata.tss.Definitstack(Segkerneldata, thread.Stack+ThreadstackMărime)

	definitcr3(thread.PAGINĂDirectorînregistrare)
	definitgs(thread.CpuStare.Gs)

	schedata.curentăthread = thread
	schedata.Activat = true

	eip := thread.CpuStare.Eip
	utilizatoresp := thread.Utilizatorstack_2 + thread.UtilizatorstackMărime_2
	eflags := thread.CpuStare.Eflags
	cs := thread.CpuStare.Cs
	esp := schedata.tss.Getesp0()

	console_2.MTipărește(([]byte)("jump["))
	console_2.MUnsignedinteger32Tipărește(eip)
	console_2.MTipărește(([]byte)(":"))
	console_2.MUnsignedinteger32Tipărește(utilizatoresp)
	console_2.MTipărește(([]byte)(":"))
	console_2.MUnsignedinteger32Tipărește(eflags)
	console_2.MTipărește(([]byte)(":"))
	console_2.MUnsignedinteger32Tipărește(cs)
	console_2.MTipărește(([]byte)(":"))

	console_2.MUnsignedinteger32Tipărește(esp)
	console_2.MTipărește(([]byte)("]"))

	userprocînregistrare := thread.CpuStare.Ecx
	globaloffsetTabel_2 := thread.CpuStare.Edx
	dinamică := thread.CpuStare.Esi

	PortScrierebyte(0x20, 0x20)
	jumpusermodeiret(eip, utilizatoresp, eflags, userprocînregistrare, globaloffsetTabel_2, dinamică)
	console_2.MTipărește(([]byte)("usermode end"))
}
func tipăreșteesp(esp uint32) {
	console_2.MTipărește(([]byte)("esp["))
	console_2.MUnsignedinteger32Tipărește(esp)
}
