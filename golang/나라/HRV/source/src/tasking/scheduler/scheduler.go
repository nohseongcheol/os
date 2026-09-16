/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/popis"

import . "prekid"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memorijamanager"

const SchedulerUčestalost = 1
const KernelheapPokreni = 1024 * 1024
const schedulerdebug = false
const pitUčestalost = 100

var popis LinkedPopis

type Schedulerdata struct {
	učestalost	uint32
	tickcount	uint32

	switchforced	bool

	Omogućeno	bool

	trenutnothread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (sam *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.učestalost = SchedulerUčestalost
	schedata.trenutnothread = nil
	schedata.Omogućeno = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var trenutnothreadKazalo int = 0
var slijedećeProcesIdentifikacija uint32 = 1

func Allocatepid() uint32 {
	pid := slijedećeProcesIdentifikacija
	slijedećeProcesIdentifikacija++
	return pid
}

func (sam *Schedulerdata) GetSlijedećeSpremanthread() *TThread {
	if popis.Veličina_2 <= 0 {
		return nil
	}

	if schedata.trenutnothread != nil {
		trenutnothreadKazalo = popis.Kazalood(uintptr(Pointer(schedata.trenutnothread)))
		if trenutnothreadKazalo < 0 {
			trenutnothreadKazalo = 0
		}
	} else {
		trenutnothreadKazalo = -1
	}

	for checked := 0; checked < popis.Veličina_2; checked++ {
		trenutnothreadKazalo++
		if trenutnothreadKazalo >= popis.Veličina_2 {
			trenutnothreadKazalo = 0
		}
		thread := (*TThread)(popis.Getat(trenutnothreadKazalo))
		if thread != nil && thread.ThreadStanje != Blocked && thread.ThreadStanje != Zaustavljen {
			if schedulerdebug {
				console_2.MIspis("ti:")
				console_2.MUnsignedinteger32Ispis(uint32(trenutnothreadKazalo))
				console_2.MIspis(":")
				console_2.MUnsignedinteger32Ispis(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.trenutnothread

}
func (sam *Scheduler) Dodajthread(thread *TThread) {
	if thread == nil {
		return
	}
	popis.Append_to_list(uintptr(Pointer(thread)))
}
func Dodajrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	popis.Append_to_list(uintptr(Pointer(thread)))
}

func Trenutnopid() uint32 {
	if schedata.trenutnothread == nil || schedata.trenutnothread.Pid == 0 {
		return 1
	}
	return schedata.trenutnothread.Pid
}

func Trenutnoroditeljpid() uint32 {
	if schedata.trenutnothread == nil {
		return 0
	}
	return schedata.trenutnothread.Roditeljpid
}
func (sam *Scheduler) Uklonithread(thread *TThread) {
	popis.Ukloni(uintptr(Pointer(thread)))
}

func (sam *Scheduler) Uklonithreadat(kazalo int) {
	popis.Ukloniat(kazalo)
}

type Scheduler struct {
	TPrekidhandler
}

func (sam *Scheduler) Init(manager *TPrekidmanager, mem *mem.TMemorijamanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitUčestalost)

	popis = LinkedPopis{}
	popis.Init(mem)
	console_2.MIspis("list:")
	console_2.MUnsignedinteger32Ispis(uint32(uintptr(Pointer(&popis))))

	prekidhandler = ručkaPrekid
	var address uintptr
	address = uintptr(Pointer(&prekidhandler))
	sam.TPrekidhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (sam *Scheduler) Omogućeno(omogućeno bool) {
	schedata.Omogućeno = omogućeno
}

func initpit(učestalost uint32) {
	if učestalost == 0 {
		return
	}
	divisor := uint32(1193180) / učestalost
	PortZapišibyte(0x43, 0x36)
	PortZapišibyte(0x40, uint8(divisor&0xFF))
	PortZapišibyte(0x40, uint8((divisor>>8)&0xFF))
}

func postavids(dssegment uint32)
func postavigs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func obnovifpregs(buffer_2 uintptr)

var jmpKorisnik uint32 = 0
var prekidhandler func(uint32) uint32

func schedulestack(fn func())
func postavicr3(address uint32)
func getcr3() uint32

func ručkaPrekid(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MIspisxy(([]byte)("sche1:"), 1, 17)

		console_2.MIspis(":")
		console_2.MUnsignedinteger32Ispis(esp)
		console_2.MIspis(":")

		console_2.MUnsignedinteger32Ispis(uint32(schedata.tickcount))
		console_2.MIspis(":")
		console_2.MUnsignedinteger32Ispis(KernelheapPokreni)
	}

	if schedata.tickcount == schedata.učestalost {
		schedata.tickcount = 0

		if popis.Veličina_2 > 0 && schedata.Omogućeno == true {
			var slijedećethread = schedata.GetSlijedećeSpremanthread()
			if slijedećethread == nil {
				return esp
			}
			if schedata.trenutnothread == nil {
				MEmergencyZapisujZnakovniniz("\nSCHED first esp=")
				MEmergencyZapisujunsignedinteger32(esp)
				MEmergencyZapisujZnakovniniz(" thread=")
				MEmergencyZapisujunsignedinteger32(uint32(uintptr(Pointer(slijedećethread))))
				MEmergencyZapisujZnakovniniz(" cpu=")
				MEmergencyZapisujunsignedinteger32(uint32(uintptr(Pointer(slijedećethread.ProcesorStanje))))
				MEmergencyZapisujZnakovniniz(" state=")
				MEmergencyZapisujunsignedinteger32(uint32(slijedećethread.ThreadStanje))
				MEmergencyZapisujZnakovniniz(" eip=")
				MEmergencyZapisujunsignedinteger32(slijedećethread.ProcesorStanje.Eip)
				MEmergencyZapisujZnakovniniz(" cs=")
				MEmergencyZapisujunsignedinteger32(slijedećethread.ProcesorStanje.Cs)
				MEmergencyZapisujZnakovniniz("\n")
			}

			if esp >= KernelheapPokreni && schedata.trenutnothread != nil {
				schedata.trenutnothread.ProcesorStanje = (*TcpuStanje)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.trenutnothread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.trenutnothread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MIspis(([]byte)("backup"))
					console_2.MUnsignedinteger32Ispis(esp)
				}
			}

			address := uintptr(Pointer(&(slijedećethread.Fpubuffer)))
			offset := slijedećethread.Fpuoffset
			if offset != 0xffffffff {
				obnovifpregs(address + offset)
				if schedulerdebug {
					console_2.MIspis(([]byte)("restore"))
				}
			}

			schedata.trenutnothread = slijedećethread

			if schedata.trenutnothread.ThreadStanje == Pokrenuto {
				schedata.trenutnothread.ThreadStanje = Spreman

				InitialthreadKorisnikjump(schedata.trenutnothread)
				return esp
			}

			esp = uint32(uintptr(Pointer(slijedećethread.ProcesorStanje)))
			if slijedećethread.Stack != 0 {
				schedata.tss.Postavistack(Segkerneldata, slijedećethread.Stack+ThreadstackVeličina)
			}

			postavicr3(slijedećethread.StranicaDirektorijentry)
			postavigs(slijedećethread.ProcesorStanje.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Onemogućiint()

func getesp() uint32
func threadIzađiloop()

func postavithreadIzađiloopStanje(procesorStanje *TcpuStanje) {
	procesorStanje.Eip = uint32(ValueOf(threadIzađiloop).Pointer())
	procesorStanje.Cs = Segkernelcode
	procesorStanje.Ds = Segkerneldata
	procesorStanje.Es = Segkerneldata
	procesorStanje.Fs = Segkerneldata
	procesorStanje.Gs = Segkernelgs
	procesorStanje.Ss = Segkerneldata
	procesorStanje.Eflags = 0x202
}

func ZaustaviTrenutnothread(procesorStanje *TcpuStanje) *TcpuStanje {
	if schedata.trenutnothread == nil {
		postavithreadIzađiloopStanje(procesorStanje)
		return procesorStanje
	}

	zaustavljenthread := schedata.trenutnothread
	for i := 0; i < popis.Veličina_2; i++ {
		thread := (*TThread)(popis.Getat(i))
		if thread != nil && thread.ProcesorStanje == procesorStanje {
			zaustavljenthread = thread
			break
		}
	}
	zaustavljenthread.ProcesorStanje = procesorStanje
	zaustavljenthread.ThreadStanje = Zaustavljen
	schedata.trenutnothread = zaustavljenthread

	slijedećethread := schedata.GetSlijedećeSpremanthread()
	if slijedećethread == nil || slijedećethread == zaustavljenthread || slijedećethread.ProcesorStanje == nil || slijedećethread.ProcesorStanje == procesorStanje {
		postavithreadIzađiloopStanje(procesorStanje)
		return procesorStanje
	}

	schedata.trenutnothread = slijedećethread
	if slijedećethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Postavistack(Segkerneldata, slijedećethread.Stack+ThreadstackVeličina)
	}
	postavicr3(slijedećethread.StranicaDirektorijentry)
	postavigs(slijedećethread.ProcesorStanje.Gs)
	return slijedećethread.ProcesorStanje
}

func InitialthreadKorisnikjump(thread *TThread) {

	Onemogućiint()

	schedata.tss.Postavistack(Segkerneldata, thread.Stack+ThreadstackVeličina)

	postavicr3(thread.StranicaDirektorijentry)
	postavigs(thread.ProcesorStanje.Gs)

	schedata.trenutnothread = thread
	schedata.Omogućeno = true

	eip := thread.ProcesorStanje.Eip
	korisnikesp := thread.Korisnikstack_2 + thread.KorisnikstackVeličina_2
	eflags := thread.ProcesorStanje.Eflags
	cs := thread.ProcesorStanje.Cs
	esp := schedata.tss.Getesp0()

	console_2.MIspis(([]byte)("jump["))
	console_2.MUnsignedinteger32Ispis(eip)
	console_2.MIspis(([]byte)(":"))
	console_2.MUnsignedinteger32Ispis(korisnikesp)
	console_2.MIspis(([]byte)(":"))
	console_2.MUnsignedinteger32Ispis(eflags)
	console_2.MIspis(([]byte)(":"))
	console_2.MUnsignedinteger32Ispis(cs)
	console_2.MIspis(([]byte)(":"))

	console_2.MUnsignedinteger32Ispis(esp)
	console_2.MIspis(([]byte)("]"))

	userprocentry := thread.ProcesorStanje.Ecx
	općioffsetTablica_2 := thread.ProcesorStanje.Edx
	dinamično := thread.ProcesorStanje.Esi

	PortZapišibyte(0x20, 0x20)
	jumpusermodeiret(eip, korisnikesp, eflags, userprocentry, općioffsetTablica_2, dinamično)
	console_2.MIspis(([]byte)("usermode end"))
}
func ispisesp(esp uint32) {
	console_2.MIspis(([]byte)("esp["))
	console_2.MUnsignedinteger32Ispis(esp)
}
