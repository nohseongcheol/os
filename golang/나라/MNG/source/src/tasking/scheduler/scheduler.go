package scheduler

import . "unsafe"
import . "reflect"

import . "консол"
import . "gdt"
import . "порт"
import . "util/list"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "санахойЗохицуулагч"

const Schedulerfrequency = 1
const KernelheapЭхлэл = 1024 * 1024
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

var консол_2 = TКонсол{}
var currentthreadҮзүүлэлт int = 0
var дараахprocessДугаар uint32 = 1

func Allocatepid() uint32 {
	pid := дараахprocessДугаар
	дараахprocessДугаар++
	return pid
}

func (self *Schedulerdata) GetДараахreadythread() *TThread {
	if list.Хэмжээ_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadҮзүүлэлт = list.Үзүүлэлтof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadҮзүүлэлт < 0 {
			currentthreadҮзүүлэлт = 0
		}
	} else {
		currentthreadҮзүүлэлт = -1
	}

	for checked := 0; checked < list.Хэмжээ_2; checked++ {
		currentthreadҮзүүлэлт++
		if currentthreadҮзүүлэлт >= list.Хэмжээ_2 {
			currentthreadҮзүүлэлт = 0
		}
		thread := (*TThread)(list.Getat(currentthreadҮзүүлэлт))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Зогсоох {
			if schedulerdebug {
				консол_2.MХэвлэх("ti:")
				консол_2.MUnsignedinteger32Хэвлэх(uint32(currentthreadҮзүүлэлт))
				консол_2.MХэвлэх(":")
				консол_2.MUnsignedinteger32Хэвлэх(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) Нэмэхthread(thread *TThread) {
	if thread == nil {
		return
	}
	list.Append_to_list(uintptr(Pointer(thread)))
}
func Нэмэхrunnablethread(thread *TThread) {
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
func (self *Scheduler) Устгахthread(thread *TThread) {
	list.Устгах_2(uintptr(Pointer(thread)))
}

func (self *Scheduler) Устгахthreadat(үзүүлэлт int) {
	list.Устгахat(үзүүлэлт)
}

type Scheduler struct {
	TInterrupthandler
}

func (self *Scheduler) Init(зохицуулагч *TInterruptЗохицуулагч, mem *mem.TСанахойЗохицуулагч, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	list = Linkedlist{}
	list.Init(mem)
	консол_2.MХэвлэх("list:")
	консол_2.MUnsignedinteger32Хэвлэх(uint32(uintptr(Pointer(&list))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0x20, uintptr(Pointer(зохицуулагч)), address)
}

func (self *Scheduler) Enabled(enabled bool) {
	schedata.Enabled = enabled
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	ПортБичихbyte(0x43, 0x36)
	ПортБичихbyte(0x40, uint8(divisor&0xFF))
	ПортБичихbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restorefpregs(buffer_2 uintptr)

var jmpХэрэглэгч uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		консол_2.MХэвлэхxy(([]byte)("sche1:"), 1, 17)

		консол_2.MХэвлэх(":")
		консол_2.MUnsignedinteger32Хэвлэх(esp)
		консол_2.MХэвлэх(":")

		консол_2.MUnsignedinteger32Хэвлэх(uint32(schedata.tickcount))
		консол_2.MХэвлэх(":")
		консол_2.MUnsignedinteger32Хэвлэх(KernelheapЭхлэл)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if list.Хэмжээ_2 > 0 && schedata.Enabled == true {
			var дараахthread = schedata.GetДараахreadythread()
			if дараахthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogБИЧВЭР("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogБИЧВЭР(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(дараахthread))))
				MEmergencylogБИЧВЭР(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(дараахthread.Cpustate))))
				MEmergencylogБИЧВЭР(" state=")
				MEmergencylogunsignedinteger32(uint32(дараахthread.Threadstate))
				MEmergencylogБИЧВЭР(" eip=")
				MEmergencylogunsignedinteger32(дараахthread.Cpustate.Eip)
				MEmergencylogБИЧВЭР(" cs=")
				MEmergencylogunsignedinteger32(дараахthread.Cpustate.Cs)
				MEmergencylogБИЧВЭР("\n")
			}

			if esp >= KernelheapЭхлэл && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					консол_2.MХэвлэх(([]byte)("backup"))
					консол_2.MUnsignedinteger32Хэвлэх(esp)
				}
			}

			address := uintptr(Pointer(&(дараахthread.Fpubuffer)))
			offset := дараахthread.Fpuoffset
			if offset != 0xffffffff {
				restorefpregs(address + offset)
				if schedulerdebug {
					консол_2.MХэвлэх(([]byte)("restore"))
				}
			}

			schedata.currentthread = дараахthread

			if schedata.currentthread.Threadstate == Started {
				schedata.currentthread.Threadstate = Ready

				InitialthreadХэрэглэгчjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(дараахthread.Cpustate)))
			if дараахthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, дараахthread.Stack+ThreadstackХэмжээ)
			}

			setcr3(дараахthread.ХУУДАСЛавлахentry)
			setgs(дараахthread.Cpustate.Gs)

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

func Зогсcurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		setthreadexitloopstate(cpustate)
		return cpustate
	}

	зогсоохthread := schedata.currentthread
	for i := 0; i < list.Хэмжээ_2; i++ {
		thread := (*TThread)(list.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			зогсоохthread = thread
			break
		}
	}
	зогсоохthread.Cpustate = cpustate
	зогсоохthread.Threadstate = Зогсоох
	schedata.currentthread = зогсоохthread

	дараахthread := schedata.GetДараахreadythread()
	if дараахthread == nil || дараахthread == зогсоохthread || дараахthread.Cpustate == nil || дараахthread.Cpustate == cpustate {
		setthreadexitloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = дараахthread
	if дараахthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, дараахthread.Stack+ThreadstackХэмжээ)
	}
	setcr3(дараахthread.ХУУДАСЛавлахentry)
	setgs(дараахthread.Cpustate.Gs)
	return дараахthread.Cpustate
}

func InitialthreadХэрэглэгчjump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+ThreadstackХэмжээ)

	setcr3(thread.ХУУДАСЛавлахentry)
	setgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Enabled = true

	eip := thread.Cpustate.Eip
	хэрэглэгчesp := thread.Хэрэглэгчstack_2 + thread.ХэрэглэгчstackХэмжээ_2
	eflags := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	консол_2.MХэвлэх(([]byte)("jump["))
	консол_2.MUnsignedinteger32Хэвлэх(eip)
	консол_2.MХэвлэх(([]byte)(":"))
	консол_2.MUnsignedinteger32Хэвлэх(хэрэглэгчesp)
	консол_2.MХэвлэх(([]byte)(":"))
	консол_2.MUnsignedinteger32Хэвлэх(eflags)
	консол_2.MХэвлэх(([]byte)(":"))
	консол_2.MUnsignedinteger32Хэвлэх(cs)
	консол_2.MХэвлэх(([]byte)(":"))

	консол_2.MUnsignedinteger32Хэвлэх(esp)
	консол_2.MХэвлэх(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	globaloffsettable_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	ПортБичихbyte(0x20, 0x20)
	jumpusermodeiret(eip, хэрэглэгчesp, eflags, userprocentry, globaloffsettable_2, dynamic)
	консол_2.MХэвлэх(([]byte)("usermode end"))
}
func хэвлэхesp(esp uint32) {
	консол_2.MХэвлэх(([]byte)("esp["))
	консол_2.MUnsignedinteger32Хэвлэх(esp)
}
