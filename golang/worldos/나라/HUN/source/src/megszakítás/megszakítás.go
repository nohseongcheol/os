/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Megszakítás

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "konzol"

func megszakításignore()

func megszakításexceptionhandler()
func megszakításexceptionhandler0x00()
func megszakításexceptionhandler0x01()
func megszakításexceptionhandler0x02()
func megszakításexceptionhandler0x03()
func megszakításexceptionhandler0x04()
func megszakításexceptionhandler0x05()
func megszakításexceptionhandler0x06()
func megszakításexceptionhandler0x07()
func megszakításexceptionhandler0x08()
func megszakításexceptionhandler0x09()
func megszakításexceptionhandler0x0a()
func megszakításexceptionhandler0x0b()
func megszakításexceptionhandler0x0c()
func megszakításexceptionhandler0x0d()
func megszakításexceptionhandler0x0e()
func megszakításexceptionhandler0x0f()
func megszakításexceptionhandler0x10()
func megszakításexceptionhandler0x11()
func megszakításexceptionhandler0x12()
func megszakításexceptionhandler0x13()

func megszakításrequesthandler0x00()
func megszakításrequesthandler0x01()
func megszakításrequesthandler0x02()
func megszakításrequesthandler0x03()
func megszakításrequesthandler0x04()
func megszakításrequesthandler0x05()
func megszakításrequesthandler0x06()
func megszakításrequesthandler0x07()
func megszakításrequesthandler0x08()
func megszakításrequesthandler0x09()
func megszakításrequesthandler0x0a()
func megszakításrequesthandler0x0b()
func megszakításrequesthandler0x0c()
func megszakításrequesthandler0x0d()
func megszakításrequesthandler0x0e()
func megszakításrequesthandler0x0f()

func megszakításrequesthandler0x80()
func megszakításrequesthandler0x81()
func megszakításrequesthandler0x82()

func TesztNyomtatás(pozíció uint8, data uint8)
func halmazds(dssegment uint32)
func halmazgs(gssegment uint32)
func megszakításKilépésHurok()

type TMegszakításhandler struct {
	MegszakításSzám		uint8
	Megszakításmanager	uintptr
}
type IMegszakításhandler interface {
	FogantyúMegszakítás(uint32) uint32
}

func ÚjMegszakításhandler(Megszakításmanager uintptr, MegszakításSzám uint8) *TMegszakításhandler {
	megszakításhandler_2 := new(TMegszakításhandler)
	megszakításhandler_2.MegszakításSzám = MegszakításSzám
	megszakításhandler_2.Megszakításmanager = Megszakításmanager
	return megszakításhandler_2

}

var handler_2 [256]uintptr

func (self *TMegszakításhandler) Init(MegszakításSzám uint8, Megszakításmanager uintptr, funcaddress uintptr) {

	handler_2[MegszakításSzám] = funcaddress

	self.MegszakításSzám = MegszakításSzám
	self.Megszakításmanager = Megszakításmanager

}
func (self *TMegszakításhandler) HalmazFogantyúMegszakításfuction(MegszakításSzám uint32, address uintptr) {
	handler_2[MegszakításSzám] = address
}
func (self *TMegszakításhandler) Megsemmisítés() {
	selfuintptr := uintptr(Pointer(self))
	Megszakításmanager := (*TMegszakításmanager)(Pointer(self.Megszakításmanager))
	if selfuintptr == Megszakításmanager.Gethandler(self.MegszakításSzám) {
		Megszakításmanager.Halmazhandler(0, self.MegszakításSzám)
	}

}
func (self *TMegszakításhandler) HalmazMegszakításmanager(Megszakításmanager uintptr) {
}
func (self *TMegszakításhandler) HalmazMegszakításSzám(MegszakításSzám uint8) {
	self.MegszakításSzám = MegszakításSzám
}
func (self *TMegszakításhandler) FogantyúMegszakítás(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	konzol_2 := TKonzol{}
	konzol_2.MNyomtatás(buffer)
	return esp
}
func FogantyúMegszakítás1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	konzol_2 := TKonzol{}
	konzol_2.MNyomtatás(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TMegszakításdescriptorTáblázatMutató struct {
}

var idtdata [256 * 8]uint8
var AktívMegszakításmanager uintptr = 0

const megszakításHibakeresés = false

type TMegszakításmanager struct {
	handler_2	[256]uintptr

	hardverMegszakításEltolás	uint16

	feladatmanager	*TFeladatmanager
}

var PrimarypicParancsioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicParancsioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (self *TMegszakításmanager) Init(hardverMegszakításEltolás uint16, globálisdescriptorTáblázat *TShareddescriptorTáblázat, feladatmanager *TFeladatmanager) {

	self.feladatmanager = feladatmanager

	self.hardverMegszakításEltolás = hardverMegszakításEltolás
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtMegszakításgate uint8 = 0xE
	address = uint32(ValueOf(megszakításignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(megszakításexceptionhandler0x0f).Pointer())
		self.MegszakításdescriptorTáblázatbejegyzéshalmaz(i, codesegment, address, 0, IdtMegszakításgate)
	}

	address = uint32(ValueOf(megszakításexceptionhandler0x00).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x00, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x01).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x01, codesegment, address, 0, IdtMegszakításgate)
	address = uint32(ValueOf(megszakításexceptionhandler0x02).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x02, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x03).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x03, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x04).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x04, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x05).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x05, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x06).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x06, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x07).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x07, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x08).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x08, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x09).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x09, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x0a).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x0A, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x0b).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x0B, codesegment, address, 0, IdtMegszakításgate)
	address = uint32(ValueOf(megszakításexceptionhandler0x0c).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x0C, codesegment, address, 0, IdtMegszakításgate)
	address = uint32(ValueOf(megszakításexceptionhandler0x0d).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x0D, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x0e).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x0E, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x0f).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x0F, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x10).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x10, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x11).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x11, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x12).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x12, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításexceptionhandler0x13).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x13, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x00).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x20, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x01).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x21, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x02).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x22, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x03).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x23, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x04).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x24, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x05).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x25, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x06).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x26, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x07).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x27, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x08).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x28, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x09).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x29, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x0a).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x2A, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x0b).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x2B, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x0c).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x2C, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x0d).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x2D, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x0e).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x2E, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x0f).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x2F, codesegment, address, 0, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x80).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x80, codesegment, address, 3, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x81).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x81, codesegment, address, 3, IdtMegszakításgate)

	address = uint32(ValueOf(megszakításrequesthandler0x82).Pointer())
	self.MegszakításdescriptorTáblázatbejegyzéshalmaz(0x82, codesegment, address, 3, IdtMegszakításgate)

	PortÍrásbyte(PrimarypicParancsioport, 0x11)
	PortÍrásbyte(SecondarypicParancsioport, 0x11)

	PortÍrásbyte(Primarypicdataioport, 0x20)
	PortÍrásbyte(Secondarypicdataioport, 0x28)

	PortÍrásbyte(Primarypicdataioport, 0x04)
	PortÍrásbyte(Secondarypicdataioport, 0x02)

	PortÍrásbyte(Primarypicdataioport, 0x01)
	PortÍrásbyte(Secondarypicdataioport, 0x01)

	PortÍrásbyte(Primarypicdataioport, 0xF8)
	PortÍrásbyte(Secondarypicdataioport, 0xEF)

	idtMutató := [6]uint8{0, 0, 0, 0, 0, 0}
	méret := (*uint16)(Pointer(&idtMutató[0]))
	(*méret) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtMutató[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtMutató)))
}
func Lidt(lidtaddr uintptr)

func (self *TMegszakításmanager) MegszakításdescriptorTáblázatbejegyzéshalmaz(megszakítás int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTípus uint8) {

	handleraddressAlacsonybit := (*uint16)(Pointer(&idtdata[megszakítás*8+0]))
	(*handleraddressAlacsonybit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[megszakítás*8+2]))
	(*gdtcodesegmentselector) = codesegment

	fenntartva := (*uint8)(Pointer(&idtdata[megszakítás*8+4]))
	(*fenntartva) = 0

	var IdtdescriptorJelenvan uint8 = 0x80
	elérés := (*uint8)(Pointer(&idtdata[megszakítás*8+5]))
	(*elérés) = (IdtdescriptorJelenvan | DescriptorTípus | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressMagasbit := (*uint16)(Pointer(&idtdata[megszakítás*8+6]))
	(*handleraddressMagasbit) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TMegszakításmanager) Halmazhandler(handler uintptr, MegszakításSzám uint8) {
	handler_2[MegszakításSzám] = handler
}
func (self *TMegszakításmanager) Gethandler(MegszakításSzám uint8) uintptr {
	return handler_2[MegszakításSzám]
}
func (self *TMegszakításmanager) DoFogantyúMegszakítás(megszakítás uint8, esp uint32) uint32 {

	if megszakításHibakeresés {
		konzol_2.MNyomtatásxy("[esp:", 1, 20)
		konzol_2.MUnsignedinteger32Nyomtatás(uint32(megszakítás))
		konzol_2.MNyomtatás(":")
		konzol_2.MUnsignedinteger32Nyomtatás(esp)
	}
	handlerFuttatás := false
	if handler_2[megszakítás] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[megszakítás])))
		esp = myfunction(esp)
		handlerFuttatás = true

	}

	if !handlerFuttatás && megszakítás == uint8(self.hardverMegszakításEltolás) && self.feladatmanager != nil {
		esp = uint32(uintptr(Pointer(self.feladatmanager.Schedule((*TcpuÁllapot)(Pointer(uintptr(esp)))))))

	}
	if !handlerFuttatás && megszakítás == 0x80 {
		esp = fogantyúunhandledsyscall(esp)
	}

	if megszakítás <= 0x1F {
	}
	if 0x20 <= megszakítás && megszakítás < 0x30 {
		if 0x28 <= megszakítás {
			PortÍrásbyte(SecondarypicParancsioport, 0x20)
		}
		PortÍrásbyte(PrimarypicParancsioport, 0x20)
	}
	return esp
}

var számláló2 uint8 = 1

func halmazcr3(address uint32)

var konzol_2 TKonzol = TKonzol{}

func FogantyúMegszakítás(esp uint32, megszakítás uint32) uint32 {

	if megszakításHibakeresés && megszakítás != 0x80 && megszakítás != 0x20 {
		konzol_2.MNyomtatásxy("[esp:", 1, 21)
		konzol_2.MUnsignedinteger32Nyomtatás(uint32(megszakítás))
		konzol_2.MNyomtatás(":")
		konzol_2.MUnsignedinteger32Nyomtatás(esp)
	}

	if AktívMegszakításmanager != 0 {
		p := (*TMegszakításmanager)(Pointer(AktívMegszakításmanager))
		esp = p.DoFogantyúMegszakítás(uint8(megszakítás), esp)
		return esp
	}
	if handler_2[megszakítás] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[megszakítás])))
		esp = myfunction(esp)
	}
	if megszakítás == 0x80 {
		return fogantyúunhandledsyscall(esp)
	}
	if 0x20 <= megszakítás && megszakítás < 0x30 {
		if 0x28 <= megszakítás {
			PortÍrásbyte(SecondarypicParancsioport, 0x20)
		}
		PortÍrásbyte(PrimarypicParancsioport, 0x20)
	}

	return esp
}

func fogantyúunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuÁllapot)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(megszakításKilépésHurok).Pointer())
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

func exceptionHasDistrictHibacode(megszakítás uint32) bool {
	switch megszakítás {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNév(megszakítás uint32) string {
	switch megszakítás {
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

func exceptionKeretÉrték(keret uint32, eltolás uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(keret + eltolás)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func nyomtatásOldalfaultInfó(hiba uint32) {
	MEmergencylogKarakterlánc(" pf=[")
	if (hiba & 0x01) != 0 {
		MEmergencylogKarakterlánc("protection")
	} else {
		MEmergencylogKarakterlánc("not-present")
	}
	if (hiba & 0x02) != 0 {
		MEmergencylogKarakterlánc(",write")
	} else {
		MEmergencylogKarakterlánc(",read")
	}
	if (hiba & 0x04) != 0 {
		MEmergencylogKarakterlánc(",user")
	} else {
		MEmergencylogKarakterlánc(",kernel")
	}
	if (hiba & 0x08) != 0 {
		MEmergencylogKarakterlánc(",reserved-bit")
	}
	if (hiba & 0x10) != 0 {
		MEmergencylogKarakterlánc(",instruction-fetch")
	}
	MEmergencylogKarakterlánc("]")
}

func nyomtatásexceptionselectorInfó(hiba uint32) {
	MEmergencylogKarakterlánc(" selector=")
	MEmergencylogunsignedinteger32(hiba & 0xFFFFFFF8)
	MEmergencylogKarakterlánc(" index=")
	MEmergencylogunsignedinteger32(hiba >> 3)
	MEmergencylogKarakterlánc(" table=")
	if (hiba & 0x02) != 0 {
		MEmergencylogKarakterlánc("IDT")
	} else if (hiba & 0x04) != 0 {
		MEmergencylogKarakterlánc("LDT")
	} else {
		MEmergencylogKarakterlánc("GDT")
	}
	MEmergencylogKarakterlánc(" ext=")
	MEmergencylogunsignedinteger32(hiba & 0x01)
}

func Fogantyúexception(esp uint32, megszakítás uint32) uint32 {
	MEmergencylogKarakterlánc("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(megszakítás))
	MEmergencylogKarakterlánc(" ")
	MEmergencylogKarakterlánc(exceptionNév(megszakítás))
	MEmergencylogKarakterlánc(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogKarakterlánc(" invalid-frame")
		if exceptionHasDistrictHibacode(megszakítás) {
			MEmergencylogKarakterlánc(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			nyomtatásexceptionselectorInfó(esp)
		}
		MEmergencylogKarakterlánc("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var hiba uint32 = 0
	var eipEltolás uint32 = 0
	if exceptionHasDistrictHibacode(megszakítás) {
		hiba = exceptionKeretÉrték(esp, 0)
		eipEltolás = 4
	}
	eip := exceptionKeretÉrték(esp, eipEltolás)
	cs := exceptionKeretÉrték(esp, eipEltolás+4)
	eflags := exceptionKeretÉrték(esp, eipEltolás+8)

	MEmergencylogKarakterlánc(" err=")
	MEmergencylogunsignedinteger32(hiba)
	MEmergencylogKarakterlánc(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogKarakterlánc(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogKarakterlánc(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogKarakterlánc(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogKarakterlánc(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if megszakítás == 0x0E {
		MEmergencylogKarakterlánc(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		nyomtatásOldalfaultInfó(hiba)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogKarakterlánc(" useresp=")
		MEmergencylogunsignedinteger32(exceptionKeretÉrték(esp, eipEltolás+12))
		MEmergencylogKarakterlánc(" ss=")
		MEmergencylogunsignedinteger32(exceptionKeretÉrték(esp, eipEltolás+16))
	}

	if exceptionHasDistrictHibacode(megszakítás) {
		nyomtatásexceptionselectorInfó(hiba)
	}
	MEmergencylogKarakterlánc("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltUtánfatalexception()

func FogantyúfatalMegszakításKeret(mentettesp uint32, megszakítás uint32) uint32 {
	Fogantyúexception(mentettesp+52, megszakítás)
	haltUtánfatalexception()
	return mentettesp
}

func MegszakításAktív()
func (self *TMegszakításmanager) Aktív() {
	if AktívMegszakításmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	AktívMegszakításmanager = address
	MegszakításAktív()
}
func Megszakításdeactive()
func (self *TMegszakításmanager) Deactive() {
	AktívMegszakításmanager = 0
	Megszakításdeactive()
}

func MyFogantyúMegszakítás(megszakítás uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	konzol_2 := TKonzol{}
	konzol_2.MNyomtatás(buffer)
	return esp
}
func MyTeszt(megszakítás uint8, esp uint32)

func UnhandleMegszakítás() {
	buffer := []byte("unhandle interrupt\n")
	konzol_2 := TKonzol{}
	konzol_2.MNyomtatás(buffer)
}

func megszakításhandler_2(megszakítás uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	konzol_2 := TKonzol{}
	konzol_2.MNyomtatás(buffer)
	konzol_2.MHexadecimalNyomtatás(0x40)
	return esp
}
func nyomtatásesp(esp uint32) {
	konzol_2 := TKonzol{}
	konzol_2.MUnsignedinteger32Nyomtatásxy(esp, 20, 21)
}
func gettls() uint32
func Nyomtatástls() {

}
