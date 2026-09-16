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
var навбатӣprocessid uint32 = 1

func Allocatepid() uint32 {
	pid := навбатӣprocessid
	навбатӣprocessid++
	return pid
}

func (self *Schedulerdata) GetНавбатӣreadythread() *TThread {
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
				console_2.MЧопкардан("ti:")
				console_2.MUnsignedinteger32Чопкардан(uint32(currentthreadindex))
				console_2.MЧопкардан(":")
				console_2.MUnsignedinteger32Чопкардан(uint32(uintptr(Pointer(thread))))
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
func (self *Scheduler) Нобудкарданthread(thread *TThread) {
	list.Нобудкардан(uintptr(Pointer(thread)))
}

func (self *Scheduler) Нобудкарданthreadat(index int) {
	list.Нобудкарданat(index)
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
	console_2.MЧопкардан("list:")
	console_2.MUnsignedinteger32Чопкардан(uint32(uintptr(Pointer(&list))))

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
	PortНавиштанbyte(0x43, 0x36)
	PortНавиштанbyte(0x40, uint8(divisor&0xFF))
	PortНавиштанbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restorefpregs(buffer_2 uintptr)

var jmpИстифодакунанда uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MЧопкарданxy(([]byte)("sche1:"), 1, 17)

		console_2.MЧопкардан(":")
		console_2.MUnsignedinteger32Чопкардан(esp)
		console_2.MЧопкардан(":")

		console_2.MUnsignedinteger32Чопкардан(uint32(schedata.tickcount))
		console_2.MЧопкардан(":")
		console_2.MUnsignedinteger32Чопкардан(Kernelheapstart)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if list.Size_2 > 0 && schedata.Enabled == true {
			var навбатӣthread = schedata.GetНавбатӣreadythread()
			if навбатӣthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(навбатӣthread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(навбатӣthread.Cpustate))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(навбатӣthread.Threadstate))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(навбатӣthread.Cpustate.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(навбатӣthread.Cpustate.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= Kernelheapstart && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MЧопкардан(([]byte)("backup"))
					console_2.MUnsignedinteger32Чопкардан(esp)
				}
			}

			address := uintptr(Pointer(&(навбатӣthread.Fpubuffer)))
			offset := навбатӣthread.Fpuoffset
			if offset != 0xffffffff {
				restorefpregs(address + offset)
				if schedulerdebug {
					console_2.MЧопкардан(([]byte)("restore"))
				}
			}

			schedata.currentthread = навбатӣthread

			if schedata.currentthread.Threadstate == Started {
				schedata.currentthread.Threadstate = Ready

				InitialthreadИстифодакунандаjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(навбатӣthread.Cpustate)))
			if навбатӣthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, навбатӣthread.Stack+Threadstacksize)
			}

			setcr3(навбатӣthread.PageФеҳрастentry)
			setgs(навбатӣthread.Cpustate.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadХуруҷloop()

func setthreadХуруҷloopstate(cpustate *Tcpustate) {
	cpustate.Eip = uint32(ValueOf(threadХуруҷloop).Pointer())
	cpustate.Cs = Segkernelcode
	cpustate.Ds = Segkerneldata
	cpustate.Es = Segkerneldata
	cpustate.Fs = Segkerneldata
	cpustate.Gs = Segkernelgs
	cpustate.Ss = Segkerneldata
	cpustate.Eflags = 0x202
}

func Манъcurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		setthreadХуруҷloopstate(cpustate)
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

	навбатӣthread := schedata.GetНавбатӣreadythread()
	if навбатӣthread == nil || навбатӣthread == stoppedthread || навбатӣthread.Cpustate == nil || навбатӣthread.Cpustate == cpustate {
		setthreadХуруҷloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = навбатӣthread
	if навбатӣthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, навбатӣthread.Stack+Threadstacksize)
	}
	setcr3(навбатӣthread.PageФеҳрастentry)
	setgs(навбатӣthread.Cpustate.Gs)
	return навбатӣthread.Cpustate
}

func InitialthreadИстифодакунандаjump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+Threadstacksize)

	setcr3(thread.PageФеҳрастentry)
	setgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Enabled = true

	eip := thread.Cpustate.Eip
	истифодакунандаesp := thread.Истифодакунандаstack_2 + thread.Истифодакунандаstacksize_2
	eflags_2 := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	console_2.MЧопкардан(([]byte)("jump["))
	console_2.MUnsignedinteger32Чопкардан(eip)
	console_2.MЧопкардан(([]byte)(":"))
	console_2.MUnsignedinteger32Чопкардан(истифодакунандаesp)
	console_2.MЧопкардан(([]byte)(":"))
	console_2.MUnsignedinteger32Чопкардан(eflags_2)
	console_2.MЧопкардан(([]byte)(":"))
	console_2.MUnsignedinteger32Чопкардан(cs)
	console_2.MЧопкардан(([]byte)(":"))

	console_2.MUnsignedinteger32Чопкардан(esp)
	console_2.MЧопкардан(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	умумӣoffsettable_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	PortНавиштанbyte(0x20, 0x20)
	jumpusermodeiret(eip, истифодакунандаesp, eflags_2, userprocentry, умумӣoffsettable_2, dynamic)
	console_2.MЧопкардан(([]byte)("usermode end"))
}
func чопкарданesp(esp uint32) {
	console_2.MЧопкардан(([]byte)("esp["))
	console_2.MUnsignedinteger32Чопкардан(esp)
}
