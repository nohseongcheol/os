/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Переривання

import . "unsafe"
import . "reflect"

import . "порт"
import . "gdt"
import . "multitasking"
import . "консоль"

func перериванняignore()

func перериванняexceptionhandler()
func перериванняexceptionhandler0x00()
func перериванняexceptionhandler0x01()
func перериванняexceptionhandler0x02()
func перериванняexceptionhandler0x03()
func перериванняexceptionhandler0x04()
func перериванняexceptionhandler0x05()
func перериванняexceptionhandler0x06()
func перериванняexceptionhandler0x07()
func перериванняexceptionhandler0x08()
func перериванняexceptionhandler0x09()
func перериванняexceptionhandler0x0a()
func перериванняexceptionhandler0x0b()
func перериванняexceptionhandler0x0c()
func перериванняexceptionhandler0x0d()
func перериванняexceptionhandler0x0e()
func перериванняexceptionhandler0x0f()
func перериванняexceptionhandler0x10()
func перериванняexceptionhandler0x11()
func перериванняexceptionhandler0x12()
func перериванняexceptionhandler0x13()

func перериванняrequesthandler0x00()
func перериванняrequesthandler0x01()
func перериванняrequesthandler0x02()
func перериванняrequesthandler0x03()
func перериванняrequesthandler0x04()
func перериванняrequesthandler0x05()
func перериванняrequesthandler0x06()
func перериванняrequesthandler0x07()
func перериванняrequesthandler0x08()
func перериванняrequesthandler0x09()
func перериванняrequesthandler0x0a()
func перериванняrequesthandler0x0b()
func перериванняrequesthandler0x0c()
func перериванняrequesthandler0x0d()
func перериванняrequesthandler0x0e()
func перериванняrequesthandler0x0f()

func перериванняrequesthandler0x80()
func перериванняrequesthandler0x81()
func перериванняrequesthandler0x82()

func ТестДрук(позиція uint8, data uint8)
func множинаds(dssegment uint32)
func множинаgs(gssegment uint32)
func перериванняВийтиloop()

type TПерериванняhandler struct {
	ПерериванняЧисло	uint8
	Перериванняmanager	uintptr
}
type IПерериванняhandler interface {
	ЕлементкеруванняПереривання(uint32) uint32
}

func НовийПерериванняhandler(Перериванняmanager uintptr, ПерериванняЧисло uint8) *TПерериванняhandler {
	перериванняhandler_2 := new(TПерериванняhandler)
	перериванняhandler_2.ПерериванняЧисло = ПерериванняЧисло
	перериванняhandler_2.Перериванняmanager = Перериванняmanager
	return перериванняhandler_2

}

var handler_2 [256]uintptr

func (поточний *TПерериванняhandler) Init(ПерериванняЧисло uint8, Перериванняmanager uintptr, funcАдреса uintptr) {

	handler_2[ПерериванняЧисло] = funcАдреса

	поточний.ПерериванняЧисло = ПерериванняЧисло
	поточний.Перериванняmanager = Перериванняmanager

}
func (поточний *TПерериванняhandler) МножинаЕлементкеруванняПерериванняfuction(ПерериванняЧисло uint32, адреса uintptr) {
	handler_2[ПерериванняЧисло] = адреса
}
func (поточний *TПерериванняhandler) Знищити() {
	поточнийuintptr := uintptr(Pointer(поточний))
	Перериванняmanager := (*TПерериванняmanager)(Pointer(поточний.Перериванняmanager))
	if поточнийuintptr == Перериванняmanager.Gethandler(поточний.ПерериванняЧисло) {
		Перериванняmanager.Множинаhandler(0, поточний.ПерериванняЧисло)
	}

}
func (поточний *TПерериванняhandler) МножинаПерериванняmanager(Перериванняmanager uintptr) {
}
func (поточний *TПерериванняhandler) МножинаПерериванняЧисло(ПерериванняЧисло uint8) {
	поточний.ПерериванняЧисло = ПерериванняЧисло
}
func (поточний *TПерериванняhandler) ЕлементкеруванняПереривання(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	консоль_2 := TКонсоль{}
	консоль_2.MДрук(buffer)
	return esp
}
func ЕлементкеруванняПереривання1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	консоль_2 := TКонсоль{}
	консоль_2.MДрук(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TПерериванняdescriptorТаблицяВказівник struct {
}

var idtdata [256 * 8]uint8
var АктивнийПерериванняmanager uintptr = 0

const перериванняДіагностика = false

type TПерериванняmanager struct {
	handler_2	[256]uintptr

	пристроїПерериванняoffset	uint16

	задачаmanager	*TЗадачаmanager
}

var PrimarypicКомандаВвідвивідПорт uint16 = 0x20
var PrimarypicdataВвідвивідПорт uint16 = 0x21
var SecondarypicКомандаВвідвивідПорт uint16 = 0xA0
var SecondarypicdataВвідвивідПорт uint16 = 0xA1

func (поточний *TПерериванняmanager) Init(пристроїПерериванняoffset uint16, глобальніdescriptorТаблиця *TShareddescriptorТаблиця, задачаmanager *TЗадачаmanager) {

	поточний.задачаmanager = задачаmanager

	поточний.пристроїПерериванняoffset = пристроїПерериванняoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var адреса uint32
	var IdtПерериванняgate uint8 = 0xE
	адреса = uint32(ValueOf(перериванняignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		адреса = uint32(ValueOf(перериванняexceptionhandler0x0f).Pointer())
		поточний.ПерериванняdescriptorТаблицязаписмножина(i, codesegment, адреса, 0, IdtПерериванняgate)
	}

	адреса = uint32(ValueOf(перериванняexceptionhandler0x00).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x00, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x01).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x01, codesegment, адреса, 0, IdtПерериванняgate)
	адреса = uint32(ValueOf(перериванняexceptionhandler0x02).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x02, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x03).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x03, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x04).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x04, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x05).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x05, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x06).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x06, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x07).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x07, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x08).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x08, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x09).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x09, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x0a).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x0A, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x0b).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x0B, codesegment, адреса, 0, IdtПерериванняgate)
	адреса = uint32(ValueOf(перериванняexceptionhandler0x0c).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x0C, codesegment, адреса, 0, IdtПерериванняgate)
	адреса = uint32(ValueOf(перериванняexceptionhandler0x0d).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x0D, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x0e).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x0E, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x0f).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x0F, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x10).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x10, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x11).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x11, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x12).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x12, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняexceptionhandler0x13).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x13, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x00).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x20, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x01).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x21, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x02).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x22, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x03).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x23, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x04).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x24, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x05).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x25, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x06).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x26, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x07).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x27, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x08).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x28, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x09).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x29, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x0a).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x2A, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x0b).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x2B, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x0c).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x2C, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x0d).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x2D, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x0e).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x2E, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x0f).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x2F, codesegment, адреса, 0, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x80).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x80, codesegment, адреса, 3, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x81).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x81, codesegment, адреса, 3, IdtПерериванняgate)

	адреса = uint32(ValueOf(перериванняrequesthandler0x82).Pointer())
	поточний.ПерериванняdescriptorТаблицязаписмножина(0x82, codesegment, адреса, 3, IdtПерериванняgate)

	ПортЗаписbyte(PrimarypicКомандаВвідвивідПорт, 0x11)
	ПортЗаписbyte(SecondarypicКомандаВвідвивідПорт, 0x11)

	ПортЗаписbyte(PrimarypicdataВвідвивідПорт, 0x20)
	ПортЗаписbyte(SecondarypicdataВвідвивідПорт, 0x28)

	ПортЗаписbyte(PrimarypicdataВвідвивідПорт, 0x04)
	ПортЗаписbyte(SecondarypicdataВвідвивідПорт, 0x02)

	ПортЗаписbyte(PrimarypicdataВвідвивідПорт, 0x01)
	ПортЗаписbyte(SecondarypicdataВвідвивідПорт, 0x01)

	ПортЗаписbyte(PrimarypicdataВвідвивідПорт, 0xF8)
	ПортЗаписbyte(SecondarypicdataВвідвивідПорт, 0xEF)

	idtВказівник := [6]uint8{0, 0, 0, 0, 0, 0}
	розмір := (*uint16)(Pointer(&idtВказівник[0]))
	(*розмір) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtВказівник[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtВказівник)))
}
func Lidt(lidtaddr uintptr)

func (поточний *TПерериванняmanager) ПерериванняdescriptorТаблицязаписмножина(переривання int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorТип uint8) {

	handlerАдресаНизькабіт := (*uint16)(Pointer(&idtdata[переривання*8+0]))
	(*handlerАдресаНизькабіт) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[переривання*8+2]))
	(*gdtcodesegmentselector) = codesegment

	зарезервована := (*uint8)(Pointer(&idtdata[переривання*8+4]))
	(*зарезервована) = 0

	var IdtdescriptorПрисутній uint8 = 0x80
	доступ := (*uint8)(Pointer(&idtdata[переривання*8+5]))
	(*доступ) = (IdtdescriptorПрисутній | DescriptorТип | ((Descriptorprivilegelevel & 3) << 5))

	handlerАдресаВисокийбіт := (*uint16)(Pointer(&idtdata[переривання*8+6]))
	(*handlerАдресаВисокийбіт) = uint16((handler >> 16) & 0xFFFF)

}

func (поточний *TПерериванняmanager) Множинаhandler(handler uintptr, ПерериванняЧисло uint8) {
	handler_2[ПерериванняЧисло] = handler
}
func (поточний *TПерериванняmanager) Gethandler(ПерериванняЧисло uint8) uintptr {
	return handler_2[ПерериванняЧисло]
}
func (поточний *TПерериванняmanager) DoЕлементкеруванняПереривання(переривання uint8, esp uint32) uint32 {

	if перериванняДіагностика {
		консоль_2.MДрукxy("[esp:", 1, 20)
		консоль_2.MUnsignedinteger32Друк(uint32(переривання))
		консоль_2.MДрук(":")
		консоль_2.MUnsignedinteger32Друк(esp)
	}
	handlerЗапустити := false
	if handler_2[переривання] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[переривання])))
		esp = myfunction(esp)
		handlerЗапустити = true

	}

	if !handlerЗапустити && переривання == uint8(поточний.пристроїПерериванняoffset) && поточний.задачаmanager != nil {
		esp = uint32(uintptr(Pointer(поточний.задачаmanager.Schedule((*TcpuСтан)(Pointer(uintptr(esp)))))))

	}
	if !handlerЗапустити && переривання == 0x80 {
		esp = елементкеруванняunhandledsyscall(esp)
	}

	if переривання <= 0x1F {
	}
	if 0x20 <= переривання && переривання < 0x30 {
		if 0x28 <= переривання {
			ПортЗаписbyte(SecondarypicКомандаВвідвивідПорт, 0x20)
		}
		ПортЗаписbyte(PrimarypicКомандаВвідвивідПорт, 0x20)
	}
	return esp
}

var відлік2 uint8 = 1

func множинаcr3(адреса uint32)

var консоль_2 TКонсоль = TКонсоль{}

func ЕлементкеруванняПереривання(esp uint32, переривання uint32) uint32 {

	if перериванняДіагностика && переривання != 0x80 && переривання != 0x20 {
		консоль_2.MДрукxy("[esp:", 1, 21)
		консоль_2.MUnsignedinteger32Друк(uint32(переривання))
		консоль_2.MДрук(":")
		консоль_2.MUnsignedinteger32Друк(esp)
	}

	if АктивнийПерериванняmanager != 0 {
		p := (*TПерериванняmanager)(Pointer(АктивнийПерериванняmanager))
		esp = p.DoЕлементкеруванняПереривання(uint8(переривання), esp)
		return esp
	}
	if handler_2[переривання] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[переривання])))
		esp = myfunction(esp)
	}
	if переривання == 0x80 {
		return елементкеруванняunhandledsyscall(esp)
	}
	if 0x20 <= переривання && переривання < 0x30 {
		if 0x28 <= переривання {
			ПортЗаписbyte(SecondarypicКомандаВвідвивідПорт, 0x20)
		}
		ПортЗаписbyte(PrimarypicКомандаВвідвивідПорт, 0x20)
	}

	return esp
}

func елементкеруванняunhandledsyscall(esp uint32) uint32 {
	процесор := (*TcpuСтан)(Pointer(uintptr(esp)))
	if процесор.Eax == 1 || процесор.Eax == 252 {
		процесор.Eip = uint32(ValueOf(перериванняВийтиloop).Pointer())
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

func exceptionХасіПомилкаcode(переривання uint32) bool {
	switch переривання {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionНазва(переривання uint32) string {
	switch переривання {
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

func exceptionБлокЗначення(блок uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(блок + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func друкСторінкаfaultІнфо(err uint32) {
	MEmergencyЖурналРядок(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencyЖурналРядок("protection")
	} else {
		MEmergencyЖурналРядок("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencyЖурналРядок(",write")
	} else {
		MEmergencyЖурналРядок(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencyЖурналРядок(",user")
	} else {
		MEmergencyЖурналРядок(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencyЖурналРядок(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencyЖурналРядок(",instruction-fetch")
	}
	MEmergencyЖурналРядок("]")
}

func друкexceptionselectorІнфо(err uint32) {
	MEmergencyЖурналРядок(" selector=")
	MEmergencyЖурналunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencyЖурналРядок(" index=")
	MEmergencyЖурналunsignedinteger32(err >> 3)
	MEmergencyЖурналРядок(" table=")
	if (err & 0x02) != 0 {
		MEmergencyЖурналРядок("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencyЖурналРядок("LDT")
	} else {
		MEmergencyЖурналРядок("GDT")
	}
	MEmergencyЖурналРядок(" ext=")
	MEmergencyЖурналunsignedinteger32(err & 0x01)
}

func Елементкеруванняexception(esp uint32, переривання uint32) uint32 {
	MEmergencyЖурналРядок("\nEXCEPTION vec=")
	MEmergencyЖурналhexadecimal8(uint8(переривання))
	MEmergencyЖурналРядок(" ")
	MEmergencyЖурналРядок(exceptionНазва(переривання))
	MEmergencyЖурналРядок(" frame=")
	MEmergencyЖурналunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyЖурналРядок(" invalid-frame")
		if exceptionХасіПомилкаcode(переривання) {
			MEmergencyЖурналРядок(" raw-error-or-bad-esp=")
			MEmergencyЖурналunsignedinteger32(esp)
			друкexceptionselectorІнфо(esp)
		}
		MEmergencyЖурналРядок("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionХасіПомилкаcode(переривання) {
		err = exceptionБлокЗначення(esp, 0)
		eipoffset = 4
	}
	eip := exceptionБлокЗначення(esp, eipoffset)
	cs := exceptionБлокЗначення(esp, eipoffset+4)
	eflags := exceptionБлокЗначення(esp, eipoffset+8)

	MEmergencyЖурналРядок(" err=")
	MEmergencyЖурналunsignedinteger32(err)
	MEmergencyЖурналРядок(" eip=")
	MEmergencyЖурналunsignedinteger32(eip)
	MEmergencyЖурналРядок(" cs=")
	MEmergencyЖурналunsignedinteger32(cs)
	MEmergencyЖурналРядок(" eflags=")
	MEmergencyЖурналunsignedinteger32(eflags)
	MEmergencyЖурналРядок(" cr0=")
	MEmergencyЖурналunsignedinteger32(exceptioncr0())
	MEmergencyЖурналРядок(" cr3=")
	MEmergencyЖурналunsignedinteger32(exceptioncr3())

	if переривання == 0x0E {
		MEmergencyЖурналРядок(" cr2=")
		MEmergencyЖурналunsignedinteger32(exceptioncr2())
		друкСторінкаfaultІнфо(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencyЖурналРядок(" useresp=")
		MEmergencyЖурналunsignedinteger32(exceptionБлокЗначення(esp, eipoffset+12))
		MEmergencyЖурналРядок(" ss=")
		MEmergencyЖурналunsignedinteger32(exceptionБлокЗначення(esp, eipoffset+16))
	}

	if exceptionХасіПомилкаcode(переривання) {
		друкexceptionselectorІнфо(err)
	}
	MEmergencyЖурналРядок("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltПісляfatalexception()

func ЕлементкеруванняfatalПерериванняБлок(збереженоesp uint32, переривання uint32) uint32 {
	Елементкеруванняexception(збереженоesp+52, переривання)
	haltПісляfatalexception()
	return збереженоesp
}

func ПерериванняАктивний()
func (поточний *TПерериванняmanager) Активний() {
	if АктивнийПерериванняmanager != 0 {
		поточний.Deactive()
	}
	адреса := uintptr(Pointer(поточний))
	АктивнийПерериванняmanager = адреса
	ПерериванняАктивний()
}
func Перериванняdeactive()
func (поточний *TПерериванняmanager) Deactive() {
	АктивнийПерериванняmanager = 0
	Перериванняdeactive()
}

func MyЕлементкеруванняПереривання(переривання uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	консоль_2 := TКонсоль{}
	консоль_2.MДрук(buffer)
	return esp
}
func MyТест(переривання uint8, esp uint32)

func UnhandleПереривання() {
	buffer := []byte("unhandle interrupt\n")
	консоль_2 := TКонсоль{}
	консоль_2.MДрук(buffer)
}

func перериванняhandler_2(переривання uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	консоль_2 := TКонсоль{}
	консоль_2.MДрук(buffer)
	консоль_2.MHexadecimalДрук(0x40)
	return esp
}
func друкesp(esp uint32) {
	консоль_2 := TКонсоль{}
	консоль_2.MUnsignedinteger32Друкxy(esp, 20, 21)
}
func gettls() uint32
func Друкtls() {

}
