/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Iפסק

import . "unsafe"
import . "reflect"

import . "שער"
import . "gdt"
import . "multitasking"
import . "console"

func פסקignore()

func פסקexceptionhandler()
func פסקexceptionhandler0x00()
func פסקexceptionhandler0x01()
func פסקexceptionhandler0x02()
func פסקexceptionhandler0x03()
func פסקexceptionhandler0x04()
func פסקexceptionhandler0x05()
func פסקexceptionhandler0x06()
func פסקexceptionhandler0x07()
func פסקexceptionhandler0x08()
func פסקexceptionhandler0x09()
func פסקexceptionhandler0x0a()
func פסקexceptionhandler0x0b()
func פסקexceptionhandler0x0c()
func פסקexceptionhandler0x0d()
func פסקexceptionhandler0x0e()
func פסקexceptionhandler0x0f()
func פסקexceptionhandler0x10()
func פסקexceptionhandler0x11()
func פסקexceptionhandler0x12()
func פסקexceptionhandler0x13()

func פסקrequesthandler0x00()
func פסקrequesthandler0x01()
func פסקrequesthandler0x02()
func פסקrequesthandler0x03()
func פסקrequesthandler0x04()
func פסקrequesthandler0x05()
func פסקrequesthandler0x06()
func פסקrequesthandler0x07()
func פסקrequesthandler0x08()
func פסקrequesthandler0x09()
func פסקrequesthandler0x0a()
func פסקrequesthandler0x0b()
func פסקrequesthandler0x0c()
func פסקrequesthandler0x0d()
func פסקrequesthandler0x0e()
func פסקrequesthandler0x0f()

func פסקrequesthandler0x80()
func פסקrequesthandler0x81()
func פסקrequesthandler0x82()

func Tבדיקההדפסה(מיקום uint8, data uint8)
func קבעds(dssegment uint32)
func קבעgs(gssegment uint32)
func פסקיציאהloop()

type Tפסקhandler struct {
	Iפסקמספר	uint8
	Iפסקmanager	uintptr
}
type Iפסקhandler interface {
	Hידיתפסק(uint32) uint32
}

func Nחדשפסקhandler(Iפסקmanager uintptr, Iפסקמספר uint8) *Tפסקhandler {
	פסקhandler_2 := new(Tפסקhandler)
	פסקhandler_2.Iפסקמספר = Iפסקמספר
	פסקhandler_2.Iפסקmanager = Iפסקmanager
	return פסקhandler_2

}

var handler_2 [256]uintptr

func (self *Tפסקhandler) Init(Iפסקמספר uint8, Iפסקmanager uintptr, funcaddress uintptr) {

	handler_2[Iפסקמספר] = funcaddress

	self.Iפסקמספר = Iפסקמספר
	self.Iפסקmanager = Iפסקmanager

}
func (self *Tפסקhandler) Sקבעידיתפסקfuction(Iפסקמספר uint32, address uintptr) {
	handler_2[Iפסקמספר] = address
}
func (self *Tפסקhandler) Dהשמד() {
	selfuintptr := uintptr(Pointer(self))
	Iפסקmanager := (*Tפסקmanager)(Pointer(self.Iפסקmanager))
	if selfuintptr == Iפסקmanager.Gethandler(self.Iפסקמספר) {
		Iפסקmanager.Sקבעhandler(0, self.Iפסקמספר)
	}

}
func (self *Tפסקhandler) Sקבעפסקmanager(Iפסקmanager uintptr) {
}
func (self *Tפסקhandler) Sקבעפסקמספר(Iפסקמספר uint8) {
	self.Iפסקמספר = Iפסקמספר
}
func (self *Tפסקhandler) Hידיתפסק(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.Mהדפסה(buffer)
	return esp
}
func Hידיתפסק1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.Mהדפסה(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type Tפסקdescriptortableסמן struct {
}

var idtdata [256 * 8]uint8
var Aפעילפסקmanager uintptr = 0

const פסקניפויבאגים = false

type Tפסקmanager struct {
	handler_2	[256]uintptr

	חומרהפסקoffset	uint16

	משימהmanager	*Tמשימהmanager
}

var Primarypicפקודהioשער uint16 = 0x20
var Primarypicdataioשער uint16 = 0x21
var Secondarypicפקודהioשער uint16 = 0xA0
var Secondarypicdataioשער uint16 = 0xA1

func (self *Tפסקmanager) Init(חומרהפסקoffset uint16, גלובליdescriptortable *TShareddescriptortable, משימהmanager *Tמשימהmanager) {

	self.משימהmanager = משימהmanager

	self.חומרהפסקoffset = חומרהפסקoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var Idtפסקgate uint8 = 0xE
	address = uint32(ValueOf(פסקignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(פסקexceptionhandler0x0f).Pointer())
		self.Sפסקdescriptortableentryקבע(i, codesegment, address, 0, Idtפסקgate)
	}

	address = uint32(ValueOf(פסקexceptionhandler0x00).Pointer())
	self.Sפסקdescriptortableentryקבע(0x00, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x01).Pointer())
	self.Sפסקdescriptortableentryקבע(0x01, codesegment, address, 0, Idtפסקgate)
	address = uint32(ValueOf(פסקexceptionhandler0x02).Pointer())
	self.Sפסקdescriptortableentryקבע(0x02, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x03).Pointer())
	self.Sפסקdescriptortableentryקבע(0x03, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x04).Pointer())
	self.Sפסקdescriptortableentryקבע(0x04, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x05).Pointer())
	self.Sפסקdescriptortableentryקבע(0x05, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x06).Pointer())
	self.Sפסקdescriptortableentryקבע(0x06, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x07).Pointer())
	self.Sפסקdescriptortableentryקבע(0x07, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x08).Pointer())
	self.Sפסקdescriptortableentryקבע(0x08, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x09).Pointer())
	self.Sפסקdescriptortableentryקבע(0x09, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x0a).Pointer())
	self.Sפסקdescriptortableentryקבע(0x0A, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x0b).Pointer())
	self.Sפסקdescriptortableentryקבע(0x0B, codesegment, address, 0, Idtפסקgate)
	address = uint32(ValueOf(פסקexceptionhandler0x0c).Pointer())
	self.Sפסקdescriptortableentryקבע(0x0C, codesegment, address, 0, Idtפסקgate)
	address = uint32(ValueOf(פסקexceptionhandler0x0d).Pointer())
	self.Sפסקdescriptortableentryקבע(0x0D, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x0e).Pointer())
	self.Sפסקdescriptortableentryקבע(0x0E, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x0f).Pointer())
	self.Sפסקdescriptortableentryקבע(0x0F, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x10).Pointer())
	self.Sפסקdescriptortableentryקבע(0x10, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x11).Pointer())
	self.Sפסקdescriptortableentryקבע(0x11, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x12).Pointer())
	self.Sפסקdescriptortableentryקבע(0x12, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקexceptionhandler0x13).Pointer())
	self.Sפסקdescriptortableentryקבע(0x13, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x00).Pointer())
	self.Sפסקdescriptortableentryקבע(0x20, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x01).Pointer())
	self.Sפסקdescriptortableentryקבע(0x21, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x02).Pointer())
	self.Sפסקdescriptortableentryקבע(0x22, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x03).Pointer())
	self.Sפסקdescriptortableentryקבע(0x23, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x04).Pointer())
	self.Sפסקdescriptortableentryקבע(0x24, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x05).Pointer())
	self.Sפסקdescriptortableentryקבע(0x25, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x06).Pointer())
	self.Sפסקdescriptortableentryקבע(0x26, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x07).Pointer())
	self.Sפסקdescriptortableentryקבע(0x27, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x08).Pointer())
	self.Sפסקdescriptortableentryקבע(0x28, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x09).Pointer())
	self.Sפסקdescriptortableentryקבע(0x29, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x0a).Pointer())
	self.Sפסקdescriptortableentryקבע(0x2A, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x0b).Pointer())
	self.Sפסקdescriptortableentryקבע(0x2B, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x0c).Pointer())
	self.Sפסקdescriptortableentryקבע(0x2C, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x0d).Pointer())
	self.Sפסקdescriptortableentryקבע(0x2D, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x0e).Pointer())
	self.Sפסקdescriptortableentryקבע(0x2E, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x0f).Pointer())
	self.Sפסקdescriptortableentryקבע(0x2F, codesegment, address, 0, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x80).Pointer())
	self.Sפסקdescriptortableentryקבע(0x80, codesegment, address, 3, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x81).Pointer())
	self.Sפסקdescriptortableentryקבע(0x81, codesegment, address, 3, Idtפסקgate)

	address = uint32(ValueOf(פסקrequesthandler0x82).Pointer())
	self.Sפסקdescriptortableentryקבע(0x82, codesegment, address, 3, Idtפסקgate)

	Pשערכתיבהbyte(Primarypicפקודהioשער, 0x11)
	Pשערכתיבהbyte(Secondarypicפקודהioשער, 0x11)

	Pשערכתיבהbyte(Primarypicdataioשער, 0x20)
	Pשערכתיבהbyte(Secondarypicdataioשער, 0x28)

	Pשערכתיבהbyte(Primarypicdataioשער, 0x04)
	Pשערכתיבהbyte(Secondarypicdataioשער, 0x02)

	Pשערכתיבהbyte(Primarypicdataioשער, 0x01)
	Pשערכתיבהbyte(Secondarypicdataioשער, 0x01)

	Pשערכתיבהbyte(Primarypicdataioשער, 0xF8)
	Pשערכתיבהbyte(Secondarypicdataioשער, 0xEF)

	idtסמן := [6]uint8{0, 0, 0, 0, 0, 0}
	גודל := (*uint16)(Pointer(&idtסמן[0]))
	(*גודל) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtסמן[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtסמן)))
}
func Lidt(lidtaddr uintptr)

func (self *Tפסקmanager) Sפסקdescriptortableentryקבע(פסק int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptorסוג uint8) {

	handleraddressנמוךסיביות := (*uint16)(Pointer(&idtdata[פסק*8+0]))
	(*handleraddressנמוךסיביות) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[פסק*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[פסק*8+4]))
	(*reserved) = 0

	var Idtdescriptorנוכח uint8 = 0x80
	גישה := (*uint8)(Pointer(&idtdata[פסק*8+5]))
	(*גישה) = (Idtdescriptorנוכח | Descriptorסוג | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressגבוההסיביות := (*uint16)(Pointer(&idtdata[פסק*8+6]))
	(*handleraddressגבוההסיביות) = uint16((handler >> 16) & 0xFFFF)

}

func (self *Tפסקmanager) Sקבעhandler(handler uintptr, Iפסקמספר uint8) {
	handler_2[Iפסקמספר] = handler
}
func (self *Tפסקmanager) Gethandler(Iפסקמספר uint8) uintptr {
	return handler_2[Iפסקמספר]
}
func (self *Tפסקmanager) Doידיתפסק(פסק uint8, esp uint32) uint32 {

	if פסקניפויבאגים {
		console_2.Mהדפסהxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32הדפסה(uint32(פסק))
		console_2.Mהדפסה(":")
		console_2.MUnsignedinteger32הדפסה(esp)
	}
	handlerהפעלה := false
	if handler_2[פסק] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[פסק])))
		esp = myfunction(esp)
		handlerהפעלה = true

	}

	if !handlerהפעלה && פסק == uint8(self.חומרהפסקoffset) && self.משימהmanager != nil {
		esp = uint32(uintptr(Pointer(self.משימהmanager.Schedule((*Tcpuמצב)(Pointer(uintptr(esp)))))))

	}
	if !handlerהפעלה && פסק == 0x80 {
		esp = ידיתunhandledsyscall(esp)
	}

	if פסק <= 0x1F {
	}
	if 0x20 <= פסק && פסק < 0x30 {
		if 0x28 <= פסק {
			Pשערכתיבהbyte(Secondarypicפקודהioשער, 0x20)
		}
		Pשערכתיבהbyte(Primarypicפקודהioשער, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func קבעcr3(address uint32)

var console_2 TConsole = TConsole{}

func Hידיתפסק(esp uint32, פסק uint32) uint32 {

	if פסקניפויבאגים && פסק != 0x80 && פסק != 0x20 {
		console_2.Mהדפסהxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32הדפסה(uint32(פסק))
		console_2.Mהדפסה(":")
		console_2.MUnsignedinteger32הדפסה(esp)
	}

	if Aפעילפסקmanager != 0 {
		p := (*Tפסקmanager)(Pointer(Aפעילפסקmanager))
		esp = p.Doידיתפסק(uint8(פסק), esp)
		return esp
	}
	if handler_2[פסק] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[פסק])))
		esp = myfunction(esp)
	}
	if פסק == 0x80 {
		return ידיתunhandledsyscall(esp)
	}
	if 0x20 <= פסק && פסק < 0x30 {
		if 0x28 <= פסק {
			Pשערכתיבהbyte(Secondarypicפקודהioשער, 0x20)
		}
		Pשערכתיבהbyte(Primarypicפקודהioשער, 0x20)
	}

	return esp
}

func ידיתunhandledsyscall(esp uint32) uint32 {
	מעבד := (*Tcpuמצב)(Pointer(uintptr(esp)))
	if מעבד.Eax == 1 || מעבד.Eax == 252 {
		מעבד.Eip = uint32(ValueOf(פסקיציאהloop).Pointer())
		מעבד.Cs = Segkernelcode
		מעבד.Ds = Segkerneldata
		מעבד.Es = Segkerneldata
		מעבד.Fs = Segkerneldata
		מעבד.Gs = Segkernelgs
		מעבד.Ss = Segkerneldata
		מעבד.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasשגיאהcode(פסק uint32) bool {
	switch פסק {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionשם(פסק uint32) string {
	switch פסק {
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

func exceptionframeערך(frame uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(frame + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func הדפסהעמודfaultמידע(שגיאה uint32) {
	MEmergencyיומןמחרוזת(" pf=[")
	if (שגיאה & 0x01) != 0 {
		MEmergencyיומןמחרוזת("protection")
	} else {
		MEmergencyיומןמחרוזת("not-present")
	}
	if (שגיאה & 0x02) != 0 {
		MEmergencyיומןמחרוזת(",write")
	} else {
		MEmergencyיומןמחרוזת(",read")
	}
	if (שגיאה & 0x04) != 0 {
		MEmergencyיומןמחרוזת(",user")
	} else {
		MEmergencyיומןמחרוזת(",kernel")
	}
	if (שגיאה & 0x08) != 0 {
		MEmergencyיומןמחרוזת(",reserved-bit")
	}
	if (שגיאה & 0x10) != 0 {
		MEmergencyיומןמחרוזת(",instruction-fetch")
	}
	MEmergencyיומןמחרוזת("]")
}

func הדפסהexceptionselectorמידע(שגיאה uint32) {
	MEmergencyיומןמחרוזת(" selector=")
	MEmergencyיומןunsignedinteger32(שגיאה & 0xFFFFFFF8)
	MEmergencyיומןמחרוזת(" index=")
	MEmergencyיומןunsignedinteger32(שגיאה >> 3)
	MEmergencyיומןמחרוזת(" table=")
	if (שגיאה & 0x02) != 0 {
		MEmergencyיומןמחרוזת("IDT")
	} else if (שגיאה & 0x04) != 0 {
		MEmergencyיומןמחרוזת("LDT")
	} else {
		MEmergencyיומןמחרוזת("GDT")
	}
	MEmergencyיומןמחרוזת(" ext=")
	MEmergencyיומןunsignedinteger32(שגיאה & 0x01)
}

func Hידיתexception(esp uint32, פסק uint32) uint32 {
	MEmergencyיומןמחרוזת("\nEXCEPTION vec=")
	MEmergencyיומןhexadecimal8(uint8(פסק))
	MEmergencyיומןמחרוזת(" ")
	MEmergencyיומןמחרוזת(exceptionשם(פסק))
	MEmergencyיומןמחרוזת(" frame=")
	MEmergencyיומןunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyיומןמחרוזת(" invalid-frame")
		if exceptionhasשגיאהcode(פסק) {
			MEmergencyיומןמחרוזת(" raw-error-or-bad-esp=")
			MEmergencyיומןunsignedinteger32(esp)
			הדפסהexceptionselectorמידע(esp)
		}
		MEmergencyיומןמחרוזת("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var שגיאה uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasשגיאהcode(פסק) {
		שגיאה = exceptionframeערך(esp, 0)
		eipoffset = 4
	}
	eip := exceptionframeערך(esp, eipoffset)
	cs := exceptionframeערך(esp, eipoffset+4)
	eflags := exceptionframeערך(esp, eipoffset+8)

	MEmergencyיומןמחרוזת(" err=")
	MEmergencyיומןunsignedinteger32(שגיאה)
	MEmergencyיומןמחרוזת(" eip=")
	MEmergencyיומןunsignedinteger32(eip)
	MEmergencyיומןמחרוזת(" cs=")
	MEmergencyיומןunsignedinteger32(cs)
	MEmergencyיומןמחרוזת(" eflags=")
	MEmergencyיומןunsignedinteger32(eflags)
	MEmergencyיומןמחרוזת(" cr0=")
	MEmergencyיומןunsignedinteger32(exceptioncr0())
	MEmergencyיומןמחרוזת(" cr3=")
	MEmergencyיומןunsignedinteger32(exceptioncr3())

	if פסק == 0x0E {
		MEmergencyיומןמחרוזת(" cr2=")
		MEmergencyיומןunsignedinteger32(exceptioncr2())
		הדפסהעמודfaultמידע(שגיאה)
	}

	if (cs & 0x03) != 0 {
		MEmergencyיומןמחרוזת(" useresp=")
		MEmergencyיומןunsignedinteger32(exceptionframeערך(esp, eipoffset+12))
		MEmergencyיומןמחרוזת(" ss=")
		MEmergencyיומןunsignedinteger32(exceptionframeערך(esp, eipoffset+16))
	}

	if exceptionhasשגיאהcode(פסק) {
		הדפסהexceptionselectorמידע(שגיאה)
	}
	MEmergencyיומןמחרוזת("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func Hידיתfatalפסקframe(savedesp uint32, פסק uint32) uint32 {
	Hידיתexception(savedesp+52, פסק)
	haltafterfatalexception()
	return savedesp
}

func Iפסקפעיל()
func (self *Tפסקmanager) Aפעיל() {
	if Aפעילפסקmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	Aפעילפסקmanager = address
	Iפסקפעיל()
}
func Iפסקdeactive()
func (self *Tפסקmanager) Deactive() {
	Aפעילפסקmanager = 0
	Iפסקdeactive()
}

func Myידיתפסק(פסק uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.Mהדפסה(buffer)
	return esp
}
func Myבדיקה(פסק uint8, esp uint32)

func Unhandleפסק() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.Mהדפסה(buffer)
}

func פסקhandler_2(פסק uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.Mהדפסה(buffer)
	console_2.MHexadecimalהדפסה(0x40)
	return esp
}
func הדפסהesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32הדפסהxy(esp, 20, 21)
}
func gettls() uint32
func Pהדפסהtls() {

}
