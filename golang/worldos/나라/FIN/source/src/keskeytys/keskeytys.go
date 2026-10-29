/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Keskeytys

import . "unsafe"
import . "reflect"

import . "portti"
import . "gdt"
import . "multitasking"
import . "konsoli"

func keskeytysignore()

func keskeytysexceptionhandler()
func keskeytysexceptionhandler0x00()
func keskeytysexceptionhandler0x01()
func keskeytysexceptionhandler0x02()
func keskeytysexceptionhandler0x03()
func keskeytysexceptionhandler0x04()
func keskeytysexceptionhandler0x05()
func keskeytysexceptionhandler0x06()
func keskeytysexceptionhandler0x07()
func keskeytysexceptionhandler0x08()
func keskeytysexceptionhandler0x09()
func keskeytysexceptionhandler0x0a()
func keskeytysexceptionhandler0x0b()
func keskeytysexceptionhandler0x0c()
func keskeytysexceptionhandler0x0d()
func keskeytysexceptionhandler0x0e()
func keskeytysexceptionhandler0x0f()
func keskeytysexceptionhandler0x10()
func keskeytysexceptionhandler0x11()
func keskeytysexceptionhandler0x12()
func keskeytysexceptionhandler0x13()

func keskeytysrequesthandler0x00()
func keskeytysrequesthandler0x01()
func keskeytysrequesthandler0x02()
func keskeytysrequesthandler0x03()
func keskeytysrequesthandler0x04()
func keskeytysrequesthandler0x05()
func keskeytysrequesthandler0x06()
func keskeytysrequesthandler0x07()
func keskeytysrequesthandler0x08()
func keskeytysrequesthandler0x09()
func keskeytysrequesthandler0x0a()
func keskeytysrequesthandler0x0b()
func keskeytysrequesthandler0x0c()
func keskeytysrequesthandler0x0d()
func keskeytysrequesthandler0x0e()
func keskeytysrequesthandler0x0f()

func keskeytysrequesthandler0x80()
func keskeytysrequesthandler0x81()
func keskeytysrequesthandler0x82()

func KokeileTulosta(sijainti uint8, data uint8)
func asetads(dssegment uint32)
func asetags(gssegment uint32)
func keskeytysSuljeloop()

type TKeskeytyshandler struct {
	KeskeytysNumero		uint8
	Keskeytysmanager	uintptr
}
type IKeskeytyshandler interface {
	KahvaKeskeytys(uint32) uint32
}

func UusiKeskeytyshandler(Keskeytysmanager uintptr, KeskeytysNumero uint8) *TKeskeytyshandler {
	keskeytyshandler_2 := new(TKeskeytyshandler)
	keskeytyshandler_2.KeskeytysNumero = KeskeytysNumero
	keskeytyshandler_2.Keskeytysmanager = Keskeytysmanager
	return keskeytyshandler_2

}

var handler_2 [256]uintptr

func (itse *TKeskeytyshandler) Init(KeskeytysNumero uint8, Keskeytysmanager uintptr, funcaddress uintptr) {

	handler_2[KeskeytysNumero] = funcaddress

	itse.KeskeytysNumero = KeskeytysNumero
	itse.Keskeytysmanager = Keskeytysmanager

}
func (itse *TKeskeytyshandler) AsetaKahvaKeskeytysfuction(KeskeytysNumero uint32, address uintptr) {
	handler_2[KeskeytysNumero] = address
}
func (itse *TKeskeytyshandler) Tuhoa() {
	itseuintptr := uintptr(Pointer(itse))
	Keskeytysmanager := (*TKeskeytysmanager)(Pointer(itse.Keskeytysmanager))
	if itseuintptr == Keskeytysmanager.Gethandler(itse.KeskeytysNumero) {
		Keskeytysmanager.Asetahandler(0, itse.KeskeytysNumero)
	}

}
func (itse *TKeskeytyshandler) AsetaKeskeytysmanager(Keskeytysmanager uintptr) {
}
func (itse *TKeskeytyshandler) AsetaKeskeytysNumero(KeskeytysNumero uint8) {
	itse.KeskeytysNumero = KeskeytysNumero
}
func (itse *TKeskeytyshandler) KahvaKeskeytys(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konsoli_2 := TKonsoli{}
	konsoli_2.MTulosta(buffer)
	return esp
}
func KahvaKeskeytys1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konsoli_2 := TKonsoli{}
	konsoli_2.MTulosta(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TKeskeytysdescriptorTaulukkoOsoitin struct {
}

var idtdata [256 * 8]uint8
var AktiivinenKeskeytysmanager uintptr = 0

const keskeytysVirheenpaikannus = false

type TKeskeytysmanager struct {
	handler_2	[256]uintptr

	laitteistoKeskeytysoffset	uint16

	tehtävämanager	*TTehtävämanager
}

var PrimarypicKomentoSiirräntäPortti uint16 = 0x20
var PrimarypicdataSiirräntäPortti uint16 = 0x21
var SecondarypicKomentoSiirräntäPortti uint16 = 0xA0
var SecondarypicdataSiirräntäPortti uint16 = 0xA1

func (itse *TKeskeytysmanager) Init(laitteistoKeskeytysoffset uint16, globaalissadescriptorTaulukko *TShareddescriptorTaulukko, tehtävämanager *TTehtävämanager) {

	itse.tehtävämanager = tehtävämanager

	itse.laitteistoKeskeytysoffset = laitteistoKeskeytysoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtKeskeytysgate uint8 = 0xE
	address = uint32(ValueOf(keskeytysignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(keskeytysexceptionhandler0x0f).Pointer())
		itse.KeskeytysdescriptorTaulukkohakusanaaseta(i, codesegment, address, 0, IdtKeskeytysgate)
	}

	address = uint32(ValueOf(keskeytysexceptionhandler0x00).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x00, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x01).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x01, codesegment, address, 0, IdtKeskeytysgate)
	address = uint32(ValueOf(keskeytysexceptionhandler0x02).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x02, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x03).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x03, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x04).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x04, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x05).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x05, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x06).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x06, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x07).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x07, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x08).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x08, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x09).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x09, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x0a).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x0A, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x0b).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x0B, codesegment, address, 0, IdtKeskeytysgate)
	address = uint32(ValueOf(keskeytysexceptionhandler0x0c).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x0C, codesegment, address, 0, IdtKeskeytysgate)
	address = uint32(ValueOf(keskeytysexceptionhandler0x0d).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x0D, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x0e).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x0E, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x0f).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x0F, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x10).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x10, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x11).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x11, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x12).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x12, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysexceptionhandler0x13).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x13, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x00).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x20, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x01).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x21, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x02).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x22, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x03).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x23, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x04).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x24, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x05).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x25, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x06).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x26, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x07).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x27, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x08).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x28, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x09).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x29, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x0a).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x2A, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x0b).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x2B, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x0c).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x2C, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x0d).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x2D, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x0e).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x2E, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x0f).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x2F, codesegment, address, 0, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x80).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x80, codesegment, address, 3, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x81).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x81, codesegment, address, 3, IdtKeskeytysgate)

	address = uint32(ValueOf(keskeytysrequesthandler0x82).Pointer())
	itse.KeskeytysdescriptorTaulukkohakusanaaseta(0x82, codesegment, address, 3, IdtKeskeytysgate)

	PorttiKirjoitusbyte(PrimarypicKomentoSiirräntäPortti, 0x11)
	PorttiKirjoitusbyte(SecondarypicKomentoSiirräntäPortti, 0x11)

	PorttiKirjoitusbyte(PrimarypicdataSiirräntäPortti, 0x20)
	PorttiKirjoitusbyte(SecondarypicdataSiirräntäPortti, 0x28)

	PorttiKirjoitusbyte(PrimarypicdataSiirräntäPortti, 0x04)
	PorttiKirjoitusbyte(SecondarypicdataSiirräntäPortti, 0x02)

	PorttiKirjoitusbyte(PrimarypicdataSiirräntäPortti, 0x01)
	PorttiKirjoitusbyte(SecondarypicdataSiirräntäPortti, 0x01)

	PorttiKirjoitusbyte(PrimarypicdataSiirräntäPortti, 0xF8)
	PorttiKirjoitusbyte(SecondarypicdataSiirräntäPortti, 0xEF)

	idtOsoitin := [6]uint8{0, 0, 0, 0, 0, 0}
	koko := (*uint16)(Pointer(&idtOsoitin[0]))
	(*koko) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtOsoitin[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtOsoitin)))
}
func Lidt(lidtaddr uintptr)

func (itse *TKeskeytysmanager) KeskeytysdescriptorTaulukkohakusanaaseta(keskeytys int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTyyppi uint8) {

	handleraddressMatalabittiä := (*uint16)(Pointer(&idtdata[keskeytys*8+0]))
	(*handleraddressMatalabittiä) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[keskeytys*8+2]))
	(*gdtcodesegmentselector) = codesegment

	varattu := (*uint8)(Pointer(&idtdata[keskeytys*8+4]))
	(*varattu) = 0

	var IdtdescriptorLiitetty uint8 = 0x80
	pääsy := (*uint8)(Pointer(&idtdata[keskeytys*8+5]))
	(*pääsy) = (IdtdescriptorLiitetty | DescriptorTyyppi | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressKorkeabittiä := (*uint16)(Pointer(&idtdata[keskeytys*8+6]))
	(*handleraddressKorkeabittiä) = uint16((handler >> 16) & 0xFFFF)

}

func (itse *TKeskeytysmanager) Asetahandler(handler uintptr, KeskeytysNumero uint8) {
	handler_2[KeskeytysNumero] = handler
}
func (itse *TKeskeytysmanager) Gethandler(KeskeytysNumero uint8) uintptr {
	return handler_2[KeskeytysNumero]
}
func (itse *TKeskeytysmanager) DoKahvaKeskeytys(keskeytys uint8, esp uint32) uint32 {

	if keskeytysVirheenpaikannus {
		konsoli_2.MTulostaxy("[esp:", 1, 20)
		konsoli_2.MUnsignedinteger32Tulosta(uint32(keskeytys))
		konsoli_2.MTulosta(":")
		konsoli_2.MUnsignedinteger32Tulosta(esp)
	}
	handlerSuorita := false
	if handler_2[keskeytys] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[keskeytys])))
		esp = myfunction(esp)
		handlerSuorita = true

	}

	if !handlerSuorita && keskeytys == uint8(itse.laitteistoKeskeytysoffset) && itse.tehtävämanager != nil {
		esp = uint32(uintptr(Pointer(itse.tehtävämanager.Schedule((*TcpuTila)(Pointer(uintptr(esp)))))))

	}
	if !handlerSuorita && keskeytys == 0x80 {
		esp = kahvaunhandledsyscall(esp)
	}

	if keskeytys <= 0x1F {
	}
	if 0x20 <= keskeytys && keskeytys < 0x30 {
		if 0x28 <= keskeytys {
			PorttiKirjoitusbyte(SecondarypicKomentoSiirräntäPortti, 0x20)
		}
		PorttiKirjoitusbyte(PrimarypicKomentoSiirräntäPortti, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func asetacr3(address uint32)

var konsoli_2 TKonsoli = TKonsoli{}

func KahvaKeskeytys(esp uint32, keskeytys uint32) uint32 {

	if keskeytysVirheenpaikannus && keskeytys != 0x80 && keskeytys != 0x20 {
		konsoli_2.MTulostaxy("[esp:", 1, 21)
		konsoli_2.MUnsignedinteger32Tulosta(uint32(keskeytys))
		konsoli_2.MTulosta(":")
		konsoli_2.MUnsignedinteger32Tulosta(esp)
	}

	if AktiivinenKeskeytysmanager != 0 {
		p := (*TKeskeytysmanager)(Pointer(AktiivinenKeskeytysmanager))
		esp = p.DoKahvaKeskeytys(uint8(keskeytys), esp)
		return esp
	}
	if handler_2[keskeytys] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[keskeytys])))
		esp = myfunction(esp)
	}
	if keskeytys == 0x80 {
		return kahvaunhandledsyscall(esp)
	}
	if 0x20 <= keskeytys && keskeytys < 0x30 {
		if 0x28 <= keskeytys {
			PorttiKirjoitusbyte(SecondarypicKomentoSiirräntäPortti, 0x20)
		}
		PorttiKirjoitusbyte(PrimarypicKomentoSiirräntäPortti, 0x20)
	}

	return esp
}

func kahvaunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuTila)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(keskeytysSuljeloop).Pointer())
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

func exceptionhasVirhecode(keskeytys uint32) bool {
	switch keskeytys {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNimi(keskeytys uint32) string {
	switch keskeytys {
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

func exceptionKehysArvo(kehys uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(kehys + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func tulostaSivufaultTieto(virhe uint32) {
	MEmergencyKäytälokiaMerkkijono(" pf=[")
	if (virhe & 0x01) != 0 {
		MEmergencyKäytälokiaMerkkijono("protection")
	} else {
		MEmergencyKäytälokiaMerkkijono("not-present")
	}
	if (virhe & 0x02) != 0 {
		MEmergencyKäytälokiaMerkkijono(",write")
	} else {
		MEmergencyKäytälokiaMerkkijono(",read")
	}
	if (virhe & 0x04) != 0 {
		MEmergencyKäytälokiaMerkkijono(",user")
	} else {
		MEmergencyKäytälokiaMerkkijono(",kernel")
	}
	if (virhe & 0x08) != 0 {
		MEmergencyKäytälokiaMerkkijono(",reserved-bit")
	}
	if (virhe & 0x10) != 0 {
		MEmergencyKäytälokiaMerkkijono(",instruction-fetch")
	}
	MEmergencyKäytälokiaMerkkijono("]")
}

func tulostaexceptionselectorTieto(virhe uint32) {
	MEmergencyKäytälokiaMerkkijono(" selector=")
	MEmergencyKäytälokiaunsignedinteger32(virhe & 0xFFFFFFF8)
	MEmergencyKäytälokiaMerkkijono(" index=")
	MEmergencyKäytälokiaunsignedinteger32(virhe >> 3)
	MEmergencyKäytälokiaMerkkijono(" table=")
	if (virhe & 0x02) != 0 {
		MEmergencyKäytälokiaMerkkijono("IDT")
	} else if (virhe & 0x04) != 0 {
		MEmergencyKäytälokiaMerkkijono("LDT")
	} else {
		MEmergencyKäytälokiaMerkkijono("GDT")
	}
	MEmergencyKäytälokiaMerkkijono(" ext=")
	MEmergencyKäytälokiaunsignedinteger32(virhe & 0x01)
}

func Kahvaexception(esp uint32, keskeytys uint32) uint32 {
	MEmergencyKäytälokiaMerkkijono("\nEXCEPTION vec=")
	MEmergencyKäytälokiahexadecimal8(uint8(keskeytys))
	MEmergencyKäytälokiaMerkkijono(" ")
	MEmergencyKäytälokiaMerkkijono(exceptionNimi(keskeytys))
	MEmergencyKäytälokiaMerkkijono(" frame=")
	MEmergencyKäytälokiaunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyKäytälokiaMerkkijono(" invalid-frame")
		if exceptionhasVirhecode(keskeytys) {
			MEmergencyKäytälokiaMerkkijono(" raw-error-or-bad-esp=")
			MEmergencyKäytälokiaunsignedinteger32(esp)
			tulostaexceptionselectorTieto(esp)
		}
		MEmergencyKäytälokiaMerkkijono("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var virhe uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasVirhecode(keskeytys) {
		virhe = exceptionKehysArvo(esp, 0)
		eipoffset = 4
	}
	eip := exceptionKehysArvo(esp, eipoffset)
	cs := exceptionKehysArvo(esp, eipoffset+4)
	eflags := exceptionKehysArvo(esp, eipoffset+8)

	MEmergencyKäytälokiaMerkkijono(" err=")
	MEmergencyKäytälokiaunsignedinteger32(virhe)
	MEmergencyKäytälokiaMerkkijono(" eip=")
	MEmergencyKäytälokiaunsignedinteger32(eip)
	MEmergencyKäytälokiaMerkkijono(" cs=")
	MEmergencyKäytälokiaunsignedinteger32(cs)
	MEmergencyKäytälokiaMerkkijono(" eflags=")
	MEmergencyKäytälokiaunsignedinteger32(eflags)
	MEmergencyKäytälokiaMerkkijono(" cr0=")
	MEmergencyKäytälokiaunsignedinteger32(exceptioncr0())
	MEmergencyKäytälokiaMerkkijono(" cr3=")
	MEmergencyKäytälokiaunsignedinteger32(exceptioncr3())

	if keskeytys == 0x0E {
		MEmergencyKäytälokiaMerkkijono(" cr2=")
		MEmergencyKäytälokiaunsignedinteger32(exceptioncr2())
		tulostaSivufaultTieto(virhe)
	}

	if (cs & 0x03) != 0 {
		MEmergencyKäytälokiaMerkkijono(" useresp=")
		MEmergencyKäytälokiaunsignedinteger32(exceptionKehysArvo(esp, eipoffset+12))
		MEmergencyKäytälokiaMerkkijono(" ss=")
		MEmergencyKäytälokiaunsignedinteger32(exceptionKehysArvo(esp, eipoffset+16))
	}

	if exceptionhasVirhecode(keskeytys) {
		tulostaexceptionselectorTieto(virhe)
	}
	MEmergencyKäytälokiaMerkkijono("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltJälkeenfatalexception()

func KahvafatalKeskeytysKehys(tallennettuesp uint32, keskeytys uint32) uint32 {
	Kahvaexception(tallennettuesp+52, keskeytys)
	haltJälkeenfatalexception()
	return tallennettuesp
}

func KeskeytysAktiivinen()
func (itse *TKeskeytysmanager) Aktiivinen() {
	if AktiivinenKeskeytysmanager != 0 {
		itse.Deactive()
	}
	address := uintptr(Pointer(itse))
	AktiivinenKeskeytysmanager = address
	KeskeytysAktiivinen()
}
func Keskeytysdeactive()
func (itse *TKeskeytysmanager) Deactive() {
	AktiivinenKeskeytysmanager = 0
	Keskeytysdeactive()
}

func MyKahvaKeskeytys(keskeytys uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konsoli_2 := TKonsoli{}
	konsoli_2.MTulosta(buffer)
	return esp
}
func MyKokeile(keskeytys uint8, esp uint32)

func UnhandleKeskeytys() {
	buffer := []byte("unhandle interrupt\n")
	konsoli_2 := TKonsoli{}
	konsoli_2.MTulosta(buffer)
}

func keskeytyshandler_2(keskeytys uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konsoli_2 := TKonsoli{}
	konsoli_2.MTulosta(buffer)
	konsoli_2.MHexadecimalTulosta(0x40)
	return esp
}
func tulostaesp(esp uint32) {
	konsoli_2 := TKonsoli{}
	konsoli_2.MUnsignedinteger32Tulostaxy(esp, 20, 21)
}
func gettls() uint32
func Tulostatls() {

}
