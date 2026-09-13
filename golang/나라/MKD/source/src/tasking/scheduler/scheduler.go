package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "порта"
import . "util/листа"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "меморијаmanager"

const Schedulerfrequency = 1
const KernelheapПушти = 1024 * 1024
const schedulerdebug = false
const pitfrequency = 100

var листа LinkedЛиста

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Овозможено	bool

	currentthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (само *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Овозможено = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadИндекс int = 0
var следнаПроцесИд uint32 = 1

func Allocatepid() uint32 {
	pid := следнаПроцесИд
	следнаПроцесИд++
	return pid
}

func (само *Schedulerdata) GetСледнаПодготвеноthread() *TThread {
	if листа.Големина_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadИндекс = листа.Индексна(uintptr(Pointer(schedata.currentthread)))
		if currentthreadИндекс < 0 {
			currentthreadИндекс = 0
		}
	} else {
		currentthreadИндекс = -1
	}

	for checked := 0; checked < листа.Големина_2; checked++ {
		currentthreadИндекс++
		if currentthreadИндекс >= листа.Големина_2 {
			currentthreadИндекс = 0
		}
		thread := (*TThread)(листа.Getat(currentthreadИндекс))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Стопирано {
			if schedulerdebug {
				console_2.MПечати("ti:")
				console_2.MUnsignedinteger32Печати(uint32(currentthreadИндекс))
				console_2.MПечати(":")
				console_2.MUnsignedinteger32Печати(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (само *Scheduler) Додајthread(thread *TThread) {
	if thread == nil {
		return
	}
	листа.Append_to_list(uintptr(Pointer(thread)))
}
func Додајrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	листа.Append_to_list(uintptr(Pointer(thread)))
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
func (само *Scheduler) Отстраниthread(thread *TThread) {
	листа.Отстрани(uintptr(Pointer(thread)))
}

func (само *Scheduler) Отстраниthreadat(индекс int) {
	листа.Отстраниat(индекс)
}

type Scheduler struct {
	TInterrupthandler
}

func (само *Scheduler) Init(manager *TInterruptmanager, mem *mem.TМеморијаmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	листа = LinkedЛиста{}
	листа.Init(mem)
	console_2.MПечати("list:")
	console_2.MUnsignedinteger32Печати(uint32(uintptr(Pointer(&листа))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	само.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (само *Scheduler) Овозможено(овозможено bool) {
	schedata.Овозможено = овозможено
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	ПортаЗапишиbyte(0x43, 0x36)
	ПортаЗапишиbyte(0x40, uint8(divisor&0xFF))
	ПортаЗапишиbyte(0x40, uint8((divisor>>8)&0xFF))
}

func поставиds(dssegment uint32)
func поставиgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func вратиfpregs(buffer_2 uintptr)

var jmpКорисник uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func поставиcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MПечатиxy(([]byte)("sche1:"), 1, 17)

		console_2.MПечати(":")
		console_2.MUnsignedinteger32Печати(esp)
		console_2.MПечати(":")

		console_2.MUnsignedinteger32Печати(uint32(schedata.tickcount))
		console_2.MПечати(":")
		console_2.MUnsignedinteger32Печати(KernelheapПушти)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if листа.Големина_2 > 0 && schedata.Овозможено == true {
			var следнаthread = schedata.GetСледнаПодготвеноthread()
			if следнаthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(следнаthread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(следнаthread.Cpustate))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(следнаthread.Threadstate))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(следнаthread.Cpustate.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(следнаthread.Cpustate.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= KernelheapПушти && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MПечати(([]byte)("backup"))
					console_2.MUnsignedinteger32Печати(esp)
				}
			}

			address := uintptr(Pointer(&(следнаthread.Fpubuffer)))
			offset := следнаthread.Fpuoffset
			if offset != 0xffffffff {
				вратиfpregs(address + offset)
				if schedulerdebug {
					console_2.MПечати(([]byte)("restore"))
				}
			}

			schedata.currentthread = следнаthread

			if schedata.currentthread.Threadstate == Работи {
				schedata.currentthread.Threadstate = Подготвено

				InitialthreadКорисникjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(следнаthread.Cpustate)))
			if следнаthread.Stack != 0 {
				schedata.tss.Поставиstack(Segkerneldata, следнаthread.Stack+ThreadstackГолемина)
			}

			поставиcr3(следнаthread.СтраницаДиректориумentry)
			поставиgs(следнаthread.Cpustate.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadИзлезloop()

func поставиthreadИзлезloopstate(cpustate *Tcpustate) {
	cpustate.Eip = uint32(ValueOf(threadИзлезloop).Pointer())
	cpustate.Cs = Segkernelcode
	cpustate.Ds = Segkerneldata
	cpustate.Es = Segkerneldata
	cpustate.Fs = Segkerneldata
	cpustate.Gs = Segkernelgs
	cpustate.Ss = Segkerneldata
	cpustate.Eflags = 0x202
}

func Стопcurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		поставиthreadИзлезloopstate(cpustate)
		return cpustate
	}

	стопираноthread := schedata.currentthread
	for i := 0; i < листа.Големина_2; i++ {
		thread := (*TThread)(листа.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			стопираноthread = thread
			break
		}
	}
	стопираноthread.Cpustate = cpustate
	стопираноthread.Threadstate = Стопирано
	schedata.currentthread = стопираноthread

	следнаthread := schedata.GetСледнаПодготвеноthread()
	if следнаthread == nil || следнаthread == стопираноthread || следнаthread.Cpustate == nil || следнаthread.Cpustate == cpustate {
		поставиthreadИзлезloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = следнаthread
	if следнаthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Поставиstack(Segkerneldata, следнаthread.Stack+ThreadstackГолемина)
	}
	поставиcr3(следнаthread.СтраницаДиректориумentry)
	поставиgs(следнаthread.Cpustate.Gs)
	return следнаthread.Cpustate
}

func InitialthreadКорисникjump(thread *TThread) {

	Disableint()

	schedata.tss.Поставиstack(Segkerneldata, thread.Stack+ThreadstackГолемина)

	поставиcr3(thread.СтраницаДиректориумentry)
	поставиgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Овозможено = true

	eip := thread.Cpustate.Eip
	корисникesp := thread.Корисникstack_2 + thread.КорисникstackГолемина_2
	eflags := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	console_2.MПечати(([]byte)("jump["))
	console_2.MUnsignedinteger32Печати(eip)
	console_2.MПечати(([]byte)(":"))
	console_2.MUnsignedinteger32Печати(корисникesp)
	console_2.MПечати(([]byte)(":"))
	console_2.MUnsignedinteger32Печати(eflags)
	console_2.MПечати(([]byte)(":"))
	console_2.MUnsignedinteger32Печати(cs)
	console_2.MПечати(([]byte)(":"))

	console_2.MUnsignedinteger32Печати(esp)
	console_2.MПечати(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	глобалнаoffsetТабела_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	ПортаЗапишиbyte(0x20, 0x20)
	jumpusermodeiret(eip, корисникesp, eflags, userprocentry, глобалнаoffsetТабела_2, dynamic)
	console_2.MПечати(([]byte)("usermode end"))
}
func печатиesp(esp uint32) {
	console_2.MПечати(([]byte)("esp["))
	console_2.MUnsignedinteger32Печати(esp)
}
