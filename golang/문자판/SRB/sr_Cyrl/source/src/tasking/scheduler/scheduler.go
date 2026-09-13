package scheduler

import . "unsafe"
import . "reflect"

import . "конзола"
import . "gdt"
import . "порт"
import . "util/списак"

import . "ометање"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "меморијаmanager"

const SchedulerУчестаност = 1
const KernelheapПокрени = 1024 * 1024
const schedulerИсправљање = false
const pitУчестаност = 100

var списак LinkedСписак

type Schedulerdata struct {
	учестаност	uint32
	tickcount	uint32

	switchforced	bool

	Омогућено	bool

	тренутноthread	*TThread
	tss		*Tssунос
}

var schedata Schedulerdata = Schedulerdata{}

func (исти *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.учестаност = SchedulerУчестаност
	schedata.тренутноthread = nil
	schedata.Омогућено = false
	schedata.switchforced = false

}

var конзола_2 = TКонзола{}
var тренутноthreadПопис int = 0
var следећеПроцесИБ uint32 = 1

func AllocateПИД() uint32 {
	пИД := следећеПроцесИБ
	следећеПроцесИБ++
	return пИД
}

func (исти *Schedulerdata) GetСледећеСпреманthread() *TThread {
	if списак.Величина_2 <= 0 {
		return nil
	}

	if schedata.тренутноthread != nil {
		тренутноthreadПопис = списак.Пописод(uintptr(Pointer(schedata.тренутноthread)))
		if тренутноthreadПопис < 0 {
			тренутноthreadПопис = 0
		}
	} else {
		тренутноthreadПопис = -1
	}

	for checked := 0; checked < списак.Величина_2; checked++ {
		тренутноthreadПопис++
		if тренутноthreadПопис >= списак.Величина_2 {
			тренутноthreadПопис = 0
		}
		thread := (*TThread)(списак.Getat(тренутноthreadПопис))
		if thread != nil && thread.ThreadСтање != Blocked && thread.ThreadСтање != Заустављен {
			if schedulerИсправљање {
				конзола_2.MШтампај("ti:")
				конзола_2.MUnsignedinteger32Штампај(uint32(тренутноthreadПопис))
				конзола_2.MШтампај(":")
				конзола_2.MUnsignedinteger32Штампај(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.тренутноthread

}
func (исти *Scheduler) Додајthread(thread *TThread) {
	if thread == nil {
		return
	}
	списак.Append_to_list(uintptr(Pointer(thread)))
}
func Додајrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	списак.Append_to_list(uintptr(Pointer(thread)))
}

func ТренутноПИД() uint32 {
	if schedata.тренутноthread == nil || schedata.тренутноthread.ПИД == 0 {
		return 1
	}
	return schedata.тренутноthread.ПИД
}

func ТренутнонадређениПИД() uint32 {
	if schedata.тренутноthread == nil {
		return 0
	}
	return schedata.тренутноthread.НадређениПИД
}
func (исти *Scheduler) Уклониthread(thread *TThread) {
	списак.Уклони(uintptr(Pointer(thread)))
}

func (исти *Scheduler) Уклониthreadat(попис int) {
	списак.Уклониat(попис)
}

type Scheduler struct {
	TОметањеhandler
}

func (исти *Scheduler) Init(manager *TОметањеmanager, mem *mem.TМеморијаmanager, tss *Tssунос) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitУчестаност)

	списак = LinkedСписак{}
	списак.Init(mem)
	конзола_2.MШтампај("list:")
	конзола_2.MUnsignedinteger32Штампај(uint32(uintptr(Pointer(&списак))))

	ометањеhandler = ручкаОметање
	var address uintptr
	address = uintptr(Pointer(&ометањеhandler))
	исти.TОметањеhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (исти *Scheduler) Омогућено(омогућено bool) {
	schedata.Омогућено = омогућено
}

func initpit(учестаност uint32) {
	if учестаност == 0 {
		return
	}
	divisor := uint32(1193180) / учестаност
	ПортПишеbyte(0x43, 0x36)
	ПортПишеbyte(0x40, uint8(divisor&0xFF))
	ПортПишеbyte(0x40, uint8((divisor>>8)&0xFF))
}

func скупds(dssegment uint32)
func скупgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func повратиfpregs(buffer_2 uintptr)

var jmpКорисник uint32 = 0
var ометањеhandler func(uint32) uint32

func schedulestack(fn func())
func скупcr3(address uint32)
func getcr3() uint32

func ручкаОметање(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerИсправљање {
		конзола_2.MШтампајxy(([]byte)("sche1:"), 1, 17)

		конзола_2.MШтампај(":")
		конзола_2.MUnsignedinteger32Штампај(esp)
		конзола_2.MШтампај(":")

		конзола_2.MUnsignedinteger32Штампај(uint32(schedata.tickcount))
		конзола_2.MШтампај(":")
		конзола_2.MUnsignedinteger32Штампај(KernelheapПокрени)
	}

	if schedata.tickcount == schedata.учестаност {
		schedata.tickcount = 0

		if списак.Величина_2 > 0 && schedata.Омогућено == true {
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

			if esp >= KernelheapПокрени && schedata.тренутноthread != nil {
				schedata.тренутноthread.ПроцесорСтање = (*TcpuСтање)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.тренутноthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.тренутноthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerИсправљање {
					конзола_2.MШтампај(([]byte)("backup"))
					конзола_2.MUnsignedinteger32Штампај(esp)
				}
			}

			address := uintptr(Pointer(&(следећеthread.Fpubuffer)))
			offset := следећеthread.Fpuoffset
			if offset != 0xffffffff {
				повратиfpregs(address + offset)
				if schedulerИсправљање {
					конзола_2.MШтампај(([]byte)("restore"))
				}
			}

			schedata.тренутноthread = следећеthread

			if schedata.тренутноthread.ThreadСтање == Покренут {
				schedata.тренутноthread.ThreadСтање = Спреман

				InitialthreadКорисникjump(schedata.тренутноthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(следећеthread.ПроцесорСтање)))
			if следећеthread.Stack != 0 {
				schedata.tss.Скупstack(Segkerneldata, следећеthread.Stack+ThreadstackВеличина)
			}

			скупcr3(следећеthread.СТРАНАДиректоријумунос)
			скупgs(следећеthread.ПроцесорСтање.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func ИскључиЦелиброј()

func getesp() uint32
func threadИзлазloop()

func скупthreadИзлазloopСтање(процесорСтање *TcpuСтање) {
	процесорСтање.Eip = uint32(ValueOf(threadИзлазloop).Pointer())
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
		скупthreadИзлазloopСтање(процесорСтање)
		return процесорСтање
	}

	заустављенthread := schedata.тренутноthread
	for i := 0; i < списак.Величина_2; i++ {
		thread := (*TThread)(списак.Getat(i))
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
		скупthreadИзлазloopСтање(процесорСтање)
		return процесорСтање
	}

	schedata.тренутноthread = следећеthread
	if следећеthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Скупstack(Segkerneldata, следећеthread.Stack+ThreadstackВеличина)
	}
	скупcr3(следећеthread.СТРАНАДиректоријумунос)
	скупgs(следећеthread.ПроцесорСтање.Gs)
	return следећеthread.ПроцесорСтање
}

func InitialthreadКорисникjump(thread *TThread) {

	ИскључиЦелиброј()

	schedata.tss.Скупstack(Segkerneldata, thread.Stack+ThreadstackВеличина)

	скупcr3(thread.СТРАНАДиректоријумунос)
	скупgs(thread.ПроцесорСтање.Gs)

	schedata.тренутноthread = thread
	schedata.Омогућено = true

	eip := thread.ПроцесорСтање.Eip
	корисникesp := thread.Корисникstack_2 + thread.КорисникstackВеличина_2
	eflags := thread.ПроцесорСтање.Eflags
	cs := thread.ПроцесорСтање.Cs
	esp := schedata.tss.Getesp0()

	конзола_2.MШтампај(([]byte)("jump["))
	конзола_2.MUnsignedinteger32Штампај(eip)
	конзола_2.MШтампај(([]byte)(":"))
	конзола_2.MUnsignedinteger32Штампај(корисникesp)
	конзола_2.MШтампај(([]byte)(":"))
	конзола_2.MUnsignedinteger32Штампај(eflags)
	конзола_2.MШтампај(([]byte)(":"))
	конзола_2.MUnsignedinteger32Штампај(cs)
	конзола_2.MШтампај(([]byte)(":"))

	конзола_2.MUnsignedinteger32Штампај(esp)
	конзола_2.MШтампај(([]byte)("]"))

	userprocунос := thread.ПроцесорСтање.Ecx
	општеoffsetТабела_2 := thread.ПроцесорСтање.Edx
	растегљиво := thread.ПроцесорСтање.Esi

	ПортПишеbyte(0x20, 0x20)
	jumpusermodeiret(eip, корисникesp, eflags, userprocунос, општеoffsetТабела_2, растегљиво)
	конзола_2.MШтампај(([]byte)("usermode end"))
}
func штампајesp(esp uint32) {
	конзола_2.MШтампај(([]byte)("esp["))
	конзола_2.MUnsignedinteger32Штампај(esp)
}
