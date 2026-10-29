/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interrupt

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func 인터럽트무시하기()

func 인터럽트예외처리기()
func 인터럽트예외처리기0x00()
func 인터럽트예외처리기0x01()
func 인터럽트예외처리기0x02()
func 인터럽트예외처리기0x03()
func 인터럽트예외처리기0x04()
func 인터럽트예외처리기0x05()
func 인터럽트예외처리기0x06()
func 인터럽트예외처리기0x07()
func 인터럽트예외처리기0x08()
func 인터럽트예외처리기0x09()
func 인터럽트예외처리기0x0A()
func 인터럽트예외처리기0x0B()
func 인터럽트예외처리기0x0C()
func 인터럽트예외처리기0x0D()
func 인터럽트예외처리기0x0E()
func 인터럽트예외처리기0x0F()
func 인터럽트예외처리기0x10()
func 인터럽트예외처리기0x11()
func 인터럽트예외처리기0x12()
func 인터럽트예외처리기0x13()

func 인터럽트요청처리0x00()
func 인터럽트요청처리0x01()
func 인터럽트요청처리0x02()
func 인터럽트요청처리0x03()
func 인터럽트요청처리0x04()
func 인터럽트요청처리0x05()
func 인터럽트요청처리0x06()
func 인터럽트요청처리0x07()
func 인터럽트요청처리0x08()
func 인터럽트요청처리0x09()
func 인터럽트요청처리0x0A()
func 인터럽트요청처리0x0B()
func 인터럽트요청처리0x0C()
func 인터럽트요청처리0x0D()
func 인터럽트요청처리0x0E()
func 인터럽트요청처리0x0F()

func 인터럽트요청처리0x80()
func 인터럽트요청처리0x81()
func 인터럽트요청처리0x82()

func TestPrint(pos uint8, data uint8)
func setDS(ds_segment uint32)
func setGS(gs_segment uint32)
func interruptExitLoop()

type TInterruptHandler struct {
	InterruptNumber		uint8
	InterruptManager	uintptr
}
type IInterruptHandler interface {
	HandleInterrupt(uint32) uint32
}

func NewInterruptHandler(InterruptManager uintptr, InterruptNumber uint8) *TInterruptHandler {
	인터럽트처리기 := new(TInterruptHandler)
	인터럽트처리기.InterruptNumber = InterruptNumber
	인터럽트처리기.InterruptManager = InterruptManager
	return 인터럽트처리기

}

var handlers [256]uintptr

func (self *TInterruptHandler) Vઆરંભ_કરવો(InterruptNumber uint8, InterruptManager uintptr, func_addr uintptr) {

	handlers[InterruptNumber] = func_addr

	self.InterruptNumber = InterruptNumber
	self.InterruptManager = InterruptManager

}
func (self *TInterruptHandler) SetHandleInterruptFuction(InterruptNumber uint32, addr uintptr) {
	handlers[InterruptNumber] = addr
}
func (self *TInterruptHandler) Destroy() {
	self_uintptr := uintptr(Pointer(self))
	InterruptManager := (*TInterruptManager)(Pointer(self.InterruptManager))
	if self_uintptr == InterruptManager.GetHandler(self.InterruptNumber) {
		InterruptManager.SetHandler(0, self.InterruptNumber)
	}

}
func (self *TInterruptHandler) SetInterruptManager(InterruptManager uintptr) {
}
func (self *TInterruptHandler) SetInterruptNumber(InterruptNumber uint8) {
	self.InterruptNumber = InterruptNumber
}
func (self *TInterruptHandler) HandleInterrupt(esp uint32) uint32 {
	buf := []byte("\n\n\n\n\n   TInterruptHandler")
	콘솔 := T콘솔{}
	콘솔.M출력(buf)
	return esp
}
func HandleInterrupt1() {
	buf := []byte("\n\n\n\n   TInterruptHandler")
	콘솔 := T콘솔{}
	콘솔.M출력(buf)
}

type TGateDescriptor struct {
	gateData [8]uint8
}
type TInterruptDescriptorTablePointer struct {
}

var idtData [256 * 8]uint8
var ActiveInterruptManager uintptr = 0

const interruptDebug = false

type TInterruptManager struct {
	handlers	[256]uintptr

	hardwareInterruptOffset	uint16

	taskManager	*T작업관리자
}

var PICMasterCommandPort uint16 = 0x20
var PICMasterDataPort uint16 = 0x21
var PICSlaveCommandPort uint16 = 0xA0
var PICSlaveDataPort uint16 = 0xA1

func (self *TInterruptManager) Vઆરંભ_કરવો(hardwareInterruptOffset uint16, globalDescriptorTable *T공용서술자테이블, taskManager *T작업관리자) {

	self.taskManager = taskManager

	self.hardwareInterruptOffset = hardwareInterruptOffset
	codeSegment := uint16(SEG_KERNEL_CODE)

	for i := 0; i < (256 * 8); i++ {
		idtData[i] = 0
	}
	var addr uint32
	var IDT_INTERRUPT_GATE uint8 = 0xE
	addr = uint32(ValueOf(인터럽트무시하기).Pointer())
	for i := 0; i < 256; i++ {
		handlers[i] = 0
		addr = uint32(ValueOf(인터럽트예외처리기0x0F).Pointer())
		self.SetInterruptDescriptorTableEntry(i, codeSegment, addr, 0, IDT_INTERRUPT_GATE)
	}

	addr = uint32(ValueOf(인터럽트예외처리기0x00).Pointer())
	self.SetInterruptDescriptorTableEntry(0x00, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x01).Pointer())
	self.SetInterruptDescriptorTableEntry(0x01, codeSegment, addr, 0, IDT_INTERRUPT_GATE)
	addr = uint32(ValueOf(인터럽트예외처리기0x02).Pointer())
	self.SetInterruptDescriptorTableEntry(0x02, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x03).Pointer())
	self.SetInterruptDescriptorTableEntry(0x03, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x04).Pointer())
	self.SetInterruptDescriptorTableEntry(0x04, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x05).Pointer())
	self.SetInterruptDescriptorTableEntry(0x05, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x06).Pointer())
	self.SetInterruptDescriptorTableEntry(0x06, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x07).Pointer())
	self.SetInterruptDescriptorTableEntry(0x07, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x08).Pointer())
	self.SetInterruptDescriptorTableEntry(0x08, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x09).Pointer())
	self.SetInterruptDescriptorTableEntry(0x09, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x0A).Pointer())
	self.SetInterruptDescriptorTableEntry(0x0A, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x0B).Pointer())
	self.SetInterruptDescriptorTableEntry(0x0B, codeSegment, addr, 0, IDT_INTERRUPT_GATE)
	addr = uint32(ValueOf(인터럽트예외처리기0x0C).Pointer())
	self.SetInterruptDescriptorTableEntry(0x0C, codeSegment, addr, 0, IDT_INTERRUPT_GATE)
	addr = uint32(ValueOf(인터럽트예외처리기0x0D).Pointer())
	self.SetInterruptDescriptorTableEntry(0x0D, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x0E).Pointer())
	self.SetInterruptDescriptorTableEntry(0x0E, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x0F).Pointer())
	self.SetInterruptDescriptorTableEntry(0x0F, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x10).Pointer())
	self.SetInterruptDescriptorTableEntry(0x10, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x11).Pointer())
	self.SetInterruptDescriptorTableEntry(0x11, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x12).Pointer())
	self.SetInterruptDescriptorTableEntry(0x12, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트예외처리기0x13).Pointer())
	self.SetInterruptDescriptorTableEntry(0x13, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x00).Pointer())
	self.SetInterruptDescriptorTableEntry(0x20, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x01).Pointer())
	self.SetInterruptDescriptorTableEntry(0x21, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x02).Pointer())
	self.SetInterruptDescriptorTableEntry(0x22, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x03).Pointer())
	self.SetInterruptDescriptorTableEntry(0x23, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x04).Pointer())
	self.SetInterruptDescriptorTableEntry(0x24, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x05).Pointer())
	self.SetInterruptDescriptorTableEntry(0x25, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x06).Pointer())
	self.SetInterruptDescriptorTableEntry(0x26, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x07).Pointer())
	self.SetInterruptDescriptorTableEntry(0x27, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x08).Pointer())
	self.SetInterruptDescriptorTableEntry(0x28, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x09).Pointer())
	self.SetInterruptDescriptorTableEntry(0x29, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x0A).Pointer())
	self.SetInterruptDescriptorTableEntry(0x2A, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x0B).Pointer())
	self.SetInterruptDescriptorTableEntry(0x2B, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x0C).Pointer())
	self.SetInterruptDescriptorTableEntry(0x2C, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x0D).Pointer())
	self.SetInterruptDescriptorTableEntry(0x2D, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x0E).Pointer())
	self.SetInterruptDescriptorTableEntry(0x2E, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x0F).Pointer())
	self.SetInterruptDescriptorTableEntry(0x2F, codeSegment, addr, 0, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x80).Pointer())
	self.SetInterruptDescriptorTableEntry(0x80, codeSegment, addr, 3, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x81).Pointer())
	self.SetInterruptDescriptorTableEntry(0x81, codeSegment, addr, 3, IDT_INTERRUPT_GATE)

	addr = uint32(ValueOf(인터럽트요청처리0x82).Pointer())
	self.SetInterruptDescriptorTableEntry(0x82, codeSegment, addr, 3, IDT_INTERRUPT_GATE)

	PortWriteByte(PICMasterCommandPort, 0x11)
	PortWriteByte(PICSlaveCommandPort, 0x11)

	PortWriteByte(PICMasterDataPort, 0x20)
	PortWriteByte(PICSlaveDataPort, 0x28)

	PortWriteByte(PICMasterDataPort, 0x04)
	PortWriteByte(PICSlaveDataPort, 0x02)

	PortWriteByte(PICMasterDataPort, 0x01)
	PortWriteByte(PICSlaveDataPort, 0x01)

	PortWriteByte(PICMasterDataPort, 0xF8)
	PortWriteByte(PICSlaveDataPort, 0xEF)

	idtPointer := [6]uint8{0, 0, 0, 0, 0, 0}
	કદ := (*uint16)(Pointer(&idtPointer[0]))
	(*કદ) = (uint16)(Sizeof(idtData) - 1)

	base := (*uint32)(Pointer(&idtPointer[2]))
	(*base) = uint32(uintptr(Pointer(&idtData)))

	LIDT(uintptr(Pointer(&idtPointer)))
}
func LIDT(lidtaddr uintptr)

func (self *TInterruptManager) SetInterruptDescriptorTableEntry(interrupt int,
	codeSegment uint16,
	handler uint32,
	DescriptorPrivilegeLevel uint8,
	DescriptorType uint8) {

	handlerAddressLowBits := (*uint16)(Pointer(&idtData[interrupt*8+0]))
	(*handlerAddressLowBits) = uint16(handler & 0xFFFF)

	gdt_codeSegmentSelector := (*uint16)(Pointer(&idtData[interrupt*8+2]))
	(*gdt_codeSegmentSelector) = codeSegment

	reserved := (*uint8)(Pointer(&idtData[interrupt*8+4]))
	(*reserved) = 0

	var IDT_DESC_PRESENT uint8 = 0x80
	access := (*uint8)(Pointer(&idtData[interrupt*8+5]))
	(*access) = (IDT_DESC_PRESENT | DescriptorType | ((DescriptorPrivilegeLevel & 3) << 5))

	handlerAddressHighBits := (*uint16)(Pointer(&idtData[interrupt*8+6]))
	(*handlerAddressHighBits) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TInterruptManager) SetHandler(handler uintptr, InterruptNumber uint8) {
	handlers[InterruptNumber] = handler
}
func (self *TInterruptManager) GetHandler(InterruptNumber uint8) uintptr {
	return handlers[InterruptNumber]
}
func (self *TInterruptManager) DoHandleInterrupt(interrupt uint8, esp uint32) uint32 {

	if interruptDebug {
		콘솔.M출력XY("[esp:", 1, 20)
		콘솔.MUint32출력(uint32(interrupt))
		콘솔.M출력(":")
		콘솔.MUint32출력(esp)
	}
	handlerRun := false
	if handlers[interrupt] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handlers[interrupt])))
		esp = myfunction(esp)
		handlerRun = true

	}

	if !handlerRun && interrupt == uint8(self.hardwareInterruptOffset) && self.taskManager != nil {
		esp = uint32(uintptr(Pointer(self.taskManager.Schedule((*TCPUState)(Pointer(uintptr(esp)))))))

	}
	if !handlerRun && interrupt == 0x80 {
		esp = handleUnhandledSyscall(esp)
	}

	if interrupt <= 0x1F {
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortWriteByte(PICSlaveCommandPort, 0x20)
		}
		PortWriteByte(PICMasterCommandPort, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func setCR3(addr uint32)

var 콘솔 T콘솔 = T콘솔{}

func HandleInterrupt(esp uint32, interrupt uint32) uint32 {

	if interruptDebug && interrupt != 0x80 && interrupt != 0x20 {
		콘솔.M출력XY("[esp:", 1, 21)
		콘솔.MUint32출력(uint32(interrupt))
		콘솔.M출력(":")
		콘솔.MUint32출력(esp)
	}

	if ActiveInterruptManager != 0 {
		p := (*TInterruptManager)(Pointer(ActiveInterruptManager))
		esp = p.DoHandleInterrupt(uint8(interrupt), esp)
		return esp
	}
	if handlers[interrupt] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handlers[interrupt])))
		esp = myfunction(esp)
	}
	if interrupt == 0x80 {
		return handleUnhandledSyscall(esp)
	}
	if 0x20 <= interrupt && interrupt < 0x30 {
		if 0x28 <= interrupt {
			PortWriteByte(PICSlaveCommandPort, 0x20)
		}
		PortWriteByte(PICMasterCommandPort, 0x20)
	}

	return esp
}

func handleUnhandledSyscall(esp uint32) uint32 {
	cpu := (*TCPUState)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interruptExitLoop).Pointer())
		cpu.Cs = SEG_KERNEL_CODE
		cpu.Ds = SEG_KERNEL_DATA
		cpu.Es = SEG_KERNEL_DATA
		cpu.Fs = SEG_KERNEL_DATA
		cpu.Gs = SEG_KERNEL_GS
		cpu.Ss = SEG_KERNEL_DATA
		cpu.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionHasErrorCode(interrupt uint32) bool {
	switch interrupt {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionName(interrupt uint32) string {
	switch interrupt {
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

func exceptionFrameValue(frame uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(frame + offset)))
}

func exceptionCR0() uint32
func exceptionCR2() uint32
func exceptionCR3() uint32

func printPageFaultInfo(err uint32) {
	M긴급로그문자열(" pf=[")
	if (err & 0x01) != 0 {
		M긴급로그문자열("protection")
	} else {
		M긴급로그문자열("not-present")
	}
	if (err & 0x02) != 0 {
		M긴급로그문자열(",write")
	} else {
		M긴급로그문자열(",read")
	}
	if (err & 0x04) != 0 {
		M긴급로그문자열(",user")
	} else {
		M긴급로그문자열(",kernel")
	}
	if (err & 0x08) != 0 {
		M긴급로그문자열(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		M긴급로그문자열(",instruction-fetch")
	}
	M긴급로그문자열("]")
}

func printExceptionSelectorInfo(err uint32) {
	M긴급로그문자열(" selector=")
	M긴급로그Uint32(err & 0xFFFFFFF8)
	M긴급로그문자열(" index=")
	M긴급로그Uint32(err >> 3)
	M긴급로그문자열(" table=")
	if (err & 0x02) != 0 {
		M긴급로그문자열("IDT")
	} else if (err & 0x04) != 0 {
		M긴급로그문자열("LDT")
	} else {
		M긴급로그문자열("GDT")
	}
	M긴급로그문자열(" ext=")
	M긴급로그Uint32(err & 0x01)
}

func HandleException(esp uint32, interrupt uint32) uint32 {
	M긴급로그문자열("\nEXCEPTION vec=")
	M긴급로그Hex8(uint8(interrupt))
	M긴급로그문자열(" ")
	M긴급로그문자열(exceptionName(interrupt))
	M긴급로그문자열(" frame=")
	M긴급로그Uint32(esp)

	if esp < 0x1000 {
		M긴급로그문자열(" invalid-frame")
		if exceptionHasErrorCode(interrupt) {
			M긴급로그문자열(" raw-error-or-bad-esp=")
			M긴급로그Uint32(esp)
			printExceptionSelectorInfo(esp)
		}
		M긴급로그문자열("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipOffset uint32 = 0
	if exceptionHasErrorCode(interrupt) {
		err = exceptionFrameValue(esp, 0)
		eipOffset = 4
	}
	eip := exceptionFrameValue(esp, eipOffset)
	cs := exceptionFrameValue(esp, eipOffset+4)
	eflags := exceptionFrameValue(esp, eipOffset+8)

	M긴급로그문자열(" err=")
	M긴급로그Uint32(err)
	M긴급로그문자열(" eip=")
	M긴급로그Uint32(eip)
	M긴급로그문자열(" cs=")
	M긴급로그Uint32(cs)
	M긴급로그문자열(" eflags=")
	M긴급로그Uint32(eflags)
	M긴급로그문자열(" cr0=")
	M긴급로그Uint32(exceptionCR0())
	M긴급로그문자열(" cr3=")
	M긴급로그Uint32(exceptionCR3())

	if interrupt == 0x0E {
		M긴급로그문자열(" cr2=")
		M긴급로그Uint32(exceptionCR2())
		printPageFaultInfo(err)
	}

	if (cs & 0x03) != 0 {
		M긴급로그문자열(" useresp=")
		M긴급로그Uint32(exceptionFrameValue(esp, eipOffset+12))
		M긴급로그문자열(" ss=")
		M긴급로그Uint32(exceptionFrameValue(esp, eipOffset+16))
	}

	if exceptionHasErrorCode(interrupt) {
		printExceptionSelectorInfo(err)
	}
	M긴급로그문자열("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltAfterFatalException()

func HandleFatalInterruptFrame(savedESP uint32, interrupt uint32) uint32 {
	HandleException(savedESP+52, interrupt)
	haltAfterFatalException()
	return savedESP
}

func InterruptActive()
func (self *TInterruptManager) Active() {
	if ActiveInterruptManager != 0 {
		self.Deactive()
	}
	addr := uintptr(Pointer(self))
	ActiveInterruptManager = addr
	InterruptActive()
}
func InterruptDeactive()
func (self *TInterruptManager) Deactive() {
	ActiveInterruptManager = 0
	InterruptDeactive()
}

func MyHandleInterrupt(interrupt uint8, esp uint32) uint32 {
	buf := []byte("interrupt")
	콘솔 := T콘솔{}
	콘솔.M출력(buf)
	return esp
}
func MyTest(interrupt uint8, esp uint32)

func UnhandleInterrupt() {
	buf := []byte("unhandle interrupt\n")
	콘솔 := T콘솔{}
	콘솔.M출력(buf)
}

func 인터럽트처리기(interrupt uint8, esp uint32) uint32 {
	buf := []byte("interrupt\nhandler\nhi")
	콘솔 := T콘솔{}
	콘솔.M출력(buf)
	콘솔.MHex출력(0x40)
	return esp
}
func printESP(esp uint32) {
	콘솔 := T콘솔{}
	콘솔.MUint32출력XY(esp, 20, 21)
}
func getTLS() uint32
func PrintTLS() {

}
