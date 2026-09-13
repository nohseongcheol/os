package Interrupt

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func interruptignore()

func interruptexceptionhandler()
func interruptexceptionhandler0x00()
func interruptexceptionhandler0x01()
func interruptexceptionhandler0x02()
func interruptexceptionhandler0x03()
func interruptexceptionhandler0x04()
func interruptexceptionhandler0x05()
func interruptexceptionhandler0x06()
func interruptexceptionhandler0x07()
func interruptexceptionhandler0x08()
func interruptexceptionhandler0x09()
func interruptexceptionhandler0x0a()
func interruptexceptionhandler0x0b()
func interruptexceptionhandler0x0c()
func interruptexceptionhandler0x0d()
func interruptexceptionhandler0x0e()
func interruptexceptionhandler0x0f()
func interruptexceptionhandler0x10()
func interruptexceptionhandler0x11()
func interruptexceptionhandler0x12()
func interruptexceptionhandler0x13()

func interruptrequesthandler0x00()
func interruptrequesthandler0x01()
func interruptrequesthandler0x02()
func interruptrequesthandler0x03()
func interruptrequesthandler0x04()
func interruptrequesthandler0x05()
func interruptrequesthandler0x06()
func interruptrequesthandler0x07()
func interruptrequesthandler0x08()
func interruptrequesthandler0x09()
func interruptrequesthandler0x0a()
func interruptrequesthandler0x0b()
func interruptrequesthandler0x0c()
func interruptrequesthandler0x0d()
func interruptrequesthandler0x0e()
func interruptrequesthandler0x0f()

func interruptrequesthandler0x80()
func interruptrequesthandler0x81()
func interruptrequesthandler0x82()

func PrøvUdskriv(placering uint8, data uint8)
func satds(dssegment uint32)
func satgs(gssegment uint32)
func interruptAfslutLøkkekolonier()

type TInterrupthandler struct {
	InterruptTal		uint8
	Interruptmanager	uintptr
}
type IInterrupthandler interface {
	Håndtaginterrupt(uint32) uint32
}

func Nyinterrupthandler(Interruptmanager uintptr, InterruptTal uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.InterruptTal = InterruptTal
	interrupthandler_2.Interruptmanager = Interruptmanager
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (selv *TInterrupthandler) Init(InterruptTal uint8, Interruptmanager uintptr, funcaddress uintptr) {

	handler_2[InterruptTal] = funcaddress

	selv.InterruptTal = InterruptTal
	selv.Interruptmanager = Interruptmanager

}
func (selv *TInterrupthandler) SatHåndtaginterruptfuction(InterruptTal uint32, address uintptr) {
	handler_2[InterruptTal] = address
}
func (selv *TInterrupthandler) Destruer() {
	selvuintptr := uintptr(Pointer(selv))
	Interruptmanager := (*TInterruptmanager)(Pointer(selv.Interruptmanager))
	if selvuintptr == Interruptmanager.Gethandler(selv.InterruptTal) {
		Interruptmanager.Sathandler(0, selv.InterruptTal)
	}

}
func (selv *TInterrupthandler) Satinterruptmanager(Interruptmanager uintptr) {
}
func (selv *TInterrupthandler) SatinterruptTal(InterruptTal uint8) {
	selv.InterruptTal = InterruptTal
}
func (selv *TInterrupthandler) Håndtaginterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MUdskriv(buffer)
	return esp
}
func Håndtaginterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MUdskriv(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptorTabelMarkør struct {
}

var idtdata [256 * 8]uint8
var Aktivinterruptmanager uintptr = 0

const interruptFejlsøgning = false

type TInterruptmanager struct {
	handler_2	[256]uintptr

	udstyrinterruptForskydning	uint16

	opgavemanager	*TOpgavemanager
}

var PrimarypicKommandoioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicKommandoioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (selv *TInterruptmanager) Init(udstyrinterruptForskydning uint16, globaltdescriptorTabel *TShareddescriptorTabel, opgavemanager *TOpgavemanager) {

	selv.opgavemanager = opgavemanager

	selv.udstyrinterruptForskydning = udstyrinterruptForskydning
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var Idtinterruptgate uint8 = 0xE
	address = uint32(ValueOf(interruptignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
		selv.InterruptdescriptorTabelemnesat(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	selv.InterruptdescriptorTabelemnesat(0x82, codesegment, address, 3, Idtinterruptgate)

	PortSkrivebyte(PrimarypicKommandoioport, 0x11)
	PortSkrivebyte(SecondarypicKommandoioport, 0x11)

	PortSkrivebyte(Primarypicdataioport, 0x20)
	PortSkrivebyte(Secondarypicdataioport, 0x28)

	PortSkrivebyte(Primarypicdataioport, 0x04)
	PortSkrivebyte(Secondarypicdataioport, 0x02)

	PortSkrivebyte(Primarypicdataioport, 0x01)
	PortSkrivebyte(Secondarypicdataioport, 0x01)

	PortSkrivebyte(Primarypicdataioport, 0xF8)
	PortSkrivebyte(Secondarypicdataioport, 0xEF)

	idtMarkør := [6]uint8{0, 0, 0, 0, 0, 0}
	størrelse := (*uint16)(Pointer(&idtMarkør[0]))
	(*størrelse) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtMarkør[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtMarkør)))
}
func Lidt(lidtaddr uintptr)

func (selv *TInterruptmanager) InterruptdescriptorTabelemnesat(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptortype uint8) {

	handleraddressLavbit := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddressLavbit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserveret := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*reserveret) = 0

	var IdtdescriptorTilstedeværende uint8 = 0x80
	tilgå := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*tilgå) = (IdtdescriptorTilstedeværende | Descriptortype | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressHøjbit := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddressHøjbit) = uint16((handler >> 16) & 0xFFFF)

}

func (selv *TInterruptmanager) Sathandler(handler uintptr, InterruptTal uint8) {
	handler_2[InterruptTal] = handler
}
func (selv *TInterruptmanager) Gethandler(InterruptTal uint8) uintptr {
	return handler_2[InterruptTal]
}
func (selv *TInterruptmanager) DoHåndtaginterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptFejlsøgning {
		console_2.MUdskrivxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Udskriv(uint32(interrupt))
		console_2.MUdskriv(":")
		console_2.MUnsignedinteger32Udskriv(esp)
	}
	handlerKør := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerKør = true

	}

	if !handlerKør && interrupt == uint8(selv.udstyrinterruptForskydning) && selv.opgavemanager != nil {
		esp = uint32(uintptr(Pointer(selv.opgavemanager.Schedule((*TcpuStatus)(Pointer(uintptr(esp)))))))

	}
	if !handlerKør && interrupt == 0x80 {
		esp = håndtagunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortSkrivebyte(SecondarypicKommandoioport, 0x20)
		}
		PortSkrivebyte(PrimarypicKommandoioport, 0x20)
	}
	return esp
}

var antal2 uint8 = 1

func satcr3(address uint32)

var console_2 TConsole = TConsole{}

func Håndtaginterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptFejlsøgning && interrupt != 0x80 && interrupt != 0x20 {
		console_2.MUdskrivxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Udskriv(uint32(interrupt))
		console_2.MUdskriv(":")
		console_2.MUnsignedinteger32Udskriv(esp)
	}

	if Aktivinterruptmanager != 0 {
		p := (*TInterruptmanager)(Pointer(Aktivinterruptmanager))
		esp = p.DoHåndtaginterrupt(uint8(interrupt), esp)
		return esp
	}
	if handler_2[interrupt] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
	}
	if interrupt == 0x80 {
		return håndtagunhandledsyscall(esp)
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortSkrivebyte(SecondarypicKommandoioport, 0x20)
		}
		PortSkrivebyte(PrimarypicKommandoioport, 0x20)
	}

	return esp
}

func håndtagunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStatus)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptAfslutLøkkekolonier).Pointer())
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

func exceptionhasFejlcode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNavn(interrupt uint32) string {
	switch interrupt {
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

func exceptionRammeVærdi(ramme uint32, forskydning uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ramme + forskydning)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func udskrivSidefaultInformation(err uint32) {
	MEmergencylogStreng(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogStreng("protection")
	} else {
		MEmergencylogStreng("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogStreng(",write")
	} else {
		MEmergencylogStreng(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogStreng(",user")
	} else {
		MEmergencylogStreng(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogStreng(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogStreng(",instruction-fetch")
	}
	MEmergencylogStreng("]")
}

func udskrivexceptionselectorInformation(err uint32) {
	MEmergencylogStreng(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogStreng(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogStreng(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogStreng("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogStreng("LDT")
	} else {
		MEmergencylogStreng("GDT")
	}
	MEmergencylogStreng(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Håndtagexception(esp uint32, interrupt uint32) uint32 {
	MEmergencylogStreng("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(interrupt))
	MEmergencylogStreng(" ")
	MEmergencylogStreng(exceptionNavn(interrupt))
	MEmergencylogStreng(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogStreng(" invalid-frame")
		if exceptionhasFejlcode(interrupt) {
			MEmergencylogStreng(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			udskrivexceptionselectorInformation(esp)
		}
		MEmergencylogStreng("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipForskydning uint32 = 0
	if exceptionhasFejlcode(interrupt) {
		err = exceptionRammeVærdi(esp, 0)
		eipForskydning = 4
	}
	eip := exceptionRammeVærdi(esp, eipForskydning)
	cs := exceptionRammeVærdi(esp, eipForskydning+4)
	eflags := exceptionRammeVærdi(esp, eipForskydning+8)

	MEmergencylogStreng(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogStreng(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogStreng(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogStreng(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogStreng(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogStreng(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencylogStreng(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		udskrivSidefaultInformation(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogStreng(" useresp=")
		MEmergencylogunsignedinteger32(exceptionRammeVærdi(esp, eipForskydning+12))
		MEmergencylogStreng(" ss=")
		MEmergencylogunsignedinteger32(exceptionRammeVærdi(esp, eipForskydning+16))
	}

	if exceptionhasFejlcode(interrupt) {
		udskrivexceptionselectorInformation(err)
	}
	MEmergencylogStreng("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltEfterfatalexception()

func HåndtagfatalinterruptRamme(gemtesp uint32, interrupt uint32) uint32 {
	Håndtagexception(gemtesp+52, interrupt)
	haltEfterfatalexception()
	return gemtesp
}

func InterruptAktiv()
func (selv *TInterruptmanager) Aktiv() {
	if Aktivinterruptmanager != 0 {
		selv.Deactive()
	}
	address := uintptr(Pointer(selv))
	Aktivinterruptmanager = address
	InterruptAktiv()
}
func Interruptdeactive()
func (selv *TInterruptmanager) Deactive() {
	Aktivinterruptmanager = 0
	Interruptdeactive()
}

func MyHåndtaginterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MUdskriv(buffer)
	return esp
}
func MyPrøv(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MUdskriv(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MUdskriv(buffer)
	console_2.MHexadecimalUdskriv(0x40)
	return esp
}
func udskrivesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Udskrivxy(esp, 20, 21)
}
func gettls() uint32
func Udskrivtls() {

}
