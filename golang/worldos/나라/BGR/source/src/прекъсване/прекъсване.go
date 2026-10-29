/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Прекъсване

import . "unsafe"
import . "reflect"

import . "порт"
import . "gdt"
import . "multitasking"
import . "console"

func прекъсванеignore()

func прекъсванеexceptionhandler()
func прекъсванеexceptionhandler0x00()
func прекъсванеexceptionhandler0x01()
func прекъсванеexceptionhandler0x02()
func прекъсванеexceptionhandler0x03()
func прекъсванеexceptionhandler0x04()
func прекъсванеexceptionhandler0x05()
func прекъсванеexceptionhandler0x06()
func прекъсванеexceptionhandler0x07()
func прекъсванеexceptionhandler0x08()
func прекъсванеexceptionhandler0x09()
func прекъсванеexceptionhandler0x0a()
func прекъсванеexceptionhandler0x0b()
func прекъсванеexceptionhandler0x0c()
func прекъсванеexceptionhandler0x0d()
func прекъсванеexceptionhandler0x0e()
func прекъсванеexceptionhandler0x0f()
func прекъсванеexceptionhandler0x10()
func прекъсванеexceptionhandler0x11()
func прекъсванеexceptionhandler0x12()
func прекъсванеexceptionhandler0x13()

func прекъсванеrequesthandler0x00()
func прекъсванеrequesthandler0x01()
func прекъсванеrequesthandler0x02()
func прекъсванеrequesthandler0x03()
func прекъсванеrequesthandler0x04()
func прекъсванеrequesthandler0x05()
func прекъсванеrequesthandler0x06()
func прекъсванеrequesthandler0x07()
func прекъсванеrequesthandler0x08()
func прекъсванеrequesthandler0x09()
func прекъсванеrequesthandler0x0a()
func прекъсванеrequesthandler0x0b()
func прекъсванеrequesthandler0x0c()
func прекъсванеrequesthandler0x0d()
func прекъсванеrequesthandler0x0e()
func прекъсванеrequesthandler0x0f()

func прекъсванеrequesthandler0x80()
func прекъсванеrequesthandler0x81()
func прекъсванеrequesthandler0x82()

func ТестПечат(позиция uint8, data uint8)
func задайds(dssegment uint32)
func задайgs(gssegment uint32)
func прекъсванеИзходloop()

type TПрекъсванеhandler struct {
	ПрекъсванеЧисло		uint8
	Прекъсванеmanager	uintptr
}
type IПрекъсванеhandler interface {
	РъкохваткаПрекъсване(uint32) uint32
}

func НовПрекъсванеhandler(Прекъсванеmanager uintptr, ПрекъсванеЧисло uint8) *TПрекъсванеhandler {
	прекъсванеhandler_2 := new(TПрекъсванеhandler)
	прекъсванеhandler_2.ПрекъсванеЧисло = ПрекъсванеЧисло
	прекъсванеhandler_2.Прекъсванеmanager = Прекъсванеmanager
	return прекъсванеhandler_2

}

var handler_2 [256]uintptr

func (себеси *TПрекъсванеhandler) Init(ПрекъсванеЧисло uint8, Прекъсванеmanager uintptr, funcaddress uintptr) {

	handler_2[ПрекъсванеЧисло] = funcaddress

	себеси.ПрекъсванеЧисло = ПрекъсванеЧисло
	себеси.Прекъсванеmanager = Прекъсванеmanager

}
func (себеси *TПрекъсванеhandler) ЗадайРъкохваткаПрекъсванеfuction(ПрекъсванеЧисло uint32, address uintptr) {
	handler_2[ПрекъсванеЧисло] = address
}
func (себеси *TПрекъсванеhandler) Унищожаване() {
	себесиuintptr := uintptr(Pointer(себеси))
	Прекъсванеmanager := (*TПрекъсванеmanager)(Pointer(себеси.Прекъсванеmanager))
	if себесиuintptr == Прекъсванеmanager.Gethandler(себеси.ПрекъсванеЧисло) {
		Прекъсванеmanager.Задайhandler(0, себеси.ПрекъсванеЧисло)
	}

}
func (себеси *TПрекъсванеhandler) ЗадайПрекъсванеmanager(Прекъсванеmanager uintptr) {
}
func (себеси *TПрекъсванеhandler) ЗадайПрекъсванеЧисло(ПрекъсванеЧисло uint8) {
	себеси.ПрекъсванеЧисло = ПрекъсванеЧисло
}
func (себеси *TПрекъсванеhandler) РъкохваткаПрекъсване(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MПечат(buffer)
	return esp
}
func РъкохваткаПрекъсване1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MПечат(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TПрекъсванеdescriptorТаблицаПоказалци struct {
}

var idtdata [256 * 8]uint8
var АктивнаПрекъсванеmanager uintptr = 0

const прекъсванеdebug = false

type TПрекъсванеmanager struct {
	handler_2	[256]uintptr

	хардуерПрекъсванеoffset	uint16

	задачаmanager	*TЗадачаmanager
}

var PrimarypicКомандаioПорт uint16 = 0x20
var PrimarypicdataioПорт uint16 = 0x21
var SecondarypicКомандаioПорт uint16 = 0xA0
var SecondarypicdataioПорт uint16 = 0xA1

func (себеси *TПрекъсванеmanager) Init(хардуерПрекъсванеoffset uint16, глобалноdescriptorТаблица *TShareddescriptorТаблица, задачаmanager *TЗадачаmanager) {

	себеси.задачаmanager = задачаmanager

	себеси.хардуерПрекъсванеoffset = хардуерПрекъсванеoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtПрекъсванеgate uint8 = 0xE
	address = uint32(ValueOf(прекъсванеignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(прекъсванеexceptionhandler0x0f).Pointer())
		себеси.ПрекъсванеdescriptorТаблицазаписЗадай(i, codesegment, address, 0, IdtПрекъсванеgate)
	}

	address = uint32(ValueOf(прекъсванеexceptionhandler0x00).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x00, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x01).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x01, codesegment, address, 0, IdtПрекъсванеgate)
	address = uint32(ValueOf(прекъсванеexceptionhandler0x02).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x02, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x03).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x03, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x04).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x04, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x05).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x05, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x06).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x06, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x07).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x07, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x08).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x08, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x09).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x09, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x0a).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x0A, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x0b).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x0B, codesegment, address, 0, IdtПрекъсванеgate)
	address = uint32(ValueOf(прекъсванеexceptionhandler0x0c).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x0C, codesegment, address, 0, IdtПрекъсванеgate)
	address = uint32(ValueOf(прекъсванеexceptionhandler0x0d).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x0D, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x0e).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x0E, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x0f).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x0F, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x10).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x10, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x11).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x11, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x12).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x12, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеexceptionhandler0x13).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x13, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x00).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x20, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x01).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x21, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x02).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x22, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x03).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x23, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x04).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x24, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x05).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x25, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x06).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x26, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x07).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x27, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x08).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x28, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x09).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x29, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x0a).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x2A, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x0b).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x2B, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x0c).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x2C, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x0d).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x2D, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x0e).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x2E, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x0f).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x2F, codesegment, address, 0, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x80).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x80, codesegment, address, 3, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x81).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x81, codesegment, address, 3, IdtПрекъсванеgate)

	address = uint32(ValueOf(прекъсванеrequesthandler0x82).Pointer())
	себеси.ПрекъсванеdescriptorТаблицазаписЗадай(0x82, codesegment, address, 3, IdtПрекъсванеgate)

	ПортПисанеbyte(PrimarypicКомандаioПорт, 0x11)
	ПортПисанеbyte(SecondarypicКомандаioПорт, 0x11)

	ПортПисанеbyte(PrimarypicdataioПорт, 0x20)
	ПортПисанеbyte(SecondarypicdataioПорт, 0x28)

	ПортПисанеbyte(PrimarypicdataioПорт, 0x04)
	ПортПисанеbyte(SecondarypicdataioПорт, 0x02)

	ПортПисанеbyte(PrimarypicdataioПорт, 0x01)
	ПортПисанеbyte(SecondarypicdataioПорт, 0x01)

	ПортПисанеbyte(PrimarypicdataioПорт, 0xF8)
	ПортПисанеbyte(SecondarypicdataioПорт, 0xEF)

	idtПоказалци := [6]uint8{0, 0, 0, 0, 0, 0}
	размер := (*uint16)(Pointer(&idtПоказалци[0]))
	(*размер) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtПоказалци[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtПоказалци)))
}
func Lidt(lidtaddr uintptr)

func (себеси *TПрекъсванеmanager) ПрекъсванеdescriptorТаблицазаписЗадай(прекъсване int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorТип uint8) {

	handleraddressНисъкбита := (*uint16)(Pointer(&idtdata[прекъсване*8+0]))
	(*handleraddressНисъкбита) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[прекъсване*8+2]))
	(*gdtcodesegmentselector) = codesegment

	резервирано := (*uint8)(Pointer(&idtdata[прекъсване*8+4]))
	(*резервирано) = 0

	var IdtdescriptorНалична uint8 = 0x80
	достъп := (*uint8)(Pointer(&idtdata[прекъсване*8+5]))
	(*достъп) = (IdtdescriptorНалична | DescriptorТип | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressВисокбита := (*uint16)(Pointer(&idtdata[прекъсване*8+6]))
	(*handleraddressВисокбита) = uint16((handler >> 16) & 0xFFFF)

}

func (себеси *TПрекъсванеmanager) Задайhandler(handler uintptr, ПрекъсванеЧисло uint8) {
	handler_2[ПрекъсванеЧисло] = handler
}
func (себеси *TПрекъсванеmanager) Gethandler(ПрекъсванеЧисло uint8) uintptr {
	return handler_2[ПрекъсванеЧисло]
}
func (себеси *TПрекъсванеmanager) DoРъкохваткаПрекъсване(прекъсване uint8, esp uint32) uint32 {

	if прекъсванеdebug {
		console_2.MПечатxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Печат(uint32(прекъсване))
		console_2.MПечат(":")
		console_2.MUnsignedinteger32Печат(esp)
	}
	handlerСтарт := false
	if handler_2[прекъсване] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[прекъсване])))
		esp = myfunction(esp)
		handlerСтарт = true

	}

	if !handlerСтарт && прекъсване == uint8(себеси.хардуерПрекъсванеoffset) && себеси.задачаmanager != nil {
		esp = uint32(uintptr(Pointer(себеси.задачаmanager.Schedule((*TcpuСъстояние)(Pointer(uintptr(esp)))))))

	}
	if !handlerСтарт && прекъсване == 0x80 {
		esp = ръкохваткаunhandledsyscall(esp)
	}

	if прекъсване <= 0x1F {
	}
	if 0x20 <= прекъсване && прекъсване < 0x30 {
		if 0x28 <= прекъсване {
			ПортПисанеbyte(SecondarypicКомандаioПорт, 0x20)
		}
		ПортПисанеbyte(PrimarypicКомандаioПорт, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func задайcr3(address uint32)

var console_2 TConsole = TConsole{}

func РъкохваткаПрекъсване(esp uint32, прекъсване uint32) uint32 {

	if прекъсванеdebug && прекъсване != 0x80 && прекъсване != 0x20 {
		console_2.MПечатxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Печат(uint32(прекъсване))
		console_2.MПечат(":")
		console_2.MUnsignedinteger32Печат(esp)
	}

	if АктивнаПрекъсванеmanager != 0 {
		p := (*TПрекъсванеmanager)(Pointer(АктивнаПрекъсванеmanager))
		esp = p.DoРъкохваткаПрекъсване(uint8(прекъсване), esp)
		return esp
	}
	if handler_2[прекъсване] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[прекъсване])))
		esp = myfunction(esp)
	}
	if прекъсване == 0x80 {
		return ръкохваткаunhandledsyscall(esp)
	}
	if 0x20 <= прекъсване && прекъсване < 0x30 {
		if 0x28 <= прекъсване {
			ПортПисанеbyte(SecondarypicКомандаioПорт, 0x20)
		}
		ПортПисанеbyte(PrimarypicКомандаioПорт, 0x20)
	}

	return esp
}

func ръкохваткаunhandledsyscall(esp uint32) uint32 {
	процесор := (*TcpuСъстояние)(Pointer(uintptr(esp)))
	if процесор.Eax == 1 || процесор.Eax == 252 {
		процесор.Eip = uint32(ValueOf(прекъсванеИзходloop).Pointer())
		процесор.Cs = Segkernelcode
		процесор.Ds = Segkerneldata
		процесор.Es = Segkerneldata
		процесор.Fs = Segkerneldata
		процесор.Gs = Segkernelgs
		процесор.Ss = Segkerneldata
		процесор.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasГрешкаcode(прекъсване uint32) bool {
	switch прекъсване {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionИме(прекъсване uint32) string {
	switch прекъсване {
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

func exceptionРамкаСтойност(рамка uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(рамка + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func печатСтраницаfaultИнформация(грешка uint32) {
	MEmergencyЛогНиз(" pf=[")
	if (грешка & 0x01) != 0 {
		MEmergencyЛогНиз("protection")
	} else {
		MEmergencyЛогНиз("not-present")
	}
	if (грешка & 0x02) != 0 {
		MEmergencyЛогНиз(",write")
	} else {
		MEmergencyЛогНиз(",read")
	}
	if (грешка & 0x04) != 0 {
		MEmergencyЛогНиз(",user")
	} else {
		MEmergencyЛогНиз(",kernel")
	}
	if (грешка & 0x08) != 0 {
		MEmergencyЛогНиз(",reserved-bit")
	}
	if (грешка & 0x10) != 0 {
		MEmergencyЛогНиз(",instruction-fetch")
	}
	MEmergencyЛогНиз("]")
}

func печатexceptionselectorИнформация(грешка uint32) {
	MEmergencyЛогНиз(" selector=")
	MEmergencyЛогunsignedinteger32(грешка & 0xFFFFFFF8)
	MEmergencyЛогНиз(" index=")
	MEmergencyЛогunsignedinteger32(грешка >> 3)
	MEmergencyЛогНиз(" table=")
	if (грешка & 0x02) != 0 {
		MEmergencyЛогНиз("IDT")
	} else if (грешка & 0x04) != 0 {
		MEmergencyЛогНиз("LDT")
	} else {
		MEmergencyЛогНиз("GDT")
	}
	MEmergencyЛогНиз(" ext=")
	MEmergencyЛогunsignedinteger32(грешка & 0x01)
}

func Ръкохваткаexception(esp uint32, прекъсване uint32) uint32 {
	MEmergencyЛогНиз("\nEXCEPTION vec=")
	MEmergencyЛогhexadecimal8(uint8(прекъсване))
	MEmergencyЛогНиз(" ")
	MEmergencyЛогНиз(exceptionИме(прекъсване))
	MEmergencyЛогНиз(" frame=")
	MEmergencyЛогunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyЛогНиз(" invalid-frame")
		if exceptionhasГрешкаcode(прекъсване) {
			MEmergencyЛогНиз(" raw-error-or-bad-esp=")
			MEmergencyЛогunsignedinteger32(esp)
			печатexceptionselectorИнформация(esp)
		}
		MEmergencyЛогНиз("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var грешка uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasГрешкаcode(прекъсване) {
		грешка = exceptionРамкаСтойност(esp, 0)
		eipoffset = 4
	}
	eip := exceptionРамкаСтойност(esp, eipoffset)
	cs := exceptionРамкаСтойност(esp, eipoffset+4)
	eflags := exceptionРамкаСтойност(esp, eipoffset+8)

	MEmergencyЛогНиз(" err=")
	MEmergencyЛогunsignedinteger32(грешка)
	MEmergencyЛогНиз(" eip=")
	MEmergencyЛогunsignedinteger32(eip)
	MEmergencyЛогНиз(" cs=")
	MEmergencyЛогunsignedinteger32(cs)
	MEmergencyЛогНиз(" eflags=")
	MEmergencyЛогunsignedinteger32(eflags)
	MEmergencyЛогНиз(" cr0=")
	MEmergencyЛогunsignedinteger32(exceptioncr0())
	MEmergencyЛогНиз(" cr3=")
	MEmergencyЛогunsignedinteger32(exceptioncr3())

	if прекъсване == 0x0E {
		MEmergencyЛогНиз(" cr2=")
		MEmergencyЛогunsignedinteger32(exceptioncr2())
		печатСтраницаfaultИнформация(грешка)
	}

	if (cs & 0x03) != 0 {
		MEmergencyЛогНиз(" useresp=")
		MEmergencyЛогunsignedinteger32(exceptionРамкаСтойност(esp, eipoffset+12))
		MEmergencyЛогНиз(" ss=")
		MEmergencyЛогunsignedinteger32(exceptionРамкаСтойност(esp, eipoffset+16))
	}

	if exceptionhasГрешкаcode(прекъсване) {
		печатexceptionselectorИнформация(грешка)
	}
	MEmergencyЛогНиз("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltСледfatalexception()

func РъкохваткаfatalПрекъсванеРамка(savedesp uint32, прекъсване uint32) uint32 {
	Ръкохваткаexception(savedesp+52, прекъсване)
	haltСледfatalexception()
	return savedesp
}

func ПрекъсванеАктивна()
func (себеси *TПрекъсванеmanager) Активна() {
	if АктивнаПрекъсванеmanager != 0 {
		себеси.Deactive()
	}
	address := uintptr(Pointer(себеси))
	АктивнаПрекъсванеmanager = address
	ПрекъсванеАктивна()
}
func Прекъсванеdeactive()
func (себеси *TПрекъсванеmanager) Deactive() {
	АктивнаПрекъсванеmanager = 0
	Прекъсванеdeactive()
}

func MyРъкохваткаПрекъсване(прекъсване uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MПечат(buffer)
	return esp
}
func MyТест(прекъсване uint8, esp uint32)

func UnhandleПрекъсване() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MПечат(buffer)
}

func прекъсванеhandler_2(прекъсване uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MПечат(buffer)
	console_2.MHexadecimalПечат(0x40)
	return esp
}
func печатesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Печатxy(esp, 20, 21)
}
func gettls() uint32
func Печатtls() {

}
