package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/royxat"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "xotiramanager"

const Schedulerfrequency = 1
const KernelheapBoshlash = 1024 * 1024
const schedulerdebug = false
const pitfrequency = 100

var royxat Linkedroyxat

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Yoqilgan	bool

	currentthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Yoqilgan = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadindex int = 0
var keyingiJarayonid uint32 = 1

func Allocatepid() uint32 {
	pid := keyingiJarayonid
	keyingiJarayonid++
	return pid
}

func (self *Schedulerdata) GetKeyingiTayyorthread() *TThread {
	if royxat.Hajmi_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadindex = royxat.Indexof(uintptr(Pointer(schedata.currentthread)))
		if currentthreadindex < 0 {
			currentthreadindex = 0
		}
	} else {
		currentthreadindex = -1
	}

	for checked := 0; checked < royxat.Hajmi_2; checked++ {
		currentthreadindex++
		if currentthreadindex >= royxat.Hajmi_2 {
			currentthreadindex = 0
		}
		thread := (*TThread)(royxat.Getat(currentthreadindex))
		if thread != nil && thread.Threadstate != Blocked && thread.Threadstate != Stopped {
			if schedulerdebug {
				console_2.MChopetish("ti:")
				console_2.MUnsignedinteger32Chopetish(uint32(currentthreadindex))
				console_2.MChopetish(":")
				console_2.MUnsignedinteger32Chopetish(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) Qoʻshishthread(thread *TThread) {
	if thread == nil {
		return
	}
	royxat.Append_to_list(uintptr(Pointer(thread)))
}
func Qoʻshishrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	royxat.Append_to_list(uintptr(Pointer(thread)))
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
func (self *Scheduler) Olibtashlashthread(thread *TThread) {
	royxat.Olibtashlash_2(uintptr(Pointer(thread)))
}

func (self *Scheduler) Olibtashlashthreadat(index int) {
	royxat.Olibtashlashat(index)
}

type Scheduler struct {
	TInterrupthandler
}

func (self *Scheduler) Init(manager *TInterruptmanager, mem *mem.TXotiramanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	royxat = Linkedroyxat{}
	royxat.Init(mem)
	console_2.MChopetish("list:")
	console_2.MUnsignedinteger32Chopetish(uint32(uintptr(Pointer(&royxat))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	self.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Yoqilgan(yoqilgan bool) {
	schedata.Yoqilgan = yoqilgan
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	PortYozishbyte(0x43, 0x36)
	PortYozishbyte(0x40, uint8(divisor&0xFF))
	PortYozishbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func tiklashfpregs(buffer_2 uintptr)

var jmpFoydalanuvchi uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MChopetishxy(([]byte)("sche1:"), 1, 17)

		console_2.MChopetish(":")
		console_2.MUnsignedinteger32Chopetish(esp)
		console_2.MChopetish(":")

		console_2.MUnsignedinteger32Chopetish(uint32(schedata.tickcount))
		console_2.MChopetish(":")
		console_2.MUnsignedinteger32Chopetish(KernelheapBoshlash)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if royxat.Hajmi_2 > 0 && schedata.Yoqilgan == true {
			var keyingithread = schedata.GetKeyingiTayyorthread()
			if keyingithread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(keyingithread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(keyingithread.Cpustate))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(keyingithread.Threadstate))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(keyingithread.Cpustate.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(keyingithread.Cpustate.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= KernelheapBoshlash && schedata.currentthread != nil {
				schedata.currentthread.Cpustate = (*Tcpustate)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MChopetish(([]byte)("backup"))
					console_2.MUnsignedinteger32Chopetish(esp)
				}
			}

			address := uintptr(Pointer(&(keyingithread.Fpubuffer)))
			offset := keyingithread.Fpuoffset
			if offset != 0xffffffff {
				tiklashfpregs(address + offset)
				if schedulerdebug {
					console_2.MChopetish(([]byte)("restore"))
				}
			}

			schedata.currentthread = keyingithread

			if schedata.currentthread.Threadstate == Started {
				schedata.currentthread.Threadstate = Tayyor

				InitialthreadFoydalanuvchijump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(keyingithread.Cpustate)))
			if keyingithread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, keyingithread.Stack+ThreadstackHajmi)
			}

			setcr3(keyingithread.SAHIFAJildentry)
			setgs(keyingithread.Cpustate.Gs)

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

func Toʻxtatishcurrentthread(cpustate *Tcpustate) *Tcpustate {
	if schedata.currentthread == nil {
		setthreadexitloopstate(cpustate)
		return cpustate
	}

	stoppedthread := schedata.currentthread
	for i := 0; i < royxat.Hajmi_2; i++ {
		thread := (*TThread)(royxat.Getat(i))
		if thread != nil && thread.Cpustate == cpustate {
			stoppedthread = thread
			break
		}
	}
	stoppedthread.Cpustate = cpustate
	stoppedthread.Threadstate = Stopped
	schedata.currentthread = stoppedthread

	keyingithread := schedata.GetKeyingiTayyorthread()
	if keyingithread == nil || keyingithread == stoppedthread || keyingithread.Cpustate == nil || keyingithread.Cpustate == cpustate {
		setthreadexitloopstate(cpustate)
		return cpustate
	}

	schedata.currentthread = keyingithread
	if keyingithread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, keyingithread.Stack+ThreadstackHajmi)
	}
	setcr3(keyingithread.SAHIFAJildentry)
	setgs(keyingithread.Cpustate.Gs)
	return keyingithread.Cpustate
}

func InitialthreadFoydalanuvchijump(thread *TThread) {

	Disableint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+ThreadstackHajmi)

	setcr3(thread.SAHIFAJildentry)
	setgs(thread.Cpustate.Gs)

	schedata.currentthread = thread
	schedata.Yoqilgan = true

	eip := thread.Cpustate.Eip
	foydalanuvchiesp := thread.Foydalanuvchistack_2 + thread.FoydalanuvchistackHajmi_2
	eflags := thread.Cpustate.Eflags
	cs := thread.Cpustate.Cs
	esp := schedata.tss.Getesp0()

	console_2.MChopetish(([]byte)("jump["))
	console_2.MUnsignedinteger32Chopetish(eip)
	console_2.MChopetish(([]byte)(":"))
	console_2.MUnsignedinteger32Chopetish(foydalanuvchiesp)
	console_2.MChopetish(([]byte)(":"))
	console_2.MUnsignedinteger32Chopetish(eflags)
	console_2.MChopetish(([]byte)(":"))
	console_2.MUnsignedinteger32Chopetish(cs)
	console_2.MChopetish(([]byte)(":"))

	console_2.MUnsignedinteger32Chopetish(esp)
	console_2.MChopetish(([]byte)("]"))

	userprocentry := thread.Cpustate.Ecx
	globaloffsettable_2 := thread.Cpustate.Edx
	dynamic := thread.Cpustate.Esi

	PortYozishbyte(0x20, 0x20)
	jumpusermodeiret(eip, foydalanuvchiesp, eflags, userprocentry, globaloffsettable_2, dynamic)
	console_2.MChopetish(([]byte)("usermode end"))
}
func chopetishesp(esp uint32) {
	console_2.MChopetish(([]byte)("esp["))
	console_2.MUnsignedinteger32Chopetish(esp)
}
