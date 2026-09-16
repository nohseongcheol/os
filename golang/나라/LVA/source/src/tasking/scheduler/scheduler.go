/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "ports"
import . "util/saraksts"

import . "pārtraukums"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "atmiņamanager"

const SchedulerBiežums = 1
const KernelheapStartēt = 1024 * 1024
const schedulerAtkļūdot = false
const pitBiežums = 100

var saraksts LinkedSaraksts

type Schedulerdata struct {
	biežums		uint32
	tickcount	uint32

	switchforced	bool

	Ieslēgt	bool

	pašreizējaisthread	*TThread
	tss			*Tssieraksts
}

var schedata Schedulerdata = Schedulerdata{}

func (pats *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.biežums = SchedulerBiežums
	schedata.pašreizējaisthread = nil
	schedata.Ieslēgt = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var pašreizējaisthreadSaturs int = 0
var nākamaisprocessid uint32 = 1

func Allocatepid() uint32 {
	pid := nākamaisprocessid
	nākamaisprocessid++
	return pid
}

func (pats *Schedulerdata) GetNākamaisGatavsthread() *TThread {
	if saraksts.Izmērs_2 <= 0 {
		return nil
	}

	if schedata.pašreizējaisthread != nil {
		pašreizējaisthreadSaturs = saraksts.Satursno(uintptr(Pointer(schedata.pašreizējaisthread)))
		if pašreizējaisthreadSaturs < 0 {
			pašreizējaisthreadSaturs = 0
		}
	} else {
		pašreizējaisthreadSaturs = -1
	}

	for checked := 0; checked < saraksts.Izmērs_2; checked++ {
		pašreizējaisthreadSaturs++
		if pašreizējaisthreadSaturs >= saraksts.Izmērs_2 {
			pašreizējaisthreadSaturs = 0
		}
		thread := (*TThread)(saraksts.Getat(pašreizējaisthreadSaturs))
		if thread != nil && thread.ThreadStāvoklis != Blocked && thread.ThreadStāvoklis != Apturēts {
			if schedulerAtkļūdot {
				console_2.MDrukāt("ti:")
				console_2.MUnsignedinteger32Drukāt(uint32(pašreizējaisthreadSaturs))
				console_2.MDrukāt(":")
				console_2.MUnsignedinteger32Drukāt(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.pašreizējaisthread

}
func (pats *Scheduler) Pievienotthread(thread *TThread) {
	if thread == nil {
		return
	}
	saraksts.Append_to_list(uintptr(Pointer(thread)))
}
func Pievienotrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	saraksts.Append_to_list(uintptr(Pointer(thread)))
}

func Pašreizējaispid() uint32 {
	if schedata.pašreizējaisthread == nil || schedata.pašreizējaisthread.Pid == 0 {
		return 1
	}
	return schedata.pašreizējaisthread.Pid
}

func Pašreizējaisvecākspid() uint32 {
	if schedata.pašreizējaisthread == nil {
		return 0
	}
	return schedata.pašreizējaisthread.Vecākspid
}
func (pats *Scheduler) Izņemtthread(thread *TThread) {
	saraksts.Izņemt(uintptr(Pointer(thread)))
}

func (pats *Scheduler) Izņemtthreadat(saturs int) {
	saraksts.Izņemtat(saturs)
}

type Scheduler struct {
	TPārtraukumshandler
}

func (pats *Scheduler) Init(manager *TPārtraukumsmanager, mem *mem.TAtmiņamanager, tss *Tssieraksts) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitBiežums)

	saraksts = LinkedSaraksts{}
	saraksts.Init(mem)
	console_2.MDrukāt("list:")
	console_2.MUnsignedinteger32Drukāt(uint32(uintptr(Pointer(&saraksts))))

	pārtraukumshandler = handlePārtraukums
	var address uintptr
	address = uintptr(Pointer(&pārtraukumshandler))
	pats.TPārtraukumshandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (pats *Scheduler) Ieslēgt(ieslēgt bool) {
	schedata.Ieslēgt = ieslēgt
}

func initpit(biežums uint32) {
	if biežums == 0 {
		return
	}
	divisor := uint32(1193180) / biežums
	PortsRakstītbyte(0x43, 0x36)
	PortsRakstītbyte(0x40, uint8(divisor&0xFF))
	PortsRakstītbyte(0x40, uint8((divisor>>8)&0xFF))
}

func kopads(dssegment uint32)
func kopags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func atjaunotfpregs(buffer_2 uintptr)

var jmpLietotājs uint32 = 0
var pārtraukumshandler func(uint32) uint32

func schedulestack(fn func())
func kopacr3(address uint32)
func getcr3() uint32

func handlePārtraukums(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerAtkļūdot {
		console_2.MDrukātxy(([]byte)("sche1:"), 1, 17)

		console_2.MDrukāt(":")
		console_2.MUnsignedinteger32Drukāt(esp)
		console_2.MDrukāt(":")

		console_2.MUnsignedinteger32Drukāt(uint32(schedata.tickcount))
		console_2.MDrukāt(":")
		console_2.MUnsignedinteger32Drukāt(KernelheapStartēt)
	}

	if schedata.tickcount == schedata.biežums {
		schedata.tickcount = 0

		if saraksts.Izmērs_2 > 0 && schedata.Ieslēgt == true {
			var nākamaisthread = schedata.GetNākamaisGatavsthread()
			if nākamaisthread == nil {
				return esp
			}
			if schedata.pašreizējaisthread == nil {
				MEmergencylogvirkne("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogvirkne(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(nākamaisthread))))
				MEmergencylogvirkne(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(nākamaisthread.CpuStāvoklis))))
				MEmergencylogvirkne(" state=")
				MEmergencylogunsignedinteger32(uint32(nākamaisthread.ThreadStāvoklis))
				MEmergencylogvirkne(" eip=")
				MEmergencylogunsignedinteger32(nākamaisthread.CpuStāvoklis.Eip)
				MEmergencylogvirkne(" cs=")
				MEmergencylogunsignedinteger32(nākamaisthread.CpuStāvoklis.Cs)
				MEmergencylogvirkne("\n")
			}

			if esp >= KernelheapStartēt && schedata.pašreizējaisthread != nil {
				schedata.pašreizējaisthread.CpuStāvoklis = (*TcpuStāvoklis)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.pašreizējaisthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.pašreizējaisthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerAtkļūdot {
					console_2.MDrukāt(([]byte)("backup"))
					console_2.MUnsignedinteger32Drukāt(esp)
				}
			}

			address := uintptr(Pointer(&(nākamaisthread.Fpubuffer)))
			offset := nākamaisthread.Fpuoffset
			if offset != 0xffffffff {
				atjaunotfpregs(address + offset)
				if schedulerAtkļūdot {
					console_2.MDrukāt(([]byte)("restore"))
				}
			}

			schedata.pašreizējaisthread = nākamaisthread

			if schedata.pašreizējaisthread.ThreadStāvoklis == Palaists {
				schedata.pašreizējaisthread.ThreadStāvoklis = Gatavs

				InitialthreadLietotājsjump(schedata.pašreizējaisthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(nākamaisthread.CpuStāvoklis)))
			if nākamaisthread.Stack != 0 {
				schedata.tss.Kopastack(Segkerneldata, nākamaisthread.Stack+ThreadstackIzmērs)
			}

			kopacr3(nākamaisthread.LapaMapeieraksts)
			kopags(nākamaisthread.CpuStāvoklis.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Izslēgtint()

func getesp() uint32
func threadIzietloop()

func kopathreadIzietloopStāvoklis(cpuStāvoklis *TcpuStāvoklis) {
	cpuStāvoklis.Eip = uint32(ValueOf(threadIzietloop).Pointer())
	cpuStāvoklis.Cs = Segkernelcode
	cpuStāvoklis.Ds = Segkerneldata
	cpuStāvoklis.Es = Segkerneldata
	cpuStāvoklis.Fs = Segkerneldata
	cpuStāvoklis.Gs = Segkernelgs
	cpuStāvoklis.Ss = Segkerneldata
	cpuStāvoklis.Eflags = 0x202
}

func ApturētPašreizējaisthread(cpuStāvoklis *TcpuStāvoklis) *TcpuStāvoklis {
	if schedata.pašreizējaisthread == nil {
		kopathreadIzietloopStāvoklis(cpuStāvoklis)
		return cpuStāvoklis
	}

	apturētsthread := schedata.pašreizējaisthread
	for i := 0; i < saraksts.Izmērs_2; i++ {
		thread := (*TThread)(saraksts.Getat(i))
		if thread != nil && thread.CpuStāvoklis == cpuStāvoklis {
			apturētsthread = thread
			break
		}
	}
	apturētsthread.CpuStāvoklis = cpuStāvoklis
	apturētsthread.ThreadStāvoklis = Apturēts
	schedata.pašreizējaisthread = apturētsthread

	nākamaisthread := schedata.GetNākamaisGatavsthread()
	if nākamaisthread == nil || nākamaisthread == apturētsthread || nākamaisthread.CpuStāvoklis == nil || nākamaisthread.CpuStāvoklis == cpuStāvoklis {
		kopathreadIzietloopStāvoklis(cpuStāvoklis)
		return cpuStāvoklis
	}

	schedata.pašreizējaisthread = nākamaisthread
	if nākamaisthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Kopastack(Segkerneldata, nākamaisthread.Stack+ThreadstackIzmērs)
	}
	kopacr3(nākamaisthread.LapaMapeieraksts)
	kopags(nākamaisthread.CpuStāvoklis.Gs)
	return nākamaisthread.CpuStāvoklis
}

func InitialthreadLietotājsjump(thread *TThread) {

	Izslēgtint()

	schedata.tss.Kopastack(Segkerneldata, thread.Stack+ThreadstackIzmērs)

	kopacr3(thread.LapaMapeieraksts)
	kopags(thread.CpuStāvoklis.Gs)

	schedata.pašreizējaisthread = thread
	schedata.Ieslēgt = true

	eip := thread.CpuStāvoklis.Eip
	lietotājsesp := thread.Lietotājsstack_2 + thread.LietotājsstackIzmērs_2
	eflags := thread.CpuStāvoklis.Eflags
	cs := thread.CpuStāvoklis.Cs
	esp := schedata.tss.Getesp0()

	console_2.MDrukāt(([]byte)("jump["))
	console_2.MUnsignedinteger32Drukāt(eip)
	console_2.MDrukāt(([]byte)(":"))
	console_2.MUnsignedinteger32Drukāt(lietotājsesp)
	console_2.MDrukāt(([]byte)(":"))
	console_2.MUnsignedinteger32Drukāt(eflags)
	console_2.MDrukāt(([]byte)(":"))
	console_2.MUnsignedinteger32Drukāt(cs)
	console_2.MDrukāt(([]byte)(":"))

	console_2.MUnsignedinteger32Drukāt(esp)
	console_2.MDrukāt(([]byte)("]"))

	userprocieraksts := thread.CpuStāvoklis.Ecx
	globālaisoffsetTabula_2 := thread.CpuStāvoklis.Edx
	dynamic := thread.CpuStāvoklis.Esi

	PortsRakstītbyte(0x20, 0x20)
	jumpusermodeiret(eip, lietotājsesp, eflags, userprocieraksts, globālaisoffsetTabula_2, dynamic)
	console_2.MDrukāt(([]byte)("usermode end"))
}
func drukātesp(esp uint32) {
	console_2.MDrukāt(([]byte)("esp["))
	console_2.MUnsignedinteger32Drukāt(esp)
}
