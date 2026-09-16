/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "שער"
import . "util/רשימה"

import . "פסק"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "זיכרוןmanager"

const Schedulerfrequency = 1
const Kernelheapהתחלה = 1024 * 1024
const schedulerניפויבאגים = false
const pitfrequency = 100

var רשימה Linkedרשימה

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Eמופעל	bool

	נוכחיthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.נוכחיthread = nil
	schedata.Eמופעל = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var נוכחיthreadמפתח int = 0
var הבאתהליךמזהה uint32 = 1

func Allocateמזההתהליך() uint32 {
	מזההתהליך := הבאתהליךמזהה
	הבאתהליךמזהה++
	return מזההתהליך
}

func (self *Schedulerdata) Getהבאמוכןthread() *TThread {
	if רשימה.Sגודל_2 <= 0 {
		return nil
	}

	if schedata.נוכחיthread != nil {
		נוכחיthreadמפתח = רשימה.Iמפתחמתוך(uintptr(Pointer(schedata.נוכחיthread)))
		if נוכחיthreadמפתח < 0 {
			נוכחיthreadמפתח = 0
		}
	} else {
		נוכחיthreadמפתח = -1
	}

	for checked := 0; checked < רשימה.Sגודל_2; checked++ {
		נוכחיthreadמפתח++
		if נוכחיthreadמפתח >= רשימה.Sגודל_2 {
			נוכחיthreadמפתח = 0
		}
		thread := (*TThread)(רשימה.Getat(נוכחיthreadמפתח))
		if thread != nil && thread.Threadמצב != Blocked && thread.Threadמצב != Sמופסק {
			if schedulerניפויבאגים {
				console_2.Mהדפסה("ti:")
				console_2.MUnsignedinteger32הדפסה(uint32(נוכחיthreadמפתח))
				console_2.Mהדפסה(":")
				console_2.MUnsignedinteger32הדפסה(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.נוכחיthread

}
func (self *Scheduler) Aהוספהthread(thread *TThread) {
	if thread == nil {
		return
	}
	רשימה.Append_to_list(uintptr(Pointer(thread)))
}
func Aהוספהrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	רשימה.Append_to_list(uintptr(Pointer(thread)))
}

func Cנוכחימזההתהליך() uint32 {
	if schedata.נוכחיthread == nil || schedata.נוכחיthread.Pמזההתהליך == 0 {
		return 1
	}
	return schedata.נוכחיthread.Pמזההתהליך
}

func Cנוכחיparentמזההתהליך() uint32 {
	if schedata.נוכחיthread == nil {
		return 0
	}
	return schedata.נוכחיthread.Parentמזההתהליך
}
func (self *Scheduler) Rהסרthread(thread *TThread) {
	רשימה.Rהסר(uintptr(Pointer(thread)))
}

func (self *Scheduler) Rהסרthreadat(מפתח int) {
	רשימה.Rהסרat(מפתח)
}

type Scheduler struct {
	Tפסקhandler
}

func (self *Scheduler) Init(manager *Tפסקmanager, mem *mem.Tזיכרוןmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	רשימה = Linkedרשימה{}
	רשימה.Init(mem)
	console_2.Mהדפסה("list:")
	console_2.MUnsignedinteger32הדפסה(uint32(uintptr(Pointer(&רשימה))))

	פסקhandler = ידיתפסק
	var address uintptr
	address = uintptr(Pointer(&פסקhandler))
	self.Tפסקhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Eמופעל(מופעל bool) {
	schedata.Eמופעל = מופעל
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	Pשערכתיבהbyte(0x43, 0x36)
	Pשערכתיבהbyte(0x40, uint8(divisor&0xFF))
	Pשערכתיבהbyte(0x40, uint8((divisor>>8)&0xFF))
}

func קבעds(dssegment uint32)
func קבעgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func שחזורfpregs(buffer_2 uintptr)

var jmpמשתמש uint32 = 0
var פסקhandler func(uint32) uint32

func schedulestack(fn func())
func קבעcr3(address uint32)
func getcr3() uint32

func ידיתפסק(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerניפויבאגים {
		console_2.Mהדפסהxy(([]byte)("sche1:"), 1, 17)

		console_2.Mהדפסה(":")
		console_2.MUnsignedinteger32הדפסה(esp)
		console_2.Mהדפסה(":")

		console_2.MUnsignedinteger32הדפסה(uint32(schedata.tickcount))
		console_2.Mהדפסה(":")
		console_2.MUnsignedinteger32הדפסה(Kernelheapהתחלה)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if רשימה.Sגודל_2 > 0 && schedata.Eמופעל == true {
			var הבאthread = schedata.Getהבאמוכןthread()
			if הבאthread == nil {
				return esp
			}
			if schedata.נוכחיthread == nil {
				MEmergencyיומןמחרוזת("\nSCHED first esp=")
				MEmergencyיומןunsignedinteger32(esp)
				MEmergencyיומןמחרוזת(" thread=")
				MEmergencyיומןunsignedinteger32(uint32(uintptr(Pointer(הבאthread))))
				MEmergencyיומןמחרוזת(" cpu=")
				MEmergencyיומןunsignedinteger32(uint32(uintptr(Pointer(הבאthread.Cמעבדמצב))))
				MEmergencyיומןמחרוזת(" state=")
				MEmergencyיומןunsignedinteger32(uint32(הבאthread.Threadמצב))
				MEmergencyיומןמחרוזת(" eip=")
				MEmergencyיומןunsignedinteger32(הבאthread.Cמעבדמצב.Eip)
				MEmergencyיומןמחרוזת(" cs=")
				MEmergencyיומןunsignedinteger32(הבאthread.Cמעבדמצב.Cs)
				MEmergencyיומןמחרוזת("\n")
			}

			if esp >= Kernelheapהתחלה && schedata.נוכחיthread != nil {
				schedata.נוכחיthread.Cמעבדמצב = (*Tcpuמצב)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.נוכחיthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.נוכחיthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerניפויבאגים {
					console_2.Mהדפסה(([]byte)("backup"))
					console_2.MUnsignedinteger32הדפסה(esp)
				}
			}

			address := uintptr(Pointer(&(הבאthread.Fpubuffer)))
			offset := הבאthread.Fpuoffset
			if offset != 0xffffffff {
				שחזורfpregs(address + offset)
				if schedulerניפויבאגים {
					console_2.Mהדפסה(([]byte)("restore"))
				}
			}

			schedata.נוכחיthread = הבאthread

			if schedata.נוכחיthread.Threadמצב == Sהתחיל {
				schedata.נוכחיthread.Threadמצב = Rמוכן

				Initialthreadמשתמשjump(schedata.נוכחיthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(הבאthread.Cמעבדמצב)))
			if הבאthread.Stack != 0 {
				schedata.tss.Sקבעstack(Segkerneldata, הבאthread.Stack+Threadstackגודל)
			}

			קבעcr3(הבאthread.Pעמודספרייהentry)
			קבעgs(הבאthread.Cמעבדמצב.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Dנטרלint()

func getesp() uint32
func threadיציאהloop()

func קבעthreadיציאהloopמצב(מעבדמצב *Tcpuמצב) {
	מעבדמצב.Eip = uint32(ValueOf(threadיציאהloop).Pointer())
	מעבדמצב.Cs = Segkernelcode
	מעבדמצב.Ds = Segkerneldata
	מעבדמצב.Es = Segkerneldata
	מעבדמצב.Fs = Segkerneldata
	מעבדמצב.Gs = Segkernelgs
	מעבדמצב.Ss = Segkerneldata
	מעבדמצב.Eflags = 0x202
}

func Sעצורנוכחיthread(מעבדמצב *Tcpuמצב) *Tcpuמצב {
	if schedata.נוכחיthread == nil {
		קבעthreadיציאהloopמצב(מעבדמצב)
		return מעבדמצב
	}

	מופסקthread := schedata.נוכחיthread
	for i := 0; i < רשימה.Sגודל_2; i++ {
		thread := (*TThread)(רשימה.Getat(i))
		if thread != nil && thread.Cמעבדמצב == מעבדמצב {
			מופסקthread = thread
			break
		}
	}
	מופסקthread.Cמעבדמצב = מעבדמצב
	מופסקthread.Threadמצב = Sמופסק
	schedata.נוכחיthread = מופסקthread

	הבאthread := schedata.Getהבאמוכןthread()
	if הבאthread == nil || הבאthread == מופסקthread || הבאthread.Cמעבדמצב == nil || הבאthread.Cמעבדמצב == מעבדמצב {
		קבעthreadיציאהloopמצב(מעבדמצב)
		return מעבדמצב
	}

	schedata.נוכחיthread = הבאthread
	if הבאthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Sקבעstack(Segkerneldata, הבאthread.Stack+Threadstackגודל)
	}
	קבעcr3(הבאthread.Pעמודספרייהentry)
	קבעgs(הבאthread.Cמעבדמצב.Gs)
	return הבאthread.Cמעבדמצב
}

func Initialthreadמשתמשjump(thread *TThread) {

	Dנטרלint()

	schedata.tss.Sקבעstack(Segkerneldata, thread.Stack+Threadstackגודל)

	קבעcr3(thread.Pעמודספרייהentry)
	קבעgs(thread.Cמעבדמצב.Gs)

	schedata.נוכחיthread = thread
	schedata.Eמופעל = true

	eip := thread.Cמעבדמצב.Eip
	משתמשesp := thread.Uמשתמשstack_2 + thread.Uמשתמשstackגודל_2
	eflags := thread.Cמעבדמצב.Eflags
	cs := thread.Cמעבדמצב.Cs
	esp := schedata.tss.Getesp0()

	console_2.Mהדפסה(([]byte)("jump["))
	console_2.MUnsignedinteger32הדפסה(eip)
	console_2.Mהדפסה(([]byte)(":"))
	console_2.MUnsignedinteger32הדפסה(משתמשesp)
	console_2.Mהדפסה(([]byte)(":"))
	console_2.MUnsignedinteger32הדפסה(eflags)
	console_2.Mהדפסה(([]byte)(":"))
	console_2.MUnsignedinteger32הדפסה(cs)
	console_2.Mהדפסה(([]byte)(":"))

	console_2.MUnsignedinteger32הדפסה(esp)
	console_2.Mהדפסה(([]byte)("]"))

	userprocentry := thread.Cמעבדמצב.Ecx
	גלובליoffsettable_2 := thread.Cמעבדמצב.Edx
	דינמי := thread.Cמעבדמצב.Esi

	Pשערכתיבהbyte(0x20, 0x20)
	jumpusermodeiret(eip, משתמשesp, eflags, userprocentry, גלובליoffsettable_2, דינמי)
	console_2.Mהדפסה(([]byte)("usermode end"))
}
func הדפסהesp(esp uint32) {
	console_2.Mהדפסה(([]byte)("esp["))
	console_2.MUnsignedinteger32הדפסה(esp)
}
