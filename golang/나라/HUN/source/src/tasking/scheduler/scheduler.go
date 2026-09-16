/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "konzol"
import . "gdt"
import . "port"
import . "util/lista"

import . "megszakítás"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memóriamanager"

const SchedulerGyakoriság = 1
const KernelheapIndítás = 1024 * 1024
const schedulerHibakeresés = false
const pitGyakoriság = 100

var lista LinkedLista

type Schedulerdata struct {
	gyakoriság	uint32
	tickSzámláló	uint32

	switchforced	bool

	Engedélyezve	bool

	jelenlegithread	*TThread
	tss		*Tssbejegyzés
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickSzámláló = 0
	schedata.gyakoriság = SchedulerGyakoriság
	schedata.jelenlegithread = nil
	schedata.Engedélyezve = false
	schedata.switchforced = false

}

var konzol_2 = TKonzol{}
var jelenlegithreadindex int = 0
var következőFolyamatAzonosító uint32 = 1

func Allocatepid() uint32 {
	pid := következőFolyamatAzonosító
	következőFolyamatAzonosító++
	return pid
}

func (self *Schedulerdata) GetKövetkezőKészthread() *TThread {
	if lista.Méret_2 <= 0 {
		return nil
	}

	if schedata.jelenlegithread != nil {
		jelenlegithreadindex = lista.Indexof(uintptr(Pointer(schedata.jelenlegithread)))
		if jelenlegithreadindex < 0 {
			jelenlegithreadindex = 0
		}
	} else {
		jelenlegithreadindex = -1
	}

	for checked := 0; checked < lista.Méret_2; checked++ {
		jelenlegithreadindex++
		if jelenlegithreadindex >= lista.Méret_2 {
			jelenlegithreadindex = 0
		}
		thread := (*TThread)(lista.Getat(jelenlegithreadindex))
		if thread != nil && thread.ThreadÁllapot != Blocked && thread.ThreadÁllapot != Leállítva {
			if schedulerHibakeresés {
				konzol_2.MNyomtatás("ti:")
				konzol_2.MUnsignedinteger32Nyomtatás(uint32(jelenlegithreadindex))
				konzol_2.MNyomtatás(":")
				konzol_2.MUnsignedinteger32Nyomtatás(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.jelenlegithread

}
func (self *Scheduler) Hozzáadásthread(thread *TThread) {
	if thread == nil {
		return
	}
	lista.Append_to_list(uintptr(Pointer(thread)))
}
func Hozzáadásrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	lista.Append_to_list(uintptr(Pointer(thread)))
}

func Jelenlegipid() uint32 {
	if schedata.jelenlegithread == nil || schedata.jelenlegithread.Pid == 0 {
		return 1
	}
	return schedata.jelenlegithread.Pid
}

func Jelenlegiparentpid() uint32 {
	if schedata.jelenlegithread == nil {
		return 0
	}
	return schedata.jelenlegithread.Parentpid
}
func (self *Scheduler) Eltávolításthread(thread *TThread) {
	lista.Eltávolítás(uintptr(Pointer(thread)))
}

func (self *Scheduler) Eltávolításthreadat(index int) {
	lista.Eltávolításat(index)
}

type Scheduler struct {
	TMegszakításhandler
}

func (self *Scheduler) Init(manager *TMegszakításmanager, mem *mem.TMemóriamanager, tss *Tssbejegyzés) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitGyakoriság)

	lista = LinkedLista{}
	lista.Init(mem)
	konzol_2.MNyomtatás("list:")
	konzol_2.MUnsignedinteger32Nyomtatás(uint32(uintptr(Pointer(&lista))))

	megszakításhandler = fogantyúMegszakítás
	var address uintptr
	address = uintptr(Pointer(&megszakításhandler))
	self.TMegszakításhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Engedélyezve(engedélyezve bool) {
	schedata.Engedélyezve = engedélyezve
}

func initpit(gyakoriság uint32) {
	if gyakoriság == 0 {
		return
	}
	divisor := uint32(1193180) / gyakoriság
	PortÍrásbyte(0x43, 0x36)
	PortÍrásbyte(0x40, uint8(divisor&0xFF))
	PortÍrásbyte(0x40, uint8((divisor>>8)&0xFF))
}

func halmazds(dssegment uint32)
func halmazgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func helyreállításfpregs(buffer_2 uintptr)

var jmpFelhasználó uint32 = 0
var megszakításhandler func(uint32) uint32

func schedulestack(fn func())
func halmazcr3(address uint32)
func getcr3() uint32

func fogantyúMegszakítás(esp uint32) uint32 {

	schedata.tickSzámláló++

	if schedulerHibakeresés {
		konzol_2.MNyomtatásxy(([]byte)("sche1:"), 1, 17)

		konzol_2.MNyomtatás(":")
		konzol_2.MUnsignedinteger32Nyomtatás(esp)
		konzol_2.MNyomtatás(":")

		konzol_2.MUnsignedinteger32Nyomtatás(uint32(schedata.tickSzámláló))
		konzol_2.MNyomtatás(":")
		konzol_2.MUnsignedinteger32Nyomtatás(KernelheapIndítás)
	}

	if schedata.tickSzámláló == schedata.gyakoriság {
		schedata.tickSzámláló = 0

		if lista.Méret_2 > 0 && schedata.Engedélyezve == true {
			var következőthread = schedata.GetKövetkezőKészthread()
			if következőthread == nil {
				return esp
			}
			if schedata.jelenlegithread == nil {
				MEmergencylogKarakterlánc("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogKarakterlánc(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(következőthread))))
				MEmergencylogKarakterlánc(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(következőthread.CpuÁllapot))))
				MEmergencylogKarakterlánc(" state=")
				MEmergencylogunsignedinteger32(uint32(következőthread.ThreadÁllapot))
				MEmergencylogKarakterlánc(" eip=")
				MEmergencylogunsignedinteger32(következőthread.CpuÁllapot.Eip)
				MEmergencylogKarakterlánc(" cs=")
				MEmergencylogunsignedinteger32(következőthread.CpuÁllapot.Cs)
				MEmergencylogKarakterlánc("\n")
			}

			if esp >= KernelheapIndítás && schedata.jelenlegithread != nil {
				schedata.jelenlegithread.CpuÁllapot = (*TcpuÁllapot)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.jelenlegithread.Fpubuffer)))
				eltolás := (16 - (address % 16)) & 0xF
				schedata.jelenlegithread.FpuEltolás = eltolás
				backupfpregs(address + eltolás)
				if schedulerHibakeresés {
					konzol_2.MNyomtatás(([]byte)("backup"))
					konzol_2.MUnsignedinteger32Nyomtatás(esp)
				}
			}

			address := uintptr(Pointer(&(következőthread.Fpubuffer)))
			eltolás := következőthread.FpuEltolás
			if eltolás != 0xffffffff {
				helyreállításfpregs(address + eltolás)
				if schedulerHibakeresés {
					konzol_2.MNyomtatás(([]byte)("restore"))
				}
			}

			schedata.jelenlegithread = következőthread

			if schedata.jelenlegithread.ThreadÁllapot == Indítva {
				schedata.jelenlegithread.ThreadÁllapot = Kész

				InitialthreadFelhasználójump(schedata.jelenlegithread)
				return esp
			}

			esp = uint32(uintptr(Pointer(következőthread.CpuÁllapot)))
			if következőthread.Stack != 0 {
				schedata.tss.Halmazstack(Segkerneldata, következőthread.Stack+ThreadstackMéret)
			}

			halmazcr3(következőthread.OldalKönyvtárbejegyzés)
			halmazgs(következőthread.CpuÁllapot.Gs)

		}

	}

	return esp
}

func jumpFelhasználóiüzemmódiret(uint32, uint32, uint32, uint32, uint32, uint32)
func LetiltvaEgész()

func getesp() uint32
func threadKilépésHurok()

func halmazthreadKilépésHurokÁllapot(cpuÁllapot *TcpuÁllapot) {
	cpuÁllapot.Eip = uint32(ValueOf(threadKilépésHurok).Pointer())
	cpuÁllapot.Cs = Segkernelcode
	cpuÁllapot.Ds = Segkerneldata
	cpuÁllapot.Es = Segkerneldata
	cpuÁllapot.Fs = Segkerneldata
	cpuÁllapot.Gs = Segkernelgs
	cpuÁllapot.Ss = Segkerneldata
	cpuÁllapot.Eflags = 0x202
}

func LeállításJelenlegithread(cpuÁllapot *TcpuÁllapot) *TcpuÁllapot {
	if schedata.jelenlegithread == nil {
		halmazthreadKilépésHurokÁllapot(cpuÁllapot)
		return cpuÁllapot
	}

	leállítvathread := schedata.jelenlegithread
	for i := 0; i < lista.Méret_2; i++ {
		thread := (*TThread)(lista.Getat(i))
		if thread != nil && thread.CpuÁllapot == cpuÁllapot {
			leállítvathread = thread
			break
		}
	}
	leállítvathread.CpuÁllapot = cpuÁllapot
	leállítvathread.ThreadÁllapot = Leállítva
	schedata.jelenlegithread = leállítvathread

	következőthread := schedata.GetKövetkezőKészthread()
	if következőthread == nil || következőthread == leállítvathread || következőthread.CpuÁllapot == nil || következőthread.CpuÁllapot == cpuÁllapot {
		halmazthreadKilépésHurokÁllapot(cpuÁllapot)
		return cpuÁllapot
	}

	schedata.jelenlegithread = következőthread
	if következőthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Halmazstack(Segkerneldata, következőthread.Stack+ThreadstackMéret)
	}
	halmazcr3(következőthread.OldalKönyvtárbejegyzés)
	halmazgs(következőthread.CpuÁllapot.Gs)
	return következőthread.CpuÁllapot
}

func InitialthreadFelhasználójump(thread *TThread) {

	LetiltvaEgész()

	schedata.tss.Halmazstack(Segkerneldata, thread.Stack+ThreadstackMéret)

	halmazcr3(thread.OldalKönyvtárbejegyzés)
	halmazgs(thread.CpuÁllapot.Gs)

	schedata.jelenlegithread = thread
	schedata.Engedélyezve = true

	eip := thread.CpuÁllapot.Eip
	felhasználóesp := thread.Felhasználóstack_2 + thread.FelhasználóstackMéret_2
	eflags := thread.CpuÁllapot.Eflags
	cs := thread.CpuÁllapot.Cs
	esp := schedata.tss.Getesp0()

	konzol_2.MNyomtatás(([]byte)("jump["))
	konzol_2.MUnsignedinteger32Nyomtatás(eip)
	konzol_2.MNyomtatás(([]byte)(":"))
	konzol_2.MUnsignedinteger32Nyomtatás(felhasználóesp)
	konzol_2.MNyomtatás(([]byte)(":"))
	konzol_2.MUnsignedinteger32Nyomtatás(eflags)
	konzol_2.MNyomtatás(([]byte)(":"))
	konzol_2.MUnsignedinteger32Nyomtatás(cs)
	konzol_2.MNyomtatás(([]byte)(":"))

	konzol_2.MUnsignedinteger32Nyomtatás(esp)
	konzol_2.MNyomtatás(([]byte)("]"))

	userprocbejegyzés := thread.CpuÁllapot.Ecx
	globálisEltolásTáblázat_2 := thread.CpuÁllapot.Edx
	dinamikus := thread.CpuÁllapot.Esi

	PortÍrásbyte(0x20, 0x20)
	jumpFelhasználóiüzemmódiret(eip, felhasználóesp, eflags, userprocbejegyzés, globálisEltolásTáblázat_2, dinamikus)
	konzol_2.MNyomtatás(([]byte)("usermode end"))
}
func nyomtatásesp(esp uint32) {
	konzol_2.MNyomtatás(([]byte)("esp["))
	konzol_2.MUnsignedinteger32Nyomtatás(esp)
}
