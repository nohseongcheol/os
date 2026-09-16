/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "პორტი"
import . "util/სია"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "მეხსიერებაmanager"

const Schedulerfrequency = 1
const Kernelheapstart = 1024 * 1024
const schedulerdebug = false
const pitfrequency = 100

var სია Linkedსია

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Eჩართულია	bool

	currentthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Eჩართულია = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadინდექსი int = 0
var შემდეგიპროცესიid uint32 = 1

func Allocatepid() uint32 {
	pid := შემდეგიპროცესიid
	შემდეგიპროცესიid++
	return pid
}

func (self *Schedulerdata) Getშემდეგიreadythread() *TThread {
	if სია.Sზომა_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadინდექსი = სია.Iინდექსიof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadინდექსი < 0 {
			currentthreadინდექსი = 0
		}
	} else {
		currentthreadინდექსი = -1
	}

	for checked := 0; checked < სია.Sზომა_2; checked++ {
		currentthreadინდექსი++
		if currentthreadინდექსი >= სია.Sზომა_2 {
			currentthreadინდექსი = 0
		}
		thread := (*TThread)(სია.Getat(currentthreadინდექსი))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Sგაჩერებულია {
			if schedulerdebug {
				console_2.Mბეჭდვა("ti:")
				console_2.MUnsignedinteger32ბეჭდვა(uint32(currentthreadინდექსი))
				console_2.Mბეჭდვა(":")
				console_2.MUnsignedinteger32ბეჭდვა(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) Aდამატებაthread(thread *TThread) {
	if thread == nil {
		return
	}
	სია.Append_to_list(uintptr(Pointer(thread)))
}
func Aდამატებაrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	სია.Append_to_list(uintptr(Pointer(thread)))
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
func (self *Scheduler) Rწაშლაthread(thread *TThread) {
	სია.Rწაშლა(uintptr(Pointer(thread)))
}

func (self *Scheduler) Rწაშლაthreadat(ინდექსი int) {
	სია.Rწაშლაat(ინდექსი)
}

type Scheduler struct {
	TInterrupthandler
}

func (self *Scheduler) Init(manager *TInterruptmanager, mem *mem.Tმეხსიერებაmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	სია = Linkedსია{}
	სია.Init(mem)
	console_2.Mბეჭდვა("list:")
	console_2.MUnsignedinteger32ბეჭდვა(uint32(uintptr(Pointer(&სია))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Eჩართულია(ჩართულია bool) {
	schedata.Eჩართულია = ჩართულია
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	Pპორტიჩაწერაbyte(0x43, 0x36)
	Pპორტიჩაწერაbyte(0x40, uint8(divisor&0xFF))
	Pპორტიჩაწერაbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func აღდგენაfpregs(buffer_2 uintptr)

var jmpმომხმარებელი uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.Mბეჭდვაxy(([]byte)("sche1:"), 1, 17)

		console_2.Mბეჭდვა(":")
		console_2.MUnsignedinteger32ბეჭდვა(esp)
		console_2.Mბეჭდვა(":")

		console_2.MUnsignedinteger32ბეჭდვა(uint32(schedata.tickcount))
		console_2.Mბეჭდვა(":")
		console_2.MUnsignedinteger32ბეჭდვა(Kernelheapstart)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if სია.Sზომა_2 > 0 && schedata.Eჩართულია == true {
			var შემდეგიthread = schedata.Getშემდეგიreadythread()
			if შემდეგიthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(შემდეგიthread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(შემდეგიthread.Cpustate))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(შემდეგიthread.Threadstate))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(შემდეგიthread.Cpustate.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(შემდეგიthread.Cpustate.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= Kernelheapstart && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.Mბეჭდვა(([]byte)("backup"))
					console_2.MUnsignedinteger32ბეჭდვა(esp)
				}
			}

			address := uintptr(Pointer(&(შემდეგიthread.Fpubuffer)))
			offset := შემდეგიthread.Fpuoffset
			if offset != 0xffffffff {
				აღდგენაfpregs(address + offset)
				if schedulerdebug {
					console_2.Mბეჭდვა(([]byte)("restore"))
				}
			}

			schedata.currentthread = შემდეგიthread

			if schedata.currentthread.Threadstate == Sგაშვებული {
				schedata.currentthread.Threadstate = Ready

				Initialthreadმომხმარებელიjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(შემდეგიthread.Cpustate)))
			if შემდეგიthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, შემდეგიthread.Stack+Threadstackზომა)
			}

			setcr3(შემდეგიthread.Pგვერდიდასტაentry)
			setgs(შემდეგიthread.Cpustate.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadგასვლაloop()

func setthreadგასვლაloopstate(cpustate *Tcpustate) {
	cpustate.Eip = uint32(ValueOf(threadგასვლაloop).Pointer())
	cpustate.Cs = Segkernelcode
	cpustate.Ds = Segkerneldata
	cpustate.Es = Segkerneldata
	cpustate.Fs = Segkerneldata
	cpustate.Gs = Segkernelgs
	cpustate.Ss = Segkerneldata
	cpustate.Eflags = 0x202
}

func Sშეჩერებაcurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		setthreadგასვლაloopstate(cpustate)
		return cpustate
	}

	გაჩერებულიაthread := schedata.currentthread
	for i := 0; i < სია.Sზომა_2; i++ {
		thread := (*TThread)(სია.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			გაჩერებულიაthread = thread
			break
		}
	}
	გაჩერებულიაthread.Cpustate = cpustate
	გაჩერებულიაthread.Threadstate = Sგაჩერებულია
	schedata.currentthread = გაჩერებულიაthread

	შემდეგიthread := schedata.Getშემდეგიreadythread()
	if შემდეგიthread == nil || შემდეგიthread == გაჩერებულიაthread || შემდეგიthread.Cpustate == nil || შემდეგიthread.Cpustate == cpustate {
		setthreadგასვლაloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = შემდეგიthread
	if შემდეგიthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, შემდეგიthread.Stack+Threadstackზომა)
	}
	setcr3(შემდეგიthread.Pგვერდიდასტაentry)
	setgs(შემდეგიthread.Cpustate.Gs)
	return შემდეგიthread.Cpustate
}

func Initialthreadმომხმარებელიjump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+Threadstackზომა)

	setcr3(thread.Pგვერდიდასტაentry)
	setgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Eჩართულია = true

	eip := thread.Cpustate.Eip
	მომხმარებელიesp := thread.Uმომხმარებელიstack_2 + thread.Uმომხმარებელიstackზომა_2
	eflags := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	console_2.Mბეჭდვა(([]byte)("jump["))
	console_2.MUnsignedinteger32ბეჭდვა(eip)
	console_2.Mბეჭდვა(([]byte)(":"))
	console_2.MUnsignedinteger32ბეჭდვა(მომხმარებელიesp)
	console_2.Mბეჭდვა(([]byte)(":"))
	console_2.MUnsignedinteger32ბეჭდვა(eflags)
	console_2.Mბეჭდვა(([]byte)(":"))
	console_2.MUnsignedinteger32ბეჭდვა(cs)
	console_2.Mბეჭდვა(([]byte)(":"))

	console_2.MUnsignedinteger32ბეჭდვა(esp)
	console_2.Mბეჭდვა(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	globaloffsetცხრილი_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	Pპორტიჩაწერაbyte(0x20, 0x20)
	jumpusermodeiret(eip, მომხმარებელიesp, eflags, userprocentry, globaloffsetცხრილი_2, dynamic)
	console_2.Mბეჭდვა(([]byte)("usermode end"))
}
func ბეჭდვაesp(esp uint32) {
	console_2.Mბეჭდვა(([]byte)("esp["))
	console_2.MUnsignedinteger32ბეჭდვა(esp)
}
