package Interrupt

import . "unsafe"
import . "reflect"

import . "порт"
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

func ТекшерүүБасма(турганжери uint8, data uint8)
func setds(dssegment uint32)
func setgs(gssegment uint32)
func interruptexitloop()

type TInterrupthandler struct {
	InterruptНОМЕР		uint8
	Interruptmanager	uintptr
}
type IInterrupthandler interface {
	Handleinterrupt(uint32) uint32
}

func Жаңыinterrupthandler(Interruptmanager uintptr, InterruptНОМЕР uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.InterruptНОМЕР = InterruptНОМЕР
	interrupthandler_2.Interruptmanager = Interruptmanager
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (self *TInterrupthandler) Init(InterruptНОМЕР uint8, Interruptmanager uintptr, funcaddress uintptr) {

	handler_2[InterruptНОМЕР] = funcaddress

	self.InterruptНОМЕР = InterruptНОМЕР
	self.Interruptmanager = Interruptmanager

}
func (self *TInterrupthandler) Sethandleinterruptfuction(InterruptНОМЕР uint32, address uintptr) {
	handler_2[InterruptНОМЕР] = address
}
func (self *TInterrupthandler) Destroy() {
	selfuintptr := uintptr(Pointer(self))
	Interruptmanager := (*TInterruptmanager)(Pointer(self.Interruptmanager))
	if selfuintptr == Interruptmanager.Gethandler(self.InterruptНОМЕР) {
		Interruptmanager.Sethandler(0, self.InterruptНОМЕР)
	}

}
func (self *TInterrupthandler) Setinterruptmanager(Interruptmanager uintptr) {
}
func (self *TInterrupthandler) SetinterruptНОМЕР(InterruptНОМЕР uint8) {
	self.InterruptНОМЕР = InterruptНОМЕР
}
func (self *TInterrupthandler) Handleinterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MБасма(buffer)
	return esp
}
func Handleinterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MБасма(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptorЖадыбалКөрсөткүч struct {
}

var idtdata [256 * 8]uint8
var Активдүүinterruptmanager uintptr = 0

const interruptdebug = false

type TInterruptmanager struct {
	handler_2	[256]uintptr

	жабдууларinterruptoffset	uint16

	taskmanager	*TTaskmanager
}

var PrimarypicКомандаioПорт uint16 = 0x20
var PrimarypicdataioПорт uint16 = 0x21
var SecondarypicКомандаioПорт uint16 = 0xA0
var SecondarypicdataioПорт uint16 = 0xA1

func (self *TInterruptmanager) Init(жабдууларinterruptoffset uint16, globaldescriptorЖадыбал *TShareddescriptorЖадыбал, taskmanager *TTaskmanager) {

	self.taskmanager = taskmanager

	self.жабдууларinterruptoffset = жабдууларinterruptoffset
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
		self.InterruptdescriptorЖадыбалentryset(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	self.InterruptdescriptorЖадыбалentryset(0x82, codesegment, address, 3, Idtinterruptgate)

	ПортЖазууbyte(PrimarypicКомандаioПорт, 0x11)
	ПортЖазууbyte(SecondarypicКомандаioПорт, 0x11)

	ПортЖазууbyte(PrimarypicdataioПорт, 0x20)
	ПортЖазууbyte(SecondarypicdataioПорт, 0x28)

	ПортЖазууbyte(PrimarypicdataioПорт, 0x04)
	ПортЖазууbyte(SecondarypicdataioПорт, 0x02)

	ПортЖазууbyte(PrimarypicdataioПорт, 0x01)
	ПортЖазууbyte(SecondarypicdataioПорт, 0x01)

	ПортЖазууbyte(PrimarypicdataioПорт, 0xF8)
	ПортЖазууbyte(SecondarypicdataioПорт, 0xEF)

	idtКөрсөткүч := [6]uint8{0, 0, 0, 0, 0, 0}
	өлчөм := (*uint16)(Pointer(&idtКөрсөткүч[0]))
	(*өлчөм) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtКөрсөткүч[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtКөрсөткүч)))
}
func Lidt(lidtaddr uintptr)

func (self *TInterruptmanager) InterruptdescriptorЖадыбалentryset(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorТүрү uint8) {

	handleraddresslowbits := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddresslowbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*reserved) = 0

	var Idtdescriptorpresent uint8 = 0x80
	кирүү := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*кирүү) = (Idtdescriptorpresent | DescriptorТүрү | ((Descriptorprivilegelevel & 3) << 5))

	handleraddresshighbits := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddresshighbits) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TInterruptmanager) Sethandler(handler uintptr, InterruptНОМЕР uint8) {
	handler_2[InterruptНОМЕР] = handler
}
func (self *TInterruptmanager) Gethandler(InterruptНОМЕР uint8) uintptr {
	return handler_2[InterruptНОМЕР]
}
func (self *TInterruptmanager) Dohandleinterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptdebug {
		console_2.MБасмаxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Басма(uint32(interrupt))
		console_2.MБасма(":")
		console_2.MUnsignedinteger32Басма(esp)
	}
	handlerЖүргүзүү := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerЖүргүзүү = true

	}

	if !handlerЖүргүзүү && interrupt == uint8(self.жабдууларinterruptoffset) && self.taskmanager != nil {
		esp = uint32(uintptr(Pointer(self.taskmanager.Schedule((*TcpuАбал)(Pointer(uintptr(esp)))))))

	}
	if !handlerЖүргүзүү && interrupt == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			ПортЖазууbyte(SecondarypicКомандаioПорт, 0x20)
		}
		ПортЖазууbyte(PrimarypicКомандаioПорт, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func setcr3(address uint32)

var console_2 TConsole = TConsole{}

func Handleinterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptdebug && interrupt != 0x80 && interrupt != 0x20 {
		console_2.MБасмаxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Басма(uint32(interrupt))
		console_2.MБасма(":")
		console_2.MUnsignedinteger32Басма(esp)
	}

	if Активдүүinterruptmanager != 0 {
		p := (*TInterruptmanager)(Pointer(Активдүүinterruptmanager))
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
			ПортЖазууbyte(SecondarypicКомандаioПорт, 0x20)
		}
		ПортЖазууbyte(PrimarypicКомандаioПорт, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	бП := (*TcpuАбал)(Pointer(uintptr(esp)))
	if бП.Eax == 1 || бП.Eax == 252 {
		бП.Eip = uint32(ValueOf(interruptexitloop).Pointer())
		бП.Cs = Segkernelcode
		бП.Ds = Segkerneldata
		бП.Es = Segkerneldata
		бП.Fs = Segkerneldata
		бП.Gs = Segkernelgs
		бП.Ss = Segkerneldata
		бП.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasКатаcode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionАты(interrupt uint32) string {
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

func exceptionframeМааниси(frame uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(frame + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func басмаБАРАКfaultinfo(err uint32) {
	MEmergencylogСАП(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogСАП("protection")
	} else {
		MEmergencylogСАП("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogСАП(",write")
	} else {
		MEmergencylogСАП(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogСАП(",user")
	} else {
		MEmergencylogСАП(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogСАП(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogСАП(",instruction-fetch")
	}
	MEmergencylogСАП("]")
}

func басмаexceptionselectorinfo(err uint32) {
	MEmergencylogСАП(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogСАП(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogСАП(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogСАП("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogСАП("LDT")
	} else {
		MEmergencylogСАП("GDT")
	}
	MEmergencylogСАП(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, interrupt uint32) uint32 {
	MEmergencylogСАП("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(interrupt))
	MEmergencylogСАП(" ")
	MEmergencylogСАП(exceptionАты(interrupt))
	MEmergencylogСАП(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogСАП(" invalid-frame")
		if exceptionhasКатаcode(interrupt) {
			MEmergencylogСАП(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			басмаexceptionselectorinfo(esp)
		}
		MEmergencylogСАП("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasКатаcode(interrupt) {
		err = exceptionframeМааниси(esp, 0)
		eipoffset = 4
	}
	eip := exceptionframeМааниси(esp, eipoffset)
	cs := exceptionframeМааниси(esp, eipoffset+4)
	eflags := exceptionframeМааниси(esp, eipoffset+8)

	MEmergencylogСАП(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogСАП(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogСАП(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogСАП(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogСАП(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogСАП(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencylogСАП(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		басмаБАРАКfaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogСАП(" useresp=")
		MEmergencylogunsignedinteger32(exceptionframeМааниси(esp, eipoffset+12))
		MEmergencylogСАП(" ss=")
		MEmergencylogunsignedinteger32(exceptionframeМааниси(esp, eipoffset+16))
	}

	if exceptionhasКатаcode(interrupt) {
		басмаexceptionselectorinfo(err)
	}
	MEmergencylogСАП("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func Handlefatalinterruptframe(savedesp uint32, interrupt uint32) uint32 {
	Handleexception(savedesp+52, interrupt)
	haltafterfatalexception()
	return savedesp
}

func Interruptактивдүү()
func (self *TInterruptmanager) Активдүү() {
	if Активдүүinterruptmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	Активдүүinterruptmanager = address
	Interruptактивдүү()
}
func Interruptdeactive()
func (self *TInterruptmanager) Deactive() {
	Активдүүinterruptmanager = 0
	Interruptdeactive()
}

func Myhandleinterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MБасма(buffer)
	return esp
}
func MyТекшерүү(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MБасма(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MБасма(buffer)
	console_2.MHexadecimalБасма(0x40)
	return esp
}
func басмаesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Басмаxy(esp, 20, 21)
}
func gettls() uint32
func Басмаtls() {

}
