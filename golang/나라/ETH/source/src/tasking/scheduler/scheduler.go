package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/ዝርዝር"

import . "ማቋረጫ"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "ማስታወሻmanager"

const Schedulerተደጋጋሚነት = 1
const Kernelheapማስጀመሪያ = 1024 * 1024
const schedulerdebug = false
const pitተደጋጋሚነት = 100

var ዝርዝር Linkedዝርዝር

type Schedulerdata struct {
	ተደጋጋሚነት		uint32
	tickcount	uint32

	switchforced	bool

	Eያስችላል	bool

	currentthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.ተደጋጋሚነት = Schedulerተደጋጋሚነት
	schedata.currentthread = nil
	schedata.Eያስችላል = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadማውጫ int = 0
var የሚቀጥለውሂደቶችመለያ uint32 = 1

func Allocatepid() uint32 {
	pid := የሚቀጥለውሂደቶችመለያ
	የሚቀጥለውሂደቶችመለያ++
	return pid
}

func (self *Schedulerdata) Getየሚቀጥለውዝግጁthread() *TThread {
	if ዝርዝር.Sመጠን_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadማውጫ = ዝርዝር.Iማውጫከ(uintptr(Pointer(schedata.currentthread)))
		if currentthreadማውጫ < 0 {
			currentthreadማውጫ = 0
		}
	} else {
		currentthreadማውጫ = -1
	}

	for checked := 0; checked < ዝርዝር.Sመጠን_2; checked++ {
		currentthreadማውጫ++
		if currentthreadማውጫ >= ዝርዝር.Sመጠን_2 {
			currentthreadማውጫ = 0
		}
		thread := (*TThread)(ዝርዝር.Getat(currentthreadማውጫ))
		if thread != nil && thread.Threadሁኔታ != Blocked && thread.Threadሁኔታ != Sቆሟል {
			if schedulerdebug {
				console_2.Mማተሚያ("ti:")
				console_2.MUnsignedinteger32ማተሚያ(uint32(currentthreadማውጫ))
				console_2.Mማተሚያ(":")
				console_2.MUnsignedinteger32ማተሚያ(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (self *Scheduler) Aመጨመሪያthread(thread *TThread) {
	if thread == nil {
		return
	}
	ዝርዝር.Append_to_list(uintptr(Pointer(thread)))
}
func Aመጨመሪያrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	ዝርዝር.Append_to_list(uintptr(Pointer(thread)))
}

func Currentpid() uint32 {
	if schedata.currentthread == nil || schedata.currentthread.Pid == 0 {
		return 1
	}
	return schedata.currentthread.Pid
}

func Currentወላጅpid() uint32 {
	if schedata.currentthread == nil {
		return 0
	}
	return schedata.currentthread.Pወላጅpid
}
func (self *Scheduler) Rአስወግድthread(thread *TThread) {
	ዝርዝር.Rአስወግድ(uintptr(Pointer(thread)))
}

func (self *Scheduler) Rአስወግድthreadat(ማውጫ int) {
	ዝርዝር.Rአስወግድat(ማውጫ)
}

type Scheduler struct {
	Tማቋረጫhandler
}

func (self *Scheduler) Init(manager *Tማቋረጫmanager, mem *mem.Tማስታወሻmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitተደጋጋሚነት)

	ዝርዝር = Linkedዝርዝር{}
	ዝርዝር.Init(mem)
	console_2.Mማተሚያ("list:")
	console_2.MUnsignedinteger32ማተሚያ(uint32(uintptr(Pointer(&ዝርዝር))))

	ማቋረጫhandler = handleማቋረጫ
	var address uintptr
	address = uintptr(Pointer(&ማቋረጫhandler))
	self.Tማቋረጫhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Eያስችላል(ያስችላል bool) {
	schedata.Eያስችላል = ያስችላል
}

func initpit(ተደጋጋሚነት uint32) {
	if ተደጋጋሚነት == 0 {
		return
	}
	divisor := uint32(1193180) / ተደጋጋሚነት
	Portመጻፊያbyte(0x43, 0x36)
	Portመጻፊያbyte(0x40, uint8(divisor&0xFF))
	Portመጻፊያbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setds(dssegment uint32)
func setgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func እንደነበርመመለሻfpregs(buffer_2 uintptr)

var jmpተጠቃሚ uint32 = 0
var ማቋረጫhandler func(uint32) uint32

func schedulestack(fn func())
func setcr3(address uint32)
func getcr3() uint32

func handleማቋረጫ(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.Mማተሚያxy(([]byte)("sche1:"), 1, 17)

		console_2.Mማተሚያ(":")
		console_2.MUnsignedinteger32ማተሚያ(esp)
		console_2.Mማተሚያ(":")

		console_2.MUnsignedinteger32ማተሚያ(uint32(schedata.tickcount))
		console_2.Mማተሚያ(":")
		console_2.MUnsignedinteger32ማተሚያ(Kernelheapማስጀመሪያ)
	}

	if schedata.tickcount == schedata.ተደጋጋሚነት {
		schedata.tickcount = 0

		if ዝርዝር.Sመጠን_2 > 0 && schedata.Eያስችላል == true {
			var የሚቀጥለውthread = schedata.Getየሚቀጥለውዝግጁthread()
			if የሚቀጥለውthread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogሐረግ("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogሐረግ(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(የሚቀጥለውthread))))
				MEmergencylogሐረግ(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(የሚቀጥለውthread.Cpuሁኔታ))))
				MEmergencylogሐረግ(" state=")
				MEmergencylogunsignedinteger32(uint32(የሚቀጥለውthread.Threadሁኔታ))
				MEmergencylogሐረግ(" eip=")
				MEmergencylogunsignedinteger32(የሚቀጥለውthread.Cpuሁኔታ.Eip)
				MEmergencylogሐረግ(" cs=")
				MEmergencylogunsignedinteger32(የሚቀጥለውthread.Cpuሁኔታ.Cs)
				MEmergencylogሐረግ("\n")
			}

			if esp >= Kernelheapማስጀመሪያ && schedata.currentthread != nil {
				schedata.currentthread.Cpuሁኔታ = (*Tcpuሁኔታ)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.Mማተሚያ(([]byte)("backup"))
					console_2.MUnsignedinteger32ማተሚያ(esp)
				}
			}

			address := uintptr(Pointer(&(የሚቀጥለውthread.Fpubuffer)))
			offset := የሚቀጥለውthread.Fpuoffset
			if offset != 0xffffffff {
				እንደነበርመመለሻfpregs(address + offset)
				if schedulerdebug {
					console_2.Mማተሚያ(([]byte)("restore"))
				}
			}

			schedata.currentthread = የሚቀጥለውthread

			if schedata.currentthread.Threadሁኔታ == Sጀምሯል {
				schedata.currentthread.Threadሁኔታ = Rዝግጁ

				Initialthreadተጠቃሚjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(የሚቀጥለውthread.Cpuሁኔታ)))
			if የሚቀጥለውthread.Stack != 0 {
				schedata.tss.Setstack(Segkerneldata, የሚቀጥለውthread.Stack+Threadstackመጠን)
			}

			setcr3(የሚቀጥለውthread.Pገጽዳይሬክቶሪentry)
			setgs(የሚቀጥለውthread.Cpuሁኔታ.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Dአበላሽint()

func getesp() uint32
func threadውጣloop()

func setthreadውጣloopሁኔታ(cpuሁኔታ *Tcpuሁኔታ) {
	cpuሁኔታ.Eip = uint32(ValueOf(threadውጣloop).Pointer())
	cpuሁኔታ.Cs = Segkernelcode
	cpuሁኔታ.Ds = Segkerneldata
	cpuሁኔታ.Es = Segkerneldata
	cpuሁኔታ.Fs = Segkerneldata
	cpuሁኔታ.Gs = Segkernelgs
	cpuሁኔታ.Ss = Segkerneldata
	cpuሁኔታ.Eflags = 0x202
}

func Sማስቆሚያcurrentthread(cpuሁኔታ *Tcpuሁኔታ) *Tcpuሁኔታ {
	if schedata.currentthread == nil {
		setthreadውጣloopሁኔታ(cpuሁኔታ)
		return cpuሁኔታ
	}

	ቆሟልthread := schedata.currentthread
	for i := 0; i < ዝርዝር.Sመጠን_2; i++ {
		thread := (*TThread)(ዝርዝር.Getat(i))
		if thread != nil && thread.Cpuሁኔታ == cpuሁኔታ {
			ቆሟልthread = thread
			break
		}
	}
	ቆሟልthread.Cpuሁኔታ = cpuሁኔታ
	ቆሟልthread.Threadሁኔታ = Sቆሟል
	schedata.currentthread = ቆሟልthread

	የሚቀጥለውthread := schedata.Getየሚቀጥለውዝግጁthread()
	if የሚቀጥለውthread == nil || የሚቀጥለውthread == ቆሟልthread || የሚቀጥለውthread.Cpuሁኔታ == nil || የሚቀጥለውthread.Cpuሁኔታ == cpuሁኔታ {
		setthreadውጣloopሁኔታ(cpuሁኔታ)
		return cpuሁኔታ
	}

	schedata.currentthread = የሚቀጥለውthread
	if የሚቀጥለውthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setstack(Segkerneldata, የሚቀጥለውthread.Stack+Threadstackመጠን)
	}
	setcr3(የሚቀጥለውthread.Pገጽዳይሬክቶሪentry)
	setgs(የሚቀጥለውthread.Cpuሁኔታ.Gs)
	return የሚቀጥለውthread.Cpuሁኔታ
}

func Initialthreadተጠቃሚjump(thread *TThread) {

	Dአበላሽint()

	schedata.tss.Setstack(Segkerneldata, thread.Stack+Threadstackመጠን)

	setcr3(thread.Pገጽዳይሬክቶሪentry)
	setgs(thread.Cpuሁኔታ.Gs)

	schedata.currentthread = thread
	schedata.Eያስችላል = true

	eip := thread.Cpuሁኔታ.Eip
	ተጠቃሚesp := thread.Uተጠቃሚstack_2 + thread.Uተጠቃሚstackመጠን_2
	eflags := thread.Cpuሁኔታ.Eflags
	cs := thread.Cpuሁኔታ.Cs
	esp := schedata.tss.Getesp0()

	console_2.Mማተሚያ(([]byte)("jump["))
	console_2.MUnsignedinteger32ማተሚያ(eip)
	console_2.Mማተሚያ(([]byte)(":"))
	console_2.MUnsignedinteger32ማተሚያ(ተጠቃሚesp)
	console_2.Mማተሚያ(([]byte)(":"))
	console_2.MUnsignedinteger32ማተሚያ(eflags)
	console_2.Mማተሚያ(([]byte)(":"))
	console_2.MUnsignedinteger32ማተሚያ(cs)
	console_2.Mማተሚያ(([]byte)(":"))

	console_2.MUnsignedinteger32ማተሚያ(esp)
	console_2.Mማተሚያ(([]byte)("]"))

	userprocentry := thread.Cpuሁኔታ.Ecx
	አለምአቀፍoffsetሰንጠረዥ_2 := thread.Cpuሁኔታ.Edx
	dynamic := thread.Cpuሁኔታ.Esi

	Portመጻፊያbyte(0x20, 0x20)
	jumpusermodeiret(eip, ተጠቃሚesp, eflags, userprocentry, አለምአቀፍoffsetሰንጠረዥ_2, dynamic)
	console_2.Mማተሚያ(([]byte)("usermode end"))
}
func ማተሚያesp(esp uint32) {
	console_2.Mማተሚያ(([]byte)("esp["))
	console_2.MUnsignedinteger32ማተሚያ(esp)
}
