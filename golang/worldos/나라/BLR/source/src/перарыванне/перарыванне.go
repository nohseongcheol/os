/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Перарыванне

import . "unsafe"
import . "reflect"

import . "порт"
import . "gdt"
import . "multitasking"
import . "console"

func перарываннеignore()

func перарываннеexceptionhandler()
func перарываннеexceptionhandler0x00()
func перарываннеexceptionhandler0x01()
func перарываннеexceptionhandler0x02()
func перарываннеexceptionhandler0x03()
func перарываннеexceptionhandler0x04()
func перарываннеexceptionhandler0x05()
func перарываннеexceptionhandler0x06()
func перарываннеexceptionhandler0x07()
func перарываннеexceptionhandler0x08()
func перарываннеexceptionhandler0x09()
func перарываннеexceptionhandler0x0a()
func перарываннеexceptionhandler0x0b()
func перарываннеexceptionhandler0x0c()
func перарываннеexceptionhandler0x0d()
func перарываннеexceptionhandler0x0e()
func перарываннеexceptionhandler0x0f()
func перарываннеexceptionhandler0x10()
func перарываннеexceptionhandler0x11()
func перарываннеexceptionhandler0x12()
func перарываннеexceptionhandler0x13()

func перарываннеrequesthandler0x00()
func перарываннеrequesthandler0x01()
func перарываннеrequesthandler0x02()
func перарываннеrequesthandler0x03()
func перарываннеrequesthandler0x04()
func перарываннеrequesthandler0x05()
func перарываннеrequesthandler0x06()
func перарываннеrequesthandler0x07()
func перарываннеrequesthandler0x08()
func перарываннеrequesthandler0x09()
func перарываннеrequesthandler0x0a()
func перарываннеrequesthandler0x0b()
func перарываннеrequesthandler0x0c()
func перарываннеrequesthandler0x0d()
func перарываннеrequesthandler0x0e()
func перарываннеrequesthandler0x0f()

func перарываннеrequesthandler0x80()
func перарываннеrequesthandler0x81()
func перарываннеrequesthandler0x82()

func ПраверкаДрукаваць(пазіцыя uint8, data uint8)
func вызначанаds(dssegment uint32)
func вызначанаgs(gssegment uint32)
func перарываннеВыхадloop()

type TПерарываннеhandler struct {
	ПерарываннеНУМАР	uint8
	Перарываннеmanager	uintptr
}
type IПерарываннеhandler interface {
	HandleПерарыванне(uint32) uint32
}

func НовыПерарываннеhandler(Перарываннеmanager uintptr, ПерарываннеНУМАР uint8) *TПерарываннеhandler {
	перарываннеhandler_2 := new(TПерарываннеhandler)
	перарываннеhandler_2.ПерарываннеНУМАР = ПерарываннеНУМАР
	перарываннеhandler_2.Перарываннеmanager = Перарываннеmanager
	return перарываннеhandler_2

}

var handler_2 [256]uintptr

func (self *TПерарываннеhandler) Init(ПерарываннеНУМАР uint8, Перарываннеmanager uintptr, funcaddress uintptr) {

	handler_2[ПерарываннеНУМАР] = funcaddress

	self.ПерарываннеНУМАР = ПерарываннеНУМАР
	self.Перарываннеmanager = Перарываннеmanager

}
func (self *TПерарываннеhandler) ВызначанаhandleПерарываннеfuction(ПерарываннеНУМАР uint32, address uintptr) {
	handler_2[ПерарываннеНУМАР] = address
}
func (self *TПерарываннеhandler) Зьнішчыць() {
	selfuintptr := uintptr(Pointer(self))
	Перарываннеmanager := (*TПерарываннеmanager)(Pointer(self.Перарываннеmanager))
	if selfuintptr == Перарываннеmanager.Gethandler(self.ПерарываннеНУМАР) {
		Перарываннеmanager.Вызначанаhandler(0, self.ПерарываннеНУМАР)
	}

}
func (self *TПерарываннеhandler) ВызначанаПерарываннеmanager(Перарываннеmanager uintptr) {
}
func (self *TПерарываннеhandler) ВызначанаПерарываннеНУМАР(ПерарываннеНУМАР uint8) {
	self.ПерарываннеНУМАР = ПерарываннеНУМАР
}
func (self *TПерарываннеhandler) HandleПерарыванне(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MДрукаваць(buffer)
	return esp
}
func HandleПерарыванне1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MДрукаваць(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TПерарываннеdescriptorТабліцаПаказальнік struct {
}

var idtdata [256 * 8]uint8
var АктыўнаПерарываннеmanager uintptr = 0

const перарываннеdebug = false

type TПерарываннеmanager struct {
	handler_2	[256]uintptr

	апаратураПерарываннеoffset	uint16

	задачаmanager	*TЗадачаmanager
}

var PrimarypicЗагадioПорт uint16 = 0x20
var PrimarypicdataioПорт uint16 = 0x21
var SecondarypicЗагадioПорт uint16 = 0xA0
var SecondarypicdataioПорт uint16 = 0xA1

func (self *TПерарываннеmanager) Init(апаратураПерарываннеoffset uint16, агульныяdescriptorТабліца *TShareddescriptorТабліца, задачаmanager *TЗадачаmanager) {

	self.задачаmanager = задачаmanager

	self.апаратураПерарываннеoffset = апаратураПерарываннеoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtПерарываннеgate uint8 = 0xE
	address = uint32(ValueOf(перарываннеignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(перарываннеexceptionhandler0x0f).Pointer())
		self.ПерарываннеdescriptorТабліцаentryвызначана(i, codesegment, address, 0, IdtПерарываннеgate)
	}

	address = uint32(ValueOf(перарываннеexceptionhandler0x00).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x00, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x01).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x01, codesegment, address, 0, IdtПерарываннеgate)
	address = uint32(ValueOf(перарываннеexceptionhandler0x02).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x02, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x03).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x03, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x04).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x04, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x05).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x05, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x06).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x06, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x07).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x07, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x08).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x08, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x09).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x09, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x0a).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x0A, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x0b).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x0B, codesegment, address, 0, IdtПерарываннеgate)
	address = uint32(ValueOf(перарываннеexceptionhandler0x0c).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x0C, codesegment, address, 0, IdtПерарываннеgate)
	address = uint32(ValueOf(перарываннеexceptionhandler0x0d).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x0D, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x0e).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x0E, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x0f).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x0F, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x10).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x10, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x11).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x11, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x12).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x12, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеexceptionhandler0x13).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x13, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x00).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x20, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x01).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x21, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x02).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x22, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x03).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x23, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x04).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x24, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x05).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x25, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x06).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x26, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x07).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x27, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x08).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x28, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x09).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x29, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x0a).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x2A, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x0b).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x2B, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x0c).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x2C, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x0d).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x2D, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x0e).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x2E, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x0f).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x2F, codesegment, address, 0, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x80).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x80, codesegment, address, 3, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x81).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x81, codesegment, address, 3, IdtПерарываннеgate)

	address = uint32(ValueOf(перарываннеrequesthandler0x82).Pointer())
	self.ПерарываннеdescriptorТабліцаentryвызначана(0x82, codesegment, address, 3, IdtПерарываннеgate)

	ПортЗапісbyte(PrimarypicЗагадioПорт, 0x11)
	ПортЗапісbyte(SecondarypicЗагадioПорт, 0x11)

	ПортЗапісbyte(PrimarypicdataioПорт, 0x20)
	ПортЗапісbyte(SecondarypicdataioПорт, 0x28)

	ПортЗапісbyte(PrimarypicdataioПорт, 0x04)
	ПортЗапісbyte(SecondarypicdataioПорт, 0x02)

	ПортЗапісbyte(PrimarypicdataioПорт, 0x01)
	ПортЗапісbyte(SecondarypicdataioПорт, 0x01)

	ПортЗапісbyte(PrimarypicdataioПорт, 0xF8)
	ПортЗапісbyte(SecondarypicdataioПорт, 0xEF)

	idtПаказальнік := [6]uint8{0, 0, 0, 0, 0, 0}
	памер := (*uint16)(Pointer(&idtПаказальнік[0]))
	(*памер) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtПаказальнік[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtПаказальнік)))
}
func Lidt(lidtaddr uintptr)

func (self *TПерарываннеmanager) ПерарываннеdescriptorТабліцаentryвызначана(перарыванне int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorТып uint8) {

	handleraddressНізкібітаў := (*uint16)(Pointer(&idtdata[перарыванне*8+0]))
	(*handleraddressНізкібітаў) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[перарыванне*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[перарыванне*8+4]))
	(*reserved) = 0

	var IdtdescriptorПрысутнічае uint8 = 0x80
	доступ := (*uint8)(Pointer(&idtdata[перарыванне*8+5]))
	(*доступ) = (IdtdescriptorПрысутнічае | DescriptorТып | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressВысокібітаў := (*uint16)(Pointer(&idtdata[перарыванне*8+6]))
	(*handleraddressВысокібітаў) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TПерарываннеmanager) Вызначанаhandler(handler uintptr, ПерарываннеНУМАР uint8) {
	handler_2[ПерарываннеНУМАР] = handler
}
func (self *TПерарываннеmanager) Gethandler(ПерарываннеНУМАР uint8) uintptr {
	return handler_2[ПерарываннеНУМАР]
}
func (self *TПерарываннеmanager) DohandleПерарыванне(перарыванне uint8, esp uint32) uint32 {

	if перарываннеdebug {
		console_2.MДрукавацьxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Друкаваць(uint32(перарыванне))
		console_2.MДрукаваць(":")
		console_2.MUnsignedinteger32Друкаваць(esp)
	}
	handlerВыканаць := false
	if handler_2[перарыванне] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[перарыванне])))
		esp = myfunction(esp)
		handlerВыканаць = true

	}

	if !handlerВыканаць && перарыванне == uint8(self.апаратураПерарываннеoffset) && self.задачаmanager != nil {
		esp = uint32(uintptr(Pointer(self.задачаmanager.Schedule((*TcpuСтан)(Pointer(uintptr(esp)))))))

	}
	if !handlerВыканаць && перарыванне == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if перарыванне <= 0x1F {
	}
	if 0x20 <= перарыванне && перарыванне < 0x30 {
		if 0x28 <= перарыванне {
			ПортЗапісbyte(SecondarypicЗагадioПорт, 0x20)
		}
		ПортЗапісbyte(PrimarypicЗагадioПорт, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func вызначанаcr3(address uint32)

var console_2 TConsole = TConsole{}

func HandleПерарыванне(esp uint32, перарыванне uint32) uint32 {

	if перарываннеdebug && перарыванне != 0x80 && перарыванне != 0x20 {
		console_2.MДрукавацьxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Друкаваць(uint32(перарыванне))
		console_2.MДрукаваць(":")
		console_2.MUnsignedinteger32Друкаваць(esp)
	}

	if АктыўнаПерарываннеmanager != 0 {
		p := (*TПерарываннеmanager)(Pointer(АктыўнаПерарываннеmanager))
		esp = p.DohandleПерарыванне(uint8(перарыванне), esp)
		return esp
	}
	if handler_2[перарыванне] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[перарыванне])))
		esp = myfunction(esp)
	}
	if перарыванне == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= перарыванне && перарыванне < 0x30 {
		if 0x28 <= перарыванне {
			ПортЗапісbyte(SecondarypicЗагадioПорт, 0x20)
		}
		ПортЗапісbyte(PrimarypicЗагадioПорт, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	цП := (*TcpuСтан)(Pointer(uintptr(esp)))
	if цП.Eax == 1 || цП.Eax == 252 {
		цП.Eip = uint32(ValueOf(перарываннеВыхадloop).Pointer())
		цП.Cs = Segkernelcode
		цП.Ds = Segkerneldata
		цП.Es = Segkerneldata
		цП.Fs = Segkerneldata
		цП.Gs = Segkernelgs
		цП.Ss = Segkerneldata
		цП.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionХасПамылкаcode(перарыванне uint32) bool {
	switch перарыванне {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionНазва(перарыванне uint32) string {
	switch перарыванне {
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

func exceptionФрэймЗначэнне(фрэйм uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(фрэйм + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func друкавацьСтаронкаfaultІнф(пам uint32) {
	MEmergencylogРадок(" pf=[")
	if (пам & 0x01) != 0 {
		MEmergencylogРадок("protection")
	} else {
		MEmergencylogРадок("not-present")
	}
	if (пам & 0x02) != 0 {
		MEmergencylogРадок(",write")
	} else {
		MEmergencylogРадок(",read")
	}
	if (пам & 0x04) != 0 {
		MEmergencylogРадок(",user")
	} else {
		MEmergencylogРадок(",kernel")
	}
	if (пам & 0x08) != 0 {
		MEmergencylogРадок(",reserved-bit")
	}
	if (пам & 0x10) != 0 {
		MEmergencylogРадок(",instruction-fetch")
	}
	MEmergencylogРадок("]")
}

func друкавацьexceptionselectorІнф(пам uint32) {
	MEmergencylogРадок(" selector=")
	MEmergencylogunsignedinteger32(пам & 0xFFFFFFF8)
	MEmergencylogРадок(" index=")
	MEmergencylogunsignedinteger32(пам >> 3)
	MEmergencylogРадок(" table=")
	if (пам & 0x02) != 0 {
		MEmergencylogРадок("IDT")
	} else if (пам & 0x04) != 0 {
		MEmergencylogРадок("LDT")
	} else {
		MEmergencylogРадок("GDT")
	}
	MEmergencylogРадок(" ext=")
	MEmergencylogunsignedinteger32(пам & 0x01)
}

func Handleexception(esp uint32, перарыванне uint32) uint32 {
	MEmergencylogРадок("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(перарыванне))
	MEmergencylogРадок(" ")
	MEmergencylogРадок(exceptionНазва(перарыванне))
	MEmergencylogРадок(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogРадок(" invalid-frame")
		if exceptionХасПамылкаcode(перарыванне) {
			MEmergencylogРадок(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			друкавацьexceptionselectorІнф(esp)
		}
		MEmergencylogРадок("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var пам uint32 = 0
	var eipoffset uint32 = 0
	if exceptionХасПамылкаcode(перарыванне) {
		пам = exceptionФрэймЗначэнне(esp, 0)
		eipoffset = 4
	}
	eip := exceptionФрэймЗначэнне(esp, eipoffset)
	cs := exceptionФрэймЗначэнне(esp, eipoffset+4)
	eflags := exceptionФрэймЗначэнне(esp, eipoffset+8)

	MEmergencylogРадок(" err=")
	MEmergencylogunsignedinteger32(пам)
	MEmergencylogРадок(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogРадок(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogРадок(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogРадок(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogРадок(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if перарыванне == 0x0E {
		MEmergencylogРадок(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		друкавацьСтаронкаfaultІнф(пам)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogРадок(" useresp=")
		MEmergencylogunsignedinteger32(exceptionФрэймЗначэнне(esp, eipoffset+12))
		MEmergencylogРадок(" ss=")
		MEmergencylogunsignedinteger32(exceptionФрэймЗначэнне(esp, eipoffset+16))
	}

	if exceptionХасПамылкаcode(перарыванне) {
		друкавацьexceptionselectorІнф(пам)
	}
	MEmergencylogРадок("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandlefatalПерарываннеФрэйм(savedesp uint32, перарыванне uint32) uint32 {
	Handleexception(savedesp+52, перарыванне)
	haltafterfatalexception()
	return savedesp
}

func ПерарываннеАктыўна()
func (self *TПерарываннеmanager) Актыўна() {
	if АктыўнаПерарываннеmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	АктыўнаПерарываннеmanager = address
	ПерарываннеАктыўна()
}
func Перарываннеdeactive()
func (self *TПерарываннеmanager) Deactive() {
	АктыўнаПерарываннеmanager = 0
	Перарываннеdeactive()
}

func MyhandleПерарыванне(перарыванне uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MДрукаваць(buffer)
	return esp
}
func MyПраверка(перарыванне uint8, esp uint32)

func UnhandleПерарыванне() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MДрукаваць(buffer)
}

func перарываннеhandler_2(перарыванне uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MДрукаваць(buffer)
	console_2.MHexadecimalДрукаваць(0x40)
	return esp
}
func друкавацьesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Друкавацьxy(esp, 20, 21)
}
func gettls() uint32
func Друкавацьtls() {

}
