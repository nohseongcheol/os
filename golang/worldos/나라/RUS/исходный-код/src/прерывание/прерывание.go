/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Прерывание

import . "unsafe"
import . "reflect"

import . "порт"
import . "gdt"
import . "многоуправлениеЗадачами"
import . "консоль"

func прерываниеignore()

func прерываниеexceptionhandler()
func прерываниеexceptionhandler0x00()
func прерываниеexceptionhandler0x01()
func прерываниеexceptionhandler0x02()
func прерываниеexceptionhandler0x03()
func прерываниеexceptionhandler0x04()
func прерываниеexceptionhandler0x05()
func прерываниеexceptionhandler0x06()
func прерываниеexceptionhandler0x07()
func прерываниеexceptionhandler0x08()
func прерываниеexceptionhandler0x09()
func прерываниеexceptionhandler0x0a()
func прерываниеexceptionhandler0x0b()
func прерываниеexceptionhandler0x0c()
func прерываниеexceptionhandler0x0d()
func прерываниеexceptionhandler0x0e()
func прерываниеexceptionhandler0x0f()
func прерываниеexceptionhandler0x10()
func прерываниеexceptionhandler0x11()
func прерываниеexceptionhandler0x12()
func прерываниеexceptionhandler0x13()

func прерываниеrequesthandler0x00()
func прерываниеrequesthandler0x01()
func прерываниеrequesthandler0x02()
func прерываниеrequesthandler0x03()
func прерываниеrequesthandler0x04()
func прерываниеrequesthandler0x05()
func прерываниеrequesthandler0x06()
func прерываниеrequesthandler0x07()
func прерываниеrequesthandler0x08()
func прерываниеrequesthandler0x09()
func прерываниеrequesthandler0x0a()
func прерываниеrequesthandler0x0b()
func прерываниеrequesthandler0x0c()
func прерываниеrequesthandler0x0d()
func прерываниеrequesthandler0x0e()
func прерываниеrequesthandler0x0f()

func прерываниеrequesthandler0x80()
func прерываниеrequesthandler0x81()
func прерываниеrequesthandler0x82()

func ПроверитьПечать(позиция uint8, данные uint8)
func указатьds(dssegment uint32)
func указатьgs(gssegment uint32)
func прерываниеВыходloop()

type TПрерываниеhandler struct {
	ПрерываниеЧисло		uint8
	Прерываниедиспетчер	uintptr
}
type IПрерываниеhandler interface {
	Ручкапрерывание(uint32) uint32
}

func Новыйпрерываниеhandler(Прерываниедиспетчер uintptr, ПрерываниеЧисло uint8) *TПрерываниеhandler {
	прерываниеhandler_2 := new(TПрерываниеhandler)
	прерываниеhandler_2.ПрерываниеЧисло = ПрерываниеЧисло
	прерываниеhandler_2.Прерываниедиспетчер = Прерываниедиспетчер
	return прерываниеhandler_2

}

var handler_2 [256]uintptr

func (текущий *TПрерываниеhandler) Init(ПрерываниеЧисло uint8, Прерываниедиспетчер uintptr, funcaddress uintptr) {

	handler_2[ПрерываниеЧисло] = funcaddress

	текущий.ПрерываниеЧисло = ПрерываниеЧисло
	текущий.Прерываниедиспетчер = Прерываниедиспетчер

}
func (текущий *TПрерываниеhandler) УказатьРучкапрерываниеfuction(ПрерываниеЧисло uint32, address uintptr) {
	handler_2[ПрерываниеЧисло] = address
}
func (текущий *TПрерываниеhandler) Уничтожить() {
	текущийuintptr := uintptr(Pointer(текущий))
	Прерываниедиспетчер := (*TПрерываниедиспетчер)(Pointer(текущий.Прерываниедиспетчер))
	if текущийuintptr == Прерываниедиспетчер.Gethandler(текущий.ПрерываниеЧисло) {
		Прерываниедиспетчер.Указатьhandler(0, текущий.ПрерываниеЧисло)
	}

}
func (текущий *TПрерываниеhandler) Указатьпрерываниедиспетчер(Прерываниедиспетчер uintptr) {
}
func (текущий *TПрерываниеhandler) УказатьпрерываниеЧисло(ПрерываниеЧисло uint8) {
	текущий.ПрерываниеЧисло = ПрерываниеЧисло
}
func (текущий *TПрерываниеhandler) Ручкапрерывание(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	консоль_2 := TКонсоль{}
	консоль_2.MПечать(buffer)
	return esp
}
func Ручкапрерывание1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	консоль_2 := TКонсоль{}
	консоль_2.MПечать(buffer)
}

type TШлюзdescriptor struct {
	шлюзданные [8]uint8
}
type TПрерываниеdescriptorТаблицаУказатели struct {
}

var idtданные [256 * 8]uint8
var Активнопрерываниедиспетчер uintptr = 0

const прерываниеОтладка = false

type TПрерываниедиспетчер struct {
	handler_2	[256]uintptr

	оборудованиепрерываниеoffset	uint16

	задачадиспетчер	*TЗадачадиспетчер
}

var PrimarypicКомандаВводивыводпорт uint16 = 0x20
var PrimarypicданныеВводивыводпорт uint16 = 0x21
var SecondarypicКомандаВводивыводпорт uint16 = 0xA0
var SecondarypicданныеВводивыводпорт uint16 = 0xA1

func (текущий *TПрерываниедиспетчер) Init(оборудованиепрерываниеoffset uint16, глобальныеdescriptorТаблица *TShareddescriptorТаблица, задачадиспетчер *TЗадачадиспетчер) {

	текущий.задачадиспетчер = задачадиспетчер

	текущий.оборудованиепрерываниеoffset = оборудованиепрерываниеoffset
	codesegment := uint16(Segядроcode)

	for i := 0; i < (256 * 8); i++ {
		idtданные[i] = 0
	}
	var address uint32
	var Idtпрерываниешлюз uint8 = 0xE
	address = uint32(ValueOf(прерываниеignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(прерываниеexceptionhandler0x0f).Pointer())
		текущий.ПрерываниеdescriptorТаблицазаписьуказать(i, codesegment, address, 0, Idtпрерываниешлюз)
	}

	address = uint32(ValueOf(прерываниеexceptionhandler0x00).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x00, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x01).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x01, codesegment, address, 0, Idtпрерываниешлюз)
	address = uint32(ValueOf(прерываниеexceptionhandler0x02).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x02, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x03).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x03, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x04).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x04, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x05).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x05, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x06).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x06, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x07).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x07, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x08).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x08, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x09).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x09, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x0a).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x0A, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x0b).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x0B, codesegment, address, 0, Idtпрерываниешлюз)
	address = uint32(ValueOf(прерываниеexceptionhandler0x0c).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x0C, codesegment, address, 0, Idtпрерываниешлюз)
	address = uint32(ValueOf(прерываниеexceptionhandler0x0d).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x0D, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x0e).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x0E, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x0f).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x0F, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x10).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x10, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x11).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x11, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x12).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x12, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеexceptionhandler0x13).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x13, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x00).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x20, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x01).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x21, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x02).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x22, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x03).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x23, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x04).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x24, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x05).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x25, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x06).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x26, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x07).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x27, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x08).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x28, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x09).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x29, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x0a).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x2A, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x0b).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x2B, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x0c).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x2C, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x0d).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x2D, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x0e).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x2E, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x0f).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x2F, codesegment, address, 0, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x80).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x80, codesegment, address, 3, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x81).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x81, codesegment, address, 3, Idtпрерываниешлюз)

	address = uint32(ValueOf(прерываниеrequesthandler0x82).Pointer())
	текущий.ПрерываниеdescriptorТаблицазаписьуказать(0x82, codesegment, address, 3, Idtпрерываниешлюз)

	Портписатьбайт(PrimarypicКомандаВводивыводпорт, 0x11)
	Портписатьбайт(SecondarypicКомандаВводивыводпорт, 0x11)

	Портписатьбайт(PrimarypicданныеВводивыводпорт, 0x20)
	Портписатьбайт(SecondarypicданныеВводивыводпорт, 0x28)

	Портписатьбайт(PrimarypicданныеВводивыводпорт, 0x04)
	Портписатьбайт(SecondarypicданныеВводивыводпорт, 0x02)

	Портписатьбайт(PrimarypicданныеВводивыводпорт, 0x01)
	Портписатьбайт(SecondarypicданныеВводивыводпорт, 0x01)

	Портписатьбайт(PrimarypicданныеВводивыводпорт, 0xF8)
	Портписатьбайт(SecondarypicданныеВводивыводпорт, 0xEF)

	idtУказатели := [6]uint8{0, 0, 0, 0, 0, 0}
	размер := (*uint16)(Pointer(&idtУказатели[0]))
	(*размер) = (uint16)(Sizeof(idtданные) - 1)

	base := (*uint32)(Pointer(&idtУказатели[2]))
	(*base) = uint32(uintptr(Pointer(&idtданные)))

	Lidt(uintptr(Pointer(&idtУказатели)))
}
func Lidt(lidtaddr uintptr)

func (текущий *TПрерываниедиспетчер) ПрерываниеdescriptorТаблицазаписьуказать(прерывание int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptorтип uint8) {

	handleraddressНизкийбит := (*uint16)(Pointer(&idtданные[прерывание*8+0]))
	(*handleraddressНизкийбит) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtданные[прерывание*8+2]))
	(*gdtcodesegmentselector) = codesegment

	зарезервированная := (*uint8)(Pointer(&idtданные[прерывание*8+4]))
	(*зарезервированная) = 0

	var IdtdescriptorПрисутствует uint8 = 0x80
	доступ := (*uint8)(Pointer(&idtданные[прерывание*8+5]))
	(*доступ) = (IdtdescriptorПрисутствует | Descriptorтип | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressВысокийбит := (*uint16)(Pointer(&idtданные[прерывание*8+6]))
	(*handleraddressВысокийбит) = uint16((handler >> 16) & 0xFFFF)

}

func (текущий *TПрерываниедиспетчер) Указатьhandler(handler uintptr, ПрерываниеЧисло uint8) {
	handler_2[ПрерываниеЧисло] = handler
}
func (текущий *TПрерываниедиспетчер) Gethandler(ПрерываниеЧисло uint8) uintptr {
	return handler_2[ПрерываниеЧисло]
}
func (текущий *TПрерываниедиспетчер) DoРучкапрерывание(прерывание uint8, esp uint32) uint32 {

	if прерываниеОтладка {
		консоль_2.MПечатьxy("[esp:", 1, 20)
		консоль_2.MUnsignedinteger32Печать(uint32(прерывание))
		консоль_2.MПечать(":")
		консоль_2.MUnsignedinteger32Печать(esp)
	}
	handlerЗапустить := false
	if handler_2[прерывание] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[прерывание])))
		esp = myfunction(esp)
		handlerЗапустить = true

	}

	if !handlerЗапустить && прерывание == uint8(текущий.оборудованиепрерываниеoffset) && текущий.задачадиспетчер != nil {
		esp = uint32(uintptr(Pointer(текущий.задачадиспетчер.Schedule((*TcpuСостояние)(Pointer(uintptr(esp)))))))

	}
	if !handlerЗапустить && прерывание == 0x80 {
		esp = ручкаunhandledsyscall(esp)
	}

	if прерывание <= 0x1F {
	}
	if 0x20 <= прерывание && прерывание < 0x30 {
		if 0x28 <= прерывание {
			Портписатьбайт(SecondarypicКомандаВводивыводпорт, 0x20)
		}
		Портписатьбайт(PrimarypicКомандаВводивыводпорт, 0x20)
	}
	return esp
}

var количество2 uint8 = 1

func указатьcr3(address uint32)

var консоль_2 TКонсоль = TКонсоль{}

func Ручкапрерывание(esp uint32, прерывание uint32) uint32 {

	if прерываниеОтладка && прерывание != 0x80 && прерывание != 0x20 {
		консоль_2.MПечатьxy("[esp:", 1, 21)
		консоль_2.MUnsignedinteger32Печать(uint32(прерывание))
		консоль_2.MПечать(":")
		консоль_2.MUnsignedinteger32Печать(esp)
	}

	if Активнопрерываниедиспетчер != 0 {
		p := (*TПрерываниедиспетчер)(Pointer(Активнопрерываниедиспетчер))
		esp = p.DoРучкапрерывание(uint8(прерывание), esp)
		return esp
	}
	if handler_2[прерывание] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[прерывание])))
		esp = myfunction(esp)
	}
	if прерывание == 0x80 {
		return ручкаunhandledsyscall(esp)
	}
	if 0x20 <= прерывание && прерывание < 0x30 {
		if 0x28 <= прерывание {
			Портписатьбайт(SecondarypicКомандаВводивыводпорт, 0x20)
		}
		Портписатьбайт(PrimarypicКомандаВводивыводпорт, 0x20)
	}

	return esp
}

func ручкаunhandledsyscall(esp uint32) uint32 {
	цП := (*TcpuСостояние)(Pointer(uintptr(esp)))
	if цП.Eax == 1 || цП.Eax == 252 {
		цП.Eip = uint32(ValueOf(прерываниеВыходloop).Pointer())
		цП.Cs = Segядроcode
		цП.Ds = Segядроданные
		цП.Es = Segядроданные
		цП.Fs = Segядроданные
		цП.Gs = Segядроgs
		цП.Ss = Segядроданные
		цП.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasОшибкаcode(прерывание uint32) bool {
	switch прерывание {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionИмя(прерывание uint32) string {
	switch прерывание {
	case 0x00:
		return "#DE divide error"
	case 0x06:
		return "#UD invalid opcode"
	case 0x08:
		return "#DF double fault"
	case 0x0A:
		return "#TS invalid TSS"
	case 0x0B:
		return "#NP segment not present"
	case 0x0C:
		return "#SS stack fault"
	case 0x0D:
		return "#GP general protection"
	case 0x0E:
		return "#PF page fault"
	case 0x11:
		return "#AC alignment check"
	}
	return "#EX exception"
}

func exceptionкадрЗначение(кадр uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(кадр + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func печатьстраницаошибкаИнформация(ошибка uint32) {
	MEmergencyЖурналСтрока(" pf=[")
	if (ошибка & 0x01) != 0 {
		MEmergencyЖурналСтрока("protection")
	} else {
		MEmergencyЖурналСтрока("not-present")
	}
	if (ошибка & 0x02) != 0 {
		MEmergencyЖурналСтрока(",write")
	} else {
		MEmergencyЖурналСтрока(",read")
	}
	if (ошибка & 0x04) != 0 {
		MEmergencyЖурналСтрока(",user")
	} else {
		MEmergencyЖурналСтрока(",kernel")
	}
	if (ошибка & 0x08) != 0 {
		MEmergencyЖурналСтрока(",reserved-bit")
	}
	if (ошибка & 0x10) != 0 {
		MEmergencyЖурналСтрока(",instruction-fetch")
	}
	MEmergencyЖурналСтрока("]")
}

func печатьexceptionselectorИнформация(ошибка uint32) {
	MEmergencyЖурналСтрока(" selector=")
	MEmergencyЖурналunsignedinteger32(ошибка & 0xFFFFFFF8)
	MEmergencyЖурналСтрока(" index=")
	MEmergencyЖурналunsignedinteger32(ошибка >> 3)
	MEmergencyЖурналСтрока(" table=")
	if (ошибка & 0x02) != 0 {
		MEmergencyЖурналСтрока("IDT")
	} else if (ошибка & 0x04) != 0 {
		MEmergencyЖурналСтрока("LDT")
	} else {
		MEmergencyЖурналСтрока("GDT")
	}
	MEmergencyЖурналСтрока(" ext=")
	MEmergencyЖурналunsignedinteger32(ошибка & 0x01)
}

func Ручкаexception(esp uint32, прерывание uint32) uint32 {
	MEmergencyЖурналСтрока("\nEXCEPTION vec=")
	MEmergencyЖурналhexadecimal8(uint8(прерывание))
	MEmergencyЖурналСтрока(" ")
	MEmergencyЖурналСтрока(exceptionИмя(прерывание))
	MEmergencyЖурналСтрока(" frame=")
	MEmergencyЖурналunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyЖурналСтрока(" invalid-frame")
		if exceptionhasОшибкаcode(прерывание) {
			MEmergencyЖурналСтрока(" raw-error-or-bad-esp=")
			MEmergencyЖурналunsignedinteger32(esp)
			печатьexceptionselectorИнформация(esp)
		}
		MEmergencyЖурналСтрока("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var ошибка uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasОшибкаcode(прерывание) {
		ошибка = exceptionкадрЗначение(esp, 0)
		eipoffset = 4
	}
	eip := exceptionкадрЗначение(esp, eipoffset)
	cs := exceptionкадрЗначение(esp, eipoffset+4)
	eflags := exceptionкадрЗначение(esp, eipoffset+8)

	MEmergencyЖурналСтрока(" err=")
	MEmergencyЖурналunsignedinteger32(ошибка)
	MEmergencyЖурналСтрока(" eip=")
	MEmergencyЖурналunsignedinteger32(eip)
	MEmergencyЖурналСтрока(" cs=")
	MEmergencyЖурналunsignedinteger32(cs)
	MEmergencyЖурналСтрока(" eflags=")
	MEmergencyЖурналunsignedinteger32(eflags)
	MEmergencyЖурналСтрока(" cr0=")
	MEmergencyЖурналunsignedinteger32(exceptioncr0())
	MEmergencyЖурналСтрока(" cr3=")
	MEmergencyЖурналunsignedinteger32(exceptioncr3())

	if прерывание == 0x0E {
		MEmergencyЖурналСтрока(" cr2=")
		MEmergencyЖурналunsignedinteger32(exceptioncr2())
		печатьстраницаошибкаИнформация(ошибка)
	}

	if (cs & 0x03) != 0 {
		MEmergencyЖурналСтрока(" useresp=")
		MEmergencyЖурналunsignedinteger32(exceptionкадрЗначение(esp, eipoffset+12))
		MEmergencyЖурналСтрока(" ss=")
		MEmergencyЖурналunsignedinteger32(exceptionкадрЗначение(esp, eipoffset+16))
	}

	if exceptionhasОшибкаcode(прерывание) {
		печатьexceptionselectorИнформация(ошибка)
	}
	MEmergencyЖурналСтрока("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltПослеfatalexception()

func Ручкаfatalпрерываниекадр(сохраненоesp uint32, прерывание uint32) uint32 {
	Ручкаexception(сохраненоesp+52, прерывание)
	haltПослеfatalexception()
	return сохраненоesp
}

func ПрерываниеАктивно()
func (текущий *TПрерываниедиспетчер) Активно() {
	if Активнопрерываниедиспетчер != 0 {
		текущий.Deactive()
	}
	address := uintptr(Pointer(текущий))
	Активнопрерываниедиспетчер = address
	ПрерываниеАктивно()
}
func Прерываниеdeactive()
func (текущий *TПрерываниедиспетчер) Deactive() {
	Активнопрерываниедиспетчер = 0
	Прерываниеdeactive()
}

func MyРучкапрерывание(прерывание uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	консоль_2 := TКонсоль{}
	консоль_2.MПечать(buffer)
	return esp
}
func MyПроверить(прерывание uint8, esp uint32)

func Unhandleпрерывание() {
	buffer := []byte("unhandle interrupt\n")
	консоль_2 := TКонсоль{}
	консоль_2.MПечать(buffer)
}

func прерываниеhandler_2(прерывание uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	консоль_2 := TКонсоль{}
	консоль_2.MПечать(buffer)
	консоль_2.MHexadecimalПечать(0x40)
	return esp
}
func печатьesp(esp uint32) {
	консоль_2 := TКонсоль{}
	консоль_2.MUnsignedinteger32Печатьxy(esp, 20, 21)
}
func gettls() uint32
func Печатьtls() {

}
