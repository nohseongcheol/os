package Intrerupere

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func intrerupereignore()

func intrerupereexceptionhandler()
func intrerupereexceptionhandler0x00()
func intrerupereexceptionhandler0x01()
func intrerupereexceptionhandler0x02()
func intrerupereexceptionhandler0x03()
func intrerupereexceptionhandler0x04()
func intrerupereexceptionhandler0x05()
func intrerupereexceptionhandler0x06()
func intrerupereexceptionhandler0x07()
func intrerupereexceptionhandler0x08()
func intrerupereexceptionhandler0x09()
func intrerupereexceptionhandler0x0a()
func intrerupereexceptionhandler0x0b()
func intrerupereexceptionhandler0x0c()
func intrerupereexceptionhandler0x0d()
func intrerupereexceptionhandler0x0e()
func intrerupereexceptionhandler0x0f()
func intrerupereexceptionhandler0x10()
func intrerupereexceptionhandler0x11()
func intrerupereexceptionhandler0x12()
func intrerupereexceptionhandler0x13()

func intrerupererequesthandler0x00()
func intrerupererequesthandler0x01()
func intrerupererequesthandler0x02()
func intrerupererequesthandler0x03()
func intrerupererequesthandler0x04()
func intrerupererequesthandler0x05()
func intrerupererequesthandler0x06()
func intrerupererequesthandler0x07()
func intrerupererequesthandler0x08()
func intrerupererequesthandler0x09()
func intrerupererequesthandler0x0a()
func intrerupererequesthandler0x0b()
func intrerupererequesthandler0x0c()
func intrerupererequesthandler0x0d()
func intrerupererequesthandler0x0e()
func intrerupererequesthandler0x0f()

func intrerupererequesthandler0x80()
func intrerupererequesthandler0x81()
func intrerupererequesthandler0x82()

func TesteazăTipărește(poziție uint8, data uint8)
func definitds(dssegment uint32)
func definitgs(gssegment uint32)
func intrerupereIeșireloop()

type TIntreruperehandler struct {
	IntrerupereNumăr	uint8
	Intreruperemanager	uintptr
}
type IIntreruperehandler interface {
	MânerIntrerupere(uint32) uint32
}

func NouIntreruperehandler(Intreruperemanager uintptr, IntrerupereNumăr uint8) *TIntreruperehandler {
	intreruperehandler_2 := new(TIntreruperehandler)
	intreruperehandler_2.IntrerupereNumăr = IntrerupereNumăr
	intreruperehandler_2.Intreruperemanager = Intreruperemanager
	return intreruperehandler_2

}

var handler_2 [256]uintptr

func (sine *TIntreruperehandler) Init(IntrerupereNumăr uint8, Intreruperemanager uintptr, funcaddress uintptr) {

	handler_2[IntrerupereNumăr] = funcaddress

	sine.IntrerupereNumăr = IntrerupereNumăr
	sine.Intreruperemanager = Intreruperemanager

}
func (sine *TIntreruperehandler) DefinitMânerIntreruperefuction(IntrerupereNumăr uint32, address uintptr) {
	handler_2[IntrerupereNumăr] = address
}
func (sine *TIntreruperehandler) Distruge() {
	sineuintptr := uintptr(Pointer(sine))
	Intreruperemanager := (*TIntreruperemanager)(Pointer(sine.Intreruperemanager))
	if sineuintptr == Intreruperemanager.Gethandler(sine.IntrerupereNumăr) {
		Intreruperemanager.Definithandler(0, sine.IntrerupereNumăr)
	}

}
func (sine *TIntreruperehandler) DefinitIntreruperemanager(Intreruperemanager uintptr) {
}
func (sine *TIntreruperehandler) DefinitIntrerupereNumăr(IntrerupereNumăr uint8) {
	sine.IntrerupereNumăr = IntrerupereNumăr
}
func (sine *TIntreruperehandler) MânerIntrerupere(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MTipărește(buffer)
	return esp
}
func MânerIntrerupere1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MTipărește(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TIntreruperedescriptorTabelIndicator struct {
}

var idtdata [256 * 8]uint8
var ActivIntreruperemanager uintptr = 0

const intrerupereDepanează = false

type TIntreruperemanager struct {
	handler_2	[256]uintptr

	componenteIntrerupereoffset	uint16

	taskmanager	*TTaskmanager
}

var PrimarypicComandăioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicComandăioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (sine *TIntreruperemanager) Init(componenteIntrerupereoffset uint16, globaldescriptorTabel *TShareddescriptorTabel, taskmanager *TTaskmanager) {

	sine.taskmanager = taskmanager

	sine.componenteIntrerupereoffset = componenteIntrerupereoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtIntreruperegate uint8 = 0xE
	address = uint32(ValueOf(intrerupereignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(intrerupereexceptionhandler0x0f).Pointer())
		sine.IntreruperedescriptorTabelînregistraredefinit(i, codesegment, address, 0, IdtIntreruperegate)
	}

	address = uint32(ValueOf(intrerupereexceptionhandler0x00).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x00, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x01).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x01, codesegment, address, 0, IdtIntreruperegate)
	address = uint32(ValueOf(intrerupereexceptionhandler0x02).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x02, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x03).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x03, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x04).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x04, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x05).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x05, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x06).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x06, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x07).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x07, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x08).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x08, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x09).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x09, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x0a).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x0A, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x0b).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x0B, codesegment, address, 0, IdtIntreruperegate)
	address = uint32(ValueOf(intrerupereexceptionhandler0x0c).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x0C, codesegment, address, 0, IdtIntreruperegate)
	address = uint32(ValueOf(intrerupereexceptionhandler0x0d).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x0D, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x0e).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x0E, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x0f).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x0F, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x10).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x10, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x11).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x11, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x12).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x12, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupereexceptionhandler0x13).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x13, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x00).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x20, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x01).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x21, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x02).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x22, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x03).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x23, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x04).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x24, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x05).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x25, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x06).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x26, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x07).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x27, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x08).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x28, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x09).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x29, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x0a).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x2A, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x0b).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x2B, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x0c).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x2C, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x0d).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x2D, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x0e).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x2E, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x0f).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x2F, codesegment, address, 0, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x80).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x80, codesegment, address, 3, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x81).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x81, codesegment, address, 3, IdtIntreruperegate)

	address = uint32(ValueOf(intrerupererequesthandler0x82).Pointer())
	sine.IntreruperedescriptorTabelînregistraredefinit(0x82, codesegment, address, 3, IdtIntreruperegate)

	PortScrierebyte(PrimarypicComandăioport, 0x11)
	PortScrierebyte(SecondarypicComandăioport, 0x11)

	PortScrierebyte(Primarypicdataioport, 0x20)
	PortScrierebyte(Secondarypicdataioport, 0x28)

	PortScrierebyte(Primarypicdataioport, 0x04)
	PortScrierebyte(Secondarypicdataioport, 0x02)

	PortScrierebyte(Primarypicdataioport, 0x01)
	PortScrierebyte(Secondarypicdataioport, 0x01)

	PortScrierebyte(Primarypicdataioport, 0xF8)
	PortScrierebyte(Secondarypicdataioport, 0xEF)

	idtIndicator := [6]uint8{0, 0, 0, 0, 0, 0}
	mărime := (*uint16)(Pointer(&idtIndicator[0]))
	(*mărime) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtIndicator[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtIndicator)))
}
func Lidt(lidtaddr uintptr)

func (sine *TIntreruperemanager) IntreruperedescriptorTabelînregistraredefinit(intrerupere int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTip uint8) {

	handleraddressScăzutăbiți := (*uint16)(Pointer(&idtdata[intrerupere*8+0]))
	(*handleraddressScăzutăbiți) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[intrerupere*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[intrerupere*8+4]))
	(*reserved) = 0

	var IdtdescriptorPrezent uint8 = 0x80
	acces := (*uint8)(Pointer(&idtdata[intrerupere*8+5]))
	(*acces) = (IdtdescriptorPrezent | DescriptorTip | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressRidicatăbiți := (*uint16)(Pointer(&idtdata[intrerupere*8+6]))
	(*handleraddressRidicatăbiți) = uint16((handler >> 16) & 0xFFFF)

}

func (sine *TIntreruperemanager) Definithandler(handler uintptr, IntrerupereNumăr uint8) {
	handler_2[IntrerupereNumăr] = handler
}
func (sine *TIntreruperemanager) Gethandler(IntrerupereNumăr uint8) uintptr {
	return handler_2[IntrerupereNumăr]
}
func (sine *TIntreruperemanager) DoMânerIntrerupere(intrerupere uint8, esp uint32) uint32 {

	if intrerupereDepanează {
		console_2.MTipăreștexy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Tipărește(uint32(intrerupere))
		console_2.MTipărește(":")
		console_2.MUnsignedinteger32Tipărește(esp)
	}
	handlerRulează := false
	if handler_2[intrerupere] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[intrerupere])))
		esp = myfunction(esp)
		handlerRulează = true

	}

	if !handlerRulează && intrerupere == uint8(sine.componenteIntrerupereoffset) && sine.taskmanager != nil {
		esp = uint32(uintptr(Pointer(sine.taskmanager.Schedule((*TcpuStare)(Pointer(uintptr(esp)))))))

	}
	if !handlerRulează && intrerupere == 0x80 {
		esp = mânerunhandledsyscall(esp)
	}

	if intrerupere <= 0x1F {
	}
	if 0x20 <= intrerupere && intrerupere < 0x30 {
		if 0x28 <= intrerupere {
			PortScrierebyte(SecondarypicComandăioport, 0x20)
		}
		PortScrierebyte(PrimarypicComandăioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func definitcr3(address uint32)

var console_2 TConsole = TConsole{}

func MânerIntrerupere(esp uint32, intrerupere uint32) uint32 {

	if intrerupereDepanează && intrerupere != 0x80 && intrerupere != 0x20 {
		console_2.MTipăreștexy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Tipărește(uint32(intrerupere))
		console_2.MTipărește(":")
		console_2.MUnsignedinteger32Tipărește(esp)
	}

	if ActivIntreruperemanager != 0 {
		p := (*TIntreruperemanager)(Pointer(ActivIntreruperemanager))
		esp = p.DoMânerIntrerupere(uint8(intrerupere), esp)
		return esp
	}
	if handler_2[intrerupere] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[intrerupere])))
		esp = myfunction(esp)
	}
	if intrerupere == 0x80 {
		return mânerunhandledsyscall(esp)
	}
	if 0x20 <= intrerupere && intrerupere < 0x30 {
		if 0x28 <= intrerupere {
			PortScrierebyte(SecondarypicComandăioport, 0x20)
		}
		PortScrierebyte(PrimarypicComandăioport, 0x20)
	}

	return esp
}

func mânerunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStare)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(intrerupereIeșireloop).Pointer())
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

func exceptionhasEroarecode(intrerupere uint32) bool {
	switch intrerupere {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNume(intrerupere uint32) string {
	switch intrerupere {
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

func exceptionCadruValoare(cadru uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(cadru + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func tipăreștePAGINĂfaultDetaliat(erori uint32) {
	MEmergencylogȘir(" pf=[")
	if (erori & 0x01) != 0 {
		MEmergencylogȘir("protection")
	} else {
		MEmergencylogȘir("not-present")
	}
	if (erori & 0x02) != 0 {
		MEmergencylogȘir(",write")
	} else {
		MEmergencylogȘir(",read")
	}
	if (erori & 0x04) != 0 {
		MEmergencylogȘir(",user")
	} else {
		MEmergencylogȘir(",kernel")
	}
	if (erori & 0x08) != 0 {
		MEmergencylogȘir(",reserved-bit")
	}
	if (erori & 0x10) != 0 {
		MEmergencylogȘir(",instruction-fetch")
	}
	MEmergencylogȘir("]")
}

func tipăreșteexceptionselectorDetaliat(erori uint32) {
	MEmergencylogȘir(" selector=")
	MEmergencylogunsignedinteger32(erori & 0xFFFFFFF8)
	MEmergencylogȘir(" index=")
	MEmergencylogunsignedinteger32(erori >> 3)
	MEmergencylogȘir(" table=")
	if (erori & 0x02) != 0 {
		MEmergencylogȘir("IDT")
	} else if (erori & 0x04) != 0 {
		MEmergencylogȘir("LDT")
	} else {
		MEmergencylogȘir("GDT")
	}
	MEmergencylogȘir(" ext=")
	MEmergencylogunsignedinteger32(erori & 0x01)
}

func Mânerexception(esp uint32, intrerupere uint32) uint32 {
	MEmergencylogȘir("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(intrerupere))
	MEmergencylogȘir(" ")
	MEmergencylogȘir(exceptionNume(intrerupere))
	MEmergencylogȘir(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogȘir(" invalid-frame")
		if exceptionhasEroarecode(intrerupere) {
			MEmergencylogȘir(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			tipăreșteexceptionselectorDetaliat(esp)
		}
		MEmergencylogȘir("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var erori uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasEroarecode(intrerupere) {
		erori = exceptionCadruValoare(esp, 0)
		eipoffset = 4
	}
	eip := exceptionCadruValoare(esp, eipoffset)
	cs := exceptionCadruValoare(esp, eipoffset+4)
	eflags := exceptionCadruValoare(esp, eipoffset+8)

	MEmergencylogȘir(" err=")
	MEmergencylogunsignedinteger32(erori)
	MEmergencylogȘir(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogȘir(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogȘir(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogȘir(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogȘir(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if intrerupere == 0x0E {
		MEmergencylogȘir(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		tipăreștePAGINĂfaultDetaliat(erori)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogȘir(" useresp=")
		MEmergencylogunsignedinteger32(exceptionCadruValoare(esp, eipoffset+12))
		MEmergencylogȘir(" ss=")
		MEmergencylogunsignedinteger32(exceptionCadruValoare(esp, eipoffset+16))
	}

	if exceptionhasEroarecode(intrerupere) {
		tipăreșteexceptionselectorDetaliat(erori)
	}
	MEmergencylogȘir("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func MânerfatalIntrerupereCadru(savedesp uint32, intrerupere uint32) uint32 {
	Mânerexception(savedesp+52, intrerupere)
	haltafterfatalexception()
	return savedesp
}

func IntrerupereActiv()
func (sine *TIntreruperemanager) Activ() {
	if ActivIntreruperemanager != 0 {
		sine.Deactive()
	}
	address := uintptr(Pointer(sine))
	ActivIntreruperemanager = address
	IntrerupereActiv()
}
func Intreruperedeactive()
func (sine *TIntreruperemanager) Deactive() {
	ActivIntreruperemanager = 0
	Intreruperedeactive()
}

func MyMânerIntrerupere(intrerupere uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MTipărește(buffer)
	return esp
}
func MyTestează(intrerupere uint8, esp uint32)

func UnhandleIntrerupere() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MTipărește(buffer)
}

func intreruperehandler_2(intrerupere uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MTipărește(buffer)
	console_2.MHexadecimalTipărește(0x40)
	return esp
}
func tipăreșteesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Tipăreștexy(esp, 20, 21)
}
func gettls() uint32
func Tipăreștetls() {

}
