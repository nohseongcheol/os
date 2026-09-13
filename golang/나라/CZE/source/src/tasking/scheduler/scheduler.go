package scheduler

import . "unsafe"
import . "reflect"

import . "konzole"
import . "gdt"
import . "port"
import . "util/seznam"

import . "přerušení"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "paměťmanager"

const SchedulerČetnost = 1
const KernelheapSpustit = 1024 * 1024
const schedulerLadit = false
const pitČetnost = 100

var seznam LinkedSeznam

type Schedulerdata struct {
	četnost		uint32
	tickPočet	uint32

	switchforced	bool

	Povoleno	bool

	současnýthread	*TThread
	tss		*TssZáznam
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickPočet = 0
	schedata.četnost = SchedulerČetnost
	schedata.současnýthread = nil
	schedata.Povoleno = false
	schedata.switchforced = false

}

var konzole_2 = TKonzole{}
var současnýthreadRejstřík int = 0
var následujícíProcesid uint32 = 1

func Allocatepid() uint32 {
	pid := následujícíProcesid
	následujícíProcesid++
	return pid
}

func (self *Schedulerdata) GetNásledujícíPřipraventhread() *TThread {
	if seznam.Velikost_2 <= 0 {
		return nil
	}

	if schedata.současnýthread != nil {
		současnýthreadRejstřík = seznam.Rejstříkz(uintptr(Pointer(schedata.současnýthread)))
		if současnýthreadRejstřík < 0 {
			současnýthreadRejstřík = 0
		}
	} else {
		současnýthreadRejstřík = -1
	}

	for checked := 0; checked < seznam.Velikost_2; checked++ {
		současnýthreadRejstřík++
		if současnýthreadRejstřík >= seznam.Velikost_2 {
			současnýthreadRejstřík = 0
		}
		thread := (*TThread)(seznam.Getat(současnýthreadRejstřík))
		if thread != nil && thread.ThreadStav != Blocked && thread.ThreadStav != Zastaven {
			if schedulerLadit {
				konzole_2.MTisknout("ti:")
				konzole_2.MUnsignedinteger32Tisknout(uint32(současnýthreadRejstřík))
				konzole_2.MTisknout(":")
				konzole_2.MUnsignedinteger32Tisknout(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.současnýthread

}
func (self *Scheduler) Přidatthread(thread *TThread) {
	if thread == nil {
		return
	}
	seznam.Přidat_na_konec_seznamu(uintptr(Pointer(thread)))
}
func Přidatrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	seznam.Přidat_na_konec_seznamu(uintptr(Pointer(thread)))
}

func Současnýpid() uint32 {
	if schedata.současnýthread == nil || schedata.současnýthread.Pid == 0 {
		return 1
	}
	return schedata.současnýthread.Pid
}

func Současnýrodičpid() uint32 {
	if schedata.současnýthread == nil {
		return 0
	}
	return schedata.současnýthread.Rodičpid
}
func (self *Scheduler) Odstranitthread(thread *TThread) {
	seznam.Odstranit(uintptr(Pointer(thread)))
}

func (self *Scheduler) Odstranitthreadat(rejstřík int) {
	seznam.Odstranitat(rejstřík)
}

type Scheduler struct {
	TPřerušeníhandler
}

func (self *Scheduler) Init(manager *TPřerušenímanager, mem *mem.TPaměťmanager, tss *TssZáznam) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitČetnost)

	seznam = LinkedSeznam{}
	seznam.Init(mem)
	konzole_2.MTisknout("list:")
	konzole_2.MUnsignedinteger32Tisknout(uint32(uintptr(Pointer(&seznam))))

	přerušeníhandler = úchytkaPřerušení
	var adresa uintptr
	adresa = uintptr(Pointer(&přerušeníhandler))
	self.TPřerušeníhandler.Init(0x20, uintptr(Pointer(manager)), adresa)
}

func (self *Scheduler) Povoleno(povoleno bool) {
	schedata.Povoleno = povoleno
}

func initpit(četnost uint32) {
	if četnost == 0 {
		return
	}
	divisor := uint32(1193180) / četnost
	PortZápisbyte(0x43, 0x36)
	PortZápisbyte(0x40, uint8(divisor&0xFF))
	PortZápisbyte(0x40, uint8((divisor>>8)&0xFF))
}

func nastavitds(dssegment uint32)
func nastavitgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func obnovitfpregs(buffer_2 uintptr)

var jmpUživatel uint32 = 0
var přerušeníhandler func(uint32) uint32

func schedulestack(fn func())
func nastavitcr3(adresa uint32)
func getcr3() uint32

func úchytkaPřerušení(esp uint32) uint32 {

	schedata.tickPočet++

	if schedulerLadit {
		konzole_2.MTisknoutxy(([]byte)("sche1:"), 1, 17)

		konzole_2.MTisknout(":")
		konzole_2.MUnsignedinteger32Tisknout(esp)
		konzole_2.MTisknout(":")

		konzole_2.MUnsignedinteger32Tisknout(uint32(schedata.tickPočet))
		konzole_2.MTisknout(":")
		konzole_2.MUnsignedinteger32Tisknout(KernelheapSpustit)
	}

	if schedata.tickPočet == schedata.četnost {
		schedata.tickPočet = 0

		if seznam.Velikost_2 > 0 && schedata.Povoleno == true {
			var následujícíthread = schedata.GetNásledujícíPřipraventhread()
			if následujícíthread == nil {
				return esp
			}
			if schedata.současnýthread == nil {
				MEmergencyProtokolřetězec("\nSCHED first esp=")
				MEmergencyProtokolunsignedinteger32(esp)
				MEmergencyProtokolřetězec(" thread=")
				MEmergencyProtokolunsignedinteger32(uint32(uintptr(Pointer(následujícíthread))))
				MEmergencyProtokolřetězec(" cpu=")
				MEmergencyProtokolunsignedinteger32(uint32(uintptr(Pointer(následujícíthread.CpuStav))))
				MEmergencyProtokolřetězec(" state=")
				MEmergencyProtokolunsignedinteger32(uint32(následujícíthread.ThreadStav))
				MEmergencyProtokolřetězec(" eip=")
				MEmergencyProtokolunsignedinteger32(následujícíthread.CpuStav.Eip)
				MEmergencyProtokolřetězec(" cs=")
				MEmergencyProtokolunsignedinteger32(následujícíthread.CpuStav.Cs)
				MEmergencyProtokolřetězec("\n")
			}

			if esp >= KernelheapSpustit && schedata.současnýthread != nil {
				schedata.současnýthread.CpuStav = (*TcpuStav)(Pointer(uintptr(esp)))

				adresa := uintptr(Pointer(&(schedata.současnýthread.Fpubuffer)))
				offset := (16 - (adresa % 16)) & 0xF
				schedata.současnýthread.Fpuoffset = offset
				backupfpregs(adresa + offset)
				if schedulerLadit {
					konzole_2.MTisknout(([]byte)("backup"))
					konzole_2.MUnsignedinteger32Tisknout(esp)
				}
			}

			adresa := uintptr(Pointer(&(následujícíthread.Fpubuffer)))
			offset := následujícíthread.Fpuoffset
			if offset != 0xffffffff {
				obnovitfpregs(adresa + offset)
				if schedulerLadit {
					konzole_2.MTisknout(([]byte)("restore"))
				}
			}

			schedata.současnýthread = následujícíthread

			if schedata.současnýthread.ThreadStav == Spuštěn {
				schedata.současnýthread.ThreadStav = Připraven

				InitialthreadUživateljump(schedata.současnýthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(následujícíthread.CpuStav)))
			if následujícíthread.Stack != 0 {
				schedata.tss.Nastavitstack(Segkerneldata, následujícíthread.Stack+ThreadstackVelikost)
			}

			nastavitcr3(následujícíthread.StránkaadresářZáznam)
			nastavitgs(následujícíthread.CpuStav.Gs)

		}

	}

	return esp
}

func jumpUživatelskýmódiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Zakázatint()

func getesp() uint32
func threadKonecloop()

func nastavitthreadKonecloopStav(cpuStav *TcpuStav) {
	cpuStav.Eip = uint32(ValueOf(threadKonecloop).Pointer())
	cpuStav.Cs = Segkernelcode
	cpuStav.Ds = Segkerneldata
	cpuStav.Es = Segkerneldata
	cpuStav.Fs = Segkerneldata
	cpuStav.Gs = Segkernelgs
	cpuStav.Ss = Segkerneldata
	cpuStav.Eflags = 0x202
}

func ZastavitSoučasnýthread(cpuStav *TcpuStav) *TcpuStav {
	if schedata.současnýthread == nil {
		nastavitthreadKonecloopStav(cpuStav)
		return cpuStav
	}

	zastaventhread := schedata.současnýthread
	for i := 0; i < seznam.Velikost_2; i++ {
		thread := (*TThread)(seznam.Getat(i))
		if thread != nil && thread.CpuStav == cpuStav {
			zastaventhread = thread
			break
		}
	}
	zastaventhread.CpuStav = cpuStav
	zastaventhread.ThreadStav = Zastaven
	schedata.současnýthread = zastaventhread

	následujícíthread := schedata.GetNásledujícíPřipraventhread()
	if následujícíthread == nil || následujícíthread == zastaventhread || následujícíthread.CpuStav == nil || následujícíthread.CpuStav == cpuStav {
		nastavitthreadKonecloopStav(cpuStav)
		return cpuStav
	}

	schedata.současnýthread = následujícíthread
	if následujícíthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Nastavitstack(Segkerneldata, následujícíthread.Stack+ThreadstackVelikost)
	}
	nastavitcr3(následujícíthread.StránkaadresářZáznam)
	nastavitgs(následujícíthread.CpuStav.Gs)
	return následujícíthread.CpuStav
}

func InitialthreadUživateljump(thread *TThread) {

	Zakázatint()

	schedata.tss.Nastavitstack(Segkerneldata, thread.Stack+ThreadstackVelikost)

	nastavitcr3(thread.StránkaadresářZáznam)
	nastavitgs(thread.CpuStav.Gs)

	schedata.současnýthread = thread
	schedata.Povoleno = true

	eip := thread.CpuStav.Eip
	uživatelesp := thread.Uživatelstack_2 + thread.UživatelstackVelikost_2
	eflags := thread.CpuStav.Eflags
	cs := thread.CpuStav.Cs
	esp := schedata.tss.Getesp0()

	konzole_2.MTisknout(([]byte)("jump["))
	konzole_2.MUnsignedinteger32Tisknout(eip)
	konzole_2.MTisknout(([]byte)(":"))
	konzole_2.MUnsignedinteger32Tisknout(uživatelesp)
	konzole_2.MTisknout(([]byte)(":"))
	konzole_2.MUnsignedinteger32Tisknout(eflags)
	konzole_2.MTisknout(([]byte)(":"))
	konzole_2.MUnsignedinteger32Tisknout(cs)
	konzole_2.MTisknout(([]byte)(":"))

	konzole_2.MUnsignedinteger32Tisknout(esp)
	konzole_2.MTisknout(([]byte)("]"))

	userprocZáznam := thread.CpuStav.Ecx
	globálníoffsetTabulka_2 := thread.CpuStav.Edx
	dynamické := thread.CpuStav.Esi

	PortZápisbyte(0x20, 0x20)
	jumpUživatelskýmódiret(eip, uživatelesp, eflags, userprocZáznam, globálníoffsetTabulka_2, dynamické)
	konzole_2.MTisknout(([]byte)("usermode end"))
}
func tisknoutesp(esp uint32) {
	konzole_2.MTisknout(([]byte)("esp["))
	konzole_2.MUnsignedinteger32Tisknout(esp)
}
