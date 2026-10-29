/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupt

import . "unsafe"
import . "reflect"

import . "poort"
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

func ProefAfdrukken(positie uint8, data uint8)
func instellends(dssegment uint32)
func instellengs(gssegment uint32)
func interruptAfsluitenloop()

type TInterrupthandler struct {
	InterruptGetal		uint8
	Interruptmanager	uintptr
}
type IInterrupthandler interface {
	Handgreepinterrupt(uint32) uint32
}

func Nieuwinterrupthandler(Interruptmanager uintptr, InterruptGetal uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.InterruptGetal = InterruptGetal
	interrupthandler_2.Interruptmanager = Interruptmanager
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (zelf *TInterrupthandler) Init(InterruptGetal uint8, Interruptmanager uintptr, funcaddress uintptr) {

	handler_2[InterruptGetal] = funcaddress

	zelf.InterruptGetal = InterruptGetal
	zelf.Interruptmanager = Interruptmanager

}
func (zelf *TInterrupthandler) InstellenHandgreepinterruptfuction(InterruptGetal uint32, address uintptr) {
	handler_2[InterruptGetal] = address
}
func (zelf *TInterrupthandler) Vernietigen() {
	zelfuintptr := uintptr(Pointer(zelf))
	Interruptmanager := (*TInterruptmanager)(Pointer(zelf.Interruptmanager))
	if zelfuintptr == Interruptmanager.Gethandler(zelf.InterruptGetal) {
		Interruptmanager.Instellenhandler(0, zelf.InterruptGetal)
	}

}
func (zelf *TInterrupthandler) Instelleninterruptmanager(Interruptmanager uintptr) {
}
func (zelf *TInterrupthandler) InstelleninterruptGetal(InterruptGetal uint8) {
	zelf.InterruptGetal = InterruptGetal
}
func (zelf *TInterrupthandler) Handgreepinterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MAfdrukken(buffer)
	return esp
}
func Handgreepinterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MAfdrukken(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptorTabelMuisaanwijzer struct {
}

var idtdata [256 * 8]uint8
var Actiefinterruptmanager uintptr = 0

const interruptDebuggen = false

type TInterruptmanager struct {
	handler_2	[256]uintptr

	apparatuurinterruptVerschuiving	uint16

	taakmanager	*TTaakmanager
}

var PrimarypicOpdrachtioPoort uint16 = 0x20
var PrimarypicdataioPoort uint16 = 0x21
var SecondarypicOpdrachtioPoort uint16 = 0xA0
var SecondarypicdataioPoort uint16 = 0xA1

func (zelf *TInterruptmanager) Init(apparatuurinterruptVerschuiving uint16, algemeendescriptorTabel *TShareddescriptorTabel, taakmanager *TTaakmanager) {

	zelf.taakmanager = taakmanager

	zelf.apparatuurinterruptVerschuiving = apparatuurinterruptVerschuiving
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
		zelf.InterruptdescriptorTabelItemInstellen(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	zelf.InterruptdescriptorTabelItemInstellen(0x82, codesegment, address, 3, Idtinterruptgate)

	PoortSchrijvenbyte(PrimarypicOpdrachtioPoort, 0x11)
	PoortSchrijvenbyte(SecondarypicOpdrachtioPoort, 0x11)

	PoortSchrijvenbyte(PrimarypicdataioPoort, 0x20)
	PoortSchrijvenbyte(SecondarypicdataioPoort, 0x28)

	PoortSchrijvenbyte(PrimarypicdataioPoort, 0x04)
	PoortSchrijvenbyte(SecondarypicdataioPoort, 0x02)

	PoortSchrijvenbyte(PrimarypicdataioPoort, 0x01)
	PoortSchrijvenbyte(SecondarypicdataioPoort, 0x01)

	PoortSchrijvenbyte(PrimarypicdataioPoort, 0xF8)
	PoortSchrijvenbyte(SecondarypicdataioPoort, 0xEF)

	idtMuisaanwijzer := [6]uint8{0, 0, 0, 0, 0, 0}
	grootte := (*uint16)(Pointer(&idtMuisaanwijzer[0]))
	(*grootte) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtMuisaanwijzer[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtMuisaanwijzer)))
}
func Lidt(lidtaddr uintptr)

func (zelf *TInterruptmanager) InterruptdescriptorTabelItemInstellen(interrupt int,
	codesegment uint16,
	handler uint32,
	DescriptorprivilegeNiveau uint8,
	DescriptorSoort uint8) {

	handleraddressLaagbits := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddressLaagbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	gereserveerd := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*gereserveerd) = 0

	var IdtdescriptorAanwezig uint8 = 0x80
	toegang := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*toegang) = (IdtdescriptorAanwezig | DescriptorSoort | ((DescriptorprivilegeNiveau & 3) << 5))

	handleraddressHoogbits := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddressHoogbits) = uint16((handler >> 16) & 0xFFFF)

}

func (zelf *TInterruptmanager) Instellenhandler(handler uintptr, InterruptGetal uint8) {
	handler_2[InterruptGetal] = handler
}
func (zelf *TInterruptmanager) Gethandler(InterruptGetal uint8) uintptr {
	return handler_2[InterruptGetal]
}
func (zelf *TInterruptmanager) DoHandgreepinterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptDebuggen {
		console_2.MAfdrukkenxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Afdrukken(uint32(interrupt))
		console_2.MAfdrukken(":")
		console_2.MUnsignedinteger32Afdrukken(esp)
	}
	handlerUitvoeren := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerUitvoeren = true

	}

	if !handlerUitvoeren && interrupt == uint8(zelf.apparatuurinterruptVerschuiving) && zelf.taakmanager != nil {
		esp = uint32(uintptr(Pointer(zelf.taakmanager.Schedule((*TcpuStatus)(Pointer(uintptr(esp)))))))

	}
	if !handlerUitvoeren && interrupt == 0x80 {
		esp = handgreepunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PoortSchrijvenbyte(SecondarypicOpdrachtioPoort, 0x20)
		}
		PoortSchrijvenbyte(PrimarypicOpdrachtioPoort, 0x20)
	}
	return esp
}

var aantal2 uint8 = 1

func instellencr3(address uint32)

var console_2 TConsole = TConsole{}

func Handgreepinterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptDebuggen && interrupt != 0x80 && interrupt != 0x20 {
		console_2.MAfdrukkenxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Afdrukken(uint32(interrupt))
		console_2.MAfdrukken(":")
		console_2.MUnsignedinteger32Afdrukken(esp)
	}

	if Actiefinterruptmanager != 0 {
		p := (*TInterruptmanager)(Pointer(Actiefinterruptmanager))
		esp = p.DoHandgreepinterrupt(uint8(interrupt), esp)
		return esp
	}
	if handler_2[interrupt] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
	}
	if interrupt == 0x80 {
		return handgreepunhandledsyscall(esp)
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PoortSchrijvenbyte(SecondarypicOpdrachtioPoort, 0x20)
		}
		PoortSchrijvenbyte(PrimarypicOpdrachtioPoort, 0x20)
	}

	return esp
}

func handgreepunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStatus)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptAfsluitenloop).Pointer())
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

func exceptionhasFoutcode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNaam(interrupt uint32) string {
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

func exceptionframeWaarde(frame uint32, verschuiving uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(frame + verschuiving)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func afdrukkenPaginafaultInformatie(fout uint32) {
	MEmergencyLogboekTekstsnoer(" pf=[")
	if (fout & 0x01) != 0 {
		MEmergencyLogboekTekstsnoer("protection")
	} else {
		MEmergencyLogboekTekstsnoer("not-present")
	}
	if (fout & 0x02) != 0 {
		MEmergencyLogboekTekstsnoer(",write")
	} else {
		MEmergencyLogboekTekstsnoer(",read")
	}
	if (fout & 0x04) != 0 {
		MEmergencyLogboekTekstsnoer(",user")
	} else {
		MEmergencyLogboekTekstsnoer(",kernel")
	}
	if (fout & 0x08) != 0 {
		MEmergencyLogboekTekstsnoer(",reserved-bit")
	}
	if (fout & 0x10) != 0 {
		MEmergencyLogboekTekstsnoer(",instruction-fetch")
	}
	MEmergencyLogboekTekstsnoer("]")
}

func afdrukkenexceptionselectorInformatie(fout uint32) {
	MEmergencyLogboekTekstsnoer(" selector=")
	MEmergencyLogboekunsignedinteger32(fout & 0xFFFFFFF8)
	MEmergencyLogboekTekstsnoer(" index=")
	MEmergencyLogboekunsignedinteger32(fout >> 3)
	MEmergencyLogboekTekstsnoer(" table=")
	if (fout & 0x02) != 0 {
		MEmergencyLogboekTekstsnoer("IDT")
	} else if (fout & 0x04) != 0 {
		MEmergencyLogboekTekstsnoer("LDT")
	} else {
		MEmergencyLogboekTekstsnoer("GDT")
	}
	MEmergencyLogboekTekstsnoer(" ext=")
	MEmergencyLogboekunsignedinteger32(fout & 0x01)
}

func Handgreepexception(esp uint32, interrupt uint32) uint32 {
	MEmergencyLogboekTekstsnoer("\nEXCEPTION vec=")
	MEmergencyLogboekhexadecimal8(uint8(interrupt))
	MEmergencyLogboekTekstsnoer(" ")
	MEmergencyLogboekTekstsnoer(exceptionNaam(interrupt))
	MEmergencyLogboekTekstsnoer(" frame=")
	MEmergencyLogboekunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyLogboekTekstsnoer(" invalid-frame")
		if exceptionhasFoutcode(interrupt) {
			MEmergencyLogboekTekstsnoer(" raw-error-or-bad-esp=")
			MEmergencyLogboekunsignedinteger32(esp)
			afdrukkenexceptionselectorInformatie(esp)
		}
		MEmergencyLogboekTekstsnoer("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var fout uint32 = 0
	var eipVerschuiving uint32 = 0
	if exceptionhasFoutcode(interrupt) {
		fout = exceptionframeWaarde(esp, 0)
		eipVerschuiving = 4
	}
	eip := exceptionframeWaarde(esp, eipVerschuiving)
	cs := exceptionframeWaarde(esp, eipVerschuiving+4)
	eflags := exceptionframeWaarde(esp, eipVerschuiving+8)

	MEmergencyLogboekTekstsnoer(" err=")
	MEmergencyLogboekunsignedinteger32(fout)
	MEmergencyLogboekTekstsnoer(" eip=")
	MEmergencyLogboekunsignedinteger32(eip)
	MEmergencyLogboekTekstsnoer(" cs=")
	MEmergencyLogboekunsignedinteger32(cs)
	MEmergencyLogboekTekstsnoer(" eflags=")
	MEmergencyLogboekunsignedinteger32(eflags)
	MEmergencyLogboekTekstsnoer(" cr0=")
	MEmergencyLogboekunsignedinteger32(exceptioncr0())
	MEmergencyLogboekTekstsnoer(" cr3=")
	MEmergencyLogboekunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencyLogboekTekstsnoer(" cr2=")
		MEmergencyLogboekunsignedinteger32(exceptioncr2())
		afdrukkenPaginafaultInformatie(fout)
	}

	if (cs & 0x03) != 0 {
		MEmergencyLogboekTekstsnoer(" useresp=")
		MEmergencyLogboekunsignedinteger32(exceptionframeWaarde(esp, eipVerschuiving+12))
		MEmergencyLogboekTekstsnoer(" ss=")
		MEmergencyLogboekunsignedinteger32(exceptionframeWaarde(esp, eipVerschuiving+16))
	}

	if exceptionhasFoutcode(interrupt) {
		afdrukkenexceptionselectorInformatie(fout)
	}
	MEmergencyLogboekTekstsnoer("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltNafatalexception()

func Handgreepfatalinterruptframe(opgeslagenesp uint32, interrupt uint32) uint32 {
	Handgreepexception(opgeslagenesp+52, interrupt)
	haltNafatalexception()
	return opgeslagenesp
}

func InterruptActief()
func (zelf *TInterruptmanager) Actief() {
	if Actiefinterruptmanager != 0 {
		zelf.Deactive()
	}
	address := uintptr(Pointer(zelf))
	Actiefinterruptmanager = address
	InterruptActief()
}
func Interruptdeactive()
func (zelf *TInterruptmanager) Deactive() {
	Actiefinterruptmanager = 0
	Interruptdeactive()
}

func MyHandgreepinterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MAfdrukken(buffer)
	return esp
}
func MyProef(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MAfdrukken(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MAfdrukken(buffer)
	console_2.MHexadecimalAfdrukken(0x40)
	return esp
}
func afdrukkenesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Afdrukkenxy(esp, 20, 21)
}
func gettls() uint32
func Afdrukkentls() {

}
