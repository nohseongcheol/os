/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Iわりこみ

import . "unsafe"
import . "reflect"

import . "ぽーと"
import . "gdt"
import . "ふくすうたすくかんり"
import . "こんそーる"

func わりこみignore()

func わりこみexceptionhandler()
func わりこみexceptionhandler0x00()
func わりこみexceptionhandler0x01()
func わりこみexceptionhandler0x02()
func わりこみexceptionhandler0x03()
func わりこみexceptionhandler0x04()
func わりこみexceptionhandler0x05()
func わりこみexceptionhandler0x06()
func わりこみexceptionhandler0x07()
func わりこみexceptionhandler0x08()
func わりこみexceptionhandler0x09()
func わりこみexceptionhandler0x0a()
func わりこみexceptionhandler0x0b()
func わりこみexceptionhandler0x0c()
func わりこみexceptionhandler0x0d()
func わりこみexceptionhandler0x0e()
func わりこみexceptionhandler0x0f()
func わりこみexceptionhandler0x10()
func わりこみexceptionhandler0x11()
func わりこみexceptionhandler0x12()
func わりこみexceptionhandler0x13()

func わりこみrequesthandler0x00()
func わりこみrequesthandler0x01()
func わりこみrequesthandler0x02()
func わりこみrequesthandler0x03()
func わりこみrequesthandler0x04()
func わりこみrequesthandler0x05()
func わりこみrequesthandler0x06()
func わりこみrequesthandler0x07()
func わりこみrequesthandler0x08()
func わりこみrequesthandler0x09()
func わりこみrequesthandler0x0a()
func わりこみrequesthandler0x0b()
func わりこみrequesthandler0x0c()
func わりこみrequesthandler0x0d()
func わりこみrequesthandler0x0e()
func わりこみrequesthandler0x0f()

func わりこみrequesthandler0x80()
func わりこみrequesthandler0x81()
func わりこみrequesthandler0x82()

func Tてすといんさつ(はいち uint8, でーた uint8)
func ありds(dssegment uint32)
func ありgs(gssegment uint32)
func わりこみしゅうりょうloop()

type Tわりこみhandler struct {
	Iわりこみnumber	uint8
	Iわりこみかんりしゃ		uintptr
}
type Iわりこみhandler interface {
	Hとってわりこみ(uint32) uint32
}

func Nしんきわりこみhandler(Iわりこみかんりしゃ uintptr, Iわりこみnumber uint8) *Tわりこみhandler {
	わりこみhandler_2 := new(Tわりこみhandler)
	わりこみhandler_2.Iわりこみnumber = Iわりこみnumber
	わりこみhandler_2.Iわりこみかんりしゃ = Iわりこみかんりしゃ
	return わりこみhandler_2

}

var handler_2 [256]uintptr

func (self *Tわりこみhandler) Init(Iわりこみnumber uint8, Iわりこみかんりしゃ uintptr, funcaddress uintptr) {

	handler_2[Iわりこみnumber] = funcaddress

	self.Iわりこみnumber = Iわりこみnumber
	self.Iわりこみかんりしゃ = Iわりこみかんりしゃ

}
func (self *Tわりこみhandler) Sありとってわりこみfuction(Iわりこみnumber uint32, address uintptr) {
	handler_2[Iわりこみnumber] = address
}
func (self *Tわりこみhandler) Dはき() {
	selfuintptr := uintptr(Pointer(self))
	Iわりこみかんりしゃ := (*Tわりこみかんりしゃ)(Pointer(self.Iわりこみかんりしゃ))
	if selfuintptr == Iわりこみかんりしゃ.Gethandler(self.Iわりこみnumber) {
		Iわりこみかんりしゃ.Sありhandler(0, self.Iわりこみnumber)
	}

}
func (self *Tわりこみhandler) Sありわりこみかんりしゃ(Iわりこみかんりしゃ uintptr) {
}
func (self *Tわりこみhandler) Sありわりこみnumber(Iわりこみnumber uint8) {
	self.Iわりこみnumber = Iわりこみnumber
}
func (self *Tわりこみhandler) Hとってわりこみ(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	こんそーる_2 := Tこんそーる{}
	こんそーる_2.Mいんさつ(buffer)
	return esp
}
func Hとってわりこみ1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	こんそーる_2 := Tこんそーる{}
	こんそーる_2.Mいんさつ(buffer)
}

type Tげーとdescriptor struct {
	げーとでーた [8]uint8
}
type Tわりこみdescriptortableぽいんた struct {
}

var idtでーた [256 * 8]uint8
var Aゆうこうわりこみかんりしゃ uintptr = 0

const わりこみdebug = false

type Tわりこみかんりしゃ struct {
	handler_2	[256]uintptr

	はーどうぇあわりこみoffset	uint16

	たすくかんりしゃ	*Tたすくかんりしゃ
}

var Primarypicこまんどioぽーと uint16 = 0x20
var Primarypicでーたioぽーと uint16 = 0x21
var Secondarypicこまんどioぽーと uint16 = 0xA0
var Secondarypicでーたioぽーと uint16 = 0xA1

func (self *Tわりこみかんりしゃ) Init(はーどうぇあわりこみoffset uint16, ぜんぱんdescriptortable *TShareddescriptortable, たすくかんりしゃ *Tたすくかんりしゃ) {

	self.たすくかんりしゃ = たすくかんりしゃ

	self.はーどうぇあわりこみoffset = はーどうぇあわりこみoffset
	codesegment := uint16(Segちゅうかくcode)

	for i := 0; i < (256 * 8); i++ {
		idtでーた[i] = 0
	}
	var address uint32
	var Idtわりこみげーと uint8 = 0xE
	address = uint32(ValueOf(わりこみignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(わりこみexceptionhandler0x0f).Pointer())
		self.Sわりこみdescriptortableentryあり(i, codesegment, address, 0, Idtわりこみげーと)
	}

	address = uint32(ValueOf(わりこみexceptionhandler0x00).Pointer())
	self.Sわりこみdescriptortableentryあり(0x00, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x01).Pointer())
	self.Sわりこみdescriptortableentryあり(0x01, codesegment, address, 0, Idtわりこみげーと)
	address = uint32(ValueOf(わりこみexceptionhandler0x02).Pointer())
	self.Sわりこみdescriptortableentryあり(0x02, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x03).Pointer())
	self.Sわりこみdescriptortableentryあり(0x03, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x04).Pointer())
	self.Sわりこみdescriptortableentryあり(0x04, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x05).Pointer())
	self.Sわりこみdescriptortableentryあり(0x05, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x06).Pointer())
	self.Sわりこみdescriptortableentryあり(0x06, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x07).Pointer())
	self.Sわりこみdescriptortableentryあり(0x07, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x08).Pointer())
	self.Sわりこみdescriptortableentryあり(0x08, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x09).Pointer())
	self.Sわりこみdescriptortableentryあり(0x09, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x0a).Pointer())
	self.Sわりこみdescriptortableentryあり(0x0A, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x0b).Pointer())
	self.Sわりこみdescriptortableentryあり(0x0B, codesegment, address, 0, Idtわりこみげーと)
	address = uint32(ValueOf(わりこみexceptionhandler0x0c).Pointer())
	self.Sわりこみdescriptortableentryあり(0x0C, codesegment, address, 0, Idtわりこみげーと)
	address = uint32(ValueOf(わりこみexceptionhandler0x0d).Pointer())
	self.Sわりこみdescriptortableentryあり(0x0D, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x0e).Pointer())
	self.Sわりこみdescriptortableentryあり(0x0E, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x0f).Pointer())
	self.Sわりこみdescriptortableentryあり(0x0F, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x10).Pointer())
	self.Sわりこみdescriptortableentryあり(0x10, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x11).Pointer())
	self.Sわりこみdescriptortableentryあり(0x11, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x12).Pointer())
	self.Sわりこみdescriptortableentryあり(0x12, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみexceptionhandler0x13).Pointer())
	self.Sわりこみdescriptortableentryあり(0x13, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x00).Pointer())
	self.Sわりこみdescriptortableentryあり(0x20, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x01).Pointer())
	self.Sわりこみdescriptortableentryあり(0x21, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x02).Pointer())
	self.Sわりこみdescriptortableentryあり(0x22, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x03).Pointer())
	self.Sわりこみdescriptortableentryあり(0x23, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x04).Pointer())
	self.Sわりこみdescriptortableentryあり(0x24, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x05).Pointer())
	self.Sわりこみdescriptortableentryあり(0x25, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x06).Pointer())
	self.Sわりこみdescriptortableentryあり(0x26, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x07).Pointer())
	self.Sわりこみdescriptortableentryあり(0x27, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x08).Pointer())
	self.Sわりこみdescriptortableentryあり(0x28, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x09).Pointer())
	self.Sわりこみdescriptortableentryあり(0x29, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x0a).Pointer())
	self.Sわりこみdescriptortableentryあり(0x2A, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x0b).Pointer())
	self.Sわりこみdescriptortableentryあり(0x2B, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x0c).Pointer())
	self.Sわりこみdescriptortableentryあり(0x2C, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x0d).Pointer())
	self.Sわりこみdescriptortableentryあり(0x2D, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x0e).Pointer())
	self.Sわりこみdescriptortableentryあり(0x2E, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x0f).Pointer())
	self.Sわりこみdescriptortableentryあり(0x2F, codesegment, address, 0, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x80).Pointer())
	self.Sわりこみdescriptortableentryあり(0x80, codesegment, address, 3, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x81).Pointer())
	self.Sわりこみdescriptortableentryあり(0x81, codesegment, address, 3, Idtわりこみげーと)

	address = uint32(ValueOf(わりこみrequesthandler0x82).Pointer())
	self.Sわりこみdescriptortableentryあり(0x82, codesegment, address, 3, Idtわりこみげーと)

	Pぽーとかきこみばいと(Primarypicこまんどioぽーと, 0x11)
	Pぽーとかきこみばいと(Secondarypicこまんどioぽーと, 0x11)

	Pぽーとかきこみばいと(Primarypicでーたioぽーと, 0x20)
	Pぽーとかきこみばいと(Secondarypicでーたioぽーと, 0x28)

	Pぽーとかきこみばいと(Primarypicでーたioぽーと, 0x04)
	Pぽーとかきこみばいと(Secondarypicでーたioぽーと, 0x02)

	Pぽーとかきこみばいと(Primarypicでーたioぽーと, 0x01)
	Pぽーとかきこみばいと(Secondarypicでーたioぽーと, 0x01)

	Pぽーとかきこみばいと(Primarypicでーたioぽーと, 0xF8)
	Pぽーとかきこみばいと(Secondarypicでーたioぽーと, 0xEF)

	idtぽいんた := [6]uint8{0, 0, 0, 0, 0, 0}
	さいず := (*uint16)(Pointer(&idtぽいんた[0]))
	(*さいず) = (uint16)(Sizeof(idtでーた) - 1)

	base := (*uint32)(Pointer(&idtぽいんた[2]))
	(*base) = uint32(uintptr(Pointer(&idtでーた)))

	Lidt(uintptr(Pointer(&idtぽいんた)))
}
func Lidt(lidtaddr uintptr)

func (self *Tわりこみかんりしゃ) Sわりこみdescriptortableentryあり(わりこみ int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptorかた uint8) {

	handleraddressひくいびっと := (*uint16)(Pointer(&idtでーた[わりこみ*8+0]))
	(*handleraddressひくいびっと) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtでーた[わりこみ*8+2]))
	(*gdtcodesegmentselector) = codesegment

	よやく := (*uint8)(Pointer(&idtでーた[わりこみ*8+4]))
	(*よやく) = 0

	var Idtdescriptorげんざい uint8 = 0x80
	あくせす := (*uint8)(Pointer(&idtでーた[わりこみ*8+5]))
	(*あくせす) = (Idtdescriptorげんざい | Descriptorかた | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressたかいびっと := (*uint16)(Pointer(&idtでーた[わりこみ*8+6]))
	(*handleraddressたかいびっと) = uint16((handler >> 16) & 0xFFFF)

}

func (self *Tわりこみかんりしゃ) Sありhandler(handler uintptr, Iわりこみnumber uint8) {
	handler_2[Iわりこみnumber] = handler
}
func (self *Tわりこみかんりしゃ) Gethandler(Iわりこみnumber uint8) uintptr {
	return handler_2[Iわりこみnumber]
}
func (self *Tわりこみかんりしゃ) Doとってわりこみ(わりこみ uint8, esp uint32) uint32 {

	if わりこみdebug {
		こんそーる_2.Mいんさつxy("[esp:", 1, 20)
		こんそーる_2.MUnsignedinteger32いんさつ(uint32(わりこみ))
		こんそーる_2.Mいんさつ(":")
		こんそーる_2.MUnsignedinteger32いんさつ(esp)
	}
	handlerじっこう := false
	if handler_2[わりこみ] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[わりこみ])))
		esp = myfunction(esp)
		handlerじっこう = true

	}

	if !handlerじっこう && わりこみ == uint8(self.はーどうぇあわりこみoffset) && self.たすくかんりしゃ != nil {
		esp = uint32(uintptr(Pointer(self.たすくかんりしゃ.Schedule((*Tcpuじょうたい)(Pointer(uintptr(esp)))))))

	}
	if !handlerじっこう && わりこみ == 0x80 {
		esp = とってunhandledsyscall(esp)
	}

	if わりこみ <= 0x1F {
	}
	if 0x20 <= わりこみ && わりこみ < 0x30 {
		if 0x28 <= わりこみ {
			Pぽーとかきこみばいと(Secondarypicこまんどioぽーと, 0x20)
		}
		Pぽーとかきこみばいと(Primarypicこまんどioぽーと, 0x20)
	}
	return esp
}

var かうんと2 uint8 = 1

func ありcr3(address uint32)

var こんそーる_2 Tこんそーる = Tこんそーる{}

func Hとってわりこみ(esp uint32, わりこみ uint32) uint32 {

	if わりこみdebug && わりこみ != 0x80 && わりこみ != 0x20 {
		こんそーる_2.Mいんさつxy("[esp:", 1, 21)
		こんそーる_2.MUnsignedinteger32いんさつ(uint32(わりこみ))
		こんそーる_2.Mいんさつ(":")
		こんそーる_2.MUnsignedinteger32いんさつ(esp)
	}

	if Aゆうこうわりこみかんりしゃ != 0 {
		p := (*Tわりこみかんりしゃ)(Pointer(Aゆうこうわりこみかんりしゃ))
		esp = p.Doとってわりこみ(uint8(わりこみ), esp)
		return esp
	}
	if handler_2[わりこみ] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[わりこみ])))
		esp = myfunction(esp)
	}
	if わりこみ == 0x80 {
		return とってunhandledsyscall(esp)
	}
	if 0x20 <= わりこみ && わりこみ < 0x30 {
		if 0x28 <= わりこみ {
			Pぽーとかきこみばいと(Secondarypicこまんどioぽーと, 0x20)
		}
		Pぽーとかきこみばいと(Primarypicこまんどioぽーと, 0x20)
	}

	return esp
}

func とってunhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpuじょうたい)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(わりこみしゅうりょうloop).Pointer())
		cpu.Cs = Segちゅうかくcode
		cpu.Ds = Segちゅうかくでーた
		cpu.Es = Segちゅうかくでーた
		cpu.Fs = Segちゅうかくでーた
		cpu.Gs = Segちゅうかくgs
		cpu.Ss = Segちゅうかくでーた
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasえらーcode(わりこみ uint32) bool {
	switch わりこみ {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionなまえ(わりこみ uint32) string {
	switch わりこみ {
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

func exceptionふれーむあたい(ふれーむ uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ふれーむ + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func いんさつぺーじしょうがいinfo(えらー uint32) {
	MEmergencyろぐもじれつ(" pf=[")
	if (えらー & 0x01) != 0 {
		MEmergencyろぐもじれつ("protection")
	} else {
		MEmergencyろぐもじれつ("not-present")
	}
	if (えらー & 0x02) != 0 {
		MEmergencyろぐもじれつ(",write")
	} else {
		MEmergencyろぐもじれつ(",read")
	}
	if (えらー & 0x04) != 0 {
		MEmergencyろぐもじれつ(",user")
	} else {
		MEmergencyろぐもじれつ(",kernel")
	}
	if (えらー & 0x08) != 0 {
		MEmergencyろぐもじれつ(",reserved-bit")
	}
	if (えらー & 0x10) != 0 {
		MEmergencyろぐもじれつ(",instruction-fetch")
	}
	MEmergencyろぐもじれつ("]")
}

func いんさつexceptionselectorinfo(えらー uint32) {
	MEmergencyろぐもじれつ(" selector=")
	MEmergencyろぐunsignedinteger32(えらー & 0xFFFFFFF8)
	MEmergencyろぐもじれつ(" index=")
	MEmergencyろぐunsignedinteger32(えらー >> 3)
	MEmergencyろぐもじれつ(" table=")
	if (えらー & 0x02) != 0 {
		MEmergencyろぐもじれつ("IDT")
	} else if (えらー & 0x04) != 0 {
		MEmergencyろぐもじれつ("LDT")
	} else {
		MEmergencyろぐもじれつ("GDT")
	}
	MEmergencyろぐもじれつ(" ext=")
	MEmergencyろぐunsignedinteger32(えらー & 0x01)
}

func Hとってexception(esp uint32, わりこみ uint32) uint32 {
	MEmergencyろぐもじれつ("\nEXCEPTION vec=")
	MEmergencyろぐhexadecimal8(uint8(わりこみ))
	MEmergencyろぐもじれつ(" ")
	MEmergencyろぐもじれつ(exceptionなまえ(わりこみ))
	MEmergencyろぐもじれつ(" frame=")
	MEmergencyろぐunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyろぐもじれつ(" invalid-frame")
		if exceptionhasえらーcode(わりこみ) {
			MEmergencyろぐもじれつ(" raw-error-or-bad-esp=")
			MEmergencyろぐunsignedinteger32(esp)
			いんさつexceptionselectorinfo(esp)
		}
		MEmergencyろぐもじれつ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var えらー uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasえらーcode(わりこみ) {
		えらー = exceptionふれーむあたい(esp, 0)
		eipoffset = 4
	}
	eip := exceptionふれーむあたい(esp, eipoffset)
	cs := exceptionふれーむあたい(esp, eipoffset+4)
	eflags := exceptionふれーむあたい(esp, eipoffset+8)

	MEmergencyろぐもじれつ(" err=")
	MEmergencyろぐunsignedinteger32(えらー)
	MEmergencyろぐもじれつ(" eip=")
	MEmergencyろぐunsignedinteger32(eip)
	MEmergencyろぐもじれつ(" cs=")
	MEmergencyろぐunsignedinteger32(cs)
	MEmergencyろぐもじれつ(" eflags=")
	MEmergencyろぐunsignedinteger32(eflags)
	MEmergencyろぐもじれつ(" cr0=")
	MEmergencyろぐunsignedinteger32(exceptioncr0())
	MEmergencyろぐもじれつ(" cr3=")
	MEmergencyろぐunsignedinteger32(exceptioncr3())

	if わりこみ == 0x0E {
		MEmergencyろぐもじれつ(" cr2=")
		MEmergencyろぐunsignedinteger32(exceptioncr2())
		いんさつぺーじしょうがいinfo(えらー)
	}

	if (cs & 0x03) != 0 {
		MEmergencyろぐもじれつ(" useresp=")
		MEmergencyろぐunsignedinteger32(exceptionふれーむあたい(esp, eipoffset+12))
		MEmergencyろぐもじれつ(" ss=")
		MEmergencyろぐunsignedinteger32(exceptionふれーむあたい(esp, eipoffset+16))
	}

	if exceptionhasえらーcode(わりこみ) {
		いんさつexceptionselectorinfo(えらー)
	}
	MEmergencyろぐもじれつ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltのちfatalexception()

func Hとってfatalわりこみふれーむ(ほぞんすみesp uint32, わりこみ uint32) uint32 {
	Hとってexception(ほぞんすみesp+52, わりこみ)
	haltのちfatalexception()
	return ほぞんすみesp
}

func Iわりこみゆうこう()
func (self *Tわりこみかんりしゃ) Aゆうこう() {
	if Aゆうこうわりこみかんりしゃ != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	Aゆうこうわりこみかんりしゃ = address
	Iわりこみゆうこう()
}
func Iわりこみdeactive()
func (self *Tわりこみかんりしゃ) Deactive() {
	Aゆうこうわりこみかんりしゃ = 0
	Iわりこみdeactive()
}

func Myとってわりこみ(わりこみ uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	こんそーる_2 := Tこんそーる{}
	こんそーる_2.Mいんさつ(buffer)
	return esp
}
func Myてすと(わりこみ uint8, esp uint32)

func Unhandleわりこみ() {
	buffer := []byte("unhandle interrupt\n")
	こんそーる_2 := Tこんそーる{}
	こんそーる_2.Mいんさつ(buffer)
}

func わりこみhandler_2(わりこみ uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	こんそーる_2 := Tこんそーる{}
	こんそーる_2.Mいんさつ(buffer)
	こんそーる_2.MHexadecimalいんさつ(0x40)
	return esp
}
func いんさつesp(esp uint32) {
	こんそーる_2 := Tこんそーる{}
	こんそーる_2.MUnsignedinteger32いんさつxy(esp, 20, 21)
}
func gettls() uint32
func Pいんさつtls() {

}
