/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/listi"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "minnimanager"

const Schedulerfrequency = 1
const KernelheapRæsa = 1024 * 1024
const schedulerAflúsa = false
const pitfrequency = 100

var listi LinkedListi

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Virkjað	bool

	núverandithread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (sjálft *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.núverandithread = nil
	schedata.Virkjað = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var núverandithreadindex int = 0
var næstaprocessAuðkenni uint32 = 1

func Allocatepid() uint32 {
	pid := næstaprocessAuðkenni
	næstaprocessAuðkenni++
	return pid
}

func (sjálft *Schedulerdata) GetNæstaTilbúiðthread() *TThread {
	if listi.Stærð_2 <= 0 {
		return nil
	}

	if schedata.núverandithread != nil {
		núverandithreadindex = listi.Indexaf(uintptr(Pointer(schedata.núverandithread)))
		if núverandithreadindex < 0 {
			núverandithreadindex = 0
		}
	} else {
		núverandithreadindex = -1
	}

	for checked := 0; checked < listi.Stærð_2; checked++ {
		núverandithreadindex++
		if núverandithreadindex >= listi.Stærð_2 {
			núverandithreadindex = 0
		}
		thread := (*TThread)(listi.Getat(núverandithreadindex))
		if thread != nil && thread.ThreadStaða != Blocked && thread.ThreadStaða != Stopped {
			if schedulerAflúsa {
				console_2.MPrenta("ti:")
				console_2.MUnsignedinteger32Prenta(uint32(núverandithreadindex))
				console_2.MPrenta(":")
				console_2.MUnsignedinteger32Prenta(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.núverandithread

}
func (sjálft *Scheduler) Bætaviðthread(thread *TThread) {
	if thread == nil {
		return
	}
	listi.Append_to_list(uintptr(Pointer(thread)))
}
func Bætaviðrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	listi.Append_to_list(uintptr(Pointer(thread)))
}

func Núverandipid() uint32 {
	if schedata.núverandithread == nil || schedata.núverandithread.Pid == 0 {
		return 1
	}
	return schedata.núverandithread.Pid
}

func Núverandiforeldripid() uint32 {
	if schedata.núverandithread == nil {
		return 0
	}
	return schedata.núverandithread.Foreldripid
}
func (sjálft *Scheduler) Fjarlægjathread(thread *TThread) {
	listi.Fjarlægja(uintptr(Pointer(thread)))
}

func (sjálft *Scheduler) Fjarlægjathreadat(index int) {
	listi.Fjarlægjaat(index)
}

type Scheduler struct {
	TInterrupthandler
}

func (sjálft *Scheduler) Init(manager *TInterruptmanager, mem *mem.TMinnimanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	listi = LinkedListi{}
	listi.Init(mem)
	console_2.MPrenta("list:")
	console_2.MUnsignedinteger32Prenta(uint32(uintptr(Pointer(&listi))))

	interrupthandler = haldfanginterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	sjálft.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (sjálft *Scheduler) Virkjað(virkjað bool) {
	schedata.Virkjað = virkjað
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	PortSkriftbyte(0x43, 0x36)
	PortSkriftbyte(0x40, uint8(divisor&0xFF))
	PortSkriftbyte(0x40, uint8((divisor>>8)&0xFF))
}

func setjads(dssegment uint32)
func setjags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func endurheimtafpregs(buffer_2 uintptr)

var jmpNotandi uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func setjacr3(address uint32)
func getcr3() uint32

func haldfanginterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerAflúsa {
		console_2.MPrentaxy(([]byte)("sche1:"), 1, 17)

		console_2.MPrenta(":")
		console_2.MUnsignedinteger32Prenta(esp)
		console_2.MPrenta(":")

		console_2.MUnsignedinteger32Prenta(uint32(schedata.tickcount))
		console_2.MPrenta(":")
		console_2.MUnsignedinteger32Prenta(KernelheapRæsa)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if listi.Stærð_2 > 0 && schedata.Virkjað == true {
			var næstathread = schedata.GetNæstaTilbúiðthread()
			if næstathread == nil {
				return esp
			}
			if schedata.núverandithread == nil {
				MEmergencylogStrengur("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogStrengur(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(næstathread))))
				MEmergencylogStrengur(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(næstathread.CpuStaða))))
				MEmergencylogStrengur(" state=")
				MEmergencylogunsignedinteger32(uint32(næstathread.ThreadStaða))
				MEmergencylogStrengur(" eip=")
				MEmergencylogunsignedinteger32(næstathread.CpuStaða.Eip)
				MEmergencylogStrengur(" cs=")
				MEmergencylogunsignedinteger32(næstathread.CpuStaða.Cs)
				MEmergencylogStrengur("\n")
			}

			if esp >= KernelheapRæsa && schedata.núverandithread != nil {
				schedata.núverandithread.CpuStaða = (*TcpuStaða)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.núverandithread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.núverandithread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerAflúsa {
					console_2.MPrenta(([]byte)("backup"))
					console_2.MUnsignedinteger32Prenta(esp)
				}
			}

			address := uintptr(Pointer(&(næstathread.Fpubuffer)))
			offset := næstathread.Fpuoffset
			if offset != 0xffffffff {
				endurheimtafpregs(address + offset)
				if schedulerAflúsa {
					console_2.MPrenta(([]byte)("restore"))
				}
			}

			schedata.núverandithread = næstathread

			if schedata.núverandithread.ThreadStaða == Started {
				schedata.núverandithread.ThreadStaða = Tilbúið

				InitialthreadNotandijump(schedata.núverandithread)
				return esp
			}

			esp = uint32(uintptr(Pointer(næstathread.CpuStaða)))
			if næstathread.Stack != 0 {
				schedata.tss.Setjastack(Segkerneldata, næstathread.Stack+ThreadstackStærð)
			}

			setjacr3(næstathread.Síðamappaentry)
			setjags(næstathread.CpuStaða.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Afvirkjaint()

func getesp() uint32
func threadHættaloop()

func setjathreadHættaloopStaða(cpuStaða *TcpuStaða) {
	cpuStaða.Eip = uint32(ValueOf(threadHættaloop).Pointer())
	cpuStaða.Cs = Segkernelcode
	cpuStaða.Ds = Segkerneldata
	cpuStaða.Es = Segkerneldata
	cpuStaða.Fs = Segkerneldata
	cpuStaða.Gs = Segkernelgs
	cpuStaða.Ss = Segkerneldata
	cpuStaða.Eflags = 0x202
}

func StöðvaNúverandithread(cpuStaða *TcpuStaða) *TcpuStaða {
	if schedata.núverandithread == nil {
		setjathreadHættaloopStaða(cpuStaða)
		return cpuStaða
	}

	stoppedthread := schedata.núverandithread
	for i := 0; i < listi.Stærð_2; i++ {
		thread := (*TThread)(listi.Getat(i))
		if thread != nil && thread.CpuStaða == cpuStaða {
			stoppedthread = thread
			break
		}
	}
	stoppedthread.CpuStaða = cpuStaða
	stoppedthread.ThreadStaða = Stopped
	schedata.núverandithread = stoppedthread

	næstathread := schedata.GetNæstaTilbúiðthread()
	if næstathread == nil || næstathread == stoppedthread || næstathread.CpuStaða == nil || næstathread.CpuStaða == cpuStaða {
		setjathreadHættaloopStaða(cpuStaða)
		return cpuStaða
	}

	schedata.núverandithread = næstathread
	if næstathread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Setjastack(Segkerneldata, næstathread.Stack+ThreadstackStærð)
	}
	setjacr3(næstathread.Síðamappaentry)
	setjags(næstathread.CpuStaða.Gs)
	return næstathread.CpuStaða
}

func InitialthreadNotandijump(thread *TThread) {

	Afvirkjaint()

	schedata.tss.Setjastack(Segkerneldata, thread.Stack+ThreadstackStærð)

	setjacr3(thread.Síðamappaentry)
	setjags(thread.CpuStaða.Gs)

	schedata.núverandithread = thread
	schedata.Virkjað = true

	eip := thread.CpuStaða.Eip
	notandiesp := thread.Notandistack_2 + thread.NotandistackStærð_2
	eflags_2 := thread.CpuStaða.Eflags
	cs := thread.CpuStaða.Cs
	esp := schedata.tss.Getesp0()

	console_2.MPrenta(([]byte)("jump["))
	console_2.MUnsignedinteger32Prenta(eip)
	console_2.MPrenta(([]byte)(":"))
	console_2.MUnsignedinteger32Prenta(notandiesp)
	console_2.MPrenta(([]byte)(":"))
	console_2.MUnsignedinteger32Prenta(eflags_2)
	console_2.MPrenta(([]byte)(":"))
	console_2.MUnsignedinteger32Prenta(cs)
	console_2.MPrenta(([]byte)(":"))

	console_2.MUnsignedinteger32Prenta(esp)
	console_2.MPrenta(([]byte)("]"))

	userprocentry := thread.CpuStaða.Ecx
	víðværtoffsetTafla_2 := thread.CpuStaða.Edx
	breytilegt := thread.CpuStaða.Esi

	PortSkriftbyte(0x20, 0x20)
	jumpusermodeiret(eip, notandiesp, eflags_2, userprocentry, víðværtoffsetTafla_2, breytilegt)
	console_2.MPrenta(([]byte)("usermode end"))
}
func prentaesp(esp uint32) {
	console_2.MPrenta(([]byte)("esp["))
	console_2.MUnsignedinteger32Prenta(esp)
}
