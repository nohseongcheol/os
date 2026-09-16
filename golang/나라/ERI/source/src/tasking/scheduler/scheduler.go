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
import mem "memorymanager"

const Schedulerfrequency = 1
const Kernelheapstart = 1024 * 1024
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

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Enabled = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadindex int = 0
var nextprocessid uint32 = 1

func Allocatepid() uint32 {
	pid := nextprocessid
	nextprocessid++
	return pid
}

func (self *Schedulerdata) Getnextreadythread() *TThread {
	if list.Size_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadindex = list.Indexof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadindex < 0 {
			currentthreadindex = 0
		}
	} else {
		currentthreadindex = -1
	}

	for checked := 0; checked < list.Size_2; checked++ {
		currentthreadindex++
		if currentthreadindex >= list.Size_2 {
			currentthreadindex = 0
		}
		thread := (*TThread)(list.Getat(currentthreadindex))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Stopped {
			if schedulerdebug {
				console_2.MPrint("ti:")
				console_2.MUnsignedinteger32print(uint32(currentthreadindex))
				console_2.MPrint(":")
				console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) Addthread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}
func Addrunnablethread(thread *TThread) {
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
func (self *Scheduler) Removethread(thread *TThread) {
	list.Remove(uintptr(Pointer(thread)))
}

func (self *Scheduler) Removethreadat(index int) {
	list.Removeat(index)
}

type Scheduler struct {
	TInterrupthandler
}

func (self *Scheduler) Init(manager *TInterruptmanager, mem *mem.TMemorymanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	list = Linkedlist{}
	list.Init(mem)
	console_2.MPrint("list:")
	console_2.MUnsignedinteger32print(uint32(uintptr(Pointer(&list))))

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
	Porttsahafbyte(0x43, 0x36)
	Porttsahafbyte(0x40, uint8(divisor&0xFF))
	Porttsahafbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restorefpregs(buffer_2 uintptr)

var jmpuser uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MPrintxy(([]byte)("sche1:"), 1, 17)

		console_2.MPrint(":")
		console_2.MUnsignedinteger32print(esp)
		console_2.MPrint(":")

		console_2.MUnsignedinteger32print(uint32(schedata.tickcount))
		console_2.MPrint(":")
		console_2.MUnsignedinteger32print(Kernelheapstart)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if list.Size_2 > 0 && schedata.Enabled == true {
			var nextthread = schedata.Getnextreadythread()
			if nextthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(nextthread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(nextthread.Cpustate))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(nextthread.Threadstate))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(nextthread.Cpustate.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(nextthread.Cpustate.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= Kernelheapstart && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MPrint(([]byte)("backup"))
					console_2.MUnsignedinteger32print(esp)
				}
			}

			address := uintptr(Pointer(&(nextthread.Fpubuffer)))
			offset := nextthread.Fpuoffset
			if offset != 0xffffffff {
				restorefpregs(address + offset)
				if schedulerdebug {
					console_2.MPrint(([]byte)("restore"))
				}
			}

			schedata.currentthread = nextthread

			if schedata.currentthread.Threadstate == Started {
				schedata.currentthread.Threadstate = Ready

				Initialthreaduserjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(nextthread.Cpustate)))
			if nextthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, nextthread.Stack+Threadstacksize)
			}

			setcr3(nextthread.Pagedirectoryentry)
			setgs(nextthread.Cpustate.Gs)

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

func Stopcurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		setthreadexitloopstate(cpustate)
		return cpustate
	}

	stoppedthread := schedata.currentthread
	for i := 0; i < list.Size_2; i++ {
		thread := (*TThread)(list.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			stoppedthread = thread
			break
		}
	}
	stoppedthread.Cpustate = cpustate
	stoppedthread.Threadstate = Stopped
	schedata.currentthread = stoppedthread

	nextthread := schedata.Getnextreadythread()
	if nextthread == nil || nextthread == stoppedthread || nextthread.Cpustate == nil || nextthread.Cpustate == cpustate {
		setthreadexitloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = nextthread
	if nextthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, nextthread.Stack+Threadstacksize)
	}
	setcr3(nextthread.Pagedirectoryentry)
	setgs(nextthread.Cpustate.Gs)
	return nextthread.Cpustate
}

func Initialthreaduserjump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+Threadstacksize)

	setcr3(thread.Pagedirectoryentry)
	setgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Enabled = true

	eip := thread.Cpustate.Eip
	useresp := thread.Userstack_2 + thread.Userstacksize_2
	eflags_2 := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	console_2.MPrint(([]byte)("jump["))
	console_2.MUnsignedinteger32print(eip)
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger32print(useresp)
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger32print(eflags_2)
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger32print(cs)
	console_2.MPrint(([]byte)(":"))

	console_2.MUnsignedinteger32print(esp)
	console_2.MPrint(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	globaloffsettable_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	Porttsahafbyte(0x20, 0x20)
	jumpusermodeiret(eip, useresp, eflags_2, userprocentry, globaloffsettable_2, dynamic)
	console_2.MPrint(([]byte)("usermode end"))
}
func printesp(esp uint32) {
	console_2.MPrint(([]byte)("esp["))
	console_2.MUnsignedinteger32print(esp)
}
