/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package I割込み

import . "unsafe"
import . "reflect"

import . "ポート"
import . "gdt"
import . "複数タスク管理"
import . "コンソール"

func 割込みignore()

func 割込みexceptionhandler()
func 割込みexceptionhandler0x00()
func 割込みexceptionhandler0x01()
func 割込みexceptionhandler0x02()
func 割込みexceptionhandler0x03()
func 割込みexceptionhandler0x04()
func 割込みexceptionhandler0x05()
func 割込みexceptionhandler0x06()
func 割込みexceptionhandler0x07()
func 割込みexceptionhandler0x08()
func 割込みexceptionhandler0x09()
func 割込みexceptionhandler0x0a()
func 割込みexceptionhandler0x0b()
func 割込みexceptionhandler0x0c()
func 割込みexceptionhandler0x0d()
func 割込みexceptionhandler0x0e()
func 割込みexceptionhandler0x0f()
func 割込みexceptionhandler0x10()
func 割込みexceptionhandler0x11()
func 割込みexceptionhandler0x12()
func 割込みexceptionhandler0x13()

func 割込みrequesthandler0x00()
func 割込みrequesthandler0x01()
func 割込みrequesthandler0x02()
func 割込みrequesthandler0x03()
func 割込みrequesthandler0x04()
func 割込みrequesthandler0x05()
func 割込みrequesthandler0x06()
func 割込みrequesthandler0x07()
func 割込みrequesthandler0x08()
func 割込みrequesthandler0x09()
func 割込みrequesthandler0x0a()
func 割込みrequesthandler0x0b()
func 割込みrequesthandler0x0c()
func 割込みrequesthandler0x0d()
func 割込みrequesthandler0x0e()
func 割込みrequesthandler0x0f()

func 割込みrequesthandler0x80()
func 割込みrequesthandler0x81()
func 割込みrequesthandler0x82()

func Tテスト印刷(配置 uint8, データ uint8)
func ありds(dssegment uint32)
func ありgs(gssegment uint32)
func 割込み終了loop()

type T割込みhandler struct {
	I割込みnumber	uint8
	I割込み管理者		uintptr
}
type I割込みhandler interface {
	H取っ手割込み(uint32) uint32
}

func N新規割込みhandler(I割込み管理者 uintptr, I割込みnumber uint8) *T割込みhandler {
	割込みhandler_2 := new(T割込みhandler)
	割込みhandler_2.I割込みnumber = I割込みnumber
	割込みhandler_2.I割込み管理者 = I割込み管理者
	return 割込みhandler_2

}

var handler_2 [256]uintptr

func (self *T割込みhandler) Init(I割込みnumber uint8, I割込み管理者 uintptr, funcaddress uintptr) {

	handler_2[I割込みnumber] = funcaddress

	self.I割込みnumber = I割込みnumber
	self.I割込み管理者 = I割込み管理者

}
func (self *T割込みhandler) Sあり取っ手割込みfuction(I割込みnumber uint32, address uintptr) {
	handler_2[I割込みnumber] = address
}
func (self *T割込みhandler) D破棄() {
	selfuintptr := uintptr(Pointer(self))
	I割込み管理者 := (*T割込み管理者)(Pointer(self.I割込み管理者))
	if selfuintptr == I割込み管理者.Gethandler(self.I割込みnumber) {
		I割込み管理者.Sありhandler(0, self.I割込みnumber)
	}

}
func (self *T割込みhandler) Sあり割込み管理者(I割込み管理者 uintptr) {
}
func (self *T割込みhandler) Sあり割込みnumber(I割込みnumber uint8) {
	self.I割込みnumber = I割込みnumber
}
func (self *T割込みhandler) H取っ手割込み(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	コンソール_2 := Tコンソール{}
	コンソール_2.M印刷(buffer)
	return esp
}
func H取っ手割込み1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	コンソール_2 := Tコンソール{}
	コンソール_2.M印刷(buffer)
}

type Tゲートdescriptor struct {
	ゲートデータ [8]uint8
}
type T割込みdescriptortableポインタ struct {
}

var idtデータ [256 * 8]uint8
var A有効割込み管理者 uintptr = 0

const 割込みdebug = false

type T割込み管理者 struct {
	handler_2	[256]uintptr

	ハードウェア割込みoffset	uint16

	タスク管理者	*Tタスク管理者
}

var Primarypicコマンドioポート uint16 = 0x20
var Primarypicデータioポート uint16 = 0x21
var Secondarypicコマンドioポート uint16 = 0xA0
var Secondarypicデータioポート uint16 = 0xA1

func (self *T割込み管理者) Init(ハードウェア割込みoffset uint16, 全般descriptortable *TShareddescriptortable, タスク管理者 *Tタスク管理者) {

	self.タスク管理者 = タスク管理者

	self.ハードウェア割込みoffset = ハードウェア割込みoffset
	codesegment := uint16(Seg中核code)

	for i := 0; i < (256 * 8); i++ {
		idtデータ[i] = 0
	}
	var address uint32
	var Idt割込みゲート uint8 = 0xE
	address = uint32(ValueOf(割込みignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(割込みexceptionhandler0x0f).Pointer())
		self.S割込みdescriptortableentryあり(i, codesegment, address, 0, Idt割込みゲート)
	}

	address = uint32(ValueOf(割込みexceptionhandler0x00).Pointer())
	self.S割込みdescriptortableentryあり(0x00, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x01).Pointer())
	self.S割込みdescriptortableentryあり(0x01, codesegment, address, 0, Idt割込みゲート)
	address = uint32(ValueOf(割込みexceptionhandler0x02).Pointer())
	self.S割込みdescriptortableentryあり(0x02, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x03).Pointer())
	self.S割込みdescriptortableentryあり(0x03, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x04).Pointer())
	self.S割込みdescriptortableentryあり(0x04, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x05).Pointer())
	self.S割込みdescriptortableentryあり(0x05, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x06).Pointer())
	self.S割込みdescriptortableentryあり(0x06, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x07).Pointer())
	self.S割込みdescriptortableentryあり(0x07, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x08).Pointer())
	self.S割込みdescriptortableentryあり(0x08, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x09).Pointer())
	self.S割込みdescriptortableentryあり(0x09, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x0a).Pointer())
	self.S割込みdescriptortableentryあり(0x0A, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x0b).Pointer())
	self.S割込みdescriptortableentryあり(0x0B, codesegment, address, 0, Idt割込みゲート)
	address = uint32(ValueOf(割込みexceptionhandler0x0c).Pointer())
	self.S割込みdescriptortableentryあり(0x0C, codesegment, address, 0, Idt割込みゲート)
	address = uint32(ValueOf(割込みexceptionhandler0x0d).Pointer())
	self.S割込みdescriptortableentryあり(0x0D, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x0e).Pointer())
	self.S割込みdescriptortableentryあり(0x0E, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x0f).Pointer())
	self.S割込みdescriptortableentryあり(0x0F, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x10).Pointer())
	self.S割込みdescriptortableentryあり(0x10, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x11).Pointer())
	self.S割込みdescriptortableentryあり(0x11, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x12).Pointer())
	self.S割込みdescriptortableentryあり(0x12, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みexceptionhandler0x13).Pointer())
	self.S割込みdescriptortableentryあり(0x13, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x00).Pointer())
	self.S割込みdescriptortableentryあり(0x20, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x01).Pointer())
	self.S割込みdescriptortableentryあり(0x21, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x02).Pointer())
	self.S割込みdescriptortableentryあり(0x22, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x03).Pointer())
	self.S割込みdescriptortableentryあり(0x23, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x04).Pointer())
	self.S割込みdescriptortableentryあり(0x24, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x05).Pointer())
	self.S割込みdescriptortableentryあり(0x25, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x06).Pointer())
	self.S割込みdescriptortableentryあり(0x26, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x07).Pointer())
	self.S割込みdescriptortableentryあり(0x27, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x08).Pointer())
	self.S割込みdescriptortableentryあり(0x28, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x09).Pointer())
	self.S割込みdescriptortableentryあり(0x29, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x0a).Pointer())
	self.S割込みdescriptortableentryあり(0x2A, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x0b).Pointer())
	self.S割込みdescriptortableentryあり(0x2B, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x0c).Pointer())
	self.S割込みdescriptortableentryあり(0x2C, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x0d).Pointer())
	self.S割込みdescriptortableentryあり(0x2D, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x0e).Pointer())
	self.S割込みdescriptortableentryあり(0x2E, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x0f).Pointer())
	self.S割込みdescriptortableentryあり(0x2F, codesegment, address, 0, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x80).Pointer())
	self.S割込みdescriptortableentryあり(0x80, codesegment, address, 3, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x81).Pointer())
	self.S割込みdescriptortableentryあり(0x81, codesegment, address, 3, Idt割込みゲート)

	address = uint32(ValueOf(割込みrequesthandler0x82).Pointer())
	self.S割込みdescriptortableentryあり(0x82, codesegment, address, 3, Idt割込みゲート)

	Pポート書込みバイト(Primarypicコマンドioポート, 0x11)
	Pポート書込みバイト(Secondarypicコマンドioポート, 0x11)

	Pポート書込みバイト(Primarypicデータioポート, 0x20)
	Pポート書込みバイト(Secondarypicデータioポート, 0x28)

	Pポート書込みバイト(Primarypicデータioポート, 0x04)
	Pポート書込みバイト(Secondarypicデータioポート, 0x02)

	Pポート書込みバイト(Primarypicデータioポート, 0x01)
	Pポート書込みバイト(Secondarypicデータioポート, 0x01)

	Pポート書込みバイト(Primarypicデータioポート, 0xF8)
	Pポート書込みバイト(Secondarypicデータioポート, 0xEF)

	idtポインタ := [6]uint8{0, 0, 0, 0, 0, 0}
	サイズ := (*uint16)(Pointer(&idtポインタ[0]))
	(*サイズ) = (uint16)(Sizeof(idtデータ) - 1)

	base := (*uint32)(Pointer(&idtポインタ[2]))
	(*base) = uint32(uintptr(Pointer(&idtデータ)))

	Lidt(uintptr(Pointer(&idtポインタ)))
}
func Lidt(lidtaddr uintptr)

func (self *T割込み管理者) S割込みdescriptortableentryあり(割込み int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptor型 uint8) {

	handleraddress低いビット := (*uint16)(Pointer(&idtデータ[割込み*8+0]))
	(*handleraddress低いビット) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtデータ[割込み*8+2]))
	(*gdtcodesegmentselector) = codesegment

	予約 := (*uint8)(Pointer(&idtデータ[割込み*8+4]))
	(*予約) = 0

	var Idtdescriptor現在 uint8 = 0x80
	アクセス := (*uint8)(Pointer(&idtデータ[割込み*8+5]))
	(*アクセス) = (Idtdescriptor現在 | Descriptor型 | ((Descriptorprivilegelevel & 3) << 5))

	handleraddress高いビット := (*uint16)(Pointer(&idtデータ[割込み*8+6]))
	(*handleraddress高いビット) = uint16((handler >> 16) & 0xFFFF)

}

func (self *T割込み管理者) Sありhandler(handler uintptr, I割込みnumber uint8) {
	handler_2[I割込みnumber] = handler
}
func (self *T割込み管理者) Gethandler(I割込みnumber uint8) uintptr {
	return handler_2[I割込みnumber]
}
func (self *T割込み管理者) Do取っ手割込み(割込み uint8, esp uint32) uint32 {

	if 割込みdebug {
		コンソール_2.M印刷xy("[esp:", 1, 20)
		コンソール_2.MUnsignedinteger32印刷(uint32(割込み))
		コンソール_2.M印刷(":")
		コンソール_2.MUnsignedinteger32印刷(esp)
	}
	handler実行 := false
	if handler_2[割込み] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[割込み])))
		esp = myfunction(esp)
		handler実行 = true

	}

	if !handler実行 && 割込み == uint8(self.ハードウェア割込みoffset) && self.タスク管理者 != nil {
		esp = uint32(uintptr(Pointer(self.タスク管理者.Schedule((*Tcpu状態)(Pointer(uintptr(esp)))))))

	}
	if !handler実行 && 割込み == 0x80 {
		esp = 取っ手unhandledsyscall(esp)
	}

	if 割込み <= 0x1F {
	}
	if 0x20 <= 割込み && 割込み < 0x30 {
		if 0x28 <= 割込み {
			Pポート書込みバイト(Secondarypicコマンドioポート, 0x20)
		}
		Pポート書込みバイト(Primarypicコマンドioポート, 0x20)
	}
	return esp
}

var カウント2 uint8 = 1

func ありcr3(address uint32)

var コンソール_2 Tコンソール = Tコンソール{}

func H取っ手割込み(esp uint32, 割込み uint32) uint32 {

	if 割込みdebug && 割込み != 0x80 && 割込み != 0x20 {
		コンソール_2.M印刷xy("[esp:", 1, 21)
		コンソール_2.MUnsignedinteger32印刷(uint32(割込み))
		コンソール_2.M印刷(":")
		コンソール_2.MUnsignedinteger32印刷(esp)
	}

	if A有効割込み管理者 != 0 {
		p := (*T割込み管理者)(Pointer(A有効割込み管理者))
		esp = p.Do取っ手割込み(uint8(割込み), esp)
		return esp
	}
	if handler_2[割込み] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[割込み])))
		esp = myfunction(esp)
	}
	if 割込み == 0x80 {
		return 取っ手unhandledsyscall(esp)
	}
	if 0x20 <= 割込み && 割込み < 0x30 {
		if 0x28 <= 割込み {
			Pポート書込みバイト(Secondarypicコマンドioポート, 0x20)
		}
		Pポート書込みバイト(Primarypicコマンドioポート, 0x20)
	}

	return esp
}

func 取っ手unhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpu状態)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(割込み終了loop).Pointer())
		cpu.Cs = Seg中核code
		cpu.Ds = Seg中核データ
		cpu.Es = Seg中核データ
		cpu.Fs = Seg中核データ
		cpu.Gs = Seg中核gs
		cpu.Ss = Seg中核データ
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasエラーcode(割込み uint32) bool {
	switch 割込み {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exception名前(割込み uint32) string {
	switch 割込み {
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

func exceptionフレーム値(フレーム uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(フレーム + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func 印刷ページ障害info(エラー uint32) {
	MEmergencyログ文字列(" pf=[")
	if (エラー & 0x01) != 0 {
		MEmergencyログ文字列("protection")
	} else {
		MEmergencyログ文字列("not-present")
	}
	if (エラー & 0x02) != 0 {
		MEmergencyログ文字列(",write")
	} else {
		MEmergencyログ文字列(",read")
	}
	if (エラー & 0x04) != 0 {
		MEmergencyログ文字列(",user")
	} else {
		MEmergencyログ文字列(",kernel")
	}
	if (エラー & 0x08) != 0 {
		MEmergencyログ文字列(",reserved-bit")
	}
	if (エラー & 0x10) != 0 {
		MEmergencyログ文字列(",instruction-fetch")
	}
	MEmergencyログ文字列("]")
}

func 印刷exceptionselectorinfo(エラー uint32) {
	MEmergencyログ文字列(" selector=")
	MEmergencyログunsignedinteger32(エラー & 0xFFFFFFF8)
	MEmergencyログ文字列(" index=")
	MEmergencyログunsignedinteger32(エラー >> 3)
	MEmergencyログ文字列(" table=")
	if (エラー & 0x02) != 0 {
		MEmergencyログ文字列("IDT")
	} else if (エラー & 0x04) != 0 {
		MEmergencyログ文字列("LDT")
	} else {
		MEmergencyログ文字列("GDT")
	}
	MEmergencyログ文字列(" ext=")
	MEmergencyログunsignedinteger32(エラー & 0x01)
}

func H取っ手exception(esp uint32, 割込み uint32) uint32 {
	MEmergencyログ文字列("\nEXCEPTION vec=")
	MEmergencyログhexadecimal8(uint8(割込み))
	MEmergencyログ文字列(" ")
	MEmergencyログ文字列(exception名前(割込み))
	MEmergencyログ文字列(" frame=")
	MEmergencyログunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyログ文字列(" invalid-frame")
		if exceptionhasエラーcode(割込み) {
			MEmergencyログ文字列(" raw-error-or-bad-esp=")
			MEmergencyログunsignedinteger32(esp)
			印刷exceptionselectorinfo(esp)
		}
		MEmergencyログ文字列("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var エラー uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasエラーcode(割込み) {
		エラー = exceptionフレーム値(esp, 0)
		eipoffset = 4
	}
	eip := exceptionフレーム値(esp, eipoffset)
	cs := exceptionフレーム値(esp, eipoffset+4)
	eflags := exceptionフレーム値(esp, eipoffset+8)

	MEmergencyログ文字列(" err=")
	MEmergencyログunsignedinteger32(エラー)
	MEmergencyログ文字列(" eip=")
	MEmergencyログunsignedinteger32(eip)
	MEmergencyログ文字列(" cs=")
	MEmergencyログunsignedinteger32(cs)
	MEmergencyログ文字列(" eflags=")
	MEmergencyログunsignedinteger32(eflags)
	MEmergencyログ文字列(" cr0=")
	MEmergencyログunsignedinteger32(exceptioncr0())
	MEmergencyログ文字列(" cr3=")
	MEmergencyログunsignedinteger32(exceptioncr3())

	if 割込み == 0x0E {
		MEmergencyログ文字列(" cr2=")
		MEmergencyログunsignedinteger32(exceptioncr2())
		印刷ページ障害info(エラー)
	}

	if (cs & 0x03) != 0 {
		MEmergencyログ文字列(" useresp=")
		MEmergencyログunsignedinteger32(exceptionフレーム値(esp, eipoffset+12))
		MEmergencyログ文字列(" ss=")
		MEmergencyログunsignedinteger32(exceptionフレーム値(esp, eipoffset+16))
	}

	if exceptionhasエラーcode(割込み) {
		印刷exceptionselectorinfo(エラー)
	}
	MEmergencyログ文字列("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func halt後fatalexception()

func H取っ手fatal割込みフレーム(保存済みesp uint32, 割込み uint32) uint32 {
	H取っ手exception(保存済みesp+52, 割込み)
	halt後fatalexception()
	return 保存済みesp
}

func I割込み有効()
func (self *T割込み管理者) A有効() {
	if A有効割込み管理者 != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	A有効割込み管理者 = address
	I割込み有効()
}
func I割込みdeactive()
func (self *T割込み管理者) Deactive() {
	A有効割込み管理者 = 0
	I割込みdeactive()
}

func My取っ手割込み(割込み uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	コンソール_2 := Tコンソール{}
	コンソール_2.M印刷(buffer)
	return esp
}
func Myテスト(割込み uint8, esp uint32)

func Unhandle割込み() {
	buffer := []byte("unhandle interrupt\n")
	コンソール_2 := Tコンソール{}
	コンソール_2.M印刷(buffer)
}

func 割込みhandler_2(割込み uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	コンソール_2 := Tコンソール{}
	コンソール_2.M印刷(buffer)
	コンソール_2.MHexadecimal印刷(0x40)
	return esp
}
func 印刷esp(esp uint32) {
	コンソール_2 := Tコンソール{}
	コンソール_2.MUnsignedinteger32印刷xy(esp, 20, 21)
}
func gettls() uint32
func P印刷tls() {

}
