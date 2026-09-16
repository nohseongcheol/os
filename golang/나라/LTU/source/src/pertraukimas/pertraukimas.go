/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Pertraukimas

import . "unsafe"
import . "reflect"

import . "prievadas"
import . "gdt"
import . "multitasking"
import . "console"

func pertraukimasignore()

func pertraukimasexceptionhandler()
func pertraukimasexceptionhandler0x00()
func pertraukimasexceptionhandler0x01()
func pertraukimasexceptionhandler0x02()
func pertraukimasexceptionhandler0x03()
func pertraukimasexceptionhandler0x04()
func pertraukimasexceptionhandler0x05()
func pertraukimasexceptionhandler0x06()
func pertraukimasexceptionhandler0x07()
func pertraukimasexceptionhandler0x08()
func pertraukimasexceptionhandler0x09()
func pertraukimasexceptionhandler0x0a()
func pertraukimasexceptionhandler0x0b()
func pertraukimasexceptionhandler0x0c()
func pertraukimasexceptionhandler0x0d()
func pertraukimasexceptionhandler0x0e()
func pertraukimasexceptionhandler0x0f()
func pertraukimasexceptionhandler0x10()
func pertraukimasexceptionhandler0x11()
func pertraukimasexceptionhandler0x12()
func pertraukimasexceptionhandler0x13()

func pertraukimasrequesthandler0x00()
func pertraukimasrequesthandler0x01()
func pertraukimasrequesthandler0x02()
func pertraukimasrequesthandler0x03()
func pertraukimasrequesthandler0x04()
func pertraukimasrequesthandler0x05()
func pertraukimasrequesthandler0x06()
func pertraukimasrequesthandler0x07()
func pertraukimasrequesthandler0x08()
func pertraukimasrequesthandler0x09()
func pertraukimasrequesthandler0x0a()
func pertraukimasrequesthandler0x0b()
func pertraukimasrequesthandler0x0c()
func pertraukimasrequesthandler0x0d()
func pertraukimasrequesthandler0x0e()
func pertraukimasrequesthandler0x0f()

func pertraukimasrequesthandler0x80()
func pertraukimasrequesthandler0x81()
func pertraukimasrequesthandler0x82()

func TestasSpausdinti(pozicija uint8, data uint8)
func nustatytads(dssegment uint32)
func nustatytags(gssegment uint32)
func pertraukimasIšeitiloop()

type TPertraukimashandler struct {
	PertraukimasSkaičius	uint8
	Pertraukimasmanager	uintptr
}
type IPertraukimashandler interface {
	PozicijaPertraukimas(uint32) uint32
}

func NaujasPertraukimashandler(Pertraukimasmanager uintptr, PertraukimasSkaičius uint8) *TPertraukimashandler {
	pertraukimashandler_2 := new(TPertraukimashandler)
	pertraukimashandler_2.PertraukimasSkaičius = PertraukimasSkaičius
	pertraukimashandler_2.Pertraukimasmanager = Pertraukimasmanager
	return pertraukimashandler_2

}

var handler_2 [256]uintptr

func (self *TPertraukimashandler) Init(PertraukimasSkaičius uint8, Pertraukimasmanager uintptr, funcaddress uintptr) {

	handler_2[PertraukimasSkaičius] = funcaddress

	self.PertraukimasSkaičius = PertraukimasSkaičius
	self.Pertraukimasmanager = Pertraukimasmanager

}
func (self *TPertraukimashandler) NustatytaPozicijaPertraukimasfuction(PertraukimasSkaičius uint32, address uintptr) {
	handler_2[PertraukimasSkaičius] = address
}
func (self *TPertraukimashandler) Sunaikinti() {
	selfuintptr := uintptr(Pointer(self))
	Pertraukimasmanager := (*TPertraukimasmanager)(Pointer(self.Pertraukimasmanager))
	if selfuintptr == Pertraukimasmanager.Gethandler(self.PertraukimasSkaičius) {
		Pertraukimasmanager.Nustatytahandler(0, self.PertraukimasSkaičius)
	}

}
func (self *TPertraukimashandler) NustatytaPertraukimasmanager(Pertraukimasmanager uintptr) {
}
func (self *TPertraukimashandler) NustatytaPertraukimasSkaičius(PertraukimasSkaičius uint8) {
	self.PertraukimasSkaičius = PertraukimasSkaičius
}
func (self *TPertraukimashandler) PozicijaPertraukimas(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MSpausdinti(buffer)
	return esp
}
func PozicijaPertraukimas1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MSpausdinti(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TPertraukimasdescriptorLentelėRodyklė struct {
}

var idtdata [256 * 8]uint8
var AktyvusPertraukimasmanager uintptr = 0

const pertraukimasDerinti = false

type TPertraukimasmanager struct {
	handler_2	[256]uintptr

	aparatinėįrangaPertraukimasoffset	uint16

	užduotismanager	*TUžduotismanager
}

var PrimarypicKomandaioPrievadas uint16 = 0x20
var PrimarypicdataioPrievadas uint16 = 0x21
var SecondarypicKomandaioPrievadas uint16 = 0xA0
var SecondarypicdataioPrievadas uint16 = 0xA1

func (self *TPertraukimasmanager) Init(aparatinėįrangaPertraukimasoffset uint16, visuotinėdescriptorLentelė *TShareddescriptorLentelė, užduotismanager *TUžduotismanager) {

	self.užduotismanager = užduotismanager

	self.aparatinėįrangaPertraukimasoffset = aparatinėįrangaPertraukimasoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtPertraukimasgate uint8 = 0xE
	address = uint32(ValueOf(pertraukimasignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(pertraukimasexceptionhandler0x0f).Pointer())
		self.PertraukimasdescriptorLentelėįrašasnustatyta(i, codesegment, address, 0, IdtPertraukimasgate)
	}

	address = uint32(ValueOf(pertraukimasexceptionhandler0x00).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x00, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x01).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x01, codesegment, address, 0, IdtPertraukimasgate)
	address = uint32(ValueOf(pertraukimasexceptionhandler0x02).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x02, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x03).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x03, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x04).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x04, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x05).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x05, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x06).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x06, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x07).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x07, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x08).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x08, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x09).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x09, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x0a).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x0A, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x0b).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x0B, codesegment, address, 0, IdtPertraukimasgate)
	address = uint32(ValueOf(pertraukimasexceptionhandler0x0c).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x0C, codesegment, address, 0, IdtPertraukimasgate)
	address = uint32(ValueOf(pertraukimasexceptionhandler0x0d).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x0D, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x0e).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x0E, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x0f).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x0F, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x10).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x10, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x11).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x11, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x12).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x12, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasexceptionhandler0x13).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x13, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x00).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x20, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x01).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x21, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x02).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x22, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x03).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x23, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x04).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x24, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x05).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x25, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x06).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x26, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x07).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x27, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x08).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x28, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x09).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x29, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x0a).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x2A, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x0b).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x2B, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x0c).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x2C, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x0d).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x2D, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x0e).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x2E, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x0f).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x2F, codesegment, address, 0, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x80).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x80, codesegment, address, 3, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x81).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x81, codesegment, address, 3, IdtPertraukimasgate)

	address = uint32(ValueOf(pertraukimasrequesthandler0x82).Pointer())
	self.PertraukimasdescriptorLentelėįrašasnustatyta(0x82, codesegment, address, 3, IdtPertraukimasgate)

	PrievadasRašymasbyte(PrimarypicKomandaioPrievadas, 0x11)
	PrievadasRašymasbyte(SecondarypicKomandaioPrievadas, 0x11)

	PrievadasRašymasbyte(PrimarypicdataioPrievadas, 0x20)
	PrievadasRašymasbyte(SecondarypicdataioPrievadas, 0x28)

	PrievadasRašymasbyte(PrimarypicdataioPrievadas, 0x04)
	PrievadasRašymasbyte(SecondarypicdataioPrievadas, 0x02)

	PrievadasRašymasbyte(PrimarypicdataioPrievadas, 0x01)
	PrievadasRašymasbyte(SecondarypicdataioPrievadas, 0x01)

	PrievadasRašymasbyte(PrimarypicdataioPrievadas, 0xF8)
	PrievadasRašymasbyte(SecondarypicdataioPrievadas, 0xEF)

	idtRodyklė := [6]uint8{0, 0, 0, 0, 0, 0}
	dydis := (*uint16)(Pointer(&idtRodyklė[0]))
	(*dydis) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtRodyklė[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtRodyklė)))
}
func Lidt(lidtaddr uintptr)

func (self *TPertraukimasmanager) PertraukimasdescriptorLentelėįrašasnustatyta(pertraukimas int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTipas uint8) {

	handleraddressŽemasbitų := (*uint16)(Pointer(&idtdata[pertraukimas*8+0]))
	(*handleraddressŽemasbitų) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[pertraukimas*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[pertraukimas*8+4]))
	(*reserved) = 0

	var IdtdescriptorYra uint8 = 0x80
	prieiti := (*uint8)(Pointer(&idtdata[pertraukimas*8+5]))
	(*prieiti) = (IdtdescriptorYra | DescriptorTipas | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressAukštasbitų := (*uint16)(Pointer(&idtdata[pertraukimas*8+6]))
	(*handleraddressAukštasbitų) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TPertraukimasmanager) Nustatytahandler(handler uintptr, PertraukimasSkaičius uint8) {
	handler_2[PertraukimasSkaičius] = handler
}
func (self *TPertraukimasmanager) Gethandler(PertraukimasSkaičius uint8) uintptr {
	return handler_2[PertraukimasSkaičius]
}
func (self *TPertraukimasmanager) DoPozicijaPertraukimas(pertraukimas uint8, esp uint32) uint32 {

	if pertraukimasDerinti {
		console_2.MSpausdintixy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Spausdinti(uint32(pertraukimas))
		console_2.MSpausdinti(":")
		console_2.MUnsignedinteger32Spausdinti(esp)
	}
	handlerPaleisti := false
	if handler_2[pertraukimas] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[pertraukimas])))
		esp = myfunction(esp)
		handlerPaleisti = true

	}

	if !handlerPaleisti && pertraukimas == uint8(self.aparatinėįrangaPertraukimasoffset) && self.užduotismanager != nil {
		esp = uint32(uintptr(Pointer(self.užduotismanager.Schedule((*TcpuBūsena)(Pointer(uintptr(esp)))))))

	}
	if !handlerPaleisti && pertraukimas == 0x80 {
		esp = pozicijaunhandledsyscall(esp)
	}

	if pertraukimas <= 0x1F {
	}
	if 0x20 <= pertraukimas && pertraukimas < 0x30 {
		if 0x28 <= pertraukimas {
			PrievadasRašymasbyte(SecondarypicKomandaioPrievadas, 0x20)
		}
		PrievadasRašymasbyte(PrimarypicKomandaioPrievadas, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func nustatytacr3(address uint32)

var console_2 TConsole = TConsole{}

func PozicijaPertraukimas(esp uint32, pertraukimas uint32) uint32 {

	if pertraukimasDerinti && pertraukimas != 0x80 && pertraukimas != 0x20 {
		console_2.MSpausdintixy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Spausdinti(uint32(pertraukimas))
		console_2.MSpausdinti(":")
		console_2.MUnsignedinteger32Spausdinti(esp)
	}

	if AktyvusPertraukimasmanager != 0 {
		p := (*TPertraukimasmanager)(Pointer(AktyvusPertraukimasmanager))
		esp = p.DoPozicijaPertraukimas(uint8(pertraukimas), esp)
		return esp
	}
	if handler_2[pertraukimas] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[pertraukimas])))
		esp = myfunction(esp)
	}
	if pertraukimas == 0x80 {
		return pozicijaunhandledsyscall(esp)
	}
	if 0x20 <= pertraukimas && pertraukimas < 0x30 {
		if 0x28 <= pertraukimas {
			PrievadasRašymasbyte(SecondarypicKomandaioPrievadas, 0x20)
		}
		PrievadasRašymasbyte(PrimarypicKomandaioPrievadas, 0x20)
	}

	return esp
}

func pozicijaunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuBūsena)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(pertraukimasIšeitiloop).Pointer())
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

func exceptionhasKlaidacode(pertraukimas uint32) bool {
	switch pertraukimas {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionPavadinimas(pertraukimas uint32) string {
	switch pertraukimas {
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

func exceptionKadrasReikšmė(kadras uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(kadras + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func spausdintiPuslapisfaultInformacija(klaidos uint32) {
	MEmergencyŽurnalasEilutė(" pf=[")
	if (klaidos & 0x01) != 0 {
		MEmergencyŽurnalasEilutė("protection")
	} else {
		MEmergencyŽurnalasEilutė("not-present")
	}
	if (klaidos & 0x02) != 0 {
		MEmergencyŽurnalasEilutė(",write")
	} else {
		MEmergencyŽurnalasEilutė(",read")
	}
	if (klaidos & 0x04) != 0 {
		MEmergencyŽurnalasEilutė(",user")
	} else {
		MEmergencyŽurnalasEilutė(",kernel")
	}
	if (klaidos & 0x08) != 0 {
		MEmergencyŽurnalasEilutė(",reserved-bit")
	}
	if (klaidos & 0x10) != 0 {
		MEmergencyŽurnalasEilutė(",instruction-fetch")
	}
	MEmergencyŽurnalasEilutė("]")
}

func spausdintiexceptionselectorInformacija(klaidos uint32) {
	MEmergencyŽurnalasEilutė(" selector=")
	MEmergencyŽurnalasunsignedinteger32(klaidos & 0xFFFFFFF8)
	MEmergencyŽurnalasEilutė(" index=")
	MEmergencyŽurnalasunsignedinteger32(klaidos >> 3)
	MEmergencyŽurnalasEilutė(" table=")
	if (klaidos & 0x02) != 0 {
		MEmergencyŽurnalasEilutė("IDT")
	} else if (klaidos & 0x04) != 0 {
		MEmergencyŽurnalasEilutė("LDT")
	} else {
		MEmergencyŽurnalasEilutė("GDT")
	}
	MEmergencyŽurnalasEilutė(" ext=")
	MEmergencyŽurnalasunsignedinteger32(klaidos & 0x01)
}

func Pozicijaexception(esp uint32, pertraukimas uint32) uint32 {
	MEmergencyŽurnalasEilutė("\nEXCEPTION vec=")
	MEmergencyŽurnalashexadecimal8(uint8(pertraukimas))
	MEmergencyŽurnalasEilutė(" ")
	MEmergencyŽurnalasEilutė(exceptionPavadinimas(pertraukimas))
	MEmergencyŽurnalasEilutė(" frame=")
	MEmergencyŽurnalasunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyŽurnalasEilutė(" invalid-frame")
		if exceptionhasKlaidacode(pertraukimas) {
			MEmergencyŽurnalasEilutė(" raw-error-or-bad-esp=")
			MEmergencyŽurnalasunsignedinteger32(esp)
			spausdintiexceptionselectorInformacija(esp)
		}
		MEmergencyŽurnalasEilutė("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var klaidos uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasKlaidacode(pertraukimas) {
		klaidos = exceptionKadrasReikšmė(esp, 0)
		eipoffset = 4
	}
	eip := exceptionKadrasReikšmė(esp, eipoffset)
	cs := exceptionKadrasReikšmė(esp, eipoffset+4)
	eflags := exceptionKadrasReikšmė(esp, eipoffset+8)

	MEmergencyŽurnalasEilutė(" err=")
	MEmergencyŽurnalasunsignedinteger32(klaidos)
	MEmergencyŽurnalasEilutė(" eip=")
	MEmergencyŽurnalasunsignedinteger32(eip)
	MEmergencyŽurnalasEilutė(" cs=")
	MEmergencyŽurnalasunsignedinteger32(cs)
	MEmergencyŽurnalasEilutė(" eflags=")
	MEmergencyŽurnalasunsignedinteger32(eflags)
	MEmergencyŽurnalasEilutė(" cr0=")
	MEmergencyŽurnalasunsignedinteger32(exceptioncr0())
	MEmergencyŽurnalasEilutė(" cr3=")
	MEmergencyŽurnalasunsignedinteger32(exceptioncr3())

	if pertraukimas == 0x0E {
		MEmergencyŽurnalasEilutė(" cr2=")
		MEmergencyŽurnalasunsignedinteger32(exceptioncr2())
		spausdintiPuslapisfaultInformacija(klaidos)
	}

	if (cs & 0x03) != 0 {
		MEmergencyŽurnalasEilutė(" useresp=")
		MEmergencyŽurnalasunsignedinteger32(exceptionKadrasReikšmė(esp, eipoffset+12))
		MEmergencyŽurnalasEilutė(" ss=")
		MEmergencyŽurnalasunsignedinteger32(exceptionKadrasReikšmė(esp, eipoffset+16))
	}

	if exceptionhasKlaidacode(pertraukimas) {
		spausdintiexceptionselectorInformacija(klaidos)
	}
	MEmergencyŽurnalasEilutė("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func PozicijafatalPertraukimasKadras(savedesp uint32, pertraukimas uint32) uint32 {
	Pozicijaexception(savedesp+52, pertraukimas)
	haltafterfatalexception()
	return savedesp
}

func PertraukimasAktyvus()
func (self *TPertraukimasmanager) Aktyvus() {
	if AktyvusPertraukimasmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	AktyvusPertraukimasmanager = address
	PertraukimasAktyvus()
}
func Pertraukimasdeactive()
func (self *TPertraukimasmanager) Deactive() {
	AktyvusPertraukimasmanager = 0
	Pertraukimasdeactive()
}

func MyPozicijaPertraukimas(pertraukimas uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MSpausdinti(buffer)
	return esp
}
func MyTestas(pertraukimas uint8, esp uint32)

func UnhandlePertraukimas() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MSpausdinti(buffer)
}

func pertraukimashandler_2(pertraukimas uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MSpausdinti(buffer)
	console_2.MHexadecimalSpausdinti(0x40)
	return esp
}
func spausdintiesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Spausdintixy(esp, 20, 21)
}
func gettls() uint32
func Spausdintitls() {

}
