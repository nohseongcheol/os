package Iمداخلت

import . "unsafe"
import . "reflect"

import . "پورٹ"
import . "gdt"
import . "multitasking"
import . "console"

func مداخلتignore()

func مداخلتexceptionhandler()
func مداخلتexceptionhandler0x00()
func مداخلتexceptionhandler0x01()
func مداخلتexceptionhandler0x02()
func مداخلتexceptionhandler0x03()
func مداخلتexceptionhandler0x04()
func مداخلتexceptionhandler0x05()
func مداخلتexceptionhandler0x06()
func مداخلتexceptionhandler0x07()
func مداخلتexceptionhandler0x08()
func مداخلتexceptionhandler0x09()
func مداخلتexceptionhandler0x0a()
func مداخلتexceptionhandler0x0b()
func مداخلتexceptionhandler0x0c()
func مداخلتexceptionhandler0x0d()
func مداخلتexceptionhandler0x0e()
func مداخلتexceptionhandler0x0f()
func مداخلتexceptionhandler0x10()
func مداخلتexceptionhandler0x11()
func مداخلتexceptionhandler0x12()
func مداخلتexceptionhandler0x13()

func مداخلتrequesthandler0x00()
func مداخلتrequesthandler0x01()
func مداخلتrequesthandler0x02()
func مداخلتrequesthandler0x03()
func مداخلتrequesthandler0x04()
func مداخلتrequesthandler0x05()
func مداخلتrequesthandler0x06()
func مداخلتrequesthandler0x07()
func مداخلتrequesthandler0x08()
func مداخلتrequesthandler0x09()
func مداخلتrequesthandler0x0a()
func مداخلتrequesthandler0x0b()
func مداخلتrequesthandler0x0c()
func مداخلتrequesthandler0x0d()
func مداخلتrequesthandler0x0e()
func مداخلتrequesthandler0x0f()

func مداخلتrequesthandler0x80()
func مداخلتrequesthandler0x81()
func مداخلتrequesthandler0x82()

func Tٹیسٹچھاپیں(position uint8, data uint8)
func سیٹds(dssegment uint32)
func سیٹgs(gssegment uint32)
func مداخلتexitloop()

type Tمداخلتhandler struct {
	Iمداخلتnumber	uint8
	Iمداخلتmanager	uintptr
}
type Iمداخلتhandler interface {
	Handleمداخلت(uint32) uint32
}

func Nنیامداخلتhandler(Iمداخلتmanager uintptr, Iمداخلتnumber uint8) *Tمداخلتhandler {
	مداخلتhandler_2 := new(Tمداخلتhandler)
	مداخلتhandler_2.Iمداخلتnumber = Iمداخلتnumber
	مداخلتhandler_2.Iمداخلتmanager = Iمداخلتmanager
	return مداخلتhandler_2

}

var handler_2 [256]uintptr

func (self *Tمداخلتhandler) Init(Iمداخلتnumber uint8, Iمداخلتmanager uintptr, funcaddress uintptr) {

	handler_2[Iمداخلتnumber] = funcaddress

	self.Iمداخلتnumber = Iمداخلتnumber
	self.Iمداخلتmanager = Iمداخلتmanager

}
func (self *Tمداخلتhandler) Sسیٹhandleمداخلتfuction(Iمداخلتnumber uint32, address uintptr) {
	handler_2[Iمداخلتnumber] = address
}
func (self *Tمداخلتhandler) Dتباہکریں() {
	selfuintptr := uintptr(Pointer(self))
	Iمداخلتmanager := (*Tمداخلتmanager)(Pointer(self.Iمداخلتmanager))
	if selfuintptr == Iمداخلتmanager.Gethandler(self.Iمداخلتnumber) {
		Iمداخلتmanager.Sسیٹhandler(0, self.Iمداخلتnumber)
	}

}
func (self *Tمداخلتhandler) Sسیٹمداخلتmanager(Iمداخلتmanager uintptr) {
}
func (self *Tمداخلتhandler) Sسیٹمداخلتnumber(Iمداخلتnumber uint8) {
	self.Iمداخلتnumber = Iمداخلتnumber
}
func (self *Tمداخلتhandler) Handleمداخلت(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.Mچھاپیں(buffer)
	return esp
}
func Handleمداخلت1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.Mچھاپیں(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type Tمداخلتdescriptorجدولپؤائنٹر struct {
}

var idtdata [256 * 8]uint8
var Aفعالمداخلتmanager uintptr = 0

const مداخلتdebug = false

type Tمداخلتmanager struct {
	handler_2	[256]uintptr

	ہارڈویئرمداخلتoffset	uint16

	taskmanager	*TTaskmanager
}

var Primarypicکمانڈioپورٹ uint16 = 0x20
var Primarypicdataioپورٹ uint16 = 0x21
var Secondarypicکمانڈioپورٹ uint16 = 0xA0
var Secondarypicdataioپورٹ uint16 = 0xA1

func (self *Tمداخلتmanager) Init(ہارڈویئرمداخلتoffset uint16, globaldescriptorجدول *TShareddescriptorجدول, taskmanager *TTaskmanager) {

	self.taskmanager = taskmanager

	self.ہارڈویئرمداخلتoffset = ہارڈویئرمداخلتoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var Idtمداخلتgate uint8 = 0xE
	address = uint32(ValueOf(مداخلتignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(مداخلتexceptionhandler0x0f).Pointer())
		self.Sمداخلتdescriptorجدولentryسیٹ(i, codesegment, address, 0, Idtمداخلتgate)
	}

	address = uint32(ValueOf(مداخلتexceptionhandler0x00).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x00, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x01).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x01, codesegment, address, 0, Idtمداخلتgate)
	address = uint32(ValueOf(مداخلتexceptionhandler0x02).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x02, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x03).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x03, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x04).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x04, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x05).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x05, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x06).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x06, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x07).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x07, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x08).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x08, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x09).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x09, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x0a).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x0A, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x0b).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x0B, codesegment, address, 0, Idtمداخلتgate)
	address = uint32(ValueOf(مداخلتexceptionhandler0x0c).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x0C, codesegment, address, 0, Idtمداخلتgate)
	address = uint32(ValueOf(مداخلتexceptionhandler0x0d).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x0D, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x0e).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x0E, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x0f).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x0F, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x10).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x10, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x11).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x11, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x12).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x12, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتexceptionhandler0x13).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x13, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x00).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x20, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x01).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x21, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x02).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x22, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x03).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x23, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x04).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x24, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x05).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x25, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x06).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x26, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x07).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x27, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x08).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x28, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x09).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x29, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x0a).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x2A, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x0b).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x2B, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x0c).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x2C, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x0d).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x2D, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x0e).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x2E, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x0f).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x2F, codesegment, address, 0, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x80).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x80, codesegment, address, 3, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x81).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x81, codesegment, address, 3, Idtمداخلتgate)

	address = uint32(ValueOf(مداخلتrequesthandler0x82).Pointer())
	self.Sمداخلتdescriptorجدولentryسیٹ(0x82, codesegment, address, 3, Idtمداخلتgate)

	Pپورٹلکھیںbyte(Primarypicکمانڈioپورٹ, 0x11)
	Pپورٹلکھیںbyte(Secondarypicکمانڈioپورٹ, 0x11)

	Pپورٹلکھیںbyte(Primarypicdataioپورٹ, 0x20)
	Pپورٹلکھیںbyte(Secondarypicdataioپورٹ, 0x28)

	Pپورٹلکھیںbyte(Primarypicdataioپورٹ, 0x04)
	Pپورٹلکھیںbyte(Secondarypicdataioپورٹ, 0x02)

	Pپورٹلکھیںbyte(Primarypicdataioپورٹ, 0x01)
	Pپورٹلکھیںbyte(Secondarypicdataioپورٹ, 0x01)

	Pپورٹلکھیںbyte(Primarypicdataioپورٹ, 0xF8)
	Pپورٹلکھیںbyte(Secondarypicdataioپورٹ, 0xEF)

	idtپؤائنٹر := [6]uint8{0, 0, 0, 0, 0, 0}
	حجم := (*uint16)(Pointer(&idtپؤائنٹر[0]))
	(*حجم) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtپؤائنٹر[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtپؤائنٹر)))
}
func Lidt(lidtaddr uintptr)

func (self *Tمداخلتmanager) Sمداخلتdescriptorجدولentryسیٹ(مداخلت int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptorنوعیت uint8) {

	handleraddressکمbits := (*uint16)(Pointer(&idtdata[مداخلت*8+0]))
	(*handleraddressکمbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[مداخلت*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[مداخلت*8+4]))
	(*reserved) = 0

	var Idtdescriptorموجود uint8 = 0x80
	رسائی := (*uint8)(Pointer(&idtdata[مداخلت*8+5]))
	(*رسائی) = (Idtdescriptorموجود | Descriptorنوعیت | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressاونچاbits := (*uint16)(Pointer(&idtdata[مداخلت*8+6]))
	(*handleraddressاونچاbits) = uint16((handler >> 16) & 0xFFFF)

}

func (self *Tمداخلتmanager) Sسیٹhandler(handler uintptr, Iمداخلتnumber uint8) {
	handler_2[Iمداخلتnumber] = handler
}
func (self *Tمداخلتmanager) Gethandler(Iمداخلتnumber uint8) uintptr {
	return handler_2[Iمداخلتnumber]
}
func (self *Tمداخلتmanager) Dohandleمداخلت(مداخلت uint8, esp uint32) uint32 {

	if مداخلتdebug {
		console_2.Mچھاپیںxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32چھاپیں(uint32(مداخلت))
		console_2.Mچھاپیں(":")
		console_2.MUnsignedinteger32چھاپیں(esp)
	}
	handlerچلائیں := false
	if handler_2[مداخلت] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[مداخلت])))
		esp = myfunction(esp)
		handlerچلائیں = true

	}

	if !handlerچلائیں && مداخلت == uint8(self.ہارڈویئرمداخلتoffset) && self.taskmanager != nil {
		esp = uint32(uintptr(Pointer(self.taskmanager.Schedule((*Tcpuحالت)(Pointer(uintptr(esp)))))))

	}
	if !handlerچلائیں && مداخلت == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if مداخلت <= 0x1F {
	}
	if 0x20 <= مداخلت && مداخلت < 0x30 {
		if 0x28 <= مداخلت {
			Pپورٹلکھیںbyte(Secondarypicکمانڈioپورٹ, 0x20)
		}
		Pپورٹلکھیںbyte(Primarypicکمانڈioپورٹ, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func سیٹcr3(address uint32)

var console_2 TConsole = TConsole{}

func Handleمداخلت(esp uint32, مداخلت uint32) uint32 {

	if مداخلتdebug && مداخلت != 0x80 && مداخلت != 0x20 {
		console_2.Mچھاپیںxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32چھاپیں(uint32(مداخلت))
		console_2.Mچھاپیں(":")
		console_2.MUnsignedinteger32چھاپیں(esp)
	}

	if Aفعالمداخلتmanager != 0 {
		p := (*Tمداخلتmanager)(Pointer(Aفعالمداخلتmanager))
		esp = p.Dohandleمداخلت(uint8(مداخلت), esp)
		return esp
	}
	if handler_2[مداخلت] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[مداخلت])))
		esp = myfunction(esp)
	}
	if مداخلت == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= مداخلت && مداخلت < 0x30 {
		if 0x28 <= مداخلت {
			Pپورٹلکھیںbyte(Secondarypicکمانڈioپورٹ, 0x20)
		}
		Pپورٹلکھیںbyte(Primarypicکمانڈioپورٹ, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	سیپییو := (*Tcpuحالت)(Pointer(uintptr(esp)))
	if سیپییو.Eax == 1 || سیپییو.Eax == 252 {
		سیپییو.Eip = uint32(ValueOf(مداخلتexitloop).Pointer())
		سیپییو.Cs = Segkernelcode
		سیپییو.Ds = Segkerneldata
		سیپییو.Es = Segkerneldata
		سیپییو.Fs = Segkerneldata
		سیپییو.Gs = Segkernelgs
		سیپییو.Ss = Segkerneldata
		سیپییو.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasغلطیcode(مداخلت uint32) bool {
	switch مداخلت {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionنام(مداخلت uint32) string {
	switch مداخلت {
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

func exceptionframeقدر(frame uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(frame + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func چھاپیںصفحہfaultinfo(err uint32) {
	MEmergencylogڈورا(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogڈورا("protection")
	} else {
		MEmergencylogڈورا("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogڈورا(",write")
	} else {
		MEmergencylogڈورا(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogڈورا(",user")
	} else {
		MEmergencylogڈورا(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogڈورا(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogڈورا(",instruction-fetch")
	}
	MEmergencylogڈورا("]")
}

func چھاپیںexceptionselectorinfo(err uint32) {
	MEmergencylogڈورا(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogڈورا(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogڈورا(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogڈورا("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogڈورا("LDT")
	} else {
		MEmergencylogڈورا("GDT")
	}
	MEmergencylogڈورا(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, مداخلت uint32) uint32 {
	MEmergencylogڈورا("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(مداخلت))
	MEmergencylogڈورا(" ")
	MEmergencylogڈورا(exceptionنام(مداخلت))
	MEmergencylogڈورا(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogڈورا(" invalid-frame")
		if exceptionhasغلطیcode(مداخلت) {
			MEmergencylogڈورا(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			چھاپیںexceptionselectorinfo(esp)
		}
		MEmergencylogڈورا("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasغلطیcode(مداخلت) {
		err = exceptionframeقدر(esp, 0)
		eipoffset = 4
	}
	eip := exceptionframeقدر(esp, eipoffset)
	cs := exceptionframeقدر(esp, eipoffset+4)
	eflags := exceptionframeقدر(esp, eipoffset+8)

	MEmergencylogڈورا(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogڈورا(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogڈورا(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogڈورا(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogڈورا(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogڈورا(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if مداخلت == 0x0E {
		MEmergencylogڈورا(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		چھاپیںصفحہfaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogڈورا(" useresp=")
		MEmergencylogunsignedinteger32(exceptionframeقدر(esp, eipoffset+12))
		MEmergencylogڈورا(" ss=")
		MEmergencylogunsignedinteger32(exceptionframeقدر(esp, eipoffset+16))
	}

	if exceptionhasغلطیcode(مداخلت) {
		چھاپیںexceptionselectorinfo(err)
	}
	MEmergencylogڈورا("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func Handlefatalمداخلتframe(savedesp uint32, مداخلت uint32) uint32 {
	Handleexception(savedesp+52, مداخلت)
	haltafterfatalexception()
	return savedesp
}

func Iمداخلتفعال()
func (self *Tمداخلتmanager) Aفعال() {
	if Aفعالمداخلتmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	Aفعالمداخلتmanager = address
	Iمداخلتفعال()
}
func Iمداخلتdeactive()
func (self *Tمداخلتmanager) Deactive() {
	Aفعالمداخلتmanager = 0
	Iمداخلتdeactive()
}

func Myhandleمداخلت(مداخلت uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.Mچھاپیں(buffer)
	return esp
}
func Myٹیسٹ(مداخلت uint8, esp uint32)

func Unhandleمداخلت() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.Mچھاپیں(buffer)
}

func مداخلتhandler_2(مداخلت uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.Mچھاپیں(buffer)
	console_2.MHexadecimalچھاپیں(0x40)
	return esp
}
func چھاپیںesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32چھاپیںxy(esp, 20, 21)
}
func gettls() uint32
func Pچھاپیںtls() {

}
