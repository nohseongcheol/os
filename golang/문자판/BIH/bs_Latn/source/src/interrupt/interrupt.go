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

func TestŠtampaj(položaj uint8, data uint8)
func skupds(dssegment uint32)
func skupgs(gssegment uint32)
func interruptIzlazloop()

type TInterrupthandler struct {
	InterruptBroj		uint8
	Interruptmanager	uintptr
}
type IInterrupthandler interface {
	Handleinterrupt(uint32) uint32
}

func Novainterrupthandler(Interruptmanager uintptr, InterruptBroj uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.InterruptBroj = InterruptBroj
	interrupthandler_2.Interruptmanager = Interruptmanager
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (self *TInterrupthandler) Init(InterruptBroj uint8, Interruptmanager uintptr, funcaddress uintptr) {

	handler_2[InterruptBroj] = funcaddress

	self.InterruptBroj = InterruptBroj
	self.Interruptmanager = Interruptmanager

}
func (self *TInterrupthandler) Skuphandleinterruptfuction(InterruptBroj uint32, address uintptr) {
	handler_2[InterruptBroj] = address
}
func (self *TInterrupthandler) Destroy() {
	selfuintptr := uintptr(Pointer(self))
	Interruptmanager := (*TInterruptmanager)(Pointer(self.Interruptmanager))
	if selfuintptr == Interruptmanager.Gethandler(self.InterruptBroj) {
		Interruptmanager.Skuphandler(0, self.InterruptBroj)
	}

}
func (self *TInterrupthandler) Skupinterruptmanager(Interruptmanager uintptr) {
}
func (self *TInterrupthandler) SkupinterruptBroj(InterruptBroj uint8) {
	self.InterruptBroj = InterruptBroj
}
func (self *TInterrupthandler) Handleinterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MŠtampaj(buffer)
	return esp
}
func Handleinterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MŠtampaj(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptortablepointer struct {
}

var idtdata [256 * 8]uint8
var Activeinterruptmanager uintptr = 0

const interruptIspravljanje = false

type TInterruptmanager struct {
	handler_2	[256]uintptr

	hardverinterruptoffset	uint16

	taskmanager	*TTaskmanager
}

var PrimarypicNaredbaioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicNaredbaioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (self *TInterruptmanager) Init(hardverinterruptoffset uint16, globalnadescriptortable *TShareddescriptortable, taskmanager *TTaskmanager) {

	self.taskmanager = taskmanager

	self.hardverinterruptoffset = hardverinterruptoffset
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
		self.Interruptdescriptortableunosskup(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	self.Interruptdescriptortableunosskup(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	self.Interruptdescriptortableunosskup(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	self.Interruptdescriptortableunosskup(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	self.Interruptdescriptortableunosskup(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	self.Interruptdescriptortableunosskup(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	self.Interruptdescriptortableunosskup(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	self.Interruptdescriptortableunosskup(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	self.Interruptdescriptortableunosskup(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	self.Interruptdescriptortableunosskup(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	self.Interruptdescriptortableunosskup(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	self.Interruptdescriptortableunosskup(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	self.Interruptdescriptortableunosskup(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	self.Interruptdescriptortableunosskup(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	self.Interruptdescriptortableunosskup(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	self.Interruptdescriptortableunosskup(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	self.Interruptdescriptortableunosskup(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	self.Interruptdescriptortableunosskup(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	self.Interruptdescriptortableunosskup(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	self.Interruptdescriptortableunosskup(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	self.Interruptdescriptortableunosskup(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	self.Interruptdescriptortableunosskup(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	self.Interruptdescriptortableunosskup(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	self.Interruptdescriptortableunosskup(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	self.Interruptdescriptortableunosskup(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	self.Interruptdescriptortableunosskup(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	self.Interruptdescriptortableunosskup(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	self.Interruptdescriptortableunosskup(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	self.Interruptdescriptortableunosskup(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	self.Interruptdescriptortableunosskup(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	self.Interruptdescriptortableunosskup(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	self.Interruptdescriptortableunosskup(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	self.Interruptdescriptortableunosskup(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	self.Interruptdescriptortableunosskup(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	self.Interruptdescriptortableunosskup(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	self.Interruptdescriptortableunosskup(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	self.Interruptdescriptortableunosskup(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	self.Interruptdescriptortableunosskup(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	self.Interruptdescriptortableunosskup(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	self.Interruptdescriptortableunosskup(0x82, codesegment, address, 3, Idtinterruptgate)

	PortPišibyte(PrimarypicNaredbaioport, 0x11)
	PortPišibyte(SecondarypicNaredbaioport, 0x11)

	PortPišibyte(Primarypicdataioport, 0x20)
	PortPišibyte(Secondarypicdataioport, 0x28)

	PortPišibyte(Primarypicdataioport, 0x04)
	PortPišibyte(Secondarypicdataioport, 0x02)

	PortPišibyte(Primarypicdataioport, 0x01)
	PortPišibyte(Secondarypicdataioport, 0x01)

	PortPišibyte(Primarypicdataioport, 0xF8)
	PortPišibyte(Secondarypicdataioport, 0xEF)

	idtpointer := [6]uint8{0, 0, 0, 0, 0, 0}
	veličina := (*uint16)(Pointer(&idtpointer[0]))
	(*veličina) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtpointer[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtpointer)))
}
func Lidt(lidtaddr uintptr)

func (self *TInterruptmanager) Interruptdescriptortableunosskup(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTip uint8) {

	handleraddresslowbits := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddresslowbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*reserved) = 0

	var Idtdescriptorpresent uint8 = 0x80
	access := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*access) = (Idtdescriptorpresent | DescriptorTip | ((Descriptorprivilegelevel & 3) << 5))

	handleraddresshighbits := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddresshighbits) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TInterruptmanager) Skuphandler(handler uintptr, InterruptBroj uint8) {
	handler_2[InterruptBroj] = handler
}
func (self *TInterruptmanager) Gethandler(InterruptBroj uint8) uintptr {
	return handler_2[InterruptBroj]
}
func (self *TInterruptmanager) Dohandleinterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptIspravljanje {
		console_2.MŠtampajxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Štampaj(uint32(interrupt))
		console_2.MŠtampaj(":")
		console_2.MUnsignedinteger32Štampaj(esp)
	}
	handlerPokreni := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerPokreni = true

	}

	if !handlerPokreni && interrupt == uint8(self.hardverinterruptoffset) && self.taskmanager != nil {
		esp = uint32(uintptr(Pointer(self.taskmanager.Schedule((*Tcpustate)(Pointer(uintptr(esp)))))))

	}
	if !handlerPokreni && interrupt == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortPišibyte(SecondarypicNaredbaioport, 0x20)
		}
		PortPišibyte(PrimarypicNaredbaioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func skupcr3(address uint32)

var console_2 TConsole = TConsole{}

func Handleinterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptIspravljanje && interrupt != 0x80 && interrupt != 0x20 {
		console_2.MŠtampajxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Štampaj(uint32(interrupt))
		console_2.MŠtampaj(":")
		console_2.MUnsignedinteger32Štampaj(esp)
	}

	if Activeinterruptmanager != 0 {
		p := (*TInterruptmanager)(Pointer(Activeinterruptmanager))
		esp = p.Dohandleinterrupt(uint8(interrupt), esp)
		return esp
	}
	if handler_2[interrupt] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
	}
	if interrupt == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortPišibyte(SecondarypicNaredbaioport, 0x20)
		}
		PortPišibyte(PrimarypicNaredbaioport, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpustate)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptIzlazloop).Pointer())
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

func exceptionhasGreškacode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNaziv(interrupt uint32) string {
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

func exceptionOkvirVrijednost(okvir uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(okvir + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func štampajStranicafaultinfo(err uint32) {
	MEmergencylogNIZ(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogNIZ("protection")
	} else {
		MEmergencylogNIZ("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogNIZ(",write")
	} else {
		MEmergencylogNIZ(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogNIZ(",user")
	} else {
		MEmergencylogNIZ(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogNIZ(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogNIZ(",instruction-fetch")
	}
	MEmergencylogNIZ("]")
}

func štampajexceptionselectorinfo(err uint32) {
	MEmergencylogNIZ(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogNIZ(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogNIZ(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogNIZ("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogNIZ("LDT")
	} else {
		MEmergencylogNIZ("GDT")
	}
	MEmergencylogNIZ(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, interrupt uint32) uint32 {
	MEmergencylogNIZ("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(interrupt))
	MEmergencylogNIZ(" ")
	MEmergencylogNIZ(exceptionNaziv(interrupt))
	MEmergencylogNIZ(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogNIZ(" invalid-frame")
		if exceptionhasGreškacode(interrupt) {
			MEmergencylogNIZ(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			štampajexceptionselectorinfo(esp)
		}
		MEmergencylogNIZ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasGreškacode(interrupt) {
		err = exceptionOkvirVrijednost(esp, 0)
		eipoffset = 4
	}
	eip := exceptionOkvirVrijednost(esp, eipoffset)
	cs := exceptionOkvirVrijednost(esp, eipoffset+4)
	eflags := exceptionOkvirVrijednost(esp, eipoffset+8)

	MEmergencylogNIZ(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogNIZ(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogNIZ(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogNIZ(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogNIZ(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogNIZ(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencylogNIZ(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		štampajStranicafaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogNIZ(" useresp=")
		MEmergencylogunsignedinteger32(exceptionOkvirVrijednost(esp, eipoffset+12))
		MEmergencylogNIZ(" ss=")
		MEmergencylogunsignedinteger32(exceptionOkvirVrijednost(esp, eipoffset+16))
	}

	if exceptionhasGreškacode(interrupt) {
		štampajexceptionselectorinfo(err)
	}
	MEmergencylogNIZ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandlefatalinterruptOkvir(savedesp uint32, interrupt uint32) uint32 {
	Handleexception(savedesp+52, interrupt)
	haltafterfatalexception()
	return savedesp
}

func Interruptactive()
func (self *TInterruptmanager) Active() {
	if Activeinterruptmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	Activeinterruptmanager = address
	Interruptactive()
}
func Interruptdeactive()
func (self *TInterruptmanager) Deactive() {
	Activeinterruptmanager = 0
	Interruptdeactive()
}

func Myhandleinterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MŠtampaj(buffer)
	return esp
}
func Mytest(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MŠtampaj(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MŠtampaj(buffer)
	console_2.MHexadecimalŠtampaj(0x40)
	return esp
}
func štampajesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Štampajxy(esp, 20, 21)
}
func gettls() uint32
func Štampajtls() {

}
