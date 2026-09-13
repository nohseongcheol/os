package Interrupt

import . "unsafe"
import . "reflect"

import . "porta"
import . "gdt"
import . "multitasking"
import . "konsolë"

func interruptignore()

func interruptexceptionhandler()
func interruptexceptionhandler0x00()
func interruptexceptionhandler0x01()
func interruptexceptionhandler0x02()
func interruptexceptionhandler0x03()
func interruptexceptionhandler0x04()
func interruptexceptionhandler0x05()
func interruptexceptionhandler0x06()
func interruptexceptionhandler0x07()
func interruptexceptionhandler0x08()
func interruptexceptionhandler0x09()
func interruptexceptionhandler0x0a()
func interruptexceptionhandler0x0b()
func interruptexceptionhandler0x0c()
func interruptexceptionhandler0x0d()
func interruptexceptionhandler0x0e()
func interruptexceptionhandler0x0f()
func interruptexceptionhandler0x10()
func interruptexceptionhandler0x11()
func interruptexceptionhandler0x12()
func interruptexceptionhandler0x13()

func interruptrequesthandler0x00()
func interruptrequesthandler0x01()
func interruptrequesthandler0x02()
func interruptrequesthandler0x03()
func interruptrequesthandler0x04()
func interruptrequesthandler0x05()
func interruptrequesthandler0x06()
func interruptrequesthandler0x07()
func interruptrequesthandler0x08()
func interruptrequesthandler0x09()
func interruptrequesthandler0x0a()
func interruptrequesthandler0x0b()
func interruptrequesthandler0x0c()
func interruptrequesthandler0x0d()
func interruptrequesthandler0x0e()
func interruptrequesthandler0x0f()

func interruptrequesthandler0x80()
func interruptrequesthandler0x81()
func interruptrequesthandler0x82()

func ProvoPrinto(pozicion uint8, data uint8)
func caktonids(dssegment uint32)
func caktonigs(gssegment uint32)
func interruptDaljaloop()

type TInterrupthandler struct {
	Interruptnumber		uint8
	InterruptManazhuesi	uintptr
}
type IInterrupthandler interface {
	Handleinterrupt(uint32) uint32
}

func IRiinterrupthandler(InterruptManazhuesi uintptr, Interruptnumber uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.Interruptnumber = Interruptnumber
	interrupthandler_2.InterruptManazhuesi = InterruptManazhuesi
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (vetvetja *TInterrupthandler) Init(Interruptnumber uint8, InterruptManazhuesi uintptr, funcaddress uintptr) {

	handler_2[Interruptnumber] = funcaddress

	vetvetja.Interruptnumber = Interruptnumber
	vetvetja.InterruptManazhuesi = InterruptManazhuesi

}
func (vetvetja *TInterrupthandler) Caktonihandleinterruptfuction(Interruptnumber uint32, address uintptr) {
	handler_2[Interruptnumber] = address
}
func (vetvetja *TInterrupthandler) Shkatërroje() {
	vetvetjauintptr := uintptr(Pointer(vetvetja))
	InterruptManazhuesi := (*TInterruptManazhuesi)(Pointer(vetvetja.InterruptManazhuesi))
	if vetvetjauintptr == InterruptManazhuesi.Gethandler(vetvetja.Interruptnumber) {
		InterruptManazhuesi.Caktonihandler(0, vetvetja.Interruptnumber)
	}

}
func (vetvetja *TInterrupthandler) CaktoniinterruptManazhuesi(InterruptManazhuesi uintptr) {
}
func (vetvetja *TInterrupthandler) Caktoniinterruptnumber(Interruptnumber uint8) {
	vetvetja.Interruptnumber = Interruptnumber
}
func (vetvetja *TInterrupthandler) Handleinterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konsolë_2 := TKonsolë{}
	konsolë_2.MPrinto(buffer)
	return esp
}
func Handleinterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konsolë_2 := TKonsolë{}
	konsolë_2.MPrinto(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptorTabelaKursori struct {
}

var idtdata [256 * 8]uint8
var AktivinterruptManazhuesi uintptr = 0

const interruptdebug = false

type TInterruptManazhuesi struct {
	handler_2	[256]uintptr

	hardwareinterruptoffset	uint16

	procesManazhuesi	*TProcesManazhuesi
}

var PrimarypicUrdhërioPorta uint16 = 0x20
var PrimarypicdataioPorta uint16 = 0x21
var SecondarypicUrdhërioPorta uint16 = 0xA0
var SecondarypicdataioPorta uint16 = 0xA1

func (vetvetja *TInterruptManazhuesi) Init(hardwareinterruptoffset uint16, globaldescriptorTabela *TShareddescriptorTabela, procesManazhuesi *TProcesManazhuesi) {

	vetvetja.procesManazhuesi = procesManazhuesi

	vetvetja.hardwareinterruptoffset = hardwareinterruptoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var Idtinterruptgate uint8 = 0xE
	address = uint32(ValueOf(interruptignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
		vetvetja.InterruptdescriptorTabelaentryCaktoni(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	vetvetja.InterruptdescriptorTabelaentryCaktoni(0x82, codesegment, address, 3, Idtinterruptgate)

	PortaShkrimibyte(PrimarypicUrdhërioPorta, 0x11)
	PortaShkrimibyte(SecondarypicUrdhërioPorta, 0x11)

	PortaShkrimibyte(PrimarypicdataioPorta, 0x20)
	PortaShkrimibyte(SecondarypicdataioPorta, 0x28)

	PortaShkrimibyte(PrimarypicdataioPorta, 0x04)
	PortaShkrimibyte(SecondarypicdataioPorta, 0x02)

	PortaShkrimibyte(PrimarypicdataioPorta, 0x01)
	PortaShkrimibyte(SecondarypicdataioPorta, 0x01)

	PortaShkrimibyte(PrimarypicdataioPorta, 0xF8)
	PortaShkrimibyte(SecondarypicdataioPorta, 0xEF)

	idtKursori := [6]uint8{0, 0, 0, 0, 0, 0}
	madhësia := (*uint16)(Pointer(&idtKursori[0]))
	(*madhësia) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtKursori[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtKursori)))
}
func Lidt(lidtaddr uintptr)

func (vetvetja *TInterruptManazhuesi) InterruptdescriptorTabelaentryCaktoni(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorLloji uint8) {

	handleraddressUlëtbits := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddressUlëtbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*reserved) = 0

	var Idtdescriptorpresent uint8 = 0x80
	futja := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*futja) = (Idtdescriptorpresent | DescriptorLloji | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressLartëbits := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddressLartëbits) = uint16((handler >> 16) & 0xFFFF)

}

func (vetvetja *TInterruptManazhuesi) Caktonihandler(handler uintptr, Interruptnumber uint8) {
	handler_2[Interruptnumber] = handler
}
func (vetvetja *TInterruptManazhuesi) Gethandler(Interruptnumber uint8) uintptr {
	return handler_2[Interruptnumber]
}
func (vetvetja *TInterruptManazhuesi) Dohandleinterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptdebug {
		konsolë_2.MPrintoxy("[esp:", 1, 20)
		konsolë_2.MUnsignedinteger32Printo(uint32(interrupt))
		konsolë_2.MPrinto(":")
		konsolë_2.MUnsignedinteger32Printo(esp)
	}
	handlerEkzekuto := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerEkzekuto = true

	}

	if !handlerEkzekuto && interrupt == uint8(vetvetja.hardwareinterruptoffset) && vetvetja.procesManazhuesi != nil {
		esp = uint32(uintptr(Pointer(vetvetja.procesManazhuesi.Schedule((*TcpuGjendje)(Pointer(uintptr(esp)))))))

	}
	if !handlerEkzekuto && interrupt == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortaShkrimibyte(SecondarypicUrdhërioPorta, 0x20)
		}
		PortaShkrimibyte(PrimarypicUrdhërioPorta, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func caktonicr3(address uint32)

var konsolë_2 TKonsolë = TKonsolë{}

func Handleinterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptdebug && interrupt != 0x80 && interrupt != 0x20 {
		konsolë_2.MPrintoxy("[esp:", 1, 21)
		konsolë_2.MUnsignedinteger32Printo(uint32(interrupt))
		konsolë_2.MPrinto(":")
		konsolë_2.MUnsignedinteger32Printo(esp)
	}

	if AktivinterruptManazhuesi != 0 {
		p := (*TInterruptManazhuesi)(Pointer(AktivinterruptManazhuesi))
		esp = p.Dohandleinterrupt(uint8(interrupt), esp)
		return esp
	}
	if handler_2[interrupt] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
	}
	if interrupt == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortaShkrimibyte(SecondarypicUrdhërioPorta, 0x20)
		}
		PortaShkrimibyte(PrimarypicUrdhërioPorta, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuGjendje)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptDaljaloop).Pointer())
		cpu.Cs = Segkernelcode
		cpu.Ds = Segkerneldata
		cpu.Es = Segkerneldata
		cpu.Fs = Segkerneldata
		cpu.Gs = Segkernelgs
		cpu.Ss = Segkerneldata
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasGabimcode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionEmri(interrupt uint32) string {
	switch interrupt {
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

func exceptionKornizëVlera(kornizë uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(kornizë + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func printofaqefaultinfo(err uint32) {
	MEmergencyRegjistërvarg(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencyRegjistërvarg("protection")
	} else {
		MEmergencyRegjistërvarg("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencyRegjistërvarg(",write")
	} else {
		MEmergencyRegjistërvarg(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencyRegjistërvarg(",user")
	} else {
		MEmergencyRegjistërvarg(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencyRegjistërvarg(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencyRegjistërvarg(",instruction-fetch")
	}
	MEmergencyRegjistërvarg("]")
}

func printoexceptionselectorinfo(err uint32) {
	MEmergencyRegjistërvarg(" selector=")
	MEmergencyRegjistërunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencyRegjistërvarg(" index=")
	MEmergencyRegjistërunsignedinteger32(err >> 3)
	MEmergencyRegjistërvarg(" table=")
	if (err & 0x02) != 0 {
		MEmergencyRegjistërvarg("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencyRegjistërvarg("LDT")
	} else {
		MEmergencyRegjistërvarg("GDT")
	}
	MEmergencyRegjistërvarg(" ext=")
	MEmergencyRegjistërunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, interrupt uint32) uint32 {
	MEmergencyRegjistërvarg("\nEXCEPTION vec=")
	MEmergencyRegjistërhexadecimal8(uint8(interrupt))
	MEmergencyRegjistërvarg(" ")
	MEmergencyRegjistërvarg(exceptionEmri(interrupt))
	MEmergencyRegjistërvarg(" frame=")
	MEmergencyRegjistërunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyRegjistërvarg(" invalid-frame")
		if exceptionhasGabimcode(interrupt) {
			MEmergencyRegjistërvarg(" raw-error-or-bad-esp=")
			MEmergencyRegjistërunsignedinteger32(esp)
			printoexceptionselectorinfo(esp)
		}
		MEmergencyRegjistërvarg("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasGabimcode(interrupt) {
		err = exceptionKornizëVlera(esp, 0)
		eipoffset = 4
	}
	eip := exceptionKornizëVlera(esp, eipoffset)
	cs := exceptionKornizëVlera(esp, eipoffset+4)
	eflags := exceptionKornizëVlera(esp, eipoffset+8)

	MEmergencyRegjistërvarg(" err=")
	MEmergencyRegjistërunsignedinteger32(err)
	MEmergencyRegjistërvarg(" eip=")
	MEmergencyRegjistërunsignedinteger32(eip)
	MEmergencyRegjistërvarg(" cs=")
	MEmergencyRegjistërunsignedinteger32(cs)
	MEmergencyRegjistërvarg(" eflags=")
	MEmergencyRegjistërunsignedinteger32(eflags)
	MEmergencyRegjistërvarg(" cr0=")
	MEmergencyRegjistërunsignedinteger32(exceptioncr0())
	MEmergencyRegjistërvarg(" cr3=")
	MEmergencyRegjistërunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencyRegjistërvarg(" cr2=")
		MEmergencyRegjistërunsignedinteger32(exceptioncr2())
		printofaqefaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencyRegjistërvarg(" useresp=")
		MEmergencyRegjistërunsignedinteger32(exceptionKornizëVlera(esp, eipoffset+12))
		MEmergencyRegjistërvarg(" ss=")
		MEmergencyRegjistërunsignedinteger32(exceptionKornizëVlera(esp, eipoffset+16))
	}

	if exceptionhasGabimcode(interrupt) {
		printoexceptionselectorinfo(err)
	}
	MEmergencyRegjistërvarg("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandlefatalinterruptKornizë(savedesp uint32, interrupt uint32) uint32 {
	Handleexception(savedesp+52, interrupt)
	haltafterfatalexception()
	return savedesp
}

func Interruptaktiv()
func (vetvetja *TInterruptManazhuesi) Aktiv() {
	if AktivinterruptManazhuesi != 0 {
		vetvetja.Deactive()
	}
	address := uintptr(Pointer(vetvetja))
	AktivinterruptManazhuesi = address
	Interruptaktiv()
}
func Interruptdeactive()
func (vetvetja *TInterruptManazhuesi) Deactive() {
	AktivinterruptManazhuesi = 0
	Interruptdeactive()
}

func Myhandleinterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konsolë_2 := TKonsolë{}
	konsolë_2.MPrinto(buffer)
	return esp
}
func MyProvo(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	konsolë_2 := TKonsolë{}
	konsolë_2.MPrinto(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konsolë_2 := TKonsolë{}
	konsolë_2.MPrinto(buffer)
	konsolë_2.MHexadecimalPrinto(0x40)
	return esp
}
func printoesp(esp uint32) {
	konsolë_2 := TKonsolë{}
	konsolë_2.MUnsignedinteger32Printoxy(esp, 20, 21)
}
func gettls() uint32
func Printotls() {

}
