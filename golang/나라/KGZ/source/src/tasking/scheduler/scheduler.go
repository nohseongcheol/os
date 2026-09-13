package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "порт"
import . "util/тизме"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "эсиmanager"

const Schedulerfrequency = 1
const KernelheapЖүргүзүү = 1024 * 1024
const schedulerdebug = false
const pitfrequency = 100

var тизме LinkedТизме

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Күйүк	bool

	currentthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Күйүк = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadМазмун int = 0
var кийинкиПроцессиИДЕНТИФИКАТОР uint32 = 1

func Allocatepid() uint32 {
	pid := кийинкиПроцессиИДЕНТИФИКАТОР
	кийинкиПроцессиИДЕНТИФИКАТОР++
	return pid
}

func (self *Schedulerdata) GetКийинкиДаярthread() *TThread {
	if тизме.Өлчөм_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadМазмун = тизме.Мазмунof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadМазмун < 0 {
			currentthreadМазмун = 0
		}
	} else {
		currentthreadМазмун = -1
	}

	for checked := 0; checked < тизме.Өлчөм_2; checked++ {
		currentthreadМазмун++
		if currentthreadМазмун >= тизме.Өлчөм_2 {
			currentthreadМазмун = 0
		}
		thread := (*TThread)(тизме.Getat(currentthreadМазмун))
		if thread != nil && thread.ThreadАбал != Blocked && thread.ThreadАбал != Токтотулган {
			if schedulerdebug {
				console_2.MБасма("ti:")
				console_2.MUnsignedinteger32Басма(uint32(currentthreadМазмун))
				console_2.MБасма(":")
				console_2.MUnsignedinteger32Басма(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) Кошууthread(thread *TThread) {
	if thread == nil {
		return
	}
	тизме.Append_to_list(uintptr(Pointer(thread)))
}
func Кошууrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	тизме.Append_to_list(uintptr(Pointer(thread)))
}

func Currentpid() uint32 {
	if schedata.currentthread == nil || schedata.currentthread.Pid == 0 {
		return 1
	}
	return schedata.currentthread.Pid
}

func Currentатаэнеpid() uint32 {
	if schedata.currentthread == nil {
		return 0
	}
	return schedata.currentthread.Атаэнеpid
}
func (self *Scheduler) Өчүрүүthread(thread *TThread) {
	тизме.Өчүрүү_2(uintptr(Pointer(thread)))
}

func (self *Scheduler) Өчүрүүthreadat(мазмун int) {
	тизме.Өчүрүүat(мазмун)
}

type Scheduler struct {
	TInterrupthandler
}

func (self *Scheduler) Init(manager *TInterruptmanager, mem *mem.TЭсиmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	тизме = LinkedТизме{}
	тизме.Init(mem)
	console_2.MБасма("list:")
	console_2.MUnsignedinteger32Басма(uint32(uintptr(Pointer(&тизме))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Күйүк(күйүк bool) {
	schedata.Күйүк = күйүк
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	ПортЖазууbyte(0x43, 0x36)
	ПортЖазууbyte(0x40, uint8(divisor&0xFF))
	ПортЖазууbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func калыбынакелтирүүfpregs(buffer_2 uintptr)

var jmpКолдонуучу uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MБасмаxy(([]byte)("sche1:"), 1, 17)

		console_2.MБасма(":")
		console_2.MUnsignedinteger32Басма(esp)
		console_2.MБасма(":")

		console_2.MUnsignedinteger32Басма(uint32(schedata.tickcount))
		console_2.MБасма(":")
		console_2.MUnsignedinteger32Басма(KernelheapЖүргүзүү)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if тизме.Өлчөм_2 > 0 && schedata.Күйүк == true {
			var кийинкиthread = schedata.GetКийинкиДаярthread()
			if кийинкиthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogСАП("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogСАП(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(кийинкиthread))))
				MEmergencylogСАП(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(кийинкиthread.БПАбал))))
				MEmergencylogСАП(" state=")
				MEmergencylogunsignedinteger32(uint32(кийинкиthread.ThreadАбал))
				MEmergencylogСАП(" eip=")
				MEmergencylogunsignedinteger32(кийинкиthread.БПАбал.Eip)
				MEmergencylogСАП(" cs=")
				MEmergencylogunsignedinteger32(кийинкиthread.БПАбал.Cs)
				MEmergencylogСАП("\n")
			}

			if esp >= KernelheapЖүргүзүү && schedata.currentthread != nil {
				schedata.currentthread.БПАбал = (*TcpuАбал)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MБасма(([]byte)("backup"))
					console_2.MUnsignedinteger32Басма(esp)
				}
			}

			address := uintptr(Pointer(&(кийинкиthread.Fpubuffer)))
			offset := кийинкиthread.Fpuoffset
			if offset != 0xffffffff {
				калыбынакелтирүүfpregs(address + offset)
				if schedulerdebug {
					console_2.MБасма(([]byte)("restore"))
				}
			}

			schedata.currentthread = кийинкиthread

			if schedata.currentthread.ThreadАбал == Жүргүзүлгөнкүнү {
				schedata.currentthread.ThreadАбал = Даяр

				InitialthreadКолдонуучуjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(кийинкиthread.БПАбал)))
			if кийинкиthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, кийинкиthread.Stack+ThreadstackӨлчөм)
			}

			setcr3(кийинкиthread.БАРАКкаталогentry)
			setgs(кийинкиthread.БПАбал.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadexitloop()

func setthreadexitloopАбал(бПАбал *TcpuАбал) {
	бПАбал.Eip = uint32(ValueOf(threadexitloop).Pointer())
	бПАбал.Cs = Segkernelcode
	бПАбал.Ds = Segkerneldata
	бПАбал.Es = Segkerneldata
	бПАбал.Fs = Segkerneldata
	бПАбал.Gs = Segkernelgs
	бПАбал.Ss = Segkerneldata
	бПАбал.Eflags = 0x202
}

func Токтотууcurrentthread(бПАбал *TcpuАбал) *TcpuАбал {
	if schedata.currentthread == nil {
		setthreadexitloopАбал(бПАбал)
		return бПАбал
	}

	токтотулганthread := schedata.currentthread
	for i := 0; i < тизме.Өлчөм_2; i++ {
		thread := (*TThread)(тизме.Getat(i))
		if thread != nil && thread.БПАбал == бПАбал {
			токтотулганthread = thread
			break
		}
	}
	токтотулганthread.БПАбал = бПАбал
	токтотулганthread.ThreadАбал = Токтотулган
	schedata.currentthread = токтотулганthread

	кийинкиthread := schedata.GetКийинкиДаярthread()
	if кийинкиthread == nil || кийинкиthread == токтотулганthread || кийинкиthread.БПАбал == nil || кийинкиthread.БПАбал == бПАбал {
		setthreadexitloopАбал(бПАбал)
		return бПАбал
	}

	schedata.currentthread = кийинкиthread
	if кийинкиthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, кийинкиthread.Stack+ThreadstackӨлчөм)
	}
	setcr3(кийинкиthread.БАРАКкаталогentry)
	setgs(кийинкиthread.БПАбал.Gs)
	return кийинкиthread.БПАбал
}

func InitialthreadКолдонуучуjump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+ThreadstackӨлчөм)

	setcr3(thread.БАРАКкаталогentry)
	setgs(thread.БПАбал.Gs)

	schedata.currentthread = thread
	schedata.Күйүк = true

	eip := thread.БПАбал.Eip
	колдонуучуesp := thread.Колдонуучуstack_2 + thread.КолдонуучуstackӨлчөм_2
	eflags := thread.БПАбал.Eflags
	cs := thread.БПАбал.Cs
	esp := schedata.tss.Getesp0()

	console_2.MБасма(([]byte)("jump["))
	console_2.MUnsignedinteger32Басма(eip)
	console_2.MБасма(([]byte)(":"))
	console_2.MUnsignedinteger32Басма(колдонуучуesp)
	console_2.MБасма(([]byte)(":"))
	console_2.MUnsignedinteger32Басма(eflags)
	console_2.MБасма(([]byte)(":"))
	console_2.MUnsignedinteger32Басма(cs)
	console_2.MБасма(([]byte)(":"))

	console_2.MUnsignedinteger32Басма(esp)
	console_2.MБасма(([]byte)("]"))

	userprocentry := thread.БПАбал.Ecx
	globaloffsetЖадыбал_2 := thread.БПАбал.Edx
	dynamic := thread.БПАбал.Esi

	ПортЖазууbyte(0x20, 0x20)
	jumpusermodeiret(eip, колдонуучуesp, eflags, userprocentry, globaloffsetЖадыбал_2, dynamic)
	console_2.MБасма(([]byte)("usermode end"))
}
func басмаesp(esp uint32) {
	console_2.MБасма(([]byte)("esp["))
	console_2.MUnsignedinteger32Басма(esp)
}
