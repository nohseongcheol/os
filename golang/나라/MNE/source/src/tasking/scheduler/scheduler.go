/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "конзола"
import . "gdt"
import . "порт"
import . "util/spisak"

import . "ометање"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "memorijamanager"

const SchedulerУчестаност = 1
const KernelheapPokreni = 1024 * 1024
const schedulerИсправљање = false
const pitУчестаност = 100

var spisak LinkedSpisak

type Schedulerdata struct {
	учестаност	uint32
	tickcount	uint32

	switchforced	bool

	Омогућено	bool

	тренутноthread	*TThread
	tss		*Tssунос
}

var schedata Schedulerdata = Schedulerdata{}

func (isti *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.учестаност = SchedulerУчестаност
	schedata.тренутноthread = nil
	schedata.Омогућено = false
	schedata.switchforced = false

}

var конзола_2 = TКонзола{}
var тренутноthreadPopis int = 0
var следећеПроцесIB uint32 = 1

func AllocateПИД() uint32 {
	пИД := следећеПроцесIB
	следећеПроцесIB++
	return пИД
}

func (isti *Schedulerdata) GetСледећеСпреманthread() *TThread {
	if spisak.Величина_2 <= 0 {
		return nil
	}

	if schedata.тренутноthread != nil {
		тренутноthreadPopis = spisak.Popisod(uintptr(Pointer(schedata.тренутноthread)))
		if тренутноthreadPopis < 0 {
			тренутноthreadPopis = 0
		}
	} else {
		тренутноthreadPopis = -1
	}

	for checked := 0; checked < spisak.Величина_2; checked++ {
		тренутноthreadPopis++
		if тренутноthreadPopis >= spisak.Величина_2 {
			тренутноthreadPopis = 0
		}
		thread := (*TThread)(spisak.Getat(тренутноthreadPopis))
		if thread != nil && thread.ThreadСтање != Blocked && thread.ThreadСтање != Заустављен {
			if schedulerИсправљање {
				конзола_2.MŠtampaj("ti:")
				конзола_2.MUnsignedinteger32Štampaj(uint32(тренутноthreadPopis))
				конзола_2.MŠtampaj(":")
				конзола_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.тренутноthread

}
func (isti *Scheduler) Додајthread(thread *TThread) {
	if thread == nil {
		return
	}
	spisak.Append_to_list(uintptr(Pointer(thread)))
}
func Додајrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	spisak.Append_to_list(uintptr(Pointer(thread)))
}

func ТренутноПИД() uint32 {
	if schedata.тренутноthread == nil || schedata.тренутноthread.ПИД == 0 {
		return 1
	}
	return schedata.тренутноthread.ПИД
}

func ТренутноnadređeniПИД() uint32 {
	if schedata.тренутноthread == nil {
		return 0
	}
	return schedata.тренутноthread.NadređeniПИД
}
func (isti *Scheduler) Уклониthread(thread *TThread) {
	spisak.Уклони(uintptr(Pointer(thread)))
}

func (isti *Scheduler) Уклониthreadat(popis int) {
	spisak.Уклониat(popis)
}

type Scheduler struct {
	TОметањеhandler
}

func (isti *Scheduler) Init(manager *TОметањеmanager, mem *mem.TMemorijamanager, tss *Tssунос) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitУчестаност)

	spisak = LinkedSpisak{}
	spisak.Init(mem)
	конзола_2.MŠtampaj("list:")
	конзола_2.MUnsignedinteger32Štampaj(uint32(uintptr(Pointer(&spisak))))

	ометањеhandler = ручкаОметање
	var address uintptr
	address = uintptr(Pointer(&ометањеhandler))
	isti.TОметањеhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (isti *Scheduler) Омогућено(омогућено bool) {
	schedata.Омогућено = омогућено
}

func initpit(учестаност uint32) {
	if учестаност == 0 {
		return
	}
	divisor := uint32(1193180) / учестаност
	Портupisbyte(0x43, 0x36)
	Портupisbyte(0x40, uint8(divisor&0xFF))
	Портupisbyte(0x40, uint8((divisor>>8)&0xFF))
}

func скупds(dssegment uint32)
func скупgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func повратиfpregs(buffer_2 uintptr)

var jmpKorisnik uint32 = 0
var ометањеhandler func(uint32) uint32

func schedulestack(fn func())
func скупcr3(address uint32)
func getcr3() uint32

func ручкаОметање(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerИсправљање {
		конзола_2.MŠtampajxy(([]byte)("sche1:"), 1, 17)

		конзола_2.MŠtampaj(":")
		конзола_2.MUnsignedinteger32Štampaj(esp)
		конзола_2.MŠtampaj(":")

		конзола_2.MUnsignedinteger32Štampaj(uint32(schedata.tickcount))
		конзола_2.MŠtampaj(":")
		конзола_2.MUnsignedinteger32Štampaj(KernelheapPokreni)
	}

	if schedata.tickcount == schedata.учестаност {
		schedata.tickcount = 0

		if spisak.Величина_2 > 0 && schedata.Омогућено == true {
			var следећеthread = schedata.GetСледећеСпреманthread()
			if следећеthread == nil {
				return esp
			}
			if schedata.тренутноthread == nil {
				MEmergencyДневникниска("\nSCHED first esp=")
				MEmergencyДневникunsignedinteger32(esp)
				MEmergencyДневникниска(" thread=")
				MEmergencyДневникunsignedinteger32(uint32(uintptr(Pointer(следећеthread))))
				MEmergencyДневникниска(" cpu=")
				MEmergencyДневникunsignedinteger32(uint32(uintptr(Pointer(следећеthread.ПроцесорСтање))))
				MEmergencyДневникниска(" state=")
				MEmergencyДневникunsignedinteger32(uint32(следећеthread.ThreadСтање))
				MEmergencyДневникниска(" eip=")
				MEmergencyДневникunsignedinteger32(следећеthread.ПроцесорСтање.Eip)
				MEmergencyДневникниска(" cs=")
				MEmergencyДневникunsignedinteger32(следећеthread.ПроцесорСтање.Cs)
				MEmergencyДневникниска("\n")
			}

			if esp >= KernelheapPokreni && schedata.тренутноthread != nil {
				schedata.тренутноthread.ПроцесорСтање = (*TcpuСтање)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.тренутноthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.тренутноthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerИсправљање {
					конзола_2.MŠtampaj(([]byte)("backup"))
					конзола_2.MUnsignedinteger32Štampaj(esp)
				}
			}

			address := uintptr(Pointer(&(следећеthread.Fpubuffer)))
			offset := следећеthread.Fpuoffset
			if offset != 0xffffffff {
				повратиfpregs(address + offset)
				if schedulerИсправљање {
					конзола_2.MŠtampaj(([]byte)("restore"))
				}
			}

			schedata.тренутноthread = следећеthread

			if schedata.тренутноthread.ThreadСтање == Započet {
				schedata.тренутноthread.ThreadСтање = Спреман

				InitialthreadKorisnikjump(schedata.тренутноthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(следећеthread.ПроцесорСтање)))
			if следећеthread.Stack != 0 {
				schedata.tss.Скупstack(Segkerneldata, следећеthread.Stack+ThreadstackВеличина)
			}

			скупcr3(следећеthread.ListDirektorijumунос)
			скупgs(следећеthread.ПроцесорСтање.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func ИскључиЦелиброј()

func getesp() uint32
func threadIzlazloop()

func скупthreadIzlazloopСтање(процесорСтање *TcpuСтање) {
	процесорСтање.Eip = uint32(ValueOf(threadIzlazloop).Pointer())
	процесорСтање.Cs = Segkernelcode
	процесорСтање.Ds = Segkerneldata
	процесорСтање.Es = Segkerneldata
	процесорСтање.Fs = Segkerneldata
	процесорСтање.Gs = Segkernelgs
	процесорСтање.Ss = Segkerneldata
	процесорСтање.Eflags = 0x202
}

func ЗауставиТренутноthread(процесорСтање *TcpuСтање) *TcpuСтање {
	if schedata.тренутноthread == nil {
		скупthreadIzlazloopСтање(процесорСтање)
		return процесорСтање
	}

	заустављенthread := schedata.тренутноthread
	for i := 0; i < spisak.Величина_2; i++ {
		thread := (*TThread)(spisak.Getat(i))
		if thread != nil && thread.ПроцесорСтање == процесорСтање {
			заустављенthread = thread
			break
		}
	}
	заустављенthread.ПроцесорСтање = процесорСтање
	заустављенthread.ThreadСтање = Заустављен
	schedata.тренутноthread = заустављенthread

	следећеthread := schedata.GetСледећеСпреманthread()
	if следећеthread == nil || следећеthread == заустављенthread || следећеthread.ПроцесорСтање == nil || следећеthread.ПроцесорСтање == процесорСтање {
		скупthreadIzlazloopСтање(процесорСтање)
		return процесорСтање
	}

	schedata.тренутноthread = следећеthread
	if следећеthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Скупstack(Segkerneldata, следећеthread.Stack+ThreadstackВеличина)
	}
	скупcr3(следећеthread.ListDirektorijumунос)
	скупgs(следећеthread.ПроцесорСтање.Gs)
	return следећеthread.ПроцесорСтање
}

func InitialthreadKorisnikjump(thread *TThread) {

	ИскључиЦелиброј()

	schedata.tss.Скупstack(Segkerneldata, thread.Stack+ThreadstackВеличина)

	скупcr3(thread.ListDirektorijumунос)
	скупgs(thread.ПроцесорСтање.Gs)

	schedata.тренутноthread = thread
	schedata.Омогућено = true

	eip := thread.ПроцесорСтање.Eip
	korisnikesp := thread.Korisnikstack_2 + thread.KorisnikstackВеличина_2
	eflags := thread.ПроцесорСтање.Eflags
	cs := thread.ПроцесорСтање.Cs
	esp := schedata.tss.Getesp0()

	конзола_2.MŠtampaj(([]byte)("jump["))
	конзола_2.MUnsignedinteger32Štampaj(eip)
	конзола_2.MŠtampaj(([]byte)(":"))
	конзола_2.MUnsignedinteger32Štampaj(korisnikesp)
	конзола_2.MŠtampaj(([]byte)(":"))
	конзола_2.MUnsignedinteger32Štampaj(eflags)
	конзола_2.MŠtampaj(([]byte)(":"))
	конзола_2.MUnsignedinteger32Štampaj(cs)
	конзола_2.MŠtampaj(([]byte)(":"))

	конзола_2.MUnsignedinteger32Štampaj(esp)
	конзола_2.MŠtampaj(([]byte)("]"))

	userprocунос := thread.ПроцесорСтање.Ecx
	општеoffsetTabela_2 := thread.ПроцесорСтање.Edx
	rastegǉivo := thread.ПроцесорСтање.Esi

	Портupisbyte(0x20, 0x20)
	jumpusermodeiret(eip, korisnikesp, eflags, userprocунос, општеoffsetTabela_2, rastegǉivo)
	конзола_2.MŠtampaj(([]byte)("usermode end"))
}
func štampajesp(esp uint32) {
	конзола_2.MŠtampaj(([]byte)("esp["))
	конзола_2.MUnsignedinteger32Štampaj(esp)
}
