package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "պորտ"
import . "util/ցուցակ"

import . "ընդհատել"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "հիշողությունmanager"

const Schedulerfrequency = 1
const KernelheapՍկիզբ = 1024 * 1024
const schedulerdebug = false
const pitfrequency = 100

var ցուցակ LinkedՑուցակ

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Միացված	bool

	currentthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (ինքնուրույն *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Միացված = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadԻնդեքս int = 0
var հաջորդԳործընթացid uint32 = 1

func Allocatepid() uint32 {
	pid := հաջորդԳործընթացid
	հաջորդԳործընթացid++
	return pid
}

func (ինքնուրույն *Schedulerdata) GetՀաջորդՊատրաստthread() *TThread {
	if ցուցակ.Չափս_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadԻնդեքս = ցուցակ.Ինդեքսof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadԻնդեքս < 0 {
			currentthreadԻնդեքս = 0
		}
	} else {
		currentthreadԻնդեքս = -1
	}

	for checked := 0; checked < ցուցակ.Չափս_2; checked++ {
		currentthreadԻնդեքս++
		if currentthreadԻնդեքս >= ցուցակ.Չափս_2 {
			currentthreadԻնդեքս = 0
		}
		thread := (*TThread)(ցուցակ.Getat(currentthreadԻնդեքս))
		if thread != nil && thread.ThreadՎիճակ != Blocked && thread.ThreadՎիճակ != Կանգնեցված {
			if schedulerdebug {
				console_2.MՏպել("ti:")
				console_2.MUnsignedinteger32Տպել(uint32(currentthreadԻնդեքս))
				console_2.MՏպել(":")
				console_2.MUnsignedinteger32Տպել(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (ինքնուրույն *Scheduler) Ավելացնելthread(thread *TThread) {
	if thread == nil {
		return
	}
	ցուցակ.Append_to_list(uintptr(Pointer(thread)))
}
func Ավելացնելrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	ցուցակ.Append_to_list(uintptr(Pointer(thread)))
}

func Currentpid() uint32 {
	if schedata.currentthread == nil || schedata.currentthread.Pid == 0 {
		return 1
	}
	return schedata.currentthread.Pid
}

func Currentծնողpid() uint32 {
	if schedata.currentthread == nil {
		return 0
	}
	return schedata.currentthread.Ծնողpid
}
func (ինքնուրույն *Scheduler) Հեռացնելthread(thread *TThread) {
	ցուցակ.Հեռացնել_2(uintptr(Pointer(thread)))
}

func (ինքնուրույն *Scheduler) Հեռացնելthreadat(ինդեքս int) {
	ցուցակ.Հեռացնելat(ինդեքս)
}

type Scheduler struct {
	TԸնդհատելhandler
}

func (ինքնուրույն *Scheduler) Init(manager *TԸնդհատելmanager, mem *mem.TՀիշողությունmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	ցուցակ = LinkedՑուցակ{}
	ցուցակ.Init(mem)
	console_2.MՏպել("list:")
	console_2.MUnsignedinteger32Տպել(uint32(uintptr(Pointer(&ցուցակ))))

	ընդհատելhandler = handleԸնդհատել
	var address uintptr
	address = uintptr(Pointer(&ընդհատելhandler))
	ինքնուրույն.TԸնդհատելhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (ինքնուրույն *Scheduler) Միացված(միացված bool) {
	schedata.Միացված = միացված
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	ՊորտԳրելbyte(0x43, 0x36)
	ՊորտԳրելbyte(0x40, uint8(divisor&0xFF))
	ՊորտԳրելbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func վերականգնելfpregs(buffer_2 uintptr)

var jmpՕգտագործող uint32 = 0
var ընդհատելhandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleԸնդհատել(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MՏպելxy(([]byte)("sche1:"), 1, 17)

		console_2.MՏպել(":")
		console_2.MUnsignedinteger32Տպել(esp)
		console_2.MՏպել(":")

		console_2.MUnsignedinteger32Տպել(uint32(schedata.tickcount))
		console_2.MՏպել(":")
		console_2.MUnsignedinteger32Տպել(KernelheapՍկիզբ)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if ցուցակ.Չափս_2 > 0 && schedata.Միացված == true {
			var հաջորդthread = schedata.GetՀաջորդՊատրաստthread()
			if հաջորդthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogՏՈՂ("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogՏՈՂ(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(հաջորդthread))))
				MEmergencylogՏՈՂ(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(հաջորդthread.ԿՄՀՎիճակ))))
				MEmergencylogՏՈՂ(" state=")
				MEmergencylogunsignedinteger32(uint32(հաջորդthread.ThreadՎիճակ))
				MEmergencylogՏՈՂ(" eip=")
				MEmergencylogunsignedinteger32(հաջորդthread.ԿՄՀՎիճակ.Eip)
				MEmergencylogՏՈՂ(" cs=")
				MEmergencylogunsignedinteger32(հաջորդthread.ԿՄՀՎիճակ.Cs)
				MEmergencylogՏՈՂ("\n")
			}

			if esp >= KernelheapՍկիզբ && schedata.currentthread != nil {
				schedata.currentthread.ԿՄՀՎիճակ = (*TcpuՎիճակ)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MՏպել(([]byte)("backup"))
					console_2.MUnsignedinteger32Տպել(esp)
				}
			}

			address := uintptr(Pointer(&(հաջորդthread.Fpubuffer)))
			offset := հաջորդthread.Fpuoffset
			if offset != 0xffffffff {
				վերականգնելfpregs(address + offset)
				if schedulerdebug {
					console_2.MՏպել(([]byte)("restore"))
				}
			}

			schedata.currentthread = հաջորդthread

			if schedata.currentthread.ThreadՎիճակ == Սկսված {
				schedata.currentthread.ThreadՎիճակ = Պատրաստ

				InitialthreadՕգտագործողjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(հաջորդthread.ԿՄՀՎիճակ)))
			if հաջորդthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, հաջորդthread.Stack+ThreadstackՉափս)
			}

			setcr3(հաջորդthread.Էջֆայլապանակentry)
			setgs(հաջորդthread.ԿՄՀՎիճակ.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadexitloop()

func setthreadexitloopՎիճակ(կՄՀՎիճակ *TcpuՎիճակ) {
	կՄՀՎիճակ.Eip = uint32(ValueOf(threadexitloop).Pointer())
	կՄՀՎիճակ.Cs = Segkernelcode
	կՄՀՎիճակ.Ds = Segkerneldata
	կՄՀՎիճակ.Es = Segkerneldata
	կՄՀՎիճակ.Fs = Segkerneldata
	կՄՀՎիճակ.Gs = Segkernelgs
	կՄՀՎիճակ.Ss = Segkerneldata
	կՄՀՎիճակ.Eflags = 0x202
}

func Կանգառcurrentthread(կՄՀՎիճակ *TcpuՎիճակ) *TcpuՎիճակ {
	if schedata.currentthread == nil {
		setthreadexitloopՎիճակ(կՄՀՎիճակ)
		return կՄՀՎիճակ
	}

	կանգնեցվածthread := schedata.currentthread
	for i := 0; i < ցուցակ.Չափս_2; i++ {
		thread := (*TThread)(ցուցակ.Getat(i))
		if thread != nil && thread.ԿՄՀՎիճակ == կՄՀՎիճակ {
			կանգնեցվածthread = thread
			break
		}
	}
	կանգնեցվածthread.ԿՄՀՎիճակ = կՄՀՎիճակ
	կանգնեցվածthread.ThreadՎիճակ = Կանգնեցված
	schedata.currentthread = կանգնեցվածthread

	հաջորդthread := schedata.GetՀաջորդՊատրաստthread()
	if հաջորդthread == nil || հաջորդthread == կանգնեցվածthread || հաջորդthread.ԿՄՀՎիճակ == nil || հաջորդthread.ԿՄՀՎիճակ == կՄՀՎիճակ {
		setthreadexitloopՎիճակ(կՄՀՎիճակ)
		return կՄՀՎիճակ
	}

	schedata.currentthread = հաջորդthread
	if հաջորդthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, հաջորդthread.Stack+ThreadstackՉափս)
	}
	setcr3(հաջորդthread.Էջֆայլապանակentry)
	setgs(հաջորդthread.ԿՄՀՎիճակ.Gs)
	return հաջորդthread.ԿՄՀՎիճակ
}

func InitialthreadՕգտագործողjump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+ThreadstackՉափս)

	setcr3(thread.Էջֆայլապանակentry)
	setgs(thread.ԿՄՀՎիճակ.Gs)

	schedata.currentthread = thread
	schedata.Միացված = true

	eip := thread.ԿՄՀՎիճակ.Eip
	օգտագործողesp := thread.Օգտագործողstack_2 + thread.ՕգտագործողstackՉափս_2
	eflags := thread.ԿՄՀՎիճակ.Eflags
	cs := thread.ԿՄՀՎիճակ.Cs
	esp := schedata.tss.Getesp0()

	console_2.MՏպել(([]byte)("jump["))
	console_2.MUnsignedinteger32Տպել(eip)
	console_2.MՏպել(([]byte)(":"))
	console_2.MUnsignedinteger32Տպել(օգտագործողesp)
	console_2.MՏպել(([]byte)(":"))
	console_2.MUnsignedinteger32Տպել(eflags)
	console_2.MՏպել(([]byte)(":"))
	console_2.MUnsignedinteger32Տպել(cs)
	console_2.MՏպել(([]byte)(":"))

	console_2.MUnsignedinteger32Տպել(esp)
	console_2.MՏպել(([]byte)("]"))

	userprocentry := thread.ԿՄՀՎիճակ.Ecx
	գլոբալoffsetԱղյուսակ_2 := thread.ԿՄՀՎիճակ.Edx
	dynamic := thread.ԿՄՀՎիճակ.Esi

	ՊորտԳրելbyte(0x20, 0x20)
	jumpusermodeiret(eip, օգտագործողesp, eflags, userprocentry, գլոբալoffsetԱղյուսակ_2, dynamic)
	console_2.MՏպել(([]byte)("usermode end"))
}
func տպելesp(esp uint32) {
	console_2.MՏպել(([]byte)("esp["))
	console_2.MUnsignedinteger32Տպել(esp)
}
