package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "порт"
import . "util/списък"

import . "прекъсване"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "паметmanager"

const SchedulerПовторяемост = 1
const KernelheapСтартиране = 1024 * 1024
const schedulerdebug = false
const pitПовторяемост = 100

var списък LinkedСписък

type Schedulerdata struct {
	повторяемост	uint32
	tickcount	uint32

	switchforced	bool

	Включена	bool

	текущадатаthread	*TThread
	tss			*Tssзапис
}

var schedata Schedulerdata = Schedulerdata{}

func (себеси *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.повторяемост = SchedulerПовторяемост
	schedata.текущадатаthread = nil
	schedata.Включена = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var текущадатаthreadСъдържание int = 0
var следващоПроцесИДЕНТИФИКАТОР uint32 = 1

func AllocateИдПр() uint32 {
	идПр := следващоПроцесИДЕНТИФИКАТОР
	следващоПроцесИДЕНТИФИКАТОР++
	return идПр
}

func (себеси *Schedulerdata) GetСледващоГотовоthread() *TThread {
	if списък.Размер_2 <= 0 {
		return nil
	}

	if schedata.текущадатаthread != nil {
		текущадатаthreadСъдържание = списък.Съдържаниеот(uintptr(Pointer(schedata.текущадатаthread)))
		if текущадатаthreadСъдържание < 0 {
			текущадатаthreadСъдържание = 0
		}
	} else {
		текущадатаthreadСъдържание = -1
	}

	for checked := 0; checked < списък.Размер_2; checked++ {
		текущадатаthreadСъдържание++
		if текущадатаthreadСъдържание >= списък.Размер_2 {
			текущадатаthreadСъдържание = 0
		}
		thread := (*TThread)(списък.Getat(текущадатаthreadСъдържание))
		if thread != nil && thread.ThreadСъстояние != Blocked && thread.ThreadСъстояние != Спрян {
			if schedulerdebug {
				console_2.MПечат("ti:")
				console_2.MUnsignedinteger32Печат(uint32(текущадатаthreadСъдържание))
				console_2.MПечат(":")
				console_2.MUnsignedinteger32Печат(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.текущадатаthread

}
func (себеси *Scheduler) Добавянеthread(thread *TThread) {
	if thread == nil {
		return
	}
	списък.Append_to_list(uintptr(Pointer(thread)))
}
func Добавянеrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	списък.Append_to_list(uintptr(Pointer(thread)))
}

func ТекущадатаИдПр() uint32 {
	if schedata.текущадатаthread == nil || schedata.текущадатаthread.ИдПр == 0 {
		return 1
	}
	return schedata.текущадатаthread.ИдПр
}

func ТекущадатародителИдПр() uint32 {
	if schedata.текущадатаthread == nil {
		return 0
	}
	return schedata.текущадатаthread.РодителИдПр
}
func (себеси *Scheduler) Премахванеthread(thread *TThread) {
	списък.Премахване(uintptr(Pointer(thread)))
}

func (себеси *Scheduler) Премахванеthreadat(съдържание int) {
	списък.Премахванеat(съдържание)
}

type Scheduler struct {
	TПрекъсванеhandler
}

func (себеси *Scheduler) Init(manager *TПрекъсванеmanager, mem *mem.TПаметmanager, tss *Tssзапис) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitПовторяемост)

	списък = LinkedСписък{}
	списък.Init(mem)
	console_2.MПечат("list:")
	console_2.MUnsignedinteger32Печат(uint32(uintptr(Pointer(&списък))))

	прекъсванеhandler = ръкохваткаПрекъсване
	var address uintptr
	address = uintptr(Pointer(&прекъсванеhandler))
	себеси.TПрекъсванеhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (себеси *Scheduler) Включена(включена bool) {
	schedata.Включена = включена
}

func initpit(повторяемост uint32) {
	if повторяемост == 0 {
		return
	}
	divisor := uint32(1193180) / повторяемост
	ПортПисанеbyte(0x43, 0x36)
	ПортПисанеbyte(0x40, uint8(divisor&0xFF))
	ПортПисанеbyte(0x40, uint8((divisor>>8)&0xFF))
}

func задайds(dssegment uint32)
func задайgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func възстановяванеfpregs(buffer_2 uintptr)

var jmpСобственик uint32 = 0
var прекъсванеhandler func(uint32) uint32

func schedulestack(fn func())
func задайcr3(address uint32)
func getcr3() uint32

func ръкохваткаПрекъсване(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MПечатxy(([]byte)("sche1:"), 1, 17)

		console_2.MПечат(":")
		console_2.MUnsignedinteger32Печат(esp)
		console_2.MПечат(":")

		console_2.MUnsignedinteger32Печат(uint32(schedata.tickcount))
		console_2.MПечат(":")
		console_2.MUnsignedinteger32Печат(KernelheapСтартиране)
	}

	if schedata.tickcount == schedata.повторяемост {
		schedata.tickcount = 0

		if списък.Размер_2 > 0 && schedata.Включена == true {
			var следващоthread = schedata.GetСледващоГотовоthread()
			if следващоthread == nil {
				return esp
			}
			if schedata.текущадатаthread == nil {
				MEmergencyЛогНиз("\nSCHED first esp=")
				MEmergencyЛогunsignedinteger32(esp)
				MEmergencyЛогНиз(" thread=")
				MEmergencyЛогunsignedinteger32(uint32(uintptr(Pointer(следващоthread))))
				MEmergencyЛогНиз(" cpu=")
				MEmergencyЛогunsignedinteger32(uint32(uintptr(Pointer(следващоthread.ПроцесорСъстояние))))
				MEmergencyЛогНиз(" state=")
				MEmergencyЛогunsignedinteger32(uint32(следващоthread.ThreadСъстояние))
				MEmergencyЛогНиз(" eip=")
				MEmergencyЛогunsignedinteger32(следващоthread.ПроцесорСъстояние.Eip)
				MEmergencyЛогНиз(" cs=")
				MEmergencyЛогunsignedinteger32(следващоthread.ПроцесорСъстояние.Cs)
				MEmergencyЛогНиз("\n")
			}

			if esp >= KernelheapСтартиране && schedata.текущадатаthread != nil {
				schedata.текущадатаthread.ПроцесорСъстояние = (*TcpuСъстояние)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.текущадатаthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.текущадатаthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MПечат(([]byte)("backup"))
					console_2.MUnsignedinteger32Печат(esp)
				}
			}

			address := uintptr(Pointer(&(следващоthread.Fpubuffer)))
			offset := следващоthread.Fpuoffset
			if offset != 0xffffffff {
				възстановяванеfpregs(address + offset)
				if schedulerdebug {
					console_2.MПечат(([]byte)("restore"))
				}
			}

			schedata.текущадатаthread = следващоthread

			if schedata.текущадатаthread.ThreadСъстояние == Стартиранна {
				schedata.текущадатаthread.ThreadСъстояние = Готово

				InitialthreadСобственикjump(schedata.текущадатаthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(следващоthread.ПроцесорСъстояние)))
			if следващоthread.Stack != 0 {
				schedata.tss.Задайstack(Segkerneldata, следващоthread.Stack+ThreadstackРазмер)
			}

			задайcr3(следващоthread.Страницапапказапис)
			задайgs(следващоthread.ПроцесорСъстояние.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func ИзключванеЦялочисло()

func getesp() uint32
func threadИзходloop()

func задайthreadИзходloopСъстояние(процесорСъстояние *TcpuСъстояние) {
	процесорСъстояние.Eip = uint32(ValueOf(threadИзходloop).Pointer())
	процесорСъстояние.Cs = Segkernelcode
	процесорСъстояние.Ds = Segkerneldata
	процесорСъстояние.Es = Segkerneldata
	процесорСъстояние.Fs = Segkerneldata
	процесорСъстояние.Gs = Segkernelgs
	процесорСъстояние.Ss = Segkerneldata
	процесорСъстояние.Eflags = 0x202
}

func СпиранеТекущадатаthread(процесорСъстояние *TcpuСъстояние) *TcpuСъстояние {
	if schedata.текущадатаthread == nil {
		задайthreadИзходloopСъстояние(процесорСъстояние)
		return процесорСъстояние
	}

	спрянthread := schedata.текущадатаthread
	for i := 0; i < списък.Размер_2; i++ {
		thread := (*TThread)(списък.Getat(i))
		if thread != nil && thread.ПроцесорСъстояние == процесорСъстояние {
			спрянthread = thread
			break
		}
	}
	спрянthread.ПроцесорСъстояние = процесорСъстояние
	спрянthread.ThreadСъстояние = Спрян
	schedata.текущадатаthread = спрянthread

	следващоthread := schedata.GetСледващоГотовоthread()
	if следващоthread == nil || следващоthread == спрянthread || следващоthread.ПроцесорСъстояние == nil || следващоthread.ПроцесорСъстояние == процесорСъстояние {
		задайthreadИзходloopСъстояние(процесорСъстояние)
		return процесорСъстояние
	}

	schedata.текущадатаthread = следващоthread
	if следващоthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Задайstack(Segkerneldata, следващоthread.Stack+ThreadstackРазмер)
	}
	задайcr3(следващоthread.Страницапапказапис)
	задайgs(следващоthread.ПроцесорСъстояние.Gs)
	return следващоthread.ПроцесорСъстояние
}

func InitialthreadСобственикjump(thread *TThread) {

	ИзключванеЦялочисло()

	schedata.tss.Задайstack(Segkerneldata, thread.Stack+ThreadstackРазмер)

	задайcr3(thread.Страницапапказапис)
	задайgs(thread.ПроцесорСъстояние.Gs)

	schedata.текущадатаthread = thread
	schedata.Включена = true

	eip := thread.ПроцесорСъстояние.Eip
	собственикesp := thread.Собственикstack_2 + thread.СобственикstackРазмер_2
	eflags := thread.ПроцесорСъстояние.Eflags
	cs := thread.ПроцесорСъстояние.Cs
	esp := schedata.tss.Getesp0()

	console_2.MПечат(([]byte)("jump["))
	console_2.MUnsignedinteger32Печат(eip)
	console_2.MПечат(([]byte)(":"))
	console_2.MUnsignedinteger32Печат(собственикesp)
	console_2.MПечат(([]byte)(":"))
	console_2.MUnsignedinteger32Печат(eflags)
	console_2.MПечат(([]byte)(":"))
	console_2.MUnsignedinteger32Печат(cs)
	console_2.MПечат(([]byte)(":"))

	console_2.MUnsignedinteger32Печат(esp)
	console_2.MПечат(([]byte)("]"))

	userprocзапис := thread.ПроцесорСъстояние.Ecx
	глобалноoffsetТаблица_2 := thread.ПроцесорСъстояние.Edx
	динамично := thread.ПроцесорСъстояние.Esi

	ПортПисанеbyte(0x20, 0x20)
	jumpusermodeiret(eip, собственикesp, eflags, userprocзапис, глобалноoffsetТаблица_2, динамично)
	console_2.MПечат(([]byte)("usermode end"))
}
func печатesp(esp uint32) {
	console_2.MПечат(([]byte)("esp["))
	console_2.MUnsignedinteger32Печат(esp)
}
