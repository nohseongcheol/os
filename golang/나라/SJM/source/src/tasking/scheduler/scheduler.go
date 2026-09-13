package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/liste"

import . "avbrudd"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "minnemanager"

const SchedulerFrekvens = 1
const Kernelheapstart = 1024 * 1024
const schedulerFeilsøk = false
const pitFrekvens = 100

var liste LinkedListe

type Schedulerdata struct {
	frekvens	uint32
	tickAntall	uint32

	switchforced	bool

	Aktivert	bool

	gjeldendethread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (selv *Schedulerdata) Init() {
	schedata.tickAntall = 0
	schedata.frekvens = SchedulerFrekvens
	schedata.gjeldendethread = nil
	schedata.Aktivert = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var gjeldendethreadIndeks int = 0
var nesteProsessid uint32 = 1

func Allocatepid() uint32 {
	pid := nesteProsessid
	nesteProsessid++
	return pid
}

func (selv *Schedulerdata) GetNesteKlarthread() *TThread {
	if liste.Størrelse_2 <= 0 {
		return nil
	}

	if schedata.gjeldendethread != nil {
		gjeldendethreadIndeks = liste.Indeksav(uintptr(Pointer(schedata.gjeldendethread)))
		if gjeldendethreadIndeks < 0 {
			gjeldendethreadIndeks = 0
		}
	} else {
		gjeldendethreadIndeks = -1
	}

	for checked := 0; checked < liste.Størrelse_2; checked++ {
		gjeldendethreadIndeks++
		if gjeldendethreadIndeks >= liste.Størrelse_2 {
			gjeldendethreadIndeks = 0
		}
		thread := (*TThread)(liste.Getat(gjeldendethreadIndeks))
		if thread != nil && thread.ThreadStatus != Blocked && thread.ThreadStatus != Stoppet {
			if schedulerFeilsøk {
				console_2.MSkrivut("ti:")
				console_2.MUnsignedinteger32Skrivut(uint32(gjeldendethreadIndeks))
				console_2.MSkrivut(":")
				console_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.gjeldendethread

}
func (selv *Scheduler) Leggtilthread(thread *TThread) {
	if thread == nil {
		return
	}
	liste.Append_to_list(uintptr(Pointer(thread)))
}
func Leggtilrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	liste.Append_to_list(uintptr(Pointer(thread)))
}

func Gjeldendepid() uint32 {
	if schedata.gjeldendethread == nil || schedata.gjeldendethread.Pid == 0 {
		return 1
	}
	return schedata.gjeldendethread.Pid
}

func Gjeldendeopphavpid() uint32 {
	if schedata.gjeldendethread == nil {
		return 0
	}
	return schedata.gjeldendethread.Opphavpid
}
func (selv *Scheduler) Fjernthread(thread *TThread) {
	liste.Fjern(uintptr(Pointer(thread)))
}

func (selv *Scheduler) Fjernthreadat(indeks int) {
	liste.Fjernat(indeks)
}

type Scheduler struct {
	TAvbruddhandler
}

func (selv *Scheduler) Init(manager *TAvbruddmanager, mem *mem.TMinnemanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitFrekvens)

	liste = LinkedListe{}
	liste.Init(mem)
	console_2.MSkrivut("list:")
	console_2.MUnsignedinteger32Skrivut(uint32(uintptr(Pointer(&liste))))

	avbruddhandler = håndtakAvbrudd
	var address uintptr
	address = uintptr(Pointer(&avbruddhandler))
	selv.TAvbruddhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (selv *Scheduler) Aktivert(aktivert bool) {
	schedata.Aktivert = aktivert
}

func initpit(frekvens uint32) {
	if frekvens == 0 {
		return
	}
	divisor := uint32(1193180) / frekvens
	PortSkrivbyte(0x43, 0x36)
	PortSkrivbyte(0x40, uint8(divisor&0xFF))
	PortSkrivbyte(0x40, uint8((divisor>>8)&0xFF))
}

func settds(dssegment uint32)
func settgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func gjenopprettfpregs(buffer_2 uintptr)

var jmpBruker uint32 = 0
var avbruddhandler func(uint32) uint32

func schedulestack(fn func())
func settcr3(address uint32)
func getcr3() uint32

func håndtakAvbrudd(esp uint32) uint32 {

	schedata.tickAntall++

	if schedulerFeilsøk {
		console_2.MSkrivutxy(([]byte)("sche1:"), 1, 17)

		console_2.MSkrivut(":")
		console_2.MUnsignedinteger32Skrivut(esp)
		console_2.MSkrivut(":")

		console_2.MUnsignedinteger32Skrivut(uint32(schedata.tickAntall))
		console_2.MSkrivut(":")
		console_2.MUnsignedinteger32Skrivut(Kernelheapstart)
	}

	if schedata.tickAntall == schedata.frekvens {
		schedata.tickAntall = 0

		if liste.Størrelse_2 > 0 && schedata.Aktivert == true {
			var nestethread = schedata.GetNesteKlarthread()
			if nestethread == nil {
				return esp
			}
			if schedata.gjeldendethread == nil {
				MEmergencyLoggStreng("\nSCHED first esp=")
				MEmergencyLoggunsignedinteger32(esp)
				MEmergencyLoggStreng(" thread=")
				MEmergencyLoggunsignedinteger32(uint32(uintptr(Pointer(nestethread))))
				MEmergencyLoggStreng(" cpu=")
				MEmergencyLoggunsignedinteger32(uint32(uintptr(Pointer(nestethread.CpuStatus))))
				MEmergencyLoggStreng(" state=")
				MEmergencyLoggunsignedinteger32(uint32(nestethread.ThreadStatus))
				MEmergencyLoggStreng(" eip=")
				MEmergencyLoggunsignedinteger32(nestethread.CpuStatus.Eip)
				MEmergencyLoggStreng(" cs=")
				MEmergencyLoggunsignedinteger32(nestethread.CpuStatus.Cs)
				MEmergencyLoggStreng("\n")
			}

			if esp >= Kernelheapstart && schedata.gjeldendethread != nil {
				schedata.gjeldendethread.CpuStatus = (*TcpuStatus)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.gjeldendethread.Fpubuffer)))
				avstand := (16 - (address % 16)) & 0xF
				schedata.gjeldendethread.FpuAvstand = avstand
				backupfpregs(address + avstand)
				if schedulerFeilsøk {
					console_2.MSkrivut(([]byte)("backup"))
					console_2.MUnsignedinteger32Skrivut(esp)
				}
			}

			address := uintptr(Pointer(&(nestethread.Fpubuffer)))
			avstand := nestethread.FpuAvstand
			if avstand != 0xffffffff {
				gjenopprettfpregs(address + avstand)
				if schedulerFeilsøk {
					console_2.MSkrivut(([]byte)("restore"))
				}
			}

			schedata.gjeldendethread = nestethread

			if schedata.gjeldendethread.ThreadStatus == Startet {
				schedata.gjeldendethread.ThreadStatus = Klar

				InitialthreadBrukerjump(schedata.gjeldendethread)
				return esp
			}

			esp = uint32(uintptr(Pointer(nestethread.CpuStatus)))
			if nestethread.Stack != 0 {
				schedata.tss.Settstack(Segkerneldata, nestethread.Stack+ThreadstackStørrelse)
			}

			settcr3(nestethread.SideKatalogentry)
			settgs(nestethread.CpuStatus.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Slåavint()

func getesp() uint32
func threadAvsluttLøkke()

func settthreadAvsluttLøkkeStatus(cpuStatus *TcpuStatus) {
	cpuStatus.Eip = uint32(ValueOf(threadAvsluttLøkke).Pointer())
	cpuStatus.Cs = Segkernelcode
	cpuStatus.Ds = Segkerneldata
	cpuStatus.Es = Segkerneldata
	cpuStatus.Fs = Segkerneldata
	cpuStatus.Gs = Segkernelgs
	cpuStatus.Ss = Segkerneldata
	cpuStatus.Eflags = 0x202
}

func StoppGjeldendethread(cpuStatus *TcpuStatus) *TcpuStatus {
	if schedata.gjeldendethread == nil {
		settthreadAvsluttLøkkeStatus(cpuStatus)
		return cpuStatus
	}

	stoppetthread := schedata.gjeldendethread
	for i := 0; i < liste.Størrelse_2; i++ {
		thread := (*TThread)(liste.Getat(i))
		if thread != nil && thread.CpuStatus == cpuStatus {
			stoppetthread = thread
			break
		}
	}
	stoppetthread.CpuStatus = cpuStatus
	stoppetthread.ThreadStatus = Stoppet
	schedata.gjeldendethread = stoppetthread

	nestethread := schedata.GetNesteKlarthread()
	if nestethread == nil || nestethread == stoppetthread || nestethread.CpuStatus == nil || nestethread.CpuStatus == cpuStatus {
		settthreadAvsluttLøkkeStatus(cpuStatus)
		return cpuStatus
	}

	schedata.gjeldendethread = nestethread
	if nestethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Settstack(Segkerneldata, nestethread.Stack+ThreadstackStørrelse)
	}
	settcr3(nestethread.SideKatalogentry)
	settgs(nestethread.CpuStatus.Gs)
	return nestethread.CpuStatus
}

func InitialthreadBrukerjump(thread *TThread) {

	Slåavint()

	schedata.tss.Settstack(Segkerneldata, thread.Stack+ThreadstackStørrelse)

	settcr3(thread.SideKatalogentry)
	settgs(thread.CpuStatus.Gs)

	schedata.gjeldendethread = thread
	schedata.Aktivert = true

	eip := thread.CpuStatus.Eip
	brukeresp := thread.Brukerstack_2 + thread.BrukerstackStørrelse_2
	eflags := thread.CpuStatus.Eflags
	cs := thread.CpuStatus.Cs
	esp := schedata.tss.Getesp0()

	console_2.MSkrivut(([]byte)("jump["))
	console_2.MUnsignedinteger32Skrivut(eip)
	console_2.MSkrivut(([]byte)(":"))
	console_2.MUnsignedinteger32Skrivut(brukeresp)
	console_2.MSkrivut(([]byte)(":"))
	console_2.MUnsignedinteger32Skrivut(eflags)
	console_2.MSkrivut(([]byte)(":"))
	console_2.MUnsignedinteger32Skrivut(cs)
	console_2.MSkrivut(([]byte)(":"))

	console_2.MUnsignedinteger32Skrivut(esp)
	console_2.MSkrivut(([]byte)("]"))

	userprocentry := thread.CpuStatus.Ecx
	globalAvstandTabell_2 := thread.CpuStatus.Edx
	dynamisk := thread.CpuStatus.Esi

	PortSkrivbyte(0x20, 0x20)
	jumpusermodeiret(eip, brukeresp, eflags, userprocentry, globalAvstandTabell_2, dynamisk)
	console_2.MSkrivut(([]byte)("usermode end"))
}
func skrivutesp(esp uint32) {
	console_2.MSkrivut(([]byte)("esp["))
	console_2.MUnsignedinteger32Skrivut(esp)
}
