/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Prekinitev

import . "unsafe"
import . "reflect"

import . "vrata"
import . "gdt"
import . "multitasking"
import . "console"

func prekinitevignore()

func prekinitevexceptionhandler()
func prekinitevexceptionhandler0x00()
func prekinitevexceptionhandler0x01()
func prekinitevexceptionhandler0x02()
func prekinitevexceptionhandler0x03()
func prekinitevexceptionhandler0x04()
func prekinitevexceptionhandler0x05()
func prekinitevexceptionhandler0x06()
func prekinitevexceptionhandler0x07()
func prekinitevexceptionhandler0x08()
func prekinitevexceptionhandler0x09()
func prekinitevexceptionhandler0x0a()
func prekinitevexceptionhandler0x0b()
func prekinitevexceptionhandler0x0c()
func prekinitevexceptionhandler0x0d()
func prekinitevexceptionhandler0x0e()
func prekinitevexceptionhandler0x0f()
func prekinitevexceptionhandler0x10()
func prekinitevexceptionhandler0x11()
func prekinitevexceptionhandler0x12()
func prekinitevexceptionhandler0x13()

func prekinitevrequesthandler0x00()
func prekinitevrequesthandler0x01()
func prekinitevrequesthandler0x02()
func prekinitevrequesthandler0x03()
func prekinitevrequesthandler0x04()
func prekinitevrequesthandler0x05()
func prekinitevrequesthandler0x06()
func prekinitevrequesthandler0x07()
func prekinitevrequesthandler0x08()
func prekinitevrequesthandler0x09()
func prekinitevrequesthandler0x0a()
func prekinitevrequesthandler0x0b()
func prekinitevrequesthandler0x0c()
func prekinitevrequesthandler0x0d()
func prekinitevrequesthandler0x0e()
func prekinitevrequesthandler0x0f()

func prekinitevrequesthandler0x80()
func prekinitevrequesthandler0x81()
func prekinitevrequesthandler0x82()

func PreizkusNatisni(položaj uint8, data uint8)
func množicads(dssegment uint32)
func množicags(gssegment uint32)
func prekinitevIzhodloop()

type TPrekinitevhandler struct {
	PrekinitevŠtevilka	uint8
	Prekinitevmanager	uintptr
}
type IPrekinitevhandler interface {
	RočicaPrekinitev(uint32) uint32
}

func NovaPrekinitevhandler(Prekinitevmanager uintptr, PrekinitevŠtevilka uint8) *TPrekinitevhandler {
	prekinitevhandler_2 := new(TPrekinitevhandler)
	prekinitevhandler_2.PrekinitevŠtevilka = PrekinitevŠtevilka
	prekinitevhandler_2.Prekinitevmanager = Prekinitevmanager
	return prekinitevhandler_2

}

var handler_2 [256]uintptr

func (sam *TPrekinitevhandler) Init(PrekinitevŠtevilka uint8, Prekinitevmanager uintptr, funcaddress uintptr) {

	handler_2[PrekinitevŠtevilka] = funcaddress

	sam.PrekinitevŠtevilka = PrekinitevŠtevilka
	sam.Prekinitevmanager = Prekinitevmanager

}
func (sam *TPrekinitevhandler) MnožicaRočicaPrekinitevfuction(PrekinitevŠtevilka uint32, address uintptr) {
	handler_2[PrekinitevŠtevilka] = address
}
func (sam *TPrekinitevhandler) Uniči() {
	samuintptr := uintptr(Pointer(sam))
	Prekinitevmanager := (*TPrekinitevmanager)(Pointer(sam.Prekinitevmanager))
	if samuintptr == Prekinitevmanager.Gethandler(sam.PrekinitevŠtevilka) {
		Prekinitevmanager.Množicahandler(0, sam.PrekinitevŠtevilka)
	}

}
func (sam *TPrekinitevhandler) MnožicaPrekinitevmanager(Prekinitevmanager uintptr) {
}
func (sam *TPrekinitevhandler) MnožicaPrekinitevŠtevilka(PrekinitevŠtevilka uint8) {
	sam.PrekinitevŠtevilka = PrekinitevŠtevilka
}
func (sam *TPrekinitevhandler) RočicaPrekinitev(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MNatisni(buffer)
	return esp
}
func RočicaPrekinitev1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MNatisni(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TPrekinitevdescriptorPreglednicaKazalnik struct {
}

var idtdata [256 * 8]uint8
var DejavenPrekinitevmanager uintptr = 0

const prekinitevRazhrošči = false

type TPrekinitevmanager struct {
	handler_2	[256]uintptr

	strojnaopremaPrekinitevoffset	uint16

	nalogamanager	*TNalogamanager
}

var PrimarypicUkazVIVrata uint16 = 0x20
var PrimarypicdataVIVrata uint16 = 0x21
var SecondarypicUkazVIVrata uint16 = 0xA0
var SecondarypicdataVIVrata uint16 = 0xA1

func (sam *TPrekinitevmanager) Init(strojnaopremaPrekinitevoffset uint16, splošnodescriptorPreglednica *TShareddescriptorPreglednica, nalogamanager *TNalogamanager) {

	sam.nalogamanager = nalogamanager

	sam.strojnaopremaPrekinitevoffset = strojnaopremaPrekinitevoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtPrekinitevgate uint8 = 0xE
	address = uint32(ValueOf(prekinitevignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(prekinitevexceptionhandler0x0f).Pointer())
		sam.PrekinitevdescriptorPreglednicavnosmnožica(i, codesegment, address, 0, IdtPrekinitevgate)
	}

	address = uint32(ValueOf(prekinitevexceptionhandler0x00).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x00, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x01).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x01, codesegment, address, 0, IdtPrekinitevgate)
	address = uint32(ValueOf(prekinitevexceptionhandler0x02).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x02, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x03).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x03, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x04).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x04, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x05).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x05, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x06).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x06, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x07).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x07, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x08).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x08, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x09).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x09, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x0a).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x0A, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x0b).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x0B, codesegment, address, 0, IdtPrekinitevgate)
	address = uint32(ValueOf(prekinitevexceptionhandler0x0c).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x0C, codesegment, address, 0, IdtPrekinitevgate)
	address = uint32(ValueOf(prekinitevexceptionhandler0x0d).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x0D, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x0e).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x0E, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x0f).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x0F, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x10).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x10, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x11).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x11, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x12).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x12, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevexceptionhandler0x13).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x13, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x00).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x20, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x01).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x21, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x02).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x22, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x03).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x23, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x04).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x24, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x05).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x25, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x06).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x26, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x07).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x27, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x08).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x28, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x09).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x29, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x0a).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x2A, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x0b).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x2B, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x0c).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x2C, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x0d).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x2D, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x0e).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x2E, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x0f).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x2F, codesegment, address, 0, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x80).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x80, codesegment, address, 3, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x81).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x81, codesegment, address, 3, IdtPrekinitevgate)

	address = uint32(ValueOf(prekinitevrequesthandler0x82).Pointer())
	sam.PrekinitevdescriptorPreglednicavnosmnožica(0x82, codesegment, address, 3, IdtPrekinitevgate)

	VrataPisanjebyte(PrimarypicUkazVIVrata, 0x11)
	VrataPisanjebyte(SecondarypicUkazVIVrata, 0x11)

	VrataPisanjebyte(PrimarypicdataVIVrata, 0x20)
	VrataPisanjebyte(SecondarypicdataVIVrata, 0x28)

	VrataPisanjebyte(PrimarypicdataVIVrata, 0x04)
	VrataPisanjebyte(SecondarypicdataVIVrata, 0x02)

	VrataPisanjebyte(PrimarypicdataVIVrata, 0x01)
	VrataPisanjebyte(SecondarypicdataVIVrata, 0x01)

	VrataPisanjebyte(PrimarypicdataVIVrata, 0xF8)
	VrataPisanjebyte(SecondarypicdataVIVrata, 0xEF)

	idtKazalnik := [6]uint8{0, 0, 0, 0, 0, 0}
	velikost := (*uint16)(Pointer(&idtKazalnik[0]))
	(*velikost) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtKazalnik[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtKazalnik)))
}
func Lidt(lidtaddr uintptr)

func (sam *TPrekinitevmanager) PrekinitevdescriptorPreglednicavnosmnožica(prekinitev int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorVrsta uint8) {

	handleraddressNizkobiti := (*uint16)(Pointer(&idtdata[prekinitev*8+0]))
	(*handleraddressNizkobiti) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[prekinitev*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[prekinitev*8+4]))
	(*reserved) = 0

	var IdtdescriptorPrisotnost uint8 = 0x80
	dostop := (*uint8)(Pointer(&idtdata[prekinitev*8+5]))
	(*dostop) = (IdtdescriptorPrisotnost | DescriptorVrsta | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressVisokobiti := (*uint16)(Pointer(&idtdata[prekinitev*8+6]))
	(*handleraddressVisokobiti) = uint16((handler >> 16) & 0xFFFF)

}

func (sam *TPrekinitevmanager) Množicahandler(handler uintptr, PrekinitevŠtevilka uint8) {
	handler_2[PrekinitevŠtevilka] = handler
}
func (sam *TPrekinitevmanager) Gethandler(PrekinitevŠtevilka uint8) uintptr {
	return handler_2[PrekinitevŠtevilka]
}
func (sam *TPrekinitevmanager) DoRočicaPrekinitev(prekinitev uint8, esp uint32) uint32 {

	if prekinitevRazhrošči {
		console_2.MNatisnixy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Natisni(uint32(prekinitev))
		console_2.MNatisni(":")
		console_2.MUnsignedinteger32Natisni(esp)
	}
	handlerZaženi := false
	if handler_2[prekinitev] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[prekinitev])))
		esp = myfunction(esp)
		handlerZaženi = true

	}

	if !handlerZaženi && prekinitev == uint8(sam.strojnaopremaPrekinitevoffset) && sam.nalogamanager != nil {
		esp = uint32(uintptr(Pointer(sam.nalogamanager.Schedule((*TcpuStanje)(Pointer(uintptr(esp)))))))

	}
	if !handlerZaženi && prekinitev == 0x80 {
		esp = ročicaunhandledsyscall(esp)
	}

	if prekinitev <= 0x1F {
	}
	if 0x20 <= prekinitev && prekinitev < 0x30 {
		if 0x28 <= prekinitev {
			VrataPisanjebyte(SecondarypicUkazVIVrata, 0x20)
		}
		VrataPisanjebyte(PrimarypicUkazVIVrata, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func množicacr3(address uint32)

var console_2 TConsole = TConsole{}

func RočicaPrekinitev(esp uint32, prekinitev uint32) uint32 {

	if prekinitevRazhrošči && prekinitev != 0x80 && prekinitev != 0x20 {
		console_2.MNatisnixy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Natisni(uint32(prekinitev))
		console_2.MNatisni(":")
		console_2.MUnsignedinteger32Natisni(esp)
	}

	if DejavenPrekinitevmanager != 0 {
		p := (*TPrekinitevmanager)(Pointer(DejavenPrekinitevmanager))
		esp = p.DoRočicaPrekinitev(uint8(prekinitev), esp)
		return esp
	}
	if handler_2[prekinitev] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[prekinitev])))
		esp = myfunction(esp)
	}
	if prekinitev == 0x80 {
		return ročicaunhandledsyscall(esp)
	}
	if 0x20 <= prekinitev && prekinitev < 0x30 {
		if 0x28 <= prekinitev {
			VrataPisanjebyte(SecondarypicUkazVIVrata, 0x20)
		}
		VrataPisanjebyte(PrimarypicUkazVIVrata, 0x20)
	}

	return esp
}

func ročicaunhandledsyscall(esp uint32) uint32 {
	cPE := (*TcpuStanje)(Pointer(uintptr(esp)))
	if cPE.Eax == 1 || cPE.Eax == 252 {
		cPE.Eip = uint32(ValueOf(prekinitevIzhodloop).Pointer())
		cPE.Cs = Segkernelcode
		cPE.Ds = Segkerneldata
		cPE.Es = Segkerneldata
		cPE.Fs = Segkerneldata
		cPE.Gs = Segkernelgs
		cPE.Ss = Segkerneldata
		cPE.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasNapakacode(prekinitev uint32) bool {
	switch prekinitev {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionIme(prekinitev uint32) string {
	switch prekinitev {
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

func natisniStranfaultPodatki(napaka uint32) {
	MEmergencylogNiz(" pf=[")
	if (napaka & 0x01) != 0 {
		MEmergencylogNiz("protection")
	} else {
		MEmergencylogNiz("not-present")
	}
	if (napaka & 0x02) != 0 {
		MEmergencylogNiz(",write")
	} else {
		MEmergencylogNiz(",read")
	}
	if (napaka & 0x04) != 0 {
		MEmergencylogNiz(",user")
	} else {
		MEmergencylogNiz(",kernel")
	}
	if (napaka & 0x08) != 0 {
		MEmergencylogNiz(",reserved-bit")
	}
	if (napaka & 0x10) != 0 {
		MEmergencylogNiz(",instruction-fetch")
	}
	MEmergencylogNiz("]")
}

func natisniexceptionselectorPodatki(napaka uint32) {
	MEmergencylogNiz(" selector=")
	MEmergencylogunsignedinteger32(napaka & 0xFFFFFFF8)
	MEmergencylogNiz(" index=")
	MEmergencylogunsignedinteger32(napaka >> 3)
	MEmergencylogNiz(" table=")
	if (napaka & 0x02) != 0 {
		MEmergencylogNiz("IDT")
	} else if (napaka & 0x04) != 0 {
		MEmergencylogNiz("LDT")
	} else {
		MEmergencylogNiz("GDT")
	}
	MEmergencylogNiz(" ext=")
	MEmergencylogunsignedinteger32(napaka & 0x01)
}

func Ročicaexception(esp uint32, prekinitev uint32) uint32 {
	MEmergencylogNiz("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(prekinitev))
	MEmergencylogNiz(" ")
	MEmergencylogNiz(exceptionIme(prekinitev))
	MEmergencylogNiz(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogNiz(" invalid-frame")
		if exceptionhasNapakacode(prekinitev) {
			MEmergencylogNiz(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			natisniexceptionselectorPodatki(esp)
		}
		MEmergencylogNiz("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var napaka uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasNapakacode(prekinitev) {
		napaka = exceptionOkvirVrednost(esp, 0)
		eipoffset = 4
	}
	eip := exceptionOkvirVrednost(esp, eipoffset)
	cs := exceptionOkvirVrednost(esp, eipoffset+4)
	eflags := exceptionOkvirVrednost(esp, eipoffset+8)

	MEmergencylogNiz(" err=")
	MEmergencylogunsignedinteger32(napaka)
	MEmergencylogNiz(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogNiz(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogNiz(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogNiz(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogNiz(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if prekinitev == 0x0E {
		MEmergencylogNiz(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		natisniStranfaultPodatki(napaka)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogNiz(" useresp=")
		MEmergencylogunsignedinteger32(exceptionOkvirVrednost(esp, eipoffset+12))
		MEmergencylogNiz(" ss=")
		MEmergencylogunsignedinteger32(exceptionOkvirVrednost(esp, eipoffset+16))
	}

	if exceptionhasNapakacode(prekinitev) {
		natisniexceptionselectorPodatki(napaka)
	}
	MEmergencylogNiz("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func RočicafatalPrekinitevOkvir(savedesp uint32, prekinitev uint32) uint32 {
	Ročicaexception(savedesp+52, prekinitev)
	haltafterfatalexception()
	return savedesp
}

func PrekinitevDejaven()
func (sam *TPrekinitevmanager) Dejaven() {
	if DejavenPrekinitevmanager != 0 {
		sam.Deactive()
	}
	address := uintptr(Pointer(sam))
	DejavenPrekinitevmanager = address
	PrekinitevDejaven()
}
func Prekinitevdeactive()
func (sam *TPrekinitevmanager) Deactive() {
	DejavenPrekinitevmanager = 0
	Prekinitevdeactive()
}

func MyRočicaPrekinitev(prekinitev uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MNatisni(buffer)
	return esp
}
func MyPreizkus(prekinitev uint8, esp uint32)

func UnhandlePrekinitev() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MNatisni(buffer)
}

func prekinitevhandler_2(prekinitev uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MNatisni(buffer)
	console_2.MHexadecimalNatisni(0x40)
	return esp
}
func natisniesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Natisnixy(esp, 20, 21)
}
func gettls() uint32
func Natisnitls() {

}
