/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "درگاه"
import . "util/list"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "حافظهmanager"

const Schedulerfrequency = 1
const Kernelheapstart = 1024 * 1024
const schedulerdebug = false
const pitfrequency = 100

var list Linkedlist

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Eفعالشده	bool

	currentthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (خود *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Eفعالشده = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadنمایه int = 0
var بعدیprocessشناسه uint32 = 1

func Allocateمشخصهبرنامه() uint32 {
	مشخصهبرنامه := بعدیprocessشناسه
	بعدیprocessشناسه++
	return مشخصهبرنامه
}

func (خود *Schedulerdata) Getبعدیآمادهthread() *TThread {
	if list.Sاندازه_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadنمایه = list.Iنمایهof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadنمایه < 0 {
			currentthreadنمایه = 0
		}
	} else {
		currentthreadنمایه = -1
	}

	for checked := 0; checked < list.Sاندازه_2; checked++ {
		currentthreadنمایه++
		if currentthreadنمایه >= list.Sاندازه_2 {
			currentthreadنمایه = 0
		}
		thread := (*TThread)(list.Getat(currentthreadنمایه))
		if thread != nil && thread.Threadحالت != Blocked && thread.Threadحالت != Stopped {
			if schedulerdebug {
				console_2.Mچاپ("ti:")
				console_2.MUnsignedinteger32چاپ(uint32(currentthreadنمایه))
				console_2.Mچاپ(":")
				console_2.MUnsignedinteger32چاپ(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (خود *Scheduler) Aاضافهکردنthread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}
func Aاضافهکردنrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}

func Currentمشخصهبرنامه() uint32 {
	if schedata.currentthread == nil || schedata.currentthread.Pمشخصهبرنامه == 0 {
		return 1
	}
	return schedata.currentthread.Pمشخصهبرنامه
}

func Currentوالدمشخصهبرنامه() uint32 {
	if schedata.currentthread == nil {
		return 0
	}
	return schedata.currentthread.Pوالدمشخصهبرنامه
}
func (خود *Scheduler) Rحذفthread(thread *TThread) {
	list.Rحذف(uintptr(Pointer(thread)))
}

func (خود *Scheduler) Rحذفthreadat(نمایه int) {
	list.Rحذفat(نمایه)
}

type Scheduler struct {
	TInterrupthandler
}

func (خود *Scheduler) Init(manager *TInterruptmanager, mem *mem.Tحافظهmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	list = Linkedlist{}
	list.Init(mem)
	console_2.Mچاپ("list:")
	console_2.MUnsignedinteger32چاپ(uint32(uintptr(Pointer(&list))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	خود.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (خود *Scheduler) Eفعالشده(فعالشده bool) {
	schedata.Eفعالشده = فعالشده
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	Pدرگاهنوشتنbyte(0x43, 0x36)
	Pدرگاهنوشتنbyte(0x40, uint8(divisor&0xFF))
	Pدرگاهنوشتنbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func بازیابیfpregs(buffer_2 uintptr)

var jmpکاربر uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.Mچاپxy(([]byte)("sche1:"), 1, 17)

		console_2.Mچاپ(":")
		console_2.MUnsignedinteger32چاپ(esp)
		console_2.Mچاپ(":")

		console_2.MUnsignedinteger32چاپ(uint32(schedata.tickcount))
		console_2.Mچاپ(":")
		console_2.MUnsignedinteger32چاپ(Kernelheapstart)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if list.Sاندازه_2 > 0 && schedata.Eفعالشده == true {
			var بعدیthread = schedata.Getبعدیآمادهthread()
			if بعدیthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogرشته("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogرشته(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(بعدیthread))))
				MEmergencylogرشته(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(بعدیthread.Cpuحالت))))
				MEmergencylogرشته(" state=")
				MEmergencylogunsignedinteger32(uint32(بعدیthread.Threadحالت))
				MEmergencylogرشته(" eip=")
				MEmergencylogunsignedinteger32(بعدیthread.Cpuحالت.Eip)
				MEmergencylogرشته(" cs=")
				MEmergencylogunsignedinteger32(بعدیthread.Cpuحالت.Cs)
				MEmergencylogرشته("\n")
			}

			if esp >= Kernelheapstart && schedata.currentthread != nil {
				schedata.currentthread.Cpuحالت = (*Tcpuحالت)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.Mچاپ(([]byte)("backup"))
					console_2.MUnsignedinteger32چاپ(esp)
				}
			}

			address := uintptr(Pointer(&(بعدیthread.Fpubuffer)))
			offset := بعدیthread.Fpuoffset
			if offset != 0xffffffff {
				بازیابیfpregs(address + offset)
				if schedulerdebug {
					console_2.Mچاپ(([]byte)("restore"))
				}
			}

			schedata.currentthread = بعدیthread

			if schedata.currentthread.Threadحالت == Started {
				schedata.currentthread.Threadحالت = Rآماده

				Initialthreadکاربرjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(بعدیthread.Cpuحالت)))
			if بعدیthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, بعدیthread.Stack+Threadstackاندازه)
			}

			setcr3(بعدیthread.Pصفحهشاخهentry)
			setgs(بعدیthread.Cpuحالت.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Dغیرفعالکردنint()

func getesp() uint32
func threadخروجloop()

func setthreadخروجloopحالت(cpuحالت *Tcpuحالت) {
	cpuحالت.Eip = uint32(ValueOf(threadخروجloop).Pointer())
	cpuحالت.Cs = Segkernelcode
	cpuحالت.Ds = Segkerneldata
	cpuحالت.Es = Segkerneldata
	cpuحالت.Fs = Segkerneldata
	cpuحالت.Gs = Segkernelgs
	cpuحالت.Ss = Segkerneldata
	cpuحالت.Eflags = 0x202
}

func Sایستcurrentthread(cpuحالت *Tcpuحالت) *Tcpuحالت {
	if schedata.currentthread == nil {
		setthreadخروجloopحالت(cpuحالت)
		return cpuحالت
	}

	stoppedthread := schedata.currentthread
	for i := 0; i < list.Sاندازه_2; i++ {
		thread := (*TThread)(list.Getat(i))
		if thread != nil && thread.Cpuحالت == cpuحالت {
			stoppedthread = thread
			break
		}
	}
	stoppedthread.Cpuحالت = cpuحالت
	stoppedthread.Threadحالت = Stopped
	schedata.currentthread = stoppedthread

	بعدیthread := schedata.Getبعدیآمادهthread()
	if بعدیthread == nil || بعدیthread == stoppedthread || بعدیthread.Cpuحالت == nil || بعدیthread.Cpuحالت == cpuحالت {
		setthreadخروجloopحالت(cpuحالت)
		return cpuحالت
	}

	schedata.currentthread = بعدیthread
	if بعدیthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, بعدیthread.Stack+Threadstackاندازه)
	}
	setcr3(بعدیthread.Pصفحهشاخهentry)
	setgs(بعدیthread.Cpuحالت.Gs)
	return بعدیthread.Cpuحالت
}

func Initialthreadکاربرjump(thread *TThread) {

	Dغیرفعالکردنint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+Threadstackاندازه)

	setcr3(thread.Pصفحهشاخهentry)
	setgs(thread.Cpuحالت.Gs)

	schedata.currentthread = thread
	schedata.Eفعالشده = true

	eip := thread.Cpuحالت.Eip
	کاربرesp := thread.Uکاربرstack_2 + thread.Uکاربرstackاندازه_2
	eflags_2 := thread.Cpuحالت.Eflags
	cs := thread.Cpuحالت.Cs
	esp := schedata.tss.Getesp0()

	console_2.Mچاپ(([]byte)("jump["))
	console_2.MUnsignedinteger32چاپ(eip)
	console_2.Mچاپ(([]byte)(":"))
	console_2.MUnsignedinteger32چاپ(کاربرesp)
	console_2.Mچاپ(([]byte)(":"))
	console_2.MUnsignedinteger32چاپ(eflags_2)
	console_2.Mچاپ(([]byte)(":"))
	console_2.MUnsignedinteger32چاپ(cs)
	console_2.Mچاپ(([]byte)(":"))

	console_2.MUnsignedinteger32چاپ(esp)
	console_2.Mچاپ(([]byte)("]"))

	userprocentry := thread.Cpuحالت.Ecx
	سراسریoffsetجدول_2 := thread.Cpuحالت.Edx
	پویا := thread.Cpuحالت.Esi

	Pدرگاهنوشتنbyte(0x20, 0x20)
	jumpusermodeiret(eip, کاربرesp, eflags_2, userprocentry, سراسریoffsetجدول_2, پویا)
	console_2.Mچاپ(([]byte)("usermode end"))
}
func چاپesp(esp uint32) {
	console_2.Mچاپ(([]byte)("esp["))
	console_2.MUnsignedinteger32چاپ(esp)
}
