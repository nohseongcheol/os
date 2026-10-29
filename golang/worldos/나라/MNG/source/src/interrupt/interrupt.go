/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupt

import . "unsafe"
import . "reflect"

import . "порт"
import . "gdt"
import . "multitasking"
import . "консол"

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

func TestХэвлэх(position uint8, data uint8)
func setds(dssegment uint32)
func setgs(gssegment uint32)
func interruptexitloop()

type TInterrupthandler struct {
	Interruptnumber		uint8
	InterruptЗохицуулагч	uintptr
}
type IInterrupthandler interface {
	Handleinterrupt(uint32) uint32
}

func Шинэinterrupthandler(InterruptЗохицуулагч uintptr, Interruptnumber uint8) *TInterrupthandler {
	interrupthandler_2 := new(TInterrupthandler)
	interrupthandler_2.Interruptnumber = Interruptnumber
	interrupthandler_2.InterruptЗохицуулагч = InterruptЗохицуулагч
	return interrupthandler_2

}

var handler_2 [256]uintptr

func (self *TInterrupthandler) Init(Interruptnumber uint8, InterruptЗохицуулагч uintptr, funcaddress uintptr) {

	handler_2[Interruptnumber] = funcaddress

	self.Interruptnumber = Interruptnumber
	self.InterruptЗохицуулагч = InterruptЗохицуулагч

}
func (self *TInterrupthandler) Sethandleinterruptfuction(Interruptnumber uint32, address uintptr) {
	handler_2[Interruptnumber] = address
}
func (self *TInterrupthandler) Destroy() {
	selfuintptr := uintptr(Pointer(self))
	InterruptЗохицуулагч := (*TInterruptЗохицуулагч)(Pointer(self.InterruptЗохицуулагч))
	if selfuintptr == InterruptЗохицуулагч.Gethandler(self.Interruptnumber) {
		InterruptЗохицуулагч.Sethandler(0, self.Interruptnumber)
	}

}
func (self *TInterrupthandler) SetinterruptЗохицуулагч(InterruptЗохицуулагч uintptr) {
}
func (self *TInterrupthandler) Setinterruptnumber(Interruptnumber uint8) {
	self.Interruptnumber = Interruptnumber
}
func (self *TInterrupthandler) Handleinterrupt(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	консол_2 := TКонсол{}
	консол_2.MХэвлэх(buffer)
	return esp
}
func Handleinterrupt1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	консол_2 := TКонсол{}
	консол_2.MХэвлэх(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterruptdescriptortablepointer struct {
}

var idtdata [256 * 8]uint8
var ИдэвхтэйinterruptЗохицуулагч uintptr = 0

const interruptdebug = false

type TInterruptЗохицуулагч struct {
	handler_2	[256]uintptr

	техникхангамжinterruptoffset	uint16

	taskЗохицуулагч	*TTaskЗохицуулагч
}

var PrimarypicТушаалioПорт uint16 = 0x20
var PrimarypicdataioПорт uint16 = 0x21
var SecondarypicТушаалioПорт uint16 = 0xA0
var SecondarypicdataioПорт uint16 = 0xA1

func (self *TInterruptЗохицуулагч) Init(техникхангамжinterruptoffset uint16, globaldescriptortable *TShareddescriptortable, taskЗохицуулагч *TTaskЗохицуулагч) {

	self.taskЗохицуулагч = taskЗохицуулагч

	self.техникхангамжinterruptoffset = техникхангамжinterruptoffset
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
		self.Interruptdescriptortableentryset(i, codesegment, address, 0, Idtinterruptgate)
	}

	address = uint32(ValueOf(interruptexceptionhandler0x00).Pointer())
	self.Interruptdescriptortableentryset(0x00, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x01).Pointer())
	self.Interruptdescriptortableentryset(0x01, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x02).Pointer())
	self.Interruptdescriptortableentryset(0x02, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x03).Pointer())
	self.Interruptdescriptortableentryset(0x03, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x04).Pointer())
	self.Interruptdescriptortableentryset(0x04, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x05).Pointer())
	self.Interruptdescriptortableentryset(0x05, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x06).Pointer())
	self.Interruptdescriptortableentryset(0x06, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x07).Pointer())
	self.Interruptdescriptortableentryset(0x07, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x08).Pointer())
	self.Interruptdescriptortableentryset(0x08, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x09).Pointer())
	self.Interruptdescriptortableentryset(0x09, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0a).Pointer())
	self.Interruptdescriptortableentryset(0x0A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0b).Pointer())
	self.Interruptdescriptortableentryset(0x0B, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0c).Pointer())
	self.Interruptdescriptortableentryset(0x0C, codesegment, address, 0, Idtinterruptgate)
	address = uint32(ValueOf(interruptexceptionhandler0x0d).Pointer())
	self.Interruptdescriptortableentryset(0x0D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0e).Pointer())
	self.Interruptdescriptortableentryset(0x0E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x0f).Pointer())
	self.Interruptdescriptortableentryset(0x0F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x10).Pointer())
	self.Interruptdescriptortableentryset(0x10, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x11).Pointer())
	self.Interruptdescriptortableentryset(0x11, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x12).Pointer())
	self.Interruptdescriptortableentryset(0x12, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptexceptionhandler0x13).Pointer())
	self.Interruptdescriptortableentryset(0x13, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x00).Pointer())
	self.Interruptdescriptortableentryset(0x20, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x01).Pointer())
	self.Interruptdescriptortableentryset(0x21, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x02).Pointer())
	self.Interruptdescriptortableentryset(0x22, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x03).Pointer())
	self.Interruptdescriptortableentryset(0x23, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x04).Pointer())
	self.Interruptdescriptortableentryset(0x24, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x05).Pointer())
	self.Interruptdescriptortableentryset(0x25, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x06).Pointer())
	self.Interruptdescriptortableentryset(0x26, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x07).Pointer())
	self.Interruptdescriptortableentryset(0x27, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x08).Pointer())
	self.Interruptdescriptortableentryset(0x28, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x09).Pointer())
	self.Interruptdescriptortableentryset(0x29, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0a).Pointer())
	self.Interruptdescriptortableentryset(0x2A, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0b).Pointer())
	self.Interruptdescriptortableentryset(0x2B, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0c).Pointer())
	self.Interruptdescriptortableentryset(0x2C, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0d).Pointer())
	self.Interruptdescriptortableentryset(0x2D, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0e).Pointer())
	self.Interruptdescriptortableentryset(0x2E, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x0f).Pointer())
	self.Interruptdescriptortableentryset(0x2F, codesegment, address, 0, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x80).Pointer())
	self.Interruptdescriptortableentryset(0x80, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x81).Pointer())
	self.Interruptdescriptortableentryset(0x81, codesegment, address, 3, Idtinterruptgate)

	address = uint32(ValueOf(interruptrequesthandler0x82).Pointer())
	self.Interruptdescriptortableentryset(0x82, codesegment, address, 3, Idtinterruptgate)

	ПортБичихbyte(PrimarypicТушаалioПорт, 0x11)
	ПортБичихbyte(SecondarypicТушаалioПорт, 0x11)

	ПортБичихbyte(PrimarypicdataioПорт, 0x20)
	ПортБичихbyte(SecondarypicdataioПорт, 0x28)

	ПортБичихbyte(PrimarypicdataioПорт, 0x04)
	ПортБичихbyte(SecondarypicdataioПорт, 0x02)

	ПортБичихbyte(PrimarypicdataioПорт, 0x01)
	ПортБичихbyte(SecondarypicdataioПорт, 0x01)

	ПортБичихbyte(PrimarypicdataioПорт, 0xF8)
	ПортБичихbyte(SecondarypicdataioПорт, 0xEF)

	idtpointer := [6]uint8{0, 0, 0, 0, 0, 0}
	хэмжээ := (*uint16)(Pointer(&idtpointer[0]))
	(*хэмжээ) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtpointer[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtpointer)))
}
func Lidt(lidtaddr uintptr)

func (self *TInterruptЗохицуулагч) Interruptdescriptortableentryset(interrupt int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorТөрөл uint8) {

	handleraddressБагаbits := (*uint16)(Pointer(&idtdata[interrupt*8+0]))
	(*handleraddressБагаbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interrupt*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[interrupt*8+4]))
	(*reserved) = 0

	var Idtdescriptorpresent uint8 = 0x80
	access := (*uint8)(Pointer(&idtdata[interrupt*8+5]))
	(*access) = (Idtdescriptorpresent | DescriptorТөрөл | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressБүрэнцэнэглэгдсэнbits := (*uint16)(Pointer(&idtdata[interrupt*8+6]))
	(*handleraddressБүрэнцэнэглэгдсэнbits) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TInterruptЗохицуулагч) Sethandler(handler uintptr, Interruptnumber uint8) {
	handler_2[Interruptnumber] = handler
}
func (self *TInterruptЗохицуулагч) Gethandler(Interruptnumber uint8) uintptr {
	return handler_2[Interruptnumber]
}
func (self *TInterruptЗохицуулагч) Dohandleinterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptdebug {
		консол_2.MХэвлэхxy("[esp:", 1, 20)
		консол_2.MUnsignedinteger32Хэвлэх(uint32(interrupt))
		консол_2.MХэвлэх(":")
		консол_2.MUnsignedinteger32Хэвлэх(esp)
	}
	handlerАжиллуулах := false
	if handler_2[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interrupt])))
		esp = myfunction(esp)
		handlerАжиллуулах = true

	}

	if !handlerАжиллуулах && interrupt == uint8(self.техникхангамжinterruptoffset) && self.taskЗохицуулагч != nil {
		esp = uint32(uintptr(Pointer(self.taskЗохицуулагч.Schedule((*Tcpustate)(Pointer(uintptr(esp)))))))

	}
	if !handlerАжиллуулах && interrupt == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			ПортБичихbyte(SecondarypicТушаалioПорт, 0x20)
		}
		ПортБичихbyte(PrimarypicТушаалioПорт, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func setcr3(address uint32)

var консол_2 TКонсол = TКонсол{}

func Handleinterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptdebug && interrupt != 0x80 && interrupt != 0x20 {
		консол_2.MХэвлэхxy("[esp:", 1, 21)
		консол_2.MUnsignedinteger32Хэвлэх(uint32(interrupt))
		консол_2.MХэвлэх(":")
		консол_2.MUnsignedinteger32Хэвлэх(esp)
	}

	if ИдэвхтэйinterruptЗохицуулагч != 0 {
		p := (*TInterruptЗохицуулагч)(Pointer(ИдэвхтэйinterruptЗохицуулагч))
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
			ПортБичихbyte(SecondarypicТушаалioПорт, 0x20)
		}
		ПортБичихbyte(PrimarypicТушаалioПорт, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpustate)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptexitloop).Pointer())
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

func exceptionhasАлдааcode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionНэр(interrupt uint32) string {
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

func exceptionframeУтга(frame uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(frame + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func хэвлэхХУУДАСfaultinfo(err uint32) {
	MEmergencylogБИЧВЭР(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogБИЧВЭР("protection")
	} else {
		MEmergencylogБИЧВЭР("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogБИЧВЭР(",write")
	} else {
		MEmergencylogБИЧВЭР(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogБИЧВЭР(",user")
	} else {
		MEmergencylogБИЧВЭР(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogБИЧВЭР(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogБИЧВЭР(",instruction-fetch")
	}
	MEmergencylogБИЧВЭР("]")
}

func хэвлэхexceptionselectorinfo(err uint32) {
	MEmergencylogБИЧВЭР(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogБИЧВЭР(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogБИЧВЭР(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogБИЧВЭР("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogБИЧВЭР("LDT")
	} else {
		MEmergencylogБИЧВЭР("GDT")
	}
	MEmergencylogБИЧВЭР(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, interrupt uint32) uint32 {
	MEmergencylogБИЧВЭР("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(interrupt))
	MEmergencylogБИЧВЭР(" ")
	MEmergencylogБИЧВЭР(exceptionНэр(interrupt))
	MEmergencylogБИЧВЭР(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogБИЧВЭР(" invalid-frame")
		if exceptionhasАлдааcode(interrupt) {
			MEmergencylogБИЧВЭР(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			хэвлэхexceptionselectorinfo(esp)
		}
		MEmergencylogБИЧВЭР("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasАлдааcode(interrupt) {
		err = exceptionframeУтга(esp, 0)
		eipoffset = 4
	}
	eip := exceptionframeУтга(esp, eipoffset)
	cs := exceptionframeУтга(esp, eipoffset+4)
	eflags := exceptionframeУтга(esp, eipoffset+8)

	MEmergencylogБИЧВЭР(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogБИЧВЭР(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogБИЧВЭР(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogБИЧВЭР(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogБИЧВЭР(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogБИЧВЭР(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if interrupt == 0x0E {
		MEmergencylogБИЧВЭР(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		хэвлэхХУУДАСfaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogБИЧВЭР(" useresp=")
		MEmergencylogunsignedinteger32(exceptionframeУтга(esp, eipoffset+12))
		MEmergencylogБИЧВЭР(" ss=")
		MEmergencylogunsignedinteger32(exceptionframeУтга(esp, eipoffset+16))
	}

	if exceptionhasАлдааcode(interrupt) {
		хэвлэхexceptionselectorinfo(err)
	}
	MEmergencylogБИЧВЭР("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func Handlefatalinterruptframe(savedesp uint32, interrupt uint32) uint32 {
	Handleexception(savedesp+52, interrupt)
	haltafterfatalexception()
	return savedesp
}

func InterruptИдэвхтэй()
func (self *TInterruptЗохицуулагч) Идэвхтэй() {
	if ИдэвхтэйinterruptЗохицуулагч != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	ИдэвхтэйinterruptЗохицуулагч = address
	InterruptИдэвхтэй()
}
func Interruptdeactive()
func (self *TInterruptЗохицуулагч) Deactive() {
	ИдэвхтэйinterruptЗохицуулагч = 0
	Interruptdeactive()
}

func Myhandleinterrupt(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	консол_2 := TКонсол{}
	консол_2.MХэвлэх(buffer)
	return esp
}
func Mytest(interrupt uint8, esp uint32)

func Unhandleinterrupt() {
	buffer := []byte("unhandle interrupt\n")
	консол_2 := TКонсол{}
	консол_2.MХэвлэх(buffer)
}

func interrupthandler_2(interrupt uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	консол_2 := TКонсол{}
	консол_2.MХэвлэх(buffer)
	консол_2.MHexadecimalХэвлэх(0x40)
	return esp
}
func хэвлэхesp(esp uint32) {
	консол_2 := TКонсол{}
	консол_2.MUnsignedinteger32Хэвлэхxy(esp, 20, 21)
}
func gettls() uint32
func Хэвлэхtls() {

}
