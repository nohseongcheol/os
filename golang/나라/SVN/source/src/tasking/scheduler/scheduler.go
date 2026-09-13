package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "vrata"
import . "util/seznam"

import . "prekinitev"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "pomnilnikmanager"

const Schedulerfrequency = 1
const KernelheapZačni = 1024 * 1024
const schedulerRazhrošči = false
const pitfrequency = 100

var seznam LinkedSeznam

type Schedulerdata struct {
	frequency	uint32
	tickcount	uint32

	switchforced	bool

	Omogočeno	bool

	currentthread	*TThread
	tss		*Tssvnos
}

var schedata Schedulerdata = Schedulerdata{}

func (sam *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.frequency = Schedulerfrequency
	schedata.currentthread = nil
	schedata.Omogočeno = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var currentthreadKazalo int = 0
var naslednjeOpraviloid uint32 = 1

func Allocatepid() uint32 {
	pid := naslednjeOpraviloid
	naslednjeOpraviloid++
	return pid
}

func (sam *Schedulerdata) GetNaslednjePripravljenthread() *TThread {
	if seznam.Velikost_2 <= 0 {
		return nil
	}

	if schedata.currentthread != nil {
		currentthreadKazalo = seznam.Kazalood(uintptr(Pointer(schedata.currentthread)))
		if currentthreadKazalo < 0 {
			currentthreadKazalo = 0
		}
	} else {
		currentthreadKazalo = -1
	}

	for checked := 0; checked < seznam.Velikost_2; checked++ {
		currentthreadKazalo++
		if currentthreadKazalo >= seznam.Velikost_2 {
			currentthreadKazalo = 0
		}
		thread := (*TThread)(seznam.Getat(currentthreadKazalo))
		if thread != nil && thread.ThreadStanje != Blocked && thread.ThreadStanje != Zaustavljeno {
			if schedulerRazhrošči {
				console_2.MNatisni("ti:")
				console_2.MUnsignedinteger32Natisni(uint32(currentthreadKazalo))
				console_2.MNatisni(":")
				console_2.MUnsignedinteger32Natisni(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.currentthread

}
func (sam *Scheduler) Dodajthread(thread *TThread) {
	if thread == nil {
		return
	}
	seznam.Append_to_list(uintptr(Pointer(thread)))
}
func Dodajrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	seznam.Append_to_list(uintptr(Pointer(thread)))
}

func Currentpid() uint32 {
	if schedata.currentthread == nil || schedata.currentthread.Pid == 0 {
		return 1
	}
	return schedata.currentthread.Pid
}

func Currentnadrejenipredmetpid() uint32 {
	if schedata.currentthread == nil {
		return 0
	}
	return schedata.currentthread.Nadrejenipredmetpid
}
func (sam *Scheduler) Odstranithread(thread *TThread) {
	seznam.Odstrani(uintptr(Pointer(thread)))
}

func (sam *Scheduler) Odstranithreadat(kazalo int) {
	seznam.Odstraniat(kazalo)
}

type Scheduler struct {
	TPrekinitevhandler
}

func (sam *Scheduler) Init(manager *TPrekinitevmanager, mem *mem.TPomnilnikmanager, tss *Tssvnos) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitfrequency)

	seznam = LinkedSeznam{}
	seznam.Init(mem)
	console_2.MNatisni("list:")
	console_2.MUnsignedinteger32Natisni(uint32(uintptr(Pointer(&seznam))))

	prekinitevhandler = ročicaPrekinitev
	var address uintptr
	address = uintptr(Pointer(&prekinitevhandler))
	sam.TPrekinitevhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (sam *Scheduler) Omogočeno(omogočeno bool) {
	schedata.Omogočeno = omogočeno
}

func initpit(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	VrataPisanjebyte(0x43, 0x36)
	VrataPisanjebyte(0x40, uint8(divisor&0xFF))
	VrataPisanjebyte(0x40, uint8((divisor>>8)&0xFF))
}

func množicads(dssegment uint32)
func množicags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func obnovifpregs(buffer_2 uintptr)

var jmpUporabnik uint32 = 0
var prekinitevhandler func(uint32) uint32

func schedulestack(fn func())
func množicacr3(address uint32)
func getcr3() uint32

func ročicaPrekinitev(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerRazhrošči {
		console_2.MNatisnixy(([]byte)("sche1:"), 1, 17)

		console_2.MNatisni(":")
		console_2.MUnsignedinteger32Natisni(esp)
		console_2.MNatisni(":")

		console_2.MUnsignedinteger32Natisni(uint32(schedata.tickcount))
		console_2.MNatisni(":")
		console_2.MUnsignedinteger32Natisni(KernelheapZačni)
	}

	if schedata.tickcount == schedata.frequency {
		schedata.tickcount = 0

		if seznam.Velikost_2 > 0 && schedata.Omogočeno == true {
			var naslednjethread = schedata.GetNaslednjePripravljenthread()
			if naslednjethread == nil {
				return esp
			}
			if schedata.currentthread == nil {
				MEmergencylogNiz("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogNiz(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(naslednjethread))))
				MEmergencylogNiz(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(naslednjethread.CPEStanje))))
				MEmergencylogNiz(" state=")
				MEmergencylogunsignedinteger32(uint32(naslednjethread.ThreadStanje))
				MEmergencylogNiz(" eip=")
				MEmergencylogunsignedinteger32(naslednjethread.CPEStanje.Eip)
				MEmergencylogNiz(" cs=")
				MEmergencylogunsignedinteger32(naslednjethread.CPEStanje.Cs)
				MEmergencylogNiz("\n")
			}

			if esp >= KernelheapZačni && schedata.currentthread != nil {
				schedata.currentthread.CPEStanje = (*TcpuStanje)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.currentthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.currentthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerRazhrošči {
					console_2.MNatisni(([]byte)("backup"))
					console_2.MUnsignedinteger32Natisni(esp)
				}
			}

			address := uintptr(Pointer(&(naslednjethread.Fpubuffer)))
			offset := naslednjethread.Fpuoffset
			if offset != 0xffffffff {
				obnovifpregs(address + offset)
				if schedulerRazhrošči {
					console_2.MNatisni(([]byte)("restore"))
				}
			}

			schedata.currentthread = naslednjethread

			if schedata.currentthread.ThreadStanje == Začeto {
				schedata.currentthread.ThreadStanje = Pripravljen

				InitialthreadUporabnikjump(schedata.currentthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(naslednjethread.CPEStanje)))
			if naslednjethread.Stack != 0 {
				schedata.tss.Množicastack(Segkerneldata, naslednjethread.Stack+ThreadstackVelikost)
			}

			množicacr3(naslednjethread.StranMapavnos)
			množicags(naslednjethread.CPEStanje.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func OnemogočiŠtevilo()

func getesp() uint32
func threadIzhodloop()

func množicathreadIzhodloopStanje(cPEStanje *TcpuStanje) {
	cPEStanje.Eip = uint32(ValueOf(threadIzhodloop).Pointer())
	cPEStanje.Cs = Segkernelcode
	cPEStanje.Ds = Segkerneldata
	cPEStanje.Es = Segkerneldata
	cPEStanje.Fs = Segkerneldata
	cPEStanje.Gs = Segkernelgs
	cPEStanje.Ss = Segkerneldata
	cPEStanje.Eflags = 0x202
}

func Zaustavicurrentthread(cPEStanje *TcpuStanje) *TcpuStanje {
	if schedata.currentthread == nil {
		množicathreadIzhodloopStanje(cPEStanje)
		return cPEStanje
	}

	zaustavljenothread := schedata.currentthread
	for i := 0; i < seznam.Velikost_2; i++ {
		thread := (*TThread)(seznam.Getat(i))
		if thread != nil && thread.CPEStanje == cPEStanje {
			zaustavljenothread = thread
			break
		}
	}
	zaustavljenothread.CPEStanje = cPEStanje
	zaustavljenothread.ThreadStanje = Zaustavljeno
	schedata.currentthread = zaustavljenothread

	naslednjethread := schedata.GetNaslednjePripravljenthread()
	if naslednjethread == nil || naslednjethread == zaustavljenothread || naslednjethread.CPEStanje == nil || naslednjethread.CPEStanje == cPEStanje {
		množicathreadIzhodloopStanje(cPEStanje)
		return cPEStanje
	}

	schedata.currentthread = naslednjethread
	if naslednjethread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Množicastack(Segkerneldata, naslednjethread.Stack+ThreadstackVelikost)
	}
	množicacr3(naslednjethread.StranMapavnos)
	množicags(naslednjethread.CPEStanje.Gs)
	return naslednjethread.CPEStanje
}

func InitialthreadUporabnikjump(thread *TThread) {

	OnemogočiŠtevilo()

	schedata.tss.Množicastack(Segkerneldata, thread.Stack+ThreadstackVelikost)

	množicacr3(thread.StranMapavnos)
	množicags(thread.CPEStanje.Gs)

	schedata.currentthread = thread
	schedata.Omogočeno = true

	eip := thread.CPEStanje.Eip
	uporabnikesp := thread.Uporabnikstack_2 + thread.UporabnikstackVelikost_2
	eflags := thread.CPEStanje.Eflags
	cs := thread.CPEStanje.Cs
	esp := schedata.tss.Getesp0()

	console_2.MNatisni(([]byte)("jump["))
	console_2.MUnsignedinteger32Natisni(eip)
	console_2.MNatisni(([]byte)(":"))
	console_2.MUnsignedinteger32Natisni(uporabnikesp)
	console_2.MNatisni(([]byte)(":"))
	console_2.MUnsignedinteger32Natisni(eflags)
	console_2.MNatisni(([]byte)(":"))
	console_2.MUnsignedinteger32Natisni(cs)
	console_2.MNatisni(([]byte)(":"))

	console_2.MUnsignedinteger32Natisni(esp)
	console_2.MNatisni(([]byte)("]"))

	userprocvnos := thread.CPEStanje.Ecx
	splošnooffsetPreglednica_2 := thread.CPEStanje.Edx
	dinamično := thread.CPEStanje.Esi

	VrataPisanjebyte(0x20, 0x20)
	jumpusermodeiret(eip, uporabnikesp, eflags, userprocvnos, splošnooffsetPreglednica_2, dinamično)
	console_2.MNatisni(([]byte)("usermode end"))
}
func natisniesp(esp uint32) {
	console_2.MNatisni(([]byte)("esp["))
	console_2.MUnsignedinteger32Natisni(esp)
}
