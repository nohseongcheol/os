package scheduler

import . "unsafe"
import . "reflect"

import . "consola"
import . "gdt"
import . "port"
import . "util/llista"

import . "interrupció"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memòriamanager"

const SchedulerFreqüència = 1
const KernelheapInicia = 1024 * 1024
const schedulerDepura = false
const pitFreqüència = 100

var llista LinkedLlista

type Schedulerdata struct {
	freqüència	uint32
	tickRecompte	uint32

	switchforced	bool

	Habilitat	bool

	actualthread	*TThread
	tss		*Tssentrada
}

var schedata Schedulerdata = Schedulerdata{}

func (unmateix *Schedulerdata) Init() {
	schedata.tickRecompte = 0
	schedata.freqüència = SchedulerFreqüència
	schedata.actualthread = nil
	schedata.Habilitat = false
	schedata.switchforced = false

}

var consola_2 = TConsola{}
var actualthreadÍndex int = 0
var següentProcésIdentificador uint32 = 1

func Allocatepid() uint32 {
	pid := següentProcésIdentificador
	següentProcésIdentificador++
	return pid
}

func (unmateix *Schedulerdata) GetSegüentPreparatthread() *TThread {
	if llista.Mida_2 <= 0 {
		return nil
	}

	if schedata.actualthread != nil {
		actualthreadÍndex = llista.Índexde(uintptr(Pointer(schedata.actualthread)))
		if actualthreadÍndex < 0 {
			actualthreadÍndex = 0
		}
	} else {
		actualthreadÍndex = -1
	}

	for checked := 0; checked < llista.Mida_2; checked++ {
		actualthreadÍndex++
		if actualthreadÍndex >= llista.Mida_2 {
			actualthreadÍndex = 0
		}
		thread := (*TThread)(llista.Getat(actualthreadÍndex))
		if thread != nil && thread.ThreadEstat != Blocked && thread.ThreadEstat != Aturat {
			if schedulerDepura {
				consola_2.MImprimeix("ti:")
				consola_2.MUnsignedinteger32Imprimeix(uint32(actualthreadÍndex))
				consola_2.MImprimeix(":")
				consola_2.MUnsignedinteger32Imprimeix(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.actualthread

}
func (unmateix *Scheduler) Afegeixthread(thread *TThread) {
	if thread == nil {
		return
	}
	llista.Append_to_list(uintptr(Pointer(thread)))
}
func Afegeixrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	llista.Append_to_list(uintptr(Pointer(thread)))
}

func Actualpid() uint32 {
	if schedata.actualthread == nil || schedata.actualthread.Pid == 0 {
		return 1
	}
	return schedata.actualthread.Pid
}

func Actualparepid() uint32 {
	if schedata.actualthread == nil {
		return 0
	}
	return schedata.actualthread.Parepid
}
func (unmateix *Scheduler) Eliminathread(thread *TThread) {
	llista.Elimina(uintptr(Pointer(thread)))
}

func (unmateix *Scheduler) Eliminathreadat(índex int) {
	llista.Eliminaat(índex)
}

type Scheduler struct {
	TInterrupcióhandler
}

func (unmateix *Scheduler) Init(manager *TInterrupciómanager, mem *mem.TMemòriamanager, tss *Tssentrada) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitFreqüència)

	llista = LinkedLlista{}
	llista.Init(mem)
	consola_2.MImprimeix("list:")
	consola_2.MUnsignedinteger32Imprimeix(uint32(uintptr(Pointer(&llista))))

	interrupcióhandler = gestorInterrupció
	var adreça uintptr
	adreça = uintptr(Pointer(&interrupcióhandler))
	unmateix.TInterrupcióhandler.Init(0x20, uintptr(Pointer(manager)), adreça)
}

func (unmateix *Scheduler) Habilitat(habilitat bool) {
	schedata.Habilitat = habilitat
}

func initpit(freqüència uint32) {
	if freqüència == 0 {
		return
	}
	divisor := uint32(1193180) / freqüència
	PortEscripturabyte(0x43, 0x36)
	PortEscripturabyte(0x40, uint8(divisor&0xFF))
	PortEscripturabyte(0x40, uint8((divisor>>8)&0xFF))
}

func estableixds(dssegment uint32)
func estableixgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func restaurafpregs(buffer_2 uintptr)

var jmpUsuari uint32 = 0
var interrupcióhandler func(uint32) uint32

func schedulestack(fn func())
func estableixcr3(adreça uint32)
func getcr3() uint32

func gestorInterrupció(esp uint32) uint32 {

	schedata.tickRecompte++

	if schedulerDepura {
		consola_2.MImprimeixxy(([]byte)("sche1:"), 1, 17)

		consola_2.MImprimeix(":")
		consola_2.MUnsignedinteger32Imprimeix(esp)
		consola_2.MImprimeix(":")

		consola_2.MUnsignedinteger32Imprimeix(uint32(schedata.tickRecompte))
		consola_2.MImprimeix(":")
		consola_2.MUnsignedinteger32Imprimeix(KernelheapInicia)
	}

	if schedata.tickRecompte == schedata.freqüència {
		schedata.tickRecompte = 0

		if llista.Mida_2 > 0 && schedata.Habilitat == true {
			var següentthread = schedata.GetSegüentPreparatthread()
			if següentthread == nil {
				return esp
			}
			if schedata.actualthread == nil {
				MEmergencyRegistreCadena("\nSCHED first esp=")
				MEmergencyRegistreunsignedinteger32(esp)
				MEmergencyRegistreCadena(" thread=")
				MEmergencyRegistreunsignedinteger32(uint32(uintptr(Pointer(següentthread))))
				MEmergencyRegistreCadena(" cpu=")
				MEmergencyRegistreunsignedinteger32(uint32(uintptr(Pointer(següentthread.CpuEstat))))
				MEmergencyRegistreCadena(" state=")
				MEmergencyRegistreunsignedinteger32(uint32(següentthread.ThreadEstat))
				MEmergencyRegistreCadena(" eip=")
				MEmergencyRegistreunsignedinteger32(següentthread.CpuEstat.Eip)
				MEmergencyRegistreCadena(" cs=")
				MEmergencyRegistreunsignedinteger32(següentthread.CpuEstat.Cs)
				MEmergencyRegistreCadena("\n")
			}

			if esp >= KernelheapInicia && schedata.actualthread != nil {
				schedata.actualthread.CpuEstat = (*TcpuEstat)(Pointer(uintptr(esp)))

				adreça := uintptr(Pointer(&(schedata.actualthread.Fpubuffer)))
				offset := (16 - (adreça % 16)) & 0xF
				schedata.actualthread.Fpuoffset = offset
				backupfpregs(adreça + offset)
				if schedulerDepura {
					consola_2.MImprimeix(([]byte)("backup"))
					consola_2.MUnsignedinteger32Imprimeix(esp)
				}
			}

			adreça := uintptr(Pointer(&(següentthread.Fpubuffer)))
			offset := següentthread.Fpuoffset
			if offset != 0xffffffff {
				restaurafpregs(adreça + offset)
				if schedulerDepura {
					consola_2.MImprimeix(([]byte)("restore"))
				}
			}

			schedata.actualthread = següentthread

			if schedata.actualthread.ThreadEstat == Iniciat {
				schedata.actualthread.ThreadEstat = Preparat

				InitialthreadUsuarijump(schedata.actualthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(següentthread.CpuEstat)))
			if següentthread.Stack != 0 {
				schedata.tss.Estableixstack(Segkerneldata, següentthread.Stack+ThreadstackMida)
			}

			estableixcr3(següentthread.PàginaDirectorientrada)
			estableixgs(següentthread.CpuEstat.Gs)

		}

	}

	return esp
}

func jumpModedusuariiret(uint32, uint32, uint32, uint32, uint32, uint32)
func InhabilitaEnter()

func getesp() uint32
func threadSurtloop()

func estableixthreadSurtloopEstat(cpuEstat *TcpuEstat) {
	cpuEstat.Eip = uint32(ValueOf(threadSurtloop).Pointer())
	cpuEstat.Cs = Segkernelcode
	cpuEstat.Ds = Segkerneldata
	cpuEstat.Es = Segkerneldata
	cpuEstat.Fs = Segkerneldata
	cpuEstat.Gs = Segkernelgs
	cpuEstat.Ss = Segkerneldata
	cpuEstat.Eflags = 0x202
}

func AturaActualthread(cpuEstat *TcpuEstat) *TcpuEstat {
	if schedata.actualthread == nil {
		estableixthreadSurtloopEstat(cpuEstat)
		return cpuEstat
	}

	aturatthread := schedata.actualthread
	for i := 0; i < llista.Mida_2; i++ {
		thread := (*TThread)(llista.Getat(i))
		if thread != nil && thread.CpuEstat == cpuEstat {
			aturatthread = thread
			break
		}
	}
	aturatthread.CpuEstat = cpuEstat
	aturatthread.ThreadEstat = Aturat
	schedata.actualthread = aturatthread

	següentthread := schedata.GetSegüentPreparatthread()
	if següentthread == nil || següentthread == aturatthread || següentthread.CpuEstat == nil || següentthread.CpuEstat == cpuEstat {
		estableixthreadSurtloopEstat(cpuEstat)
		return cpuEstat
	}

	schedata.actualthread = següentthread
	if següentthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Estableixstack(Segkerneldata, següentthread.Stack+ThreadstackMida)
	}
	estableixcr3(següentthread.PàginaDirectorientrada)
	estableixgs(següentthread.CpuEstat.Gs)
	return següentthread.CpuEstat
}

func InitialthreadUsuarijump(thread *TThread) {

	InhabilitaEnter()

	schedata.tss.Estableixstack(Segkerneldata, thread.Stack+ThreadstackMida)

	estableixcr3(thread.PàginaDirectorientrada)
	estableixgs(thread.CpuEstat.Gs)

	schedata.actualthread = thread
	schedata.Habilitat = true

	eip := thread.CpuEstat.Eip
	usuariesp := thread.Usuaristack_2 + thread.UsuaristackMida_2
	eflags := thread.CpuEstat.Eflags
	cs := thread.CpuEstat.Cs
	esp := schedata.tss.Getesp0()

	consola_2.MImprimeix(([]byte)("jump["))
	consola_2.MUnsignedinteger32Imprimeix(eip)
	consola_2.MImprimeix(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimeix(usuariesp)
	consola_2.MImprimeix(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimeix(eflags)
	consola_2.MImprimeix(([]byte)(":"))
	consola_2.MUnsignedinteger32Imprimeix(cs)
	consola_2.MImprimeix(([]byte)(":"))

	consola_2.MUnsignedinteger32Imprimeix(esp)
	consola_2.MImprimeix(([]byte)("]"))

	userprocentrada := thread.CpuEstat.Ecx
	globaloffsetTaula_2 := thread.CpuEstat.Edx
	dinàmic := thread.CpuEstat.Esi

	PortEscripturabyte(0x20, 0x20)
	jumpModedusuariiret(eip, usuariesp, eflags, userprocentrada, globaloffsetTaula_2, dinàmic)
	consola_2.MImprimeix(([]byte)("usermode end"))
}
func imprimeixesp(esp uint32) {
	consola_2.MImprimeix(([]byte)("esp["))
	consola_2.MUnsignedinteger32Imprimeix(esp)
}
