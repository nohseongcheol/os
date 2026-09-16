/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "qapı"
import . "util/list"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "yaddaşmanager"

const Schedulerfrequency = 1
const Kernelheapstart = 1024 * 1024
const schedulerXətaHəlli = false
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
var sonrakıprocessid uint32 = 1

func Allocatepid() uint32 {
	pid := sonrakıprocessid
	sonrakıprocessid++
	return pid
}

func (self *Schedulerdata) GetSonrakıreadythread() *TThread {
	if list.Böyüklük_2 <= 0 {
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

	for checked := 0; checked < list.Böyüklük_2; checked++ {
		currentthreadindex++
		if currentthreadindex >= list.Böyüklük_2 {
			currentthreadindex = 0
		}
		thread := (*TThread)(list.Getat(currentthreadindex))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Dayandırılıb {
			if schedulerXətaHəlli {
				console_2.MÇapEt("ti:")
				console_2.MUnsignedinteger32ÇapEt(uint32(currentthreadindex))
				console_2.MÇapEt(":")
				console_2.MUnsignedinteger32ÇapEt(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) ƏlavəEtthread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}
func ƏlavəEtrunnablethread(thread *TThread) {
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
func (self *Scheduler) Çıxartthread(thread *TThread) {
	list.Çıxart(uintptr(Pointer(thread)))
}

func (self *Scheduler) Çıxartthreadat(index int) {
	list.Çıxartat(index)
}

type Scheduler struct {
	TInterrupthandler
}

func (self *Scheduler) Init(manager *TInterruptmanager, mem *mem.TYaddaşmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	list = Linkedlist{}
	list.Init(mem)
	console_2.MÇapEt("list:")
	console_2.MUnsignedinteger32ÇapEt(uint32(uintptr(Pointer(&list))))

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
	QapıYazmabyte(0x43, 0x36)
	QapıYazmabyte(0x40, uint8(divisor&0xFF))
	QapıYazmabyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restorefpregs(buffer_2 uintptr)

var jmpİstifadəçi uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerXətaHəlli {
		console_2.MÇapEtxy(([]byte)("sche1:"), 1, 17)

		console_2.MÇapEt(":")
		console_2.MUnsignedinteger32ÇapEt(esp)
		console_2.MÇapEt(":")

		console_2.MUnsignedinteger32ÇapEt(uint32(schedata.tickcount))
		console_2.MÇapEt(":")
		console_2.MUnsignedinteger32ÇapEt(Kernelheapstart)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if list.Böyüklük_2 > 0 && schedata.Enabled == true {
			var sonrakıthread = schedata.GetSonrakıreadythread()
			if sonrakıthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(sonrakıthread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(sonrakıthread.Cpustate))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(sonrakıthread.Threadstate))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(sonrakıthread.Cpustate.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(sonrakıthread.Cpustate.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= Kernelheapstart && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerXətaHəlli {
					console_2.MÇapEt(([]byte)("backup"))
					console_2.MUnsignedinteger32ÇapEt(esp)
				}
			}

			address := uintptr(Pointer(&(sonrakıthread.Fpubuffer)))
			offset := sonrakıthread.Fpuoffset
			if offset != 0xffffffff {
				restorefpregs(address + offset)
				if schedulerXətaHəlli {
					console_2.MÇapEt(([]byte)("restore"))
				}
			}

			schedata.currentthread = sonrakıthread

			if schedata.currentthread.Threadstate == Started {
				schedata.currentthread.Threadstate = Ready

				Initialthreadİstifadəçijump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(sonrakıthread.Cpustate)))
			if sonrakıthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, sonrakıthread.Stack+ThreadstackBöyüklük)
			}

			setcr3(sonrakıthread.SəhifəCərgəentry)
			setgs(sonrakıthread.Cpustate.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadÇıxloop()

func setthreadÇıxloopstate(cpustate *Tcpustate) {
	cpustate.Eip = uint32(ValueOf(threadÇıxloop).Pointer())
	cpustate.Cs = Segkernelcode
	cpustate.Ds = Segkerneldata
	cpustate.Es = Segkerneldata
	cpustate.Fs = Segkerneldata
	cpustate.Gs = Segkernelgs
	cpustate.Ss = Segkerneldata
	cpustate.Eflags = 0x202
}

func Dayancurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		setthreadÇıxloopstate(cpustate)
		return cpustate
	}

	dayandırılıbthread := schedata.currentthread
	for i := 0; i < list.Böyüklük_2; i++ {
		thread := (*TThread)(list.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			dayandırılıbthread = thread
			break
		}
	}
	dayandırılıbthread.Cpustate = cpustate
	dayandırılıbthread.Threadstate = Dayandırılıb
	schedata.currentthread = dayandırılıbthread

	sonrakıthread := schedata.GetSonrakıreadythread()
	if sonrakıthread == nil || sonrakıthread == dayandırılıbthread || sonrakıthread.Cpustate == nil || sonrakıthread.Cpustate == cpustate {
		setthreadÇıxloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = sonrakıthread
	if sonrakıthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, sonrakıthread.Stack+ThreadstackBöyüklük)
	}
	setcr3(sonrakıthread.SəhifəCərgəentry)
	setgs(sonrakıthread.Cpustate.Gs)
	return sonrakıthread.Cpustate
}

func Initialthreadİstifadəçijump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+ThreadstackBöyüklük)

	setcr3(thread.SəhifəCərgəentry)
	setgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Enabled = true

	eip := thread.Cpustate.Eip
	istifadəçiesp := thread.İstifadəçistack_2 + thread.İstifadəçistackBöyüklük_2
	eflags := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	console_2.MÇapEt(([]byte)("jump["))
	console_2.MUnsignedinteger32ÇapEt(eip)
	console_2.MÇapEt(([]byte)(":"))
	console_2.MUnsignedinteger32ÇapEt(istifadəçiesp)
	console_2.MÇapEt(([]byte)(":"))
	console_2.MUnsignedinteger32ÇapEt(eflags)
	console_2.MÇapEt(([]byte)(":"))
	console_2.MUnsignedinteger32ÇapEt(cs)
	console_2.MÇapEt(([]byte)(":"))

	console_2.MUnsignedinteger32ÇapEt(esp)
	console_2.MÇapEt(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	globaloffsettable_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	QapıYazmabyte(0x20, 0x20)
	jumpusermodeiret(eip, istifadəçiesp, eflags, userprocentry, globaloffsettable_2, dynamic)
	console_2.MÇapEt(([]byte)("usermode end"))
}
func çapEtesp(esp uint32) {
	console_2.MÇapEt(([]byte)("esp["))
	console_2.MUnsignedinteger32ÇapEt(esp)
}
