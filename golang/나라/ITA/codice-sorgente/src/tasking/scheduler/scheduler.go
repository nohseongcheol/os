/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "porta"
import . "util/elenco"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memoriamanager"

const SchedulerFrequenza = 1
const KernelheapAvvia = 1024 * 1024
const schedulerFaiildebug = false
const pitFrequenza = 100

var elenco LinkedElenco

type Schedulerdata struct {
	frequenza	uint32
	tickConteggio	uint32

	switchforced	bool

	Abilitato	bool

	correntethread	*TThread
	tss		*Tssvoce
}

var schedata Schedulerdata = Schedulerdata{}

func (séstesso *Schedulerdata) Init() {
	schedata.tickConteggio = 0
	schedata.frequenza = SchedulerFrequenza
	schedata.correntethread = nil
	schedata.Abilitato = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var correntethreadIndice int = 0
var successivoProcessiid uint32 = 1

func Allocatepid() uint32 {
	pid := successivoProcessiid
	successivoProcessiid++
	return pid
}

func (séstesso *Schedulerdata) GetSuccessivoProntothread() *TThread {
	if elenco.Dimensione_2 <= 0 {
		return nil
	}

	if schedata.correntethread != nil {
		correntethreadIndice = elenco.Indicedi(uintptr(Pointer(schedata.correntethread)))
		if correntethreadIndice < 0 {
			correntethreadIndice = 0
		}
	} else {
		correntethreadIndice = -1
	}

	for checked := 0; checked < elenco.Dimensione_2; checked++ {
		correntethreadIndice++
		if correntethreadIndice >= elenco.Dimensione_2 {
			correntethreadIndice = 0
		}
		thread := (*TThread)(elenco.Getat(correntethreadIndice))
		if thread != nil && thread.ThreadStato != Blocked && thread.ThreadStato != Fermato {
			if schedulerFaiildebug {
				console_2.MStampa("ti:")
				console_2.MUnsignedinteger32Stampa(uint32(correntethreadIndice))
				console_2.MStampa(":")
				console_2.MUnsignedinteger32Stampa(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.correntethread

}
func (séstesso *Scheduler) Aggiungithread(thread *TThread) {
	if thread == nil {
		return
	}
	elenco.Aggiungi_in_fondo_alla_lista(uintptr(Pointer(thread)))
}
func Aggiungirunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	elenco.Aggiungi_in_fondo_alla_lista(uintptr(Pointer(thread)))
}

func Correntepid() uint32 {
	if schedata.correntethread == nil || schedata.correntethread.Pid == 0 {
		return 1
	}
	return schedata.correntethread.Pid
}

func Correntegenitorepid() uint32 {
	if schedata.correntethread == nil {
		return 0
	}
	return schedata.correntethread.Genitorepid
}
func (séstesso *Scheduler) Rimuovithread(thread *TThread) {
	elenco.Rimuovi(uintptr(Pointer(thread)))
}

func (séstesso *Scheduler) Rimuovithreadat(indice int) {
	elenco.Rimuoviat(indice)
}

type Scheduler struct {
	TInterrupthandler
}

func (séstesso *Scheduler) Init(manager *TInterruptmanager, mem *mem.TMemoriamanager, tss *Tssvoce) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitFrequenza)

	elenco = LinkedElenco{}
	elenco.Init(mem)
	console_2.MStampa("list:")
	console_2.MUnsignedinteger32Stampa(uint32(uintptr(Pointer(&elenco))))

	interrupthandler = manigliainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	séstesso.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (séstesso *Scheduler) Abilitato(abilitato bool) {
	schedata.Abilitato = abilitato
}

func initpit(frequenza uint32) {
	if frequenza == 0 {
		return
	}
	divisor := uint32(1193180) / frequenza
	PortaScritturabyte(0x43, 0x36)
	PortaScritturabyte(0x40, uint8(divisor&0xFF))
	PortaScritturabyte(0x40, uint8((divisor>>8)&0xFF))
}

func impostads(dssegment uint32)
func impostags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func ripristinafpregs(buffer_2 uintptr)

var jmpUtente uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func impostacr3(address uint32)
func getcr3() uint32

func manigliainterrupt(esp uint32) uint32 {

	schedata.tickConteggio++

	if schedulerFaiildebug {
		console_2.MStampaxy(([]byte)("sche1:"), 1, 17)

		console_2.MStampa(":")
		console_2.MUnsignedinteger32Stampa(esp)
		console_2.MStampa(":")

		console_2.MUnsignedinteger32Stampa(uint32(schedata.tickConteggio))
		console_2.MStampa(":")
		console_2.MUnsignedinteger32Stampa(KernelheapAvvia)
	}

	if schedata.tickConteggio == schedata.frequenza {
		schedata.tickConteggio = 0

		if elenco.Dimensione_2 > 0 && schedata.Abilitato == true {
			var successivothread = schedata.GetSuccessivoProntothread()
			if successivothread == nil {
				return esp
			}
			if schedata.correntethread == nil {
				MEmergencyRegistroStringa("\nSCHED first esp=")
				MEmergencyRegistrounsignedinteger32(esp)
				MEmergencyRegistroStringa(" thread=")
				MEmergencyRegistrounsignedinteger32(uint32(uintptr(Pointer(successivothread))))
				MEmergencyRegistroStringa(" cpu=")
				MEmergencyRegistrounsignedinteger32(uint32(uintptr(Pointer(successivothread.CpuStato))))
				MEmergencyRegistroStringa(" state=")
				MEmergencyRegistrounsignedinteger32(uint32(successivothread.ThreadStato))
				MEmergencyRegistroStringa(" eip=")
				MEmergencyRegistrounsignedinteger32(successivothread.CpuStato.Eip)
				MEmergencyRegistroStringa(" cs=")
				MEmergencyRegistrounsignedinteger32(successivothread.CpuStato.Cs)
				MEmergencyRegistroStringa("\n")
			}

			if esp >= KernelheapAvvia && schedata.correntethread != nil {
				schedata.correntethread.CpuStato = (*TcpuStato)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.correntethread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.correntethread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerFaiildebug {
					console_2.MStampa(([]byte)("backup"))
					console_2.MUnsignedinteger32Stampa(esp)
				}
			}

			address := uintptr(Pointer(&(successivothread.Fpubuffer)))
			offset := successivothread.Fpuoffset
			if offset != 0xffffffff {
				ripristinafpregs(address + offset)
				if schedulerFaiildebug {
					console_2.MStampa(([]byte)("restore"))
				}
			}

			schedata.correntethread = successivothread

			if schedata.correntethread.ThreadStato == Avviato {
				schedata.correntethread.ThreadStato = Pronto

				InitialthreadUtentejump(schedata.correntethread)
				return esp
			}

			esp = uint32(uintptr(Pointer(successivothread.CpuStato)))
			if successivothread.Stack != 0 {
				schedata.tss.Impostastack(Segkerneldata, successivothread.Stack+ThreadstackDimensione)
			}

			impostacr3(successivothread.PAGINACartellavoce)
			impostags(successivothread.CpuStato.Gs)

		}

	}

	return esp
}

func jumpModalitàutenteiret(uint32, uint32, uint32, uint32, uint32, uint32)
func DisabilitaIntero()

func getesp() uint32
func threadEsciloop()

func impostathreadEsciloopStato(cpuStato *TcpuStato) {
	cpuStato.Eip = uint32(ValueOf(threadEsciloop).Pointer())
	cpuStato.Cs = Segkernelcode
	cpuStato.Ds = Segkerneldata
	cpuStato.Es = Segkerneldata
	cpuStato.Fs = Segkerneldata
	cpuStato.Gs = Segkernelgs
	cpuStato.Ss = Segkerneldata
	cpuStato.Eflags = 0x202
}

func FermaCorrentethread(cpuStato *TcpuStato) *TcpuStato {
	if schedata.correntethread == nil {
		impostathreadEsciloopStato(cpuStato)
		return cpuStato
	}

	fermatothread := schedata.correntethread
	for i := 0; i < elenco.Dimensione_2; i++ {
		thread := (*TThread)(elenco.Getat(i))
		if thread != nil && thread.CpuStato == cpuStato {
			fermatothread = thread
			break
		}
	}
	fermatothread.CpuStato = cpuStato
	fermatothread.ThreadStato = Fermato
	schedata.correntethread = fermatothread

	successivothread := schedata.GetSuccessivoProntothread()
	if successivothread == nil || successivothread == fermatothread || successivothread.CpuStato == nil || successivothread.CpuStato == cpuStato {
		impostathreadEsciloopStato(cpuStato)
		return cpuStato
	}

	schedata.correntethread = successivothread
	if successivothread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Impostastack(Segkerneldata, successivothread.Stack+ThreadstackDimensione)
	}
	impostacr3(successivothread.PAGINACartellavoce)
	impostags(successivothread.CpuStato.Gs)
	return successivothread.CpuStato
}

func InitialthreadUtentejump(thread *TThread) {

	DisabilitaIntero()

	schedata.tss.Impostastack(Segkerneldata, thread.Stack+ThreadstackDimensione)

	impostacr3(thread.PAGINACartellavoce)
	impostags(thread.CpuStato.Gs)

	schedata.correntethread = thread
	schedata.Abilitato = true

	eip := thread.CpuStato.Eip
	utenteesp := thread.Utentestack_2 + thread.UtentestackDimensione_2
	eflags := thread.CpuStato.Eflags
	cs := thread.CpuStato.Cs
	esp := schedata.tss.Getesp0()

	console_2.MStampa(([]byte)("jump["))
	console_2.MUnsignedinteger32Stampa(eip)
	console_2.MStampa(([]byte)(":"))
	console_2.MUnsignedinteger32Stampa(utenteesp)
	console_2.MStampa(([]byte)(":"))
	console_2.MUnsignedinteger32Stampa(eflags)
	console_2.MStampa(([]byte)(":"))
	console_2.MUnsignedinteger32Stampa(cs)
	console_2.MStampa(([]byte)(":"))

	console_2.MUnsignedinteger32Stampa(esp)
	console_2.MStampa(([]byte)("]"))

	userprocvoce := thread.CpuStato.Ecx
	globaleoffsetTabella_2 := thread.CpuStato.Edx
	dinamico := thread.CpuStato.Esi

	PortaScritturabyte(0x20, 0x20)
	jumpModalitàutenteiret(eip, utenteesp, eflags, userprocvoce, globaleoffsetTabella_2, dinamico)
	console_2.MStampa(([]byte)("usermode end"))
}
func stampaesp(esp uint32) {
	console_2.MStampa(([]byte)("esp["))
	console_2.MUnsignedinteger32Stampa(esp)
}
