package scheduler

import . "unsafe"
import . "reflect"

import . "konsoli"
import . "gdt"
import . "portti"
import . "util/listaa"

import . "keskeytys"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "muistimanager"

const SchedulerToistumistiheys = 1
const KernelheapKäynnistä = 1024 * 1024
const schedulerVirheenpaikannus = false
const pitToistumistiheys = 100

var listaa Linkedlistaa

type Schedulerdata struct {
	toistumistiheys	uint32
	tickcount	uint32

	switchforced	bool

	Käytössä	bool

	nykyinenthread	*TThread
	tss		*Tsshakusana
}

var schedata Schedulerdata = Schedulerdata{}

func (itse *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.toistumistiheys = SchedulerToistumistiheys
	schedata.nykyinenthread = nil
	schedata.Käytössä = false
	schedata.switchforced = false

}

var konsoli_2 = TKonsoli{}
var nykyinenthreadHakemisto int = 0
var seuraavaProsessiTUNNISTE uint32 = 1

func Allocatepid() uint32 {
	pid := seuraavaProsessiTUNNISTE
	seuraavaProsessiTUNNISTE++
	return pid
}

func (itse *Schedulerdata) GetSeuraavaValmisthread() *TThread {
	if listaa.Koko_2 <= 0 {
		return nil
	}

	if schedata.nykyinenthread != nil {
		nykyinenthreadHakemisto = listaa.Hakemistoof(uintptr(Pointer(schedata.nykyinenthread)))
		if nykyinenthreadHakemisto < 0 {
			nykyinenthreadHakemisto = 0
		}
	} else {
		nykyinenthreadHakemisto = -1
	}

	for checked := 0; checked < listaa.Koko_2; checked++ {
		nykyinenthreadHakemisto++
		if nykyinenthreadHakemisto >= listaa.Koko_2 {
			nykyinenthreadHakemisto = 0
		}
		thread := (*TThread)(listaa.Getat(nykyinenthreadHakemisto))
		if thread != nil && thread.ThreadTila != Blocked && thread.ThreadTila != Pysäytetty {
			if schedulerVirheenpaikannus {
				konsoli_2.MTulosta("ti:")
				konsoli_2.MUnsignedinteger32Tulosta(uint32(nykyinenthreadHakemisto))
				konsoli_2.MTulosta(":")
				konsoli_2.MUnsignedinteger32Tulosta(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.nykyinenthread

}
func (itse *Scheduler) Lisääthread(thread *TThread) {
	if thread == nil {
		return
	}
	listaa.Lisää_listan_loppuun(uintptr(Pointer(thread)))
}
func Lisäärunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	listaa.Lisää_listan_loppuun(uintptr(Pointer(thread)))
}

func Nykyinenpid() uint32 {
	if schedata.nykyinenthread == nil || schedata.nykyinenthread.Pid == 0 {
		return 1
	}
	return schedata.nykyinenthread.Pid
}

func Nykyinenvanhempipid() uint32 {
	if schedata.nykyinenthread == nil {
		return 0
	}
	return schedata.nykyinenthread.Vanhempipid
}
func (itse *Scheduler) Poistathread(thread *TThread) {
	listaa.Poista_2(uintptr(Pointer(thread)))
}

func (itse *Scheduler) Poistathreadat(hakemisto int) {
	listaa.Poistaat(hakemisto)
}

type Scheduler struct {
	TKeskeytyshandler
}

func (itse *Scheduler) Init(manager *TKeskeytysmanager, mem *mem.TMuistimanager, tss *Tsshakusana) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitToistumistiheys)

	listaa = Linkedlistaa{}
	listaa.Init(mem)
	konsoli_2.MTulosta("list:")
	konsoli_2.MUnsignedinteger32Tulosta(uint32(uintptr(Pointer(&listaa))))

	keskeytyshandler = kahvaKeskeytys
	var address uintptr
	address = uintptr(Pointer(&keskeytyshandler))
	itse.TKeskeytyshandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (itse *Scheduler) Käytössä(käytössä bool) {
	schedata.Käytössä = käytössä
}

func initpit(toistumistiheys uint32) {
	if toistumistiheys == 0 {
		return
	}
	divisor := uint32(1193180) / toistumistiheys
	PorttiKirjoitusbyte(0x43, 0x36)
	PorttiKirjoitusbyte(0x40, uint8(divisor&0xFF))
	PorttiKirjoitusbyte(0x40, uint8((divisor>>8)&0xFF))
}

func asetads(dssegment uint32)
func asetags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func palautafpregs(buffer_2 uintptr)

var jmpKäyttäjä uint32 = 0
var keskeytyshandler func(uint32) uint32

func schedulestack(fn func())
func asetacr3(address uint32)
func getcr3() uint32

func kahvaKeskeytys(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerVirheenpaikannus {
		konsoli_2.MTulostaxy(([]byte)("sche1:"), 1, 17)

		konsoli_2.MTulosta(":")
		konsoli_2.MUnsignedinteger32Tulosta(esp)
		konsoli_2.MTulosta(":")

		konsoli_2.MUnsignedinteger32Tulosta(uint32(schedata.tickcount))
		konsoli_2.MTulosta(":")
		konsoli_2.MUnsignedinteger32Tulosta(KernelheapKäynnistä)
	}

	if schedata.tickcount == schedata.toistumistiheys {
		schedata.tickcount = 0

		if listaa.Koko_2 > 0 && schedata.Käytössä == true {
			var seuraavathread = schedata.GetSeuraavaValmisthread()
			if seuraavathread == nil {
				return esp
			}
			if schedata.nykyinenthread == nil {
				MEmergencyKäytälokiaMerkkijono("\nSCHED first esp=")
				MEmergencyKäytälokiaunsignedinteger32(esp)
				MEmergencyKäytälokiaMerkkijono(" thread=")
				MEmergencyKäytälokiaunsignedinteger32(uint32(uintptr(Pointer(seuraavathread))))
				MEmergencyKäytälokiaMerkkijono(" cpu=")
				MEmergencyKäytälokiaunsignedinteger32(uint32(uintptr(Pointer(seuraavathread.CpuTila))))
				MEmergencyKäytälokiaMerkkijono(" state=")
				MEmergencyKäytälokiaunsignedinteger32(uint32(seuraavathread.ThreadTila))
				MEmergencyKäytälokiaMerkkijono(" eip=")
				MEmergencyKäytälokiaunsignedinteger32(seuraavathread.CpuTila.Eip)
				MEmergencyKäytälokiaMerkkijono(" cs=")
				MEmergencyKäytälokiaunsignedinteger32(seuraavathread.CpuTila.Cs)
				MEmergencyKäytälokiaMerkkijono("\n")
			}

			if esp >= KernelheapKäynnistä && schedata.nykyinenthread != nil {
				schedata.nykyinenthread.CpuTila = (*TcpuTila)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.nykyinenthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.nykyinenthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerVirheenpaikannus {
					konsoli_2.MTulosta(([]byte)("backup"))
					konsoli_2.MUnsignedinteger32Tulosta(esp)
				}
			}

			address := uintptr(Pointer(&(seuraavathread.Fpubuffer)))
			offset := seuraavathread.Fpuoffset
			if offset != 0xffffffff {
				palautafpregs(address + offset)
				if schedulerVirheenpaikannus {
					konsoli_2.MTulosta(([]byte)("restore"))
				}
			}

			schedata.nykyinenthread = seuraavathread

			if schedata.nykyinenthread.ThreadTila == Aloitettu {
				schedata.nykyinenthread.ThreadTila = Valmis

				InitialthreadKäyttäjäjump(schedata.nykyinenthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(seuraavathread.CpuTila)))
			if seuraavathread.Stack != 0 {
				schedata.tss.Asetastack(Segkerneldata, seuraavathread.Stack+ThreadstackKoko)
			}

			asetacr3(seuraavathread.SivuKansiohakusana)
			asetags(seuraavathread.CpuTila.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func PoistakäytöstäKokonaisluku()

func getesp() uint32
func threadSuljeloop()

func asetathreadSuljeloopTila(cpuTila *TcpuTila) {
	cpuTila.Eip = uint32(ValueOf(threadSuljeloop).Pointer())
	cpuTila.Cs = Segkernelcode
	cpuTila.Ds = Segkerneldata
	cpuTila.Es = Segkerneldata
	cpuTila.Fs = Segkerneldata
	cpuTila.Gs = Segkernelgs
	cpuTila.Ss = Segkerneldata
	cpuTila.Eflags = 0x202
}

func PysäytäNykyinenthread(cpuTila *TcpuTila) *TcpuTila {
	if schedata.nykyinenthread == nil {
		asetathreadSuljeloopTila(cpuTila)
		return cpuTila
	}

	pysäytettythread := schedata.nykyinenthread
	for i := 0; i < listaa.Koko_2; i++ {
		thread := (*TThread)(listaa.Getat(i))
		if thread != nil && thread.CpuTila == cpuTila {
			pysäytettythread = thread
			break
		}
	}
	pysäytettythread.CpuTila = cpuTila
	pysäytettythread.ThreadTila = Pysäytetty
	schedata.nykyinenthread = pysäytettythread

	seuraavathread := schedata.GetSeuraavaValmisthread()
	if seuraavathread == nil || seuraavathread == pysäytettythread || seuraavathread.CpuTila == nil || seuraavathread.CpuTila == cpuTila {
		asetathreadSuljeloopTila(cpuTila)
		return cpuTila
	}

	schedata.nykyinenthread = seuraavathread
	if seuraavathread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Asetastack(Segkerneldata, seuraavathread.Stack+ThreadstackKoko)
	}
	asetacr3(seuraavathread.SivuKansiohakusana)
	asetags(seuraavathread.CpuTila.Gs)
	return seuraavathread.CpuTila
}

func InitialthreadKäyttäjäjump(thread *TThread) {

	PoistakäytöstäKokonaisluku()

	schedata.tss.Asetastack(Segkerneldata, thread.Stack+ThreadstackKoko)

	asetacr3(thread.SivuKansiohakusana)
	asetags(thread.CpuTila.Gs)

	schedata.nykyinenthread = thread
	schedata.Käytössä = true

	eip := thread.CpuTila.Eip
	käyttäjäesp := thread.Käyttäjästack_2 + thread.KäyttäjästackKoko_2
	eflags := thread.CpuTila.Eflags
	cs := thread.CpuTila.Cs
	esp := schedata.tss.Getesp0()

	konsoli_2.MTulosta(([]byte)("jump["))
	konsoli_2.MUnsignedinteger32Tulosta(eip)
	konsoli_2.MTulosta(([]byte)(":"))
	konsoli_2.MUnsignedinteger32Tulosta(käyttäjäesp)
	konsoli_2.MTulosta(([]byte)(":"))
	konsoli_2.MUnsignedinteger32Tulosta(eflags)
	konsoli_2.MTulosta(([]byte)(":"))
	konsoli_2.MUnsignedinteger32Tulosta(cs)
	konsoli_2.MTulosta(([]byte)(":"))

	konsoli_2.MUnsignedinteger32Tulosta(esp)
	konsoli_2.MTulosta(([]byte)("]"))

	userprochakusana := thread.CpuTila.Ecx
	globaalissaoffsetTaulukko_2 := thread.CpuTila.Edx
	dynaaminen := thread.CpuTila.Esi

	PorttiKirjoitusbyte(0x20, 0x20)
	jumpusermodeiret(eip, käyttäjäesp, eflags, userprochakusana, globaalissaoffsetTaulukko_2, dynaaminen)
	konsoli_2.MTulosta(([]byte)("usermode end"))
}
func tulostaesp(esp uint32) {
	konsoli_2.MTulosta(([]byte)("esp["))
	konsoli_2.MUnsignedinteger32Tulosta(esp)
}
