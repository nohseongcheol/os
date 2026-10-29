/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Ометање

import . "unsafe"
import . "reflect"

import . "порт"
import . "gdt"
import . "multitasking"
import . "конзола"

func ометањеignore()

func ометањеexceptionhandler()
func ометањеexceptionhandler0x00()
func ометањеexceptionhandler0x01()
func ометањеexceptionhandler0x02()
func ометањеexceptionhandler0x03()
func ометањеexceptionhandler0x04()
func ометањеexceptionhandler0x05()
func ометањеexceptionhandler0x06()
func ометањеexceptionhandler0x07()
func ометањеexceptionhandler0x08()
func ометањеexceptionhandler0x09()
func ометањеexceptionhandler0x0a()
func ометањеexceptionhandler0x0b()
func ометањеexceptionhandler0x0c()
func ометањеexceptionhandler0x0d()
func ометањеexceptionhandler0x0e()
func ометањеexceptionhandler0x0f()
func ометањеexceptionhandler0x10()
func ометањеexceptionhandler0x11()
func ометањеexceptionhandler0x12()
func ометањеexceptionhandler0x13()

func ометањеrequesthandler0x00()
func ометањеrequesthandler0x01()
func ометањеrequesthandler0x02()
func ометањеrequesthandler0x03()
func ометањеrequesthandler0x04()
func ометањеrequesthandler0x05()
func ометањеrequesthandler0x06()
func ометањеrequesthandler0x07()
func ометањеrequesthandler0x08()
func ометањеrequesthandler0x09()
func ометањеrequesthandler0x0a()
func ометањеrequesthandler0x0b()
func ометањеrequesthandler0x0c()
func ометањеrequesthandler0x0d()
func ометањеrequesthandler0x0e()
func ометањеrequesthandler0x0f()

func ометањеrequesthandler0x80()
func ометањеrequesthandler0x81()
func ометањеrequesthandler0x82()

func ТестШтампај(положај uint8, data uint8)
func скупds(dssegment uint32)
func скупgs(gssegment uint32)
func ометањеИзлазloop()

type TОметањеhandler struct {
	Ометањеброј	uint8
	Ометањеmanager	uintptr
}
type IОметањеhandler interface {
	РучкаОметање(uint32) uint32
}

func НоваОметањеhandler(Ометањеmanager uintptr, Ометањеброј uint8) *TОметањеhandler {
	ометањеhandler_2 := new(TОметањеhandler)
	ометањеhandler_2.Ометањеброј = Ометањеброј
	ометањеhandler_2.Ометањеmanager = Ометањеmanager
	return ометањеhandler_2

}

var handler_2 [256]uintptr

func (исти *TОметањеhandler) Init(Ометањеброј uint8, Ометањеmanager uintptr, funcaddress uintptr) {

	handler_2[Ометањеброј] = funcaddress

	исти.Ометањеброј = Ометањеброј
	исти.Ометањеmanager = Ометањеmanager

}
func (исти *TОметањеhandler) СкупРучкаОметањеfuction(Ометањеброј uint32, address uintptr) {
	handler_2[Ометањеброј] = address
}
func (исти *TОметањеhandler) Уништи() {
	истиuintptr := uintptr(Pointer(исти))
	Ометањеmanager := (*TОметањеmanager)(Pointer(исти.Ометањеmanager))
	if истиuintptr == Ометањеmanager.Gethandler(исти.Ометањеброј) {
		Ометањеmanager.Скупhandler(0, исти.Ометањеброј)
	}

}
func (исти *TОметањеhandler) СкупОметањеmanager(Ометањеmanager uintptr) {
}
func (исти *TОметањеhandler) СкупОметањеброј(Ометањеброј uint8) {
	исти.Ометањеброј = Ометањеброј
}
func (исти *TОметањеhandler) РучкаОметање(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	конзола_2 := TКонзола{}
	конзола_2.MШтампај(buffer)
	return esp
}
func РучкаОметање1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	конзола_2 := TКонзола{}
	конзола_2.MШтампај(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TОметањеdescriptorТабелаПоказивач struct {
}

var idtdata [256 * 8]uint8
var АктивнаОметањеmanager uintptr = 0

const ометањеИсправљање = false

type TОметањеmanager struct {
	handler_2	[256]uintptr

	хардверОметањеoffset	uint16

	задатакmanager	*TЗадатакmanager
}

var PrimarypicНаредбаУИПорт uint16 = 0x20
var PrimarypicdataУИПорт uint16 = 0x21
var SecondarypicНаредбаУИПорт uint16 = 0xA0
var SecondarypicdataУИПорт uint16 = 0xA1

func (исти *TОметањеmanager) Init(хардверОметањеoffset uint16, општеdescriptorТабела *TShareddescriptorТабела, задатакmanager *TЗадатакmanager) {

	исти.задатакmanager = задатакmanager

	исти.хардверОметањеoffset = хардверОметањеoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtОметањеgate uint8 = 0xE
	address = uint32(ValueOf(ометањеignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(ометањеexceptionhandler0x0f).Pointer())
		исти.ОметањеdescriptorТабелауносскуп(i, codesegment, address, 0, IdtОметањеgate)
	}

	address = uint32(ValueOf(ометањеexceptionhandler0x00).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x00, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x01).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x01, codesegment, address, 0, IdtОметањеgate)
	address = uint32(ValueOf(ометањеexceptionhandler0x02).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x02, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x03).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x03, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x04).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x04, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x05).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x05, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x06).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x06, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x07).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x07, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x08).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x08, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x09).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x09, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x0a).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x0A, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x0b).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x0B, codesegment, address, 0, IdtОметањеgate)
	address = uint32(ValueOf(ометањеexceptionhandler0x0c).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x0C, codesegment, address, 0, IdtОметањеgate)
	address = uint32(ValueOf(ометањеexceptionhandler0x0d).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x0D, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x0e).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x0E, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x0f).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x0F, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x10).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x10, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x11).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x11, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x12).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x12, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x13).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x13, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x00).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x20, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x01).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x21, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x02).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x22, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x03).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x23, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x04).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x24, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x05).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x25, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x06).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x26, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x07).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x27, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x08).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x28, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x09).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x29, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0a).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x2A, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0b).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x2B, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0c).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x2C, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0d).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x2D, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0e).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x2E, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0f).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x2F, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x80).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x80, codesegment, address, 3, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x81).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x81, codesegment, address, 3, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x82).Pointer())
	исти.ОметањеdescriptorТабелауносскуп(0x82, codesegment, address, 3, IdtОметањеgate)

	ПортПишеbyte(PrimarypicНаредбаУИПорт, 0x11)
	ПортПишеbyte(SecondarypicНаредбаУИПорт, 0x11)

	ПортПишеbyte(PrimarypicdataУИПорт, 0x20)
	ПортПишеbyte(SecondarypicdataУИПорт, 0x28)

	ПортПишеbyte(PrimarypicdataУИПорт, 0x04)
	ПортПишеbyte(SecondarypicdataУИПорт, 0x02)

	ПортПишеbyte(PrimarypicdataУИПорт, 0x01)
	ПортПишеbyte(SecondarypicdataУИПорт, 0x01)

	ПортПишеbyte(PrimarypicdataУИПорт, 0xF8)
	ПортПишеbyte(SecondarypicdataУИПорт, 0xEF)

	idtПоказивач := [6]uint8{0, 0, 0, 0, 0, 0}
	величина := (*uint16)(Pointer(&idtПоказивач[0]))
	(*величина) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtПоказивач[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtПоказивач)))
}
func Lidt(lidtaddr uintptr)

func (исти *TОметањеmanager) ОметањеdescriptorТабелауносскуп(ометање int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorВрста uint8) {

	handleraddressТихобита := (*uint16)(Pointer(&idtdata[ометање*8+0]))
	(*handleraddressТихобита) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[ометање*8+2]))
	(*gdtcodesegmentselector) = codesegment

	заузето := (*uint8)(Pointer(&idtdata[ометање*8+4]))
	(*заузето) = 0

	var IdtdescriptorПрисутна uint8 = 0x80
	приступање := (*uint8)(Pointer(&idtdata[ометање*8+5]))
	(*приступање) = (IdtdescriptorПрисутна | DescriptorВрста | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressВисокабита := (*uint16)(Pointer(&idtdata[ометање*8+6]))
	(*handleraddressВисокабита) = uint16((handler >> 16) & 0xFFFF)

}

func (исти *TОметањеmanager) Скупhandler(handler uintptr, Ометањеброј uint8) {
	handler_2[Ометањеброј] = handler
}
func (исти *TОметањеmanager) Gethandler(Ометањеброј uint8) uintptr {
	return handler_2[Ометањеброј]
}
func (исти *TОметањеmanager) DoРучкаОметање(ометање uint8, esp uint32) uint32 {

	if ометањеИсправљање {
		конзола_2.MШтампајxy("[esp:", 1, 20)
		конзола_2.MUnsignedinteger32Штампај(uint32(ометање))
		конзола_2.MШтампај(":")
		конзола_2.MUnsignedinteger32Штампај(esp)
	}
	handlerПокрени := false
	if handler_2[ометање] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ометање])))
		esp = myfunction(esp)
		handlerПокрени = true

	}

	if !handlerПокрени && ометање == uint8(исти.хардверОметањеoffset) && исти.задатакmanager != nil {
		esp = uint32(uintptr(Pointer(исти.задатакmanager.Schedule((*TcpuСтање)(Pointer(uintptr(esp)))))))

	}
	if !handlerПокрени && ометање == 0x80 {
		esp = ручкаunhandledsyscall(esp)
	}

	if ометање <= 0x1F {
	}
	if 0x20 <= ометање && ометање < 0x30 {
		if 0x28 <= ометање {
			ПортПишеbyte(SecondarypicНаредбаУИПорт, 0x20)
		}
		ПортПишеbyte(PrimarypicНаредбаУИПорт, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func скупcr3(address uint32)

var конзола_2 TКонзола = TКонзола{}

func РучкаОметање(esp uint32, ометање uint32) uint32 {

	if ометањеИсправљање && ометање != 0x80 && ометање != 0x20 {
		конзола_2.MШтампајxy("[esp:", 1, 21)
		конзола_2.MUnsignedinteger32Штампај(uint32(ометање))
		конзола_2.MШтампај(":")
		конзола_2.MUnsignedinteger32Штампај(esp)
	}

	if АктивнаОметањеmanager != 0 {
		p := (*TОметањеmanager)(Pointer(АктивнаОметањеmanager))
		esp = p.DoРучкаОметање(uint8(ометање), esp)
		return esp
	}
	if handler_2[ометање] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ометање])))
		esp = myfunction(esp)
	}
	if ометање == 0x80 {
		return ручкаunhandledsyscall(esp)
	}
	if 0x20 <= ометање && ометање < 0x30 {
		if 0x28 <= ометање {
			ПортПишеbyte(SecondarypicНаредбаУИПорт, 0x20)
		}
		ПортПишеbyte(PrimarypicНаредбаУИПорт, 0x20)
	}

	return esp
}

func ручкаunhandledsyscall(esp uint32) uint32 {
	процесор := (*TcpuСтање)(Pointer(uintptr(esp)))
	if процесор.Eax == 1 || процесор.Eax == 252 {
		процесор.Eip = uint32(ValueOf(ометањеИзлазloop).Pointer())
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

func exceptionХасГрешкаcode(ометање uint32) bool {
	switch ометање {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionНазив(ометање uint32) string {
	switch ометање {
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

func exceptionОквирВредност(оквир uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(оквир + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func штампајСТРАНАfaultПодаци(грешка uint32) {
	MEmergencyДневникниска(" pf=[")
	if (грешка & 0x01) != 0 {
		MEmergencyДневникниска("protection")
	} else {
		MEmergencyДневникниска("not-present")
	}
	if (грешка & 0x02) != 0 {
		MEmergencyДневникниска(",write")
	} else {
		MEmergencyДневникниска(",read")
	}
	if (грешка & 0x04) != 0 {
		MEmergencyДневникниска(",user")
	} else {
		MEmergencyДневникниска(",kernel")
	}
	if (грешка & 0x08) != 0 {
		MEmergencyДневникниска(",reserved-bit")
	}
	if (грешка & 0x10) != 0 {
		MEmergencyДневникниска(",instruction-fetch")
	}
	MEmergencyДневникниска("]")
}

func штампајexceptionselectorПодаци(грешка uint32) {
	MEmergencyДневникниска(" selector=")
	MEmergencyДневникunsignedinteger32(грешка & 0xFFFFFFF8)
	MEmergencyДневникниска(" index=")
	MEmergencyДневникunsignedinteger32(грешка >> 3)
	MEmergencyДневникниска(" table=")
	if (грешка & 0x02) != 0 {
		MEmergencyДневникниска("IDT")
	} else if (грешка & 0x04) != 0 {
		MEmergencyДневникниска("LDT")
	} else {
		MEmergencyДневникниска("GDT")
	}
	MEmergencyДневникниска(" ext=")
	MEmergencyДневникunsignedinteger32(грешка & 0x01)
}

func Ручкаexception(esp uint32, ометање uint32) uint32 {
	MEmergencyДневникниска("\nEXCEPTION vec=")
	MEmergencyДневникhexadecimal8(uint8(ометање))
	MEmergencyДневникниска(" ")
	MEmergencyДневникниска(exceptionНазив(ометање))
	MEmergencyДневникниска(" frame=")
	MEmergencyДневникunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyДневникниска(" invalid-frame")
		if exceptionХасГрешкаcode(ометање) {
			MEmergencyДневникниска(" raw-error-or-bad-esp=")
			MEmergencyДневникunsignedinteger32(esp)
			штампајexceptionselectorПодаци(esp)
		}
		MEmergencyДневникниска("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var грешка uint32 = 0
	var eipoffset uint32 = 0
	if exceptionХасГрешкаcode(ометање) {
		грешка = exceptionОквирВредност(esp, 0)
		eipoffset = 4
	}
	eip := exceptionОквирВредност(esp, eipoffset)
	cs := exceptionОквирВредност(esp, eipoffset+4)
	eflags := exceptionОквирВредност(esp, eipoffset+8)

	MEmergencyДневникниска(" err=")
	MEmergencyДневникunsignedinteger32(грешка)
	MEmergencyДневникниска(" eip=")
	MEmergencyДневникunsignedinteger32(eip)
	MEmergencyДневникниска(" cs=")
	MEmergencyДневникunsignedinteger32(cs)
	MEmergencyДневникниска(" eflags=")
	MEmergencyДневникunsignedinteger32(eflags)
	MEmergencyДневникниска(" cr0=")
	MEmergencyДневникunsignedinteger32(exceptioncr0())
	MEmergencyДневникниска(" cr3=")
	MEmergencyДневникunsignedinteger32(exceptioncr3())

	if ометање == 0x0E {
		MEmergencyДневникниска(" cr2=")
		MEmergencyДневникunsignedinteger32(exceptioncr2())
		штампајСТРАНАfaultПодаци(грешка)
	}

	if (cs & 0x03) != 0 {
		MEmergencyДневникниска(" useresp=")
		MEmergencyДневникunsignedinteger32(exceptionОквирВредност(esp, eipoffset+12))
		MEmergencyДневникниска(" ss=")
		MEmergencyДневникunsignedinteger32(exceptionОквирВредност(esp, eipoffset+16))
	}

	if exceptionХасГрешкаcode(ометање) {
		штампајexceptionselectorПодаци(грешка)
	}
	MEmergencyДневникниска("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltПослеfatalexception()

func РучкаfatalОметањеОквир(savedesp uint32, ометање uint32) uint32 {
	Ручкаexception(savedesp+52, ометање)
	haltПослеfatalexception()
	return savedesp
}

func ОметањеАктивна()
func (исти *TОметањеmanager) Активна() {
	if АктивнаОметањеmanager != 0 {
		исти.Deactive()
	}
	address := uintptr(Pointer(исти))
	АктивнаОметањеmanager = address
	ОметањеАктивна()
}
func Ометањеdeactive()
func (исти *TОметањеmanager) Deactive() {
	АктивнаОметањеmanager = 0
	Ометањеdeactive()
}

func MyРучкаОметање(ометање uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	конзола_2 := TКонзола{}
	конзола_2.MШтампај(buffer)
	return esp
}
func MyТест(ометање uint8, esp uint32)

func UnhandleОметање() {
	buffer := []byte("unhandle interrupt\n")
	конзола_2 := TКонзола{}
	конзола_2.MШтампај(buffer)
}

func ометањеhandler_2(ометање uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	конзола_2 := TКонзола{}
	конзола_2.MШтампај(buffer)
	конзола_2.MHexadecimalШтампај(0x40)
	return esp
}
func штампајesp(esp uint32) {
	конзола_2 := TКонзола{}
	конзола_2.MUnsignedinteger32Штампајxy(esp, 20, 21)
}
func gettls() uint32
func Штампајtls() {

}
