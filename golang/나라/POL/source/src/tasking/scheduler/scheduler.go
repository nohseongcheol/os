/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "konsola"
import . "gdt"
import . "port"
import . "util/lista"

import . "przerwanie"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "pamięćmanager"

const Schedulerfrequency = 1
const KernelheapUruchom = 1024 * 1024
const schedulerDiagnozuj = false
const pitfrequency = 100

var lista LinkedLista

type Schedulerdata struct {
	frequency	uint32
	tickLiczba	uint32

	switchforced	bool

	Włączone	bool

	bieżącythread	*TThread
	tss		*Tsswpis
}

var schedata Schedulerdata = Schedulerdata{}

func (bieżący *Schedulerdata) Init() {
	schedata.tickLiczba = 0
	schedata.frequency = Schedulerfrequency
	schedata.bieżącythread = nil
	schedata.Włączone = false
	schedata.switchforced = false

}

var konsola_2 = TKonsola{}
var bieżącythreadIndeks int = 0
var następnyProcesIdentyfikator uint32 = 1

func AllocateIdentyfikator() uint32 {
	identyfikator_2 := następnyProcesIdentyfikator
	następnyProcesIdentyfikator++
	return identyfikator_2
}

func (bieżący *Schedulerdata) GetNastępnyGotowythread() *TThread {
	if lista.Rozmiar_2 <= 0 {
		return nil
	}

	if schedata.bieżącythread != nil {
		bieżącythreadIndeks = lista.Indeksz(uintptr(Pointer(schedata.bieżącythread)))
		if bieżącythreadIndeks < 0 {
			bieżącythreadIndeks = 0
		}
	} else {
		bieżącythreadIndeks = -1
	}

	for checked := 0; checked < lista.Rozmiar_2; checked++ {
		bieżącythreadIndeks++
		if bieżącythreadIndeks >= lista.Rozmiar_2 {
			bieżącythreadIndeks = 0
		}
		thread := (*TThread)(lista.Getat(bieżącythreadIndeks))
		if thread != nil && thread.ThreadStan != Blocked && thread.ThreadStan != Zatrzymany {
			if schedulerDiagnozuj {
				konsola_2.MWydrukuj("ti:")
				konsola_2.MUnsignedinteger32Wydrukuj(uint32(bieżącythreadIndeks))
				konsola_2.MWydrukuj(":")
				konsola_2.MUnsignedinteger32Wydrukuj(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.bieżącythread

}
func (bieżący *Scheduler) Dodajthread(thread *TThread) {
	if thread == nil {
		return
	}
	lista.Dodaj_na_końcu_listy(uintptr(Pointer(thread)))
}
func Dodajrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	lista.Dodaj_na_końcu_listy(uintptr(Pointer(thread)))
}

func BieżącyIdentyfikator() uint32 {
	if schedata.bieżącythread == nil || schedata.bieżącythread.Identyfikator == 0 {
		return 1
	}
	return schedata.bieżącythread.Identyfikator
}

func BieżącyrodzicIdentyfikator() uint32 {
	if schedata.bieżącythread == nil {
		return 0
	}
	return schedata.bieżącythread.RodzicIdentyfikator
}
func (bieżący *Scheduler) Usuńthread(thread *TThread) {
	lista.Usuń_2(uintptr(Pointer(thread)))
}

func (bieżący *Scheduler) Usuńthreadat(indeks int) {
	lista.Usuńat(indeks)
}

type Scheduler struct {
	TPrzerwaniehandler
}

func (bieżący *Scheduler) Init(manager *TPrzerwaniemanager, mem *mem.TPamięćmanager, tss *Tsswpis) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	lista = LinkedLista{}
	lista.Init(mem)
	konsola_2.MWydrukuj("list:")
	konsola_2.MUnsignedinteger32Wydrukuj(uint32(uintptr(Pointer(&lista))))

	przerwaniehandler = uchwytPrzerwanie
	var adres uintptr
	adres = uintptr(Pointer(&przerwaniehandler))
	bieżący.TPrzerwaniehandler.Init(0x20, uintptr(Pointer(manager)), adres)
}

func (bieżący *Scheduler) Włączone(włączone bool) {
	schedata.Włączone = włączone
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	PortZapisbyte(0x43, 0x36)
	PortZapisbyte(0x40, uint8(divisor&0xFF))
	PortZapisbyte(0x40, uint8((divisor>>8)&0xFF))
}

func zbiórds(dssegment uint32)
func zbiórgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func przywróćfpregs(buffer_2 uintptr)

var jmpUżytkownik uint32 = 0
var przerwaniehandler func(uint32) uint32

func schedulestack(fn func())
func zbiórcr3(adres uint32)
func getcr3() uint32

func uchwytPrzerwanie(esp uint32) uint32 {

	schedata.tickLiczba++

	if schedulerDiagnozuj {
		konsola_2.MWydrukujxy(([]byte)("sche1:"), 1, 17)

		konsola_2.MWydrukuj(":")
		konsola_2.MUnsignedinteger32Wydrukuj(esp)
		konsola_2.MWydrukuj(":")

		konsola_2.MUnsignedinteger32Wydrukuj(uint32(schedata.tickLiczba))
		konsola_2.MWydrukuj(":")
		konsola_2.MUnsignedinteger32Wydrukuj(KernelheapUruchom)
	}

	if schedata.tickLiczba == schedata.frequency {
		schedata.tickLiczba = 0

		if lista.Rozmiar_2 > 0 && schedata.Włączone == true {
			var następnythread = schedata.GetNastępnyGotowythread()
			if następnythread == nil {
				return esp
			}
			if schedata.bieżącythread == nil {
				MEmergencyDziennikCIĄG("\nSCHED first esp=")
				MEmergencyDziennikunsignedinteger32(esp)
				MEmergencyDziennikCIĄG(" thread=")
				MEmergencyDziennikunsignedinteger32(uint32(uintptr(Pointer(następnythread))))
				MEmergencyDziennikCIĄG(" cpu=")
				MEmergencyDziennikunsignedinteger32(uint32(uintptr(Pointer(następnythread.ProcesorStan))))
				MEmergencyDziennikCIĄG(" state=")
				MEmergencyDziennikunsignedinteger32(uint32(następnythread.ThreadStan))
				MEmergencyDziennikCIĄG(" eip=")
				MEmergencyDziennikunsignedinteger32(następnythread.ProcesorStan.Eip)
				MEmergencyDziennikCIĄG(" cs=")
				MEmergencyDziennikunsignedinteger32(następnythread.ProcesorStan.Cs)
				MEmergencyDziennikCIĄG("\n")
			}

			if esp >= KernelheapUruchom && schedata.bieżącythread != nil {
				schedata.bieżącythread.ProcesorStan = (*TcpuStan)(Pointer(uintptr(esp)))

				adres := uintptr(Pointer(&(schedata.bieżącythread.Fpubuffer)))
				przesunięcie := (16 - (adres % 16)) & 0xF
				schedata.bieżącythread.FpuPrzesunięcie = przesunięcie
				backupfpregs(adres + przesunięcie)
				if schedulerDiagnozuj {
					konsola_2.MWydrukuj(([]byte)("backup"))
					konsola_2.MUnsignedinteger32Wydrukuj(esp)
				}
			}

			adres := uintptr(Pointer(&(następnythread.Fpubuffer)))
			przesunięcie := następnythread.FpuPrzesunięcie
			if przesunięcie != 0xffffffff {
				przywróćfpregs(adres + przesunięcie)
				if schedulerDiagnozuj {
					konsola_2.MWydrukuj(([]byte)("restore"))
				}
			}

			schedata.bieżącythread = następnythread

			if schedata.bieżącythread.ThreadStan == Uruchomiono {
				schedata.bieżącythread.ThreadStan = Gotowy

				InitialthreadUżytkownikjump(schedata.bieżącythread)
				return esp
			}

			esp = uint32(uintptr(Pointer(następnythread.ProcesorStan)))
			if następnythread.Stack != 0 {
				schedata.tss.Zbiórstack(Segkerneldata, następnythread.Stack+ThreadstackRozmiar)
			}

			zbiórcr3(następnythread.StronaKatalogwpis)
			zbiórgs(następnythread.ProcesorStan.Gs)

		}

	}

	return esp
}

func jumpTrybużytkownikairet(uint32, uint32, uint32, uint32, uint32, uint32)
func WyłączCałkowity()

func getesp() uint32
func threadZakończloop()

func zbiórthreadZakończloopStan(procesorStan *TcpuStan) {
	procesorStan.Eip = uint32(ValueOf(threadZakończloop).Pointer())
	procesorStan.Cs = Segkernelcode
	procesorStan.Ds = Segkerneldata
	procesorStan.Es = Segkerneldata
	procesorStan.Fs = Segkerneldata
	procesorStan.Gs = Segkernelgs
	procesorStan.Ss = Segkerneldata
	procesorStan.Eflags = 0x202
}

func ZatrzymajBieżącythread(procesorStan *TcpuStan) *TcpuStan {
	if schedata.bieżącythread == nil {
		zbiórthreadZakończloopStan(procesorStan)
		return procesorStan
	}

	zatrzymanythread := schedata.bieżącythread
	for i := 0; i < lista.Rozmiar_2; i++ {
		thread := (*TThread)(lista.Getat(i))
		if thread != nil && thread.ProcesorStan == procesorStan {
			zatrzymanythread = thread
			break
		}
	}
	zatrzymanythread.ProcesorStan = procesorStan
	zatrzymanythread.ThreadStan = Zatrzymany
	schedata.bieżącythread = zatrzymanythread

	następnythread := schedata.GetNastępnyGotowythread()
	if następnythread == nil || następnythread == zatrzymanythread || następnythread.ProcesorStan == nil || następnythread.ProcesorStan == procesorStan {
		zbiórthreadZakończloopStan(procesorStan)
		return procesorStan
	}

	schedata.bieżącythread = następnythread
	if następnythread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Zbiórstack(Segkerneldata, następnythread.Stack+ThreadstackRozmiar)
	}
	zbiórcr3(następnythread.StronaKatalogwpis)
	zbiórgs(następnythread.ProcesorStan.Gs)
	return następnythread.ProcesorStan
}

func InitialthreadUżytkownikjump(thread *TThread) {

	WyłączCałkowity()

	schedata.tss.Zbiórstack(Segkerneldata, thread.Stack+ThreadstackRozmiar)

	zbiórcr3(thread.StronaKatalogwpis)
	zbiórgs(thread.ProcesorStan.Gs)

	schedata.bieżącythread = thread
	schedata.Włączone = true

	eip := thread.ProcesorStan.Eip
	użytkownikesp := thread.Użytkownikstack_2 + thread.UżytkownikstackRozmiar_2
	eflags := thread.ProcesorStan.Eflags
	cs := thread.ProcesorStan.Cs
	esp := schedata.tss.Getesp0()

	konsola_2.MWydrukuj(([]byte)("jump["))
	konsola_2.MUnsignedinteger32Wydrukuj(eip)
	konsola_2.MWydrukuj(([]byte)(":"))
	konsola_2.MUnsignedinteger32Wydrukuj(użytkownikesp)
	konsola_2.MWydrukuj(([]byte)(":"))
	konsola_2.MUnsignedinteger32Wydrukuj(eflags)
	konsola_2.MWydrukuj(([]byte)(":"))
	konsola_2.MUnsignedinteger32Wydrukuj(cs)
	konsola_2.MWydrukuj(([]byte)(":"))

	konsola_2.MUnsignedinteger32Wydrukuj(esp)
	konsola_2.MWydrukuj(([]byte)("]"))

	userprocwpis := thread.ProcesorStan.Ecx
	globalnyPrzesunięcieTabela_2 := thread.ProcesorStan.Edx
	dynamicznie := thread.ProcesorStan.Esi

	PortZapisbyte(0x20, 0x20)
	jumpTrybużytkownikairet(eip, użytkownikesp, eflags, userprocwpis, globalnyPrzesunięcieTabela_2, dynamicznie)
	konsola_2.MWydrukuj(([]byte)("usermode end"))
}
func wydrukujesp(esp uint32) {
	konsola_2.MWydrukuj(([]byte)("esp["))
	konsola_2.MUnsignedinteger32Wydrukuj(esp)
}
