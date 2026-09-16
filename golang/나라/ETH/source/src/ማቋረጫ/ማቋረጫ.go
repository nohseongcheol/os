/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Iማቋረጫ

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func ማቋረጫignore()

func ማቋረጫexceptionhandler()
func ማቋረጫexceptionhandler0x00()
func ማቋረጫexceptionhandler0x01()
func ማቋረጫexceptionhandler0x02()
func ማቋረጫexceptionhandler0x03()
func ማቋረጫexceptionhandler0x04()
func ማቋረጫexceptionhandler0x05()
func ማቋረጫexceptionhandler0x06()
func ማቋረጫexceptionhandler0x07()
func ማቋረጫexceptionhandler0x08()
func ማቋረጫexceptionhandler0x09()
func ማቋረጫexceptionhandler0x0a()
func ማቋረጫexceptionhandler0x0b()
func ማቋረጫexceptionhandler0x0c()
func ማቋረጫexceptionhandler0x0d()
func ማቋረጫexceptionhandler0x0e()
func ማቋረጫexceptionhandler0x0f()
func ማቋረጫexceptionhandler0x10()
func ማቋረጫexceptionhandler0x11()
func ማቋረጫexceptionhandler0x12()
func ማቋረጫexceptionhandler0x13()

func ማቋረጫrequesthandler0x00()
func ማቋረጫrequesthandler0x01()
func ማቋረጫrequesthandler0x02()
func ማቋረጫrequesthandler0x03()
func ማቋረጫrequesthandler0x04()
func ማቋረጫrequesthandler0x05()
func ማቋረጫrequesthandler0x06()
func ማቋረጫrequesthandler0x07()
func ማቋረጫrequesthandler0x08()
func ማቋረጫrequesthandler0x09()
func ማቋረጫrequesthandler0x0a()
func ማቋረጫrequesthandler0x0b()
func ማቋረጫrequesthandler0x0c()
func ማቋረጫrequesthandler0x0d()
func ማቋረጫrequesthandler0x0e()
func ማቋረጫrequesthandler0x0f()

func ማቋረጫrequesthandler0x80()
func ማቋረጫrequesthandler0x81()
func ማቋረጫrequesthandler0x82()

func Tመሞከሪያማተሚያ(አካባቢ_2 uint8, data uint8)
func setds(dssegment uint32)
func setgs(gssegment uint32)
func ማቋረጫውጣloop()

type Tማቋረጫhandler struct {
	Iማቋረጫቁጥር	uint8
	Iማቋረጫmanager	uintptr
}
type Iማቋረጫhandler interface {
	Handleማቋረጫ(uint32) uint32
}

func Nአዲስማቋረጫhandler(Iማቋረጫmanager uintptr, Iማቋረጫቁጥር uint8) *Tማቋረጫhandler {
	ማቋረጫhandler_2 := new(Tማቋረጫhandler)
	ማቋረጫhandler_2.Iማቋረጫቁጥር = Iማቋረጫቁጥር
	ማቋረጫhandler_2.Iማቋረጫmanager = Iማቋረጫmanager
	return ማቋረጫhandler_2

}

var handler_2 [256]uintptr

func (self *Tማቋረጫhandler) Init(Iማቋረጫቁጥር uint8, Iማቋረጫmanager uintptr, funcaddress uintptr) {

	handler_2[Iማቋረጫቁጥር] = funcaddress

	self.Iማቋረጫቁጥር = Iማቋረጫቁጥር
	self.Iማቋረጫmanager = Iማቋረጫmanager

}
func (self *Tማቋረጫhandler) Sethandleማቋረጫfuction(Iማቋረጫቁጥር uint32, address uintptr) {
	handler_2[Iማቋረጫቁጥር] = address
}
func (self *Tማቋረጫhandler) Dአጥፋ() {
	selfuintptr := uintptr(Pointer(self))
	Iማቋረጫmanager := (*Tማቋረጫmanager)(Pointer(self.Iማቋረጫmanager))
	if selfuintptr == Iማቋረጫmanager.Gethandler(self.Iማቋረጫቁጥር) {
		Iማቋረጫmanager.Sethandler(0, self.Iማቋረጫቁጥር)
	}

}
func (self *Tማቋረጫhandler) Setማቋረጫmanager(Iማቋረጫmanager uintptr) {
}
func (self *Tማቋረጫhandler) Setማቋረጫቁጥር(Iማቋረጫቁጥር uint8) {
	self.Iማቋረጫቁጥር = Iማቋረጫቁጥር
}
func (self *Tማቋረጫhandler) Handleማቋረጫ(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.Mማተሚያ(buffer)
	return esp
}
func Handleማቋረጫ1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.Mማተሚያ(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type Tማቋረጫdescriptorሰንጠረዥጠቋሚ struct {
}

var idtdata [256 * 8]uint8
var Aአሰራማቋረጫmanager uintptr = 0

const ማቋረጫdebug = false

type Tማቋረጫmanager struct {
	handler_2	[256]uintptr

	ጠንካራአካልማቋረጫoffset	uint16

	taskmanager	*TTaskmanager
}

var Primarypicትእዛዝioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var Secondarypicትእዛዝioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (self *Tማቋረጫmanager) Init(ጠንካራአካልማቋረጫoffset uint16, አለምአቀፍdescriptorሰንጠረዥ *TShareddescriptorሰንጠረዥ, taskmanager *TTaskmanager) {

	self.taskmanager = taskmanager

	self.ጠንካራአካልማቋረጫoffset = ጠንካራአካልማቋረጫoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var Idtማቋረጫgate uint8 = 0xE
	address = uint32(ValueOf(ማቋረጫignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(ማቋረጫexceptionhandler0x0f).Pointer())
		self.Sማቋረጫdescriptorሰንጠረዥentryset(i, codesegment, address, 0, Idtማቋረጫgate)
	}

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x00).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x00, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x01).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x01, codesegment, address, 0, Idtማቋረጫgate)
	address = uint32(ValueOf(ማቋረጫexceptionhandler0x02).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x02, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x03).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x03, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x04).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x04, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x05).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x05, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x06).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x06, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x07).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x07, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x08).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x08, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x09).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x09, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x0a).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x0A, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x0b).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x0B, codesegment, address, 0, Idtማቋረጫgate)
	address = uint32(ValueOf(ማቋረጫexceptionhandler0x0c).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x0C, codesegment, address, 0, Idtማቋረጫgate)
	address = uint32(ValueOf(ማቋረጫexceptionhandler0x0d).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x0D, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x0e).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x0E, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x0f).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x0F, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x10).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x10, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x11).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x11, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x12).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x12, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫexceptionhandler0x13).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x13, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x00).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x20, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x01).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x21, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x02).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x22, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x03).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x23, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x04).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x24, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x05).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x25, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x06).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x26, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x07).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x27, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x08).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x28, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x09).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x29, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x0a).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x2A, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x0b).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x2B, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x0c).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x2C, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x0d).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x2D, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x0e).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x2E, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x0f).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x2F, codesegment, address, 0, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x80).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x80, codesegment, address, 3, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x81).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x81, codesegment, address, 3, Idtማቋረጫgate)

	address = uint32(ValueOf(ማቋረጫrequesthandler0x82).Pointer())
	self.Sማቋረጫdescriptorሰንጠረዥentryset(0x82, codesegment, address, 3, Idtማቋረጫgate)

	Portመጻፊያbyte(Primarypicትእዛዝioport, 0x11)
	Portመጻፊያbyte(Secondarypicትእዛዝioport, 0x11)

	Portመጻፊያbyte(Primarypicdataioport, 0x20)
	Portመጻፊያbyte(Secondarypicdataioport, 0x28)

	Portመጻፊያbyte(Primarypicdataioport, 0x04)
	Portመጻፊያbyte(Secondarypicdataioport, 0x02)

	Portመጻፊያbyte(Primarypicdataioport, 0x01)
	Portመጻፊያbyte(Secondarypicdataioport, 0x01)

	Portመጻፊያbyte(Primarypicdataioport, 0xF8)
	Portመጻፊያbyte(Secondarypicdataioport, 0xEF)

	idtጠቋሚ := [6]uint8{0, 0, 0, 0, 0, 0}
	መጠን := (*uint16)(Pointer(&idtጠቋሚ[0]))
	(*መጠን) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtጠቋሚ[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtጠቋሚ)))
}
func Lidt(lidtaddr uintptr)

func (self *Tማቋረጫmanager) Sማቋረጫdescriptorሰንጠረዥentryset(ማቋረጫ int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptorአይነት uint8) {

	handleraddressዝቅተኛቢትስ := (*uint16)(Pointer(&idtdata[ማቋረጫ*8+0]))
	(*handleraddressዝቅተኛቢትስ) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[ማቋረጫ*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[ማቋረጫ*8+4]))
	(*reserved) = 0

	var Idtdescriptorአሁን uint8 = 0x80
	መድረሻ := (*uint8)(Pointer(&idtdata[ማቋረጫ*8+5]))
	(*መድረሻ) = (Idtdescriptorአሁን | Descriptorአይነት | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressከፍተኛቢትስ := (*uint16)(Pointer(&idtdata[ማቋረጫ*8+6]))
	(*handleraddressከፍተኛቢትስ) = uint16((handler >> 16) & 0xFFFF)

}

func (self *Tማቋረጫmanager) Sethandler(handler uintptr, Iማቋረጫቁጥር uint8) {
	handler_2[Iማቋረጫቁጥር] = handler
}
func (self *Tማቋረጫmanager) Gethandler(Iማቋረጫቁጥር uint8) uintptr {
	return handler_2[Iማቋረጫቁጥር]
}
func (self *Tማቋረጫmanager) Dohandleማቋረጫ(ማቋረጫ uint8, esp uint32) uint32 {

	if ማቋረጫdebug {
		console_2.Mማተሚያxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32ማተሚያ(uint32(ማቋረጫ))
		console_2.Mማተሚያ(":")
		console_2.MUnsignedinteger32ማተሚያ(esp)
	}
	handlerማስኬጃ := false
	if handler_2[ማቋረጫ] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ማቋረጫ])))
		esp = myfunction(esp)
		handlerማስኬጃ = true

	}

	if !handlerማስኬጃ && ማቋረጫ == uint8(self.ጠንካራአካልማቋረጫoffset) && self.taskmanager != nil {
		esp = uint32(uintptr(Pointer(self.taskmanager.Schedule((*Tcpuሁኔታ)(Pointer(uintptr(esp)))))))

	}
	if !handlerማስኬጃ && ማቋረጫ == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if ማቋረጫ <= 0x1F {
	}
	if 0x20 <= ማቋረጫ && ማቋረጫ < 0x30 {
		if 0x28 <= ማቋረጫ {
			Portመጻፊያbyte(Secondarypicትእዛዝioport, 0x20)
		}
		Portመጻፊያbyte(Primarypicትእዛዝioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func setcr3(address uint32)

var console_2 TConsole = TConsole{}

func Handleማቋረጫ(esp uint32, ማቋረጫ uint32) uint32 {

	if ማቋረጫdebug && ማቋረጫ != 0x80 && ማቋረጫ != 0x20 {
		console_2.Mማተሚያxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32ማተሚያ(uint32(ማቋረጫ))
		console_2.Mማተሚያ(":")
		console_2.MUnsignedinteger32ማተሚያ(esp)
	}

	if Aአሰራማቋረጫmanager != 0 {
		p := (*Tማቋረጫmanager)(Pointer(Aአሰራማቋረጫmanager))
		esp = p.Dohandleማቋረጫ(uint8(ማቋረጫ), esp)
		return esp
	}
	if handler_2[ማቋረጫ] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ማቋረጫ])))
		esp = myfunction(esp)
	}
	if ማቋረጫ == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= ማቋረጫ && ማቋረጫ < 0x30 {
		if 0x28 <= ማቋረጫ {
			Portመጻፊያbyte(Secondarypicትእዛዝioport, 0x20)
		}
		Portመጻፊያbyte(Primarypicትእዛዝioport, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpuሁኔታ)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(ማቋረጫውጣloop).Pointer())
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

func exceptionhasስህተትcode(ማቋረጫ uint32) bool {
	switch ማቋረጫ {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionስም(ማቋረጫ uint32) string {
	switch ማቋረጫ {
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

func exceptionክፈፍዋጋ(ክፈፍ uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ክፈፍ + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func ማተሚያገጽfaultመረጃ(err uint32) {
	MEmergencylogሐረግ(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogሐረግ("protection")
	} else {
		MEmergencylogሐረግ("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogሐረግ(",write")
	} else {
		MEmergencylogሐረግ(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogሐረግ(",user")
	} else {
		MEmergencylogሐረግ(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogሐረግ(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogሐረግ(",instruction-fetch")
	}
	MEmergencylogሐረግ("]")
}

func ማተሚያexceptionselectorመረጃ(err uint32) {
	MEmergencylogሐረግ(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogሐረግ(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogሐረግ(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogሐረግ("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogሐረግ("LDT")
	} else {
		MEmergencylogሐረግ("GDT")
	}
	MEmergencylogሐረግ(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, ማቋረጫ uint32) uint32 {
	MEmergencylogሐረግ("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(ማቋረጫ))
	MEmergencylogሐረግ(" ")
	MEmergencylogሐረግ(exceptionስም(ማቋረጫ))
	MEmergencylogሐረግ(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogሐረግ(" invalid-frame")
		if exceptionhasስህተትcode(ማቋረጫ) {
			MEmergencylogሐረግ(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			ማተሚያexceptionselectorመረጃ(esp)
		}
		MEmergencylogሐረግ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasስህተትcode(ማቋረጫ) {
		err = exceptionክፈፍዋጋ(esp, 0)
		eipoffset = 4
	}
	eip := exceptionክፈፍዋጋ(esp, eipoffset)
	cs := exceptionክፈፍዋጋ(esp, eipoffset+4)
	eflags := exceptionክፈፍዋጋ(esp, eipoffset+8)

	MEmergencylogሐረግ(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogሐረግ(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogሐረግ(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogሐረግ(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogሐረግ(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogሐረግ(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if ማቋረጫ == 0x0E {
		MEmergencylogሐረግ(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		ማተሚያገጽfaultመረጃ(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogሐረግ(" useresp=")
		MEmergencylogunsignedinteger32(exceptionክፈፍዋጋ(esp, eipoffset+12))
		MEmergencylogሐረግ(" ss=")
		MEmergencylogunsignedinteger32(exceptionክፈፍዋጋ(esp, eipoffset+16))
	}

	if exceptionhasስህተትcode(ማቋረጫ) {
		ማተሚያexceptionselectorመረጃ(err)
	}
	MEmergencylogሐረግ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func Handlefatalማቋረጫክፈፍ(savedesp uint32, ማቋረጫ uint32) uint32 {
	Handleexception(savedesp+52, ማቋረጫ)
	haltafterfatalexception()
	return savedesp
}

func Iማቋረጫአሰራ()
func (self *Tማቋረጫmanager) Aአሰራ() {
	if Aአሰራማቋረጫmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	Aአሰራማቋረጫmanager = address
	Iማቋረጫአሰራ()
}
func Iማቋረጫdeactive()
func (self *Tማቋረጫmanager) Deactive() {
	Aአሰራማቋረጫmanager = 0
	Iማቋረጫdeactive()
}

func Myhandleማቋረጫ(ማቋረጫ uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.Mማተሚያ(buffer)
	return esp
}
func Myመሞከሪያ(ማቋረጫ uint8, esp uint32)

func Unhandleማቋረጫ() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.Mማተሚያ(buffer)
}

func ማቋረጫhandler_2(ማቋረጫ uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.Mማተሚያ(buffer)
	console_2.MHexadecimalማተሚያ(0x40)
	return esp
}
func ማተሚያesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32ማተሚያxy(esp, 20, 21)
}
func gettls() uint32
func Pማተሚያtls() {

}
