package scheduler

import . "unsafe"
import . "reflect"

import . "konzola"
import . "gdt"
import . "port"
import . "util/spisak"

import . "ometanje"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memorijamanager"

const SchedulerUčestanost = 1
const KernelheapPokreni = 1024 * 1024
const schedulerIspravljanje = false
const pitUčestanost = 100

var spisak LinkedSpisak

type Schedulerdata struct {
	učestanost	uint32
	tickcount	uint32

	switchforced	bool

	Omogućeno	bool

	trenutnothread	*TThread
	tss		*Tssunos
}

var schedata Schedulerdata = Schedulerdata{}

func (isti *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.učestanost = SchedulerUčestanost
	schedata.trenutnothread = nil
	schedata.Omogućeno = false
	schedata.switchforced = false

}

var konzola_2 = TKonzola{}
var trenutnothreadPopis int = 0
var sledećeProcesIB uint32 = 1

func AllocatePID() uint32 {
	pID := sledećeProcesIB
	sledećeProcesIB++
	return pID
}

func (isti *Schedulerdata) GetSledećeSpremanthread() *TThread {
	if spisak.Veličina_2 <= 0 {
		return nil
	}

	if schedata.trenutnothread != nil {
		trenutnothreadPopis = spisak.Popisod(uintptr(Pointer(schedata.trenutnothread)))
		if trenutnothreadPopis < 0 {
			trenutnothreadPopis = 0
		}
	} else {
		trenutnothreadPopis = -1
	}

	for checked := 0; checked < spisak.Veličina_2; checked++ {
		trenutnothreadPopis++
		if trenutnothreadPopis >= spisak.Veličina_2 {
			trenutnothreadPopis = 0
		}
		thread := (*TThread)(spisak.Getat(trenutnothreadPopis))
		if thread != nil && thread.ThreadStanje != Blocked && thread.ThreadStanje != Zaustavljen {
			if schedulerIspravljanje {
				konzola_2.MŠtampaj("ti:")
				konzola_2.MUnsignedinteger32Štampaj(uint32(trenutnothreadPopis))
				konzola_2.MŠtampaj(":")
				konzola_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.trenutnothread

}
func (isti *Scheduler) Dodajthread(thread *TThread) {
	if thread == nil {
		return
	}
	spisak.Append_to_list(uintptr(Pointer(thread)))
}
func Dodajrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	spisak.Append_to_list(uintptr(Pointer(thread)))
}

func TrenutnoPID() uint32 {
	if schedata.trenutnothread == nil || schedata.trenutnothread.PID == 0 {
		return 1
	}
	return schedata.trenutnothread.PID
}

func TrenutnonadređeniPID() uint32 {
	if schedata.trenutnothread == nil {
		return 0
	}
	return schedata.trenutnothread.NadređeniPID
}
func (isti *Scheduler) Uklonithread(thread *TThread) {
	spisak.Ukloni(uintptr(Pointer(thread)))
}

func (isti *Scheduler) Uklonithreadat(popis int) {
	spisak.Ukloniat(popis)
}

type Scheduler struct {
	TOmetanjehandler
}

func (isti *Scheduler) Init(manager *TOmetanjemanager, mem *mem.TMemorijamanager, tss *Tssunos) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitUčestanost)

	spisak = LinkedSpisak{}
	spisak.Init(mem)
	konzola_2.MŠtampaj("list:")
	konzola_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&spisak))))

	ometanjehandler = ručkaOmetanje
	var address uintptr
	address = uintptr(Pointer(&ometanjehandler))
	isti.TOmetanjehandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (isti *Scheduler) Omogućeno(omogućeno bool) {
	schedata.Omogućeno = omogućeno
}

func initpit(učestanost uint32) {
	if učestanost == 0 {
		return
	}
	divisor := uint32(1193180) / učestanost
	PortPišebyte(0x43, 0x36)
	PortPišebyte(0x40, uint8(divisor&0xFF))
	PortPišebyte(0x40, uint8((divisor>>8)&0xFF))
}

func skupds(dssegment uint32)
func skupgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func povratifpregs(buffer_2 uintptr)

var jmpKorisnik uint32 = 0
var ometanjehandler func(uint32) uint32

func schedulestack(fn func())
func skupcr3(address uint32)
func getcr3() uint32

func ručkaOmetanje(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerIspravljanje {
		konzola_2.MŠtampajxy(([]byte)("sche1:"), 1, 17)

		konzola_2.MŠtampaj(":")
		konzola_2.MUnsignedinteger32Štampaj(esp)
		konzola_2.MŠtampaj(":")

		konzola_2.MUnsignedinteger32Štampaj(uint32(schedata.tickcount))
		konzola_2.MŠtampaj(":")
		konzola_2.MUnsignedinteger32Štampaj(KernelheapPokreni)
	}

	if schedata.tickcount == schedata.učestanost {
		schedata.tickcount = 0

		if spisak.Veličina_2 > 0 && schedata.Omogućeno == true {
			var sledećethread = schedata.GetSledećeSpremanthread()
			if sledećethread == nil {
				return esp
			}
			if schedata.trenutnothread == nil {
				MEmergencyDnevnikniska("\nSCHED first esp=")
				MEmergencyDnevnikunsignedinteger32(esp)
				MEmergencyDnevnikniska(" thread=")
				MEmergencyDnevnikunsignedinteger32(uint32(uintptr(Pointer(sledećethread))))
				MEmergencyDnevnikniska(" cpu=")
				MEmergencyDnevnikunsignedinteger32(uint32(uintptr(Pointer(sledećethread.ProcesorStanje))))
				MEmergencyDnevnikniska(" state=")
				MEmergencyDnevnikunsignedinteger32(uint32(sledećethread.ThreadStanje))
				MEmergencyDnevnikniska(" eip=")
				MEmergencyDnevnikunsignedinteger32(sledećethread.ProcesorStanje.Eip)
				MEmergencyDnevnikniska(" cs=")
				MEmergencyDnevnikunsignedinteger32(sledećethread.ProcesorStanje.Cs)
				MEmergencyDnevnikniska("\n")
			}

			if esp >= KernelheapPokreni && schedata.trenutnothread != nil {
				schedata.trenutnothread.ProcesorStanje = (*TcpuStanje)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.trenutnothread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.trenutnothread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerIspravljanje {
					konzola_2.MŠtampaj(([]byte)("backup"))
					konzola_2.MUnsignedinteger32Štampaj(esp)
				}
			}

			address := uintptr(Pointer(&(sledećethread.Fpubuffer)))
			offset := sledećethread.Fpuoffset
			if offset != 0xffffffff {
				povratifpregs(address + offset)
				if schedulerIspravljanje {
					konzola_2.MŠtampaj(([]byte)("restore"))
				}
			}

			schedata.trenutnothread = sledećethread

			if schedata.trenutnothread.ThreadStanje == Pokrenut {
				schedata.trenutnothread.ThreadStanje = Spreman

				InitialthreadKorisnikjump(schedata.trenutnothread)
				return esp
			}

			esp = uint32(uintptr(Pointer(sledećethread.ProcesorStanje)))
			if sledećethread.Stack != 0 {
				schedata.tss.Skupstack(Segkerneldata, sledećethread.Stack+ThreadstackVeličina)
			}

			skupcr3(sledećethread.STRANADirektorijumunos)
			skupgs(sledećethread.ProcesorStanje.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func IsključiCelibroj()

func getesp() uint32
func threadIzlazloop()

func skupthreadIzlazloopStanje(procesorStanje *TcpuStanje) {
	procesorStanje.Eip = uint32(ValueOf(threadIzlazloop).Pointer())
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
		skupthreadIzlazloopStanje(procesorStanje)
		return procesorStanje
	}

	zaustavljenthread := schedata.trenutnothread
	for i := 0; i < spisak.Veličina_2; i++ {
		thread := (*TThread)(spisak.Getat(i))
		if thread != nil && thread.ProcesorStanje == procesorStanje {
			zaustavljenthread = thread
			break
		}
	}
	zaustavljenthread.ProcesorStanje = procesorStanje
	zaustavljenthread.ThreadStanje = Zaustavljen
	schedata.trenutnothread = zaustavljenthread

	sledećethread := schedata.GetSledećeSpremanthread()
	if sledećethread == nil || sledećethread == zaustavljenthread || sledećethread.ProcesorStanje == nil || sledećethread.ProcesorStanje == procesorStanje {
		skupthreadIzlazloopStanje(procesorStanje)
		return procesorStanje
	}

	schedata.trenutnothread = sledećethread
	if sledećethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Skupstack(Segkerneldata, sledećethread.Stack+ThreadstackVeličina)
	}
	skupcr3(sledećethread.STRANADirektorijumunos)
	skupgs(sledećethread.ProcesorStanje.Gs)
	return sledećethread.ProcesorStanje
}

func InitialthreadKorisnikjump(thread *TThread) {

	IsključiCelibroj()

	schedata.tss.Skupstack(Segkerneldata, thread.Stack+ThreadstackVeličina)

	skupcr3(thread.STRANADirektorijumunos)
	skupgs(thread.ProcesorStanje.Gs)

	schedata.trenutnothread = thread
	schedata.Omogućeno = true

	eip := thread.ProcesorStanje.Eip
	korisnikesp := thread.Korisnikstack_2 + thread.KorisnikstackVeličina_2
	eflags := thread.ProcesorStanje.Eflags
	cs := thread.ProcesorStanje.Cs
	esp := schedata.tss.Getesp0()

	konzola_2.MŠtampaj(([]byte)("jump["))
	konzola_2.MUnsignedinteger32Štampaj(eip)
	konzola_2.MŠtampaj(([]byte)(":"))
	konzola_2.MUnsignedinteger32Štampaj(korisnikesp)
	konzola_2.MŠtampaj(([]byte)(":"))
	konzola_2.MUnsignedinteger32Štampaj(eflags)
	konzola_2.MŠtampaj(([]byte)(":"))
	konzola_2.MUnsignedinteger32Štampaj(cs)
	konzola_2.MŠtampaj(([]byte)(":"))

	konzola_2.MUnsignedinteger32Štampaj(esp)
	konzola_2.MŠtampaj(([]byte)("]"))

	userprocunos := thread.ProcesorStanje.Ecx
	opšteoffsetTabela_2 := thread.ProcesorStanje.Edx
	rastegljivo := thread.ProcesorStanje.Esi

	PortPišebyte(0x20, 0x20)
	jumpusermodeiret(eip, korisnikesp, eflags, userprocunos, opšteoffsetTabela_2, rastegljivo)
	konzola_2.MŠtampaj(([]byte)("usermode end"))
}
func štampajesp(esp uint32) {
	konzola_2.MŠtampaj(([]byte)("esp["))
	konzola_2.MUnsignedinteger32Štampaj(esp)
}
