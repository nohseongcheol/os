/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Ometanje

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "konzola"

func ometanjeignore()

func ometanjeexceptionhandler()
func ometanjeexceptionhandler0x00()
func ometanjeexceptionhandler0x01()
func ometanjeexceptionhandler0x02()
func ometanjeexceptionhandler0x03()
func ometanjeexceptionhandler0x04()
func ometanjeexceptionhandler0x05()
func ometanjeexceptionhandler0x06()
func ometanjeexceptionhandler0x07()
func ometanjeexceptionhandler0x08()
func ometanjeexceptionhandler0x09()
func ometanjeexceptionhandler0x0a()
func ometanjeexceptionhandler0x0b()
func ometanjeexceptionhandler0x0c()
func ometanjeexceptionhandler0x0d()
func ometanjeexceptionhandler0x0e()
func ometanjeexceptionhandler0x0f()
func ometanjeexceptionhandler0x10()
func ometanjeexceptionhandler0x11()
func ometanjeexceptionhandler0x12()
func ometanjeexceptionhandler0x13()

func ometanjerequesthandler0x00()
func ometanjerequesthandler0x01()
func ometanjerequesthandler0x02()
func ometanjerequesthandler0x03()
func ometanjerequesthandler0x04()
func ometanjerequesthandler0x05()
func ometanjerequesthandler0x06()
func ometanjerequesthandler0x07()
func ometanjerequesthandler0x08()
func ometanjerequesthandler0x09()
func ometanjerequesthandler0x0a()
func ometanjerequesthandler0x0b()
func ometanjerequesthandler0x0c()
func ometanjerequesthandler0x0d()
func ometanjerequesthandler0x0e()
func ometanjerequesthandler0x0f()

func ometanjerequesthandler0x80()
func ometanjerequesthandler0x81()
func ometanjerequesthandler0x82()

func TestŠtampaj(položaj uint8, data uint8)
func skupds(dssegment uint32)
func skupgs(gssegment uint32)
func ometanjeIzlazloop()

type TOmetanjehandler struct {
	Ometanjebroj	uint8
	Ometanjemanager	uintptr
}
type IOmetanjehandler interface {
	RučkaOmetanje(uint32) uint32
}

func NovaOmetanjehandler(Ometanjemanager uintptr, Ometanjebroj uint8) *TOmetanjehandler {
	ometanjehandler_2 := new(TOmetanjehandler)
	ometanjehandler_2.Ometanjebroj = Ometanjebroj
	ometanjehandler_2.Ometanjemanager = Ometanjemanager
	return ometanjehandler_2

}

var handler_2 [256]uintptr

func (isti *TOmetanjehandler) Init(Ometanjebroj uint8, Ometanjemanager uintptr, funcaddress uintptr) {

	handler_2[Ometanjebroj] = funcaddress

	isti.Ometanjebroj = Ometanjebroj
	isti.Ometanjemanager = Ometanjemanager

}
func (isti *TOmetanjehandler) SkupRučkaOmetanjefuction(Ometanjebroj uint32, address uintptr) {
	handler_2[Ometanjebroj] = address
}
func (isti *TOmetanjehandler) Uništi() {
	istiuintptr := uintptr(Pointer(isti))
	Ometanjemanager := (*TOmetanjemanager)(Pointer(isti.Ometanjemanager))
	if istiuintptr == Ometanjemanager.Gethandler(isti.Ometanjebroj) {
		Ometanjemanager.Skuphandler(0, isti.Ometanjebroj)
	}

}
func (isti *TOmetanjehandler) SkupOmetanjemanager(Ometanjemanager uintptr) {
}
func (isti *TOmetanjehandler) SkupOmetanjebroj(Ometanjebroj uint8) {
	isti.Ometanjebroj = Ometanjebroj
}
func (isti *TOmetanjehandler) RučkaOmetanje(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konzola_2 := TKonzola{}
	konzola_2.MŠtampaj(buffer)
	return esp
}
func RučkaOmetanje1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konzola_2 := TKonzola{}
	konzola_2.MŠtampaj(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TOmetanjedescriptorTabelaPokazivač struct {
}

var idtdata [256 * 8]uint8
var AktivnaOmetanjemanager uintptr = 0

const ometanjeIspravljanje = false

type TOmetanjemanager struct {
	handler_2	[256]uintptr

	hardverOmetanjeoffset	uint16

	zadatakmanager	*TZadatakmanager
}

var PrimarypicNaredbaUIPort uint16 = 0x20
var PrimarypicdataUIPort uint16 = 0x21
var SecondarypicNaredbaUIPort uint16 = 0xA0
var SecondarypicdataUIPort uint16 = 0xA1

func (isti *TOmetanjemanager) Init(hardverOmetanjeoffset uint16, opštedescriptorTabela *TShareddescriptorTabela, zadatakmanager *TZadatakmanager) {

	isti.zadatakmanager = zadatakmanager

	isti.hardverOmetanjeoffset = hardverOmetanjeoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtOmetanjegate uint8 = 0xE
	address = uint32(ValueOf(ometanjeignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(ometanjeexceptionhandler0x0f).Pointer())
		isti.OmetanjedescriptorTabelaunosskup(i, codesegment, address, 0, IdtOmetanjegate)
	}

	address = uint32(ValueOf(ometanjeexceptionhandler0x00).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x00, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x01).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x01, codesegment, address, 0, IdtOmetanjegate)
	address = uint32(ValueOf(ometanjeexceptionhandler0x02).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x02, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x03).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x03, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x04).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x04, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x05).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x05, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x06).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x06, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x07).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x07, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x08).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x08, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x09).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x09, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x0a).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x0A, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x0b).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x0B, codesegment, address, 0, IdtOmetanjegate)
	address = uint32(ValueOf(ometanjeexceptionhandler0x0c).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x0C, codesegment, address, 0, IdtOmetanjegate)
	address = uint32(ValueOf(ometanjeexceptionhandler0x0d).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x0D, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x0e).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x0E, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x0f).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x0F, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x10).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x10, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x11).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x11, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x12).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x12, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjeexceptionhandler0x13).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x13, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x00).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x20, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x01).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x21, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x02).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x22, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x03).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x23, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x04).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x24, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x05).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x25, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x06).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x26, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x07).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x27, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x08).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x28, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x09).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x29, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x0a).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x2A, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x0b).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x2B, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x0c).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x2C, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x0d).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x2D, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x0e).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x2E, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x0f).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x2F, codesegment, address, 0, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x80).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x80, codesegment, address, 3, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x81).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x81, codesegment, address, 3, IdtOmetanjegate)

	address = uint32(ValueOf(ometanjerequesthandler0x82).Pointer())
	isti.OmetanjedescriptorTabelaunosskup(0x82, codesegment, address, 3, IdtOmetanjegate)

	PortPišebyte(PrimarypicNaredbaUIPort, 0x11)
	PortPišebyte(SecondarypicNaredbaUIPort, 0x11)

	PortPišebyte(PrimarypicdataUIPort, 0x20)
	PortPišebyte(SecondarypicdataUIPort, 0x28)

	PortPišebyte(PrimarypicdataUIPort, 0x04)
	PortPišebyte(SecondarypicdataUIPort, 0x02)

	PortPišebyte(PrimarypicdataUIPort, 0x01)
	PortPišebyte(SecondarypicdataUIPort, 0x01)

	PortPišebyte(PrimarypicdataUIPort, 0xF8)
	PortPišebyte(SecondarypicdataUIPort, 0xEF)

	idtPokazivač := [6]uint8{0, 0, 0, 0, 0, 0}
	veličina := (*uint16)(Pointer(&idtPokazivač[0]))
	(*veličina) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtPokazivač[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtPokazivač)))
}
func Lidt(lidtaddr uintptr)

func (isti *TOmetanjemanager) OmetanjedescriptorTabelaunosskup(ometanje int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorVrsta uint8) {

	handleraddressTihobita := (*uint16)(Pointer(&idtdata[ometanje*8+0]))
	(*handleraddressTihobita) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[ometanje*8+2]))
	(*gdtcodesegmentselector) = codesegment

	zauzeto := (*uint8)(Pointer(&idtdata[ometanje*8+4]))
	(*zauzeto) = 0

	var IdtdescriptorPrisutna uint8 = 0x80
	pristupanje := (*uint8)(Pointer(&idtdata[ometanje*8+5]))
	(*pristupanje) = (IdtdescriptorPrisutna | DescriptorVrsta | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressVisokabita := (*uint16)(Pointer(&idtdata[ometanje*8+6]))
	(*handleraddressVisokabita) = uint16((handler >> 16) & 0xFFFF)

}

func (isti *TOmetanjemanager) Skuphandler(handler uintptr, Ometanjebroj uint8) {
	handler_2[Ometanjebroj] = handler
}
func (isti *TOmetanjemanager) Gethandler(Ometanjebroj uint8) uintptr {
	return handler_2[Ometanjebroj]
}
func (isti *TOmetanjemanager) DoRučkaOmetanje(ometanje uint8, esp uint32) uint32 {

	if ometanjeIspravljanje {
		konzola_2.MŠtampajxy("[esp:", 1, 20)
		konzola_2.MUnsignedinteger32Štampaj(uint32(ometanje))
		konzola_2.MŠtampaj(":")
		konzola_2.MUnsignedinteger32Štampaj(esp)
	}
	handlerPokreni := false
	if handler_2[ometanje] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ometanje])))
		esp = myfunction(esp)
		handlerPokreni = true

	}

	if !handlerPokreni && ometanje == uint8(isti.hardverOmetanjeoffset) && isti.zadatakmanager != nil {
		esp = uint32(uintptr(Pointer(isti.zadatakmanager.Schedule((*TcpuStanje)(Pointer(uintptr(esp)))))))

	}
	if !handlerPokreni && ometanje == 0x80 {
		esp = ručkaunhandledsyscall(esp)
	}

	if ometanje <= 0x1F {
	}
	if 0x20 <= ometanje && ometanje < 0x30 {
		if 0x28 <= ometanje {
			PortPišebyte(SecondarypicNaredbaUIPort, 0x20)
		}
		PortPišebyte(PrimarypicNaredbaUIPort, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func skupcr3(address uint32)

var konzola_2 TKonzola = TKonzola{}

func RučkaOmetanje(esp uint32, ometanje uint32) uint32 {

	if ometanjeIspravljanje && ometanje != 0x80 && ometanje != 0x20 {
		konzola_2.MŠtampajxy("[esp:", 1, 21)
		konzola_2.MUnsignedinteger32Štampaj(uint32(ometanje))
		konzola_2.MŠtampaj(":")
		konzola_2.MUnsignedinteger32Štampaj(esp)
	}

	if AktivnaOmetanjemanager != 0 {
		p := (*TOmetanjemanager)(Pointer(AktivnaOmetanjemanager))
		esp = p.DoRučkaOmetanje(uint8(ometanje), esp)
		return esp
	}
	if handler_2[ometanje] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ometanje])))
		esp = myfunction(esp)
	}
	if ometanje == 0x80 {
		return ručkaunhandledsyscall(esp)
	}
	if 0x20 <= ometanje && ometanje < 0x30 {
		if 0x28 <= ometanje {
			PortPišebyte(SecondarypicNaredbaUIPort, 0x20)
		}
		PortPišebyte(PrimarypicNaredbaUIPort, 0x20)
	}

	return esp
}

func ručkaunhandledsyscall(esp uint32) uint32 {
	procesor := (*TcpuStanje)(Pointer(uintptr(esp)))
	if procesor.Eax == 1 || procesor.Eax == 252 {
		procesor.Eip = uint32(ValueOf(ometanjeIzlazloop).Pointer())
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

func exceptionHasGreškacode(ometanje uint32) bool {
	switch ometanje {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNaziv(ometanje uint32) string {
	switch ometanje {
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

func exceptionOkvirVrednost(okvir uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(okvir + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func štampajSTRANAfaultPodaci(greška uint32) {
	MEmergencyDnevnikniska(" pf=[")
	if (greška & 0x01) != 0 {
		MEmergencyDnevnikniska("protection")
	} else {
		MEmergencyDnevnikniska("not-present")
	}
	if (greška & 0x02) != 0 {
		MEmergencyDnevnikniska(",write")
	} else {
		MEmergencyDnevnikniska(",read")
	}
	if (greška & 0x04) != 0 {
		MEmergencyDnevnikniska(",user")
	} else {
		MEmergencyDnevnikniska(",kernel")
	}
	if (greška & 0x08) != 0 {
		MEmergencyDnevnikniska(",reserved-bit")
	}
	if (greška & 0x10) != 0 {
		MEmergencyDnevnikniska(",instruction-fetch")
	}
	MEmergencyDnevnikniska("]")
}

func štampajexceptionselectorPodaci(greška uint32) {
	MEmergencyDnevnikniska(" selector=")
	MEmergencyDnevnikunsignedinteger32(greška & 0xFFFFFFF8)
	MEmergencyDnevnikniska(" index=")
	MEmergencyDnevnikunsignedinteger32(greška >> 3)
	MEmergencyDnevnikniska(" table=")
	if (greška & 0x02) != 0 {
		MEmergencyDnevnikniska("IDT")
	} else if (greška & 0x04) != 0 {
		MEmergencyDnevnikniska("LDT")
	} else {
		MEmergencyDnevnikniska("GDT")
	}
	MEmergencyDnevnikniska(" ext=")
	MEmergencyDnevnikunsignedinteger32(greška & 0x01)
}

func Ručkaexception(esp uint32, ometanje uint32) uint32 {
	MEmergencyDnevnikniska("\nEXCEPTION vec=")
	MEmergencyDnevnikhexadecimal8(uint8(ometanje))
	MEmergencyDnevnikniska(" ")
	MEmergencyDnevnikniska(exceptionNaziv(ometanje))
	MEmergencyDnevnikniska(" frame=")
	MEmergencyDnevnikunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyDnevnikniska(" invalid-frame")
		if exceptionHasGreškacode(ometanje) {
			MEmergencyDnevnikniska(" raw-error-or-bad-esp=")
			MEmergencyDnevnikunsignedinteger32(esp)
			štampajexceptionselectorPodaci(esp)
		}
		MEmergencyDnevnikniska("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var greška uint32 = 0
	var eipoffset uint32 = 0
	if exceptionHasGreškacode(ometanje) {
		greška = exceptionOkvirVrednost(esp, 0)
		eipoffset = 4
	}
	eip := exceptionOkvirVrednost(esp, eipoffset)
	cs := exceptionOkvirVrednost(esp, eipoffset+4)
	eflags := exceptionOkvirVrednost(esp, eipoffset+8)

	MEmergencyDnevnikniska(" err=")
	MEmergencyDnevnikunsignedinteger32(greška)
	MEmergencyDnevnikniska(" eip=")
	MEmergencyDnevnikunsignedinteger32(eip)
	MEmergencyDnevnikniska(" cs=")
	MEmergencyDnevnikunsignedinteger32(cs)
	MEmergencyDnevnikniska(" eflags=")
	MEmergencyDnevnikunsignedinteger32(eflags)
	MEmergencyDnevnikniska(" cr0=")
	MEmergencyDnevnikunsignedinteger32(exceptioncr0())
	MEmergencyDnevnikniska(" cr3=")
	MEmergencyDnevnikunsignedinteger32(exceptioncr3())

	if ometanje == 0x0E {
		MEmergencyDnevnikniska(" cr2=")
		MEmergencyDnevnikunsignedinteger32(exceptioncr2())
		štampajSTRANAfaultPodaci(greška)
	}

	if (cs & 0x03) != 0 {
		MEmergencyDnevnikniska(" useresp=")
		MEmergencyDnevnikunsignedinteger32(exceptionOkvirVrednost(esp, eipoffset+12))
		MEmergencyDnevnikniska(" ss=")
		MEmergencyDnevnikunsignedinteger32(exceptionOkvirVrednost(esp, eipoffset+16))
	}

	if exceptionHasGreškacode(ometanje) {
		štampajexceptionselectorPodaci(greška)
	}
	MEmergencyDnevnikniska("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltPoslefatalexception()

func RučkafatalOmetanjeOkvir(savedesp uint32, ometanje uint32) uint32 {
	Ručkaexception(savedesp+52, ometanje)
	haltPoslefatalexception()
	return savedesp
}

func OmetanjeAktivna()
func (isti *TOmetanjemanager) Aktivna() {
	if AktivnaOmetanjemanager != 0 {
		isti.Deactive()
	}
	address := uintptr(Pointer(isti))
	AktivnaOmetanjemanager = address
	OmetanjeAktivna()
}
func Ometanjedeactive()
func (isti *TOmetanjemanager) Deactive() {
	AktivnaOmetanjemanager = 0
	Ometanjedeactive()
}

func MyRučkaOmetanje(ometanje uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konzola_2 := TKonzola{}
	konzola_2.MŠtampaj(buffer)
	return esp
}
func MyTest(ometanje uint8, esp uint32)

func UnhandleOmetanje() {
	buffer := []byte("unhandle interrupt\n")
	konzola_2 := TKonzola{}
	konzola_2.MŠtampaj(buffer)
}

func ometanjehandler_2(ometanje uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konzola_2 := TKonzola{}
	konzola_2.MŠtampaj(buffer)
	konzola_2.MHexadecimalŠtampaj(0x40)
	return esp
}
func štampajesp(esp uint32) {
	konzola_2 := TKonzola{}
	konzola_2.MUnsignedinteger32Štampajxy(esp, 20, 21)
}
func gettls() uint32
func Štampajtls() {

}
