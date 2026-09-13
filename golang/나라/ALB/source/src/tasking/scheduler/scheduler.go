package scheduler

import . "unsafe"
import . "reflect"

import . "konsolë"
import . "gdt"
import . "porta"
import . "util/listë"

import . "interrupt"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memoriaManazhuesi"

const SchedulerShpeshti = 1
const KernelheapFillo = 1024 * 1024
const schedulerdebug = false
const pitShpeshti = 100

var listë LinkedListë

type Schedulerdata struct {
	shpeshti	uint32
	tickcount	uint32

	switchforced	bool

	Aktivuar	bool

	etanishmethread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (vetvetja *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.shpeshti = SchedulerShpeshti
	schedata.etanishmethread = nil
	schedata.Aktivuar = false
	schedata.switchforced = false

}

var konsolë_2 = TKonsolë{}
var etanishmethreadTreguesi int = 0
var pasuesenProçesid uint32 = 1

func Allocatepid() uint32 {
	pid := pasuesenProçesid
	pasuesenProçesid++
	return pid
}

func (vetvetja *Schedulerdata) GetPasuesenGatithread() *TThread {
	if listë.Madhësia_2 <= 0 {
		return nil
	}

	if schedata.etanishmethread != nil {
		etanishmethreadTreguesi = listë.Treguesinga(uintptr(Pointer(schedata.etanishmethread)))
		if etanishmethreadTreguesi < 0 {
			etanishmethreadTreguesi = 0
		}
	} else {
		etanishmethreadTreguesi = -1
	}

	for checked := 0; checked < listë.Madhësia_2; checked++ {
		etanishmethreadTreguesi++
		if etanishmethreadTreguesi >= listë.Madhësia_2 {
			etanishmethreadTreguesi = 0
		}
		thread := (*TThread)(listë.Getat(etanishmethreadTreguesi))
		if thread != nil && thread.ThreadGjendje != Blocked && thread.ThreadGjendje != Undërpre {
			if schedulerdebug {
				konsolë_2.MPrinto("ti:")
				konsolë_2.MUnsignedinteger32Printo(uint32(etanishmethreadTreguesi))
				konsolë_2.MPrinto(":")
				konsolë_2.MUnsignedinteger32Printo(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.etanishmethread

}
func (vetvetja *Scheduler) Shtothread(thread *TThread) {
	if thread == nil {
		return
	}
	listë.Append_to_list(uintptr(Pointer(thread)))
}
func Shtorunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	listë.Append_to_list(uintptr(Pointer(thread)))
}

func Etanishmepid() uint32 {
	if schedata.etanishmethread == nil || schedata.etanishmethread.Pid == 0 {
		return 1
	}
	return schedata.etanishmethread.Pid
}

func Etanishmeprindpid() uint32 {
	if schedata.etanishmethread == nil {
		return 0
	}
	return schedata.etanishmethread.Prindpid
}
func (vetvetja *Scheduler) Hiqethread(thread *TThread) {
	listë.Hiqe(uintptr(Pointer(thread)))
}

func (vetvetja *Scheduler) Hiqethreadat(treguesi int) {
	listë.Hiqeat(treguesi)
}

type Scheduler struct {
	TInterrupthandler
}

func (vetvetja *Scheduler) Init(manazhuesi *TInterruptManazhuesi, mem *mem.TMemoriaManazhuesi, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitShpeshti)

	listë = LinkedListë{}
	listë.Init(mem)
	konsolë_2.MPrinto("list:")
	konsolë_2.MUnsignedinteger32Printo(uint32(uintptr(Pointer(&listë))))

	interrupthandler = handleinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))
	vetvetja.TInterrupthandler.Init(0x20, uintptr(Pointer(manazhuesi)), address)
}

func (vetvetja *Scheduler) Aktivuar(aktivuar bool) {
	schedata.Aktivuar = aktivuar
}

func initpit(shpeshti uint32) {
	if shpeshti == 0 {
		return
	}
	divisor := uint32(1193180) / shpeshti
	PortaShkrimibyte(0x43, 0x36)
	PortaShkrimibyte(0x40, uint8(divisor&0xFF))
	PortaShkrimibyte(0x40, uint8((divisor>>8)&0xFF))
}

func caktonids(dssegment uint32)
func caktonigs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func rikthefpregs(buffer_2 uintptr)

var jmpPërdoruesi uint32 = 0
var interrupthandler func(uint32) uint32

func schedulestack(fn func())
func caktonicr3(address uint32)
func getcr3() uint32

func handleinterrupt(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		konsolë_2.MPrintoxy(([]byte)("sche1:"), 1, 17)

		konsolë_2.MPrinto(":")
		konsolë_2.MUnsignedinteger32Printo(esp)
		konsolë_2.MPrinto(":")

		konsolë_2.MUnsignedinteger32Printo(uint32(schedata.tickcount))
		konsolë_2.MPrinto(":")
		konsolë_2.MUnsignedinteger32Printo(KernelheapFillo)
	}

	if schedata.tickcount == schedata.shpeshti {
		schedata.tickcount = 0

		if listë.Madhësia_2 > 0 && schedata.Aktivuar == true {
			var pasuesenthread = schedata.GetPasuesenGatithread()
			if pasuesenthread == nil {
				return esp
			}
			if schedata.etanishmethread == nil {
				MEmergencyRegjistërvarg("\nSCHED first esp=")
				MEmergencyRegjistërunsignedinteger32(esp)
				MEmergencyRegjistërvarg(" thread=")
				MEmergencyRegjistërunsignedinteger32(uint32(uintptr(Pointer(pasuesenthread))))
				MEmergencyRegjistërvarg(" cpu=")
				MEmergencyRegjistërunsignedinteger32(uint32(uintptr(Pointer(pasuesenthread.CpuGjendje))))
				MEmergencyRegjistërvarg(" state=")
				MEmergencyRegjistërunsignedinteger32(uint32(pasuesenthread.ThreadGjendje))
				MEmergencyRegjistërvarg(" eip=")
				MEmergencyRegjistërunsignedinteger32(pasuesenthread.CpuGjendje.Eip)
				MEmergencyRegjistërvarg(" cs=")
				MEmergencyRegjistërunsignedinteger32(pasuesenthread.CpuGjendje.Cs)
				MEmergencyRegjistërvarg("\n")
			}

			if esp >= KernelheapFillo && schedata.etanishmethread != nil {
				schedata.etanishmethread.CpuGjendje = (*TcpuGjendje)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.etanishmethread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.etanishmethread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					konsolë_2.MPrinto(([]byte)("backup"))
					konsolë_2.MUnsignedinteger32Printo(esp)
				}
			}

			address := uintptr(Pointer(&(pasuesenthread.Fpubuffer)))
			offset := pasuesenthread.Fpuoffset
			if offset != 0xffffffff {
				rikthefpregs(address + offset)
				if schedulerdebug {
					konsolë_2.MPrinto(([]byte)("restore"))
				}
			}

			schedata.etanishmethread = pasuesenthread

			if schedata.etanishmethread.ThreadGjendje == Nisur {
				schedata.etanishmethread.ThreadGjendje = Gati

				InitialthreadPërdoruesijump(schedata.etanishmethread)
				return esp
			}

			esp = uint32(uintptr(Pointer(pasuesenthread.CpuGjendje)))
			if pasuesenthread.Stack != 0 {
				schedata.tss.Caktonistack(Segkerneldata, pasuesenthread.Stack+ThreadstackMadhësia)
			}

			caktonicr3(pasuesenthread.FaqeDosjeentry)
			caktonigs(pasuesenthread.CpuGjendje.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Disableint()

func getesp() uint32
func threadDaljaloop()

func caktonithreadDaljaloopGjendje(cpuGjendje *TcpuGjendje) {
	cpuGjendje.Eip = uint32(ValueOf(threadDaljaloop).Pointer())
	cpuGjendje.Cs = Segkernelcode
	cpuGjendje.Ds = Segkerneldata
	cpuGjendje.Es = Segkerneldata
	cpuGjendje.Fs = Segkerneldata
	cpuGjendje.Gs = Segkernelgs
	cpuGjendje.Ss = Segkerneldata
	cpuGjendje.Eflags = 0x202
}

func NdaloEtanishmethread(cpuGjendje *TcpuGjendje) *TcpuGjendje {
	if schedata.etanishmethread == nil {
		caktonithreadDaljaloopGjendje(cpuGjendje)
		return cpuGjendje
	}

	undërprethread := schedata.etanishmethread
	for i := 0; i < listë.Madhësia_2; i++ {
		thread := (*TThread)(listë.Getat(i))
		if thread != nil && thread.CpuGjendje == cpuGjendje {
			undërprethread = thread
			break
		}
	}
	undërprethread.CpuGjendje = cpuGjendje
	undërprethread.ThreadGjendje = Undërpre
	schedata.etanishmethread = undërprethread

	pasuesenthread := schedata.GetPasuesenGatithread()
	if pasuesenthread == nil || pasuesenthread == undërprethread || pasuesenthread.CpuGjendje == nil || pasuesenthread.CpuGjendje == cpuGjendje {
		caktonithreadDaljaloopGjendje(cpuGjendje)
		return cpuGjendje
	}

	schedata.etanishmethread = pasuesenthread
	if pasuesenthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Caktonistack(Segkerneldata, pasuesenthread.Stack+ThreadstackMadhësia)
	}
	caktonicr3(pasuesenthread.FaqeDosjeentry)
	caktonigs(pasuesenthread.CpuGjendje.Gs)
	return pasuesenthread.CpuGjendje
}

func InitialthreadPërdoruesijump(thread *TThread) {

	Disableint()

	schedata.tss.Caktonistack(Segkerneldata, thread.Stack+ThreadstackMadhësia)

	caktonicr3(thread.FaqeDosjeentry)
	caktonigs(thread.CpuGjendje.Gs)

	schedata.etanishmethread = thread
	schedata.Aktivuar = true

	eip := thread.CpuGjendje.Eip
	përdoruesiesp := thread.Përdoruesistack_2 + thread.PërdoruesistackMadhësia_2
	eflags := thread.CpuGjendje.Eflags
	cs := thread.CpuGjendje.Cs
	esp := schedata.tss.Getesp0()

	konsolë_2.MPrinto(([]byte)("jump["))
	konsolë_2.MUnsignedinteger32Printo(eip)
	konsolë_2.MPrinto(([]byte)(":"))
	konsolë_2.MUnsignedinteger32Printo(përdoruesiesp)
	konsolë_2.MPrinto(([]byte)(":"))
	konsolë_2.MUnsignedinteger32Printo(eflags)
	konsolë_2.MPrinto(([]byte)(":"))
	konsolë_2.MUnsignedinteger32Printo(cs)
	konsolë_2.MPrinto(([]byte)(":"))

	konsolë_2.MUnsignedinteger32Printo(esp)
	konsolë_2.MPrinto(([]byte)("]"))

	userprocentry := thread.CpuGjendje.Ecx
	globaloffsetTabela_2 := thread.CpuGjendje.Edx
	dynamic := thread.CpuGjendje.Esi

	PortaShkrimibyte(0x20, 0x20)
	jumpusermodeiret(eip, përdoruesiesp, eflags, userprocentry, globaloffsetTabela_2, dynamic)
	konsolë_2.MPrinto(([]byte)("usermode end"))
}
func printoesp(esp uint32) {
	konsolë_2.MPrinto(([]byte)("esp["))
	konsolë_2.MUnsignedinteger32Printo(esp)
}
