/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package I中断

import . "unsafe"
import . "reflect"

import . "端口"
import . "gdt"
import . "多重任务管理"
import . "控制台"

func 中断ignore()

func 中断exceptionhandler()
func 中断exceptionhandler0x00()
func 中断exceptionhandler0x01()
func 中断exceptionhandler0x02()
func 中断exceptionhandler0x03()
func 中断exceptionhandler0x04()
func 中断exceptionhandler0x05()
func 中断exceptionhandler0x06()
func 中断exceptionhandler0x07()
func 中断exceptionhandler0x08()
func 中断exceptionhandler0x09()
func 中断exceptionhandler0x0a()
func 中断exceptionhandler0x0b()
func 中断exceptionhandler0x0c()
func 中断exceptionhandler0x0d()
func 中断exceptionhandler0x0e()
func 中断exceptionhandler0x0f()
func 中断exceptionhandler0x10()
func 中断exceptionhandler0x11()
func 中断exceptionhandler0x12()
func 中断exceptionhandler0x13()

func 中断requesthandler0x00()
func 中断requesthandler0x01()
func 中断requesthandler0x02()
func 中断requesthandler0x03()
func 中断requesthandler0x04()
func 中断requesthandler0x05()
func 中断requesthandler0x06()
func 中断requesthandler0x07()
func 中断requesthandler0x08()
func 中断requesthandler0x09()
func 中断requesthandler0x0a()
func 中断requesthandler0x0b()
func 中断requesthandler0x0c()
func 中断requesthandler0x0d()
func 中断requesthandler0x0e()
func 中断requesthandler0x0f()

func 中断requesthandler0x80()
func 中断requesthandler0x81()
func 中断requesthandler0x82()

func T测试打印(位置 uint8, 数据 uint8)
func 集合ds(dssegment uint32)
func 集合gs(gssegment uint32)
func 中断退出loop()

type T中断handler struct {
	I中断数字	uint8
	I中断管理器	uintptr
}
type I中断handler interface {
	H控制器中断(uint32) uint32
}

func N新建中断handler(I中断管理器 uintptr, I中断数字 uint8) *T中断handler {
	中断handler_2 := new(T中断handler)
	中断handler_2.I中断数字 = I中断数字
	中断handler_2.I中断管理器 = I中断管理器
	return 中断handler_2

}

var handler_2 [256]uintptr

func (self *T中断handler) Init(I中断数字 uint8, I中断管理器 uintptr, funcaddress uintptr) {

	handler_2[I中断数字] = funcaddress

	self.I中断数字 = I中断数字
	self.I中断管理器 = I中断管理器

}
func (self *T中断handler) S集合控制器中断fuction(I中断数字 uint32, address uintptr) {
	handler_2[I中断数字] = address
}
func (self *T中断handler) D摧毁() {
	selfuintptr := uintptr(Pointer(self))
	I中断管理器 := (*T中断管理器)(Pointer(self.I中断管理器))
	if selfuintptr == I中断管理器.Gethandler(self.I中断数字) {
		I中断管理器.S集合handler(0, self.I中断数字)
	}

}
func (self *T中断handler) S集合中断管理器(I中断管理器 uintptr) {
}
func (self *T中断handler) S集合中断数字(I中断数字 uint8) {
	self.I中断数字 = I中断数字
}
func (self *T中断handler) H控制器中断(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	控制台_2 := T控制台{}
	控制台_2.M打印(buffer)
	return esp
}
func H控制器中断1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	控制台_2 := T控制台{}
	控制台_2.M打印(buffer)
}

type T入口descriptor struct {
	入口数据 [8]uint8
}
type T中断descriptor表格指针 struct {
}

var idt数据 [256 * 8]uint8
var A活跃中断管理器 uintptr = 0

const 中断调试 = false

type T中断管理器 struct {
	handler_2	[256]uintptr

	硬件中断位移	uint16

	任务管理器	*T任务管理器
}

var Primarypic命令输入输出端口 uint16 = 0x20
var Primarypic数据输入输出端口 uint16 = 0x21
var Secondarypic命令输入输出端口 uint16 = 0xA0
var Secondarypic数据输入输出端口 uint16 = 0xA1

func (self *T中断管理器) Init(硬件中断位移 uint16, 全局descriptor表格 *TShareddescriptor表格, 任务管理器 *T任务管理器) {

	self.任务管理器 = 任务管理器

	self.硬件中断位移 = 硬件中断位移
	codesegment := uint16(Seg内核code)

	for i := 0; i < (256 * 8); i++ {
		idt数据[i] = 0
	}
	var address uint32
	var Idt中断入口 uint8 = 0xE
	address = uint32(ValueOf(中断ignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(中断exceptionhandler0x0f).Pointer())
		self.S中断descriptor表格条目集合(i, codesegment, address, 0, Idt中断入口)
	}

	address = uint32(ValueOf(中断exceptionhandler0x00).Pointer())
	self.S中断descriptor表格条目集合(0x00, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x01).Pointer())
	self.S中断descriptor表格条目集合(0x01, codesegment, address, 0, Idt中断入口)
	address = uint32(ValueOf(中断exceptionhandler0x02).Pointer())
	self.S中断descriptor表格条目集合(0x02, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x03).Pointer())
	self.S中断descriptor表格条目集合(0x03, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x04).Pointer())
	self.S中断descriptor表格条目集合(0x04, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x05).Pointer())
	self.S中断descriptor表格条目集合(0x05, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x06).Pointer())
	self.S中断descriptor表格条目集合(0x06, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x07).Pointer())
	self.S中断descriptor表格条目集合(0x07, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x08).Pointer())
	self.S中断descriptor表格条目集合(0x08, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x09).Pointer())
	self.S中断descriptor表格条目集合(0x09, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x0a).Pointer())
	self.S中断descriptor表格条目集合(0x0A, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x0b).Pointer())
	self.S中断descriptor表格条目集合(0x0B, codesegment, address, 0, Idt中断入口)
	address = uint32(ValueOf(中断exceptionhandler0x0c).Pointer())
	self.S中断descriptor表格条目集合(0x0C, codesegment, address, 0, Idt中断入口)
	address = uint32(ValueOf(中断exceptionhandler0x0d).Pointer())
	self.S中断descriptor表格条目集合(0x0D, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x0e).Pointer())
	self.S中断descriptor表格条目集合(0x0E, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x0f).Pointer())
	self.S中断descriptor表格条目集合(0x0F, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x10).Pointer())
	self.S中断descriptor表格条目集合(0x10, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x11).Pointer())
	self.S中断descriptor表格条目集合(0x11, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x12).Pointer())
	self.S中断descriptor表格条目集合(0x12, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断exceptionhandler0x13).Pointer())
	self.S中断descriptor表格条目集合(0x13, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x00).Pointer())
	self.S中断descriptor表格条目集合(0x20, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x01).Pointer())
	self.S中断descriptor表格条目集合(0x21, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x02).Pointer())
	self.S中断descriptor表格条目集合(0x22, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x03).Pointer())
	self.S中断descriptor表格条目集合(0x23, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x04).Pointer())
	self.S中断descriptor表格条目集合(0x24, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x05).Pointer())
	self.S中断descriptor表格条目集合(0x25, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x06).Pointer())
	self.S中断descriptor表格条目集合(0x26, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x07).Pointer())
	self.S中断descriptor表格条目集合(0x27, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x08).Pointer())
	self.S中断descriptor表格条目集合(0x28, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x09).Pointer())
	self.S中断descriptor表格条目集合(0x29, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x0a).Pointer())
	self.S中断descriptor表格条目集合(0x2A, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x0b).Pointer())
	self.S中断descriptor表格条目集合(0x2B, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x0c).Pointer())
	self.S中断descriptor表格条目集合(0x2C, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x0d).Pointer())
	self.S中断descriptor表格条目集合(0x2D, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x0e).Pointer())
	self.S中断descriptor表格条目集合(0x2E, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x0f).Pointer())
	self.S中断descriptor表格条目集合(0x2F, codesegment, address, 0, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x80).Pointer())
	self.S中断descriptor表格条目集合(0x80, codesegment, address, 3, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x81).Pointer())
	self.S中断descriptor表格条目集合(0x81, codesegment, address, 3, Idt中断入口)

	address = uint32(ValueOf(中断requesthandler0x82).Pointer())
	self.S中断descriptor表格条目集合(0x82, codesegment, address, 3, Idt中断入口)

	P端口写入字节(Primarypic命令输入输出端口, 0x11)
	P端口写入字节(Secondarypic命令输入输出端口, 0x11)

	P端口写入字节(Primarypic数据输入输出端口, 0x20)
	P端口写入字节(Secondarypic数据输入输出端口, 0x28)

	P端口写入字节(Primarypic数据输入输出端口, 0x04)
	P端口写入字节(Secondarypic数据输入输出端口, 0x02)

	P端口写入字节(Primarypic数据输入输出端口, 0x01)
	P端口写入字节(Secondarypic数据输入输出端口, 0x01)

	P端口写入字节(Primarypic数据输入输出端口, 0xF8)
	P端口写入字节(Secondarypic数据输入输出端口, 0xEF)

	idt指针 := [6]uint8{0, 0, 0, 0, 0, 0}
	大小 := (*uint16)(Pointer(&idt指针[0]))
	(*大小) = (uint16)(Sizeof(idt数据) - 1)

	base := (*uint32)(Pointer(&idt指针[2]))
	(*base) = uint32(uintptr(Pointer(&idt数据)))

	Lidt(uintptr(Pointer(&idt指针)))
}
func Lidt(lidtaddr uintptr)

func (self *T中断管理器) S中断descriptor表格条目集合(中断 int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptor类型 uint8) {

	handleraddress低位 := (*uint16)(Pointer(&idt数据[中断*8+0]))
	(*handleraddress低位) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idt数据[中断*8+2]))
	(*gdtcodesegmentselector) = codesegment

	保留的 := (*uint8)(Pointer(&idt数据[中断*8+4]))
	(*保留的) = 0

	var Idtdescriptor当前电池 uint8 = 0x80
	访问 := (*uint8)(Pointer(&idt数据[中断*8+5]))
	(*访问) = (Idtdescriptor当前电池 | Descriptor类型 | ((Descriptorprivilegelevel & 3) << 5))

	handleraddress高位 := (*uint16)(Pointer(&idt数据[中断*8+6]))
	(*handleraddress高位) = uint16((handler >> 16) & 0xFFFF)

}

func (self *T中断管理器) S集合handler(handler uintptr, I中断数字 uint8) {
	handler_2[I中断数字] = handler
}
func (self *T中断管理器) Gethandler(I中断数字 uint8) uintptr {
	return handler_2[I中断数字]
}
func (self *T中断管理器) Do控制器中断(中断 uint8, esp uint32) uint32 {

	if 中断调试 {
		控制台_2.M打印xy("[esp:", 1, 20)
		控制台_2.MUnsignedinteger32打印(uint32(中断))
		控制台_2.M打印(":")
		控制台_2.MUnsignedinteger32打印(esp)
	}
	handler运行 := false
	if handler_2[中断] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[中断])))
		esp = myfunction(esp)
		handler运行 = true

	}

	if !handler运行 && 中断 == uint8(self.硬件中断位移) && self.任务管理器 != nil {
		esp = uint32(uintptr(Pointer(self.任务管理器.Schedule((*Tcpu状态)(Pointer(uintptr(esp)))))))

	}
	if !handler运行 && 中断 == 0x80 {
		esp = 控制器unhandledsyscall(esp)
	}

	if 中断 <= 0x1F {
	}
	if 0x20 <= 中断 && 中断 < 0x30 {
		if 0x28 <= 中断 {
			P端口写入字节(Secondarypic命令输入输出端口, 0x20)
		}
		P端口写入字节(Primarypic命令输入输出端口, 0x20)
	}
	return esp
}

var 计数2 uint8 = 1

func 集合cr3(address uint32)

var 控制台_2 T控制台 = T控制台{}

func H控制器中断(esp uint32, 中断 uint32) uint32 {

	if 中断调试 && 中断 != 0x80 && 中断 != 0x20 {
		控制台_2.M打印xy("[esp:", 1, 21)
		控制台_2.MUnsignedinteger32打印(uint32(中断))
		控制台_2.M打印(":")
		控制台_2.MUnsignedinteger32打印(esp)
	}

	if A活跃中断管理器 != 0 {
		p := (*T中断管理器)(Pointer(A活跃中断管理器))
		esp = p.Do控制器中断(uint8(中断), esp)
		return esp
	}
	if handler_2[中断] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[中断])))
		esp = myfunction(esp)
	}
	if 中断 == 0x80 {
		return 控制器unhandledsyscall(esp)
	}
	if 0x20 <= 中断 && 中断 < 0x30 {
		if 0x28 <= 中断 {
			P端口写入字节(Secondarypic命令输入输出端口, 0x20)
		}
		P端口写入字节(Primarypic命令输入输出端口, 0x20)
	}

	return esp
}

func 控制器unhandledsyscall(esp uint32) uint32 {
	cpu := (*Tcpu状态)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(中断退出loop).Pointer())
		cpu.Cs = Seg内核code
		cpu.Ds = Seg内核数据
		cpu.Es = Seg内核数据
		cpu.Fs = Seg内核数据
		cpu.Gs = Seg内核gs
		cpu.Ss = Seg内核数据
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exception哈斯区错误code(中断 uint32) bool {
	switch 中断 {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exception名称(中断 uint32) string {
	switch 中断 {
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

func exception帧值(帧 uint32, 位移 uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(帧 + 位移)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func 打印页故障信息(错误 uint32) {
	MEmergency日志字符串(" pf=[")
	if (错误 & 0x01) != 0 {
		MEmergency日志字符串("protection")
	} else {
		MEmergency日志字符串("not-present")
	}
	if (错误 & 0x02) != 0 {
		MEmergency日志字符串(",write")
	} else {
		MEmergency日志字符串(",read")
	}
	if (错误 & 0x04) != 0 {
		MEmergency日志字符串(",user")
	} else {
		MEmergency日志字符串(",kernel")
	}
	if (错误 & 0x08) != 0 {
		MEmergency日志字符串(",reserved-bit")
	}
	if (错误 & 0x10) != 0 {
		MEmergency日志字符串(",instruction-fetch")
	}
	MEmergency日志字符串("]")
}

func 打印exceptionselector信息(错误 uint32) {
	MEmergency日志字符串(" selector=")
	MEmergency日志unsignedinteger32(错误 & 0xFFFFFFF8)
	MEmergency日志字符串(" index=")
	MEmergency日志unsignedinteger32(错误 >> 3)
	MEmergency日志字符串(" table=")
	if (错误 & 0x02) != 0 {
		MEmergency日志字符串("IDT")
	} else if (错误 & 0x04) != 0 {
		MEmergency日志字符串("LDT")
	} else {
		MEmergency日志字符串("GDT")
	}
	MEmergency日志字符串(" ext=")
	MEmergency日志unsignedinteger32(错误 & 0x01)
}

func H控制器exception(esp uint32, 中断 uint32) uint32 {
	MEmergency日志字符串("\nEXCEPTION vec=")
	MEmergency日志hexadecimal8(uint8(中断))
	MEmergency日志字符串(" ")
	MEmergency日志字符串(exception名称(中断))
	MEmergency日志字符串(" frame=")
	MEmergency日志unsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergency日志字符串(" invalid-frame")
		if exception哈斯区错误code(中断) {
			MEmergency日志字符串(" raw-error-or-bad-esp=")
			MEmergency日志unsignedinteger32(esp)
			打印exceptionselector信息(esp)
		}
		MEmergency日志字符串("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var 错误 uint32 = 0
	var eip位移 uint32 = 0
	if exception哈斯区错误code(中断) {
		错误 = exception帧值(esp, 0)
		eip位移 = 4
	}
	eip := exception帧值(esp, eip位移)
	cs := exception帧值(esp, eip位移+4)
	eflags := exception帧值(esp, eip位移+8)

	MEmergency日志字符串(" err=")
	MEmergency日志unsignedinteger32(错误)
	MEmergency日志字符串(" eip=")
	MEmergency日志unsignedinteger32(eip)
	MEmergency日志字符串(" cs=")
	MEmergency日志unsignedinteger32(cs)
	MEmergency日志字符串(" eflags=")
	MEmergency日志unsignedinteger32(eflags)
	MEmergency日志字符串(" cr0=")
	MEmergency日志unsignedinteger32(exceptioncr0())
	MEmergency日志字符串(" cr3=")
	MEmergency日志unsignedinteger32(exceptioncr3())

	if 中断 == 0x0E {
		MEmergency日志字符串(" cr2=")
		MEmergency日志unsignedinteger32(exceptioncr2())
		打印页故障信息(错误)
	}

	if (cs & 0x03) != 0 {
		MEmergency日志字符串(" useresp=")
		MEmergency日志unsignedinteger32(exception帧值(esp, eip位移+12))
		MEmergency日志字符串(" ss=")
		MEmergency日志unsignedinteger32(exception帧值(esp, eip位移+16))
	}

	if exception哈斯区错误code(中断) {
		打印exceptionselector信息(错误)
	}
	MEmergency日志字符串("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func halt之后fatalexception()

func H控制器fatal中断帧(已保存esp uint32, 中断 uint32) uint32 {
	H控制器exception(已保存esp+52, 中断)
	halt之后fatalexception()
	return 已保存esp
}

func I中断活跃()
func (self *T中断管理器) A活跃() {
	if A活跃中断管理器 != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	A活跃中断管理器 = address
	I中断活跃()
}
func I中断deactive()
func (self *T中断管理器) Deactive() {
	A活跃中断管理器 = 0
	I中断deactive()
}

func My控制器中断(中断 uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	控制台_2 := T控制台{}
	控制台_2.M打印(buffer)
	return esp
}
func My测试(中断 uint8, esp uint32)

func Unhandle中断() {
	buffer := []byte("unhandle interrupt\n")
	控制台_2 := T控制台{}
	控制台_2.M打印(buffer)
}

func 中断handler_2(中断 uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	控制台_2 := T控制台{}
	控制台_2.M打印(buffer)
	控制台_2.MHexadecimal打印(0x40)
	return esp
}
func 打印esp(esp uint32) {
	控制台_2 := T控制台{}
	控制台_2.MUnsignedinteger32打印xy(esp, 20, 21)
}
func gettls() uint32
func P打印tls() {

}
