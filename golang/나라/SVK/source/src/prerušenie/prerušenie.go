package Prerušenie

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "konzola"

func prerušenieignore()

func prerušenieexceptionhandler()
func prerušenieexceptionhandler0x00()
func prerušenieexceptionhandler0x01()
func prerušenieexceptionhandler0x02()
func prerušenieexceptionhandler0x03()
func prerušenieexceptionhandler0x04()
func prerušenieexceptionhandler0x05()
func prerušenieexceptionhandler0x06()
func prerušenieexceptionhandler0x07()
func prerušenieexceptionhandler0x08()
func prerušenieexceptionhandler0x09()
func prerušenieexceptionhandler0x0a()
func prerušenieexceptionhandler0x0b()
func prerušenieexceptionhandler0x0c()
func prerušenieexceptionhandler0x0d()
func prerušenieexceptionhandler0x0e()
func prerušenieexceptionhandler0x0f()
func prerušenieexceptionhandler0x10()
func prerušenieexceptionhandler0x11()
func prerušenieexceptionhandler0x12()
func prerušenieexceptionhandler0x13()

func prerušenierequesthandler0x00()
func prerušenierequesthandler0x01()
func prerušenierequesthandler0x02()
func prerušenierequesthandler0x03()
func prerušenierequesthandler0x04()
func prerušenierequesthandler0x05()
func prerušenierequesthandler0x06()
func prerušenierequesthandler0x07()
func prerušenierequesthandler0x08()
func prerušenierequesthandler0x09()
func prerušenierequesthandler0x0a()
func prerušenierequesthandler0x0b()
func prerušenierequesthandler0x0c()
func prerušenierequesthandler0x0d()
func prerušenierequesthandler0x0e()
func prerušenierequesthandler0x0f()

func prerušenierequesthandler0x80()
func prerušenierequesthandler0x81()
func prerušenierequesthandler0x82()

func OtestovaťTlačiť(pozícia uint8, data uint8)
func sadads(dssegment uint32)
func sadags(gssegment uint32)
func prerušenieKoniecloop()

type TPrerušeniehandler struct {
	PrerušenieČíslo		uint8
	Prerušeniemanager	uintptr
}
type IPrerušeniehandler interface {
	UškoPrerušenie(uint32) uint32
}

func NovýPrerušeniehandler(Prerušeniemanager uintptr, PrerušenieČíslo uint8) *TPrerušeniehandler {
	prerušeniehandler_2 := new(TPrerušeniehandler)
	prerušeniehandler_2.PrerušenieČíslo = PrerušenieČíslo
	prerušeniehandler_2.Prerušeniemanager = Prerušeniemanager
	return prerušeniehandler_2

}

var handler_2 [256]uintptr

func (vlastný *TPrerušeniehandler) Init(PrerušenieČíslo uint8, Prerušeniemanager uintptr, funcaddress uintptr) {

	handler_2[PrerušenieČíslo] = funcaddress

	vlastný.PrerušenieČíslo = PrerušenieČíslo
	vlastný.Prerušeniemanager = Prerušeniemanager

}
func (vlastný *TPrerušeniehandler) SadaUškoPrerušeniefuction(PrerušenieČíslo uint32, address uintptr) {
	handler_2[PrerušenieČíslo] = address
}
func (vlastný *TPrerušeniehandler) Zničiť() {
	vlastnýuintptr := uintptr(Pointer(vlastný))
	Prerušeniemanager := (*TPrerušeniemanager)(Pointer(vlastný.Prerušeniemanager))
	if vlastnýuintptr == Prerušeniemanager.Gethandler(vlastný.PrerušenieČíslo) {
		Prerušeniemanager.Sadahandler(0, vlastný.PrerušenieČíslo)
	}

}
func (vlastný *TPrerušeniehandler) SadaPrerušeniemanager(Prerušeniemanager uintptr) {
}
func (vlastný *TPrerušeniehandler) SadaPrerušenieČíslo(PrerušenieČíslo uint8) {
	vlastný.PrerušenieČíslo = PrerušenieČíslo
}
func (vlastný *TPrerušeniehandler) UškoPrerušenie(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konzola_2 := TKonzola{}
	konzola_2.MTlačiť(buffer)
	return esp
}
func UškoPrerušenie1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konzola_2 := TKonzola{}
	konzola_2.MTlačiť(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TPrerušeniedescriptorTabuľkaKurzor struct {
}

var idtdata [256 * 8]uint8
var AktívnyPrerušeniemanager uintptr = 0

const prerušenieLadenie = false

type TPrerušeniemanager struct {
	handler_2	[256]uintptr

	hardvérPrerušeniePosunutie	uint16

	ulohamanager	*TUlohamanager
}

var PrimarypicPríkazioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicPríkazioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (vlastný *TPrerušeniemanager) Init(hardvérPrerušeniePosunutie uint16, globálnydescriptorTabuľka *TShareddescriptorTabuľka, ulohamanager *TUlohamanager) {

	vlastný.ulohamanager = ulohamanager

	vlastný.hardvérPrerušeniePosunutie = hardvérPrerušeniePosunutie
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtPrerušeniegate uint8 = 0xE
	address = uint32(ValueOf(prerušenieignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(prerušenieexceptionhandler0x0f).Pointer())
		vlastný.PrerušeniedescriptorTabuľkapoložkasada(i, codesegment, address, 0, IdtPrerušeniegate)
	}

	address = uint32(ValueOf(prerušenieexceptionhandler0x00).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x00, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x01).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x01, codesegment, address, 0, IdtPrerušeniegate)
	address = uint32(ValueOf(prerušenieexceptionhandler0x02).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x02, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x03).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x03, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x04).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x04, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x05).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x05, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x06).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x06, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x07).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x07, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x08).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x08, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x09).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x09, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x0a).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x0A, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x0b).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x0B, codesegment, address, 0, IdtPrerušeniegate)
	address = uint32(ValueOf(prerušenieexceptionhandler0x0c).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x0C, codesegment, address, 0, IdtPrerušeniegate)
	address = uint32(ValueOf(prerušenieexceptionhandler0x0d).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x0D, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x0e).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x0E, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x0f).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x0F, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x10).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x10, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x11).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x11, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x12).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x12, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenieexceptionhandler0x13).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x13, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x00).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x20, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x01).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x21, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x02).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x22, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x03).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x23, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x04).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x24, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x05).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x25, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x06).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x26, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x07).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x27, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x08).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x28, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x09).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x29, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x0a).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x2A, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x0b).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x2B, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x0c).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x2C, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x0d).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x2D, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x0e).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x2E, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x0f).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x2F, codesegment, address, 0, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x80).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x80, codesegment, address, 3, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x81).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x81, codesegment, address, 3, IdtPrerušeniegate)

	address = uint32(ValueOf(prerušenierequesthandler0x82).Pointer())
	vlastný.PrerušeniedescriptorTabuľkapoložkasada(0x82, codesegment, address, 3, IdtPrerušeniegate)

	PortZápisbyte(PrimarypicPríkazioport, 0x11)
	PortZápisbyte(SecondarypicPríkazioport, 0x11)

	PortZápisbyte(Primarypicdataioport, 0x20)
	PortZápisbyte(Secondarypicdataioport, 0x28)

	PortZápisbyte(Primarypicdataioport, 0x04)
	PortZápisbyte(Secondarypicdataioport, 0x02)

	PortZápisbyte(Primarypicdataioport, 0x01)
	PortZápisbyte(Secondarypicdataioport, 0x01)

	PortZápisbyte(Primarypicdataioport, 0xF8)
	PortZápisbyte(Secondarypicdataioport, 0xEF)

	idtKurzor := [6]uint8{0, 0, 0, 0, 0, 0}
	veľkosť := (*uint16)(Pointer(&idtKurzor[0]))
	(*veľkosť) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtKurzor[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtKurzor)))
}
func Lidt(lidtaddr uintptr)

func (vlastný *TPrerušeniemanager) PrerušeniedescriptorTabuľkapoložkasada(prerušenie int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTyp uint8) {

	handleraddressNízkabity := (*uint16)(Pointer(&idtdata[prerušenie*8+0]))
	(*handleraddressNízkabity) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[prerušenie*8+2]))
	(*gdtcodesegmentselector) = codesegment

	rezervovaná := (*uint8)(Pointer(&idtdata[prerušenie*8+4]))
	(*rezervovaná) = 0

	var IdtdescriptorPrítomné uint8 = 0x80
	prístup := (*uint8)(Pointer(&idtdata[prerušenie*8+5]))
	(*prístup) = (IdtdescriptorPrítomné | DescriptorTyp | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressVysokábity := (*uint16)(Pointer(&idtdata[prerušenie*8+6]))
	(*handleraddressVysokábity) = uint16((handler >> 16) & 0xFFFF)

}

func (vlastný *TPrerušeniemanager) Sadahandler(handler uintptr, PrerušenieČíslo uint8) {
	handler_2[PrerušenieČíslo] = handler
}
func (vlastný *TPrerušeniemanager) Gethandler(PrerušenieČíslo uint8) uintptr {
	return handler_2[PrerušenieČíslo]
}
func (vlastný *TPrerušeniemanager) DoUškoPrerušenie(prerušenie uint8, esp uint32) uint32 {

	if prerušenieLadenie {
		konzola_2.MTlačiťxy("[esp:", 1, 20)
		konzola_2.MUnsignedinteger32Tlačiť(uint32(prerušenie))
		konzola_2.MTlačiť(":")
		konzola_2.MUnsignedinteger32Tlačiť(esp)
	}
	handlerSpustiť := false
	if handler_2[prerušenie] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[prerušenie])))
		esp = myfunction(esp)
		handlerSpustiť = true

	}

	if !handlerSpustiť && prerušenie == uint8(vlastný.hardvérPrerušeniePosunutie) && vlastný.ulohamanager != nil {
		esp = uint32(uintptr(Pointer(vlastný.ulohamanager.Schedule((*TcpuStav)(Pointer(uintptr(esp)))))))

	}
	if !handlerSpustiť && prerušenie == 0x80 {
		esp = uškounhandledsyscall(esp)
	}

	if prerušenie <= 0x1F {
	}
	if 0x20 <= prerušenie && prerušenie < 0x30 {
		if 0x28 <= prerušenie {
			PortZápisbyte(SecondarypicPríkazioport, 0x20)
		}
		PortZápisbyte(PrimarypicPríkazioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func sadacr3(address uint32)

var konzola_2 TKonzola = TKonzola{}

func UškoPrerušenie(esp uint32, prerušenie uint32) uint32 {

	if prerušenieLadenie && prerušenie != 0x80 && prerušenie != 0x20 {
		konzola_2.MTlačiťxy("[esp:", 1, 21)
		konzola_2.MUnsignedinteger32Tlačiť(uint32(prerušenie))
		konzola_2.MTlačiť(":")
		konzola_2.MUnsignedinteger32Tlačiť(esp)
	}

	if AktívnyPrerušeniemanager != 0 {
		p := (*TPrerušeniemanager)(Pointer(AktívnyPrerušeniemanager))
		esp = p.DoUškoPrerušenie(uint8(prerušenie), esp)
		return esp
	}
	if handler_2[prerušenie] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[prerušenie])))
		esp = myfunction(esp)
	}
	if prerušenie == 0x80 {
		return uškounhandledsyscall(esp)
	}
	if 0x20 <= prerušenie && prerušenie < 0x30 {
		if 0x28 <= prerušenie {
			PortZápisbyte(SecondarypicPríkazioport, 0x20)
		}
		PortZápisbyte(PrimarypicPríkazioport, 0x20)
	}

	return esp
}

func uškounhandledsyscall(esp uint32) uint32 {
	procesor := (*TcpuStav)(Pointer(uintptr(esp)))
	if procesor.Eax == 1 || procesor.Eax == 252 {
		procesor.Eip = uint32(ValueOf(prerušenieKoniecloop).Pointer())
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

func exceptionhasChybacode(prerušenie uint32) bool {
	switch prerušenie {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNázov(prerušenie uint32) string {
	switch prerušenie {
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

func exceptionRámecHodnota(rámec uint32, posunutie uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(rámec + posunutie)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func tlačiťSTRANAfaultInformácie(err uint32) {
	MEmergencyZaznamenávaniereťazec(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencyZaznamenávaniereťazec("protection")
	} else {
		MEmergencyZaznamenávaniereťazec("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencyZaznamenávaniereťazec(",write")
	} else {
		MEmergencyZaznamenávaniereťazec(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencyZaznamenávaniereťazec(",user")
	} else {
		MEmergencyZaznamenávaniereťazec(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencyZaznamenávaniereťazec(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencyZaznamenávaniereťazec(",instruction-fetch")
	}
	MEmergencyZaznamenávaniereťazec("]")
}

func tlačiťexceptionselectorInformácie(err uint32) {
	MEmergencyZaznamenávaniereťazec(" selector=")
	MEmergencyZaznamenávanieunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencyZaznamenávaniereťazec(" index=")
	MEmergencyZaznamenávanieunsignedinteger32(err >> 3)
	MEmergencyZaznamenávaniereťazec(" table=")
	if (err & 0x02) != 0 {
		MEmergencyZaznamenávaniereťazec("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencyZaznamenávaniereťazec("LDT")
	} else {
		MEmergencyZaznamenávaniereťazec("GDT")
	}
	MEmergencyZaznamenávaniereťazec(" ext=")
	MEmergencyZaznamenávanieunsignedinteger32(err & 0x01)
}

func Uškoexception(esp uint32, prerušenie uint32) uint32 {
	MEmergencyZaznamenávaniereťazec("\nEXCEPTION vec=")
	MEmergencyZaznamenávaniehexadecimal8(uint8(prerušenie))
	MEmergencyZaznamenávaniereťazec(" ")
	MEmergencyZaznamenávaniereťazec(exceptionNázov(prerušenie))
	MEmergencyZaznamenávaniereťazec(" frame=")
	MEmergencyZaznamenávanieunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyZaznamenávaniereťazec(" invalid-frame")
		if exceptionhasChybacode(prerušenie) {
			MEmergencyZaznamenávaniereťazec(" raw-error-or-bad-esp=")
			MEmergencyZaznamenávanieunsignedinteger32(esp)
			tlačiťexceptionselectorInformácie(esp)
		}
		MEmergencyZaznamenávaniereťazec("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipPosunutie uint32 = 0
	if exceptionhasChybacode(prerušenie) {
		err = exceptionRámecHodnota(esp, 0)
		eipPosunutie = 4
	}
	eip := exceptionRámecHodnota(esp, eipPosunutie)
	cs := exceptionRámecHodnota(esp, eipPosunutie+4)
	eflags := exceptionRámecHodnota(esp, eipPosunutie+8)

	MEmergencyZaznamenávaniereťazec(" err=")
	MEmergencyZaznamenávanieunsignedinteger32(err)
	MEmergencyZaznamenávaniereťazec(" eip=")
	MEmergencyZaznamenávanieunsignedinteger32(eip)
	MEmergencyZaznamenávaniereťazec(" cs=")
	MEmergencyZaznamenávanieunsignedinteger32(cs)
	MEmergencyZaznamenávaniereťazec(" eflags=")
	MEmergencyZaznamenávanieunsignedinteger32(eflags)
	MEmergencyZaznamenávaniereťazec(" cr0=")
	MEmergencyZaznamenávanieunsignedinteger32(exceptioncr0())
	MEmergencyZaznamenávaniereťazec(" cr3=")
	MEmergencyZaznamenávanieunsignedinteger32(exceptioncr3())

	if prerušenie == 0x0E {
		MEmergencyZaznamenávaniereťazec(" cr2=")
		MEmergencyZaznamenávanieunsignedinteger32(exceptioncr2())
		tlačiťSTRANAfaultInformácie(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencyZaznamenávaniereťazec(" useresp=")
		MEmergencyZaznamenávanieunsignedinteger32(exceptionRámecHodnota(esp, eipPosunutie+12))
		MEmergencyZaznamenávaniereťazec(" ss=")
		MEmergencyZaznamenávanieunsignedinteger32(exceptionRámecHodnota(esp, eipPosunutie+16))
	}

	if exceptionhasChybacode(prerušenie) {
		tlačiťexceptionselectorInformácie(err)
	}
	MEmergencyZaznamenávaniereťazec("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func UškofatalPrerušenieRámec(uloženýesp uint32, prerušenie uint32) uint32 {
	Uškoexception(uloženýesp+52, prerušenie)
	haltafterfatalexception()
	return uloženýesp
}

func PrerušenieAktívny()
func (vlastný *TPrerušeniemanager) Aktívny() {
	if AktívnyPrerušeniemanager != 0 {
		vlastný.Deactive()
	}
	address := uintptr(Pointer(vlastný))
	AktívnyPrerušeniemanager = address
	PrerušenieAktívny()
}
func Prerušeniedeactive()
func (vlastný *TPrerušeniemanager) Deactive() {
	AktívnyPrerušeniemanager = 0
	Prerušeniedeactive()
}

func MyUškoPrerušenie(prerušenie uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konzola_2 := TKonzola{}
	konzola_2.MTlačiť(buffer)
	return esp
}
func MyOtestovať(prerušenie uint8, esp uint32)

func UnhandlePrerušenie() {
	buffer := []byte("unhandle interrupt\n")
	konzola_2 := TKonzola{}
	konzola_2.MTlačiť(buffer)
}

func prerušeniehandler_2(prerušenie uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konzola_2 := TKonzola{}
	konzola_2.MTlačiť(buffer)
	konzola_2.MHexadecimalTlačiť(0x40)
	return esp
}
func tlačiťesp(esp uint32) {
	konzola_2 := TKonzola{}
	konzola_2.MUnsignedinteger32Tlačiťxy(esp, 20, 21)
}
func gettls() uint32
func Tlačiťtls() {

}
