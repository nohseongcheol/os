package Iمقاطعة

import . "unsafe"
import . "reflect"

import . "منفذ"
import . "gdt"
import . "متعددإدارةمهام"
import . "طرفية"

func مقاطعةignore()

func مقاطعةexceptionhandler()
func مقاطعةexceptionhandler0x00()
func مقاطعةexceptionhandler0x01()
func مقاطعةexceptionhandler0x02()
func مقاطعةexceptionhandler0x03()
func مقاطعةexceptionhandler0x04()
func مقاطعةexceptionhandler0x05()
func مقاطعةexceptionhandler0x06()
func مقاطعةexceptionhandler0x07()
func مقاطعةexceptionhandler0x08()
func مقاطعةexceptionhandler0x09()
func مقاطعةexceptionhandler0x0a()
func مقاطعةexceptionhandler0x0b()
func مقاطعةexceptionhandler0x0c()
func مقاطعةexceptionhandler0x0d()
func مقاطعةexceptionhandler0x0e()
func مقاطعةexceptionhandler0x0f()
func مقاطعةexceptionhandler0x10()
func مقاطعةexceptionhandler0x11()
func مقاطعةexceptionhandler0x12()
func مقاطعةexceptionhandler0x13()

func مقاطعةrequesthandler0x00()
func مقاطعةrequesthandler0x01()
func مقاطعةrequesthandler0x02()
func مقاطعةrequesthandler0x03()
func مقاطعةrequesthandler0x04()
func مقاطعةrequesthandler0x05()
func مقاطعةrequesthandler0x06()
func مقاطعةrequesthandler0x07()
func مقاطعةrequesthandler0x08()
func مقاطعةrequesthandler0x09()
func مقاطعةrequesthandler0x0a()
func مقاطعةrequesthandler0x0b()
func مقاطعةrequesthandler0x0c()
func مقاطعةrequesthandler0x0d()
func مقاطعةrequesthandler0x0e()
func مقاطعةrequesthandler0x0f()

func مقاطعةrequesthandler0x80()
func مقاطعةrequesthandler0x81()
func مقاطعةrequesthandler0x82()

func Tتجريباطبع(الموضع uint8, بيانات uint8)
func تحديدds(dssegment uint32)
func تحديدgs(gssegment uint32)
func مقاطعةخروجloop()

type Tمقاطعةhandler struct {
	Iمقاطعةالأرقام	uint8
	Iمقاطعةمدير	uintptr
}
type Iمقاطعةhandler interface {
	Hالتعاملمقاطعة(uint32) uint32
}

func Nجديدمقاطعةhandler(Iمقاطعةمدير uintptr, Iمقاطعةالأرقام uint8) *Tمقاطعةhandler {
	مقاطعةhandler_2 := new(Tمقاطعةhandler)
	مقاطعةhandler_2.Iمقاطعةالأرقام = Iمقاطعةالأرقام
	مقاطعةhandler_2.Iمقاطعةمدير = Iمقاطعةمدير
	return مقاطعةhandler_2

}

var handler_2 [256]uintptr

func (نفسه *Tمقاطعةhandler) Init(Iمقاطعةالأرقام uint8, Iمقاطعةمدير uintptr, funcaddress uintptr) {

	handler_2[Iمقاطعةالأرقام] = funcaddress

	نفسه.Iمقاطعةالأرقام = Iمقاطعةالأرقام
	نفسه.Iمقاطعةمدير = Iمقاطعةمدير

}
func (نفسه *Tمقاطعةhandler) Sتحديدالتعاملمقاطعةfuction(Iمقاطعةالأرقام uint32, address uintptr) {
	handler_2[Iمقاطعةالأرقام] = address
}
func (نفسه *Tمقاطعةhandler) Destroy() {
	نفسهuintptr := uintptr(Pointer(نفسه))
	Iمقاطعةمدير := (*Tمقاطعةمدير)(Pointer(نفسه.Iمقاطعةمدير))
	if نفسهuintptr == Iمقاطعةمدير.Gethandler(نفسه.Iمقاطعةالأرقام) {
		Iمقاطعةمدير.Sتحديدhandler(0, نفسه.Iمقاطعةالأرقام)
	}

}
func (نفسه *Tمقاطعةhandler) Sتحديدمقاطعةمدير(Iمقاطعةمدير uintptr) {
}
func (نفسه *Tمقاطعةhandler) Sتحديدمقاطعةالأرقام(Iمقاطعةالأرقام uint8) {
	نفسه.Iمقاطعةالأرقام = Iمقاطعةالأرقام
}
func (نفسه *Tمقاطعةhandler) Hالتعاملمقاطعة(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	طرفية_2 := Tطرفية{}
	طرفية_2.Mاطبع(buffer)
	return esp
}
func Hالتعاملمقاطعة1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	طرفية_2 := Tطرفية{}
	طرفية_2.Mاطبع(buffer)
}

type Tبوابةdescriptor struct {
	بوابةبيانات [8]uint8
}
type Tمقاطعةdescriptorجدولالمؤشر struct {
}

var idtبيانات [256 * 8]uint8
var Aنشطمقاطعةمدير uintptr = 0

const مقاطعةتنقيح = false

type Tمقاطعةمدير struct {
	handler_2	[256]uintptr

	العتادمقاطعةoffset	uint16

	مهمةمدير	*Tمهمةمدير
}

var Primarypicأمرioمنفذ uint16 = 0x20
var Primarypicبياناتioمنفذ uint16 = 0x21
var Secondarypicأمرioمنفذ uint16 = 0xA0
var Secondarypicبياناتioمنفذ uint16 = 0xA1

func (نفسه *Tمقاطعةمدير) Init(العتادمقاطعةoffset uint16, الاختصارالعامdescriptorجدول *TShareddescriptorجدول, مهمةمدير *Tمهمةمدير) {

	نفسه.مهمةمدير = مهمةمدير

	نفسه.العتادمقاطعةoffset = العتادمقاطعةoffset
	codesegment := uint16(Segنواةcode)

	for i := 0; i < (256 * 8); i++ {
		idtبيانات[i] = 0
	}
	var address uint32
	var Idtمقاطعةبوابة uint8 = 0xE
	address = uint32(ValueOf(مقاطعةignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(مقاطعةexceptionhandler0x0f).Pointer())
		نفسه.Sمقاطعةdescriptorجدولentryتحديد(i, codesegment, address, 0, Idtمقاطعةبوابة)
	}

	address = uint32(ValueOf(مقاطعةexceptionhandler0x00).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x00, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x01).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x01, codesegment, address, 0, Idtمقاطعةبوابة)
	address = uint32(ValueOf(مقاطعةexceptionhandler0x02).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x02, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x03).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x03, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x04).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x04, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x05).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x05, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x06).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x06, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x07).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x07, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x08).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x08, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x09).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x09, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x0a).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x0A, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x0b).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x0B, codesegment, address, 0, Idtمقاطعةبوابة)
	address = uint32(ValueOf(مقاطعةexceptionhandler0x0c).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x0C, codesegment, address, 0, Idtمقاطعةبوابة)
	address = uint32(ValueOf(مقاطعةexceptionhandler0x0d).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x0D, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x0e).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x0E, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x0f).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x0F, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x10).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x10, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x11).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x11, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x12).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x12, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةexceptionhandler0x13).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x13, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x00).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x20, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x01).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x21, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x02).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x22, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x03).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x23, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x04).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x24, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x05).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x25, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x06).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x26, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x07).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x27, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x08).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x28, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x09).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x29, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x0a).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x2A, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x0b).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x2B, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x0c).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x2C, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x0d).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x2D, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x0e).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x2E, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x0f).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x2F, codesegment, address, 0, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x80).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x80, codesegment, address, 3, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x81).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x81, codesegment, address, 3, Idtمقاطعةبوابة)

	address = uint32(ValueOf(مقاطعةrequesthandler0x82).Pointer())
	نفسه.Sمقاطعةdescriptorجدولentryتحديد(0x82, codesegment, address, 3, Idtمقاطعةبوابة)

	Pمنفذكتابةبايت(Primarypicأمرioمنفذ, 0x11)
	Pمنفذكتابةبايت(Secondarypicأمرioمنفذ, 0x11)

	Pمنفذكتابةبايت(Primarypicبياناتioمنفذ, 0x20)
	Pمنفذكتابةبايت(Secondarypicبياناتioمنفذ, 0x28)

	Pمنفذكتابةبايت(Primarypicبياناتioمنفذ, 0x04)
	Pمنفذكتابةبايت(Secondarypicبياناتioمنفذ, 0x02)

	Pمنفذكتابةبايت(Primarypicبياناتioمنفذ, 0x01)
	Pمنفذكتابةبايت(Secondarypicبياناتioمنفذ, 0x01)

	Pمنفذكتابةبايت(Primarypicبياناتioمنفذ, 0xF8)
	Pمنفذكتابةبايت(Secondarypicبياناتioمنفذ, 0xEF)

	idtالمؤشر := [6]uint8{0, 0, 0, 0, 0, 0}
	الحجم := (*uint16)(Pointer(&idtالمؤشر[0]))
	(*الحجم) = (uint16)(Sizeof(idtبيانات) - 1)

	base := (*uint32)(Pointer(&idtالمؤشر[2]))
	(*base) = uint32(uintptr(Pointer(&idtبيانات)))

	Lidt(uintptr(Pointer(&idtالمؤشر)))
}
func Lidt(lidtaddr uintptr)

func (نفسه *Tمقاطعةمدير) Sمقاطعةdescriptorجدولentryتحديد(مقاطعة int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptorنوع uint8) {

	handleraddressمنخفضبت := (*uint16)(Pointer(&idtبيانات[مقاطعة*8+0]))
	(*handleraddressمنخفضبت) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtبيانات[مقاطعة*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtبيانات[مقاطعة*8+4]))
	(*reserved) = 0

	var Idtdescriptorالحالي uint8 = 0x80
	نفاذ := (*uint8)(Pointer(&idtبيانات[مقاطعة*8+5]))
	(*نفاذ) = (Idtdescriptorالحالي | Descriptorنوع | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressعاليةبت := (*uint16)(Pointer(&idtبيانات[مقاطعة*8+6]))
	(*handleraddressعاليةبت) = uint16((handler >> 16) & 0xFFFF)

}

func (نفسه *Tمقاطعةمدير) Sتحديدhandler(handler uintptr, Iمقاطعةالأرقام uint8) {
	handler_2[Iمقاطعةالأرقام] = handler
}
func (نفسه *Tمقاطعةمدير) Gethandler(Iمقاطعةالأرقام uint8) uintptr {
	return handler_2[Iمقاطعةالأرقام]
}
func (نفسه *Tمقاطعةمدير) Doالتعاملمقاطعة(مقاطعة uint8, esp uint32) uint32 {

	if مقاطعةتنقيح {
		طرفية_2.Mاطبعxy("[esp:", 1, 20)
		طرفية_2.MUnsignedinteger32اطبع(uint32(مقاطعة))
		طرفية_2.Mاطبع(":")
		طرفية_2.MUnsignedinteger32اطبع(esp)
	}
	handlerrun := false
	if handler_2[مقاطعة] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[مقاطعة])))
		esp = myfunction(esp)
		handlerrun = true

	}

	if !handlerrun && مقاطعة == uint8(نفسه.العتادمقاطعةoffset) && نفسه.مهمةمدير != nil {
		esp = uint32(uintptr(Pointer(نفسه.مهمةمدير.Schedule((*Tcpuالحالة)(Pointer(uintptr(esp)))))))

	}
	if !handlerrun && مقاطعة == 0x80 {
		esp = التعاملunhandledsyscall(esp)
	}

	if مقاطعة <= 0x1F {
	}
	if 0x20 <= مقاطعة && مقاطعة < 0x30 {
		if 0x28 <= مقاطعة {
			Pمنفذكتابةبايت(Secondarypicأمرioمنفذ, 0x20)
		}
		Pمنفذكتابةبايت(Primarypicأمرioمنفذ, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func تحديدcr3(address uint32)

var طرفية_2 Tطرفية = Tطرفية{}

func Hالتعاملمقاطعة(esp uint32, مقاطعة uint32) uint32 {

	if مقاطعةتنقيح && مقاطعة != 0x80 && مقاطعة != 0x20 {
		طرفية_2.Mاطبعxy("[esp:", 1, 21)
		طرفية_2.MUnsignedinteger32اطبع(uint32(مقاطعة))
		طرفية_2.Mاطبع(":")
		طرفية_2.MUnsignedinteger32اطبع(esp)
	}

	if Aنشطمقاطعةمدير != 0 {
		p := (*Tمقاطعةمدير)(Pointer(Aنشطمقاطعةمدير))
		esp = p.Doالتعاملمقاطعة(uint8(مقاطعة), esp)
		return esp
	}
	if handler_2[مقاطعة] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[مقاطعة])))
		esp = myfunction(esp)
	}
	if مقاطعة == 0x80 {
		return التعاملunhandledsyscall(esp)
	}
	if 0x20 <= مقاطعة && مقاطعة < 0x30 {
		if 0x28 <= مقاطعة {
			Pمنفذكتابةبايت(Secondarypicأمرioمنفذ, 0x20)
		}
		Pمنفذكتابةبايت(Primarypicأمرioمنفذ, 0x20)
	}

	return esp
}

func التعاملunhandledsyscall(esp uint32) uint32 {
	المعالج := (*Tcpuالحالة)(Pointer(uintptr(esp)))
	if المعالج.Eax == 1 || المعالج.Eax == 252 {
		المعالج.Eip = uint32(ValueOf(مقاطعةخروجloop).Pointer())
		المعالج.Cs = Segنواةcode
		المعالج.Ds = Segنواةبيانات
		المعالج.Es = Segنواةبيانات
		المعالج.Fs = Segنواةبيانات
		المعالج.Gs = Segنواةgs
		المعالج.Ss = Segنواةبيانات
		المعالج.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasخطأcode(مقاطعة uint32) bool {
	switch مقاطعة {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionالاسم(مقاطعة uint32) string {
	switch مقاطعة {
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

func exceptionإطارالقيمة(إطار uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(إطار + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func اطبعصفحةخللمعلومات(خطأ uint32) {
	MEmergencyالسجلسلسلة(" pf=[")
	if (خطأ & 0x01) != 0 {
		MEmergencyالسجلسلسلة("protection")
	} else {
		MEmergencyالسجلسلسلة("not-present")
	}
	if (خطأ & 0x02) != 0 {
		MEmergencyالسجلسلسلة(",write")
	} else {
		MEmergencyالسجلسلسلة(",read")
	}
	if (خطأ & 0x04) != 0 {
		MEmergencyالسجلسلسلة(",user")
	} else {
		MEmergencyالسجلسلسلة(",kernel")
	}
	if (خطأ & 0x08) != 0 {
		MEmergencyالسجلسلسلة(",reserved-bit")
	}
	if (خطأ & 0x10) != 0 {
		MEmergencyالسجلسلسلة(",instruction-fetch")
	}
	MEmergencyالسجلسلسلة("]")
}

func اطبعexceptionselectorمعلومات(خطأ uint32) {
	MEmergencyالسجلسلسلة(" selector=")
	MEmergencyالسجلunsignedinteger32(خطأ & 0xFFFFFFF8)
	MEmergencyالسجلسلسلة(" index=")
	MEmergencyالسجلunsignedinteger32(خطأ >> 3)
	MEmergencyالسجلسلسلة(" table=")
	if (خطأ & 0x02) != 0 {
		MEmergencyالسجلسلسلة("IDT")
	} else if (خطأ & 0x04) != 0 {
		MEmergencyالسجلسلسلة("LDT")
	} else {
		MEmergencyالسجلسلسلة("GDT")
	}
	MEmergencyالسجلسلسلة(" ext=")
	MEmergencyالسجلunsignedinteger32(خطأ & 0x01)
}

func Hالتعاملexception(esp uint32, مقاطعة uint32) uint32 {
	MEmergencyالسجلسلسلة("\nEXCEPTION vec=")
	MEmergencyالسجلhexadecimal8(uint8(مقاطعة))
	MEmergencyالسجلسلسلة(" ")
	MEmergencyالسجلسلسلة(exceptionالاسم(مقاطعة))
	MEmergencyالسجلسلسلة(" frame=")
	MEmergencyالسجلunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyالسجلسلسلة(" invalid-frame")
		if exceptionhasخطأcode(مقاطعة) {
			MEmergencyالسجلسلسلة(" raw-error-or-bad-esp=")
			MEmergencyالسجلunsignedinteger32(esp)
			اطبعexceptionselectorمعلومات(esp)
		}
		MEmergencyالسجلسلسلة("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var خطأ uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasخطأcode(مقاطعة) {
		خطأ = exceptionإطارالقيمة(esp, 0)
		eipoffset = 4
	}
	eip := exceptionإطارالقيمة(esp, eipoffset)
	cs := exceptionإطارالقيمة(esp, eipoffset+4)
	eflags := exceptionإطارالقيمة(esp, eipoffset+8)

	MEmergencyالسجلسلسلة(" err=")
	MEmergencyالسجلunsignedinteger32(خطأ)
	MEmergencyالسجلسلسلة(" eip=")
	MEmergencyالسجلunsignedinteger32(eip)
	MEmergencyالسجلسلسلة(" cs=")
	MEmergencyالسجلunsignedinteger32(cs)
	MEmergencyالسجلسلسلة(" eflags=")
	MEmergencyالسجلunsignedinteger32(eflags)
	MEmergencyالسجلسلسلة(" cr0=")
	MEmergencyالسجلunsignedinteger32(exceptioncr0())
	MEmergencyالسجلسلسلة(" cr3=")
	MEmergencyالسجلunsignedinteger32(exceptioncr3())

	if مقاطعة == 0x0E {
		MEmergencyالسجلسلسلة(" cr2=")
		MEmergencyالسجلunsignedinteger32(exceptioncr2())
		اطبعصفحةخللمعلومات(خطأ)
	}

	if (cs & 0x03) != 0 {
		MEmergencyالسجلسلسلة(" useresp=")
		MEmergencyالسجلunsignedinteger32(exceptionإطارالقيمة(esp, eipoffset+12))
		MEmergencyالسجلسلسلة(" ss=")
		MEmergencyالسجلunsignedinteger32(exceptionإطارالقيمة(esp, eipoffset+16))
	}

	if exceptionhasخطأcode(مقاطعة) {
		اطبعexceptionselectorمعلومات(خطأ)
	}
	MEmergencyالسجلسلسلة("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltبعدfatalexception()

func Hالتعاملfatalمقاطعةإطار(savedesp uint32, مقاطعة uint32) uint32 {
	Hالتعاملexception(savedesp+52, مقاطعة)
	haltبعدfatalexception()
	return savedesp
}

func Iمقاطعةنشط()
func (نفسه *Tمقاطعةمدير) Aنشط() {
	if Aنشطمقاطعةمدير != 0 {
		نفسه.Deactive()
	}
	address := uintptr(Pointer(نفسه))
	Aنشطمقاطعةمدير = address
	Iمقاطعةنشط()
}
func Iمقاطعةdeactive()
func (نفسه *Tمقاطعةمدير) Deactive() {
	Aنشطمقاطعةمدير = 0
	Iمقاطعةdeactive()
}

func Myالتعاملمقاطعة(مقاطعة uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	طرفية_2 := Tطرفية{}
	طرفية_2.Mاطبع(buffer)
	return esp
}
func Myتجريب(مقاطعة uint8, esp uint32)

func Unhandleمقاطعة() {
	buffer := []byte("unhandle interrupt\n")
	طرفية_2 := Tطرفية{}
	طرفية_2.Mاطبع(buffer)
}

func مقاطعةhandler_2(مقاطعة uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	طرفية_2 := Tطرفية{}
	طرفية_2.Mاطبع(buffer)
	طرفية_2.MHexadecimalاطبع(0x40)
	return esp
}
func اطبعesp(esp uint32) {
	طرفية_2 := Tطرفية{}
	طرفية_2.MUnsignedinteger32اطبعxy(esp, 20, 21)
}
func gettls() uint32
func Pاطبعtls() {

}
