/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Przerwanie

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "konsola"

func przerwanieignore()

func przerwanieexceptionhandler()
func przerwanieexceptionhandler0x00()
func przerwanieexceptionhandler0x01()
func przerwanieexceptionhandler0x02()
func przerwanieexceptionhandler0x03()
func przerwanieexceptionhandler0x04()
func przerwanieexceptionhandler0x05()
func przerwanieexceptionhandler0x06()
func przerwanieexceptionhandler0x07()
func przerwanieexceptionhandler0x08()
func przerwanieexceptionhandler0x09()
func przerwanieexceptionhandler0x0a()
func przerwanieexceptionhandler0x0b()
func przerwanieexceptionhandler0x0c()
func przerwanieexceptionhandler0x0d()
func przerwanieexceptionhandler0x0e()
func przerwanieexceptionhandler0x0f()
func przerwanieexceptionhandler0x10()
func przerwanieexceptionhandler0x11()
func przerwanieexceptionhandler0x12()
func przerwanieexceptionhandler0x13()

func przerwanierequesthandler0x00()
func przerwanierequesthandler0x01()
func przerwanierequesthandler0x02()
func przerwanierequesthandler0x03()
func przerwanierequesthandler0x04()
func przerwanierequesthandler0x05()
func przerwanierequesthandler0x06()
func przerwanierequesthandler0x07()
func przerwanierequesthandler0x08()
func przerwanierequesthandler0x09()
func przerwanierequesthandler0x0a()
func przerwanierequesthandler0x0b()
func przerwanierequesthandler0x0c()
func przerwanierequesthandler0x0d()
func przerwanierequesthandler0x0e()
func przerwanierequesthandler0x0f()

func przerwanierequesthandler0x80()
func przerwanierequesthandler0x81()
func przerwanierequesthandler0x82()

func PrzetestujWydrukuj(pozycja uint8, data uint8)
func zbiórds(dssegment uint32)
func zbiórgs(gssegment uint32)
func przerwanieZakończloop()

type TPrzerwaniehandler struct {
	PrzerwanieLiczba	uint8
	Przerwaniemanager	uintptr
}
type IPrzerwaniehandler interface {
	UchwytPrzerwanie(uint32) uint32
}

func NowyPrzerwaniehandler(Przerwaniemanager uintptr, PrzerwanieLiczba uint8) *TPrzerwaniehandler {
	przerwaniehandler_2 := new(TPrzerwaniehandler)
	przerwaniehandler_2.PrzerwanieLiczba = PrzerwanieLiczba
	przerwaniehandler_2.Przerwaniemanager = Przerwaniemanager
	return przerwaniehandler_2

}

var handler_2 [256]uintptr

func (bieżący *TPrzerwaniehandler) Init(PrzerwanieLiczba uint8, Przerwaniemanager uintptr, funcAdres uintptr) {

	handler_2[PrzerwanieLiczba] = funcAdres

	bieżący.PrzerwanieLiczba = PrzerwanieLiczba
	bieżący.Przerwaniemanager = Przerwaniemanager

}
func (bieżący *TPrzerwaniehandler) ZbiórUchwytPrzerwaniefuction(PrzerwanieLiczba uint32, adres uintptr) {
	handler_2[PrzerwanieLiczba] = adres
}
func (bieżący *TPrzerwaniehandler) Zniszcz() {
	bieżącyuintptr := uintptr(Pointer(bieżący))
	Przerwaniemanager := (*TPrzerwaniemanager)(Pointer(bieżący.Przerwaniemanager))
	if bieżącyuintptr == Przerwaniemanager.Gethandler(bieżący.PrzerwanieLiczba) {
		Przerwaniemanager.Zbiórhandler(0, bieżący.PrzerwanieLiczba)
	}

}
func (bieżący *TPrzerwaniehandler) ZbiórPrzerwaniemanager(Przerwaniemanager uintptr) {
}
func (bieżący *TPrzerwaniehandler) ZbiórPrzerwanieLiczba(PrzerwanieLiczba uint8) {
	bieżący.PrzerwanieLiczba = PrzerwanieLiczba
}
func (bieżący *TPrzerwaniehandler) UchwytPrzerwanie(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konsola_2 := TKonsola{}
	konsola_2.MWydrukuj(buffer)
	return esp
}
func UchwytPrzerwanie1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konsola_2 := TKonsola{}
	konsola_2.MWydrukuj(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TPrzerwaniedescriptorTabelaKursor struct {
}

var idtdata [256 * 8]uint8
var AktywnePrzerwaniemanager uintptr = 0

const przerwanieDiagnozuj = false

type TPrzerwaniemanager struct {
	handler_2	[256]uintptr

	sprzętPrzerwaniePrzesunięcie	uint16

	zadaniemanager	*TZadaniemanager
}

var PrimarypicPolecenieWEWYport uint16 = 0x20
var PrimarypicdataWEWYport uint16 = 0x21
var SecondarypicPolecenieWEWYport uint16 = 0xA0
var SecondarypicdataWEWYport uint16 = 0xA1

func (bieżący *TPrzerwaniemanager) Init(sprzętPrzerwaniePrzesunięcie uint16, globalnydescriptorTabela *TShareddescriptorTabela, zadaniemanager *TZadaniemanager) {

	bieżący.zadaniemanager = zadaniemanager

	bieżący.sprzętPrzerwaniePrzesunięcie = sprzętPrzerwaniePrzesunięcie
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var adres uint32
	var IdtPrzerwaniegate uint8 = 0xE
	adres = uint32(ValueOf(przerwanieignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		adres = uint32(ValueOf(przerwanieexceptionhandler0x0f).Pointer())
		bieżący.PrzerwaniedescriptorTabelawpiszbiór(i, codesegment, adres, 0, IdtPrzerwaniegate)
	}

	adres = uint32(ValueOf(przerwanieexceptionhandler0x00).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x00, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x01).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x01, codesegment, adres, 0, IdtPrzerwaniegate)
	adres = uint32(ValueOf(przerwanieexceptionhandler0x02).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x02, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x03).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x03, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x04).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x04, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x05).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x05, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x06).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x06, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x07).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x07, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x08).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x08, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x09).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x09, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x0a).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x0A, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x0b).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x0B, codesegment, adres, 0, IdtPrzerwaniegate)
	adres = uint32(ValueOf(przerwanieexceptionhandler0x0c).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x0C, codesegment, adres, 0, IdtPrzerwaniegate)
	adres = uint32(ValueOf(przerwanieexceptionhandler0x0d).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x0D, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x0e).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x0E, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x0f).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x0F, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x10).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x10, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x11).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x11, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x12).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x12, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanieexceptionhandler0x13).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x13, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x00).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x20, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x01).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x21, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x02).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x22, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x03).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x23, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x04).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x24, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x05).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x25, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x06).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x26, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x07).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x27, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x08).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x28, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x09).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x29, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x0a).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x2A, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x0b).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x2B, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x0c).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x2C, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x0d).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x2D, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x0e).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x2E, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x0f).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x2F, codesegment, adres, 0, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x80).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x80, codesegment, adres, 3, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x81).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x81, codesegment, adres, 3, IdtPrzerwaniegate)

	adres = uint32(ValueOf(przerwanierequesthandler0x82).Pointer())
	bieżący.PrzerwaniedescriptorTabelawpiszbiór(0x82, codesegment, adres, 3, IdtPrzerwaniegate)

	PortZapisbyte(PrimarypicPolecenieWEWYport, 0x11)
	PortZapisbyte(SecondarypicPolecenieWEWYport, 0x11)

	PortZapisbyte(PrimarypicdataWEWYport, 0x20)
	PortZapisbyte(SecondarypicdataWEWYport, 0x28)

	PortZapisbyte(PrimarypicdataWEWYport, 0x04)
	PortZapisbyte(SecondarypicdataWEWYport, 0x02)

	PortZapisbyte(PrimarypicdataWEWYport, 0x01)
	PortZapisbyte(SecondarypicdataWEWYport, 0x01)

	PortZapisbyte(PrimarypicdataWEWYport, 0xF8)
	PortZapisbyte(SecondarypicdataWEWYport, 0xEF)

	idtKursor := [6]uint8{0, 0, 0, 0, 0, 0}
	rozmiar := (*uint16)(Pointer(&idtKursor[0]))
	(*rozmiar) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtKursor[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtKursor)))
}
func Lidt(lidtaddr uintptr)

func (bieżący *TPrzerwaniemanager) PrzerwaniedescriptorTabelawpiszbiór(przerwanie int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTyp uint8) {

	handlerAdresNiskib := (*uint16)(Pointer(&idtdata[przerwanie*8+0]))
	(*handlerAdresNiskib) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[przerwanie*8+2]))
	(*gdtcodesegmentselector) = codesegment

	zastrzeżone := (*uint8)(Pointer(&idtdata[przerwanie*8+4]))
	(*zastrzeżone) = 0

	var IdtdescriptorObecny uint8 = 0x80
	dostępu := (*uint8)(Pointer(&idtdata[przerwanie*8+5]))
	(*dostępu) = (IdtdescriptorObecny | DescriptorTyp | ((Descriptorprivilegelevel & 3) << 5))

	handlerAdresWysokib := (*uint16)(Pointer(&idtdata[przerwanie*8+6]))
	(*handlerAdresWysokib) = uint16((handler >> 16) & 0xFFFF)

}

func (bieżący *TPrzerwaniemanager) Zbiórhandler(handler uintptr, PrzerwanieLiczba uint8) {
	handler_2[PrzerwanieLiczba] = handler
}
func (bieżący *TPrzerwaniemanager) Gethandler(PrzerwanieLiczba uint8) uintptr {
	return handler_2[PrzerwanieLiczba]
}
func (bieżący *TPrzerwaniemanager) DoUchwytPrzerwanie(przerwanie uint8, esp uint32) uint32 {

	if przerwanieDiagnozuj {
		konsola_2.MWydrukujxy("[esp:", 1, 20)
		konsola_2.MUnsignedinteger32Wydrukuj(uint32(przerwanie))
		konsola_2.MWydrukuj(":")
		konsola_2.MUnsignedinteger32Wydrukuj(esp)
	}
	handlerUruchom := false
	if handler_2[przerwanie] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[przerwanie])))
		esp = myfunction(esp)
		handlerUruchom = true

	}

	if !handlerUruchom && przerwanie == uint8(bieżący.sprzętPrzerwaniePrzesunięcie) && bieżący.zadaniemanager != nil {
		esp = uint32(uintptr(Pointer(bieżący.zadaniemanager.Schedule((*TcpuStan)(Pointer(uintptr(esp)))))))

	}
	if !handlerUruchom && przerwanie == 0x80 {
		esp = uchwytunhandledsyscall(esp)
	}

	if przerwanie <= 0x1F {
	}
	if 0x20 <= przerwanie && przerwanie < 0x30 {
		if 0x28 <= przerwanie {
			PortZapisbyte(SecondarypicPolecenieWEWYport, 0x20)
		}
		PortZapisbyte(PrimarypicPolecenieWEWYport, 0x20)
	}
	return esp
}

var liczba2 uint8 = 1

func zbiórcr3(adres uint32)

var konsola_2 TKonsola = TKonsola{}

func UchwytPrzerwanie(esp uint32, przerwanie uint32) uint32 {

	if przerwanieDiagnozuj && przerwanie != 0x80 && przerwanie != 0x20 {
		konsola_2.MWydrukujxy("[esp:", 1, 21)
		konsola_2.MUnsignedinteger32Wydrukuj(uint32(przerwanie))
		konsola_2.MWydrukuj(":")
		konsola_2.MUnsignedinteger32Wydrukuj(esp)
	}

	if AktywnePrzerwaniemanager != 0 {
		p := (*TPrzerwaniemanager)(Pointer(AktywnePrzerwaniemanager))
		esp = p.DoUchwytPrzerwanie(uint8(przerwanie), esp)
		return esp
	}
	if handler_2[przerwanie] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[przerwanie])))
		esp = myfunction(esp)
	}
	if przerwanie == 0x80 {
		return uchwytunhandledsyscall(esp)
	}
	if 0x20 <= przerwanie && przerwanie < 0x30 {
		if 0x28 <= przerwanie {
			PortZapisbyte(SecondarypicPolecenieWEWYport, 0x20)
		}
		PortZapisbyte(PrimarypicPolecenieWEWYport, 0x20)
	}

	return esp
}

func uchwytunhandledsyscall(esp uint32) uint32 {
	procesor := (*TcpuStan)(Pointer(uintptr(esp)))
	if procesor.Eax == 1 || procesor.Eax == 252 {
		procesor.Eip = uint32(ValueOf(przerwanieZakończloop).Pointer())
		procesor.Cs = Segkernelcode
		procesor.Ds = Segkerneldata
		procesor.Es = Segkerneldata
		procesor.Fs = Segkerneldata
		procesor.Gs = Segkernelgs
		procesor.Ss = Segkerneldata
		procesor.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasBłądcode(przerwanie uint32) bool {
	switch przerwanie {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNazwa(przerwanie uint32) string {
	switch przerwanie {
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

func exceptionRamkaWartość(ramka uint32, przesunięcie uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ramka + przesunięcie)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func wydrukujStronafaultInformacja(błędy uint32) {
	MEmergencyDziennikCIĄG(" pf=[")
	if (błędy & 0x01) != 0 {
		MEmergencyDziennikCIĄG("protection")
	} else {
		MEmergencyDziennikCIĄG("not-present")
	}
	if (błędy & 0x02) != 0 {
		MEmergencyDziennikCIĄG(",write")
	} else {
		MEmergencyDziennikCIĄG(",read")
	}
	if (błędy & 0x04) != 0 {
		MEmergencyDziennikCIĄG(",user")
	} else {
		MEmergencyDziennikCIĄG(",kernel")
	}
	if (błędy & 0x08) != 0 {
		MEmergencyDziennikCIĄG(",reserved-bit")
	}
	if (błędy & 0x10) != 0 {
		MEmergencyDziennikCIĄG(",instruction-fetch")
	}
	MEmergencyDziennikCIĄG("]")
}

func wydrukujexceptionselectorInformacja(błędy uint32) {
	MEmergencyDziennikCIĄG(" selector=")
	MEmergencyDziennikunsignedinteger32(błędy & 0xFFFFFFF8)
	MEmergencyDziennikCIĄG(" index=")
	MEmergencyDziennikunsignedinteger32(błędy >> 3)
	MEmergencyDziennikCIĄG(" table=")
	if (błędy & 0x02) != 0 {
		MEmergencyDziennikCIĄG("IDT")
	} else if (błędy & 0x04) != 0 {
		MEmergencyDziennikCIĄG("LDT")
	} else {
		MEmergencyDziennikCIĄG("GDT")
	}
	MEmergencyDziennikCIĄG(" ext=")
	MEmergencyDziennikunsignedinteger32(błędy & 0x01)
}

func Uchwytexception(esp uint32, przerwanie uint32) uint32 {
	MEmergencyDziennikCIĄG("\nEXCEPTION vec=")
	MEmergencyDziennikhexadecimal8(uint8(przerwanie))
	MEmergencyDziennikCIĄG(" ")
	MEmergencyDziennikCIĄG(exceptionNazwa(przerwanie))
	MEmergencyDziennikCIĄG(" frame=")
	MEmergencyDziennikunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyDziennikCIĄG(" invalid-frame")
		if exceptionhasBłądcode(przerwanie) {
			MEmergencyDziennikCIĄG(" raw-error-or-bad-esp=")
			MEmergencyDziennikunsignedinteger32(esp)
			wydrukujexceptionselectorInformacja(esp)
		}
		MEmergencyDziennikCIĄG("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var błędy uint32 = 0
	var eipPrzesunięcie uint32 = 0
	if exceptionhasBłądcode(przerwanie) {
		błędy = exceptionRamkaWartość(esp, 0)
		eipPrzesunięcie = 4
	}
	eip := exceptionRamkaWartość(esp, eipPrzesunięcie)
	cs := exceptionRamkaWartość(esp, eipPrzesunięcie+4)
	eflags := exceptionRamkaWartość(esp, eipPrzesunięcie+8)

	MEmergencyDziennikCIĄG(" err=")
	MEmergencyDziennikunsignedinteger32(błędy)
	MEmergencyDziennikCIĄG(" eip=")
	MEmergencyDziennikunsignedinteger32(eip)
	MEmergencyDziennikCIĄG(" cs=")
	MEmergencyDziennikunsignedinteger32(cs)
	MEmergencyDziennikCIĄG(" eflags=")
	MEmergencyDziennikunsignedinteger32(eflags)
	MEmergencyDziennikCIĄG(" cr0=")
	MEmergencyDziennikunsignedinteger32(exceptioncr0())
	MEmergencyDziennikCIĄG(" cr3=")
	MEmergencyDziennikunsignedinteger32(exceptioncr3())

	if przerwanie == 0x0E {
		MEmergencyDziennikCIĄG(" cr2=")
		MEmergencyDziennikunsignedinteger32(exceptioncr2())
		wydrukujStronafaultInformacja(błędy)
	}

	if (cs & 0x03) != 0 {
		MEmergencyDziennikCIĄG(" useresp=")
		MEmergencyDziennikunsignedinteger32(exceptionRamkaWartość(esp, eipPrzesunięcie+12))
		MEmergencyDziennikCIĄG(" ss=")
		MEmergencyDziennikunsignedinteger32(exceptionRamkaWartość(esp, eipPrzesunięcie+16))
	}

	if exceptionhasBłądcode(przerwanie) {
		wydrukujexceptionselectorInformacja(błędy)
	}
	MEmergencyDziennikCIĄG("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltNajpierwkoniecwierszafatalexception()

func UchwytfatalPrzerwanieRamka(zapisaneesp uint32, przerwanie uint32) uint32 {
	Uchwytexception(zapisaneesp+52, przerwanie)
	haltNajpierwkoniecwierszafatalexception()
	return zapisaneesp
}

func PrzerwanieAktywne()
func (bieżący *TPrzerwaniemanager) Aktywne() {
	if AktywnePrzerwaniemanager != 0 {
		bieżący.Deactive()
	}
	adres := uintptr(Pointer(bieżący))
	AktywnePrzerwaniemanager = adres
	PrzerwanieAktywne()
}
func Przerwaniedeactive()
func (bieżący *TPrzerwaniemanager) Deactive() {
	AktywnePrzerwaniemanager = 0
	Przerwaniedeactive()
}

func MyUchwytPrzerwanie(przerwanie uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konsola_2 := TKonsola{}
	konsola_2.MWydrukuj(buffer)
	return esp
}
func MyPrzetestuj(przerwanie uint8, esp uint32)

func UnhandlePrzerwanie() {
	buffer := []byte("unhandle interrupt\n")
	konsola_2 := TKonsola{}
	konsola_2.MWydrukuj(buffer)
}

func przerwaniehandler_2(przerwanie uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konsola_2 := TKonsola{}
	konsola_2.MWydrukuj(buffer)
	konsola_2.MHexadecimalWydrukuj(0x40)
	return esp
}
func wydrukujesp(esp uint32) {
	konsola_2 := TKonsola{}
	konsola_2.MUnsignedinteger32Wydrukujxy(esp, 20, 21)
}
func gettls() uint32
func Wydrukujtls() {

}
