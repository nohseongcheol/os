/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package I中斷

import . "unsafe"
import . "reflect"

import . "連接埠"
import . "gdt"
import . "多重工作管理"
import . "控制台"

func 中斷ignore()

func 中斷exceptionhandler()
func 中斷exceptionhandler0x00()
func 中斷exceptionhandler0x01()
func 中斷exceptionhandler0x02()
func 中斷exceptionhandler0x03()
func 中斷exceptionhandler0x04()
func 中斷exceptionhandler0x05()
func 中斷exceptionhandler0x06()
func 中斷exceptionhandler0x07()
func 中斷exceptionhandler0x08()
func 中斷exceptionhandler0x09()
func 中斷exceptionhandler0x0a()
func 中斷exceptionhandler0x0b()
func 中斷exceptionhandler0x0c()
func 中斷exceptionhandler0x0d()
func 中斷exceptionhandler0x0e()
func 中斷exceptionhandler0x0f()
func 中斷exceptionhandler0x10()
func 中斷exceptionhandler0x11()
func 中斷exceptionhandler0x12()
func 中斷exceptionhandler0x13()

func 中斷requesthandler0x00()
func 中斷requesthandler0x01()
func 中斷requesthandler0x02()
func 中斷requesthandler0x03()
func 中斷requesthandler0x04()
func 中斷requesthandler0x05()
func 中斷requesthandler0x06()
func 中斷requesthandler0x07()
func 中斷requesthandler0x08()
func 中斷requesthandler0x09()
func 中斷requesthandler0x0a()
func 中斷requesthandler0x0b()
func 中斷requesthandler0x0c()
func 中斷requesthandler0x0d()
func 中斷requesthandler0x0e()
func 中斷requesthandler0x0f()

func 中斷requesthandler0x80()
func 中斷requesthandler0x81()
func 中斷requesthandler0x82()

func T測試列印(位置 uint8, 資料 uint8)
func 設定ds(dssegment uint32)
func 設定gs(gssegment uint32)
func 中斷離開迴圈()

type T中斷handler struct {
	I中斷數字	uint8
	I中斷管理器	uintptr
}
type I中斷handler interface {
	H控制把中斷(uint32) uint32
}

func N新增中斷handler(I中斷管理器 uintptr, I中斷數字 uint8) *T中斷handler {
	中斷handler_2 := new(T中斷handler)
	中斷handler_2.I中斷數字 = I中斷數字
	中斷handler_2.I中斷管理器 = I中斷管理器
	return 中斷handler_2

}

var handler_2 [256]uintptr

func (self *T中斷handler) Init(I中斷數字 uint8, I中斷管理器 uintptr, funcaddress uintptr) {

	handler_2[I中斷數字] = funcaddress

	self.I中斷數字 = I中斷數字
	self.I中斷管理器 = I中斷管理器

}
func (self *T中斷handler) S設定控制把中斷fuction(I中斷數字 uint32, address uintptr) {
	handler_2[I中斷數字] = address
}
func (self *T中斷handler) D銷毀() {
	selfuintptr := uintptr(Pointer(self))
	I中斷管理器 := (*T中斷管理器)(Pointer(self.I中斷管理器))
	if selfuintptr == I中斷管理器.Gethandler(self.I中斷數字) {
		I中斷管理器.S設定handler(0, self.I中斷數字)
	}

}
func (self *T中斷handler) S設定中斷管理器(I中斷管理器 uintptr) {
}
func (self *T中斷handler) S設定中斷數字(I中斷數字 uint8) {
	self.I中斷數字 = I中斷數字
}
func (self *T中斷handler) H控制把中斷(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	控制台_2 := T控制台{}
	控制台_2.M列印(buffer)
	return esp
}
func H控制把中斷1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	控制台_2 := T控制台{}
	控制台_2.M列印(buffer)
}

type T入口descriptor struct {
	入口資料 [8]uint8
}
type T中斷descriptortable指標 struct {
}

var idt資料 [256 * 8]uint8
var A啟用中斷管理器 uintptr = 0

const 中斷除錯 = false

type T中斷管理器 struct {
	handler_2	[256]uintptr

	硬體中斷位移	uint16

	工作管理器	*T工作管理器
}

var Primarypic指令io連接埠 uint16 = 0x20
var Primarypic資料io連接埠 uint16 = 0x21
var Secondarypic指令io連接埠 uint16 = 0xA0
var Secondarypic資料io連接埠 uint16 = 0xA1

func (self *T中斷管理器) Init(硬體中斷位移 uint16, 全域descriptortable *TShareddescriptortable, 工作管理器 *T工作管理器) {

	self.工作管理器 = 工作管理器

	self.硬體中斷位移 = 硬體中斷位移
	codesegment := uint16(Seg核心code)

	for i := 0; i < (256 * 8); i++ {
		idt資料[i] = 0
	}
	var address uint32
	var Idt中斷入口 uint8 = 0xE
	address = uint32(ValueOf(中斷ignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(中斷exceptionhandler0x0f).Pointer())
		self.S中斷descriptortable項目設定(i, codesegment, address, 0, Idt中斷入口)
	}

	address = uint32(ValueOf(中斷exceptionhandler0x00).Pointer())
	self.S中斷descriptortable項目設定(0x00, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x01).Pointer())
	self.S中斷descriptortable項目設定(0x01, codesegment, address, 0, Idt中斷入口)
	address = uint32(ValueOf(中斷exceptionhandler0x02).Pointer())
	self.S中斷descriptortable項目設定(0x02, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x03).Pointer())
	self.S中斷descriptortable項目設定(0x03, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x04).Pointer())
	self.S中斷descriptortable項目設定(0x04, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x05).Pointer())
	self.S中斷descriptortable項目設定(0x05, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x06).Pointer())
	self.S中斷descriptortable項目設定(0x06, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x07).Pointer())
	self.S中斷descriptortable項目設定(0x07, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x08).Pointer())
	self.S中斷descriptortable項目設定(0x08, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x09).Pointer())
	self.S中斷descriptortable項目設定(0x09, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x0a).Pointer())
	self.S中斷descriptortable項目設定(0x0A, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x0b).Pointer())
	self.S中斷descriptortable項目設定(0x0B, codesegment, address, 0, Idt中斷入口)
	address = uint32(ValueOf(中斷exceptionhandler0x0c).Pointer())
	self.S中斷descriptortable項目設定(0x0C, codesegment, address, 0, Idt中斷入口)
	address = uint32(ValueOf(中斷exceptionhandler0x0d).Pointer())
	self.S中斷descriptortable項目設定(0x0D, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x0e).Pointer())
	self.S中斷descriptortable項目設定(0x0E, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x0f).Pointer())
	self.S中斷descriptortable項目設定(0x0F, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x10).Pointer())
	self.S中斷descriptortable項目設定(0x10, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x11).Pointer())
	self.S中斷descriptortable項目設定(0x11, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x12).Pointer())
	self.S中斷descriptortable項目設定(0x12, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷exceptionhandler0x13).Pointer())
	self.S中斷descriptortable項目設定(0x13, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x00).Pointer())
	self.S中斷descriptortable項目設定(0x20, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x01).Pointer())
	self.S中斷descriptortable項目設定(0x21, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x02).Pointer())
	self.S中斷descriptortable項目設定(0x22, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x03).Pointer())
	self.S中斷descriptortable項目設定(0x23, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x04).Pointer())
	self.S中斷descriptortable項目設定(0x24, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x05).Pointer())
	self.S中斷descriptortable項目設定(0x25, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x06).Pointer())
	self.S中斷descriptortable項目設定(0x26, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x07).Pointer())
	self.S中斷descriptortable項目設定(0x27, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x08).Pointer())
	self.S中斷descriptortable項目設定(0x28, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x09).Pointer())
	self.S中斷descriptortable項目設定(0x29, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x0a).Pointer())
	self.S中斷descriptortable項目設定(0x2A, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x0b).Pointer())
	self.S中斷descriptortable項目設定(0x2B, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x0c).Pointer())
	self.S中斷descriptortable項目設定(0x2C, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x0d).Pointer())
	self.S中斷descriptortable項目設定(0x2D, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x0e).Pointer())
	self.S中斷descriptortable項目設定(0x2E, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x0f).Pointer())
	self.S中斷descriptortable項目設定(0x2F, codesegment, address, 0, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x80).Pointer())
	self.S中斷descriptortable項目設定(0x80, codesegment, address, 3, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x81).Pointer())
	self.S中斷descriptortable項目設定(0x81, codesegment, address, 3, Idt中斷入口)

	address = uint32(ValueOf(中斷requesthandler0x82).Pointer())
	self.S中斷descriptortable項目設定(0x82, codesegment, address, 3, Idt中斷入口)

	P連接埠寫入位元組(Primarypic指令io連接埠, 0x11)
	P連接埠寫入位元組(Secondarypic指令io連接埠, 0x11)

	P連接埠寫入位元組(Primarypic資料io連接埠, 0x20)
	P連接埠寫入位元組(Secondarypic資料io連接埠, 0x28)

	P連接埠寫入位元組(Primarypic資料io連接埠, 0x04)
	P連接埠寫入位元組(Secondarypic資料io連接埠, 0x02)

	P連接埠寫入位元組(Primarypic資料io連接埠, 0x01)
	P連接埠寫入位元組(Secondarypic資料io連接埠, 0x01)

	P連接埠寫入位元組(Primarypic資料io連接埠, 0xF8)
	P連接埠寫入位元組(Secondarypic資料io連接埠, 0xEF)

	idt指標 := [6]uint8{0, 0, 0, 0, 0, 0}
	大小 := (*uint16)(Pointer(&idt指標[0]))
	(*大小) = (uint16)(Sizeof(idt資料) - 1)

	base := (*uint32)(Pointer(&idt指標[2]))
	(*base) = uint32(uintptr(Pointer(&idt資料)))

	Lidt(uintptr(Pointer(&idt指標)))
}
func Lidt(lidtaddr uintptr)

func (self *T中斷管理器) S中斷descriptortable項目設定(中斷 int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptor類型 uint8) {

	handleraddress低位元 := (*uint16)(Pointer(&idt資料[中斷*8+0]))
	(*handleraddress低位元) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idt資料[中斷*8+2]))
	(*gdtcodesegmentselector) = codesegment

	預留 := (*uint8)(Pointer(&idt資料[中斷*8+4]))
	(*預留) = 0

	var Idtdescriptor目前 uint8 = 0x80
	存取 := (*uint8)(Pointer(&idt資料[中斷*8+5]))
	(*存取) = (Idtdescriptor目前 | Descriptor類型 | ((Descriptorprivilegelevel & 3) << 5))

	handleraddress高位元 := (*uint16)(Pointer(&idt資料[中斷*8+6]))
	(*handleraddress高位元) = uint16((handler >> 16) & 0xFFFF)

}

func (self *T中斷管理器) S設定handler(handler uintptr, I中斷數字 uint8) {
	handler_2[I中斷數字] = handler
}
func (self *T中斷管理器) Gethandler(I中斷數字 uint8) uintptr {
	return handler_2[I中斷數字]
}
func (self *T中斷管理器) Do控制把中斷(中斷 uint8, esp uint32) uint32 {

	if 中斷除錯 {
		控制台_2.M列印xy("[esp:", 1, 20)
		控制台_2.MUnsignedinteger32列印(uint32(中斷))
		控制台_2.M列印(":")
		控制台_2.MUnsignedinteger32列印(esp)
	}
	handler執行 := false
	if handler_2[中斷] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[中斷])))
		esp = myfunction(esp)
		handler執行 = true

	}

	if !handler執行 && 中斷 == uint8(self.硬體中斷位移) && self.工作管理器 != nil {
		esp = uint32(uintptr(Pointer(self.工作管理器.Schedule((*Tcpu狀態)(Pointer(uintptr(esp)))))))

	}
	if !handler執行 && 中斷 == 0x80 {
		esp = 控制把unhandledsyscall(esp)
	}

	if 中斷 <= 0x1F {
	}
	if 0x20 <= 中斷 && 中斷 < 0x30 {
		if 0x28 <= 中斷 {
			P連接埠寫入位元組(Secondarypic指令io連接埠, 0x20)
		}
		P連接埠寫入位元組(Primarypic指令io連接埠, 0x20)
	}
	return esp
}

var 計數2 uint8 = 1

func 設定cr3(address uint32)

var 控制台_2 T控制台 = T控制台{}

func H控制把中斷(esp uint32, 中斷 uint32) uint32 {

	if 中斷除錯 && 中斷 != 0x80 && 中斷 != 0x20 {
		控制台_2.M列印xy("[esp:", 1, 21)
		控制台_2.MUnsignedinteger32列印(uint32(中斷))
		控制台_2.M列印(":")
		控制台_2.MUnsignedinteger32列印(esp)
	}

	if A啟用中斷管理器 != 0 {
		p := (*T中斷管理器)(Pointer(A啟用中斷管理器))
		esp = p.Do控制把中斷(uint8(中斷), esp)
		return esp
	}
	if handler_2[中斷] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[中斷])))
		esp = myfunction(esp)
	}
	if 中斷 == 0x80 {
		return 控制把unhandledsyscall(esp)
	}
	if 0x20 <= 中斷 && 中斷 < 0x30 {
		if 0x28 <= 中斷 {
			P連接埠寫入位元組(Secondarypic指令io連接埠, 0x20)
		}
		P連接埠寫入位元組(Primarypic指令io連接埠, 0x20)
	}

	return esp
}

func 控制把unhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpu狀態)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(中斷離開迴圈).Pointer())
		cpu.Cs = Seg核心code
		cpu.Ds = Seg核心資料
		cpu.Es = Seg核心資料
		cpu.Fs = Seg核心資料
		cpu.Gs = Seg核心gs
		cpu.Ss = Seg核心資料
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhas錯誤code(中斷 uint32) bool {
	switch 中斷 {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exception名稱(中斷 uint32) string {
	switch 中斷 {
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

func exception框架數值(框架 uint32, 位移 uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(框架 + 位移)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func 列印頁故障資訊(出錯 uint32) {
	MEmergency記錄字串(" pf=[")
	if (出錯 & 0x01) != 0 {
		MEmergency記錄字串("protection")
	} else {
		MEmergency記錄字串("not-present")
	}
	if (出錯 & 0x02) != 0 {
		MEmergency記錄字串(",write")
	} else {
		MEmergency記錄字串(",read")
	}
	if (出錯 & 0x04) != 0 {
		MEmergency記錄字串(",user")
	} else {
		MEmergency記錄字串(",kernel")
	}
	if (出錯 & 0x08) != 0 {
		MEmergency記錄字串(",reserved-bit")
	}
	if (出錯 & 0x10) != 0 {
		MEmergency記錄字串(",instruction-fetch")
	}
	MEmergency記錄字串("]")
}

func 列印exceptionselector資訊(出錯 uint32) {
	MEmergency記錄字串(" selector=")
	MEmergency記錄unsignedinteger32(出錯 & 0xFFFFFFF8)
	MEmergency記錄字串(" index=")
	MEmergency記錄unsignedinteger32(出錯 >> 3)
	MEmergency記錄字串(" table=")
	if (出錯 & 0x02) != 0 {
		MEmergency記錄字串("IDT")
	} else if (出錯 & 0x04) != 0 {
		MEmergency記錄字串("LDT")
	} else {
		MEmergency記錄字串("GDT")
	}
	MEmergency記錄字串(" ext=")
	MEmergency記錄unsignedinteger32(出錯 & 0x01)
}

func H控制把exception(esp uint32, 中斷 uint32) uint32 {
	MEmergency記錄字串("\nEXCEPTION vec=")
	MEmergency記錄hexadecimal8(uint8(中斷))
	MEmergency記錄字串(" ")
	MEmergency記錄字串(exception名稱(中斷))
	MEmergency記錄字串(" frame=")
	MEmergency記錄unsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergency記錄字串(" invalid-frame")
		if exceptionhas錯誤code(中斷) {
			MEmergency記錄字串(" raw-error-or-bad-esp=")
			MEmergency記錄unsignedinteger32(esp)
			列印exceptionselector資訊(esp)
		}
		MEmergency記錄字串("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var 出錯 uint32 = 0
	var eip位移 uint32 = 0
	if exceptionhas錯誤code(中斷) {
		出錯 = exception框架數值(esp, 0)
		eip位移 = 4
	}
	eip := exception框架數值(esp, eip位移)
	cs := exception框架數值(esp, eip位移+4)
	eflags := exception框架數值(esp, eip位移+8)

	MEmergency記錄字串(" err=")
	MEmergency記錄unsignedinteger32(出錯)
	MEmergency記錄字串(" eip=")
	MEmergency記錄unsignedinteger32(eip)
	MEmergency記錄字串(" cs=")
	MEmergency記錄unsignedinteger32(cs)
	MEmergency記錄字串(" eflags=")
	MEmergency記錄unsignedinteger32(eflags)
	MEmergency記錄字串(" cr0=")
	MEmergency記錄unsignedinteger32(exceptioncr0())
	MEmergency記錄字串(" cr3=")
	MEmergency記錄unsignedinteger32(exceptioncr3())

	if 中斷 == 0x0E {
		MEmergency記錄字串(" cr2=")
		MEmergency記錄unsignedinteger32(exceptioncr2())
		列印頁故障資訊(出錯)
	}

	if (cs & 0x03) != 0 {
		MEmergency記錄字串(" useresp=")
		MEmergency記錄unsignedinteger32(exception框架數值(esp, eip位移+12))
		MEmergency記錄字串(" ss=")
		MEmergency記錄unsignedinteger32(exception框架數值(esp, eip位移+16))
	}

	if exceptionhas錯誤code(中斷) {
		列印exceptionselector資訊(出錯)
	}
	MEmergency記錄字串("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func halt之後fatalexception()

func H控制把fatal中斷框架(已儲存esp uint32, 中斷 uint32) uint32 {
	H控制把exception(已儲存esp+52, 中斷)
	halt之後fatalexception()
	return 已儲存esp
}

func I中斷啟用()
func (self *T中斷管理器) A啟用() {
	if A啟用中斷管理器 != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	A啟用中斷管理器 = address
	I中斷啟用()
}
func I中斷deactive()
func (self *T中斷管理器) Deactive() {
	A啟用中斷管理器 = 0
	I中斷deactive()
}

func My控制把中斷(中斷 uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	控制台_2 := T控制台{}
	控制台_2.M列印(buffer)
	return esp
}
func My測試(中斷 uint8, esp uint32)

func Unhandle中斷() {
	buffer := []byte("unhandle interrupt\n")
	控制台_2 := T控制台{}
	控制台_2.M列印(buffer)
}

func 中斷handler_2(中斷 uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	控制台_2 := T控制台{}
	控制台_2.M列印(buffer)
	控制台_2.MHexadecimal列印(0x40)
	return esp
}
func 列印esp(esp uint32) {
	控制台_2 := T控制台{}
	控制台_2.MUnsignedinteger32列印xy(esp, 20, 21)
}
func gettls() uint32
func P列印tls() {

}
