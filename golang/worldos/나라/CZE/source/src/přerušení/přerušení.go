/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Přerušení

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "konzole"

func přerušeníignore()

func přerušeníexceptionhandler()
func přerušeníexceptionhandler0x00()
func přerušeníexceptionhandler0x01()
func přerušeníexceptionhandler0x02()
func přerušeníexceptionhandler0x03()
func přerušeníexceptionhandler0x04()
func přerušeníexceptionhandler0x05()
func přerušeníexceptionhandler0x06()
func přerušeníexceptionhandler0x07()
func přerušeníexceptionhandler0x08()
func přerušeníexceptionhandler0x09()
func přerušeníexceptionhandler0x0a()
func přerušeníexceptionhandler0x0b()
func přerušeníexceptionhandler0x0c()
func přerušeníexceptionhandler0x0d()
func přerušeníexceptionhandler0x0e()
func přerušeníexceptionhandler0x0f()
func přerušeníexceptionhandler0x10()
func přerušeníexceptionhandler0x11()
func přerušeníexceptionhandler0x12()
func přerušeníexceptionhandler0x13()

func přerušenírequesthandler0x00()
func přerušenírequesthandler0x01()
func přerušenírequesthandler0x02()
func přerušenírequesthandler0x03()
func přerušenírequesthandler0x04()
func přerušenírequesthandler0x05()
func přerušenírequesthandler0x06()
func přerušenírequesthandler0x07()
func přerušenírequesthandler0x08()
func přerušenírequesthandler0x09()
func přerušenírequesthandler0x0a()
func přerušenírequesthandler0x0b()
func přerušenírequesthandler0x0c()
func přerušenírequesthandler0x0d()
func přerušenírequesthandler0x0e()
func přerušenírequesthandler0x0f()

func přerušenírequesthandler0x80()
func přerušenírequesthandler0x81()
func přerušenírequesthandler0x82()

func OtestovatTisknout(umístění uint8, data uint8)
func nastavitds(dssegment uint32)
func nastavitgs(gssegment uint32)
func přerušeníKonecloop()

type TPřerušeníhandler struct {
	PřerušeníČíslo		uint8
	Přerušenímanager	uintptr
}
type IPřerušeníhandler interface {
	ÚchytkaPřerušení(uint32) uint32
}

func NovýPřerušeníhandler(Přerušenímanager uintptr, PřerušeníČíslo uint8) *TPřerušeníhandler {
	přerušeníhandler_2 := new(TPřerušeníhandler)
	přerušeníhandler_2.PřerušeníČíslo = PřerušeníČíslo
	přerušeníhandler_2.Přerušenímanager = Přerušenímanager
	return přerušeníhandler_2

}

var handler_2 [256]uintptr

func (self *TPřerušeníhandler) Init(PřerušeníČíslo uint8, Přerušenímanager uintptr, funcAdresa uintptr) {

	handler_2[PřerušeníČíslo] = funcAdresa

	self.PřerušeníČíslo = PřerušeníČíslo
	self.Přerušenímanager = Přerušenímanager

}
func (self *TPřerušeníhandler) NastavitÚchytkaPřerušenífuction(PřerušeníČíslo uint32, adresa uintptr) {
	handler_2[PřerušeníČíslo] = adresa
}
func (self *TPřerušeníhandler) Zničit() {
	selfuintptr := uintptr(Pointer(self))
	Přerušenímanager := (*TPřerušenímanager)(Pointer(self.Přerušenímanager))
	if selfuintptr == Přerušenímanager.Gethandler(self.PřerušeníČíslo) {
		Přerušenímanager.Nastavithandler(0, self.PřerušeníČíslo)
	}

}
func (self *TPřerušeníhandler) NastavitPřerušenímanager(Přerušenímanager uintptr) {
}
func (self *TPřerušeníhandler) NastavitPřerušeníČíslo(PřerušeníČíslo uint8) {
	self.PřerušeníČíslo = PřerušeníČíslo
}
func (self *TPřerušeníhandler) ÚchytkaPřerušení(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konzole_2 := TKonzole{}
	konzole_2.MTisknout(buffer)
	return esp
}
func ÚchytkaPřerušení1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konzole_2 := TKonzole{}
	konzole_2.MTisknout(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TPřerušenídescriptorTabulkaKurzor struct {
}

var idtdata [256 * 8]uint8
var AktivníPřerušenímanager uintptr = 0

const přerušeníLadit = false

type TPřerušenímanager struct {
	handler_2	[256]uintptr

	hardwarePřerušeníoffset	uint16

	úlohamanager	*TÚlohamanager
}

var PrimarypicPříkazioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicPříkazioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (self *TPřerušenímanager) Init(hardwarePřerušeníoffset uint16, globálnídescriptorTabulka *TShareddescriptorTabulka, úlohamanager *TÚlohamanager) {

	self.úlohamanager = úlohamanager

	self.hardwarePřerušeníoffset = hardwarePřerušeníoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var adresa uint32
	var IdtPřerušenígate uint8 = 0xE
	adresa = uint32(ValueOf(přerušeníignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		adresa = uint32(ValueOf(přerušeníexceptionhandler0x0f).Pointer())
		self.PřerušenídescriptorTabulkaZáznamNastavit(i, codesegment, adresa, 0, IdtPřerušenígate)
	}

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x00).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x00, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x01).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x01, codesegment, adresa, 0, IdtPřerušenígate)
	adresa = uint32(ValueOf(přerušeníexceptionhandler0x02).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x02, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x03).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x03, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x04).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x04, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x05).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x05, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x06).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x06, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x07).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x07, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x08).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x08, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x09).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x09, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x0a).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x0A, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x0b).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x0B, codesegment, adresa, 0, IdtPřerušenígate)
	adresa = uint32(ValueOf(přerušeníexceptionhandler0x0c).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x0C, codesegment, adresa, 0, IdtPřerušenígate)
	adresa = uint32(ValueOf(přerušeníexceptionhandler0x0d).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x0D, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x0e).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x0E, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x0f).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x0F, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x10).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x10, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x11).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x11, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x12).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x12, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušeníexceptionhandler0x13).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x13, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x00).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x20, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x01).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x21, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x02).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x22, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x03).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x23, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x04).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x24, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x05).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x25, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x06).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x26, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x07).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x27, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x08).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x28, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x09).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x29, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x0a).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x2A, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x0b).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x2B, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x0c).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x2C, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x0d).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x2D, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x0e).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x2E, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x0f).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x2F, codesegment, adresa, 0, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x80).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x80, codesegment, adresa, 3, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x81).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x81, codesegment, adresa, 3, IdtPřerušenígate)

	adresa = uint32(ValueOf(přerušenírequesthandler0x82).Pointer())
	self.PřerušenídescriptorTabulkaZáznamNastavit(0x82, codesegment, adresa, 3, IdtPřerušenígate)

	PortZápisbyte(PrimarypicPříkazioport, 0x11)
	PortZápisbyte(SecondarypicPříkazioport, 0x11)

	PortZápisbyte(Primarypicdataioport, 0x20)
	PortZápisbyte(Secondarypicdataioport, 0x28)

	PortZápisbyte(Primarypicdataioport, 0x04)
	PortZápisbyte(Secondarypicdataioport, 0x02)

	PortZápisbyte(Primarypicdataioport, 0x01)
	PortZápisbyte(Secondarypicdataioport, 0x01)

	PortZápisbyte(Primarypicdataioport, 0xF8)
	PortZápisbyte(Secondarypicdataioport, 0xEF)

	idtKurzor := [6]uint8{0, 0, 0, 0, 0, 0}
	velikost := (*uint16)(Pointer(&idtKurzor[0]))
	(*velikost) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtKurzor[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtKurzor)))
}
func Lidt(lidtaddr uintptr)

func (self *TPřerušenímanager) PřerušenídescriptorTabulkaZáznamNastavit(přerušení int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTyp uint8) {

	handlerAdresaNízkábitů := (*uint16)(Pointer(&idtdata[přerušení*8+0]))
	(*handlerAdresaNízkábitů) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[přerušení*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reservovaná := (*uint8)(Pointer(&idtdata[přerušení*8+4]))
	(*reservovaná) = 0

	var IdtdescriptorSoučasný uint8 = 0x80
	přístup := (*uint8)(Pointer(&idtdata[přerušení*8+5]))
	(*přístup) = (IdtdescriptorSoučasný | DescriptorTyp | ((Descriptorprivilegelevel & 3) << 5))

	handlerAdresaVysokábitů := (*uint16)(Pointer(&idtdata[přerušení*8+6]))
	(*handlerAdresaVysokábitů) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TPřerušenímanager) Nastavithandler(handler uintptr, PřerušeníČíslo uint8) {
	handler_2[PřerušeníČíslo] = handler
}
func (self *TPřerušenímanager) Gethandler(PřerušeníČíslo uint8) uintptr {
	return handler_2[PřerušeníČíslo]
}
func (self *TPřerušenímanager) DoÚchytkaPřerušení(přerušení uint8, esp uint32) uint32 {

	if přerušeníLadit {
		konzole_2.MTisknoutxy("[esp:", 1, 20)
		konzole_2.MUnsignedinteger32Tisknout(uint32(přerušení))
		konzole_2.MTisknout(":")
		konzole_2.MUnsignedinteger32Tisknout(esp)
	}
	handlerSpustit := false
	if handler_2[přerušení] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[přerušení])))
		esp = myfunction(esp)
		handlerSpustit = true

	}

	if !handlerSpustit && přerušení == uint8(self.hardwarePřerušeníoffset) && self.úlohamanager != nil {
		esp = uint32(uintptr(Pointer(self.úlohamanager.Schedule((*TcpuStav)(Pointer(uintptr(esp)))))))

	}
	if !handlerSpustit && přerušení == 0x80 {
		esp = úchytkaunhandledsyscall(esp)
	}

	if přerušení <= 0x1F {
	}
	if 0x20 <= přerušení && přerušení < 0x30 {
		if 0x28 <= přerušení {
			PortZápisbyte(SecondarypicPříkazioport, 0x20)
		}
		PortZápisbyte(PrimarypicPříkazioport, 0x20)
	}
	return esp
}

var počet2 uint8 = 1

func nastavitcr3(adresa uint32)

var konzole_2 TKonzole = TKonzole{}

func ÚchytkaPřerušení(esp uint32, přerušení uint32) uint32 {

	if přerušeníLadit && přerušení != 0x80 && přerušení != 0x20 {
		konzole_2.MTisknoutxy("[esp:", 1, 21)
		konzole_2.MUnsignedinteger32Tisknout(uint32(přerušení))
		konzole_2.MTisknout(":")
		konzole_2.MUnsignedinteger32Tisknout(esp)
	}

	if AktivníPřerušenímanager != 0 {
		p := (*TPřerušenímanager)(Pointer(AktivníPřerušenímanager))
		esp = p.DoÚchytkaPřerušení(uint8(přerušení), esp)
		return esp
	}
	if handler_2[přerušení] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[přerušení])))
		esp = myfunction(esp)
	}
	if přerušení == 0x80 {
		return úchytkaunhandledsyscall(esp)
	}
	if 0x20 <= přerušení && přerušení < 0x30 {
		if 0x28 <= přerušení {
			PortZápisbyte(SecondarypicPříkazioport, 0x20)
		}
		PortZápisbyte(PrimarypicPříkazioport, 0x20)
	}

	return esp
}

func úchytkaunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStav)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(přerušeníKonecloop).Pointer())
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

func exceptionhasChybacode(přerušení uint32) bool {
	switch přerušení {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNázev(přerušení uint32) string {
	switch přerušení {
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

func exceptionRámHodnota(rám uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(rám + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func tisknoutStránkafaultInformace(chyba uint32) {
	MEmergencyProtokolřetězec(" pf=[")
	if (chyba & 0x01) != 0 {
		MEmergencyProtokolřetězec("protection")
	} else {
		MEmergencyProtokolřetězec("not-present")
	}
	if (chyba & 0x02) != 0 {
		MEmergencyProtokolřetězec(",write")
	} else {
		MEmergencyProtokolřetězec(",read")
	}
	if (chyba & 0x04) != 0 {
		MEmergencyProtokolřetězec(",user")
	} else {
		MEmergencyProtokolřetězec(",kernel")
	}
	if (chyba & 0x08) != 0 {
		MEmergencyProtokolřetězec(",reserved-bit")
	}
	if (chyba & 0x10) != 0 {
		MEmergencyProtokolřetězec(",instruction-fetch")
	}
	MEmergencyProtokolřetězec("]")
}

func tisknoutexceptionselectorInformace(chyba uint32) {
	MEmergencyProtokolřetězec(" selector=")
	MEmergencyProtokolunsignedinteger32(chyba & 0xFFFFFFF8)
	MEmergencyProtokolřetězec(" index=")
	MEmergencyProtokolunsignedinteger32(chyba >> 3)
	MEmergencyProtokolřetězec(" table=")
	if (chyba & 0x02) != 0 {
		MEmergencyProtokolřetězec("IDT")
	} else if (chyba & 0x04) != 0 {
		MEmergencyProtokolřetězec("LDT")
	} else {
		MEmergencyProtokolřetězec("GDT")
	}
	MEmergencyProtokolřetězec(" ext=")
	MEmergencyProtokolunsignedinteger32(chyba & 0x01)
}

func Úchytkaexception(esp uint32, přerušení uint32) uint32 {
	MEmergencyProtokolřetězec("\nEXCEPTION vec=")
	MEmergencyProtokolhexadecimal8(uint8(přerušení))
	MEmergencyProtokolřetězec(" ")
	MEmergencyProtokolřetězec(exceptionNázev(přerušení))
	MEmergencyProtokolřetězec(" frame=")
	MEmergencyProtokolunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyProtokolřetězec(" invalid-frame")
		if exceptionhasChybacode(přerušení) {
			MEmergencyProtokolřetězec(" raw-error-or-bad-esp=")
			MEmergencyProtokolunsignedinteger32(esp)
			tisknoutexceptionselectorInformace(esp)
		}
		MEmergencyProtokolřetězec("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var chyba uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasChybacode(přerušení) {
		chyba = exceptionRámHodnota(esp, 0)
		eipoffset = 4
	}
	eip := exceptionRámHodnota(esp, eipoffset)
	cs := exceptionRámHodnota(esp, eipoffset+4)
	eflags := exceptionRámHodnota(esp, eipoffset+8)

	MEmergencyProtokolřetězec(" err=")
	MEmergencyProtokolunsignedinteger32(chyba)
	MEmergencyProtokolřetězec(" eip=")
	MEmergencyProtokolunsignedinteger32(eip)
	MEmergencyProtokolřetězec(" cs=")
	MEmergencyProtokolunsignedinteger32(cs)
	MEmergencyProtokolřetězec(" eflags=")
	MEmergencyProtokolunsignedinteger32(eflags)
	MEmergencyProtokolřetězec(" cr0=")
	MEmergencyProtokolunsignedinteger32(exceptioncr0())
	MEmergencyProtokolřetězec(" cr3=")
	MEmergencyProtokolunsignedinteger32(exceptioncr3())

	if přerušení == 0x0E {
		MEmergencyProtokolřetězec(" cr2=")
		MEmergencyProtokolunsignedinteger32(exceptioncr2())
		tisknoutStránkafaultInformace(chyba)
	}

	if (cs & 0x03) != 0 {
		MEmergencyProtokolřetězec(" useresp=")
		MEmergencyProtokolunsignedinteger32(exceptionRámHodnota(esp, eipoffset+12))
		MEmergencyProtokolřetězec(" ss=")
		MEmergencyProtokolunsignedinteger32(exceptionRámHodnota(esp, eipoffset+16))
	}

	if exceptionhasChybacode(přerušení) {
		tisknoutexceptionselectorInformace(chyba)
	}
	MEmergencyProtokolřetězec("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltPotomfatalexception()

func ÚchytkafatalPřerušeníRám(uloženoesp uint32, přerušení uint32) uint32 {
	Úchytkaexception(uloženoesp+52, přerušení)
	haltPotomfatalexception()
	return uloženoesp
}

func PřerušeníAktivní()
func (self *TPřerušenímanager) Aktivní() {
	if AktivníPřerušenímanager != 0 {
		self.Deactive()
	}
	adresa := uintptr(Pointer(self))
	AktivníPřerušenímanager = adresa
	PřerušeníAktivní()
}
func Přerušenídeactive()
func (self *TPřerušenímanager) Deactive() {
	AktivníPřerušenímanager = 0
	Přerušenídeactive()
}

func MyÚchytkaPřerušení(přerušení uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konzole_2 := TKonzole{}
	konzole_2.MTisknout(buffer)
	return esp
}
func MyOtestovat(přerušení uint8, esp uint32)

func UnhandlePřerušení() {
	buffer := []byte("unhandle interrupt\n")
	konzole_2 := TKonzole{}
	konzole_2.MTisknout(buffer)
}

func přerušeníhandler_2(přerušení uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konzole_2 := TKonzole{}
	konzole_2.MTisknout(buffer)
	konzole_2.MHexadecimalTisknout(0x40)
	return esp
}
func tisknoutesp(esp uint32) {
	konzole_2 := TKonzole{}
	konzole_2.MUnsignedinteger32Tisknoutxy(esp, 20, 21)
}
func gettls() uint32
func Tisknouttls() {

}
