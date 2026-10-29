/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupt

import . "unsafe"
import . "reflect"

import . "порта"
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

func TestПечати(позиција uint8, data uint8)
func поставиds(dssegment uint32)
func поставиgs(gssegment uint32)
func interruptИзлезloop()

type TInterrupthandler struct {
	Interruptnumber		uint8
	Interruptmanager	uintptr
}
type IInterrupthandler interface {
	Handleinterrupt(uint32) uint32
}

func Новinterrupthandler(Interruptmanager uintptr, Interruptnumber uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.Interruptnumber = Interruptnumber
	interrupthandler_2.Interruptmanager = Interruptmanager
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (само *TInterrupthandler) Init(Interruptnumber uint8, Interruptmanager uintptr, funcaddress uintptr) {

	handler_2[Interruptnumber] = funcaddress

	само.Interruptnumber = Interruptnumber
	само.Interruptmanager = Interruptmanager

}
func (само *TInterrupthandler) Поставиhandleinterruptfuction(Interruptnumber uint32, address uintptr) {
	handler_2[Interruptnumber] = address
}
func (само *TInterrupthandler) Destroy() {
	самоuintptr := uintptr(Pointer(само))
	Interruptmanager := (*TInterruptmanager)(Pointer(само.Interruptmanager))
	if самоuintptr == Interruptmanager.Gethandler(само.Interruptnumber) {
		Interruptmanager.Поставиhandler(0, само.Interruptnumber)
	}

}
func (само *TInterrupthandler) Поставиinterruptmanager(Interruptmanager uintptr) {
}
func (само *TInterrupthandler) Поставиinterruptnumber(Interruptnumber uint8) {
	само.Interruptnumber = Interruptnumber
}
func (само *TInterrupthandler) Handleinterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MПечати(buffer)
	return esp
}
func Handleinterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MПечати(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptorТабелаСтрелка struct {
}

var idtdata [256 * 8]uint8
var Активноinterruptmanager uintptr = 0

const interruptdebug = false

type TInterruptmanager struct {
	handler_2	[256]uintptr

	хардверinterruptoffset	uint16

	taskmanager	*TTaskmanager
}

var PrimarypicКомандаioПорта uint16 = 0x20
var PrimarypicdataioПорта uint16 = 0x21
var SecondarypicКомандаioПорта uint16 = 0xA0
var SecondarypicdataioПорта uint16 = 0xA1

func (само *TInterruptmanager) Init(хардверinterruptoffset uint16, глобалнаdescriptorТабела *TShareddescriptorТабела, taskmanager *TTaskmanager) {

	само.taskmanager = taskmanager

	само.хардверinterruptoffset = хардверinterruptoffset
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
		само.InterruptdescriptorТабелаentryпостави(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	само.InterruptdescriptorТабелаentryпостави(0x82, codesegment, address, 3, Idtinterruptgate)

	ПортаЗапишиbyte(PrimarypicКомандаioПорта, 0x11)
	ПортаЗапишиbyte(SecondarypicКомандаioПорта, 0x11)

	ПортаЗапишиbyte(PrimarypicdataioПорта, 0x20)
	ПортаЗапишиbyte(SecondarypicdataioПорта, 0x28)

	ПортаЗапишиbyte(PrimarypicdataioПорта, 0x04)
	ПортаЗапишиbyte(SecondarypicdataioПорта, 0x02)

	ПортаЗапишиbyte(PrimarypicdataioПорта, 0x01)
	ПортаЗапишиbyte(SecondarypicdataioПорта, 0x01)

	ПортаЗапишиbyte(PrimarypicdataioПорта, 0xF8)
	ПортаЗапишиbyte(SecondarypicdataioПорта, 0xEF)

	idtСтрелка := [6]uint8{0, 0, 0, 0, 0, 0}
	големина := (*uint16)(Pointer(&idtСтрелка[0]))
	(*големина) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtСтрелка[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtСтрелка)))
}
func Lidt(lidtaddr uintptr)

func (само *TInterruptmanager) InterruptdescriptorТабелаentryпостави(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorТип uint8) {

	handleraddresslowbits := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddresslowbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*reserved) = 0

	var Idtdescriptorpresent uint8 = 0x80
	пристап := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*пристап) = (Idtdescriptorpresent | DescriptorТип | ((Descriptorprivilegelevel & 3) << 5))

	handleraddresshighbits := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddresshighbits) = uint16((handler >> 16) & 0xFFFF)

}

func (само *TInterruptmanager) Поставиhandler(handler uintptr, Interruptnumber uint8) {
	handler_2[Interruptnumber] = handler
}
func (само *TInterruptmanager) Gethandler(Interruptnumber uint8) uintptr {
	return handler_2[Interruptnumber]
}
func (само *TInterruptmanager) Dohandleinterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptdebug {
		console_2.MПечатиxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Печати(uint32(interrupt))
		console_2.MПечати(":")
		console_2.MUnsignedinteger32Печати(esp)
	}
	handlerИзврши := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerИзврши = true

	}

	if !handlerИзврши && interrupt == uint8(само.хардверinterruptoffset) && само.taskmanager != nil {
		esp = uint32(uintptr(Pointer(само.taskmanager.Schedule((*Tcpustate)(Pointer(uintptr(esp)))))))

	}
	if !handlerИзврши && interrupt == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			ПортаЗапишиbyte(SecondarypicКомандаioПорта, 0x20)
		}
		ПортаЗапишиbyte(PrimarypicКомандаioПорта, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func поставиcr3(address uint32)

var console_2 TConsole = TConsole{}

func Handleinterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptdebug && interrupt != 0x80 && interrupt != 0x20 {
		console_2.MПечатиxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Печати(uint32(interrupt))
		console_2.MПечати(":")
		console_2.MUnsignedinteger32Печати(esp)
	}

	if Активноinterruptmanager != 0 {
		p := (*TInterruptmanager)(Pointer(Активноinterruptmanager))
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
			ПортаЗапишиbyte(SecondarypicКомандаioПорта, 0x20)
		}
		ПортаЗапишиbyte(PrimarypicКомандаioПорта, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpustate)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptИзлезloop).Pointer())
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

func exceptionhasГрешкаcode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionИме(interrupt uint32) string {
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

func exceptionРамкаВредност(рамка uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(рамка + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func печатиСтраницаfaultinfo(err uint32) {
	MEmergencylogstring(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogstring("protection")
	} else {
		MEmergencylogstring("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogstring(",write")
	} else {
		MEmergencylogstring(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogstring(",user")
	} else {
		MEmergencylogstring(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogstring(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogstring(",instruction-fetch")
	}
	MEmergencylogstring("]")
}

func печатиexceptionselectorinfo(err uint32) {
	MEmergencylogstring(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogstring(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogstring(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogstring("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogstring("LDT")
	} else {
		MEmergencylogstring("GDT")
	}
	MEmergencylogstring(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, interrupt uint32) uint32 {
	MEmergencylogstring("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(interrupt))
	MEmergencylogstring(" ")
	MEmergencylogstring(exceptionИме(interrupt))
	MEmergencylogstring(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogstring(" invalid-frame")
		if exceptionhasГрешкаcode(interrupt) {
			MEmergencylogstring(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			печатиexceptionselectorinfo(esp)
		}
		MEmergencylogstring("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasГрешкаcode(interrupt) {
		err = exceptionРамкаВредност(esp, 0)
		eipoffset = 4
	}
	eip := exceptionРамкаВредност(esp, eipoffset)
	cs := exceptionРамкаВредност(esp, eipoffset+4)
	eflags := exceptionРамкаВредност(esp, eipoffset+8)

	MEmergencylogstring(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogstring(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogstring(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogstring(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogstring(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogstring(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencylogstring(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		печатиСтраницаfaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogstring(" useresp=")
		MEmergencylogunsignedinteger32(exceptionРамкаВредност(esp, eipoffset+12))
		MEmergencylogstring(" ss=")
		MEmergencylogunsignedinteger32(exceptionРамкаВредност(esp, eipoffset+16))
	}

	if exceptionhasГрешкаcode(interrupt) {
		печатиexceptionselectorinfo(err)
	}
	MEmergencylogstring("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandlefatalinterruptРамка(savedesp uint32, interrupt uint32) uint32 {
	Handleexception(savedesp+52, interrupt)
	haltafterfatalexception()
	return savedesp
}

func Interruptактивно()
func (само *TInterruptmanager) Активно() {
	if Активноinterruptmanager != 0 {
		само.Deactive()
	}
	address := uintptr(Pointer(само))
	Активноinterruptmanager = address
	Interruptактивно()
}
func Interruptdeactive()
func (само *TInterruptmanager) Deactive() {
	Активноinterruptmanager = 0
	Interruptdeactive()
}

func Myhandleinterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MПечати(buffer)
	return esp
}
func Mytest(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MПечати(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MПечати(buffer)
	console_2.MHexadecimalПечати(0x40)
	return esp
}
func печатиesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Печатиxy(esp, 20, 21)
}
func gettls() uint32
func Печатиtls() {

}
