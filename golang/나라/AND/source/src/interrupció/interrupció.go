/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupció

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "consola"

func interrupcióignore()

func interrupcióexceptionhandler()
func interrupcióexceptionhandler0x00()
func interrupcióexceptionhandler0x01()
func interrupcióexceptionhandler0x02()
func interrupcióexceptionhandler0x03()
func interrupcióexceptionhandler0x04()
func interrupcióexceptionhandler0x05()
func interrupcióexceptionhandler0x06()
func interrupcióexceptionhandler0x07()
func interrupcióexceptionhandler0x08()
func interrupcióexceptionhandler0x09()
func interrupcióexceptionhandler0x0a()
func interrupcióexceptionhandler0x0b()
func interrupcióexceptionhandler0x0c()
func interrupcióexceptionhandler0x0d()
func interrupcióexceptionhandler0x0e()
func interrupcióexceptionhandler0x0f()
func interrupcióexceptionhandler0x10()
func interrupcióexceptionhandler0x11()
func interrupcióexceptionhandler0x12()
func interrupcióexceptionhandler0x13()

func interrupciórequesthandler0x00()
func interrupciórequesthandler0x01()
func interrupciórequesthandler0x02()
func interrupciórequesthandler0x03()
func interrupciórequesthandler0x04()
func interrupciórequesthandler0x05()
func interrupciórequesthandler0x06()
func interrupciórequesthandler0x07()
func interrupciórequesthandler0x08()
func interrupciórequesthandler0x09()
func interrupciórequesthandler0x0a()
func interrupciórequesthandler0x0b()
func interrupciórequesthandler0x0c()
func interrupciórequesthandler0x0d()
func interrupciórequesthandler0x0e()
func interrupciórequesthandler0x0f()

func interrupciórequesthandler0x80()
func interrupciórequesthandler0x81()
func interrupciórequesthandler0x82()

func ProvaImprimeix(posició uint8, data uint8)
func estableixds(dssegment uint32)
func estableixgs(gssegment uint32)
func interrupcióSurtloop()

type TInterrupcióhandler struct {
	InterrupcióNombre	uint8
	Interrupciómanager	uintptr
}
type IInterrupcióhandler interface {
	GestorInterrupció(uint32) uint32
}

func NouInterrupcióhandler(Interrupciómanager uintptr, InterrupcióNombre uint8) *TInterrupcióhandler {
	interrupcióhandler_2 := new(TInterrupcióhandler)
	interrupcióhandler_2.InterrupcióNombre = InterrupcióNombre
	interrupcióhandler_2.Interrupciómanager = Interrupciómanager
	return interrupcióhandler_2

}

var handler_2 [256]uintptr

func (unmateix *TInterrupcióhandler) Init(InterrupcióNombre uint8, Interrupciómanager uintptr, funcAdreça uintptr) {

	handler_2[InterrupcióNombre] = funcAdreça

	unmateix.InterrupcióNombre = InterrupcióNombre
	unmateix.Interrupciómanager = Interrupciómanager

}
func (unmateix *TInterrupcióhandler) EstableixGestorInterrupciófuction(InterrupcióNombre uint32, adreça uintptr) {
	handler_2[InterrupcióNombre] = adreça
}
func (unmateix *TInterrupcióhandler) Destrueix() {
	unmateixuintptr := uintptr(Pointer(unmateix))
	Interrupciómanager := (*TInterrupciómanager)(Pointer(unmateix.Interrupciómanager))
	if unmateixuintptr == Interrupciómanager.Gethandler(unmateix.InterrupcióNombre) {
		Interrupciómanager.Estableixhandler(0, unmateix.InterrupcióNombre)
	}

}
func (unmateix *TInterrupcióhandler) EstableixInterrupciómanager(Interrupciómanager uintptr) {
}
func (unmateix *TInterrupcióhandler) EstableixInterrupcióNombre(InterrupcióNombre uint8) {
	unmateix.InterrupcióNombre = InterrupcióNombre
}
func (unmateix *TInterrupcióhandler) GestorInterrupció(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	consola_2 := TConsola{}
	consola_2.MImprimeix(buffer)
	return esp
}
func GestorInterrupció1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	consola_2 := TConsola{}
	consola_2.MImprimeix(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterrupciódescriptorTaulaPunter struct {
}

var idtdata [256 * 8]uint8
var ActiuInterrupciómanager uintptr = 0

const interrupcióDepura = false

type TInterrupciómanager struct {
	handler_2	[256]uintptr

	maquinariInterrupcióoffset	uint16

	tascamanager	*TTascamanager
}

var PrimarypicOrdreESport uint16 = 0x20
var PrimarypicdataESport uint16 = 0x21
var SecondarypicOrdreESport uint16 = 0xA0
var SecondarypicdataESport uint16 = 0xA1

func (unmateix *TInterrupciómanager) Init(maquinariInterrupcióoffset uint16, globaldescriptorTaula *TShareddescriptorTaula, tascamanager *TTascamanager) {

	unmateix.tascamanager = tascamanager

	unmateix.maquinariInterrupcióoffset = maquinariInterrupcióoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var adreça uint32
	var IdtInterrupciógate uint8 = 0xE
	adreça = uint32(ValueOf(interrupcióignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		adreça = uint32(ValueOf(interrupcióexceptionhandler0x0f).Pointer())
		unmateix.InterrupciódescriptorTaulaentradaestableix(i, codesegment, adreça, 0, IdtInterrupciógate)
	}

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x00).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x00, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x01).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x01, codesegment, adreça, 0, IdtInterrupciógate)
	adreça = uint32(ValueOf(interrupcióexceptionhandler0x02).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x02, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x03).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x03, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x04).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x04, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x05).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x05, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x06).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x06, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x07).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x07, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x08).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x08, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x09).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x09, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x0a).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x0A, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x0b).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x0B, codesegment, adreça, 0, IdtInterrupciógate)
	adreça = uint32(ValueOf(interrupcióexceptionhandler0x0c).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x0C, codesegment, adreça, 0, IdtInterrupciógate)
	adreça = uint32(ValueOf(interrupcióexceptionhandler0x0d).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x0D, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x0e).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x0E, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x0f).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x0F, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x10).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x10, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x11).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x11, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x12).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x12, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupcióexceptionhandler0x13).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x13, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x00).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x20, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x01).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x21, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x02).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x22, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x03).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x23, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x04).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x24, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x05).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x25, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x06).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x26, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x07).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x27, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x08).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x28, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x09).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x29, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x0a).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x2A, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x0b).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x2B, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x0c).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x2C, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x0d).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x2D, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x0e).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x2E, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x0f).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x2F, codesegment, adreça, 0, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x80).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x80, codesegment, adreça, 3, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x81).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x81, codesegment, adreça, 3, IdtInterrupciógate)

	adreça = uint32(ValueOf(interrupciórequesthandler0x82).Pointer())
	unmateix.InterrupciódescriptorTaulaentradaestableix(0x82, codesegment, adreça, 3, IdtInterrupciógate)

	PortEscripturabyte(PrimarypicOrdreESport, 0x11)
	PortEscripturabyte(SecondarypicOrdreESport, 0x11)

	PortEscripturabyte(PrimarypicdataESport, 0x20)
	PortEscripturabyte(SecondarypicdataESport, 0x28)

	PortEscripturabyte(PrimarypicdataESport, 0x04)
	PortEscripturabyte(SecondarypicdataESport, 0x02)

	PortEscripturabyte(PrimarypicdataESport, 0x01)
	PortEscripturabyte(SecondarypicdataESport, 0x01)

	PortEscripturabyte(PrimarypicdataESport, 0xF8)
	PortEscripturabyte(SecondarypicdataESport, 0xEF)

	idtPunter := [6]uint8{0, 0, 0, 0, 0, 0}
	mida := (*uint16)(Pointer(&idtPunter[0]))
	(*mida) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtPunter[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtPunter)))
}
func Lidt(lidtaddr uintptr)

func (unmateix *TInterrupciómanager) InterrupciódescriptorTaulaentradaestableix(interrupció int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTipus uint8) {

	handlerAdreçaBaixabits := (*uint16)(Pointer(&idtdata[interrupció*8+0]))
	(*handlerAdreçaBaixabits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupció*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reservat := (*uint8)(Pointer(&idtdata[interrupció*8+4]))
	(*reservat) = 0

	var Idtdescriptorpresent uint8 = 0x80
	accés := (*uint8)(Pointer(&idtdata[interrupció*8+5]))
	(*accés) = (Idtdescriptorpresent | DescriptorTipus | ((Descriptorprivilegelevel & 3) << 5))

	handlerAdreçaAltabits := (*uint16)(Pointer(&idtdata[interrupció*8+6]))
	(*handlerAdreçaAltabits) = uint16((handler >> 16) & 0xFFFF)

}

func (unmateix *TInterrupciómanager) Estableixhandler(handler uintptr, InterrupcióNombre uint8) {
	handler_2[InterrupcióNombre] = handler
}
func (unmateix *TInterrupciómanager) Gethandler(InterrupcióNombre uint8) uintptr {
	return handler_2[InterrupcióNombre]
}
func (unmateix *TInterrupciómanager) DoGestorInterrupció(interrupció uint8, esp uint32) uint32 {

	if interrupcióDepura {
		consola_2.MImprimeixxy("[esp:", 1, 20)
		consola_2.MUnsignedinteger32Imprimeix(uint32(interrupció))
		consola_2.MImprimeix(":")
		consola_2.MUnsignedinteger32Imprimeix(esp)
	}
	handlerExecuta := false
	if handler_2[interrupció] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupció])))
		esp = myfunction(esp)
		handlerExecuta = true

	}

	if !handlerExecuta && interrupció == uint8(unmateix.maquinariInterrupcióoffset) && unmateix.tascamanager != nil {
		esp = uint32(uintptr(Pointer(unmateix.tascamanager.Schedule((*TcpuEstat)(Pointer(uintptr(esp)))))))

	}
	if !handlerExecuta && interrupció == 0x80 {
		esp = gestorunhandledsyscall(esp)
	}

	if interrupció <= 0x1F {
	}
	if 0x20 <= interrupció && interrupció < 0x30 {
		if 0x28 <= interrupció {
			PortEscripturabyte(SecondarypicOrdreESport, 0x20)
		}
		PortEscripturabyte(PrimarypicOrdreESport, 0x20)
	}
	return esp
}

var recompte2 uint8 = 1

func estableixcr3(adreça uint32)

var consola_2 TConsola = TConsola{}

func GestorInterrupció(esp uint32, interrupció uint32) uint32 {

	if interrupcióDepura && interrupció != 0x80 && interrupció != 0x20 {
		consola_2.MImprimeixxy("[esp:", 1, 21)
		consola_2.MUnsignedinteger32Imprimeix(uint32(interrupció))
		consola_2.MImprimeix(":")
		consola_2.MUnsignedinteger32Imprimeix(esp)
	}

	if ActiuInterrupciómanager != 0 {
		p := (*TInterrupciómanager)(Pointer(ActiuInterrupciómanager))
		esp = p.DoGestorInterrupció(uint8(interrupció), esp)
		return esp
	}
	if handler_2[interrupció] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupció])))
		esp = myfunction(esp)
	}
	if interrupció == 0x80 {
		return gestorunhandledsyscall(esp)
	}
	if 0x20 <= interrupció && interrupció < 0x30 {
		if 0x28 <= interrupció {
			PortEscripturabyte(SecondarypicOrdreESport, 0x20)
		}
		PortEscripturabyte(PrimarypicOrdreESport, 0x20)
	}

	return esp
}

func gestorunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuEstat)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interrupcióSurtloop).Pointer())
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

func exceptionhasshaproduïtunerrorcode(interrupció uint32) bool {
	switch interrupció {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNom(interrupció uint32) string {
	switch interrupció {
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

func exceptionMarcValor(marc uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(marc + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func imprimeixPàginafaultInformació(error uint32) {
	MEmergencyRegistreCadena(" pf=[")
	if (error & 0x01) != 0 {
		MEmergencyRegistreCadena("protection")
	} else {
		MEmergencyRegistreCadena("not-present")
	}
	if (error & 0x02) != 0 {
		MEmergencyRegistreCadena(",write")
	} else {
		MEmergencyRegistreCadena(",read")
	}
	if (error & 0x04) != 0 {
		MEmergencyRegistreCadena(",user")
	} else {
		MEmergencyRegistreCadena(",kernel")
	}
	if (error & 0x08) != 0 {
		MEmergencyRegistreCadena(",reserved-bit")
	}
	if (error & 0x10) != 0 {
		MEmergencyRegistreCadena(",instruction-fetch")
	}
	MEmergencyRegistreCadena("]")
}

func imprimeixexceptionselectorInformació(error uint32) {
	MEmergencyRegistreCadena(" selector=")
	MEmergencyRegistreunsignedinteger32(error & 0xFFFFFFF8)
	MEmergencyRegistreCadena(" index=")
	MEmergencyRegistreunsignedinteger32(error >> 3)
	MEmergencyRegistreCadena(" table=")
	if (error & 0x02) != 0 {
		MEmergencyRegistreCadena("IDT")
	} else if (error & 0x04) != 0 {
		MEmergencyRegistreCadena("LDT")
	} else {
		MEmergencyRegistreCadena("GDT")
	}
	MEmergencyRegistreCadena(" ext=")
	MEmergencyRegistreunsignedinteger32(error & 0x01)
}

func Gestorexception(esp uint32, interrupció uint32) uint32 {
	MEmergencyRegistreCadena("\nEXCEPTION vec=")
	MEmergencyRegistrehexadecimal8(uint8(interrupció))
	MEmergencyRegistreCadena(" ")
	MEmergencyRegistreCadena(exceptionNom(interrupció))
	MEmergencyRegistreCadena(" frame=")
	MEmergencyRegistreunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyRegistreCadena(" invalid-frame")
		if exceptionhasshaproduïtunerrorcode(interrupció) {
			MEmergencyRegistreCadena(" raw-error-or-bad-esp=")
			MEmergencyRegistreunsignedinteger32(esp)
			imprimeixexceptionselectorInformació(esp)
		}
		MEmergencyRegistreCadena("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var error uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasshaproduïtunerrorcode(interrupció) {
		error = exceptionMarcValor(esp, 0)
		eipoffset = 4
	}
	eip := exceptionMarcValor(esp, eipoffset)
	cs := exceptionMarcValor(esp, eipoffset+4)
	eflags := exceptionMarcValor(esp, eipoffset+8)

	MEmergencyRegistreCadena(" err=")
	MEmergencyRegistreunsignedinteger32(error)
	MEmergencyRegistreCadena(" eip=")
	MEmergencyRegistreunsignedinteger32(eip)
	MEmergencyRegistreCadena(" cs=")
	MEmergencyRegistreunsignedinteger32(cs)
	MEmergencyRegistreCadena(" eflags=")
	MEmergencyRegistreunsignedinteger32(eflags)
	MEmergencyRegistreCadena(" cr0=")
	MEmergencyRegistreunsignedinteger32(exceptioncr0())
	MEmergencyRegistreCadena(" cr3=")
	MEmergencyRegistreunsignedinteger32(exceptioncr3())

	if interrupció == 0x0E {
		MEmergencyRegistreCadena(" cr2=")
		MEmergencyRegistreunsignedinteger32(exceptioncr2())
		imprimeixPàginafaultInformació(error)
	}

	if (cs & 0x03) != 0 {
		MEmergencyRegistreCadena(" useresp=")
		MEmergencyRegistreunsignedinteger32(exceptionMarcValor(esp, eipoffset+12))
		MEmergencyRegistreCadena(" ss=")
		MEmergencyRegistreunsignedinteger32(exceptionMarcValor(esp, eipoffset+16))
	}

	if exceptionhasshaproduïtunerrorcode(interrupció) {
		imprimeixexceptionselectorInformació(error)
	}
	MEmergencyRegistreCadena("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func GestorfatalInterrupcióMarc(desadaesp uint32, interrupció uint32) uint32 {
	Gestorexception(desadaesp+52, interrupció)
	haltafterfatalexception()
	return desadaesp
}

func InterrupcióActiu()
func (unmateix *TInterrupciómanager) Actiu() {
	if ActiuInterrupciómanager != 0 {
		unmateix.Deactive()
	}
	adreça := uintptr(Pointer(unmateix))
	ActiuInterrupciómanager = adreça
	InterrupcióActiu()
}
func Interrupciódeactive()
func (unmateix *TInterrupciómanager) Deactive() {
	ActiuInterrupciómanager = 0
	Interrupciódeactive()
}

func MyGestorInterrupció(interrupció uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	consola_2 := TConsola{}
	consola_2.MImprimeix(buffer)
	return esp
}
func MyProva(interrupció uint8, esp uint32)

func UnhandleInterrupció() {
	buffer := []byte("unhandle interrupt\n")
	consola_2 := TConsola{}
	consola_2.MImprimeix(buffer)
}

func interrupcióhandler_2(interrupció uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	consola_2 := TConsola{}
	consola_2.MImprimeix(buffer)
	consola_2.MHexadecimalImprimeix(0x40)
	return esp
}
func imprimeixesp(esp uint32) {
	consola_2 := TConsola{}
	consola_2.MUnsignedinteger32Imprimeixxy(esp, 20, 21)
}
func gettls() uint32
func Imprimeixtls() {

}
