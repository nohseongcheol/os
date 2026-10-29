/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupt

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

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

func PrófunPrenta(staða uint8, data uint8)
func setjads(dssegment uint32)
func setjags(gssegment uint32)
func interruptHættaloop()

type TInterrupthandler struct {
	Interruptnumber		uint8
	Interruptmanager	uintptr
}
type IInterrupthandler interface {
	Haldfanginterrupt(uint32) uint32
}

func Nýttinterrupthandler(Interruptmanager uintptr, Interruptnumber uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.Interruptnumber = Interruptnumber
	interrupthandler_2.Interruptmanager = Interruptmanager
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (sjálft *TInterrupthandler) Init(Interruptnumber uint8, Interruptmanager uintptr, funcaddress uintptr) {

	handler_2[Interruptnumber] = funcaddress

	sjálft.Interruptnumber = Interruptnumber
	sjálft.Interruptmanager = Interruptmanager

}
func (sjálft *TInterrupthandler) SetjaHaldfanginterruptfuction(Interruptnumber uint32, address uintptr) {
	handler_2[Interruptnumber] = address
}
func (sjálft *TInterrupthandler) Eyðileggja() {
	sjálftuintptr := uintptr(Pointer(sjálft))
	Interruptmanager := (*TInterruptmanager)(Pointer(sjálft.Interruptmanager))
	if sjálftuintptr == Interruptmanager.Gethandler(sjálft.Interruptnumber) {
		Interruptmanager.Setjahandler(0, sjálft.Interruptnumber)
	}

}
func (sjálft *TInterrupthandler) Setjainterruptmanager(Interruptmanager uintptr) {
}
func (sjálft *TInterrupthandler) Setjainterruptnumber(Interruptnumber uint8) {
	sjálft.Interruptnumber = Interruptnumber
}
func (sjálft *TInterrupthandler) Haldfanginterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MPrenta(buffer)
	return esp
}
func Haldfanginterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MPrenta(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptorTaflaBendill struct {
}

var idtdata [256 * 8]uint8
var Virktinterruptmanager uintptr = 0

const interruptAflúsa = false

type TInterruptmanager struct {
	handler_2	[256]uintptr

	vélbúnaðurinterruptoffset	uint16

	verkmanager	*TVerkmanager
}

var PrimarypicSkipunioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicSkipunioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (sjálft *TInterruptmanager) Init(vélbúnaðurinterruptoffset uint16, víðværtdescriptorTafla *TShareddescriptorTafla, verkmanager *TVerkmanager) {

	sjálft.verkmanager = verkmanager

	sjálft.vélbúnaðurinterruptoffset = vélbúnaðurinterruptoffset
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
		sjálft.InterruptdescriptorTaflaentrySetja(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	sjálft.InterruptdescriptorTaflaentrySetja(0x82, codesegment, address, 3, Idtinterruptgate)

	PortSkriftbyte(PrimarypicSkipunioport, 0x11)
	PortSkriftbyte(SecondarypicSkipunioport, 0x11)

	PortSkriftbyte(Primarypicdataioport, 0x20)
	PortSkriftbyte(Secondarypicdataioport, 0x28)

	PortSkriftbyte(Primarypicdataioport, 0x04)
	PortSkriftbyte(Secondarypicdataioport, 0x02)

	PortSkriftbyte(Primarypicdataioport, 0x01)
	PortSkriftbyte(Secondarypicdataioport, 0x01)

	PortSkriftbyte(Primarypicdataioport, 0xF8)
	PortSkriftbyte(Secondarypicdataioport, 0xEF)

	idtBendill := [6]uint8{0, 0, 0, 0, 0, 0}
	stærð := (*uint16)(Pointer(&idtBendill[0]))
	(*stærð) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtBendill[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtBendill)))
}
func Lidt(lidtaddr uintptr)

func (sjálft *TInterruptmanager) InterruptdescriptorTaflaentrySetja(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTegund uint8) {

	handleraddressLágtbitar := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddressLágtbitar) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*reserved) = 0

	var Idtdescriptorpresent uint8 = 0x80
	aðgangur := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*aðgangur) = (Idtdescriptorpresent | DescriptorTegund | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressHáttbitar := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddressHáttbitar) = uint16((handler >> 16) & 0xFFFF)

}

func (sjálft *TInterruptmanager) Setjahandler(handler uintptr, Interruptnumber uint8) {
	handler_2[Interruptnumber] = handler
}
func (sjálft *TInterruptmanager) Gethandler(Interruptnumber uint8) uintptr {
	return handler_2[Interruptnumber]
}
func (sjálft *TInterruptmanager) DoHaldfanginterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptAflúsa {
		console_2.MPrentaxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Prenta(uint32(interrupt))
		console_2.MPrenta(":")
		console_2.MUnsignedinteger32Prenta(esp)
	}
	handlerKeyra := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerKeyra = true

	}

	if !handlerKeyra && interrupt == uint8(sjálft.vélbúnaðurinterruptoffset) && sjálft.verkmanager != nil {
		esp = uint32(uintptr(Pointer(sjálft.verkmanager.Schedule((*TcpuStaða)(Pointer(uintptr(esp)))))))

	}
	if !handlerKeyra && interrupt == 0x80 {
		esp = haldfangunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortSkriftbyte(SecondarypicSkipunioport, 0x20)
		}
		PortSkriftbyte(PrimarypicSkipunioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func setjacr3(address uint32)

var console_2 TConsole = TConsole{}

func Haldfanginterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptAflúsa && interrupt != 0x80 && interrupt != 0x20 {
		console_2.MPrentaxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Prenta(uint32(interrupt))
		console_2.MPrenta(":")
		console_2.MUnsignedinteger32Prenta(esp)
	}

	if Virktinterruptmanager != 0 {
		p := (*TInterruptmanager)(Pointer(Virktinterruptmanager))
		esp = p.DoHaldfanginterrupt(uint8(interrupt), esp)
		return esp
	}
	if handler_2[interrupt] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
	}
	if interrupt == 0x80 {
		return haldfangunhandledsyscall(esp)
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortSkriftbyte(SecondarypicSkipunioport, 0x20)
		}
		PortSkriftbyte(PrimarypicSkipunioport, 0x20)
	}

	return esp
}

func haldfangunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStaða)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptHættaloop).Pointer())
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

func exceptionhasVillacode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionHeiti(interrupt uint32) string {
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

func exceptionRammiGildi(rammi uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(rammi + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func prentasíðafaultUpplýsingar(villa uint32) {
	MEmergencylogStrengur(" pf=[")
	if (villa & 0x01) != 0 {
		MEmergencylogStrengur("protection")
	} else {
		MEmergencylogStrengur("not-present")
	}
	if (villa & 0x02) != 0 {
		MEmergencylogStrengur(",write")
	} else {
		MEmergencylogStrengur(",read")
	}
	if (villa & 0x04) != 0 {
		MEmergencylogStrengur(",user")
	} else {
		MEmergencylogStrengur(",kernel")
	}
	if (villa & 0x08) != 0 {
		MEmergencylogStrengur(",reserved-bit")
	}
	if (villa & 0x10) != 0 {
		MEmergencylogStrengur(",instruction-fetch")
	}
	MEmergencylogStrengur("]")
}

func prentaexceptionselectorUpplýsingar(villa uint32) {
	MEmergencylogStrengur(" selector=")
	MEmergencylogunsignedinteger32(villa & 0xFFFFFFF8)
	MEmergencylogStrengur(" index=")
	MEmergencylogunsignedinteger32(villa >> 3)
	MEmergencylogStrengur(" table=")
	if (villa & 0x02) != 0 {
		MEmergencylogStrengur("IDT")
	} else if (villa & 0x04) != 0 {
		MEmergencylogStrengur("LDT")
	} else {
		MEmergencylogStrengur("GDT")
	}
	MEmergencylogStrengur(" ext=")
	MEmergencylogunsignedinteger32(villa & 0x01)
}

func Haldfangexception(esp uint32, interrupt uint32) uint32 {
	MEmergencylogStrengur("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(interrupt))
	MEmergencylogStrengur(" ")
	MEmergencylogStrengur(exceptionHeiti(interrupt))
	MEmergencylogStrengur(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogStrengur(" invalid-frame")
		if exceptionhasVillacode(interrupt) {
			MEmergencylogStrengur(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			prentaexceptionselectorUpplýsingar(esp)
		}
		MEmergencylogStrengur("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var villa uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasVillacode(interrupt) {
		villa = exceptionRammiGildi(esp, 0)
		eipoffset = 4
	}
	eip := exceptionRammiGildi(esp, eipoffset)
	cs := exceptionRammiGildi(esp, eipoffset+4)
	eflags_2 := exceptionRammiGildi(esp, eipoffset+8)

	MEmergencylogStrengur(" err=")
	MEmergencylogunsignedinteger32(villa)
	MEmergencylogStrengur(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogStrengur(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogStrengur(" eflags=")
	MEmergencylogunsignedinteger32(eflags_2)
	MEmergencylogStrengur(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogStrengur(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencylogStrengur(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		prentasíðafaultUpplýsingar(villa)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogStrengur(" useresp=")
		MEmergencylogunsignedinteger32(exceptionRammiGildi(esp, eipoffset+12))
		MEmergencylogStrengur(" ss=")
		MEmergencylogunsignedinteger32(exceptionRammiGildi(esp, eipoffset+16))
	}

	if exceptionhasVillacode(interrupt) {
		prentaexceptionselectorUpplýsingar(villa)
	}
	MEmergencylogStrengur("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltEftirfatalexception()

func HaldfangfatalinterruptRammi(savedesp uint32, interrupt uint32) uint32 {
	Haldfangexception(savedesp+52, interrupt)
	haltEftirfatalexception()
	return savedesp
}

func InterruptVirkt()
func (sjálft *TInterruptmanager) Virkt() {
	if Virktinterruptmanager != 0 {
		sjálft.Deactive()
	}
	address := uintptr(Pointer(sjálft))
	Virktinterruptmanager = address
	InterruptVirkt()
}
func Interruptdeactive()
func (sjálft *TInterruptmanager) Deactive() {
	Virktinterruptmanager = 0
	Interruptdeactive()
}

func MyHaldfanginterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MPrenta(buffer)
	return esp
}
func MyPrófun(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MPrenta(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MPrenta(buffer)
	console_2.MHexadecimalPrenta(0x40)
	return esp
}
func prentaesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Prentaxy(esp, 20, 21)
}
func gettls() uint32
func Prentatls() {

}
