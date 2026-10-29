/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package планировщик

import . "unsafe"
import . "reflect"

import . "консоль"
import . "gdt"
import . "порт"
import . "утилита/список"

import . "прерывание"
import . "управлениеЗадачами/поток"
import . "управлениеЗадачами/tss"
import . "многоуправлениеЗадачами"
import mem "памятьдиспетчер"

const ПланировщикПовторяемость = 1
const ЯдроheapПуск = 1024 * 1024
const планировщикОтладка = false
const pitПовторяемость = 100

var список Linkedсписок

type Планировщикданные struct {
	повторяемость	uint32
	tickКоличество	uint32

	switchforced	bool

	Включено	bool

	текущаядатапоток	*TПоток
	tss			*Tssзапись
}

var scheданные Планировщикданные = Планировщикданные{}

func (текущий *Планировщикданные) Init() {
	scheданные.tickКоличество = 0
	scheданные.повторяемость = ПланировщикПовторяемость
	scheданные.текущаядатапоток = nil
	scheданные.Включено = false
	scheданные.switchforced = false

}

var консоль_2 = TКонсоль{}
var текущаядатапотокСодержание int = 0
var далеепроцессИДЕНТИФИКАТОР uint32 = 1

func Allocatepid() uint32 {
	pid := далеепроцессИДЕНТИФИКАТОР
	далеепроцессИДЕНТИФИКАТОР++
	return pid
}

func (текущий *Планировщикданные) GetДалееГотовопоток() *TПоток {
	if список.Размер_2 <= 0 {
		return nil
	}

	if scheданные.текущаядатапоток != nil {
		текущаядатапотокСодержание = список.Содержаниеиз(uintptr(Pointer(scheданные.текущаядатапоток)))
		if текущаядатапотокСодержание < 0 {
			текущаядатапотокСодержание = 0
		}
	} else {
		текущаядатапотокСодержание = -1
	}

	for checked := 0; checked < список.Размер_2; checked++ {
		текущаядатапотокСодержание++
		if текущаядатапотокСодержание >= список.Размер_2 {
			текущаядатапотокСодержание = 0
		}
		поток := (*TПоток)(список.Getat(текущаядатапотокСодержание))
		if поток != nil && поток.ПотокСостояние != Blocked && поток.ПотокСостояние != Остановлен {
			if планировщикОтладка {
				консоль_2.MПечать("ti:")
				консоль_2.MUnsignedinteger32Печать(uint32(текущаядатапотокСодержание))
				консоль_2.MПечать(":")
				консоль_2.MUnsignedinteger32Печать(uint32(uintptr(Pointer(поток))))
			}
			return поток
		}
	}
	return scheданные.текущаядатапоток

}
func (текущий *Планировщик) Добавитьпоток(поток *TПоток) {
	if поток == nil {
		return
	}
	список.Добавить_в_конец_списка(uintptr(Pointer(поток)))
}
func Добавитьrunnableпоток(поток *TПоток) {
	if поток == nil {
		return
	}
	список.Добавить_в_конец_списка(uintptr(Pointer(поток)))
}

func Текущаядатаpid() uint32 {
	if scheданные.текущаядатапоток == nil || scheданные.текущаядатапоток.Pid == 0 {
		return 1
	}
	return scheданные.текущаядатапоток.Pid
}

func Текущаядатародительpid() uint32 {
	if scheданные.текущаядатапоток == nil {
		return 0
	}
	return scheданные.текущаядатапоток.Родительpid
}
func (текущий *Планировщик) Удалитьпоток(поток *TПоток) {
	список.Удалить_2(uintptr(Pointer(поток)))
}

func (текущий *Планировщик) Удалитьпотокat(содержание int) {
	список.Удалитьat(содержание)
}

type Планировщик struct {
	TПрерываниеhandler
}

func (текущий *Планировщик) Init(диспетчер *TПрерываниедиспетчер, mem *mem.TПамятьдиспетчер, tss *Tssзапись) {
	scheданные.Init()
	scheданные.tss = tss
	initpit(pitПовторяемость)

	список = Linkedсписок{}
	список.Init(mem)
	консоль_2.MПечать("list:")
	консоль_2.MUnsignedinteger32Печать(uint32(uintptr(Pointer(&список))))

	прерываниеhandler = ручкапрерывание
	var address uintptr
	address = uintptr(Pointer(&прерываниеhandler))
	текущий.TПрерываниеhandler.Init(0x20, uintptr(Pointer(диспетчер)), address)
}

func (текущий *Планировщик) Включено(включено bool) {
	scheданные.Включено = включено
}

func initpit(повторяемость uint32) {
	if повторяемость == 0 {
		return
	}
	divisor := uint32(1193180) / повторяемость
	Портписатьбайт(0x43, 0x36)
	Портписатьбайт(0x40, uint8(divisor&0xFF))
	Портписатьбайт(0x40, uint8((divisor>>8)&0xFF))
}

func указатьds(dssegment uint32)
func указатьgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func восстановитьfpregs(buffer_2 uintptr)

var jmpпользователь uint32 = 0
var прерываниеhandler func(uint32) uint32

func schedulestack(fn func())
func указатьcr3(address uint32)
func getcr3() uint32

func ручкапрерывание(esp uint32) uint32 {

	scheданные.tickКоличество++

	if планировщикОтладка {
		консоль_2.MПечатьxy(([]byte)("sche1:"), 1, 17)

		консоль_2.MПечать(":")
		консоль_2.MUnsignedinteger32Печать(esp)
		консоль_2.MПечать(":")

		консоль_2.MUnsignedinteger32Печать(uint32(scheданные.tickКоличество))
		консоль_2.MПечать(":")
		консоль_2.MUnsignedinteger32Печать(ЯдроheapПуск)
	}

	if scheданные.tickКоличество == scheданные.повторяемость {
		scheданные.tickКоличество = 0

		if список.Размер_2 > 0 && scheданные.Включено == true {
			var далеепоток = scheданные.GetДалееГотовопоток()
			if далеепоток == nil {
				return esp
			}
			if scheданные.текущаядатапоток == nil {
				MEmergencyЖурналСтрока("\nSCHED first esp=")
				MEmergencyЖурналunsignedinteger32(esp)
				MEmergencyЖурналСтрока(" thread=")
				MEmergencyЖурналunsignedinteger32(uint32(uintptr(Pointer(далеепоток))))
				MEmergencyЖурналСтрока(" cpu=")
				MEmergencyЖурналunsignedinteger32(uint32(uintptr(Pointer(далеепоток.ЦПСостояние))))
				MEmergencyЖурналСтрока(" state=")
				MEmergencyЖурналunsignedinteger32(uint32(далеепоток.ПотокСостояние))
				MEmergencyЖурналСтрока(" eip=")
				MEmergencyЖурналunsignedinteger32(далеепоток.ЦПСостояние.Eip)
				MEmergencyЖурналСтрока(" cs=")
				MEmergencyЖурналunsignedinteger32(далеепоток.ЦПСостояние.Cs)
				MEmergencyЖурналСтрока("\n")
			}

			if esp >= ЯдроheapПуск && scheданные.текущаядатапоток != nil {
				scheданные.текущаядатапоток.ЦПСостояние = (*TcpuСостояние)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(scheданные.текущаядатапоток.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				scheданные.текущаядатапоток.Fpuoffset = offset
				backupfpregs(address + offset)
				if планировщикОтладка {
					консоль_2.MПечать(([]byte)("backup"))
					консоль_2.MUnsignedinteger32Печать(esp)
				}
			}

			address := uintptr(Pointer(&(далеепоток.Fpubuffer)))
			offset := далеепоток.Fpuoffset
			if offset != 0xffffffff {
				восстановитьfpregs(address + offset)
				if планировщикОтладка {
					консоль_2.MПечать(([]byte)("restore"))
				}
			}

			scheданные.текущаядатапоток = далеепоток

			if scheданные.текущаядатапоток.ПотокСостояние == Запущено {
				scheданные.текущаядатапоток.ПотокСостояние = Готово

				Initialпотокпользовательjump(scheданные.текущаядатапоток)
				return esp
			}

			esp = uint32(uintptr(Pointer(далеепоток.ЦПСостояние)))
			if далеепоток.Stack != 0 {
				scheданные.tss.Указатьstack(Segядроданные, далеепоток.Stack+ПотокstackРазмер)
			}

			указатьcr3(далеепоток.Страницакаталогзапись)
			указатьgs(далеепоток.ЦПСостояние.Gs)

		}

	}

	return esp
}

func jumpПользовательскийрежимiret(uint32, uint32, uint32, uint32, uint32, uint32)
func ОтключитьЦелое()

func getesp() uint32
func потокВыходloop()

func указатьпотокВыходloopСостояние(цПСостояние *TcpuСостояние) {
	цПСостояние.Eip = uint32(ValueOf(потокВыходloop).Pointer())
	цПСостояние.Cs = Segядроcode
	цПСостояние.Ds = Segядроданные
	цПСостояние.Es = Segядроданные
	цПСостояние.Fs = Segядроданные
	цПСостояние.Gs = Segядроgs
	цПСостояние.Ss = Segядроданные
	цПСостояние.Eflags = 0x202
}

func ОстановитьТекущаядатапоток(цПСостояние *TcpuСостояние) *TcpuСостояние {
	if scheданные.текущаядатапоток == nil {
		указатьпотокВыходloopСостояние(цПСостояние)
		return цПСостояние
	}

	остановленпоток := scheданные.текущаядатапоток
	for i := 0; i < список.Размер_2; i++ {
		поток := (*TПоток)(список.Getat(i))
		if поток != nil && поток.ЦПСостояние == цПСостояние {
			остановленпоток = поток
			break
		}
	}
	остановленпоток.ЦПСостояние = цПСостояние
	остановленпоток.ПотокСостояние = Остановлен
	scheданные.текущаядатапоток = остановленпоток

	далеепоток := scheданные.GetДалееГотовопоток()
	if далеепоток == nil || далеепоток == остановленпоток || далеепоток.ЦПСостояние == nil || далеепоток.ЦПСостояние == цПСостояние {
		указатьпотокВыходloopСостояние(цПСостояние)
		return цПСостояние
	}

	scheданные.текущаядатапоток = далеепоток
	if далеепоток.Stack != 0 && scheданные.tss != nil {
		scheданные.tss.Указатьstack(Segядроданные, далеепоток.Stack+ПотокstackРазмер)
	}
	указатьcr3(далеепоток.Страницакаталогзапись)
	указатьgs(далеепоток.ЦПСостояние.Gs)
	return далеепоток.ЦПСостояние
}

func Initialпотокпользовательjump(поток *TПоток) {

	ОтключитьЦелое()

	scheданные.tss.Указатьstack(Segядроданные, поток.Stack+ПотокstackРазмер)

	указатьcr3(поток.Страницакаталогзапись)
	указатьgs(поток.ЦПСостояние.Gs)

	scheданные.текущаядатапоток = поток
	scheданные.Включено = true

	eip := поток.ЦПСостояние.Eip
	пользовательesp := поток.Пользовательstack_2 + поток.ПользовательstackРазмер_2
	eflags := поток.ЦПСостояние.Eflags
	cs := поток.ЦПСостояние.Cs
	esp := scheданные.tss.Getesp0()

	консоль_2.MПечать(([]byte)("jump["))
	консоль_2.MUnsignedinteger32Печать(eip)
	консоль_2.MПечать(([]byte)(":"))
	консоль_2.MUnsignedinteger32Печать(пользовательesp)
	консоль_2.MПечать(([]byte)(":"))
	консоль_2.MUnsignedinteger32Печать(eflags)
	консоль_2.MПечать(([]byte)(":"))
	консоль_2.MUnsignedinteger32Печать(cs)
	консоль_2.MПечать(([]byte)(":"))

	консоль_2.MUnsignedinteger32Печать(esp)
	консоль_2.MПечать(([]byte)("]"))

	userprocзапись := поток.ЦПСостояние.Ecx
	глобальныеoffsetТаблица_2 := поток.ЦПСостояние.Edx
	динамически := поток.ЦПСостояние.Esi

	Портписатьбайт(0x20, 0x20)
	jumpПользовательскийрежимiret(eip, пользовательesp, eflags, userprocзапись, глобальныеoffsetТаблица_2, динамически)
	консоль_2.MПечать(([]byte)("usermode end"))
}
func печатьesp(esp uint32) {
	консоль_2.MПечать(([]byte)("esp["))
	консоль_2.MUnsignedinteger32Печать(esp)
}
