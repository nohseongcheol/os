package scheduler

import . "unsafe"
import . "reflect"

import . "консоль"
import . "gdt"
import . "порт"
import . "util/перелік"

import . "переривання"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "памятьmanager"

const SchedulerЧастота = 1
const KernelheapЗапустити = 1024 * 1024
const schedulerДіагностика = false
const pitЧастота = 100

var перелік LinkedПерелік

type Schedulerdata struct {
	частота		uint32
	tickВідлік	uint32

	switchforced	bool

	Включено	bool

	поточнаthread	*TThread
	tss		*Tssзапис
}

var schedata Schedulerdata = Schedulerdata{}

func (поточний *Schedulerdata) Init() {
	schedata.tickВідлік = 0
	schedata.частота = SchedulerЧастота
	schedata.поточнаthread = nil
	schedata.Включено = false
	schedata.switchforced = false

}

var консоль_2 = TКонсоль{}
var поточнаthreadІндекс int = 0
var наступнеПроцесиІДЕНТИФІКАТОР uint32 = 1

func AllocateІдентифікаторPID() uint32 {
	ідентифікаторPID := наступнеПроцесиІДЕНТИФІКАТОР
	наступнеПроцесиІДЕНТИФІКАТОР++
	return ідентифікаторPID
}

func (поточний *Schedulerdata) GetНаступнеГотовоthread() *TThread {
	if перелік.Розмір_2 <= 0 {
		return nil
	}

	if schedata.поточнаthread != nil {
		поточнаthreadІндекс = перелік.Індексз(uintptr(Pointer(schedata.поточнаthread)))
		if поточнаthreadІндекс < 0 {
			поточнаthreadІндекс = 0
		}
	} else {
		поточнаthreadІндекс = -1
	}

	for checked := 0; checked < перелік.Розмір_2; checked++ {
		поточнаthreadІндекс++
		if поточнаthreadІндекс >= перелік.Розмір_2 {
			поточнаthreadІндекс = 0
		}
		thread := (*TThread)(перелік.Getat(поточнаthreadІндекс))
		if thread != nil && thread.ThreadСтан != Blocked && thread.ThreadСтан != Зупинено {
			if schedulerДіагностика {
				консоль_2.MДрук("ti:")
				консоль_2.MUnsignedinteger32Друк(uint32(поточнаthreadІндекс))
				консоль_2.MДрук(":")
				консоль_2.MUnsignedinteger32Друк(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.поточнаthread

}
func (поточний *Scheduler) Додатиthread(thread *TThread) {
	if thread == nil {
		return
	}
	перелік.Додати_в_кінець_списку(uintptr(Pointer(thread)))
}
func Додатиrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	перелік.Додати_в_кінець_списку(uintptr(Pointer(thread)))
}

func ПоточнаІдентифікаторPID() uint32 {
	if schedata.поточнаthread == nil || schedata.поточнаthread.ІдентифікаторPID == 0 {
		return 1
	}
	return schedata.поточнаthread.ІдентифікаторPID
}

func ПоточнабатькоІдентифікаторPID() uint32 {
	if schedata.поточнаthread == nil {
		return 0
	}
	return schedata.поточнаthread.БатькоІдентифікаторPID
}
func (поточний *Scheduler) Вилучитиthread(thread *TThread) {
	перелік.Вилучити_2(uintptr(Pointer(thread)))
}

func (поточний *Scheduler) Вилучитиthreadat(індекс int) {
	перелік.Вилучитиat(індекс)
}

type Scheduler struct {
	TПерериванняhandler
}

func (поточний *Scheduler) Init(manager *TПерериванняmanager, mem *mem.TПамятьmanager, tss *Tssзапис) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitЧастота)

	перелік = LinkedПерелік{}
	перелік.Init(mem)
	консоль_2.MДрук("list:")
	консоль_2.MUnsignedinteger32Друк(uint32(uintptr(Pointer(&перелік))))

	перериванняhandler = елементкеруванняПереривання
	var адреса uintptr
	адреса = uintptr(Pointer(&перериванняhandler))
	поточний.TПерериванняhandler.Init(0x20, uintptr(Pointer(manager)), адреса)
}

func (поточний *Scheduler) Включено(включено bool) {
	schedata.Включено = включено
}

func initpit(частота uint32) {
	if частота == 0 {
		return
	}
	divisor := uint32(1193180) / частота
	ПортЗаписbyte(0x43, 0x36)
	ПортЗаписbyte(0x40, uint8(divisor&0xFF))
	ПортЗаписbyte(0x40, uint8((divisor>>8)&0xFF))
}

func множинаds(dssegment uint32)
func множинаgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func відновитиfpregs(buffer_2 uintptr)

var jmpКористувач uint32 = 0
var перериванняhandler func(uint32) uint32

func schedulestack(fn func())
func множинаcr3(адреса uint32)
func getcr3() uint32

func елементкеруванняПереривання(esp uint32) uint32 {

	schedata.tickВідлік++

	if schedulerДіагностика {
		консоль_2.MДрукxy(([]byte)("sche1:"), 1, 17)

		консоль_2.MДрук(":")
		консоль_2.MUnsignedinteger32Друк(esp)
		консоль_2.MДрук(":")

		консоль_2.MUnsignedinteger32Друк(uint32(schedata.tickВідлік))
		консоль_2.MДрук(":")
		консоль_2.MUnsignedinteger32Друк(KernelheapЗапустити)
	}

	if schedata.tickВідлік == schedata.частота {
		schedata.tickВідлік = 0

		if перелік.Розмір_2 > 0 && schedata.Включено == true {
			var наступнеthread = schedata.GetНаступнеГотовоthread()
			if наступнеthread == nil {
				return esp
			}
			if schedata.поточнаthread == nil {
				MEmergencyЖурналРядок("\nSCHED first esp=")
				MEmergencyЖурналunsignedinteger32(esp)
				MEmergencyЖурналРядок(" thread=")
				MEmergencyЖурналunsignedinteger32(uint32(uintptr(Pointer(наступнеthread))))
				MEmergencyЖурналРядок(" cpu=")
				MEmergencyЖурналunsignedinteger32(uint32(uintptr(Pointer(наступнеthread.ПроцесорСтан))))
				MEmergencyЖурналРядок(" state=")
				MEmergencyЖурналunsignedinteger32(uint32(наступнеthread.ThreadСтан))
				MEmergencyЖурналРядок(" eip=")
				MEmergencyЖурналunsignedinteger32(наступнеthread.ПроцесорСтан.Eip)
				MEmergencyЖурналРядок(" cs=")
				MEmergencyЖурналunsignedinteger32(наступнеthread.ПроцесорСтан.Cs)
				MEmergencyЖурналРядок("\n")
			}

			if esp >= KernelheapЗапустити && schedata.поточнаthread != nil {
				schedata.поточнаthread.ПроцесорСтан = (*TcpuСтан)(Pointer(uintptr(esp)))

				адреса := uintptr(Pointer(&(schedata.поточнаthread.Fpubuffer)))
				offset := (16 - (адреса % 16)) & 0xF
				schedata.поточнаthread.Fpuoffset = offset
				backupfpregs(адреса + offset)
				if schedulerДіагностика {
					консоль_2.MДрук(([]byte)("backup"))
					консоль_2.MUnsignedinteger32Друк(esp)
				}
			}

			адреса := uintptr(Pointer(&(наступнеthread.Fpubuffer)))
			offset := наступнеthread.Fpuoffset
			if offset != 0xffffffff {
				відновитиfpregs(адреса + offset)
				if schedulerДіагностика {
					консоль_2.MДрук(([]byte)("restore"))
				}
			}

			schedata.поточнаthread = наступнеthread

			if schedata.поточнаthread.ThreadСтан == Запущено {
				schedata.поточнаthread.ThreadСтан = Готово

				InitialthreadКористувачjump(schedata.поточнаthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(наступнеthread.ПроцесорСтан)))
			if наступнеthread.Stack != 0 {
				schedata.tss.Множинаstack(Segkerneldata, наступнеthread.Stack+ThreadstackРозмір)
			}

			множинаcr3(наступнеthread.СторінкаТеказапис)
			множинаgs(наступнеthread.ПроцесорСтан.Gs)

		}

	}

	return esp
}

func jumpРежимкористувачаiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Вимкнутиint()

func getesp() uint32
func threadВийтиloop()

func множинаthreadВийтиloopСтан(процесорСтан *TcpuСтан) {
	процесорСтан.Eip = uint32(ValueOf(threadВийтиloop).Pointer())
	процесорСтан.Cs = Segkernelcode
	процесорСтан.Ds = Segkerneldata
	процесорСтан.Es = Segkerneldata
	процесорСтан.Fs = Segkerneldata
	процесорСтан.Gs = Segkernelgs
	процесорСтан.Ss = Segkerneldata
	процесорСтан.Eflags = 0x202
}

func ЗупинитиПоточнаthread(процесорСтан *TcpuСтан) *TcpuСтан {
	if schedata.поточнаthread == nil {
		множинаthreadВийтиloopСтан(процесорСтан)
		return процесорСтан
	}

	зупиненоthread := schedata.поточнаthread
	for i := 0; i < перелік.Розмір_2; i++ {
		thread := (*TThread)(перелік.Getat(i))
		if thread != nil && thread.ПроцесорСтан == процесорСтан {
			зупиненоthread = thread
			break
		}
	}
	зупиненоthread.ПроцесорСтан = процесорСтан
	зупиненоthread.ThreadСтан = Зупинено
	schedata.поточнаthread = зупиненоthread

	наступнеthread := schedata.GetНаступнеГотовоthread()
	if наступнеthread == nil || наступнеthread == зупиненоthread || наступнеthread.ПроцесорСтан == nil || наступнеthread.ПроцесорСтан == процесорСтан {
		множинаthreadВийтиloopСтан(процесорСтан)
		return процесорСтан
	}

	schedata.поточнаthread = наступнеthread
	if наступнеthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Множинаstack(Segkerneldata, наступнеthread.Stack+ThreadstackРозмір)
	}
	множинаcr3(наступнеthread.СторінкаТеказапис)
	множинаgs(наступнеthread.ПроцесорСтан.Gs)
	return наступнеthread.ПроцесорСтан
}

func InitialthreadКористувачjump(thread *TThread) {

	Вимкнутиint()

	schedata.tss.Множинаstack(Segkerneldata, thread.Stack+ThreadstackРозмір)

	множинаcr3(thread.СторінкаТеказапис)
	множинаgs(thread.ПроцесорСтан.Gs)

	schedata.поточнаthread = thread
	schedata.Включено = true

	eip := thread.ПроцесорСтан.Eip
	користувачesp := thread.Користувачstack_2 + thread.КористувачstackРозмір_2
	eflags := thread.ПроцесорСтан.Eflags
	cs := thread.ПроцесорСтан.Cs
	esp := schedata.tss.Getesp0()

	консоль_2.MДрук(([]byte)("jump["))
	консоль_2.MUnsignedinteger32Друк(eip)
	консоль_2.MДрук(([]byte)(":"))
	консоль_2.MUnsignedinteger32Друк(користувачesp)
	консоль_2.MДрук(([]byte)(":"))
	консоль_2.MUnsignedinteger32Друк(eflags)
	консоль_2.MДрук(([]byte)(":"))
	консоль_2.MUnsignedinteger32Друк(cs)
	консоль_2.MДрук(([]byte)(":"))

	консоль_2.MUnsignedinteger32Друк(esp)
	консоль_2.MДрук(([]byte)("]"))

	userprocзапис := thread.ПроцесорСтан.Ecx
	глобальніoffsetТаблиця_2 := thread.ПроцесорСтан.Edx
	динамічно := thread.ПроцесорСтан.Esi

	ПортЗаписbyte(0x20, 0x20)
	jumpРежимкористувачаiret(eip, користувачesp, eflags, userprocзапис, глобальніoffsetТаблиця_2, динамічно)
	консоль_2.MДрук(([]byte)("usermode end"))
}
func друкesp(esp uint32) {
	консоль_2.MДрук(([]byte)("esp["))
	консоль_2.MUnsignedinteger32Друк(esp)
}
