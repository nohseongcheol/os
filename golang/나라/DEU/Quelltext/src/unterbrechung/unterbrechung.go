/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Unterbrechung

import . "unsafe"
import . "reflect"

import . "anschluss"
import . "gdt"
import . "mehrfachAufgabenverwaltung"
import . "konsole"

func unterbrechungignore()

func unterbrechungexceptionhandler()
func unterbrechungexceptionhandler0x00()
func unterbrechungexceptionhandler0x01()
func unterbrechungexceptionhandler0x02()
func unterbrechungexceptionhandler0x03()
func unterbrechungexceptionhandler0x04()
func unterbrechungexceptionhandler0x05()
func unterbrechungexceptionhandler0x06()
func unterbrechungexceptionhandler0x07()
func unterbrechungexceptionhandler0x08()
func unterbrechungexceptionhandler0x09()
func unterbrechungexceptionhandler0x0a()
func unterbrechungexceptionhandler0x0b()
func unterbrechungexceptionhandler0x0c()
func unterbrechungexceptionhandler0x0d()
func unterbrechungexceptionhandler0x0e()
func unterbrechungexceptionhandler0x0f()
func unterbrechungexceptionhandler0x10()
func unterbrechungexceptionhandler0x11()
func unterbrechungexceptionhandler0x12()
func unterbrechungexceptionhandler0x13()

func unterbrechungrequesthandler0x00()
func unterbrechungrequesthandler0x01()
func unterbrechungrequesthandler0x02()
func unterbrechungrequesthandler0x03()
func unterbrechungrequesthandler0x04()
func unterbrechungrequesthandler0x05()
func unterbrechungrequesthandler0x06()
func unterbrechungrequesthandler0x07()
func unterbrechungrequesthandler0x08()
func unterbrechungrequesthandler0x09()
func unterbrechungrequesthandler0x0a()
func unterbrechungrequesthandler0x0b()
func unterbrechungrequesthandler0x0c()
func unterbrechungrequesthandler0x0d()
func unterbrechungrequesthandler0x0e()
func unterbrechungrequesthandler0x0f()

func unterbrechungrequesthandler0x80()
func unterbrechungrequesthandler0x81()
func unterbrechungrequesthandler0x82()

func TestenDrucken(position uint8, daten uint8)
func setzends(dssegment uint32)
func setzengs(gssegment uint32)
func unterbrechungBeendenSchleife()

type TUnterbrechunghandler struct {
	UnterbrechungNummer	uint8
	UnterbrechungVerwalter	uintptr
}
type IUnterbrechunghandler interface {
	GriffUnterbrechung(uint32) uint32
}

func NeuUnterbrechunghandler(UnterbrechungVerwalter uintptr, UnterbrechungNummer uint8) *TUnterbrechunghandler {
	unterbrechunghandler_2 := new(TUnterbrechunghandler)
	unterbrechunghandler_2.UnterbrechungNummer = UnterbrechungNummer
	unterbrechunghandler_2.UnterbrechungVerwalter = UnterbrechungVerwalter
	return unterbrechunghandler_2

}

var handler_2 [256]uintptr

func (selbst *TUnterbrechunghandler) Init(UnterbrechungNummer uint8, UnterbrechungVerwalter uintptr, funcaddress uintptr) {

	handler_2[UnterbrechungNummer] = funcaddress

	selbst.UnterbrechungNummer = UnterbrechungNummer
	selbst.UnterbrechungVerwalter = UnterbrechungVerwalter

}
func (selbst *TUnterbrechunghandler) SetzenGriffUnterbrechungfuction(UnterbrechungNummer uint32, address uintptr) {
	handler_2[UnterbrechungNummer] = address
}
func (selbst *TUnterbrechunghandler) Zerstören() {
	selbstuintptr := uintptr(Pointer(selbst))
	UnterbrechungVerwalter := (*TUnterbrechungVerwalter)(Pointer(selbst.UnterbrechungVerwalter))
	if selbstuintptr == UnterbrechungVerwalter.Gethandler(selbst.UnterbrechungNummer) {
		UnterbrechungVerwalter.Setzenhandler(0, selbst.UnterbrechungNummer)
	}

}
func (selbst *TUnterbrechunghandler) SetzenUnterbrechungVerwalter(UnterbrechungVerwalter uintptr) {
}
func (selbst *TUnterbrechunghandler) SetzenUnterbrechungNummer(UnterbrechungNummer uint8) {
	selbst.UnterbrechungNummer = UnterbrechungNummer
}
func (selbst *TUnterbrechunghandler) GriffUnterbrechung(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konsole_2 := TKonsole{}
	konsole_2.MDrucken(buffer)
	return esp
}
func GriffUnterbrechung1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konsole_2 := TKonsole{}
	konsole_2.MDrucken(buffer)
}

type TTordescriptor struct {
	torDaten [8]uint8
}
type TUnterbrechungdescriptorTabelleZeiger struct {
}

var idtDaten [256 * 8]uint8
var AktivUnterbrechungVerwalter uintptr = 0

const unterbrechungDebuggen = false

type TUnterbrechungVerwalter struct {
	handler_2	[256]uintptr

	geräteUnterbrechungVersatz	uint16

	aufgabeVerwalter	*TAufgabeVerwalter
}

var PrimarypicBefehlEAAnschluss uint16 = 0x20
var PrimarypicDatenEAAnschluss uint16 = 0x21
var SecondarypicBefehlEAAnschluss uint16 = 0xA0
var SecondarypicDatenEAAnschluss uint16 = 0xA1

func (selbst *TUnterbrechungVerwalter) Init(geräteUnterbrechungVersatz uint16, globaldescriptorTabelle *TShareddescriptorTabelle, aufgabeVerwalter *TAufgabeVerwalter) {

	selbst.aufgabeVerwalter = aufgabeVerwalter

	selbst.geräteUnterbrechungVersatz = geräteUnterbrechungVersatz
	codesegment := uint16(SegKerncode)

	for i := 0; i < (256 * 8); i++ {
		idtDaten[i] = 0
	}
	var address uint32
	var IdtUnterbrechungTor uint8 = 0xE
	address = uint32(ValueOf(unterbrechungignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(unterbrechungexceptionhandler0x0f).Pointer())
		selbst.UnterbrechungdescriptorTabelleEintragSetzen(i, codesegment, address, 0, IdtUnterbrechungTor)
	}

	address = uint32(ValueOf(unterbrechungexceptionhandler0x00).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x00, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x01).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x01, codesegment, address, 0, IdtUnterbrechungTor)
	address = uint32(ValueOf(unterbrechungexceptionhandler0x02).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x02, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x03).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x03, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x04).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x04, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x05).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x05, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x06).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x06, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x07).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x07, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x08).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x08, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x09).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x09, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x0a).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x0A, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x0b).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x0B, codesegment, address, 0, IdtUnterbrechungTor)
	address = uint32(ValueOf(unterbrechungexceptionhandler0x0c).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x0C, codesegment, address, 0, IdtUnterbrechungTor)
	address = uint32(ValueOf(unterbrechungexceptionhandler0x0d).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x0D, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x0e).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x0E, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x0f).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x0F, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x10).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x10, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x11).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x11, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x12).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x12, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungexceptionhandler0x13).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x13, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x00).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x20, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x01).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x21, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x02).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x22, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x03).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x23, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x04).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x24, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x05).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x25, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x06).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x26, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x07).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x27, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x08).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x28, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x09).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x29, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x0a).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x2A, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x0b).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x2B, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x0c).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x2C, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x0d).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x2D, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x0e).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x2E, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x0f).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x2F, codesegment, address, 0, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x80).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x80, codesegment, address, 3, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x81).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x81, codesegment, address, 3, IdtUnterbrechungTor)

	address = uint32(ValueOf(unterbrechungrequesthandler0x82).Pointer())
	selbst.UnterbrechungdescriptorTabelleEintragSetzen(0x82, codesegment, address, 3, IdtUnterbrechungTor)

	AnschlussSchreibenByte(PrimarypicBefehlEAAnschluss, 0x11)
	AnschlussSchreibenByte(SecondarypicBefehlEAAnschluss, 0x11)

	AnschlussSchreibenByte(PrimarypicDatenEAAnschluss, 0x20)
	AnschlussSchreibenByte(SecondarypicDatenEAAnschluss, 0x28)

	AnschlussSchreibenByte(PrimarypicDatenEAAnschluss, 0x04)
	AnschlussSchreibenByte(SecondarypicDatenEAAnschluss, 0x02)

	AnschlussSchreibenByte(PrimarypicDatenEAAnschluss, 0x01)
	AnschlussSchreibenByte(SecondarypicDatenEAAnschluss, 0x01)

	AnschlussSchreibenByte(PrimarypicDatenEAAnschluss, 0xF8)
	AnschlussSchreibenByte(SecondarypicDatenEAAnschluss, 0xEF)

	idtZeiger := [6]uint8{0, 0, 0, 0, 0, 0}
	größe := (*uint16)(Pointer(&idtZeiger[0]))
	(*größe) = (uint16)(Sizeof(idtDaten) - 1)

	base := (*uint32)(Pointer(&idtZeiger[2]))
	(*base) = uint32(uintptr(Pointer(&idtDaten)))

	Lidt(uintptr(Pointer(&idtZeiger)))
}
func Lidt(lidtaddr uintptr)

func (selbst *TUnterbrechungVerwalter) UnterbrechungdescriptorTabelleEintragSetzen(unterbrechung int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTyp uint8) {

	handleraddressNiedrigBit := (*uint16)(Pointer(&idtDaten[unterbrechung*8+0]))
	(*handleraddressNiedrigBit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtDaten[unterbrechung*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserviert := (*uint8)(Pointer(&idtDaten[unterbrechung*8+4]))
	(*reserviert) = 0

	var IdtdescriptorVorhanden uint8 = 0x80
	zugreifen := (*uint8)(Pointer(&idtDaten[unterbrechung*8+5]))
	(*zugreifen) = (IdtdescriptorVorhanden | DescriptorTyp | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressHochBit := (*uint16)(Pointer(&idtDaten[unterbrechung*8+6]))
	(*handleraddressHochBit) = uint16((handler >> 16) & 0xFFFF)

}

func (selbst *TUnterbrechungVerwalter) Setzenhandler(handler uintptr, UnterbrechungNummer uint8) {
	handler_2[UnterbrechungNummer] = handler
}
func (selbst *TUnterbrechungVerwalter) Gethandler(UnterbrechungNummer uint8) uintptr {
	return handler_2[UnterbrechungNummer]
}
func (selbst *TUnterbrechungVerwalter) DoGriffUnterbrechung(unterbrechung uint8, esp uint32) uint32 {

	if unterbrechungDebuggen {
		konsole_2.MDruckenxy("[esp:", 1, 20)
		konsole_2.MUnsignedinteger32Drucken(uint32(unterbrechung))
		konsole_2.MDrucken(":")
		konsole_2.MUnsignedinteger32Drucken(esp)
	}
	handlerAusführen := false
	if handler_2[unterbrechung] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[unterbrechung])))
		esp = myfunction(esp)
		handlerAusführen = true

	}

	if !handlerAusführen && unterbrechung == uint8(selbst.geräteUnterbrechungVersatz) && selbst.aufgabeVerwalter != nil {
		esp = uint32(uintptr(Pointer(selbst.aufgabeVerwalter.Schedule((*TcpuStatus)(Pointer(uintptr(esp)))))))

	}
	if !handlerAusführen && unterbrechung == 0x80 {
		esp = griffunhandledsyscall(esp)
	}

	if unterbrechung <= 0x1F {
	}
	if 0x20 <= unterbrechung && unterbrechung < 0x30 {
		if 0x28 <= unterbrechung {
			AnschlussSchreibenByte(SecondarypicBefehlEAAnschluss, 0x20)
		}
		AnschlussSchreibenByte(PrimarypicBefehlEAAnschluss, 0x20)
	}
	return esp
}

var anzahl2 uint8 = 1

func setzencr3(address uint32)

var konsole_2 TKonsole = TKonsole{}

func GriffUnterbrechung(esp uint32, unterbrechung uint32) uint32 {

	if unterbrechungDebuggen && unterbrechung != 0x80 && unterbrechung != 0x20 {
		konsole_2.MDruckenxy("[esp:", 1, 21)
		konsole_2.MUnsignedinteger32Drucken(uint32(unterbrechung))
		konsole_2.MDrucken(":")
		konsole_2.MUnsignedinteger32Drucken(esp)
	}

	if AktivUnterbrechungVerwalter != 0 {
		p := (*TUnterbrechungVerwalter)(Pointer(AktivUnterbrechungVerwalter))
		esp = p.DoGriffUnterbrechung(uint8(unterbrechung), esp)
		return esp
	}
	if handler_2[unterbrechung] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[unterbrechung])))
		esp = myfunction(esp)
	}
	if unterbrechung == 0x80 {
		return griffunhandledsyscall(esp)
	}
	if 0x20 <= unterbrechung && unterbrechung < 0x30 {
		if 0x28 <= unterbrechung {
			AnschlussSchreibenByte(SecondarypicBefehlEAAnschluss, 0x20)
		}
		AnschlussSchreibenByte(PrimarypicBefehlEAAnschluss, 0x20)
	}

	return esp
}

func griffunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStatus)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(unterbrechungBeendenSchleife).Pointer())
		cpu.Cs = SegKerncode
		cpu.Ds = SegKernDaten
		cpu.Es = SegKernDaten
		cpu.Fs = SegKernDaten
		cpu.Gs = SegKerngs
		cpu.Ss = SegKernDaten
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasFehlercode(unterbrechung uint32) bool {
	switch unterbrechung {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionElementname(unterbrechung uint32) string {
	switch unterbrechung {
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

func exceptionRahmenWert(rahmen uint32, versatz uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(rahmen + versatz)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func druckenSeiteFehlerinfo(err uint32) {
	MEmergencyProtokollZeichenkette(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencyProtokollZeichenkette("protection")
	} else {
		MEmergencyProtokollZeichenkette("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencyProtokollZeichenkette(",write")
	} else {
		MEmergencyProtokollZeichenkette(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencyProtokollZeichenkette(",user")
	} else {
		MEmergencyProtokollZeichenkette(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencyProtokollZeichenkette(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencyProtokollZeichenkette(",instruction-fetch")
	}
	MEmergencyProtokollZeichenkette("]")
}

func druckenexceptionselectorinfo(err uint32) {
	MEmergencyProtokollZeichenkette(" selector=")
	MEmergencyProtokollunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencyProtokollZeichenkette(" index=")
	MEmergencyProtokollunsignedinteger32(err >> 3)
	MEmergencyProtokollZeichenkette(" table=")
	if (err & 0x02) != 0 {
		MEmergencyProtokollZeichenkette("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencyProtokollZeichenkette("LDT")
	} else {
		MEmergencyProtokollZeichenkette("GDT")
	}
	MEmergencyProtokollZeichenkette(" ext=")
	MEmergencyProtokollunsignedinteger32(err & 0x01)
}

func Griffexception(esp uint32, unterbrechung uint32) uint32 {
	MEmergencyProtokollZeichenkette("\nEXCEPTION vec=")
	MEmergencyProtokollhexadecimal8(uint8(unterbrechung))
	MEmergencyProtokollZeichenkette(" ")
	MEmergencyProtokollZeichenkette(exceptionElementname(unterbrechung))
	MEmergencyProtokollZeichenkette(" frame=")
	MEmergencyProtokollunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyProtokollZeichenkette(" invalid-frame")
		if exceptionhasFehlercode(unterbrechung) {
			MEmergencyProtokollZeichenkette(" raw-error-or-bad-esp=")
			MEmergencyProtokollunsignedinteger32(esp)
			druckenexceptionselectorinfo(esp)
		}
		MEmergencyProtokollZeichenkette("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipVersatz uint32 = 0
	if exceptionhasFehlercode(unterbrechung) {
		err = exceptionRahmenWert(esp, 0)
		eipVersatz = 4
	}
	eip := exceptionRahmenWert(esp, eipVersatz)
	cs := exceptionRahmenWert(esp, eipVersatz+4)
	eflags := exceptionRahmenWert(esp, eipVersatz+8)

	MEmergencyProtokollZeichenkette(" err=")
	MEmergencyProtokollunsignedinteger32(err)
	MEmergencyProtokollZeichenkette(" eip=")
	MEmergencyProtokollunsignedinteger32(eip)
	MEmergencyProtokollZeichenkette(" cs=")
	MEmergencyProtokollunsignedinteger32(cs)
	MEmergencyProtokollZeichenkette(" eflags=")
	MEmergencyProtokollunsignedinteger32(eflags)
	MEmergencyProtokollZeichenkette(" cr0=")
	MEmergencyProtokollunsignedinteger32(exceptioncr0())
	MEmergencyProtokollZeichenkette(" cr3=")
	MEmergencyProtokollunsignedinteger32(exceptioncr3())

	if unterbrechung == 0x0E {
		MEmergencyProtokollZeichenkette(" cr2=")
		MEmergencyProtokollunsignedinteger32(exceptioncr2())
		druckenSeiteFehlerinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencyProtokollZeichenkette(" useresp=")
		MEmergencyProtokollunsignedinteger32(exceptionRahmenWert(esp, eipVersatz+12))
		MEmergencyProtokollZeichenkette(" ss=")
		MEmergencyProtokollunsignedinteger32(exceptionRahmenWert(esp, eipVersatz+16))
	}

	if exceptionhasFehlercode(unterbrechung) {
		druckenexceptionselectorinfo(err)
	}
	MEmergencyProtokollZeichenkette("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltNachfatalexception()

func GrifffatalUnterbrechungRahmen(gespeichertesp uint32, unterbrechung uint32) uint32 {
	Griffexception(gespeichertesp+52, unterbrechung)
	haltNachfatalexception()
	return gespeichertesp
}

func UnterbrechungAktiv()
func (selbst *TUnterbrechungVerwalter) Aktiv() {
	if AktivUnterbrechungVerwalter != 0 {
		selbst.Deactive()
	}
	address := uintptr(Pointer(selbst))
	AktivUnterbrechungVerwalter = address
	UnterbrechungAktiv()
}
func Unterbrechungdeactive()
func (selbst *TUnterbrechungVerwalter) Deactive() {
	AktivUnterbrechungVerwalter = 0
	Unterbrechungdeactive()
}

func MyGriffUnterbrechung(unterbrechung uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konsole_2 := TKonsole{}
	konsole_2.MDrucken(buffer)
	return esp
}
func MyTesten(unterbrechung uint8, esp uint32)

func UnhandleUnterbrechung() {
	buffer := []byte("unhandle interrupt\n")
	konsole_2 := TKonsole{}
	konsole_2.MDrucken(buffer)
}

func unterbrechunghandler_2(unterbrechung uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konsole_2 := TKonsole{}
	konsole_2.MDrucken(buffer)
	konsole_2.MHexadecimalDrucken(0x40)
	return esp
}
func druckenesp(esp uint32) {
	konsole_2 := TKonsole{}
	konsole_2.MUnsignedinteger32Druckenxy(esp, 20, 21)
}
func gettls() uint32
func Druckentls() {

}
