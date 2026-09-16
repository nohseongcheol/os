/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "порт"
import . "util/спіс"

import . "перарыванне"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "памяцьmanager"

const SchedulerЧастата = 1
const KernelheapУключыць = 1024 * 1024
const schedulerdebug = false
const pitЧастата = 100

var спіс LinkedСпіс

type Schedulerdata struct {
	частата		uint32
	tickcount	uint32

	switchforced	bool

	Уключаны	bool

	дзейныthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.частата = SchedulerЧастата
	schedata.дзейныthread = nil
	schedata.Уключаны = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var дзейныthreadЗмест int = 0
var наступныПрацэсІДЭНТЫФІКАТАР uint32 = 1

func Allocatepid() uint32 {
	pid := наступныПрацэсІДЭНТЫФІКАТАР
	наступныПрацэсІДЭНТЫФІКАТАР++
	return pid
}

func (self *Schedulerdata) GetНаступныГатоваthread() *TThread {
	if спіс.Памер_2 <= 0 {
		return nil
	}

	if schedata.дзейныthread != nil {
		дзейныthreadЗмест = спіс.Зместз(uintptr(Pointer(schedata.дзейныthread)))
		if дзейныthreadЗмест < 0 {
			дзейныthreadЗмест = 0
		}
	} else {
		дзейныthreadЗмест = -1
	}

	for checked := 0; checked < спіс.Памер_2; checked++ {
		дзейныthreadЗмест++
		if дзейныthreadЗмест >= спіс.Памер_2 {
			дзейныthreadЗмест = 0
		}
		thread := (*TThread)(спіс.Getat(дзейныthreadЗмест))
		if thread != nil && thread.ThreadСтан != Blocked && thread.ThreadСтан != Спынены {
			if schedulerdebug {
				console_2.MДрукаваць("ti:")
				console_2.MUnsignedinteger32Друкаваць(uint32(дзейныthreadЗмест))
				console_2.MДрукаваць(":")
				console_2.MUnsignedinteger32Друкаваць(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.дзейныthread

}
func (self *Scheduler) Дадацьthread(thread *TThread) {
	if thread == nil {
		return
	}
	спіс.Append_to_list(uintptr(Pointer(thread)))
}
func Дадацьrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	спіс.Append_to_list(uintptr(Pointer(thread)))
}

func Дзейныpid() uint32 {
	if schedata.дзейныthread == nil || schedata.дзейныthread.Pid == 0 {
		return 1
	}
	return schedata.дзейныthread.Pid
}

func Дзейныparentpid() uint32 {
	if schedata.дзейныthread == nil {
		return 0
	}
	return schedata.дзейныthread.Parentpid
}
func (self *Scheduler) Выдаліцьthread(thread *TThread) {
	спіс.Выдаліць_2(uintptr(Pointer(thread)))
}

func (self *Scheduler) Выдаліцьthreadat(змест int) {
	спіс.Выдаліцьat(змест)
}

type Scheduler struct {
	TПерарываннеhandler
}

func (self *Scheduler) Init(manager *TПерарываннеmanager, mem *mem.TПамяцьmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitЧастата)

	спіс = LinkedСпіс{}
	спіс.Init(mem)
	console_2.MДрукаваць("list:")
	console_2.MUnsignedinteger32Друкаваць(uint32(uintptr(Pointer(&спіс))))

	перарываннеhandler = handleПерарыванне
	var address uintptr
	address = uintptr(Pointer(&перарываннеhandler))
	self.TПерарываннеhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Уключаны(уключаны bool) {
	schedata.Уключаны = уключаны
}

func initpit(частата uint32) {
	if частата == 0 {
		return
	}
	divisor := uint32(1193180) / частата
	ПортЗапісbyte(0x43, 0x36)
	ПортЗапісbyte(0x40, uint8(divisor&0xFF))
	ПортЗапісbyte(0x40, uint8((divisor>>8)&0xFF))
}

func вызначанаds(dssegment uint32)
func вызначанаgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func аднавіцьfpregs(buffer_2 uintptr)

var jmpКарыстальнік uint32 = 0
var перарываннеhandler func(uint32) uint32

func schedulestack(fn func())
func вызначанаcr3(address uint32)
func getcr3() uint32

func handleПерарыванне(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerdebug {
		console_2.MДрукавацьxy(([]byte)("sche1:"), 1, 17)

		console_2.MДрукаваць(":")
		console_2.MUnsignedinteger32Друкаваць(esp)
		console_2.MДрукаваць(":")

		console_2.MUnsignedinteger32Друкаваць(uint32(schedata.tickcount))
		console_2.MДрукаваць(":")
		console_2.MUnsignedinteger32Друкаваць(KernelheapУключыць)
	}

	if schedata.tickcount == schedata.частата {
		schedata.tickcount = 0

		if спіс.Памер_2 > 0 && schedata.Уключаны == true {
			var наступныthread = schedata.GetНаступныГатоваthread()
			if наступныthread == nil {
				return esp
			}
			if schedata.дзейныthread == nil {
				MEmergencylogРадок("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogРадок(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(наступныthread))))
				MEmergencylogРадок(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(наступныthread.ЦПСтан))))
				MEmergencylogРадок(" state=")
				MEmergencylogunsignedinteger32(uint32(наступныthread.ThreadСтан))
				MEmergencylogРадок(" eip=")
				MEmergencylogunsignedinteger32(наступныthread.ЦПСтан.Eip)
				MEmergencylogРадок(" cs=")
				MEmergencylogunsignedinteger32(наступныthread.ЦПСтан.Cs)
				MEmergencylogРадок("\n")
			}

			if esp >= KernelheapУключыць && schedata.дзейныthread != nil {
				schedata.дзейныthread.ЦПСтан = (*TcpuСтан)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.дзейныthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.дзейныthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MДрукаваць(([]byte)("backup"))
					console_2.MUnsignedinteger32Друкаваць(esp)
				}
			}

			address := uintptr(Pointer(&(наступныthread.Fpubuffer)))
			offset := наступныthread.Fpuoffset
			if offset != 0xffffffff {
				аднавіцьfpregs(address + offset)
				if schedulerdebug {
					console_2.MДрукаваць(([]byte)("restore"))
				}
			}

			schedata.дзейныthread = наступныthread

			if schedata.дзейныthread.ThreadСтан == Калізапушчаны {
				schedata.дзейныthread.ThreadСтан = Гатова

				InitialthreadКарыстальнікjump(schedata.дзейныthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(наступныthread.ЦПСтан)))
			if наступныthread.Stack != 0 {
				schedata.tss.Вызначанаstack(Segkerneldata, наступныthread.Stack+ThreadstackПамер)
			}

			вызначанаcr3(наступныthread.СтаронкаКаталогentry)
			вызначанаgs(наступныthread.ЦПСтан.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func ВыключыцьЦэлы()

func getesp() uint32
func threadВыхадloop()

func вызначанаthreadВыхадloopСтан(цПСтан *TcpuСтан) {
	цПСтан.Eip = uint32(ValueOf(threadВыхадloop).Pointer())
	цПСтан.Cs = Segkernelcode
	цПСтан.Ds = Segkerneldata
	цПСтан.Es = Segkerneldata
	цПСтан.Fs = Segkerneldata
	цПСтан.Gs = Segkernelgs
	цПСтан.Ss = Segkerneldata
	цПСтан.Eflags = 0x202
}

func СпыніцьДзейныthread(цПСтан *TcpuСтан) *TcpuСтан {
	if schedata.дзейныthread == nil {
		вызначанаthreadВыхадloopСтан(цПСтан)
		return цПСтан
	}

	спыненыthread := schedata.дзейныthread
	for i := 0; i < спіс.Памер_2; i++ {
		thread := (*TThread)(спіс.Getat(i))
		if thread != nil && thread.ЦПСтан == цПСтан {
			спыненыthread = thread
			break
		}
	}
	спыненыthread.ЦПСтан = цПСтан
	спыненыthread.ThreadСтан = Спынены
	schedata.дзейныthread = спыненыthread

	наступныthread := schedata.GetНаступныГатоваthread()
	if наступныthread == nil || наступныthread == спыненыthread || наступныthread.ЦПСтан == nil || наступныthread.ЦПСтан == цПСтан {
		вызначанаthreadВыхадloopСтан(цПСтан)
		return цПСтан
	}

	schedata.дзейныthread = наступныthread
	if наступныthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Вызначанаstack(Segkerneldata, наступныthread.Stack+ThreadstackПамер)
	}
	вызначанаcr3(наступныthread.СтаронкаКаталогentry)
	вызначанаgs(наступныthread.ЦПСтан.Gs)
	return наступныthread.ЦПСтан
}

func InitialthreadКарыстальнікjump(thread *TThread) {

	ВыключыцьЦэлы()

	schedata.tss.Вызначанаstack(Segkerneldata, thread.Stack+ThreadstackПамер)

	вызначанаcr3(thread.СтаронкаКаталогentry)
	вызначанаgs(thread.ЦПСтан.Gs)

	schedata.дзейныthread = thread
	schedata.Уключаны = true

	eip := thread.ЦПСтан.Eip
	карыстальнікesp := thread.Карыстальнікstack_2 + thread.КарыстальнікstackПамер_2
	eflags := thread.ЦПСтан.Eflags
	cs := thread.ЦПСтан.Cs
	esp := schedata.tss.Getesp0()

	console_2.MДрукаваць(([]byte)("jump["))
	console_2.MUnsignedinteger32Друкаваць(eip)
	console_2.MДрукаваць(([]byte)(":"))
	console_2.MUnsignedinteger32Друкаваць(карыстальнікesp)
	console_2.MДрукаваць(([]byte)(":"))
	console_2.MUnsignedinteger32Друкаваць(eflags)
	console_2.MДрукаваць(([]byte)(":"))
	console_2.MUnsignedinteger32Друкаваць(cs)
	console_2.MДрукаваць(([]byte)(":"))

	console_2.MUnsignedinteger32Друкаваць(esp)
	console_2.MДрукаваць(([]byte)("]"))

	userprocentry := thread.ЦПСтан.Ecx
	агульныяoffsetТабліца_2 := thread.ЦПСтан.Edx
	данамічна := thread.ЦПСтан.Esi

	ПортЗапісbyte(0x20, 0x20)
	jumpusermodeiret(eip, карыстальнікesp, eflags, userprocentry, агульныяoffsetТабліца_2, данамічна)
	console_2.MДрукаваць(([]byte)("usermode end"))
}
func друкавацьesp(esp uint32) {
	console_2.MДрукаваць(([]byte)("esp["))
	console_2.MUnsignedinteger32Друкаваць(esp)
}
