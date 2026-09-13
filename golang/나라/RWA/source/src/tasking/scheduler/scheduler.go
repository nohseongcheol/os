package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "umuyoboro"
import . "util/list"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "ububikomanager"

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
var currentthreadUmubarendanga int = 0
var ikurikiraprocessid uint32 = 1

func Allocatepid() uint32 {
	pid := ikurikiraprocessid
	ikurikiraprocessid++
	return pid
}

func (self *Schedulerdata) GetIkurikirareadythread() *TThread {
	if list.Ingano_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadUmubarendanga = list.Umubarendangaof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadUmubarendanga < 0 {
			currentthreadUmubarendanga = 0
		}
	} else {
		currentthreadUmubarendanga = -1
	}

	for checked := 0; checked < list.Ingano_2; checked++ {
		currentthreadUmubarendanga++
		if currentthreadUmubarendanga >= list.Ingano_2 {
			currentthreadUmubarendanga = 0
		}
		thread := (*TThread)(list.Getat(currentthreadUmubarendanga))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Kyahagariswe {
			if schedulerdebug {
				console_2.MGucapa("ti:")
				console_2.MUnsignedinteger32Gucapa(uint32(currentthreadUmubarendanga))
				console_2.MGucapa(":")
				console_2.MUnsignedinteger32Gucapa(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) Kongerathread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}
func Kongerarunnablethread(thread *TThread) {
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
func (self *Scheduler) Gukurahothread(thread *TThread) {
	list.Gukuraho(uintptr(Pointer(thread)))
}

func (self *Scheduler) Gukurahothreadat(umubarendanga int) {
	list.Gukurahoat(umubarendanga)
}

type Scheduler struct {
	TInterrupthandler
}

func (self *Scheduler) Init(manager *TInterruptmanager, mem *mem.TUbubikomanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	list = Linkedlist{}
	list.Init(mem)
	console_2.MGucapa("list:")
	console_2.MUnsignedinteger32Gucapa(uint32(uintptr(Pointer(&list))))

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
	Umuyoborokwandikabyte(0x43, 0x36)
	Umuyoborokwandikabyte(0x40, uint8(divisor&0xFF))
	Umuyoborokwandikabyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restorefpregs(buffer_2 uintptr)

var jmpUkoresha uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MGucapaxy(([]byte)("sche1:"), 1, 17)

		console_2.MGucapa(":")
		console_2.MUnsignedinteger32Gucapa(esp)
		console_2.MGucapa(":")

		console_2.MUnsignedinteger32Gucapa(uint32(schedata.tickcount))
		console_2.MGucapa(":")
		console_2.MUnsignedinteger32Gucapa(Kernelheapstart)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if list.Ingano_2 > 0 && schedata.Enabled == true {
			var ikurikirathread = schedata.GetIkurikirareadythread()
			if ikurikirathread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(ikurikirathread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(ikurikirathread.Cpustate))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(ikurikirathread.Threadstate))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(ikurikirathread.Cpustate.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(ikurikirathread.Cpustate.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= Kernelheapstart && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MGucapa(([]byte)("backup"))
					console_2.MUnsignedinteger32Gucapa(esp)
				}
			}

			address := uintptr(Pointer(&(ikurikirathread.Fpubuffer)))
			offset := ikurikirathread.Fpuoffset
			if offset != 0xffffffff {
				restorefpregs(address + offset)
				if schedulerdebug {
					console_2.MGucapa(([]byte)("restore"))
				}
			}

			schedata.currentthread = ikurikirathread

			if schedata.currentthread.Threadstate == Started {
				schedata.currentthread.Threadstate = Ready

				InitialthreadUkoreshajump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(ikurikirathread.Cpustate)))
			if ikurikirathread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, ikurikirathread.Stack+ThreadstackIngano)
			}

			setcr3(ikurikirathread.IpajiUbubikoentry)
			setgs(ikurikirathread.Cpustate.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadGusohokaloop()

func setthreadGusohokaloopstate(cpustate *Tcpustate) {
	cpustate.Eip = uint32(ValueOf(threadGusohokaloop).Pointer())
	cpustate.Cs = Segkernelcode
	cpustate.Ds = Segkerneldata
	cpustate.Es = Segkerneldata
	cpustate.Fs = Segkerneldata
	cpustate.Gs = Segkernelgs
	cpustate.Ss = Segkerneldata
	cpustate.Eflags = 0x202
}

func Guhagararacurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		setthreadGusohokaloopstate(cpustate)
		return cpustate
	}

	kyahagariswethread := schedata.currentthread
	for i := 0; i < list.Ingano_2; i++ {
		thread := (*TThread)(list.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			kyahagariswethread = thread
			break
		}
	}
	kyahagariswethread.Cpustate = cpustate
	kyahagariswethread.Threadstate = Kyahagariswe
	schedata.currentthread = kyahagariswethread

	ikurikirathread := schedata.GetIkurikirareadythread()
	if ikurikirathread == nil || ikurikirathread == kyahagariswethread || ikurikirathread.Cpustate == nil || ikurikirathread.Cpustate == cpustate {
		setthreadGusohokaloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = ikurikirathread
	if ikurikirathread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, ikurikirathread.Stack+ThreadstackIngano)
	}
	setcr3(ikurikirathread.IpajiUbubikoentry)
	setgs(ikurikirathread.Cpustate.Gs)
	return ikurikirathread.Cpustate
}

func InitialthreadUkoreshajump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+ThreadstackIngano)

	setcr3(thread.IpajiUbubikoentry)
	setgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Enabled = true

	eip := thread.Cpustate.Eip
	ukoreshaesp := thread.Ukoreshastack_2 + thread.UkoreshastackIngano_2
	eflags := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	console_2.MGucapa(([]byte)("jump["))
	console_2.MUnsignedinteger32Gucapa(eip)
	console_2.MGucapa(([]byte)(":"))
	console_2.MUnsignedinteger32Gucapa(ukoreshaesp)
	console_2.MGucapa(([]byte)(":"))
	console_2.MUnsignedinteger32Gucapa(eflags)
	console_2.MGucapa(([]byte)(":"))
	console_2.MUnsignedinteger32Gucapa(cs)
	console_2.MGucapa(([]byte)(":"))

	console_2.MUnsignedinteger32Gucapa(esp)
	console_2.MGucapa(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	globaloffsetImbonerahamwe_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	Umuyoborokwandikabyte(0x20, 0x20)
	jumpusermodeiret(eip, ukoreshaesp, eflags, userprocentry, globaloffsetImbonerahamwe_2, dynamic)
	console_2.MGucapa(([]byte)("usermode end"))
}
func gucapaesp(esp uint32) {
	console_2.MGucapa(([]byte)("esp["))
	console_2.MUnsignedinteger32Gucapa(esp)
}
