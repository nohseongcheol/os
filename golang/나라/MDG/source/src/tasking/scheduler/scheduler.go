/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "konsoly"
import . "gdt"
import . "irika"
import . "util/list"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "arikaMpandrindra"

const Schedulerfrequency = 1
const KernelheapAtomboy = 1024 * 1024
const schedulerdebug = false
const pitfrequency = 100

var list Linkedlist

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Enabled	bool

	currentthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (nytena *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Enabled = false
	schedata.switchforced = false

}

var konsoly_2 = TKonsoly{}
var currentthreadFizahantakila int = 0
var manarakaprocessid uint32 = 1

func Allocatepid() uint32 {
	pid := manarakaprocessid
	manarakaprocessid++
	return pid
}

func (nytena *Schedulerdata) GetManarakaVononathread() *TThread {
	if list.Habe_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadFizahantakila = list.Fizahantakilaaminny(uintptr(Pointer(schedata.currentthread)))
		if currentthreadFizahantakila < 0 {
			currentthreadFizahantakila = 0
		}
	} else {
		currentthreadFizahantakila = -1
	}

	for checked := 0; checked < list.Habe_2; checked++ {
		currentthreadFizahantakila++
		if currentthreadFizahantakila >= list.Habe_2 {
			currentthreadFizahantakila = 0
		}
		thread := (*TThread)(list.Getat(currentthreadFizahantakila))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Najanona {
			if schedulerdebug {
				konsoly_2.MAtontay("ti:")
				konsoly_2.MUnsignedinteger32Atontay(uint32(currentthreadFizahantakila))
				konsoly_2.MAtontay(":")
				konsoly_2.MUnsignedinteger32Atontay(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (nytena *Scheduler) Ampidirothread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}
func Ampidirorunnablethread(thread *TThread) {
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

func CurrentRenypid() uint32 {
	if schedata.currentthread == nil {
		return 0
	}
	return schedata.currentthread.Renypid
}
func (nytena *Scheduler) Esorythread(thread *TThread) {
	list.Esory(uintptr(Pointer(thread)))
}

func (nytena *Scheduler) Esorythreadat(fizahantakila int) {
	list.Esoryat(fizahantakila)
}

type Scheduler struct {
	TInterrupthandler
}

func (nytena *Scheduler) Init(mpandrindra *TInterruptMpandrindra, mem *mem.TArikaMpandrindra, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	list = Linkedlist{}
	list.Init(mem)
	konsoly_2.MAtontay("list:")
	konsoly_2.MUnsignedinteger32Atontay(uint32(uintptr(Pointer(&list))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	nytena.TInterrupthandler.Init(0x20, uintptr(Pointer(mpandrindra)), address)
}

func (nytena *Scheduler) Enabled(enabled bool) {
	schedata.Enabled = enabled
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	IrikaManoratrabyte(0x43, 0x36)
	IrikaManoratrabyte(0x40, uint8(divisor&0xFF))
	IrikaManoratrabyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restorefpregs(buffer_2 uintptr)

var jmpMpampiasa uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		konsoly_2.MAtontayxy(([]byte)("sche1:"), 1, 17)

		konsoly_2.MAtontay(":")
		konsoly_2.MUnsignedinteger32Atontay(esp)
		konsoly_2.MAtontay(":")

		konsoly_2.MUnsignedinteger32Atontay(uint32(schedata.tickcount))
		konsoly_2.MAtontay(":")
		konsoly_2.MUnsignedinteger32Atontay(KernelheapAtomboy)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if list.Habe_2 > 0 && schedata.Enabled == true {
			var manarakathread = schedata.GetManarakaVononathread()
			if manarakathread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(manarakathread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(manarakathread.Cpustate))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(manarakathread.Threadstate))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(manarakathread.Cpustate.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(manarakathread.Cpustate.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= KernelheapAtomboy && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					konsoly_2.MAtontay(([]byte)("backup"))
					konsoly_2.MUnsignedinteger32Atontay(esp)
				}
			}

			address := uintptr(Pointer(&(manarakathread.Fpubuffer)))
			offset := manarakathread.Fpuoffset
			if offset != 0xffffffff {
				restorefpregs(address + offset)
				if schedulerdebug {
					konsoly_2.MAtontay(([]byte)("restore"))
				}
			}

			schedata.currentthread = manarakathread

			if schedata.currentthread.Threadstate == Natomboka {
				schedata.currentthread.Threadstate = Vonona

				InitialthreadMpampiasajump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(manarakathread.Cpustate)))
			if manarakathread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, manarakathread.Stack+ThreadstackHabe)
			}

			setcr3(manarakathread.PEJYLahatahiryentry)
			setgs(manarakathread.Cpustate.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadexitloop()

func setthreadexitloopstate(cpustate *Tcpustate) {
	cpustate.Eip = uint32(ValueOf(threadexitloop).Pointer())
	cpustate.Cs = Segkernelcode
	cpustate.Ds = Segkerneldata
	cpustate.Es = Segkerneldata
	cpustate.Fs = Segkerneldata
	cpustate.Gs = Segkernelgs
	cpustate.Ss = Segkerneldata
	cpustate.Eflags = 0x202
}

func Ajanonycurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		setthreadexitloopstate(cpustate)
		return cpustate
	}

	najanonathread := schedata.currentthread
	for i := 0; i < list.Habe_2; i++ {
		thread := (*TThread)(list.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			najanonathread = thread
			break
		}
	}
	najanonathread.Cpustate = cpustate
	najanonathread.Threadstate = Najanona
	schedata.currentthread = najanonathread

	manarakathread := schedata.GetManarakaVononathread()
	if manarakathread == nil || manarakathread == najanonathread || manarakathread.Cpustate == nil || manarakathread.Cpustate == cpustate {
		setthreadexitloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = manarakathread
	if manarakathread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, manarakathread.Stack+ThreadstackHabe)
	}
	setcr3(manarakathread.PEJYLahatahiryentry)
	setgs(manarakathread.Cpustate.Gs)
	return manarakathread.Cpustate
}

func InitialthreadMpampiasajump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+ThreadstackHabe)

	setcr3(thread.PEJYLahatahiryentry)
	setgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Enabled = true

	eip := thread.Cpustate.Eip
	mpampiasaesp := thread.Mpampiasastack_2 + thread.MpampiasastackHabe_2
	eflags := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	konsoly_2.MAtontay(([]byte)("jump["))
	konsoly_2.MUnsignedinteger32Atontay(eip)
	konsoly_2.MAtontay(([]byte)(":"))
	konsoly_2.MUnsignedinteger32Atontay(mpampiasaesp)
	konsoly_2.MAtontay(([]byte)(":"))
	konsoly_2.MUnsignedinteger32Atontay(eflags)
	konsoly_2.MAtontay(([]byte)(":"))
	konsoly_2.MUnsignedinteger32Atontay(cs)
	konsoly_2.MAtontay(([]byte)(":"))

	konsoly_2.MUnsignedinteger32Atontay(esp)
	konsoly_2.MAtontay(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	globaloffsetFafana_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	IrikaManoratrabyte(0x20, 0x20)
	jumpusermodeiret(eip, mpampiasaesp, eflags, userprocentry, globaloffsetFafana_2, dynamic)
	konsoly_2.MAtontay(([]byte)("usermode end"))
}
func atontayesp(esp uint32) {
	konsoly_2.MAtontay(([]byte)("esp["))
	konsoly_2.MUnsignedinteger32Atontay(esp)
}
