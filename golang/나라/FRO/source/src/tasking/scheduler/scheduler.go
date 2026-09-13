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
var næstaprocessid uint32 = 1

func Allocatepid() uint32 {
	pid := næstaprocessid
	næstaprocessid++
	return pid
}

func (self *Schedulerdata) GetNæstareadythread() *TThread {
	if list.Stødd_2 <= 0 {
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

	for checked := 0; checked < list.Stødd_2; checked++ {
		currentthreadindex++
		if currentthreadindex >= list.Stødd_2 {
			currentthreadindex = 0
		}
		thread := (*TThread)(list.Getat(currentthreadindex))
		if thread != nil && thread.ThreadStøða != Blocked && thread.ThreadStøða != Stopped {
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
func (self *Scheduler) Takburturthread(thread *TThread) {
	list.Takburtur(uintptr(Pointer(thread)))
}

func (self *Scheduler) Takburturthreadat(index int) {
	list.Takburturat(index)
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
	Portskrivabyte(0x43, 0x36)
	Portskrivabyte(0x40, uint8(divisor&0xFF))
	Portskrivabyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func endurstovnafpregs(buffer_2 uintptr)

var jmpBrúkari uint32 = 0
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

		if list.Stødd_2 > 0 && schedata.Enabled == true {
			var næstathread = schedata.GetNæstareadythread()
			if næstathread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(næstathread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(næstathread.CpuStøða))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(næstathread.ThreadStøða))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(næstathread.CpuStøða.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(næstathread.CpuStøða.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= Kernelheapstart && schedata.currentthread != nil {
				schedata.currentthread.CpuStøða = (*TcpuStøða)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MPrint(([]byte)("backup"))
					console_2.MUnsignedinteger32print(esp)
				}
			}

			address := uintptr(Pointer(&(næstathread.Fpubuffer)))
			offset := næstathread.Fpuoffset
			if offset != 0xffffffff {
				endurstovnafpregs(address + offset)
				if schedulerdebug {
					console_2.MPrint(([]byte)("restore"))
				}
			}

			schedata.currentthread = næstathread

			if schedata.currentthread.ThreadStøða == Started {
				schedata.currentthread.ThreadStøða = Ready

				InitialthreadBrúkarijump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(næstathread.CpuStøða)))
			if næstathread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, næstathread.Stack+ThreadstackStødd)
			}

			setcr3(næstathread.PageFíluskráentry)
			setgs(næstathread.CpuStøða.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Óvirkjaint()

func getesp() uint32
func threadexitloop()

func setthreadexitloopStøða(cpuStøða *TcpuStøða) {
	cpuStøða.Eip = uint32(ValueOf(threadexitloop).Pointer())
	cpuStøða.Cs = Segkernelcode
	cpuStøða.Ds = Segkerneldata
	cpuStøða.Es = Segkerneldata
	cpuStøða.Fs = Segkerneldata
	cpuStøða.Gs = Segkernelgs
	cpuStøða.Ss = Segkerneldata
	cpuStøða.Eflags = 0x202
}

func Steðgacurrentthread(cpuStøða *TcpuStøða) *TcpuStøða {
	if schedata.currentthread == nil {
		setthreadexitloopStøða(cpuStøða)
		return cpuStøða
	}

	stoppedthread := schedata.currentthread
	for i := 0; i < list.Stødd_2; i++ {
		thread := (*TThread)(list.Getat(i))
		if thread != nil && thread.CpuStøða == cpuStøða {
			stoppedthread = thread
			break
		}
	}
	stoppedthread.CpuStøða = cpuStøða
	stoppedthread.ThreadStøða = Stopped
	schedata.currentthread = stoppedthread

	næstathread := schedata.GetNæstareadythread()
	if næstathread == nil || næstathread == stoppedthread || næstathread.CpuStøða == nil || næstathread.CpuStøða == cpuStøða {
		setthreadexitloopStøða(cpuStøða)
		return cpuStøða
	}

	schedata.currentthread = næstathread
	if næstathread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, næstathread.Stack+ThreadstackStødd)
	}
	setcr3(næstathread.PageFíluskráentry)
	setgs(næstathread.CpuStøða.Gs)
	return næstathread.CpuStøða
}

func InitialthreadBrúkarijump(thread *TThread) {

	Óvirkjaint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+ThreadstackStødd)

	setcr3(thread.PageFíluskráentry)
	setgs(thread.CpuStøða.Gs)

	schedata.currentthread = thread
	schedata.Enabled = true

	eip := thread.CpuStøða.Eip
	brúkariesp := thread.Brúkaristack_2 + thread.BrúkaristackStødd_2
	eflags_2 := thread.CpuStøða.Eflags
	cs := thread.CpuStøða.Cs
	esp := schedata.tss.Getesp0()

	console_2.MPrint(([]byte)("jump["))
	console_2.MUnsignedinteger32print(eip)
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger32print(brúkariesp)
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger32print(eflags_2)
	console_2.MPrint(([]byte)(":"))
	console_2.MUnsignedinteger32print(cs)
	console_2.MPrint(([]byte)(":"))

	console_2.MUnsignedinteger32print(esp)
	console_2.MPrint(([]byte)("]"))

	userprocentry := thread.CpuStøða.Ecx
	globaloffsettable_2 := thread.CpuStøða.Edx
	rakstrarmáttur := thread.CpuStøða.Esi

	Portskrivabyte(0x20, 0x20)
	jumpusermodeiret(eip, brúkariesp, eflags_2, userprocentry, globaloffsettable_2, rakstrarmáttur)
	console_2.MPrint(([]byte)("usermode end"))
}
func printesp(esp uint32) {
	console_2.MPrint(([]byte)("esp["))
	console_2.MUnsignedinteger32print(esp)
}
