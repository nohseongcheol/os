package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/nimekiri"

import . "katkestus"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "mälumanager"

const SchedulerSagedus = 1
const KernelheapKäivita = 1024 * 1024
const schedulerSilumine = false
const pitSagedus = 100

var nimekiri LinkedNimekiri

type Schedulerdata struct {
	sagedus		uint32
	tickcount	uint32

	switchforced	bool

	Lubatud	bool

	käesolevthread	*TThread
	tss		*Tsskirje
}

var schedata Schedulerdata = Schedulerdata{}

func (ise *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.sagedus = SchedulerSagedus
	schedata.käesolevthread = nil
	schedata.Lubatud = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var käesolevthreadSisukord int = 0
var järgmineProtsessid uint32 = 1

func Allocatepid() uint32 {
	pid := järgmineProtsessid
	järgmineProtsessid++
	return pid
}

func (ise *Schedulerdata) GetJärgmineValmisthread() *TThread {
	if nimekiri.Suurus_2 <= 0 {
		return nil
	}

	if schedata.käesolevthread != nil {
		käesolevthreadSisukord = nimekiri.Sisukordof(uintptr(Pointer(schedata.käesolevthread)))
		if käesolevthreadSisukord < 0 {
			käesolevthreadSisukord = 0
		}
	} else {
		käesolevthreadSisukord = -1
	}

	for checked := 0; checked < nimekiri.Suurus_2; checked++ {
		käesolevthreadSisukord++
		if käesolevthreadSisukord >= nimekiri.Suurus_2 {
			käesolevthreadSisukord = 0
		}
		thread := (*TThread)(nimekiri.Getat(käesolevthreadSisukord))
		if thread != nil && thread.ThreadOlek != Blocked && thread.ThreadOlek != Seisatud {
			if schedulerSilumine {
				console_2.MPrindi("ti:")
				console_2.MUnsignedinteger32Prindi(uint32(käesolevthreadSisukord))
				console_2.MPrindi(":")
				console_2.MUnsignedinteger32Prindi(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.käesolevthread

}
func (ise *Scheduler) Lisathread(thread *TThread) {
	if thread == nil {
		return
	}
	nimekiri.Append_to_list(uintptr(Pointer(thread)))
}
func Lisarunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	nimekiri.Append_to_list(uintptr(Pointer(thread)))
}

func Käesolevpid() uint32 {
	if schedata.käesolevthread == nil || schedata.käesolevthread.Pid == 0 {
		return 1
	}
	return schedata.käesolevthread.Pid
}

func Käesolevvanempid() uint32 {
	if schedata.käesolevthread == nil {
		return 0
	}
	return schedata.käesolevthread.Vanempid
}
func (ise *Scheduler) Eemaldathread(thread *TThread) {
	nimekiri.Eemalda(uintptr(Pointer(thread)))
}

func (ise *Scheduler) Eemaldathreadat(sisukord int) {
	nimekiri.Eemaldaat(sisukord)
}

type Scheduler struct {
	TKatkestushandler
}

func (ise *Scheduler) Init(manager *TKatkestusmanager, mem *mem.TMälumanager, tss *Tsskirje) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitSagedus)

	nimekiri = LinkedNimekiri{}
	nimekiri.Init(mem)
	console_2.MPrindi("list:")
	console_2.MUnsignedinteger32Prindi(uint32(uintptr(Pointer(&nimekiri))))

	katkestushandler = handleKatkestus
	var address uintptr
	address = uintptr(Pointer(&katkestushandler))
	ise.TKatkestushandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (ise *Scheduler) Lubatud(lubatud bool) {
	schedata.Lubatud = lubatud
}

func initpit(sagedus uint32) {
	if sagedus == 0 {
		return
	}
	divisor := uint32(1193180) / sagedus
	PortKirjutaminebyte(0x43, 0x36)
	PortKirjutaminebyte(0x40, uint8(divisor&0xFF))
	PortKirjutaminebyte(0x40, uint8((divisor>>8)&0xFF))
}

func määrads(dssegment uint32)
func määrags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func taastafpregs(buffer_2 uintptr)

var jmpKasutaja uint32 = 0
var katkestushandler func(uint32) uint32

func schedulestack(fn func())
func määracr3(address uint32)
func getcr3() uint32

func handleKatkestus(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerSilumine {
		console_2.MPrindixy(([]byte)("sche1:"), 1, 17)

		console_2.MPrindi(":")
		console_2.MUnsignedinteger32Prindi(esp)
		console_2.MPrindi(":")

		console_2.MUnsignedinteger32Prindi(uint32(schedata.tickcount))
		console_2.MPrindi(":")
		console_2.MUnsignedinteger32Prindi(KernelheapKäivita)
	}

	if schedata.tickcount == schedata.sagedus {
		schedata.tickcount = 0

		if nimekiri.Suurus_2 > 0 && schedata.Lubatud == true {
			var järgminethread = schedata.GetJärgmineValmisthread()
			if järgminethread == nil {
				return esp
			}
			if schedata.käesolevthread == nil {
				MEmergencylogstring("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogstring(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(järgminethread))))
				MEmergencylogstring(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(järgminethread.ProtsessorOlek))))
				MEmergencylogstring(" state=")
				MEmergencylogunsignedinteger32(uint32(järgminethread.ThreadOlek))
				MEmergencylogstring(" eip=")
				MEmergencylogunsignedinteger32(järgminethread.ProtsessorOlek.Eip)
				MEmergencylogstring(" cs=")
				MEmergencylogunsignedinteger32(järgminethread.ProtsessorOlek.Cs)
				MEmergencylogstring("\n")
			}

			if esp >= KernelheapKäivita && schedata.käesolevthread != nil {
				schedata.käesolevthread.ProtsessorOlek = (*TcpuOlek)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.käesolevthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.käesolevthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerSilumine {
					console_2.MPrindi(([]byte)("backup"))
					console_2.MUnsignedinteger32Prindi(esp)
				}
			}

			address := uintptr(Pointer(&(järgminethread.Fpubuffer)))
			offset := järgminethread.Fpuoffset
			if offset != 0xffffffff {
				taastafpregs(address + offset)
				if schedulerSilumine {
					console_2.MPrindi(([]byte)("restore"))
				}
			}

			schedata.käesolevthread = järgminethread

			if schedata.käesolevthread.ThreadOlek == Käivitatud {
				schedata.käesolevthread.ThreadOlek = Valmis

				InitialthreadKasutajajump(schedata.käesolevthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(järgminethread.ProtsessorOlek)))
			if järgminethread.Stack != 0 {
				schedata.tss.Määrastack(Segkerneldata, järgminethread.Stack+ThreadstackSuurus)
			}

			määracr3(järgminethread.LehekülgKataloogkirje)
			määrags(järgminethread.ProtsessorOlek.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Keelaint()

func getesp() uint32
func threadVäljuloop()

func määrathreadVäljuloopOlek(protsessorOlek *TcpuOlek) {
	protsessorOlek.Eip = uint32(ValueOf(threadVäljuloop).Pointer())
	protsessorOlek.Cs = Segkernelcode
	protsessorOlek.Ds = Segkerneldata
	protsessorOlek.Es = Segkerneldata
	protsessorOlek.Fs = Segkerneldata
	protsessorOlek.Gs = Segkernelgs
	protsessorOlek.Ss = Segkerneldata
	protsessorOlek.Eflags = 0x202
}

func PeataKäesolevthread(protsessorOlek *TcpuOlek) *TcpuOlek {
	if schedata.käesolevthread == nil {
		määrathreadVäljuloopOlek(protsessorOlek)
		return protsessorOlek
	}

	seisatudthread := schedata.käesolevthread
	for i := 0; i < nimekiri.Suurus_2; i++ {
		thread := (*TThread)(nimekiri.Getat(i))
		if thread != nil && thread.ProtsessorOlek == protsessorOlek {
			seisatudthread = thread
			break
		}
	}
	seisatudthread.ProtsessorOlek = protsessorOlek
	seisatudthread.ThreadOlek = Seisatud
	schedata.käesolevthread = seisatudthread

	järgminethread := schedata.GetJärgmineValmisthread()
	if järgminethread == nil || järgminethread == seisatudthread || järgminethread.ProtsessorOlek == nil || järgminethread.ProtsessorOlek == protsessorOlek {
		määrathreadVäljuloopOlek(protsessorOlek)
		return protsessorOlek
	}

	schedata.käesolevthread = järgminethread
	if järgminethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Määrastack(Segkerneldata, järgminethread.Stack+ThreadstackSuurus)
	}
	määracr3(järgminethread.LehekülgKataloogkirje)
	määrags(järgminethread.ProtsessorOlek.Gs)
	return järgminethread.ProtsessorOlek
}

func InitialthreadKasutajajump(thread *TThread) {

	Keelaint()

	schedata.tss.Määrastack(Segkerneldata, thread.Stack+ThreadstackSuurus)

	määracr3(thread.LehekülgKataloogkirje)
	määrags(thread.ProtsessorOlek.Gs)

	schedata.käesolevthread = thread
	schedata.Lubatud = true

	eip := thread.ProtsessorOlek.Eip
	kasutajaesp := thread.Kasutajastack_2 + thread.KasutajastackSuurus_2
	eflags := thread.ProtsessorOlek.Eflags
	cs := thread.ProtsessorOlek.Cs
	esp := schedata.tss.Getesp0()

	console_2.MPrindi(([]byte)("jump["))
	console_2.MUnsignedinteger32Prindi(eip)
	console_2.MPrindi(([]byte)(":"))
	console_2.MUnsignedinteger32Prindi(kasutajaesp)
	console_2.MPrindi(([]byte)(":"))
	console_2.MUnsignedinteger32Prindi(eflags)
	console_2.MPrindi(([]byte)(":"))
	console_2.MUnsignedinteger32Prindi(cs)
	console_2.MPrindi(([]byte)(":"))

	console_2.MUnsignedinteger32Prindi(esp)
	console_2.MPrindi(([]byte)("]"))

	userprockirje := thread.ProtsessorOlek.Ecx
	globaalneoffsetTabel_2 := thread.ProtsessorOlek.Edx
	dünaamiline := thread.ProtsessorOlek.Esi

	PortKirjutaminebyte(0x20, 0x20)
	jumpusermodeiret(eip, kasutajaesp, eflags, userprockirje, globaalneoffsetTabel_2, dünaamiline)
	console_2.MPrindi(([]byte)("usermode end"))
}
func prindiesp(esp uint32) {
	console_2.MPrindi(([]byte)("esp["))
	console_2.MUnsignedinteger32Prindi(esp)
}
