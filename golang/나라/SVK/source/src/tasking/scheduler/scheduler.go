/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "konzola"
import . "gdt"
import . "port"
import . "util/zoznam"

import . "prerušenie"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "pamäťmanager"

const SchedulerOpakovať = 1
const KernelheapSpustiť = 1024 * 1024
const schedulerLadenie = false
const pitOpakovať = 100

var zoznam LinkedZoznam

type Schedulerdata struct {
	opakovať	uint32
	tickcount	uint32

	switchforced	bool

	Zapnuté	bool

	aktuálnythread	*TThread
	tss		*Tsspoložka
}

var schedata Schedulerdata = Schedulerdata{}

func (vlastný *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.opakovať = SchedulerOpakovať
	schedata.aktuálnythread = nil
	schedata.Zapnuté = false
	schedata.switchforced = false

}

var konzola_2 = TKonzola{}
var aktuálnythreadindex int = 0
var nasledujúciProcesIdentifikátor uint32 = 1

func Allocatepid() uint32 {
	pid := nasledujúciProcesIdentifikátor
	nasledujúciProcesIdentifikátor++
	return pid
}

func (vlastný *Schedulerdata) GetNasledujúciPripravenýthread() *TThread {
	if zoznam.Veľkosť_2 <= 0 {
		return nil
	}

	if schedata.aktuálnythread != nil {
		aktuálnythreadindex = zoznam.Indexz(uintptr(Pointer(schedata.aktuálnythread)))
		if aktuálnythreadindex < 0 {
			aktuálnythreadindex = 0
		}
	} else {
		aktuálnythreadindex = -1
	}

	for checked := 0; checked < zoznam.Veľkosť_2; checked++ {
		aktuálnythreadindex++
		if aktuálnythreadindex >= zoznam.Veľkosť_2 {
			aktuálnythreadindex = 0
		}
		thread := (*TThread)(zoznam.Getat(aktuálnythreadindex))
		if thread != nil && thread.ThreadStav != Blocked && thread.ThreadStav != Zastavený {
			if schedulerLadenie {
				konzola_2.MTlačiť("ti:")
				konzola_2.MUnsignedinteger32Tlačiť(uint32(aktuálnythreadindex))
				konzola_2.MTlačiť(":")
				konzola_2.MUnsignedinteger32Tlačiť(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.aktuálnythread

}
func (vlastný *Scheduler) Pridaťthread(thread *TThread) {
	if thread == nil {
		return
	}
	zoznam.Append_to_list(uintptr(Pointer(thread)))
}
func Pridaťrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	zoznam.Append_to_list(uintptr(Pointer(thread)))
}

func Aktuálnypid() uint32 {
	if schedata.aktuálnythread == nil || schedata.aktuálnythread.Pid == 0 {
		return 1
	}
	return schedata.aktuálnythread.Pid
}

func Aktuálnyrodičpid() uint32 {
	if schedata.aktuálnythread == nil {
		return 0
	}
	return schedata.aktuálnythread.Rodičpid
}
func (vlastný *Scheduler) Odstrániťthread(thread *TThread) {
	zoznam.Odstrániť_2(uintptr(Pointer(thread)))
}

func (vlastný *Scheduler) Odstrániťthreadat(index int) {
	zoznam.Odstrániťat(index)
}

type Scheduler struct {
	TPrerušeniehandler
}

func (vlastný *Scheduler) Init(manager *TPrerušeniemanager, mem *mem.TPamäťmanager, tss *Tsspoložka) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitOpakovať)

	zoznam = LinkedZoznam{}
	zoznam.Init(mem)
	konzola_2.MTlačiť("list:")
	konzola_2.MUnsignedinteger32Tlačiť(uint32(uintptr(Pointer(&zoznam))))

	prerušeniehandler = uškoPrerušenie
	var address uintptr
	address = uintptr(Pointer(&prerušeniehandler))
	vlastný.TPrerušeniehandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (vlastný *Scheduler) Zapnuté(zapnuté bool) {
	schedata.Zapnuté = zapnuté
}

func initpit(opakovať uint32) {
	if opakovať == 0 {
		return
	}
	divisor := uint32(1193180) / opakovať
	PortZápisbyte(0x43, 0x36)
	PortZápisbyte(0x40, uint8(divisor&0xFF))
	PortZápisbyte(0x40, uint8((divisor>>8)&0xFF))
}

func sadads(dssegment uint32)
func sadags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func obnoviťfpregs(buffer_2 uintptr)

var jmpPoužívateľ uint32 = 0
var prerušeniehandler func(uint32) uint32

func schedulestack(fn func())
func sadacr3(address uint32)
func getcr3() uint32

func uškoPrerušenie(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerLadenie {
		konzola_2.MTlačiťxy(([]byte)("sche1:"), 1, 17)

		konzola_2.MTlačiť(":")
		konzola_2.MUnsignedinteger32Tlačiť(esp)
		konzola_2.MTlačiť(":")

		konzola_2.MUnsignedinteger32Tlačiť(uint32(schedata.tickcount))
		konzola_2.MTlačiť(":")
		konzola_2.MUnsignedinteger32Tlačiť(KernelheapSpustiť)
	}

	if schedata.tickcount == schedata.opakovať {
		schedata.tickcount = 0

		if zoznam.Veľkosť_2 > 0 && schedata.Zapnuté == true {
			var nasledujúcithread = schedata.GetNasledujúciPripravenýthread()
			if nasledujúcithread == nil {
				return esp
			}
			if schedata.aktuálnythread == nil {
				MEmergencyZaznamenávaniereťazec("\nSCHED first esp=")
				MEmergencyZaznamenávanieunsignedinteger32(esp)
				MEmergencyZaznamenávaniereťazec(" thread=")
				MEmergencyZaznamenávanieunsignedinteger32(uint32(uintptr(Pointer(nasledujúcithread))))
				MEmergencyZaznamenávaniereťazec(" cpu=")
				MEmergencyZaznamenávanieunsignedinteger32(uint32(uintptr(Pointer(nasledujúcithread.ProcesorStav))))
				MEmergencyZaznamenávaniereťazec(" state=")
				MEmergencyZaznamenávanieunsignedinteger32(uint32(nasledujúcithread.ThreadStav))
				MEmergencyZaznamenávaniereťazec(" eip=")
				MEmergencyZaznamenávanieunsignedinteger32(nasledujúcithread.ProcesorStav.Eip)
				MEmergencyZaznamenávaniereťazec(" cs=")
				MEmergencyZaznamenávanieunsignedinteger32(nasledujúcithread.ProcesorStav.Cs)
				MEmergencyZaznamenávaniereťazec("\n")
			}

			if esp >= KernelheapSpustiť && schedata.aktuálnythread != nil {
				schedata.aktuálnythread.ProcesorStav = (*TcpuStav)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.aktuálnythread.Fpubuffer)))
				posunutie := (16 - (address % 16)) & 0xF
				schedata.aktuálnythread.FpuPosunutie = posunutie
				backupfpregs(address + posunutie)
				if schedulerLadenie {
					konzola_2.MTlačiť(([]byte)("backup"))
					konzola_2.MUnsignedinteger32Tlačiť(esp)
				}
			}

			address := uintptr(Pointer(&(nasledujúcithread.Fpubuffer)))
			posunutie := nasledujúcithread.FpuPosunutie
			if posunutie != 0xffffffff {
				obnoviťfpregs(address + posunutie)
				if schedulerLadenie {
					konzola_2.MTlačiť(([]byte)("restore"))
				}
			}

			schedata.aktuálnythread = nasledujúcithread

			if schedata.aktuálnythread.ThreadStav == Začaté {
				schedata.aktuálnythread.ThreadStav = Pripravený

				InitialthreadPoužívateľjump(schedata.aktuálnythread)
				return esp
			}

			esp = uint32(uintptr(Pointer(nasledujúcithread.ProcesorStav)))
			if nasledujúcithread.Stack != 0 {
				schedata.tss.Sadastack(Segkerneldata, nasledujúcithread.Stack+ThreadstackVeľkosť)
			}

			sadacr3(nasledujúcithread.STRANAAdresárpoložka)
			sadags(nasledujúcithread.ProcesorStav.Gs)

		}

	}

	return esp
}

func jumpPoužívateľskýrežimiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Zakázaťint()

func getesp() uint32
func threadKoniecloop()

func sadathreadKoniecloopStav(procesorStav *TcpuStav) {
	procesorStav.Eip = uint32(ValueOf(threadKoniecloop).Pointer())
	procesorStav.Cs = Segkernelcode
	procesorStav.Ds = Segkerneldata
	procesorStav.Es = Segkerneldata
	procesorStav.Fs = Segkerneldata
	procesorStav.Gs = Segkernelgs
	procesorStav.Ss = Segkerneldata
	procesorStav.Eflags = 0x202
}

func ZastaviťAktuálnythread(procesorStav *TcpuStav) *TcpuStav {
	if schedata.aktuálnythread == nil {
		sadathreadKoniecloopStav(procesorStav)
		return procesorStav
	}

	zastavenýthread := schedata.aktuálnythread
	for i := 0; i < zoznam.Veľkosť_2; i++ {
		thread := (*TThread)(zoznam.Getat(i))
		if thread != nil && thread.ProcesorStav == procesorStav {
			zastavenýthread = thread
			break
		}
	}
	zastavenýthread.ProcesorStav = procesorStav
	zastavenýthread.ThreadStav = Zastavený
	schedata.aktuálnythread = zastavenýthread

	nasledujúcithread := schedata.GetNasledujúciPripravenýthread()
	if nasledujúcithread == nil || nasledujúcithread == zastavenýthread || nasledujúcithread.ProcesorStav == nil || nasledujúcithread.ProcesorStav == procesorStav {
		sadathreadKoniecloopStav(procesorStav)
		return procesorStav
	}

	schedata.aktuálnythread = nasledujúcithread
	if nasledujúcithread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Sadastack(Segkerneldata, nasledujúcithread.Stack+ThreadstackVeľkosť)
	}
	sadacr3(nasledujúcithread.STRANAAdresárpoložka)
	sadags(nasledujúcithread.ProcesorStav.Gs)
	return nasledujúcithread.ProcesorStav
}

func InitialthreadPoužívateľjump(thread *TThread) {

	Zakázaťint()

	schedata.tss.Sadastack(Segkerneldata, thread.Stack+ThreadstackVeľkosť)

	sadacr3(thread.STRANAAdresárpoložka)
	sadags(thread.ProcesorStav.Gs)

	schedata.aktuálnythread = thread
	schedata.Zapnuté = true

	eip := thread.ProcesorStav.Eip
	používateľesp := thread.Používateľstack_2 + thread.PoužívateľstackVeľkosť_2
	eflags := thread.ProcesorStav.Eflags
	cs := thread.ProcesorStav.Cs
	esp := schedata.tss.Getesp0()

	konzola_2.MTlačiť(([]byte)("jump["))
	konzola_2.MUnsignedinteger32Tlačiť(eip)
	konzola_2.MTlačiť(([]byte)(":"))
	konzola_2.MUnsignedinteger32Tlačiť(používateľesp)
	konzola_2.MTlačiť(([]byte)(":"))
	konzola_2.MUnsignedinteger32Tlačiť(eflags)
	konzola_2.MTlačiť(([]byte)(":"))
	konzola_2.MUnsignedinteger32Tlačiť(cs)
	konzola_2.MTlačiť(([]byte)(":"))

	konzola_2.MUnsignedinteger32Tlačiť(esp)
	konzola_2.MTlačiť(([]byte)("]"))

	userprocpoložka := thread.ProcesorStav.Ecx
	globálnyPosunutieTabuľka_2 := thread.ProcesorStav.Edx
	dynamická := thread.ProcesorStav.Esi

	PortZápisbyte(0x20, 0x20)
	jumpPoužívateľskýrežimiret(eip, používateľesp, eflags, userprocpoložka, globálnyPosunutieTabuľka_2, dynamická)
	konzola_2.MTlačiť(([]byte)("usermode end"))
}
func tlačiťesp(esp uint32) {
	konzola_2.MTlačiť(([]byte)("esp["))
	konzola_2.MUnsignedinteger32Tlačiť(esp)
}
