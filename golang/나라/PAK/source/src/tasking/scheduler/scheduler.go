/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "پورٹ"
import . "util/فہرست"

import . "مداخلت"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "یادداشتmanager"

const Schedulerفریکوینسی = 1
const Kernelheapچلائیں = 1024 * 1024
const schedulerdebug = false
const pitفریکوینسی = 100

var فہرست Linkedفہرست

type Schedulerdata struct {
	فریکوینسی	uint32
	tickcount	uint32

	switchforced	bool

	Eفعال	bool

	حالیہthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.فریکوینسی = Schedulerفریکوینسی
	schedata.حالیہthread = nil
	schedata.Eفعال = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var حالیہthreadindex int = 0
var اگلاعملکاریآئیڈی uint32 = 1

func Allocatepid() uint32 {
	pid := اگلاعملکاریآئیڈی
	اگلاعملکاریآئیڈی++
	return pid
}

func (self *Schedulerdata) Getاگلاتیارthread() *TThread {
	if فہرست.Sحجم_2 <= 0 {
		return nil
	}

	if schedata.حالیہthread != nil {
		حالیہthreadindex = فہرست.Indexبرائے(uintptr(Pointer(schedata.حالیہthread)))
		if حالیہthreadindex < 0 {
			حالیہthreadindex = 0
		}
	} else {
		حالیہthreadindex = -1
	}

	for checked := 0; checked < فہرست.Sحجم_2; checked++ {
		حالیہthreadindex++
		if حالیہthreadindex >= فہرست.Sحجم_2 {
			حالیہthreadindex = 0
		}
		thread := (*TThread)(فہرست.Getat(حالیہthreadindex))
		if thread != nil && thread.Threadحالت != Blocked && thread.Threadحالت != Sرکےہوئے {
			if schedulerdebug {
				console_2.Mچھاپیں("ti:")
				console_2.MUnsignedinteger32چھاپیں(uint32(حالیہthreadindex))
				console_2.Mچھاپیں(":")
				console_2.MUnsignedinteger32چھاپیں(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.حالیہthread

}
func (self *Scheduler) Aشاملکریںthread(thread *TThread) {
	if thread == nil {
		return
	}
	فہرست.Append_to_list(uintptr(Pointer(thread)))
}
func Aشاملکریںrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	فہرست.Append_to_list(uintptr(Pointer(thread)))
}

func Cحالیہpid() uint32 {
	if schedata.حالیہthread == nil || schedata.حالیہthread.Pid == 0 {
		return 1
	}
	return schedata.حالیہthread.Pid
}

func Cحالیہآبائیpid() uint32 {
	if schedata.حالیہthread == nil {
		return 0
	}
	return schedata.حالیہthread.Pآبائیpid
}
func (self *Scheduler) Rحذفکریںthread(thread *TThread) {
	فہرست.Rحذفکریں(uintptr(Pointer(thread)))
}

func (self *Scheduler) Rحذفکریںthreadat(index int) {
	فہرست.Rحذفکریںat(index)
}

type Scheduler struct {
	Tمداخلتhandler
}

func (self *Scheduler) Init(manager *Tمداخلتmanager, mem *mem.Tیادداشتmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitفریکوینسی)

	فہرست = Linkedفہرست{}
	فہرست.Init(mem)
	console_2.Mچھاپیں("list:")
	console_2.MUnsignedinteger32چھاپیں(uint32(uintptr(Pointer(&فہرست))))

	مداخلتhandler = handleمداخلت
	var address uintptr
	address = uintptr(Pointer(&مداخلتhandler))
	self.Tمداخلتhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Eفعال(فعال bool) {
	schedata.Eفعال = فعال
}

func initpit(فریکوینسی uint32) {
	if فریکوینسی == 0 {
		return
	}
	divisor := uint32(1193180) / فریکوینسی
	Pپورٹلکھیںbyte(0x43, 0x36)
	Pپورٹلکھیںbyte(0x40, uint8(divisor&0xFF))
	Pپورٹلکھیںbyte(0x40, uint8((divisor>>8)&0xFF))
}

func سیٹds(dssegment uint32)
func سیٹgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func ریسٹورfpregs(buffer_2 uintptr)

var jmpصارف uint32 = 0
var مداخلتhandler func(uint32) uint32

func schedulestack(fn func())
func سیٹcr3(address uint32)
func getcr3() uint32

func handleمداخلت(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.Mچھاپیںxy(([]byte)("sche1:"), 1, 17)

		console_2.Mچھاپیں(":")
		console_2.MUnsignedinteger32چھاپیں(esp)
		console_2.Mچھاپیں(":")

		console_2.MUnsignedinteger32چھاپیں(uint32(schedata.tickcount))
		console_2.Mچھاپیں(":")
		console_2.MUnsignedinteger32چھاپیں(Kernelheapچلائیں)
	}

	if schedata.tickcount == schedata.فریکوینسی {
		schedata.tickcount = 0

		if فہرست.Sحجم_2 > 0 && schedata.Eفعال == true {
			var اگلاthread = schedata.Getاگلاتیارthread()
			if اگلاthread == nil {
				return esp
			}
			if schedata.حالیہthread == nil {
				MEmergencylogڈورا("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogڈورا(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(اگلاthread))))
				MEmergencylogڈورا(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(اگلاthread.Cسیپییوحالت))))
				MEmergencylogڈورا(" state=")
				MEmergencylogunsignedinteger32(uint32(اگلاthread.Threadحالت))
				MEmergencylogڈورا(" eip=")
				MEmergencylogunsignedinteger32(اگلاthread.Cسیپییوحالت.Eip)
				MEmergencylogڈورا(" cs=")
				MEmergencylogunsignedinteger32(اگلاthread.Cسیپییوحالت.Cs)
				MEmergencylogڈورا("\n")
			}

			if esp >= Kernelheapچلائیں && schedata.حالیہthread != nil {
				schedata.حالیہthread.Cسیپییوحالت = (*Tcpuحالت)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.حالیہthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.حالیہthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.Mچھاپیں(([]byte)("backup"))
					console_2.MUnsignedinteger32چھاپیں(esp)
				}
			}

			address := uintptr(Pointer(&(اگلاthread.Fpubuffer)))
			offset := اگلاthread.Fpuoffset
			if offset != 0xffffffff {
				ریسٹورfpregs(address + offset)
				if schedulerdebug {
					console_2.Mچھاپیں(([]byte)("restore"))
				}
			}

			schedata.حالیہthread = اگلاthread

			if schedata.حالیہthread.Threadحالت == Sشروعکردہ {
				schedata.حالیہthread.Threadحالت = Rتیار

				Initialthreadصارفjump(schedata.حالیہthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(اگلاthread.Cسیپییوحالت)))
			if اگلاthread.Stack != 0 {
				schedata.tss.Sسیٹstack(Segkerneldata, اگلاthread.Stack+Threadstackحجم)
			}

			سیٹcr3(اگلاthread.Pصفحہڈائریکٹریentry)
			سیٹgs(اگلاthread.Cسیپییوحالت.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Dمعطلکریںint()

func getesp() uint32
func threadexitloop()

func سیٹthreadexitloopحالت(سیپییوحالت *Tcpuحالت) {
	سیپییوحالت.Eip = uint32(ValueOf(threadexitloop).Pointer())
	سیپییوحالت.Cs = Segkernelcode
	سیپییوحالت.Ds = Segkerneldata
	سیپییوحالت.Es = Segkerneldata
	سیپییوحالت.Fs = Segkerneldata
	سیپییوحالت.Gs = Segkernelgs
	سیپییوحالت.Ss = Segkerneldata
	سیپییوحالت.Eflags = 0x202
}

func Sروکیںحالیہthread(سیپییوحالت *Tcpuحالت) *Tcpuحالت {
	if schedata.حالیہthread == nil {
		سیٹthreadexitloopحالت(سیپییوحالت)
		return سیپییوحالت
	}

	رکےہوئےthread := schedata.حالیہthread
	for i := 0; i < فہرست.Sحجم_2; i++ {
		thread := (*TThread)(فہرست.Getat(i))
		if thread != nil && thread.Cسیپییوحالت == سیپییوحالت {
			رکےہوئےthread = thread
			break
		}
	}
	رکےہوئےthread.Cسیپییوحالت = سیپییوحالت
	رکےہوئےthread.Threadحالت = Sرکےہوئے
	schedata.حالیہthread = رکےہوئےthread

	اگلاthread := schedata.Getاگلاتیارthread()
	if اگلاthread == nil || اگلاthread == رکےہوئےthread || اگلاthread.Cسیپییوحالت == nil || اگلاthread.Cسیپییوحالت == سیپییوحالت {
		سیٹthreadexitloopحالت(سیپییوحالت)
		return سیپییوحالت
	}

	schedata.حالیہthread = اگلاthread
	if اگلاthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Sسیٹstack(Segkerneldata, اگلاthread.Stack+Threadstackحجم)
	}
	سیٹcr3(اگلاthread.Pصفحہڈائریکٹریentry)
	سیٹgs(اگلاthread.Cسیپییوحالت.Gs)
	return اگلاthread.Cسیپییوحالت
}

func Initialthreadصارفjump(thread *TThread) {

	Dمعطلکریںint()

	schedata.tss.Sسیٹstack(Segkerneldata, thread.Stack+Threadstackحجم)

	سیٹcr3(thread.Pصفحہڈائریکٹریentry)
	سیٹgs(thread.Cسیپییوحالت.Gs)

	schedata.حالیہthread = thread
	schedata.Eفعال = true

	eip := thread.Cسیپییوحالت.Eip
	صارفesp := thread.Uصارفstack_2 + thread.Uصارفstackحجم_2
	eflags := thread.Cسیپییوحالت.Eflags
	cs := thread.Cسیپییوحالت.Cs
	esp := schedata.tss.Getesp0()

	console_2.Mچھاپیں(([]byte)("jump["))
	console_2.MUnsignedinteger32چھاپیں(eip)
	console_2.Mچھاپیں(([]byte)(":"))
	console_2.MUnsignedinteger32چھاپیں(صارفesp)
	console_2.Mچھاپیں(([]byte)(":"))
	console_2.MUnsignedinteger32چھاپیں(eflags)
	console_2.Mچھاپیں(([]byte)(":"))
	console_2.MUnsignedinteger32چھاپیں(cs)
	console_2.Mچھاپیں(([]byte)(":"))

	console_2.MUnsignedinteger32چھاپیں(esp)
	console_2.Mچھاپیں(([]byte)("]"))

	userprocentry := thread.Cسیپییوحالت.Ecx
	globaloffsetجدول_2 := thread.Cسیپییوحالت.Edx
	محرک := thread.Cسیپییوحالت.Esi

	Pپورٹلکھیںbyte(0x20, 0x20)
	jumpusermodeiret(eip, صارفesp, eflags, userprocentry, globaloffsetجدول_2, محرک)
	console_2.Mچھاپیں(([]byte)("usermode end"))
}
func چھاپیںesp(esp uint32) {
	console_2.Mچھاپیں(([]byte)("esp["))
	console_2.MUnsignedinteger32چھاپیں(esp)
}
