package Iワリコミ

import . "unsafe"
import . "reflect"

import . "ポート"
import . "gdt"
import . "フクスウタスクカンリ"
import . "コンソール"

func ワリコミignore()

func ワリコミexceptionhandler()
func ワリコミexceptionhandler0x00()
func ワリコミexceptionhandler0x01()
func ワリコミexceptionhandler0x02()
func ワリコミexceptionhandler0x03()
func ワリコミexceptionhandler0x04()
func ワリコミexceptionhandler0x05()
func ワリコミexceptionhandler0x06()
func ワリコミexceptionhandler0x07()
func ワリコミexceptionhandler0x08()
func ワリコミexceptionhandler0x09()
func ワリコミexceptionhandler0x0a()
func ワリコミexceptionhandler0x0b()
func ワリコミexceptionhandler0x0c()
func ワリコミexceptionhandler0x0d()
func ワリコミexceptionhandler0x0e()
func ワリコミexceptionhandler0x0f()
func ワリコミexceptionhandler0x10()
func ワリコミexceptionhandler0x11()
func ワリコミexceptionhandler0x12()
func ワリコミexceptionhandler0x13()

func ワリコミrequesthandler0x00()
func ワリコミrequesthandler0x01()
func ワリコミrequesthandler0x02()
func ワリコミrequesthandler0x03()
func ワリコミrequesthandler0x04()
func ワリコミrequesthandler0x05()
func ワリコミrequesthandler0x06()
func ワリコミrequesthandler0x07()
func ワリコミrequesthandler0x08()
func ワリコミrequesthandler0x09()
func ワリコミrequesthandler0x0a()
func ワリコミrequesthandler0x0b()
func ワリコミrequesthandler0x0c()
func ワリコミrequesthandler0x0d()
func ワリコミrequesthandler0x0e()
func ワリコミrequesthandler0x0f()

func ワリコミrequesthandler0x80()
func ワリコミrequesthandler0x81()
func ワリコミrequesthandler0x82()

func Tテストインサツ(ハイチ uint8, データ uint8)
func アリds(dssegment uint32)
func アリgs(gssegment uint32)
func ワリコミシュウリョウloop()

type Tワリコミhandler struct {
	Iワリコミnumber	uint8
	Iワリコミカンリシャ		uintptr
}
type Iワリコミhandler interface {
	Hトッテワリコミ(uint32) uint32
}

func Nシンキワリコミhandler(Iワリコミカンリシャ uintptr, Iワリコミnumber uint8) *Tワリコミhandler {
	ワリコミhandler_2 := new(Tワリコミhandler)
	ワリコミhandler_2.Iワリコミnumber = Iワリコミnumber
	ワリコミhandler_2.Iワリコミカンリシャ = Iワリコミカンリシャ
	return ワリコミhandler_2

}

var handler_2 [256]uintptr

func (self *Tワリコミhandler) Init(Iワリコミnumber uint8, Iワリコミカンリシャ uintptr, funcaddress uintptr) {

	handler_2[Iワリコミnumber] = funcaddress

	self.Iワリコミnumber = Iワリコミnumber
	self.Iワリコミカンリシャ = Iワリコミカンリシャ

}
func (self *Tワリコミhandler) Sアリトッテワリコミfuction(Iワリコミnumber uint32, address uintptr) {
	handler_2[Iワリコミnumber] = address
}
func (self *Tワリコミhandler) Dハキ() {
	selfuintptr := uintptr(Pointer(self))
	Iワリコミカンリシャ := (*Tワリコミカンリシャ)(Pointer(self.Iワリコミカンリシャ))
	if selfuintptr == Iワリコミカンリシャ.Gethandler(self.Iワリコミnumber) {
		Iワリコミカンリシャ.Sアリhandler(0, self.Iワリコミnumber)
	}

}
func (self *Tワリコミhandler) Sアリワリコミカンリシャ(Iワリコミカンリシャ uintptr) {
}
func (self *Tワリコミhandler) Sアリワリコミnumber(Iワリコミnumber uint8) {
	self.Iワリコミnumber = Iワリコミnumber
}
func (self *Tワリコミhandler) Hトッテワリコミ(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	コンソール_2 := Tコンソール{}
	コンソール_2.Mインサツ(buffer)
	return esp
}
func Hトッテワリコミ1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	コンソール_2 := Tコンソール{}
	コンソール_2.Mインサツ(buffer)
}

type Tゲートdescriptor struct {
	ゲートデータ [8]uint8
}
type Tワリコミdescriptortableポインタ struct {
}

var idtデータ [256 * 8]uint8
var Aユウコウワリコミカンリシャ uintptr = 0

const ワリコミdebug = false

type Tワリコミカンリシャ struct {
	handler_2	[256]uintptr

	ハードウェアワリコミoffset	uint16

	タスクカンリシャ	*Tタスクカンリシャ
}

var Primarypicコマンドioポート uint16 = 0x20
var Primarypicデータioポート uint16 = 0x21
var Secondarypicコマンドioポート uint16 = 0xA0
var Secondarypicデータioポート uint16 = 0xA1

func (self *Tワリコミカンリシャ) Init(ハードウェアワリコミoffset uint16, ゼンパンdescriptortable *TShareddescriptortable, タスクカンリシャ *Tタスクカンリシャ) {

	self.タスクカンリシャ = タスクカンリシャ

	self.ハードウェアワリコミoffset = ハードウェアワリコミoffset
	codesegment := uint16(Segチュウカクcode)

	for i := 0; i < (256 * 8); i++ {
		idtデータ[i] = 0
	}
	var address uint32
	var Idtワリコミゲート uint8 = 0xE
	address = uint32(ValueOf(ワリコミignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(ワリコミexceptionhandler0x0f).Pointer())
		self.Sワリコミdescriptortableentryアリ(i, codesegment, address, 0, Idtワリコミゲート)
	}

	address = uint32(ValueOf(ワリコミexceptionhandler0x00).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x00, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x01).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x01, codesegment, address, 0, Idtワリコミゲート)
	address = uint32(ValueOf(ワリコミexceptionhandler0x02).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x02, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x03).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x03, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x04).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x04, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x05).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x05, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x06).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x06, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x07).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x07, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x08).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x08, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x09).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x09, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x0a).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x0A, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x0b).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x0B, codesegment, address, 0, Idtワリコミゲート)
	address = uint32(ValueOf(ワリコミexceptionhandler0x0c).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x0C, codesegment, address, 0, Idtワリコミゲート)
	address = uint32(ValueOf(ワリコミexceptionhandler0x0d).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x0D, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x0e).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x0E, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x0f).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x0F, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x10).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x10, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x11).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x11, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x12).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x12, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミexceptionhandler0x13).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x13, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x00).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x20, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x01).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x21, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x02).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x22, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x03).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x23, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x04).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x24, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x05).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x25, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x06).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x26, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x07).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x27, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x08).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x28, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x09).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x29, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x0a).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x2A, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x0b).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x2B, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x0c).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x2C, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x0d).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x2D, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x0e).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x2E, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x0f).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x2F, codesegment, address, 0, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x80).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x80, codesegment, address, 3, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x81).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x81, codesegment, address, 3, Idtワリコミゲート)

	address = uint32(ValueOf(ワリコミrequesthandler0x82).Pointer())
	self.Sワリコミdescriptortableentryアリ(0x82, codesegment, address, 3, Idtワリコミゲート)

	Pポートカキコミバイト(Primarypicコマンドioポート, 0x11)
	Pポートカキコミバイト(Secondarypicコマンドioポート, 0x11)

	Pポートカキコミバイト(Primarypicデータioポート, 0x20)
	Pポートカキコミバイト(Secondarypicデータioポート, 0x28)

	Pポートカキコミバイト(Primarypicデータioポート, 0x04)
	Pポートカキコミバイト(Secondarypicデータioポート, 0x02)

	Pポートカキコミバイト(Primarypicデータioポート, 0x01)
	Pポートカキコミバイト(Secondarypicデータioポート, 0x01)

	Pポートカキコミバイト(Primarypicデータioポート, 0xF8)
	Pポートカキコミバイト(Secondarypicデータioポート, 0xEF)

	idtポインタ := [6]uint8{0, 0, 0, 0, 0, 0}
	サイズ := (*uint16)(Pointer(&idtポインタ[0]))
	(*サイズ) = (uint16)(Sizeof(idtデータ) - 1)

	base := (*uint32)(Pointer(&idtポインタ[2]))
	(*base) = uint32(uintptr(Pointer(&idtデータ)))

	Lidt(uintptr(Pointer(&idtポインタ)))
}
func Lidt(lidtaddr uintptr)

func (self *Tワリコミカンリシャ) Sワリコミdescriptortableentryアリ(ワリコミ int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptorカタ uint8) {

	handleraddressヒクイビット := (*uint16)(Pointer(&idtデータ[ワリコミ*8+0]))
	(*handleraddressヒクイビット) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtデータ[ワリコミ*8+2]))
	(*gdtcodesegmentselector) = codesegment

	ヨヤク := (*uint8)(Pointer(&idtデータ[ワリコミ*8+4]))
	(*ヨヤク) = 0

	var Idtdescriptorゲンザイ uint8 = 0x80
	アクセス := (*uint8)(Pointer(&idtデータ[ワリコミ*8+5]))
	(*アクセス) = (Idtdescriptorゲンザイ | Descriptorカタ | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressタカイビット := (*uint16)(Pointer(&idtデータ[ワリコミ*8+6]))
	(*handleraddressタカイビット) = uint16((handler >> 16) & 0xFFFF)

}

func (self *Tワリコミカンリシャ) Sアリhandler(handler uintptr, Iワリコミnumber uint8) {
	handler_2[Iワリコミnumber] = handler
}
func (self *Tワリコミカンリシャ) Gethandler(Iワリコミnumber uint8) uintptr {
	return handler_2[Iワリコミnumber]
}
func (self *Tワリコミカンリシャ) Doトッテワリコミ(ワリコミ uint8, esp uint32) uint32 {

	if ワリコミdebug {
		コンソール_2.Mインサツxy("[esp:", 1, 20)
		コンソール_2.MUnsignedinteger32インサツ(uint32(ワリコミ))
		コンソール_2.Mインサツ(":")
		コンソール_2.MUnsignedinteger32インサツ(esp)
	}
	handlerジッコウ := false
	if handler_2[ワリコミ] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ワリコミ])))
		esp = myfunction(esp)
		handlerジッコウ = true

	}

	if !handlerジッコウ && ワリコミ == uint8(self.ハードウェアワリコミoffset) && self.タスクカンリシャ != nil {
		esp = uint32(uintptr(Pointer(self.タスクカンリシャ.Schedule((*Tcpuジョウタイ)(Pointer(uintptr(esp)))))))

	}
	if !handlerジッコウ && ワリコミ == 0x80 {
		esp = トッテunhandledsyscall(esp)
	}

	if ワリコミ <= 0x1F {
	}
	if 0x20 <= ワリコミ && ワリコミ < 0x30 {
		if 0x28 <= ワリコミ {
			Pポートカキコミバイト(Secondarypicコマンドioポート, 0x20)
		}
		Pポートカキコミバイト(Primarypicコマンドioポート, 0x20)
	}
	return esp
}

var カウント2 uint8 = 1

func アリcr3(address uint32)

var コンソール_2 Tコンソール = Tコンソール{}

func Hトッテワリコミ(esp uint32, ワリコミ uint32) uint32 {

	if ワリコミdebug && ワリコミ != 0x80 && ワリコミ != 0x20 {
		コンソール_2.Mインサツxy("[esp:", 1, 21)
		コンソール_2.MUnsignedinteger32インサツ(uint32(ワリコミ))
		コンソール_2.Mインサツ(":")
		コンソール_2.MUnsignedinteger32インサツ(esp)
	}

	if Aユウコウワリコミカンリシャ != 0 {
		p := (*Tワリコミカンリシャ)(Pointer(Aユウコウワリコミカンリシャ))
		esp = p.Doトッテワリコミ(uint8(ワリコミ), esp)
		return esp
	}
	if handler_2[ワリコミ] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[ワリコミ])))
		esp = myfunction(esp)
	}
	if ワリコミ == 0x80 {
		return トッテunhandledsyscall(esp)
	}
	if 0x20 <= ワリコミ && ワリコミ < 0x30 {
		if 0x28 <= ワリコミ {
			Pポートカキコミバイト(Secondarypicコマンドioポート, 0x20)
		}
		Pポートカキコミバイト(Primarypicコマンドioポート, 0x20)
	}

	return esp
}

func トッテunhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpuジョウタイ)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(ワリコミシュウリョウloop).Pointer())
		cpu.Cs = Segチュウカクcode
		cpu.Ds = Segチュウカクデータ
		cpu.Es = Segチュウカクデータ
		cpu.Fs = Segチュウカクデータ
		cpu.Gs = Segチュウカクgs
		cpu.Ss = Segチュウカクデータ
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasエラーcode(ワリコミ uint32) bool {
	switch ワリコミ {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionナマエ(ワリコミ uint32) string {
	switch ワリコミ {
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

func exceptionフレームアタイ(フレーム uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(フレーム + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func インサツページショウガイinfo(エラー uint32) {
	MEmergencyログモジレツ(" pf=[")
	if (エラー & 0x01) != 0 {
		MEmergencyログモジレツ("protection")
	} else {
		MEmergencyログモジレツ("not-present")
	}
	if (エラー & 0x02) != 0 {
		MEmergencyログモジレツ(",write")
	} else {
		MEmergencyログモジレツ(",read")
	}
	if (エラー & 0x04) != 0 {
		MEmergencyログモジレツ(",user")
	} else {
		MEmergencyログモジレツ(",kernel")
	}
	if (エラー & 0x08) != 0 {
		MEmergencyログモジレツ(",reserved-bit")
	}
	if (エラー & 0x10) != 0 {
		MEmergencyログモジレツ(",instruction-fetch")
	}
	MEmergencyログモジレツ("]")
}

func インサツexceptionselectorinfo(エラー uint32) {
	MEmergencyログモジレツ(" selector=")
	MEmergencyログunsignedinteger32(エラー & 0xFFFFFFF8)
	MEmergencyログモジレツ(" index=")
	MEmergencyログunsignedinteger32(エラー >> 3)
	MEmergencyログモジレツ(" table=")
	if (エラー & 0x02) != 0 {
		MEmergencyログモジレツ("IDT")
	} else if (エラー & 0x04) != 0 {
		MEmergencyログモジレツ("LDT")
	} else {
		MEmergencyログモジレツ("GDT")
	}
	MEmergencyログモジレツ(" ext=")
	MEmergencyログunsignedinteger32(エラー & 0x01)
}

func Hトッテexception(esp uint32, ワリコミ uint32) uint32 {
	MEmergencyログモジレツ("\nEXCEPTION vec=")
	MEmergencyログhexadecimal8(uint8(ワリコミ))
	MEmergencyログモジレツ(" ")
	MEmergencyログモジレツ(exceptionナマエ(ワリコミ))
	MEmergencyログモジレツ(" frame=")
	MEmergencyログunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyログモジレツ(" invalid-frame")
		if exceptionhasエラーcode(ワリコミ) {
			MEmergencyログモジレツ(" raw-error-or-bad-esp=")
			MEmergencyログunsignedinteger32(esp)
			インサツexceptionselectorinfo(esp)
		}
		MEmergencyログモジレツ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var エラー uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasエラーcode(ワリコミ) {
		エラー = exceptionフレームアタイ(esp, 0)
		eipoffset = 4
	}
	eip := exceptionフレームアタイ(esp, eipoffset)
	cs := exceptionフレームアタイ(esp, eipoffset+4)
	eflags := exceptionフレームアタイ(esp, eipoffset+8)

	MEmergencyログモジレツ(" err=")
	MEmergencyログunsignedinteger32(エラー)
	MEmergencyログモジレツ(" eip=")
	MEmergencyログunsignedinteger32(eip)
	MEmergencyログモジレツ(" cs=")
	MEmergencyログunsignedinteger32(cs)
	MEmergencyログモジレツ(" eflags=")
	MEmergencyログunsignedinteger32(eflags)
	MEmergencyログモジレツ(" cr0=")
	MEmergencyログunsignedinteger32(exceptioncr0())
	MEmergencyログモジレツ(" cr3=")
	MEmergencyログunsignedinteger32(exceptioncr3())

	if ワリコミ == 0x0E {
		MEmergencyログモジレツ(" cr2=")
		MEmergencyログunsignedinteger32(exceptioncr2())
		インサツページショウガイinfo(エラー)
	}

	if (cs & 0x03) != 0 {
		MEmergencyログモジレツ(" useresp=")
		MEmergencyログunsignedinteger32(exceptionフレームアタイ(esp, eipoffset+12))
		MEmergencyログモジレツ(" ss=")
		MEmergencyログunsignedinteger32(exceptionフレームアタイ(esp, eipoffset+16))
	}

	if exceptionhasエラーcode(ワリコミ) {
		インサツexceptionselectorinfo(エラー)
	}
	MEmergencyログモジレツ("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltノチfatalexception()

func Hトッテfatalワリコミフレーム(ホゾンスミesp uint32, ワリコミ uint32) uint32 {
	Hトッテexception(ホゾンスミesp+52, ワリコミ)
	haltノチfatalexception()
	return ホゾンスミesp
}

func Iワリコミユウコウ()
func (self *Tワリコミカンリシャ) Aユウコウ() {
	if Aユウコウワリコミカンリシャ != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	Aユウコウワリコミカンリシャ = address
	Iワリコミユウコウ()
}
func Iワリコミdeactive()
func (self *Tワリコミカンリシャ) Deactive() {
	Aユウコウワリコミカンリシャ = 0
	Iワリコミdeactive()
}

func Myトッテワリコミ(ワリコミ uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	コンソール_2 := Tコンソール{}
	コンソール_2.Mインサツ(buffer)
	return esp
}
func Myテスト(ワリコミ uint8, esp uint32)

func Unhandleワリコミ() {
	buffer := []byte("unhandle interrupt\n")
	コンソール_2 := Tコンソール{}
	コンソール_2.Mインサツ(buffer)
}

func ワリコミhandler_2(ワリコミ uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	コンソール_2 := Tコンソール{}
	コンソール_2.Mインサツ(buffer)
	コンソール_2.MHexadecimalインサツ(0x40)
	return esp
}
func インサツesp(esp uint32) {
	コンソール_2 := Tコンソール{}
	コンソール_2.MUnsignedinteger32インサツxy(esp, 20, 21)
}
func gettls() uint32
func Pインサツtls() {

}
