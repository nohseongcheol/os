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

func ТестŠtampaj(положај uint8, data uint8)
func скупds(dssegment uint32)
func скупgs(gssegment uint32)
func ометањеIzlazloop()

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

func (isti *TОметањеhandler) Init(Ометањеброј uint8, Ометањеmanager uintptr, funcaddress uintptr) {

	handler_2[Ометањеброј] = funcaddress

	isti.Ометањеброј = Ометањеброј
	isti.Ометањеmanager = Ометањеmanager

}
func (isti *TОметањеhandler) СкупРучкаОметањеfuction(Ометањеброј uint32, address uintptr) {
	handler_2[Ометањеброј] = address
}
func (isti *TОметањеhandler) Уништи() {
	istiuintptr := uintptr(Pointer(isti))
	Ометањеmanager := (*TОметањеmanager)(Pointer(isti.Ометањеmanager))
	if istiuintptr == Ометањеmanager.Gethandler(isti.Ометањеброј) {
		Ометањеmanager.Скупhandler(0, isti.Ометањеброј)
	}

}
func (isti *TОметањеhandler) СкупОметањеmanager(Ометањеmanager uintptr) {
}
func (isti *TОметањеhandler) СкупОметањеброј(Ометањеброј uint8) {
	isti.Ометањеброј = Ометањеброј
}
func (isti *TОметањеhandler) РучкаОметање(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	конзола_2 := TКонзола{}
	конзола_2.MŠtampaj(buffer)
	return esp
}
func РучкаОметање1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	конзола_2 := TКонзола{}
	конзола_2.MŠtampaj(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TОметањеdescriptorTabelaPokazivač struct {
}

var idtdata [256 * 8]uint8
var AktivnaОметањеmanager uintptr = 0

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

func (isti *TОметањеmanager) Init(хардверОметањеoffset uint16, општеdescriptorTabela *TShareddescriptorTabela, задатакmanager *TЗадатакmanager) {

	isti.задатакmanager = задатакmanager

	isti.хардверОметањеoffset = хардверОметањеoffset
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
		isti.ОметањеdescriptorTabelaуносскуп(i, codesegment, address, 0, IdtОметањеgate)
	}

	address = uint32(ValueOf(ометањеexceptionhandler0x00).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x00, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x01).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x01, codesegment, address, 0, IdtОметањеgate)
	address = uint32(ValueOf(ометањеexceptionhandler0x02).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x02, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x03).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x03, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x04).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x04, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x05).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x05, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x06).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x06, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x07).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x07, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x08).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x08, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x09).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x09, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x0a).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x0A, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x0b).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x0B, codesegment, address, 0, IdtОметањеgate)
	address = uint32(ValueOf(ометањеexceptionhandler0x0c).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x0C, codesegment, address, 0, IdtОметањеgate)
	address = uint32(ValueOf(ометањеexceptionhandler0x0d).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x0D, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x0e).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x0E, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x0f).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x0F, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x10).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x10, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x11).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x11, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x12).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x12, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеexceptionhandler0x13).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x13, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x00).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x20, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x01).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x21, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x02).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x22, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x03).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x23, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x04).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x24, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x05).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x25, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x06).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x26, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x07).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x27, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x08).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x28, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x09).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x29, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0a).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x2A, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0b).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x2B, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0c).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x2C, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0d).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x2D, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0e).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x2E, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x0f).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x2F, codesegment, address, 0, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x80).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x80, codesegment, address, 3, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x81).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x81, codesegment, address, 3, IdtОметањеgate)

	address = uint32(ValueOf(ометањеrequesthandler0x82).Pointer())
	isti.ОметањеdescriptorTabelaуносскуп(0x82, codesegment, address, 3, IdtОметањеgate)

	Портupisbyte(PrimarypicНаредбаУИПорт, 0x11)
	Портupisbyte(SecondarypicНаредбаУИПорт, 0x11)

	Портupisbyte(PrimarypicdataУИПорт, 0x20)
	Портupisbyte(SecondarypicdataУИПорт, 0x28)

	Портupisbyte(PrimarypicdataУИПорт, 0x04)
	Портupisbyte(SecondarypicdataУИПорт, 0x02)

	Портupisbyte(PrimarypicdataУИПорт, 0x01)
	Портupisbyte(SecondarypicdataУИПорт, 0x01)

	Портupisbyte(PrimarypicdataУИПорт, 0xF8)
	Портupisbyte(SecondarypicdataУИПорт, 0xEF)

	idtPokazivač := [6]uint8{0, 0, 0, 0, 0, 0}
	величина := (*uint16)(Pointer(&idtPokazivač[0]))
	(*величина) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtPokazivač[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtPokazivač)))
}
func Lidt(lidtaddr uintptr)

func (isti *TОметањеmanager) ОметањеdescriptorTabelaуносскуп(ометање int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorВрста uint8) {

	handleraddressTihoбита := (*uint16)(Pointer(&idtdata[ометање*8+0]))
	(*handleraddressTihoбита) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[ометање*8+2]))
	(*gdtcodesegmentselector) = codesegment

	zauzeto := (*uint8)(Pointer(&idtdata[ометање*8+4]))
	(*zauzeto) = 0

	var IdtdescriptorPrisutno uint8 = 0x80
	приступање := (*uint8)(Pointer(&idtdata[ометање*8+5]))
	(*приступање) = (IdtdescriptorPrisutno | DescriptorВрста | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressВисокабита := (*uint16)(Pointer(&idtdata[ометање*8+6]))
	(*handleraddressВисокабита) = uint16((handler >> 16) & 0xFFFF)

}

func (isti *TОметањеmanager) Скупhandler(handler uintptr, Ометањеброј uint8) {
	handler_2[Ометањеброј] = handler
}
func (isti *TОметањеmanager) Gethandler(Ометањеброј uint8) uintptr {
	return handler_2[Ометањеброј]
}
func (isti *TОметањеmanager) DoРучкаОметање(ометање uint8, esp uint32) uint32 {

	if ометањеИсправљање {
		конзола_2.MŠtampajxy("[esp:", 1, 20)
		конзола_2.MUnsignedinteger32Štampaj(uint32(ометање))
		конзола_2.MŠtampaj(":")
		конзола_2.MUnsignedinteger32Štampaj(esp)
	}
	handlerPokreni := false
	if handler_2[ометање] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ометање])))
		esp = myfunction(esp)
		handlerPokreni = true

	}

	if !handlerPokreni && ометање == uint8(isti.хардверОметањеoffset) && isti.задатакmanager != nil {
		esp = uint32(uintptr(Pointer(isti.задатакmanager.Schedule((*TcpuСтање)(Pointer(uintptr(esp)))))))

	}
	if !handlerPokreni && ометање == 0x80 {
		esp = ручкаunhandledsyscall(esp)
	}

	if ометање <= 0x1F {
	}
	if 0x20 <= ометање && ометање < 0x30 {
		if 0x28 <= ометање {
			Портupisbyte(SecondarypicНаредбаУИПорт, 0x20)
		}
		Портupisbyte(PrimarypicНаредбаУИПорт, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func скупcr3(address uint32)

var конзола_2 TКонзола = TКонзола{}

func РучкаОметање(esp uint32, ометање uint32) uint32 {

	if ометањеИсправљање && ометање != 0x80 && ометање != 0x20 {
		конзола_2.MŠtampajxy("[esp:", 1, 21)
		конзола_2.MUnsignedinteger32Štampaj(uint32(ометање))
		конзола_2.MŠtampaj(":")
		конзола_2.MUnsignedinteger32Štampaj(esp)
	}

	if AktivnaОметањеmanager != 0 {
		p := (*TОметањеmanager)(Pointer(AktivnaОметањеmanager))
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
			Портupisbyte(SecondarypicНаредбаУИПорт, 0x20)
		}
		Портupisbyte(PrimarypicНаредбаУИПорт, 0x20)
	}

	return esp
}

func ручкаunhandledsyscall(esp uint32) uint32 {
	процесор := (*TcpuСтање)(Pointer(uintptr(esp)))
	if процесор.Eax == 1 || процесор.Eax == 252 {
		процесор.Eip = uint32(ValueOf(ометањеIzlazloop).Pointer())
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

func exceptionOkvirВредност(okvir uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(okvir + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func štampajlistfaultПодаци(greška uint32) {
	MEmergencyДневникниска(" pf=[")
	if (greška & 0x01) != 0 {
		MEmergencyДневникниска("protection")
	} else {
		MEmergencyДневникниска("not-present")
	}
	if (greška & 0x02) != 0 {
		MEmergencyДневникниска(",write")
	} else {
		MEmergencyДневникниска(",read")
	}
	if (greška & 0x04) != 0 {
		MEmergencyДневникниска(",user")
	} else {
		MEmergencyДневникниска(",kernel")
	}
	if (greška & 0x08) != 0 {
		MEmergencyДневникниска(",reserved-bit")
	}
	if (greška & 0x10) != 0 {
		MEmergencyДневникниска(",instruction-fetch")
	}
	MEmergencyДневникниска("]")
}

func štampajexceptionselectorПодаци(greška uint32) {
	MEmergencyДневникниска(" selector=")
	MEmergencyДневникunsignedinteger32(greška & 0xFFFFFFF8)
	MEmergencyДневникниска(" index=")
	MEmergencyДневникunsignedinteger32(greška >> 3)
	MEmergencyДневникниска(" table=")
	if (greška & 0x02) != 0 {
		MEmergencyДневникниска("IDT")
	} else if (greška & 0x04) != 0 {
		MEmergencyДневникниска("LDT")
	} else {
		MEmergencyДневникниска("GDT")
	}
	MEmergencyДневникниска(" ext=")
	MEmergencyДневникunsignedinteger32(greška & 0x01)
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
			štampajexceptionselectorПодаци(esp)
		}
		MEmergencyДневникниска("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var greška uint32 = 0
	var eipoffset uint32 = 0
	if exceptionХасГрешкаcode(ометање) {
		greška = exceptionOkvirВредност(esp, 0)
		eipoffset = 4
	}
	eip := exceptionOkvirВредност(esp, eipoffset)
	cs := exceptionOkvirВредност(esp, eipoffset+4)
	eflags := exceptionOkvirВредност(esp, eipoffset+8)

	MEmergencyДневникниска(" err=")
	MEmergencyДневникunsignedinteger32(greška)
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
		štampajlistfaultПодаци(greška)
	}

	if (cs & 0x03) != 0 {
		MEmergencyДневникниска(" useresp=")
		MEmergencyДневникunsignedinteger32(exceptionOkvirВредност(esp, eipoffset+12))
		MEmergencyДневникниска(" ss=")
		MEmergencyДневникunsignedinteger32(exceptionOkvirВредност(esp, eipoffset+16))
	}

	if exceptionХасГрешкаcode(ометање) {
		štampajexceptionselectorПодаци(greška)
	}
	MEmergencyДневникниска("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltПослеfatalexception()

func РучкаfatalОметањеOkvir(savedesp uint32, ометање uint32) uint32 {
	Ручкаexception(savedesp+52, ометање)
	haltПослеfatalexception()
	return savedesp
}

func ОметањеAktivna()
func (isti *TОметањеmanager) Aktivna() {
	if AktivnaОметањеmanager != 0 {
		isti.Deactive()
	}
	address := uintptr(Pointer(isti))
	AktivnaОметањеmanager = address
	ОметањеAktivna()
}
func Ометањеdeactive()
func (isti *TОметањеmanager) Deactive() {
	AktivnaОметањеmanager = 0
	Ометањеdeactive()
}

func MyРучкаОметање(ометање uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	конзола_2 := TКонзола{}
	конзола_2.MŠtampaj(buffer)
	return esp
}
func MyТест(ометање uint8, esp uint32)

func UnhandleОметање() {
	buffer := []byte("unhandle interrupt\n")
	конзола_2 := TКонзола{}
	конзола_2.MŠtampaj(buffer)
}

func ометањеhandler_2(ометање uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	конзола_2 := TКонзола{}
	конзола_2.MŠtampaj(buffer)
	конзола_2.MHexadecimalŠtampaj(0x40)
	return esp
}
func štampajesp(esp uint32) {
	конзола_2 := TКонзола{}
	конзола_2.MUnsignedinteger32Štampajxy(esp, 20, 21)
}
func gettls() uint32
func Štampajtls() {

}
