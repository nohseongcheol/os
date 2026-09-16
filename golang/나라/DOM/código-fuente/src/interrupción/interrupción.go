/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupción

import . "unsafe"
import . "reflect"

import . "puerto"
import . "gdt"
import . "múltiplegestiónTareas"
import . "consola"

func interrupciónignore()

func interrupciónexceptionhandler()
func interrupciónexceptionhandler0x00()
func interrupciónexceptionhandler0x01()
func interrupciónexceptionhandler0x02()
func interrupciónexceptionhandler0x03()
func interrupciónexceptionhandler0x04()
func interrupciónexceptionhandler0x05()
func interrupciónexceptionhandler0x06()
func interrupciónexceptionhandler0x07()
func interrupciónexceptionhandler0x08()
func interrupciónexceptionhandler0x09()
func interrupciónexceptionhandler0x0a()
func interrupciónexceptionhandler0x0b()
func interrupciónexceptionhandler0x0c()
func interrupciónexceptionhandler0x0d()
func interrupciónexceptionhandler0x0e()
func interrupciónexceptionhandler0x0f()
func interrupciónexceptionhandler0x10()
func interrupciónexceptionhandler0x11()
func interrupciónexceptionhandler0x12()
func interrupciónexceptionhandler0x13()

func interrupciónrequesthandler0x00()
func interrupciónrequesthandler0x01()
func interrupciónrequesthandler0x02()
func interrupciónrequesthandler0x03()
func interrupciónrequesthandler0x04()
func interrupciónrequesthandler0x05()
func interrupciónrequesthandler0x06()
func interrupciónrequesthandler0x07()
func interrupciónrequesthandler0x08()
func interrupciónrequesthandler0x09()
func interrupciónrequesthandler0x0a()
func interrupciónrequesthandler0x0b()
func interrupciónrequesthandler0x0c()
func interrupciónrequesthandler0x0d()
func interrupciónrequesthandler0x0e()
func interrupciónrequesthandler0x0f()

func interrupciónrequesthandler0x80()
func interrupciónrequesthandler0x81()
func interrupciónrequesthandler0x82()

func ProbarImprimir(posición uint8, datos uint8)
func establecerds(dssegment uint32)
func establecergs(gssegment uint32)
func interrupciónSalirBucle()

type TInterrupciónhandler struct {
	InterrupciónNúmero	uint8
	Interrupcióngestor	uintptr
}
type IInterrupciónhandler interface {
	Manijainterrupción(uint32) uint32
}

func Nuevointerrupciónhandler(Interrupcióngestor uintptr, InterrupciónNúmero uint8) *TInterrupciónhandler {
	interrupciónhandler_2 := new(TInterrupciónhandler)
	interrupciónhandler_2.InterrupciónNúmero = InterrupciónNúmero
	interrupciónhandler_2.Interrupcióngestor = Interrupcióngestor
	return interrupciónhandler_2

}

var handler_2 [256]uintptr

func (propio *TInterrupciónhandler) Init(InterrupciónNúmero uint8, Interrupcióngestor uintptr, funcDirección uintptr) {

	handler_2[InterrupciónNúmero] = funcDirección

	propio.InterrupciónNúmero = InterrupciónNúmero
	propio.Interrupcióngestor = Interrupcióngestor

}
func (propio *TInterrupciónhandler) EstablecerManijainterrupciónfuction(InterrupciónNúmero uint32, dirección uintptr) {
	handler_2[InterrupciónNúmero] = dirección
}
func (propio *TInterrupciónhandler) Destruir() {
	propiouintptr := uintptr(Pointer(propio))
	Interrupcióngestor := (*TInterrupcióngestor)(Pointer(propio.Interrupcióngestor))
	if propiouintptr == Interrupcióngestor.Gethandler(propio.InterrupciónNúmero) {
		Interrupcióngestor.Establecerhandler(0, propio.InterrupciónNúmero)
	}

}
func (propio *TInterrupciónhandler) Establecerinterrupcióngestor(Interrupcióngestor uintptr) {
}
func (propio *TInterrupciónhandler) EstablecerinterrupciónNúmero(InterrupciónNúmero uint8) {
	propio.InterrupciónNúmero = InterrupciónNúmero
}
func (propio *TInterrupciónhandler) Manijainterrupción(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	consola_2 := TConsola{}
	consola_2.MImprimir(buffer)
	return esp
}
func Manijainterrupción1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	consola_2 := TConsola{}
	consola_2.MImprimir(buffer)
}

type TPuertadescriptor struct {
	puertadatos [8]uint8
}
type TInterrupcióndescriptorTablaPuntero struct {
}

var idtdatos [256 * 8]uint8
var Activointerrupcióngestor uintptr = 0

const interrupciónDepurar = false

type TInterrupcióngestor struct {
	handler_2	[256]uintptr

	hardwareinterrupciónDesplazamiento	uint16

	tareagestor	*TTareagestor
}

var PrimarypicOrdenESpuerto uint16 = 0x20
var PrimarypicdatosESpuerto uint16 = 0x21
var SecondarypicOrdenESpuerto uint16 = 0xA0
var SecondarypicdatosESpuerto uint16 = 0xA1

func (propio *TInterrupcióngestor) Init(hardwareinterrupciónDesplazamiento uint16, globaldescriptorTabla *TShareddescriptorTabla, tareagestor *TTareagestor) {

	propio.tareagestor = tareagestor

	propio.hardwareinterrupciónDesplazamiento = hardwareinterrupciónDesplazamiento
	codesegment := uint16(Segnúcleocode)

	for i := 0; i < (256 * 8); i++ {
		idtdatos[i] = 0
	}
	var dirección uint32
	var Idtinterrupciónpuerta uint8 = 0xE
	dirección = uint32(ValueOf(interrupciónignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		dirección = uint32(ValueOf(interrupciónexceptionhandler0x0f).Pointer())
		propio.InterrupcióndescriptorTablaentradaestablecer(i, codesegment, dirección, 0, Idtinterrupciónpuerta)
	}

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x00).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x00, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x01).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x01, codesegment, dirección, 0, Idtinterrupciónpuerta)
	dirección = uint32(ValueOf(interrupciónexceptionhandler0x02).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x02, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x03).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x03, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x04).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x04, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x05).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x05, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x06).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x06, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x07).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x07, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x08).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x08, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x09).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x09, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x0a).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x0A, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x0b).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x0B, codesegment, dirección, 0, Idtinterrupciónpuerta)
	dirección = uint32(ValueOf(interrupciónexceptionhandler0x0c).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x0C, codesegment, dirección, 0, Idtinterrupciónpuerta)
	dirección = uint32(ValueOf(interrupciónexceptionhandler0x0d).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x0D, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x0e).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x0E, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x0f).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x0F, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x10).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x10, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x11).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x11, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x12).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x12, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónexceptionhandler0x13).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x13, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x00).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x20, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x01).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x21, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x02).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x22, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x03).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x23, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x04).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x24, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x05).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x25, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x06).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x26, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x07).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x27, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x08).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x28, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x09).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x29, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x0a).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x2A, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x0b).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x2B, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x0c).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x2C, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x0d).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x2D, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x0e).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x2E, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x0f).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x2F, codesegment, dirección, 0, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x80).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x80, codesegment, dirección, 3, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x81).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x81, codesegment, dirección, 3, Idtinterrupciónpuerta)

	dirección = uint32(ValueOf(interrupciónrequesthandler0x82).Pointer())
	propio.InterrupcióndescriptorTablaentradaestablecer(0x82, codesegment, dirección, 3, Idtinterrupciónpuerta)

	Puertoescribirocteto(PrimarypicOrdenESpuerto, 0x11)
	Puertoescribirocteto(SecondarypicOrdenESpuerto, 0x11)

	Puertoescribirocteto(PrimarypicdatosESpuerto, 0x20)
	Puertoescribirocteto(SecondarypicdatosESpuerto, 0x28)

	Puertoescribirocteto(PrimarypicdatosESpuerto, 0x04)
	Puertoescribirocteto(SecondarypicdatosESpuerto, 0x02)

	Puertoescribirocteto(PrimarypicdatosESpuerto, 0x01)
	Puertoescribirocteto(SecondarypicdatosESpuerto, 0x01)

	Puertoescribirocteto(PrimarypicdatosESpuerto, 0xF8)
	Puertoescribirocteto(SecondarypicdatosESpuerto, 0xEF)

	idtPuntero := [6]uint8{0, 0, 0, 0, 0, 0}
	tamaño := (*uint16)(Pointer(&idtPuntero[0]))
	(*tamaño) = (uint16)(Sizeof(idtdatos) - 1)

	base := (*uint32)(Pointer(&idtPuntero[2]))
	(*base) = uint32(uintptr(Pointer(&idtdatos)))

	Lidt(uintptr(Pointer(&idtPuntero)))
}
func Lidt(lidtaddr uintptr)

func (propio *TInterrupcióngestor) InterrupcióndescriptorTablaentradaestablecer(interrupción int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptortipo uint8) {

	handlerDirecciónBajabits := (*uint16)(Pointer(&idtdatos[interrupción*8+0]))
	(*handlerDirecciónBajabits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdatos[interrupción*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reservado := (*uint8)(Pointer(&idtdatos[interrupción*8+4]))
	(*reservado) = 0

	var IdtdescriptorPresente uint8 = 0x80
	acceso := (*uint8)(Pointer(&idtdatos[interrupción*8+5]))
	(*acceso) = (IdtdescriptorPresente | Descriptortipo | ((Descriptorprivilegelevel & 3) << 5))

	handlerDirecciónAltabits := (*uint16)(Pointer(&idtdatos[interrupción*8+6]))
	(*handlerDirecciónAltabits) = uint16((handler >> 16) & 0xFFFF)

}

func (propio *TInterrupcióngestor) Establecerhandler(handler uintptr, InterrupciónNúmero uint8) {
	handler_2[InterrupciónNúmero] = handler
}
func (propio *TInterrupcióngestor) Gethandler(InterrupciónNúmero uint8) uintptr {
	return handler_2[InterrupciónNúmero]
}
func (propio *TInterrupcióngestor) DoManijainterrupción(interrupción uint8, esp uint32) uint32 {

	if interrupciónDepurar {
		consola_2.MImprimirxy("[esp:", 1, 20)
		consola_2.MUnsignedinteger32Imprimir(uint32(interrupción))
		consola_2.MImprimir(":")
		consola_2.MUnsignedinteger32Imprimir(esp)
	}
	handlerEjecutar := false
	if handler_2[interrupción] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupción])))
		esp = myfunction(esp)
		handlerEjecutar = true

	}

	if !handlerEjecutar && interrupción == uint8(propio.hardwareinterrupciónDesplazamiento) && propio.tareagestor != nil {
		esp = uint32(uintptr(Pointer(propio.tareagestor.Schedule((*TcpuEstado)(Pointer(uintptr(esp)))))))

	}
	if !handlerEjecutar && interrupción == 0x80 {
		esp = manijaunhandledsyscall(esp)
	}

	if interrupción <= 0x1F {
	}
	if 0x20 <= interrupción && interrupción < 0x30 {
		if 0x28 <= interrupción {
			Puertoescribirocteto(SecondarypicOrdenESpuerto, 0x20)
		}
		Puertoescribirocteto(PrimarypicOrdenESpuerto, 0x20)
	}
	return esp
}

var recuento2 uint8 = 1

func establecercr3(dirección uint32)

var consola_2 TConsola = TConsola{}

func Manijainterrupción(esp uint32, interrupción uint32) uint32 {

	if interrupciónDepurar && interrupción != 0x80 && interrupción != 0x20 {
		consola_2.MImprimirxy("[esp:", 1, 21)
		consola_2.MUnsignedinteger32Imprimir(uint32(interrupción))
		consola_2.MImprimir(":")
		consola_2.MUnsignedinteger32Imprimir(esp)
	}

	if Activointerrupcióngestor != 0 {
		p := (*TInterrupcióngestor)(Pointer(Activointerrupcióngestor))
		esp = p.DoManijainterrupción(uint8(interrupción), esp)
		return esp
	}
	if handler_2[interrupción] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupción])))
		esp = myfunction(esp)
	}
	if interrupción == 0x80 {
		return manijaunhandledsyscall(esp)
	}
	if 0x20 <= interrupción && interrupción < 0x30 {
		if 0x28 <= interrupción {
			Puertoescribirocteto(SecondarypicOrdenESpuerto, 0x20)
		}
		Puertoescribirocteto(PrimarypicOrdenESpuerto, 0x20)
	}

	return esp
}

func manijaunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuEstado)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interrupciónSalirBucle).Pointer())
		cpu.Cs = Segnúcleocode
		cpu.Ds = Segnúcleodatos
		cpu.Es = Segnúcleodatos
		cpu.Fs = Segnúcleodatos
		cpu.Gs = Segnúcleogs
		cpu.Ss = Segnúcleodatos
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhaserrorcode(interrupción uint32) bool {
	switch interrupción {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNombre(interrupción uint32) string {
	switch interrupción {
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

func exceptiontramaValor(trama uint32, desplazamiento uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(trama + desplazamiento)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func imprimirpáginafalloInformación(err uint32) {
	MEmergencyRegistroCadena(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencyRegistroCadena("protection")
	} else {
		MEmergencyRegistroCadena("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencyRegistroCadena(",write")
	} else {
		MEmergencyRegistroCadena(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencyRegistroCadena(",user")
	} else {
		MEmergencyRegistroCadena(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencyRegistroCadena(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencyRegistroCadena(",instruction-fetch")
	}
	MEmergencyRegistroCadena("]")
}

func imprimirexceptionselectorInformación(err uint32) {
	MEmergencyRegistroCadena(" selector=")
	MEmergencyRegistrounsignedinteger32(err & 0xFFFFFFF8)
	MEmergencyRegistroCadena(" index=")
	MEmergencyRegistrounsignedinteger32(err >> 3)
	MEmergencyRegistroCadena(" table=")
	if (err & 0x02) != 0 {
		MEmergencyRegistroCadena("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencyRegistroCadena("LDT")
	} else {
		MEmergencyRegistroCadena("GDT")
	}
	MEmergencyRegistroCadena(" ext=")
	MEmergencyRegistrounsignedinteger32(err & 0x01)
}

func Manijaexception(esp uint32, interrupción uint32) uint32 {
	MEmergencyRegistroCadena("\nEXCEPTION vec=")
	MEmergencyRegistrohexadecimal8(uint8(interrupción))
	MEmergencyRegistroCadena(" ")
	MEmergencyRegistroCadena(exceptionNombre(interrupción))
	MEmergencyRegistroCadena(" frame=")
	MEmergencyRegistrounsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyRegistroCadena(" invalid-frame")
		if exceptionhaserrorcode(interrupción) {
			MEmergencyRegistroCadena(" raw-error-or-bad-esp=")
			MEmergencyRegistrounsignedinteger32(esp)
			imprimirexceptionselectorInformación(esp)
		}
		MEmergencyRegistroCadena("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipDesplazamiento uint32 = 0
	if exceptionhaserrorcode(interrupción) {
		err = exceptiontramaValor(esp, 0)
		eipDesplazamiento = 4
	}
	eip := exceptiontramaValor(esp, eipDesplazamiento)
	cs := exceptiontramaValor(esp, eipDesplazamiento+4)
	eflags := exceptiontramaValor(esp, eipDesplazamiento+8)

	MEmergencyRegistroCadena(" err=")
	MEmergencyRegistrounsignedinteger32(err)
	MEmergencyRegistroCadena(" eip=")
	MEmergencyRegistrounsignedinteger32(eip)
	MEmergencyRegistroCadena(" cs=")
	MEmergencyRegistrounsignedinteger32(cs)
	MEmergencyRegistroCadena(" eflags=")
	MEmergencyRegistrounsignedinteger32(eflags)
	MEmergencyRegistroCadena(" cr0=")
	MEmergencyRegistrounsignedinteger32(exceptioncr0())
	MEmergencyRegistroCadena(" cr3=")
	MEmergencyRegistrounsignedinteger32(exceptioncr3())

	if interrupción == 0x0E {
		MEmergencyRegistroCadena(" cr2=")
		MEmergencyRegistrounsignedinteger32(exceptioncr2())
		imprimirpáginafalloInformación(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencyRegistroCadena(" useresp=")
		MEmergencyRegistrounsignedinteger32(exceptiontramaValor(esp, eipDesplazamiento+12))
		MEmergencyRegistroCadena(" ss=")
		MEmergencyRegistrounsignedinteger32(exceptiontramaValor(esp, eipDesplazamiento+16))
	}

	if exceptionhaserrorcode(interrupción) {
		imprimirexceptionselectorInformación(err)
	}
	MEmergencyRegistroCadena("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltDespuésfatalexception()

func Manijafatalinterrupcióntrama(guardadoesp uint32, interrupción uint32) uint32 {
	Manijaexception(guardadoesp+52, interrupción)
	haltDespuésfatalexception()
	return guardadoesp
}

func InterrupciónActivo()
func (propio *TInterrupcióngestor) Activo() {
	if Activointerrupcióngestor != 0 {
		propio.Deactive()
	}
	dirección := uintptr(Pointer(propio))
	Activointerrupcióngestor = dirección
	InterrupciónActivo()
}
func Interrupcióndeactive()
func (propio *TInterrupcióngestor) Deactive() {
	Activointerrupcióngestor = 0
	Interrupcióndeactive()
}

func MyManijainterrupción(interrupción uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	consola_2 := TConsola{}
	consola_2.MImprimir(buffer)
	return esp
}
func MyProbar(interrupción uint8, esp uint32)

func Unhandleinterrupción() {
	buffer := []byte("unhandle interrupt\n")
	consola_2 := TConsola{}
	consola_2.MImprimir(buffer)
}

func interrupciónhandler_2(interrupción uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	consola_2 := TConsola{}
	consola_2.MImprimir(buffer)
	consola_2.MHexadecimalImprimir(0x40)
	return esp
}
func imprimiresp(esp uint32) {
	consola_2 := TConsola{}
	consola_2.MUnsignedinteger32Imprimirxy(esp, 20, 21)
}
func gettls() uint32
func Imprimirtls() {

}
