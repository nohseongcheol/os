package Interrupt

import . "unsafe"
import . "reflect"

import . "porta"
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

func ProvaStampa(posizione uint8, data uint8)
func impostads(dssegment uint32)
func impostags(gssegment uint32)
func interruptEsciloop()

type TInterrupthandler struct {
	InterruptNumero		uint8
	Interruptmanager	uintptr
}
type IInterrupthandler interface {
	Manigliainterrupt(uint32) uint32
}

func Nuovointerrupthandler(Interruptmanager uintptr, InterruptNumero uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.InterruptNumero = InterruptNumero
	interrupthandler_2.Interruptmanager = Interruptmanager
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (séstesso *TInterrupthandler) Init(InterruptNumero uint8, Interruptmanager uintptr, funcaddress uintptr) {

	handler_2[InterruptNumero] = funcaddress

	séstesso.InterruptNumero = InterruptNumero
	séstesso.Interruptmanager = Interruptmanager

}
func (séstesso *TInterrupthandler) ImpostaManigliainterruptfuction(InterruptNumero uint32, address uintptr) {
	handler_2[InterruptNumero] = address
}
func (séstesso *TInterrupthandler) Distruggi() {
	séstessouintptr := uintptr(Pointer(séstesso))
	Interruptmanager := (*TInterruptmanager)(Pointer(séstesso.Interruptmanager))
	if séstessouintptr == Interruptmanager.Gethandler(séstesso.InterruptNumero) {
		Interruptmanager.Impostahandler(0, séstesso.InterruptNumero)
	}

}
func (séstesso *TInterrupthandler) Impostainterruptmanager(Interruptmanager uintptr) {
}
func (séstesso *TInterrupthandler) ImpostainterruptNumero(InterruptNumero uint8) {
	séstesso.InterruptNumero = InterruptNumero
}
func (séstesso *TInterrupthandler) Manigliainterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MStampa(buffer)
	return esp
}
func Manigliainterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MStampa(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptorTabellaPuntatore struct {
}

var idtdata [256 * 8]uint8
var Attivointerruptmanager uintptr = 0

const interruptFaiildebug = false

type TInterruptmanager struct {
	handler_2	[256]uintptr

	hardwareinterruptoffset	uint16

	processomanager	*TProcessomanager
}

var PrimarypicComandoioPorta uint16 = 0x20
var PrimarypicdataioPorta uint16 = 0x21
var SecondarypicComandoioPorta uint16 = 0xA0
var SecondarypicdataioPorta uint16 = 0xA1

func (séstesso *TInterruptmanager) Init(hardwareinterruptoffset uint16, globaledescriptorTabella *TShareddescriptorTabella, processomanager *TProcessomanager) {

	séstesso.processomanager = processomanager

	séstesso.hardwareinterruptoffset = hardwareinterruptoffset
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
		séstesso.InterruptdescriptorTabellavoceImposta(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	séstesso.InterruptdescriptorTabellavoceImposta(0x82, codesegment, address, 3, Idtinterruptgate)

	PortaScritturabyte(PrimarypicComandoioPorta, 0x11)
	PortaScritturabyte(SecondarypicComandoioPorta, 0x11)

	PortaScritturabyte(PrimarypicdataioPorta, 0x20)
	PortaScritturabyte(SecondarypicdataioPorta, 0x28)

	PortaScritturabyte(PrimarypicdataioPorta, 0x04)
	PortaScritturabyte(SecondarypicdataioPorta, 0x02)

	PortaScritturabyte(PrimarypicdataioPorta, 0x01)
	PortaScritturabyte(SecondarypicdataioPorta, 0x01)

	PortaScritturabyte(PrimarypicdataioPorta, 0xF8)
	PortaScritturabyte(SecondarypicdataioPorta, 0xEF)

	idtPuntatore := [6]uint8{0, 0, 0, 0, 0, 0}
	dimensione := (*uint16)(Pointer(&idtPuntatore[0]))
	(*dimensione) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtPuntatore[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtPuntatore)))
}
func Lidt(lidtaddr uintptr)

func (séstesso *TInterruptmanager) InterruptdescriptorTabellavoceImposta(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTipo uint8) {

	handleraddressBassobit := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddressBassobit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	riservato := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*riservato) = 0

	var IdtdescriptorPresente uint8 = 0x80
	accesso := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*accesso) = (IdtdescriptorPresente | DescriptorTipo | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressAltobit := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddressAltobit) = uint16((handler >> 16) & 0xFFFF)

}

func (séstesso *TInterruptmanager) Impostahandler(handler uintptr, InterruptNumero uint8) {
	handler_2[InterruptNumero] = handler
}
func (séstesso *TInterruptmanager) Gethandler(InterruptNumero uint8) uintptr {
	return handler_2[InterruptNumero]
}
func (séstesso *TInterruptmanager) DoManigliainterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptFaiildebug {
		console_2.MStampaxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Stampa(uint32(interrupt))
		console_2.MStampa(":")
		console_2.MUnsignedinteger32Stampa(esp)
	}
	handlerEsegui := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerEsegui = true

	}

	if !handlerEsegui && interrupt == uint8(séstesso.hardwareinterruptoffset) && séstesso.processomanager != nil {
		esp = uint32(uintptr(Pointer(séstesso.processomanager.Schedule((*TcpuStato)(Pointer(uintptr(esp)))))))

	}
	if !handlerEsegui && interrupt == 0x80 {
		esp = manigliaunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortaScritturabyte(SecondarypicComandoioPorta, 0x20)
		}
		PortaScritturabyte(PrimarypicComandoioPorta, 0x20)
	}
	return esp
}

var conteggio2 uint8 = 1

func impostacr3(address uint32)

var console_2 TConsole = TConsole{}

func Manigliainterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptFaiildebug && interrupt != 0x80 && interrupt != 0x20 {
		console_2.MStampaxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Stampa(uint32(interrupt))
		console_2.MStampa(":")
		console_2.MUnsignedinteger32Stampa(esp)
	}

	if Attivointerruptmanager != 0 {
		p := (*TInterruptmanager)(Pointer(Attivointerruptmanager))
		esp = p.DoManigliainterrupt(uint8(interrupt), esp)
		return esp
	}
	if handler_2[interrupt] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
	}
	if interrupt == 0x80 {
		return manigliaunhandledsyscall(esp)
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortaScritturabyte(SecondarypicComandoioPorta, 0x20)
		}
		PortaScritturabyte(PrimarypicComandoioPorta, 0x20)
	}

	return esp
}

func manigliaunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStato)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptEsciloop).Pointer())
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

func exceptionhasErrorecode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNome(interrupt uint32) string {
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

func exceptionRiquadroValore(riquadro uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(riquadro + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func stampaPAGINAfaultInformazioni(errori uint32) {
	MEmergencyRegistroStringa(" pf=[")
	if (errori & 0x01) != 0 {
		MEmergencyRegistroStringa("protection")
	} else {
		MEmergencyRegistroStringa("not-present")
	}
	if (errori & 0x02) != 0 {
		MEmergencyRegistroStringa(",write")
	} else {
		MEmergencyRegistroStringa(",read")
	}
	if (errori & 0x04) != 0 {
		MEmergencyRegistroStringa(",user")
	} else {
		MEmergencyRegistroStringa(",kernel")
	}
	if (errori & 0x08) != 0 {
		MEmergencyRegistroStringa(",reserved-bit")
	}
	if (errori & 0x10) != 0 {
		MEmergencyRegistroStringa(",instruction-fetch")
	}
	MEmergencyRegistroStringa("]")
}

func stampaexceptionselectorInformazioni(errori uint32) {
	MEmergencyRegistroStringa(" selector=")
	MEmergencyRegistrounsignedinteger32(errori & 0xFFFFFFF8)
	MEmergencyRegistroStringa(" index=")
	MEmergencyRegistrounsignedinteger32(errori >> 3)
	MEmergencyRegistroStringa(" table=")
	if (errori & 0x02) != 0 {
		MEmergencyRegistroStringa("IDT")
	} else if (errori & 0x04) != 0 {
		MEmergencyRegistroStringa("LDT")
	} else {
		MEmergencyRegistroStringa("GDT")
	}
	MEmergencyRegistroStringa(" ext=")
	MEmergencyRegistrounsignedinteger32(errori & 0x01)
}

func Manigliaexception(esp uint32, interrupt uint32) uint32 {
	MEmergencyRegistroStringa("\nEXCEPTION vec=")
	MEmergencyRegistrohexadecimal8(uint8(interrupt))
	MEmergencyRegistroStringa(" ")
	MEmergencyRegistroStringa(exceptionNome(interrupt))
	MEmergencyRegistroStringa(" frame=")
	MEmergencyRegistrounsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyRegistroStringa(" invalid-frame")
		if exceptionhasErrorecode(interrupt) {
			MEmergencyRegistroStringa(" raw-error-or-bad-esp=")
			MEmergencyRegistrounsignedinteger32(esp)
			stampaexceptionselectorInformazioni(esp)
		}
		MEmergencyRegistroStringa("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var errori uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasErrorecode(interrupt) {
		errori = exceptionRiquadroValore(esp, 0)
		eipoffset = 4
	}
	eip := exceptionRiquadroValore(esp, eipoffset)
	cs := exceptionRiquadroValore(esp, eipoffset+4)
	eflags := exceptionRiquadroValore(esp, eipoffset+8)

	MEmergencyRegistroStringa(" err=")
	MEmergencyRegistrounsignedinteger32(errori)
	MEmergencyRegistroStringa(" eip=")
	MEmergencyRegistrounsignedinteger32(eip)
	MEmergencyRegistroStringa(" cs=")
	MEmergencyRegistrounsignedinteger32(cs)
	MEmergencyRegistroStringa(" eflags=")
	MEmergencyRegistrounsignedinteger32(eflags)
	MEmergencyRegistroStringa(" cr0=")
	MEmergencyRegistrounsignedinteger32(exceptioncr0())
	MEmergencyRegistroStringa(" cr3=")
	MEmergencyRegistrounsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencyRegistroStringa(" cr2=")
		MEmergencyRegistrounsignedinteger32(exceptioncr2())
		stampaPAGINAfaultInformazioni(errori)
	}

	if (cs & 0x03) != 0 {
		MEmergencyRegistroStringa(" useresp=")
		MEmergencyRegistrounsignedinteger32(exceptionRiquadroValore(esp, eipoffset+12))
		MEmergencyRegistroStringa(" ss=")
		MEmergencyRegistrounsignedinteger32(exceptionRiquadroValore(esp, eipoffset+16))
	}

	if exceptionhasErrorecode(interrupt) {
		stampaexceptionselectorInformazioni(errori)
	}
	MEmergencyRegistroStringa("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltDopofatalexception()

func ManigliafatalinterruptRiquadro(salvatoesp uint32, interrupt uint32) uint32 {
	Manigliaexception(salvatoesp+52, interrupt)
	haltDopofatalexception()
	return salvatoesp
}

func InterruptAttivo()
func (séstesso *TInterruptmanager) Attivo() {
	if Attivointerruptmanager != 0 {
		séstesso.Deactive()
	}
	address := uintptr(Pointer(séstesso))
	Attivointerruptmanager = address
	InterruptAttivo()
}
func Interruptdeactive()
func (séstesso *TInterruptmanager) Deactive() {
	Attivointerruptmanager = 0
	Interruptdeactive()
}

func MyManigliainterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MStampa(buffer)
	return esp
}
func MyProva(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MStampa(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MStampa(buffer)
	console_2.MHexadecimalStampa(0x40)
	return esp
}
func stampaesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Stampaxy(esp, 20, 21)
}
func gettls() uint32
func Stampatls() {

}
