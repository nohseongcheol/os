/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Ընդհատել

import . "unsafe"
import . "reflect"

import . "պորտ"
import . "gdt"
import . "multitasking"
import . "console"

func ընդհատելignore()

func ընդհատելexceptionhandler()
func ընդհատելexceptionhandler0x00()
func ընդհատելexceptionhandler0x01()
func ընդհատելexceptionhandler0x02()
func ընդհատելexceptionhandler0x03()
func ընդհատելexceptionhandler0x04()
func ընդհատելexceptionhandler0x05()
func ընդհատելexceptionhandler0x06()
func ընդհատելexceptionhandler0x07()
func ընդհատելexceptionhandler0x08()
func ընդհատելexceptionhandler0x09()
func ընդհատելexceptionhandler0x0a()
func ընդհատելexceptionhandler0x0b()
func ընդհատելexceptionhandler0x0c()
func ընդհատելexceptionhandler0x0d()
func ընդհատելexceptionhandler0x0e()
func ընդհատելexceptionhandler0x0f()
func ընդհատելexceptionhandler0x10()
func ընդհատելexceptionhandler0x11()
func ընդհատելexceptionhandler0x12()
func ընդհատելexceptionhandler0x13()

func ընդհատելrequesthandler0x00()
func ընդհատելrequesthandler0x01()
func ընդհատելrequesthandler0x02()
func ընդհատելrequesthandler0x03()
func ընդհատելrequesthandler0x04()
func ընդհատելrequesthandler0x05()
func ընդհատելrequesthandler0x06()
func ընդհատելrequesthandler0x07()
func ընդհատելrequesthandler0x08()
func ընդհատելrequesthandler0x09()
func ընդհատելrequesthandler0x0a()
func ընդհատելrequesthandler0x0b()
func ընդհատելrequesthandler0x0c()
func ընդհատելrequesthandler0x0d()
func ընդհատելrequesthandler0x0e()
func ընդհատելrequesthandler0x0f()

func ընդհատելrequesthandler0x80()
func ընդհատելrequesthandler0x81()
func ընդհատելrequesthandler0x82()

func ԹեստՏպել(դիրք uint8, data uint8)
func setds(dssegment uint32)
func setgs(gssegment uint32)
func ընդհատելexitloop()

type TԸնդհատելhandler struct {
	ԸնդհատելՀԱՄԱՐ	uint8
	Ընդհատելmanager	uintptr
}
type IԸնդհատելhandler interface {
	HandleԸնդհատել(uint32) uint32
}

func ՆորԸնդհատելhandler(Ընդհատելmanager uintptr, ԸնդհատելՀԱՄԱՐ uint8) *TԸնդհատելhandler {
	ընդհատելhandler_2 := new(TԸնդհատելhandler)
	ընդհատելhandler_2.ԸնդհատելՀԱՄԱՐ = ԸնդհատելՀԱՄԱՐ
	ընդհատելhandler_2.Ընդհատելmanager = Ընդհատելmanager
	return ընդհատելhandler_2

}

var handler_2 [256]uintptr

func (ինքնուրույն *TԸնդհատելhandler) Init(ԸնդհատելՀԱՄԱՐ uint8, Ընդհատելmanager uintptr, funcaddress uintptr) {

	handler_2[ԸնդհատելՀԱՄԱՐ] = funcaddress

	ինքնուրույն.ԸնդհատելՀԱՄԱՐ = ԸնդհատելՀԱՄԱՐ
	ինքնուրույն.Ընդհատելmanager = Ընդհատելmanager

}
func (ինքնուրույն *TԸնդհատելhandler) SethandleԸնդհատելfuction(ԸնդհատելՀԱՄԱՐ uint32, address uintptr) {
	handler_2[ԸնդհատելՀԱՄԱՐ] = address
}
func (ինքնուրույն *TԸնդհատելhandler) Destroy() {
	ինքնուրույնuintptr := uintptr(Pointer(ինքնուրույն))
	Ընդհատելmanager := (*TԸնդհատելmanager)(Pointer(ինքնուրույն.Ընդհատելmanager))
	if ինքնուրույնuintptr == Ընդհատելmanager.Gethandler(ինքնուրույն.ԸնդհատելՀԱՄԱՐ) {
		Ընդհատելmanager.Sethandler(0, ինքնուրույն.ԸնդհատելՀԱՄԱՐ)
	}

}
func (ինքնուրույն *TԸնդհատելhandler) SetԸնդհատելmanager(Ընդհատելmanager uintptr) {
}
func (ինքնուրույն *TԸնդհատելhandler) SetԸնդհատելՀԱՄԱՐ(ԸնդհատելՀԱՄԱՐ uint8) {
	ինքնուրույն.ԸնդհատելՀԱՄԱՐ = ԸնդհատելՀԱՄԱՐ
}
func (ինքնուրույն *TԸնդհատելhandler) HandleԸնդհատել(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MՏպել(buffer)
	return esp
}
func HandleԸնդհատել1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MՏպել(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TԸնդհատելdescriptorԱղյուսակՑուցիչ struct {
}

var idtdata [256 * 8]uint8
var ԱկտիվԸնդհատելmanager uintptr = 0

const ընդհատելdebug = false

type TԸնդհատելmanager struct {
	handler_2	[256]uintptr

	ապարատայինմիջոցներԸնդհատելoffset	uint16

	taskmanager	*TTaskmanager
}

var PrimarypicՀրահանգioՊորտ uint16 = 0x20
var PrimarypicdataioՊորտ uint16 = 0x21
var SecondarypicՀրահանգioՊորտ uint16 = 0xA0
var SecondarypicdataioՊորտ uint16 = 0xA1

func (ինքնուրույն *TԸնդհատելmanager) Init(ապարատայինմիջոցներԸնդհատելoffset uint16, գլոբալdescriptorԱղյուսակ *TShareddescriptorԱղյուսակ, taskmanager *TTaskmanager) {

	ինքնուրույն.taskmanager = taskmanager

	ինքնուրույն.ապարատայինմիջոցներԸնդհատելoffset = ապարատայինմիջոցներԸնդհատելoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtԸնդհատելgate uint8 = 0xE
	address = uint32(ValueOf(ընդհատելignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(ընդհատելexceptionhandler0x0f).Pointer())
		ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(i, codesegment, address, 0, IdtԸնդհատելgate)
	}

	address = uint32(ValueOf(ընդհատելexceptionhandler0x00).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x00, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x01).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x01, codesegment, address, 0, IdtԸնդհատելgate)
	address = uint32(ValueOf(ընդհատելexceptionhandler0x02).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x02, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x03).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x03, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x04).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x04, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x05).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x05, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x06).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x06, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x07).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x07, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x08).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x08, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x09).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x09, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x0a).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x0A, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x0b).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x0B, codesegment, address, 0, IdtԸնդհատելgate)
	address = uint32(ValueOf(ընդհատելexceptionhandler0x0c).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x0C, codesegment, address, 0, IdtԸնդհատելgate)
	address = uint32(ValueOf(ընդհատելexceptionhandler0x0d).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x0D, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x0e).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x0E, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x0f).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x0F, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x10).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x10, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x11).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x11, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x12).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x12, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելexceptionhandler0x13).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x13, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x00).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x20, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x01).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x21, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x02).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x22, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x03).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x23, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x04).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x24, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x05).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x25, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x06).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x26, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x07).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x27, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x08).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x28, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x09).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x29, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x0a).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x2A, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x0b).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x2B, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x0c).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x2C, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x0d).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x2D, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x0e).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x2E, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x0f).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x2F, codesegment, address, 0, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x80).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x80, codesegment, address, 3, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x81).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x81, codesegment, address, 3, IdtԸնդհատելgate)

	address = uint32(ValueOf(ընդհատելrequesthandler0x82).Pointer())
	ինքնուրույն.ԸնդհատելdescriptorԱղյուսակentryset(0x82, codesegment, address, 3, IdtԸնդհատելgate)

	ՊորտԳրելbyte(PrimarypicՀրահանգioՊորտ, 0x11)
	ՊորտԳրելbyte(SecondarypicՀրահանգioՊորտ, 0x11)

	ՊորտԳրելbyte(PrimarypicdataioՊորտ, 0x20)
	ՊորտԳրելbyte(SecondarypicdataioՊորտ, 0x28)

	ՊորտԳրելbyte(PrimarypicdataioՊորտ, 0x04)
	ՊորտԳրելbyte(SecondarypicdataioՊորտ, 0x02)

	ՊորտԳրելbyte(PrimarypicdataioՊորտ, 0x01)
	ՊորտԳրելbyte(SecondarypicdataioՊորտ, 0x01)

	ՊորտԳրելbyte(PrimarypicdataioՊորտ, 0xF8)
	ՊորտԳրելbyte(SecondarypicdataioՊորտ, 0xEF)

	idtՑուցիչ := [6]uint8{0, 0, 0, 0, 0, 0}
	չափս := (*uint16)(Pointer(&idtՑուցիչ[0]))
	(*չափս) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtՑուցիչ[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtՑուցիչ)))
}
func Lidt(lidtaddr uintptr)

func (ինքնուրույն *TԸնդհատելmanager) ԸնդհատելdescriptorԱղյուսակentryset(ընդհատել int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorՏիպ uint8) {

	handleraddressՑածրբիթեր := (*uint16)(Pointer(&idtdata[ընդհատել*8+0]))
	(*handleraddressՑածրբիթեր) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[ընդհատել*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[ընդհատել*8+4]))
	(*reserved) = 0

	var IdtdescriptorՆերկա uint8 = 0x80
	մուտք := (*uint8)(Pointer(&idtdata[ընդհատել*8+5]))
	(*մուտք) = (IdtdescriptorՆերկա | DescriptorՏիպ | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressԲարձրբիթեր := (*uint16)(Pointer(&idtdata[ընդհատել*8+6]))
	(*handleraddressԲարձրբիթեր) = uint16((handler >> 16) & 0xFFFF)

}

func (ինքնուրույն *TԸնդհատելmanager) Sethandler(handler uintptr, ԸնդհատելՀԱՄԱՐ uint8) {
	handler_2[ԸնդհատելՀԱՄԱՐ] = handler
}
func (ինքնուրույն *TԸնդհատելmanager) Gethandler(ԸնդհատելՀԱՄԱՐ uint8) uintptr {
	return handler_2[ԸնդհատելՀԱՄԱՐ]
}
func (ինքնուրույն *TԸնդհատելmanager) DohandleԸնդհատել(ընդհատել uint8, esp uint32) uint32 {

	if ընդհատելdebug {
		console_2.MՏպելxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Տպել(uint32(ընդհատել))
		console_2.MՏպել(":")
		console_2.MUnsignedinteger32Տպել(esp)
	}
	handlerԳործարկել := false
	if handler_2[ընդհատել] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ընդհատել])))
		esp = myfunction(esp)
		handlerԳործարկել = true

	}

	if !handlerԳործարկել && ընդհատել == uint8(ինքնուրույն.ապարատայինմիջոցներԸնդհատելoffset) && ինքնուրույն.taskmanager != nil {
		esp = uint32(uintptr(Pointer(ինքնուրույն.taskmanager.Schedule((*TcpuՎիճակ)(Pointer(uintptr(esp)))))))

	}
	if !handlerԳործարկել && ընդհատել == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if ընդհատել <= 0x1F {
	}
	if 0x20 <= ընդհատել && ընդհատել < 0x30 {
		if 0x28 <= ընդհատել {
			ՊորտԳրելbyte(SecondarypicՀրահանգioՊորտ, 0x20)
		}
		ՊորտԳրելbyte(PrimarypicՀրահանգioՊորտ, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func setcr3(address uint32)

var console_2 TConsole = TConsole{}

func HandleԸնդհատել(esp uint32, ընդհատել uint32) uint32 {

	if ընդհատելdebug && ընդհատել != 0x80 && ընդհատել != 0x20 {
		console_2.MՏպելxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Տպել(uint32(ընդհատել))
		console_2.MՏպել(":")
		console_2.MUnsignedinteger32Տպել(esp)
	}

	if ԱկտիվԸնդհատելmanager != 0 {
		p := (*TԸնդհատելmanager)(Pointer(ԱկտիվԸնդհատելmanager))
		esp = p.DohandleԸնդհատել(uint8(ընդհատել), esp)
		return esp
	}
	if handler_2[ընդհատել] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ընդհատել])))
		esp = myfunction(esp)
	}
	if ընդհատել == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= ընդհատել && ընդհատել < 0x30 {
		if 0x28 <= ընդհատել {
			ՊորտԳրելbyte(SecondarypicՀրահանգioՊորտ, 0x20)
		}
		ՊորտԳրելbyte(PrimarypicՀրահանգioՊորտ, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	կՄՀ := (*TcpuՎիճակ)(Pointer(uintptr(esp)))
	if կՄՀ.Eax == 1 || կՄՀ.Eax == 252 {
		կՄՀ.Eip = uint32(ValueOf(ընդհատելexitloop).Pointer())
		կՄՀ.Cs = Segkernelcode
		կՄՀ.Ds = Segkerneldata
		կՄՀ.Es = Segkerneldata
		կՄՀ.Fs = Segkerneldata
		կՄՀ.Gs = Segkernelgs
		կՄՀ.Ss = Segkerneldata
		կՄՀ.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasՍխալcode(ընդհատել uint32) bool {
	switch ընդհատել {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionԱնուն(ընդհատել uint32) string {
	switch ընդհատել {
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

func exceptionՇրջանակԱրժեք(շրջանակ uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(շրջանակ + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func տպելԷջfaultinfo(err uint32) {
	MEmergencylogՏՈՂ(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogՏՈՂ("protection")
	} else {
		MEmergencylogՏՈՂ("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogՏՈՂ(",write")
	} else {
		MEmergencylogՏՈՂ(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogՏՈՂ(",user")
	} else {
		MEmergencylogՏՈՂ(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogՏՈՂ(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogՏՈՂ(",instruction-fetch")
	}
	MEmergencylogՏՈՂ("]")
}

func տպելexceptionselectorinfo(err uint32) {
	MEmergencylogՏՈՂ(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogՏՈՂ(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogՏՈՂ(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogՏՈՂ("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogՏՈՂ("LDT")
	} else {
		MEmergencylogՏՈՂ("GDT")
	}
	MEmergencylogՏՈՂ(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, ընդհատել uint32) uint32 {
	MEmergencylogՏՈՂ("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(ընդհատել))
	MEmergencylogՏՈՂ(" ")
	MEmergencylogՏՈՂ(exceptionԱնուն(ընդհատել))
	MEmergencylogՏՈՂ(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogՏՈՂ(" invalid-frame")
		if exceptionhasՍխալcode(ընդհատել) {
			MEmergencylogՏՈՂ(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			տպելexceptionselectorinfo(esp)
		}
		MEmergencylogՏՈՂ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasՍխալcode(ընդհատել) {
		err = exceptionՇրջանակԱրժեք(esp, 0)
		eipoffset = 4
	}
	eip := exceptionՇրջանակԱրժեք(esp, eipoffset)
	cs := exceptionՇրջանակԱրժեք(esp, eipoffset+4)
	eflags := exceptionՇրջանակԱրժեք(esp, eipoffset+8)

	MEmergencylogՏՈՂ(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogՏՈՂ(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogՏՈՂ(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogՏՈՂ(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogՏՈՂ(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogՏՈՂ(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if ընդհատել == 0x0E {
		MEmergencylogՏՈՂ(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		տպելԷջfaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogՏՈՂ(" useresp=")
		MEmergencylogunsignedinteger32(exceptionՇրջանակԱրժեք(esp, eipoffset+12))
		MEmergencylogՏՈՂ(" ss=")
		MEmergencylogunsignedinteger32(exceptionՇրջանակԱրժեք(esp, eipoffset+16))
	}

	if exceptionhasՍխալcode(ընդհատել) {
		տպելexceptionselectorinfo(err)
	}
	MEmergencylogՏՈՂ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandlefatalԸնդհատելՇրջանակ(savedesp uint32, ընդհատել uint32) uint32 {
	Handleexception(savedesp+52, ընդհատել)
	haltafterfatalexception()
	return savedesp
}

func ԸնդհատելԱկտիվ()
func (ինքնուրույն *TԸնդհատելmanager) Ակտիվ() {
	if ԱկտիվԸնդհատելmanager != 0 {
		ինքնուրույն.Deactive()
	}
	address := uintptr(Pointer(ինքնուրույն))
	ԱկտիվԸնդհատելmanager = address
	ԸնդհատելԱկտիվ()
}
func Ընդհատելdeactive()
func (ինքնուրույն *TԸնդհատելmanager) Deactive() {
	ԱկտիվԸնդհատելmanager = 0
	Ընդհատելdeactive()
}

func MyhandleԸնդհատել(ընդհատել uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MՏպել(buffer)
	return esp
}
func MyԹեստ(ընդհատել uint8, esp uint32)

func UnhandleԸնդհատել() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MՏպել(buffer)
}

func ընդհատելhandler_2(ընդհատել uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MՏպել(buffer)
	console_2.MHexadecimalՏպել(0x40)
	return esp
}
func տպելesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Տպելxy(esp, 20, 21)
}
func gettls() uint32
func Տպելtls() {

}
