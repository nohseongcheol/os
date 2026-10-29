/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupt

import . "unsafe"
import . "reflect"

import . "درگاه"
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

func Testچاپ(position uint8, data uint8)
func setds(dssegment uint32)
func setgs(gssegment uint32)
func interruptخروجloop()

type TInterrupthandler struct {
	Interruptnumber		uint8
	Interruptmanager	uintptr
}
type IInterrupthandler interface {
	Handleinterrupt(uint32) uint32
}

func Nجدیدinterrupthandler(Interruptmanager uintptr, Interruptnumber uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.Interruptnumber = Interruptnumber
	interrupthandler_2.Interruptmanager = Interruptmanager
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (خود *TInterrupthandler) Init(Interruptnumber uint8, Interruptmanager uintptr, funcaddress uintptr) {

	handler_2[Interruptnumber] = funcaddress

	خود.Interruptnumber = Interruptnumber
	خود.Interruptmanager = Interruptmanager

}
func (خود *TInterrupthandler) Sethandleinterruptfuction(Interruptnumber uint32, address uintptr) {
	handler_2[Interruptnumber] = address
}
func (خود *TInterrupthandler) Destroy() {
	خودuintptr := uintptr(Pointer(خود))
	Interruptmanager := (*TInterruptmanager)(Pointer(خود.Interruptmanager))
	if خودuintptr == Interruptmanager.Gethandler(خود.Interruptnumber) {
		Interruptmanager.Sethandler(0, خود.Interruptnumber)
	}

}
func (خود *TInterrupthandler) Setinterruptmanager(Interruptmanager uintptr) {
}
func (خود *TInterrupthandler) Setinterruptnumber(Interruptnumber uint8) {
	خود.Interruptnumber = Interruptnumber
}
func (خود *TInterrupthandler) Handleinterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.Mچاپ(buffer)
	return esp
}
func Handleinterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.Mچاپ(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptorجدولpointer struct {
}

var idtdata [256 * 8]uint8
var Aفعالinterruptmanager uintptr = 0

const interruptdebug = false

type TInterruptmanager struct {
	handler_2	[256]uintptr

	سختافزارinterruptoffset	uint16

	taskmanager	*TTaskmanager
}

var Primarypicفرمانioدرگاه uint16 = 0x20
var Primarypicdataioدرگاه uint16 = 0x21
var Secondarypicفرمانioدرگاه uint16 = 0xA0
var Secondarypicdataioدرگاه uint16 = 0xA1

func (خود *TInterruptmanager) Init(سختافزارinterruptoffset uint16, سراسریdescriptorجدول *TShareddescriptorجدول, taskmanager *TTaskmanager) {

	خود.taskmanager = taskmanager

	خود.سختافزارinterruptoffset = سختافزارinterruptoffset
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
		خود.Interruptdescriptorجدولentryset(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	خود.Interruptdescriptorجدولentryset(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	خود.Interruptdescriptorجدولentryset(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	خود.Interruptdescriptorجدولentryset(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	خود.Interruptdescriptorجدولentryset(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	خود.Interruptdescriptorجدولentryset(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	خود.Interruptdescriptorجدولentryset(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	خود.Interruptdescriptorجدولentryset(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	خود.Interruptdescriptorجدولentryset(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	خود.Interruptdescriptorجدولentryset(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	خود.Interruptdescriptorجدولentryset(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	خود.Interruptdescriptorجدولentryset(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	خود.Interruptdescriptorجدولentryset(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	خود.Interruptdescriptorجدولentryset(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	خود.Interruptdescriptorجدولentryset(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	خود.Interruptdescriptorجدولentryset(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	خود.Interruptdescriptorجدولentryset(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	خود.Interruptdescriptorجدولentryset(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	خود.Interruptdescriptorجدولentryset(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	خود.Interruptdescriptorجدولentryset(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	خود.Interruptdescriptorجدولentryset(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	خود.Interruptdescriptorجدولentryset(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	خود.Interruptdescriptorجدولentryset(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	خود.Interruptdescriptorجدولentryset(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	خود.Interruptdescriptorجدولentryset(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	خود.Interruptdescriptorجدولentryset(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	خود.Interruptdescriptorجدولentryset(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	خود.Interruptdescriptorجدولentryset(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	خود.Interruptdescriptorجدولentryset(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	خود.Interruptdescriptorجدولentryset(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	خود.Interruptdescriptorجدولentryset(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	خود.Interruptdescriptorجدولentryset(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	خود.Interruptdescriptorجدولentryset(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	خود.Interruptdescriptorجدولentryset(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	خود.Interruptdescriptorجدولentryset(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	خود.Interruptdescriptorجدولentryset(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	خود.Interruptdescriptorجدولentryset(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	خود.Interruptdescriptorجدولentryset(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	خود.Interruptdescriptorجدولentryset(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	خود.Interruptdescriptorجدولentryset(0x82, codesegment, address, 3, Idtinterruptgate)

	Pدرگاهنوشتنbyte(Primarypicفرمانioدرگاه, 0x11)
	Pدرگاهنوشتنbyte(Secondarypicفرمانioدرگاه, 0x11)

	Pدرگاهنوشتنbyte(Primarypicdataioدرگاه, 0x20)
	Pدرگاهنوشتنbyte(Secondarypicdataioدرگاه, 0x28)

	Pدرگاهنوشتنbyte(Primarypicdataioدرگاه, 0x04)
	Pدرگاهنوشتنbyte(Secondarypicdataioدرگاه, 0x02)

	Pدرگاهنوشتنbyte(Primarypicdataioدرگاه, 0x01)
	Pدرگاهنوشتنbyte(Secondarypicdataioدرگاه, 0x01)

	Pدرگاهنوشتنbyte(Primarypicdataioدرگاه, 0xF8)
	Pدرگاهنوشتنbyte(Secondarypicdataioدرگاه, 0xEF)

	idtpointer := [6]uint8{0, 0, 0, 0, 0, 0}
	اندازه := (*uint16)(Pointer(&idtpointer[0]))
	(*اندازه) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtpointer[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtpointer)))
}
func Lidt(lidtaddr uintptr)

func (خود *TInterruptmanager) Interruptdescriptorجدولentryset(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptorنوع uint8) {

	handleraddressاندکbits := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddressاندکbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*reserved) = 0

	var Idtdescriptorpresent uint8 = 0x80
	access := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*access) = (Idtdescriptorpresent | Descriptorنوع | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressزیادbits := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddressزیادbits) = uint16((handler >> 16) & 0xFFFF)

}

func (خود *TInterruptmanager) Sethandler(handler uintptr, Interruptnumber uint8) {
	handler_2[Interruptnumber] = handler
}
func (خود *TInterruptmanager) Gethandler(Interruptnumber uint8) uintptr {
	return handler_2[Interruptnumber]
}
func (خود *TInterruptmanager) Dohandleinterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptdebug {
		console_2.Mچاپxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32چاپ(uint32(interrupt))
		console_2.Mچاپ(":")
		console_2.MUnsignedinteger32چاپ(esp)
	}
	handlerاجرا := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerاجرا = true

	}

	if !handlerاجرا && interrupt == uint8(خود.سختافزارinterruptoffset) && خود.taskmanager != nil {
		esp = uint32(uintptr(Pointer(خود.taskmanager.Schedule((*Tcpuحالت)(Pointer(uintptr(esp)))))))

	}
	if !handlerاجرا && interrupt == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			Pدرگاهنوشتنbyte(Secondarypicفرمانioدرگاه, 0x20)
		}
		Pدرگاهنوشتنbyte(Primarypicفرمانioدرگاه, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func setcr3(address uint32)

var console_2 TConsole = TConsole{}

func Handleinterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptdebug && interrupt != 0x80 && interrupt != 0x20 {
		console_2.Mچاپxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32چاپ(uint32(interrupt))
		console_2.Mچاپ(":")
		console_2.MUnsignedinteger32چاپ(esp)
	}

	if Aفعالinterruptmanager != 0 {
		p := (*TInterruptmanager)(Pointer(Aفعالinterruptmanager))
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
			Pدرگاهنوشتنbyte(Secondarypicفرمانioدرگاه, 0x20)
		}
		Pدرگاهنوشتنbyte(Primarypicفرمانioدرگاه, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpuحالت)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptخروجloop).Pointer())
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

func exceptionhasخطاcode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionنام(interrupt uint32) string {
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

func exceptionچارچوبمقدار(چارچوب uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(چارچوب + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func چاپصفحهfaultinfo(err uint32) {
	MEmergencylogرشته(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogرشته("protection")
	} else {
		MEmergencylogرشته("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogرشته(",write")
	} else {
		MEmergencylogرشته(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogرشته(",user")
	} else {
		MEmergencylogرشته(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogرشته(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogرشته(",instruction-fetch")
	}
	MEmergencylogرشته("]")
}

func چاپexceptionselectorinfo(err uint32) {
	MEmergencylogرشته(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogرشته(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogرشته(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogرشته("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogرشته("LDT")
	} else {
		MEmergencylogرشته("GDT")
	}
	MEmergencylogرشته(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, interrupt uint32) uint32 {
	MEmergencylogرشته("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(interrupt))
	MEmergencylogرشته(" ")
	MEmergencylogرشته(exceptionنام(interrupt))
	MEmergencylogرشته(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogرشته(" invalid-frame")
		if exceptionhasخطاcode(interrupt) {
			MEmergencylogرشته(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			چاپexceptionselectorinfo(esp)
		}
		MEmergencylogرشته("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasخطاcode(interrupt) {
		err = exceptionچارچوبمقدار(esp, 0)
		eipoffset = 4
	}
	eip := exceptionچارچوبمقدار(esp, eipoffset)
	cs := exceptionچارچوبمقدار(esp, eipoffset+4)
	eflags_2 := exceptionچارچوبمقدار(esp, eipoffset+8)

	MEmergencylogرشته(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogرشته(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogرشته(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogرشته(" eflags=")
	MEmergencylogunsignedinteger32(eflags_2)
	MEmergencylogرشته(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogرشته(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencylogرشته(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		چاپصفحهfaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogرشته(" useresp=")
		MEmergencylogunsignedinteger32(exceptionچارچوبمقدار(esp, eipoffset+12))
		MEmergencylogرشته(" ss=")
		MEmergencylogunsignedinteger32(exceptionچارچوبمقدار(esp, eipoffset+16))
	}

	if exceptionhasخطاcode(interrupt) {
		چاپexceptionselectorinfo(err)
	}
	MEmergencylogرشته("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func Handlefatalinterruptچارچوب(savedesp uint32, interrupt uint32) uint32 {
	Handleexception(savedesp+52, interrupt)
	haltafterfatalexception()
	return savedesp
}

func Interruptفعال()
func (خود *TInterruptmanager) Aفعال() {
	if Aفعالinterruptmanager != 0 {
		خود.Deactive()
	}
	address := uintptr(Pointer(خود))
	Aفعالinterruptmanager = address
	Interruptفعال()
}
func Interruptdeactive()
func (خود *TInterruptmanager) Deactive() {
	Aفعالinterruptmanager = 0
	Interruptdeactive()
}

func Myhandleinterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.Mچاپ(buffer)
	return esp
}
func Mytest(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.Mچاپ(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.Mچاپ(buffer)
	console_2.MHexadecimalچاپ(0x40)
	return esp
}
func چاپesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32چاپxy(esp, 20, 21)
}
func gettls() uint32
func Pچاپtls() {

}
