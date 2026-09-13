package Avbrudd

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func avbruddignore()

func avbruddexceptionhandler()
func avbruddexceptionhandler0x00()
func avbruddexceptionhandler0x01()
func avbruddexceptionhandler0x02()
func avbruddexceptionhandler0x03()
func avbruddexceptionhandler0x04()
func avbruddexceptionhandler0x05()
func avbruddexceptionhandler0x06()
func avbruddexceptionhandler0x07()
func avbruddexceptionhandler0x08()
func avbruddexceptionhandler0x09()
func avbruddexceptionhandler0x0a()
func avbruddexceptionhandler0x0b()
func avbruddexceptionhandler0x0c()
func avbruddexceptionhandler0x0d()
func avbruddexceptionhandler0x0e()
func avbruddexceptionhandler0x0f()
func avbruddexceptionhandler0x10()
func avbruddexceptionhandler0x11()
func avbruddexceptionhandler0x12()
func avbruddexceptionhandler0x13()

func avbruddrequesthandler0x00()
func avbruddrequesthandler0x01()
func avbruddrequesthandler0x02()
func avbruddrequesthandler0x03()
func avbruddrequesthandler0x04()
func avbruddrequesthandler0x05()
func avbruddrequesthandler0x06()
func avbruddrequesthandler0x07()
func avbruddrequesthandler0x08()
func avbruddrequesthandler0x09()
func avbruddrequesthandler0x0a()
func avbruddrequesthandler0x0b()
func avbruddrequesthandler0x0c()
func avbruddrequesthandler0x0d()
func avbruddrequesthandler0x0e()
func avbruddrequesthandler0x0f()

func avbruddrequesthandler0x80()
func avbruddrequesthandler0x81()
func avbruddrequesthandler0x82()

func TestSkrivut(posisjon uint8, data uint8)
func settds(dssegment uint32)
func settgs(gssegment uint32)
func avbruddAvsluttLøkke()

type TAvbruddhandler struct {
	AvbruddTall	uint8
	Avbruddmanager	uintptr
}
type IAvbruddhandler interface {
	HåndtakAvbrudd(uint32) uint32
}

func NyAvbruddhandler(Avbruddmanager uintptr, AvbruddTall uint8) *TAvbruddhandler {
	avbruddhandler_2 := new(TAvbruddhandler)
	avbruddhandler_2.AvbruddTall = AvbruddTall
	avbruddhandler_2.Avbruddmanager = Avbruddmanager
	return avbruddhandler_2

}

var handler_2 [256]uintptr

func (selv *TAvbruddhandler) Init(AvbruddTall uint8, Avbruddmanager uintptr, funcaddress uintptr) {

	handler_2[AvbruddTall] = funcaddress

	selv.AvbruddTall = AvbruddTall
	selv.Avbruddmanager = Avbruddmanager

}
func (selv *TAvbruddhandler) SettHåndtakAvbruddfuction(AvbruddTall uint32, address uintptr) {
	handler_2[AvbruddTall] = address
}
func (selv *TAvbruddhandler) Ødelegg() {
	selvuintptr := uintptr(Pointer(selv))
	Avbruddmanager := (*TAvbruddmanager)(Pointer(selv.Avbruddmanager))
	if selvuintptr == Avbruddmanager.Gethandler(selv.AvbruddTall) {
		Avbruddmanager.Setthandler(0, selv.AvbruddTall)
	}

}
func (selv *TAvbruddhandler) SettAvbruddmanager(Avbruddmanager uintptr) {
}
func (selv *TAvbruddhandler) SettAvbruddTall(AvbruddTall uint8) {
	selv.AvbruddTall = AvbruddTall
}
func (selv *TAvbruddhandler) HåndtakAvbrudd(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MSkrivut(buffer)
	return esp
}
func HåndtakAvbrudd1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MSkrivut(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TAvbrudddescriptorTabellPeker struct {
}

var idtdata [256 * 8]uint8
var AktivAvbruddmanager uintptr = 0

const avbruddFeilsøk = false

type TAvbruddmanager struct {
	handler_2	[256]uintptr

	maskinvareAvbruddAvstand	uint16

	oppgavemanager	*TOppgavemanager
}

var PrimarypicKommandoioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicKommandoioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (selv *TAvbruddmanager) Init(maskinvareAvbruddAvstand uint16, globaldescriptorTabell *TShareddescriptorTabell, oppgavemanager *TOppgavemanager) {

	selv.oppgavemanager = oppgavemanager

	selv.maskinvareAvbruddAvstand = maskinvareAvbruddAvstand
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtAvbruddgate uint8 = 0xE
	address = uint32(ValueOf(avbruddignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(avbruddexceptionhandler0x0f).Pointer())
		selv.AvbrudddescriptorTabellentrySett(i, codesegment, address, 0, IdtAvbruddgate)
	}

	address = uint32(ValueOf(avbruddexceptionhandler0x00).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x00, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x01).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x01, codesegment, address, 0, IdtAvbruddgate)
	address = uint32(ValueOf(avbruddexceptionhandler0x02).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x02, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x03).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x03, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x04).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x04, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x05).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x05, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x06).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x06, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x07).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x07, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x08).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x08, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x09).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x09, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x0a).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x0A, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x0b).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x0B, codesegment, address, 0, IdtAvbruddgate)
	address = uint32(ValueOf(avbruddexceptionhandler0x0c).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x0C, codesegment, address, 0, IdtAvbruddgate)
	address = uint32(ValueOf(avbruddexceptionhandler0x0d).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x0D, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x0e).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x0E, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x0f).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x0F, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x10).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x10, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x11).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x11, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x12).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x12, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddexceptionhandler0x13).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x13, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x00).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x20, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x01).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x21, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x02).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x22, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x03).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x23, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x04).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x24, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x05).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x25, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x06).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x26, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x07).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x27, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x08).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x28, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x09).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x29, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x0a).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x2A, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x0b).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x2B, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x0c).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x2C, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x0d).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x2D, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x0e).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x2E, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x0f).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x2F, codesegment, address, 0, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x80).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x80, codesegment, address, 3, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x81).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x81, codesegment, address, 3, IdtAvbruddgate)

	address = uint32(ValueOf(avbruddrequesthandler0x82).Pointer())
	selv.AvbrudddescriptorTabellentrySett(0x82, codesegment, address, 3, IdtAvbruddgate)

	PortSkrivbyte(PrimarypicKommandoioport, 0x11)
	PortSkrivbyte(SecondarypicKommandoioport, 0x11)

	PortSkrivbyte(Primarypicdataioport, 0x20)
	PortSkrivbyte(Secondarypicdataioport, 0x28)

	PortSkrivbyte(Primarypicdataioport, 0x04)
	PortSkrivbyte(Secondarypicdataioport, 0x02)

	PortSkrivbyte(Primarypicdataioport, 0x01)
	PortSkrivbyte(Secondarypicdataioport, 0x01)

	PortSkrivbyte(Primarypicdataioport, 0xF8)
	PortSkrivbyte(Secondarypicdataioport, 0xEF)

	idtPeker := [6]uint8{0, 0, 0, 0, 0, 0}
	størrelse := (*uint16)(Pointer(&idtPeker[0]))
	(*størrelse) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtPeker[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtPeker)))
}
func Lidt(lidtaddr uintptr)

func (selv *TAvbruddmanager) AvbrudddescriptorTabellentrySett(avbrudd int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorFiltype uint8) {

	handleraddressLavbit := (*uint16)(Pointer(&idtdata[avbrudd*8+0]))
	(*handleraddressLavbit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[avbrudd*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[avbrudd*8+4]))
	(*reserved) = 0

	var IdtdescriptorTilstede uint8 = 0x80
	tilgang := (*uint8)(Pointer(&idtdata[avbrudd*8+5]))
	(*tilgang) = (IdtdescriptorTilstede | DescriptorFiltype | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressHøybit := (*uint16)(Pointer(&idtdata[avbrudd*8+6]))
	(*handleraddressHøybit) = uint16((handler >> 16) & 0xFFFF)

}

func (selv *TAvbruddmanager) Setthandler(handler uintptr, AvbruddTall uint8) {
	handler_2[AvbruddTall] = handler
}
func (selv *TAvbruddmanager) Gethandler(AvbruddTall uint8) uintptr {
	return handler_2[AvbruddTall]
}
func (selv *TAvbruddmanager) DoHåndtakAvbrudd(avbrudd uint8, esp uint32) uint32 {

	if avbruddFeilsøk {
		console_2.MSkrivutxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Skrivut(uint32(avbrudd))
		console_2.MSkrivut(":")
		console_2.MUnsignedinteger32Skrivut(esp)
	}
	handlerKjør := false
	if handler_2[avbrudd] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[avbrudd])))
		esp = myfunction(esp)
		handlerKjør = true

	}

	if !handlerKjør && avbrudd == uint8(selv.maskinvareAvbruddAvstand) && selv.oppgavemanager != nil {
		esp = uint32(uintptr(Pointer(selv.oppgavemanager.Schedule((*TcpuStatus)(Pointer(uintptr(esp)))))))

	}
	if !handlerKjør && avbrudd == 0x80 {
		esp = håndtakunhandledsyscall(esp)
	}

	if avbrudd <= 0x1F {
	}
	if 0x20 <= avbrudd && avbrudd < 0x30 {
		if 0x28 <= avbrudd {
			PortSkrivbyte(SecondarypicKommandoioport, 0x20)
		}
		PortSkrivbyte(PrimarypicKommandoioport, 0x20)
	}
	return esp
}

var antall2 uint8 = 1

func settcr3(address uint32)

var console_2 TConsole = TConsole{}

func HåndtakAvbrudd(esp uint32, avbrudd uint32) uint32 {

	if avbruddFeilsøk && avbrudd != 0x80 && avbrudd != 0x20 {
		console_2.MSkrivutxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Skrivut(uint32(avbrudd))
		console_2.MSkrivut(":")
		console_2.MUnsignedinteger32Skrivut(esp)
	}

	if AktivAvbruddmanager != 0 {
		p := (*TAvbruddmanager)(Pointer(AktivAvbruddmanager))
		esp = p.DoHåndtakAvbrudd(uint8(avbrudd), esp)
		return esp
	}
	if handler_2[avbrudd] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[avbrudd])))
		esp = myfunction(esp)
	}
	if avbrudd == 0x80 {
		return håndtakunhandledsyscall(esp)
	}
	if 0x20 <= avbrudd && avbrudd < 0x30 {
		if 0x28 <= avbrudd {
			PortSkrivbyte(SecondarypicKommandoioport, 0x20)
		}
		PortSkrivbyte(PrimarypicKommandoioport, 0x20)
	}

	return esp
}

func håndtakunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStatus)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(avbruddAvsluttLøkke).Pointer())
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

func exceptionhasFeilcode(avbrudd uint32) bool {
	switch avbrudd {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNavn(avbrudd uint32) string {
	switch avbrudd {
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

func exceptionRammeVerdi(ramme uint32, avstand uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ramme + avstand)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func skrivutSidefaultinfo(err uint32) {
	MEmergencyLoggStreng(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencyLoggStreng("protection")
	} else {
		MEmergencyLoggStreng("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencyLoggStreng(",write")
	} else {
		MEmergencyLoggStreng(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencyLoggStreng(",user")
	} else {
		MEmergencyLoggStreng(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencyLoggStreng(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencyLoggStreng(",instruction-fetch")
	}
	MEmergencyLoggStreng("]")
}

func skrivutexceptionselectorinfo(err uint32) {
	MEmergencyLoggStreng(" selector=")
	MEmergencyLoggunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencyLoggStreng(" index=")
	MEmergencyLoggunsignedinteger32(err >> 3)
	MEmergencyLoggStreng(" table=")
	if (err & 0x02) != 0 {
		MEmergencyLoggStreng("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencyLoggStreng("LDT")
	} else {
		MEmergencyLoggStreng("GDT")
	}
	MEmergencyLoggStreng(" ext=")
	MEmergencyLoggunsignedinteger32(err & 0x01)
}

func Håndtakexception(esp uint32, avbrudd uint32) uint32 {
	MEmergencyLoggStreng("\nEXCEPTION vec=")
	MEmergencyLogghexadecimal8(uint8(avbrudd))
	MEmergencyLoggStreng(" ")
	MEmergencyLoggStreng(exceptionNavn(avbrudd))
	MEmergencyLoggStreng(" frame=")
	MEmergencyLoggunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyLoggStreng(" invalid-frame")
		if exceptionhasFeilcode(avbrudd) {
			MEmergencyLoggStreng(" raw-error-or-bad-esp=")
			MEmergencyLoggunsignedinteger32(esp)
			skrivutexceptionselectorinfo(esp)
		}
		MEmergencyLoggStreng("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipAvstand uint32 = 0
	if exceptionhasFeilcode(avbrudd) {
		err = exceptionRammeVerdi(esp, 0)
		eipAvstand = 4
	}
	eip := exceptionRammeVerdi(esp, eipAvstand)
	cs := exceptionRammeVerdi(esp, eipAvstand+4)
	eflags := exceptionRammeVerdi(esp, eipAvstand+8)

	MEmergencyLoggStreng(" err=")
	MEmergencyLoggunsignedinteger32(err)
	MEmergencyLoggStreng(" eip=")
	MEmergencyLoggunsignedinteger32(eip)
	MEmergencyLoggStreng(" cs=")
	MEmergencyLoggunsignedinteger32(cs)
	MEmergencyLoggStreng(" eflags=")
	MEmergencyLoggunsignedinteger32(eflags)
	MEmergencyLoggStreng(" cr0=")
	MEmergencyLoggunsignedinteger32(exceptioncr0())
	MEmergencyLoggStreng(" cr3=")
	MEmergencyLoggunsignedinteger32(exceptioncr3())

	if avbrudd == 0x0E {
		MEmergencyLoggStreng(" cr2=")
		MEmergencyLoggunsignedinteger32(exceptioncr2())
		skrivutSidefaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencyLoggStreng(" useresp=")
		MEmergencyLoggunsignedinteger32(exceptionRammeVerdi(esp, eipAvstand+12))
		MEmergencyLoggStreng(" ss=")
		MEmergencyLoggunsignedinteger32(exceptionRammeVerdi(esp, eipAvstand+16))
	}

	if exceptionhasFeilcode(avbrudd) {
		skrivutexceptionselectorinfo(err)
	}
	MEmergencyLoggStreng("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltEtterfatalexception()

func HåndtakfatalAvbruddRamme(savedesp uint32, avbrudd uint32) uint32 {
	Håndtakexception(savedesp+52, avbrudd)
	haltEtterfatalexception()
	return savedesp
}

func AvbruddAktiv()
func (selv *TAvbruddmanager) Aktiv() {
	if AktivAvbruddmanager != 0 {
		selv.Deactive()
	}
	address := uintptr(Pointer(selv))
	AktivAvbruddmanager = address
	AvbruddAktiv()
}
func Avbrudddeactive()
func (selv *TAvbruddmanager) Deactive() {
	AktivAvbruddmanager = 0
	Avbrudddeactive()
}

func MyHåndtakAvbrudd(avbrudd uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MSkrivut(buffer)
	return esp
}
func Mytest(avbrudd uint8, esp uint32)

func UnhandleAvbrudd() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MSkrivut(buffer)
}

func avbruddhandler_2(avbrudd uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MSkrivut(buffer)
	console_2.MHexadecimalSkrivut(0x40)
	return esp
}
func skrivutesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Skrivutxy(esp, 20, 21)
}
func gettls() uint32
func Skrivuttls() {

}
