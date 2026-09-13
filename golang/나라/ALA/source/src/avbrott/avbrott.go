package Avbrott

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "konsol"

func avbrottignore()

func avbrottexceptionhandler()
func avbrottexceptionhandler0x00()
func avbrottexceptionhandler0x01()
func avbrottexceptionhandler0x02()
func avbrottexceptionhandler0x03()
func avbrottexceptionhandler0x04()
func avbrottexceptionhandler0x05()
func avbrottexceptionhandler0x06()
func avbrottexceptionhandler0x07()
func avbrottexceptionhandler0x08()
func avbrottexceptionhandler0x09()
func avbrottexceptionhandler0x0a()
func avbrottexceptionhandler0x0b()
func avbrottexceptionhandler0x0c()
func avbrottexceptionhandler0x0d()
func avbrottexceptionhandler0x0e()
func avbrottexceptionhandler0x0f()
func avbrottexceptionhandler0x10()
func avbrottexceptionhandler0x11()
func avbrottexceptionhandler0x12()
func avbrottexceptionhandler0x13()

func avbrottrequesthandler0x00()
func avbrottrequesthandler0x01()
func avbrottrequesthandler0x02()
func avbrottrequesthandler0x03()
func avbrottrequesthandler0x04()
func avbrottrequesthandler0x05()
func avbrottrequesthandler0x06()
func avbrottrequesthandler0x07()
func avbrottrequesthandler0x08()
func avbrottrequesthandler0x09()
func avbrottrequesthandler0x0a()
func avbrottrequesthandler0x0b()
func avbrottrequesthandler0x0c()
func avbrottrequesthandler0x0d()
func avbrottrequesthandler0x0e()
func avbrottrequesthandler0x0f()

func avbrottrequesthandler0x80()
func avbrottrequesthandler0x81()
func avbrottrequesthandler0x82()

func TestaSkrivut(position uint8, data uint8)
func mängdds(dssegment uint32)
func mängdgs(gssegment uint32)
func avbrottAvslutaSlinga()

type TAvbrotthandler struct {
	AvbrottNummer	uint8
	Avbrottmanager	uintptr
}
type IAvbrotthandler interface {
	HandtagAvbrott(uint32) uint32
}

func NyAvbrotthandler(Avbrottmanager uintptr, AvbrottNummer uint8) *TAvbrotthandler {
	avbrotthandler_2 := new(TAvbrotthandler)
	avbrotthandler_2.AvbrottNummer = AvbrottNummer
	avbrotthandler_2.Avbrottmanager = Avbrottmanager
	return avbrotthandler_2

}

var handler_2 [256]uintptr

func (själv *TAvbrotthandler) Init(AvbrottNummer uint8, Avbrottmanager uintptr, funcAdress uintptr) {

	handler_2[AvbrottNummer] = funcAdress

	själv.AvbrottNummer = AvbrottNummer
	själv.Avbrottmanager = Avbrottmanager

}
func (själv *TAvbrotthandler) MängdHandtagAvbrottfuction(AvbrottNummer uint32, adress uintptr) {
	handler_2[AvbrottNummer] = adress
}
func (själv *TAvbrotthandler) Förstör() {
	självuintptr := uintptr(Pointer(själv))
	Avbrottmanager := (*TAvbrottmanager)(Pointer(själv.Avbrottmanager))
	if självuintptr == Avbrottmanager.Gethandler(själv.AvbrottNummer) {
		Avbrottmanager.Mängdhandler(0, själv.AvbrottNummer)
	}

}
func (själv *TAvbrotthandler) MängdAvbrottmanager(Avbrottmanager uintptr) {
}
func (själv *TAvbrotthandler) MängdAvbrottNummer(AvbrottNummer uint8) {
	själv.AvbrottNummer = AvbrottNummer
}
func (själv *TAvbrotthandler) HandtagAvbrott(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konsol_2 := TKonsol{}
	konsol_2.MSkrivut(buffer)
	return esp
}
func HandtagAvbrott1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konsol_2 := TKonsol{}
	konsol_2.MSkrivut(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TAvbrottdescriptorTabellMuspekare struct {
}

var idtdata [256 * 8]uint8
var AktivAvbrottmanager uintptr = 0

const avbrottAvlusa = false

type TAvbrottmanager struct {
	handler_2	[256]uintptr

	hårdvaraAvbrottFörskjutning	uint16

	aktivitetmanager	*TAktivitetmanager
}

var PrimarypicKommandoioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicKommandoioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (själv *TAvbrottmanager) Init(hårdvaraAvbrottFörskjutning uint16, globaldescriptorTabell *TShareddescriptorTabell, aktivitetmanager *TAktivitetmanager) {

	själv.aktivitetmanager = aktivitetmanager

	själv.hårdvaraAvbrottFörskjutning = hårdvaraAvbrottFörskjutning
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var adress uint32
	var IdtAvbrottgate uint8 = 0xE
	adress = uint32(ValueOf(avbrottignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		adress = uint32(ValueOf(avbrottexceptionhandler0x0f).Pointer())
		själv.AvbrottdescriptorTabellpostmängd(i, codesegment, adress, 0, IdtAvbrottgate)
	}

	adress = uint32(ValueOf(avbrottexceptionhandler0x00).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x00, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x01).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x01, codesegment, adress, 0, IdtAvbrottgate)
	adress = uint32(ValueOf(avbrottexceptionhandler0x02).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x02, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x03).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x03, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x04).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x04, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x05).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x05, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x06).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x06, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x07).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x07, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x08).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x08, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x09).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x09, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x0a).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x0A, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x0b).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x0B, codesegment, adress, 0, IdtAvbrottgate)
	adress = uint32(ValueOf(avbrottexceptionhandler0x0c).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x0C, codesegment, adress, 0, IdtAvbrottgate)
	adress = uint32(ValueOf(avbrottexceptionhandler0x0d).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x0D, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x0e).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x0E, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x0f).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x0F, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x10).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x10, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x11).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x11, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x12).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x12, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottexceptionhandler0x13).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x13, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x00).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x20, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x01).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x21, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x02).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x22, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x03).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x23, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x04).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x24, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x05).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x25, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x06).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x26, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x07).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x27, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x08).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x28, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x09).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x29, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x0a).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x2A, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x0b).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x2B, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x0c).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x2C, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x0d).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x2D, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x0e).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x2E, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x0f).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x2F, codesegment, adress, 0, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x80).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x80, codesegment, adress, 3, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x81).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x81, codesegment, adress, 3, IdtAvbrottgate)

	adress = uint32(ValueOf(avbrottrequesthandler0x82).Pointer())
	själv.AvbrottdescriptorTabellpostmängd(0x82, codesegment, adress, 3, IdtAvbrottgate)

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

	idtMuspekare := [6]uint8{0, 0, 0, 0, 0, 0}
	storlek := (*uint16)(Pointer(&idtMuspekare[0]))
	(*storlek) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtMuspekare[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtMuspekare)))
}
func Lidt(lidtaddr uintptr)

func (själv *TAvbrottmanager) AvbrottdescriptorTabellpostmängd(avbrott int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTyp uint8) {

	handlerAdressLågbitar := (*uint16)(Pointer(&idtdata[avbrott*8+0]))
	(*handlerAdressLågbitar) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[avbrott*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserverat := (*uint8)(Pointer(&idtdata[avbrott*8+4]))
	(*reserverat) = 0

	var IdtdescriptorAnsluten uint8 = 0x80
	åtkomst := (*uint8)(Pointer(&idtdata[avbrott*8+5]))
	(*åtkomst) = (IdtdescriptorAnsluten | DescriptorTyp | ((Descriptorprivilegelevel & 3) << 5))

	handlerAdressHögbitar := (*uint16)(Pointer(&idtdata[avbrott*8+6]))
	(*handlerAdressHögbitar) = uint16((handler >> 16) & 0xFFFF)

}

func (själv *TAvbrottmanager) Mängdhandler(handler uintptr, AvbrottNummer uint8) {
	handler_2[AvbrottNummer] = handler
}
func (själv *TAvbrottmanager) Gethandler(AvbrottNummer uint8) uintptr {
	return handler_2[AvbrottNummer]
}
func (själv *TAvbrottmanager) DoHandtagAvbrott(avbrott uint8, esp uint32) uint32 {

	if avbrottAvlusa {
		konsol_2.MSkrivutxy("[esp:", 1, 20)
		konsol_2.MUnsignedinteger32Skrivut(uint32(avbrott))
		konsol_2.MSkrivut(":")
		konsol_2.MUnsignedinteger32Skrivut(esp)
	}
	handlerKör := false
	if handler_2[avbrott] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[avbrott])))
		esp = myfunction(esp)
		handlerKör = true

	}

	if !handlerKör && avbrott == uint8(själv.hårdvaraAvbrottFörskjutning) && själv.aktivitetmanager != nil {
		esp = uint32(uintptr(Pointer(själv.aktivitetmanager.Schedule((*TcpuTillstånd)(Pointer(uintptr(esp)))))))

	}
	if !handlerKör && avbrott == 0x80 {
		esp = handtagunhandledsyscall(esp)
	}

	if avbrott <= 0x1F {
	}
	if 0x20 <= avbrott && avbrott < 0x30 {
		if 0x28 <= avbrott {
			PortSkrivbyte(SecondarypicKommandoioport, 0x20)
		}
		PortSkrivbyte(PrimarypicKommandoioport, 0x20)
	}
	return esp
}

var antal2 uint8 = 1

func mängdcr3(adress uint32)

var konsol_2 TKonsol = TKonsol{}

func HandtagAvbrott(esp uint32, avbrott uint32) uint32 {

	if avbrottAvlusa && avbrott != 0x80 && avbrott != 0x20 {
		konsol_2.MSkrivutxy("[esp:", 1, 21)
		konsol_2.MUnsignedinteger32Skrivut(uint32(avbrott))
		konsol_2.MSkrivut(":")
		konsol_2.MUnsignedinteger32Skrivut(esp)
	}

	if AktivAvbrottmanager != 0 {
		p := (*TAvbrottmanager)(Pointer(AktivAvbrottmanager))
		esp = p.DoHandtagAvbrott(uint8(avbrott), esp)
		return esp
	}
	if handler_2[avbrott] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[avbrott])))
		esp = myfunction(esp)
	}
	if avbrott == 0x80 {
		return handtagunhandledsyscall(esp)
	}
	if 0x20 <= avbrott && avbrott < 0x30 {
		if 0x28 <= avbrott {
			PortSkrivbyte(SecondarypicKommandoioport, 0x20)
		}
		PortSkrivbyte(PrimarypicKommandoioport, 0x20)
	}

	return esp
}

func handtagunhandledsyscall(esp uint32) uint32 {
	processor := (*TcpuTillstånd)(Pointer(uintptr(esp)))
	if processor.Eax == 1 || processor.Eax == 252 {
		processor.Eip = uint32(ValueOf(avbrottAvslutaSlinga).Pointer())
		processor.Cs = Segkernelcode
		processor.Ds = Segkerneldata
		processor.Es = Segkerneldata
		processor.Fs = Segkerneldata
		processor.Gs = Segkernelgs
		processor.Ss = Segkerneldata
		processor.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasFelcode(avbrott uint32) bool {
	switch avbrott {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNamn(avbrott uint32) string {
	switch avbrott {
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

func exceptionRamVärde(ram uint32, förskjutning uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ram + förskjutning)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func skrivutSidafaultInformation(fel uint32) {
	MEmergencyLoggsträng(" pf=[")
	if (fel & 0x01) != 0 {
		MEmergencyLoggsträng("protection")
	} else {
		MEmergencyLoggsträng("not-present")
	}
	if (fel & 0x02) != 0 {
		MEmergencyLoggsträng(",write")
	} else {
		MEmergencyLoggsträng(",read")
	}
	if (fel & 0x04) != 0 {
		MEmergencyLoggsträng(",user")
	} else {
		MEmergencyLoggsträng(",kernel")
	}
	if (fel & 0x08) != 0 {
		MEmergencyLoggsträng(",reserved-bit")
	}
	if (fel & 0x10) != 0 {
		MEmergencyLoggsträng(",instruction-fetch")
	}
	MEmergencyLoggsträng("]")
}

func skrivutexceptionselectorInformation(fel uint32) {
	MEmergencyLoggsträng(" selector=")
	MEmergencyLoggunsignedinteger32(fel & 0xFFFFFFF8)
	MEmergencyLoggsträng(" index=")
	MEmergencyLoggunsignedinteger32(fel >> 3)
	MEmergencyLoggsträng(" table=")
	if (fel & 0x02) != 0 {
		MEmergencyLoggsträng("IDT")
	} else if (fel & 0x04) != 0 {
		MEmergencyLoggsträng("LDT")
	} else {
		MEmergencyLoggsträng("GDT")
	}
	MEmergencyLoggsträng(" ext=")
	MEmergencyLoggunsignedinteger32(fel & 0x01)
}

func Handtagexception(esp uint32, avbrott uint32) uint32 {
	MEmergencyLoggsträng("\nEXCEPTION vec=")
	MEmergencyLogghexadecimal8(uint8(avbrott))
	MEmergencyLoggsträng(" ")
	MEmergencyLoggsträng(exceptionNamn(avbrott))
	MEmergencyLoggsträng(" frame=")
	MEmergencyLoggunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyLoggsträng(" invalid-frame")
		if exceptionhasFelcode(avbrott) {
			MEmergencyLoggsträng(" raw-error-or-bad-esp=")
			MEmergencyLoggunsignedinteger32(esp)
			skrivutexceptionselectorInformation(esp)
		}
		MEmergencyLoggsträng("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var fel uint32 = 0
	var eipFörskjutning uint32 = 0
	if exceptionhasFelcode(avbrott) {
		fel = exceptionRamVärde(esp, 0)
		eipFörskjutning = 4
	}
	eip := exceptionRamVärde(esp, eipFörskjutning)
	cs := exceptionRamVärde(esp, eipFörskjutning+4)
	eflags := exceptionRamVärde(esp, eipFörskjutning+8)

	MEmergencyLoggsträng(" err=")
	MEmergencyLoggunsignedinteger32(fel)
	MEmergencyLoggsträng(" eip=")
	MEmergencyLoggunsignedinteger32(eip)
	MEmergencyLoggsträng(" cs=")
	MEmergencyLoggunsignedinteger32(cs)
	MEmergencyLoggsträng(" eflags=")
	MEmergencyLoggunsignedinteger32(eflags)
	MEmergencyLoggsträng(" cr0=")
	MEmergencyLoggunsignedinteger32(exceptioncr0())
	MEmergencyLoggsträng(" cr3=")
	MEmergencyLoggunsignedinteger32(exceptioncr3())

	if avbrott == 0x0E {
		MEmergencyLoggsträng(" cr2=")
		MEmergencyLoggunsignedinteger32(exceptioncr2())
		skrivutSidafaultInformation(fel)
	}

	if (cs & 0x03) != 0 {
		MEmergencyLoggsträng(" useresp=")
		MEmergencyLoggunsignedinteger32(exceptionRamVärde(esp, eipFörskjutning+12))
		MEmergencyLoggsträng(" ss=")
		MEmergencyLoggunsignedinteger32(exceptionRamVärde(esp, eipFörskjutning+16))
	}

	if exceptionhasFelcode(avbrott) {
		skrivutexceptionselectorInformation(fel)
	}
	MEmergencyLoggsträng("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandtagfatalAvbrottRam(sparadesp uint32, avbrott uint32) uint32 {
	Handtagexception(sparadesp+52, avbrott)
	haltafterfatalexception()
	return sparadesp
}

func AvbrottAktiv()
func (själv *TAvbrottmanager) Aktiv() {
	if AktivAvbrottmanager != 0 {
		själv.Deactive()
	}
	adress := uintptr(Pointer(själv))
	AktivAvbrottmanager = adress
	AvbrottAktiv()
}
func Avbrottdeactive()
func (själv *TAvbrottmanager) Deactive() {
	AktivAvbrottmanager = 0
	Avbrottdeactive()
}

func MyHandtagAvbrott(avbrott uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konsol_2 := TKonsol{}
	konsol_2.MSkrivut(buffer)
	return esp
}
func MyTesta(avbrott uint8, esp uint32)

func UnhandleAvbrott() {
	buffer := []byte("unhandle interrupt\n")
	konsol_2 := TKonsol{}
	konsol_2.MSkrivut(buffer)
}

func avbrotthandler_2(avbrott uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konsol_2 := TKonsol{}
	konsol_2.MSkrivut(buffer)
	konsol_2.MHexadecimalSkrivut(0x40)
	return esp
}
func skrivutesp(esp uint32) {
	konsol_2 := TKonsol{}
	konsol_2.MUnsignedinteger32Skrivutxy(esp, 20, 21)
}
func gettls() uint32
func Skrivuttls() {

}
