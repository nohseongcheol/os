package Prekid

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func prekidignore()

func prekidexceptionhandler()
func prekidexceptionhandler0x00()
func prekidexceptionhandler0x01()
func prekidexceptionhandler0x02()
func prekidexceptionhandler0x03()
func prekidexceptionhandler0x04()
func prekidexceptionhandler0x05()
func prekidexceptionhandler0x06()
func prekidexceptionhandler0x07()
func prekidexceptionhandler0x08()
func prekidexceptionhandler0x09()
func prekidexceptionhandler0x0a()
func prekidexceptionhandler0x0b()
func prekidexceptionhandler0x0c()
func prekidexceptionhandler0x0d()
func prekidexceptionhandler0x0e()
func prekidexceptionhandler0x0f()
func prekidexceptionhandler0x10()
func prekidexceptionhandler0x11()
func prekidexceptionhandler0x12()
func prekidexceptionhandler0x13()

func prekidrequesthandler0x00()
func prekidrequesthandler0x01()
func prekidrequesthandler0x02()
func prekidrequesthandler0x03()
func prekidrequesthandler0x04()
func prekidrequesthandler0x05()
func prekidrequesthandler0x06()
func prekidrequesthandler0x07()
func prekidrequesthandler0x08()
func prekidrequesthandler0x09()
func prekidrequesthandler0x0a()
func prekidrequesthandler0x0b()
func prekidrequesthandler0x0c()
func prekidrequesthandler0x0d()
func prekidrequesthandler0x0e()
func prekidrequesthandler0x0f()

func prekidrequesthandler0x80()
func prekidrequesthandler0x81()
func prekidrequesthandler0x82()

func ProvjeriIspis(pozicija uint8, data uint8)
func postavids(dssegment uint32)
func postavigs(gssegment uint32)
func prekidIzađiloop()

type TPrekidhandler struct {
	PrekidBROJ	uint8
	Prekidmanager	uintptr
}
type IPrekidhandler interface {
	RučkaPrekid(uint32) uint32
}

func NoviPrekidhandler(Prekidmanager uintptr, PrekidBROJ uint8) *TPrekidhandler {
	prekidhandler_2 := new(TPrekidhandler)
	prekidhandler_2.PrekidBROJ = PrekidBROJ
	prekidhandler_2.Prekidmanager = Prekidmanager
	return prekidhandler_2

}

var handler_2 [256]uintptr

func (sam *TPrekidhandler) Init(PrekidBROJ uint8, Prekidmanager uintptr, funcaddress uintptr) {

	handler_2[PrekidBROJ] = funcaddress

	sam.PrekidBROJ = PrekidBROJ
	sam.Prekidmanager = Prekidmanager

}
func (sam *TPrekidhandler) PostaviRučkaPrekidfuction(PrekidBROJ uint32, address uintptr) {
	handler_2[PrekidBROJ] = address
}
func (sam *TPrekidhandler) Uništi() {
	samuintptr := uintptr(Pointer(sam))
	Prekidmanager := (*TPrekidmanager)(Pointer(sam.Prekidmanager))
	if samuintptr == Prekidmanager.Gethandler(sam.PrekidBROJ) {
		Prekidmanager.Postavihandler(0, sam.PrekidBROJ)
	}

}
func (sam *TPrekidhandler) PostaviPrekidmanager(Prekidmanager uintptr) {
}
func (sam *TPrekidhandler) PostaviPrekidBROJ(PrekidBROJ uint8) {
	sam.PrekidBROJ = PrekidBROJ
}
func (sam *TPrekidhandler) RučkaPrekid(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MIspis(buffer)
	return esp
}
func RučkaPrekid1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MIspis(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TPrekiddescriptorTablicaPokazivač struct {
}

var idtdata [256 * 8]uint8
var AktivanPrekidmanager uintptr = 0

const prekiddebug = false

type TPrekidmanager struct {
	handler_2	[256]uintptr

	sklopovljePrekidoffset	uint16

	zadatakmanager	*TZadatakmanager
}

var PrimarypicNaredbaioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicNaredbaioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (sam *TPrekidmanager) Init(sklopovljePrekidoffset uint16, općidescriptorTablica *TShareddescriptorTablica, zadatakmanager *TZadatakmanager) {

	sam.zadatakmanager = zadatakmanager

	sam.sklopovljePrekidoffset = sklopovljePrekidoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtPrekidgate uint8 = 0xE
	address = uint32(ValueOf(prekidignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(prekidexceptionhandler0x0f).Pointer())
		sam.PrekiddescriptorTablicaentryPostavi(i, codesegment, address, 0, IdtPrekidgate)
	}

	address = uint32(ValueOf(prekidexceptionhandler0x00).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x00, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x01).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x01, codesegment, address, 0, IdtPrekidgate)
	address = uint32(ValueOf(prekidexceptionhandler0x02).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x02, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x03).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x03, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x04).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x04, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x05).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x05, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x06).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x06, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x07).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x07, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x08).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x08, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x09).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x09, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x0a).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x0A, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x0b).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x0B, codesegment, address, 0, IdtPrekidgate)
	address = uint32(ValueOf(prekidexceptionhandler0x0c).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x0C, codesegment, address, 0, IdtPrekidgate)
	address = uint32(ValueOf(prekidexceptionhandler0x0d).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x0D, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x0e).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x0E, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x0f).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x0F, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x10).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x10, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x11).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x11, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x12).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x12, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidexceptionhandler0x13).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x13, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x00).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x20, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x01).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x21, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x02).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x22, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x03).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x23, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x04).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x24, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x05).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x25, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x06).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x26, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x07).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x27, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x08).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x28, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x09).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x29, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x0a).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x2A, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x0b).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x2B, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x0c).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x2C, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x0d).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x2D, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x0e).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x2E, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x0f).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x2F, codesegment, address, 0, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x80).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x80, codesegment, address, 3, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x81).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x81, codesegment, address, 3, IdtPrekidgate)

	address = uint32(ValueOf(prekidrequesthandler0x82).Pointer())
	sam.PrekiddescriptorTablicaentryPostavi(0x82, codesegment, address, 3, IdtPrekidgate)

	PortZapišibyte(PrimarypicNaredbaioport, 0x11)
	PortZapišibyte(SecondarypicNaredbaioport, 0x11)

	PortZapišibyte(Primarypicdataioport, 0x20)
	PortZapišibyte(Secondarypicdataioport, 0x28)

	PortZapišibyte(Primarypicdataioport, 0x04)
	PortZapišibyte(Secondarypicdataioport, 0x02)

	PortZapišibyte(Primarypicdataioport, 0x01)
	PortZapišibyte(Secondarypicdataioport, 0x01)

	PortZapišibyte(Primarypicdataioport, 0xF8)
	PortZapišibyte(Secondarypicdataioport, 0xEF)

	idtPokazivač := [6]uint8{0, 0, 0, 0, 0, 0}
	veličina := (*uint16)(Pointer(&idtPokazivač[0]))
	(*veličina) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtPokazivač[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtPokazivač)))
}
func Lidt(lidtaddr uintptr)

func (sam *TPrekidmanager) PrekiddescriptorTablicaentryPostavi(prekid int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorVrsta uint8) {

	handleraddressNIskobits := (*uint16)(Pointer(&idtdata[prekid*8+0]))
	(*handleraddressNIskobits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[prekid*8+2]))
	(*gdtcodesegmentselector) = codesegment

	rezervirano := (*uint8)(Pointer(&idtdata[prekid*8+4]))
	(*rezervirano) = 0

	var IdtdescriptorPrisutno uint8 = 0x80
	pristup := (*uint8)(Pointer(&idtdata[prekid*8+5]))
	(*pristup) = (IdtdescriptorPrisutno | DescriptorVrsta | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressVisokobits := (*uint16)(Pointer(&idtdata[prekid*8+6]))
	(*handleraddressVisokobits) = uint16((handler >> 16) & 0xFFFF)

}

func (sam *TPrekidmanager) Postavihandler(handler uintptr, PrekidBROJ uint8) {
	handler_2[PrekidBROJ] = handler
}
func (sam *TPrekidmanager) Gethandler(PrekidBROJ uint8) uintptr {
	return handler_2[PrekidBROJ]
}
func (sam *TPrekidmanager) DoRučkaPrekid(prekid uint8, esp uint32) uint32 {

	if prekiddebug {
		console_2.MIspisxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Ispis(uint32(prekid))
		console_2.MIspis(":")
		console_2.MUnsignedinteger32Ispis(esp)
	}
	handlerPokreni := false
	if handler_2[prekid] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[prekid])))
		esp = myfunction(esp)
		handlerPokreni = true

	}

	if !handlerPokreni && prekid == uint8(sam.sklopovljePrekidoffset) && sam.zadatakmanager != nil {
		esp = uint32(uintptr(Pointer(sam.zadatakmanager.Schedule((*TcpuStanje)(Pointer(uintptr(esp)))))))

	}
	if !handlerPokreni && prekid == 0x80 {
		esp = ručkaunhandledsyscall(esp)
	}

	if prekid <= 0x1F {
	}
	if 0x20 <= prekid && prekid < 0x30 {
		if 0x28 <= prekid {
			PortZapišibyte(SecondarypicNaredbaioport, 0x20)
		}
		PortZapišibyte(PrimarypicNaredbaioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func postavicr3(address uint32)

var console_2 TConsole = TConsole{}

func RučkaPrekid(esp uint32, prekid uint32) uint32 {

	if prekiddebug && prekid != 0x80 && prekid != 0x20 {
		console_2.MIspisxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Ispis(uint32(prekid))
		console_2.MIspis(":")
		console_2.MUnsignedinteger32Ispis(esp)
	}

	if AktivanPrekidmanager != 0 {
		p := (*TPrekidmanager)(Pointer(AktivanPrekidmanager))
		esp = p.DoRučkaPrekid(uint8(prekid), esp)
		return esp
	}
	if handler_2[prekid] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[prekid])))
		esp = myfunction(esp)
	}
	if prekid == 0x80 {
		return ručkaunhandledsyscall(esp)
	}
	if 0x20 <= prekid && prekid < 0x30 {
		if 0x28 <= prekid {
			PortZapišibyte(SecondarypicNaredbaioport, 0x20)
		}
		PortZapišibyte(PrimarypicNaredbaioport, 0x20)
	}

	return esp
}

func ručkaunhandledsyscall(esp uint32) uint32 {
	procesor := (*TcpuStanje)(Pointer(uintptr(esp)))
	if procesor.Eax == 1 || procesor.Eax == 252 {
		procesor.Eip = uint32(ValueOf(prekidIzađiloop).Pointer())
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

func exceptionhasGreškacode(prekid uint32) bool {
	switch prekid {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionIme(prekid uint32) string {
	switch prekid {
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

func exceptionframeVrijednost(frame uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(frame + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func ispisStranicafaultInformacije(greška uint32) {
	MEmergencyZapisujZnakovniniz(" pf=[")
	if (greška & 0x01) != 0 {
		MEmergencyZapisujZnakovniniz("protection")
	} else {
		MEmergencyZapisujZnakovniniz("not-present")
	}
	if (greška & 0x02) != 0 {
		MEmergencyZapisujZnakovniniz(",write")
	} else {
		MEmergencyZapisujZnakovniniz(",read")
	}
	if (greška & 0x04) != 0 {
		MEmergencyZapisujZnakovniniz(",user")
	} else {
		MEmergencyZapisujZnakovniniz(",kernel")
	}
	if (greška & 0x08) != 0 {
		MEmergencyZapisujZnakovniniz(",reserved-bit")
	}
	if (greška & 0x10) != 0 {
		MEmergencyZapisujZnakovniniz(",instruction-fetch")
	}
	MEmergencyZapisujZnakovniniz("]")
}

func ispisexceptionselectorInformacije(greška uint32) {
	MEmergencyZapisujZnakovniniz(" selector=")
	MEmergencyZapisujunsignedinteger32(greška & 0xFFFFFFF8)
	MEmergencyZapisujZnakovniniz(" index=")
	MEmergencyZapisujunsignedinteger32(greška >> 3)
	MEmergencyZapisujZnakovniniz(" table=")
	if (greška & 0x02) != 0 {
		MEmergencyZapisujZnakovniniz("IDT")
	} else if (greška & 0x04) != 0 {
		MEmergencyZapisujZnakovniniz("LDT")
	} else {
		MEmergencyZapisujZnakovniniz("GDT")
	}
	MEmergencyZapisujZnakovniniz(" ext=")
	MEmergencyZapisujunsignedinteger32(greška & 0x01)
}

func Ručkaexception(esp uint32, prekid uint32) uint32 {
	MEmergencyZapisujZnakovniniz("\nEXCEPTION vec=")
	MEmergencyZapisujhexadecimal8(uint8(prekid))
	MEmergencyZapisujZnakovniniz(" ")
	MEmergencyZapisujZnakovniniz(exceptionIme(prekid))
	MEmergencyZapisujZnakovniniz(" frame=")
	MEmergencyZapisujunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyZapisujZnakovniniz(" invalid-frame")
		if exceptionhasGreškacode(prekid) {
			MEmergencyZapisujZnakovniniz(" raw-error-or-bad-esp=")
			MEmergencyZapisujunsignedinteger32(esp)
			ispisexceptionselectorInformacije(esp)
		}
		MEmergencyZapisujZnakovniniz("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var greška uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasGreškacode(prekid) {
		greška = exceptionframeVrijednost(esp, 0)
		eipoffset = 4
	}
	eip := exceptionframeVrijednost(esp, eipoffset)
	cs := exceptionframeVrijednost(esp, eipoffset+4)
	eflags := exceptionframeVrijednost(esp, eipoffset+8)

	MEmergencyZapisujZnakovniniz(" err=")
	MEmergencyZapisujunsignedinteger32(greška)
	MEmergencyZapisujZnakovniniz(" eip=")
	MEmergencyZapisujunsignedinteger32(eip)
	MEmergencyZapisujZnakovniniz(" cs=")
	MEmergencyZapisujunsignedinteger32(cs)
	MEmergencyZapisujZnakovniniz(" eflags=")
	MEmergencyZapisujunsignedinteger32(eflags)
	MEmergencyZapisujZnakovniniz(" cr0=")
	MEmergencyZapisujunsignedinteger32(exceptioncr0())
	MEmergencyZapisujZnakovniniz(" cr3=")
	MEmergencyZapisujunsignedinteger32(exceptioncr3())

	if prekid == 0x0E {
		MEmergencyZapisujZnakovniniz(" cr2=")
		MEmergencyZapisujunsignedinteger32(exceptioncr2())
		ispisStranicafaultInformacije(greška)
	}

	if (cs & 0x03) != 0 {
		MEmergencyZapisujZnakovniniz(" useresp=")
		MEmergencyZapisujunsignedinteger32(exceptionframeVrijednost(esp, eipoffset+12))
		MEmergencyZapisujZnakovniniz(" ss=")
		MEmergencyZapisujunsignedinteger32(exceptionframeVrijednost(esp, eipoffset+16))
	}

	if exceptionhasGreškacode(prekid) {
		ispisexceptionselectorInformacije(greška)
	}
	MEmergencyZapisujZnakovniniz("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltPoslijefatalexception()

func RučkafatalPrekidframe(savedesp uint32, prekid uint32) uint32 {
	Ručkaexception(savedesp+52, prekid)
	haltPoslijefatalexception()
	return savedesp
}

func PrekidAktivan()
func (sam *TPrekidmanager) Aktivan() {
	if AktivanPrekidmanager != 0 {
		sam.Deactive()
	}
	address := uintptr(Pointer(sam))
	AktivanPrekidmanager = address
	PrekidAktivan()
}
func Prekiddeactive()
func (sam *TPrekidmanager) Deactive() {
	AktivanPrekidmanager = 0
	Prekiddeactive()
}

func MyRučkaPrekid(prekid uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MIspis(buffer)
	return esp
}
func MyProvjeri(prekid uint8, esp uint32)

func UnhandlePrekid() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MIspis(buffer)
}

func prekidhandler_2(prekid uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MIspis(buffer)
	console_2.MHexadecimalIspis(0x40)
	return esp
}
func ispisesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Ispisxy(esp, 20, 21)
}
func gettls() uint32
func Ispistls() {

}
