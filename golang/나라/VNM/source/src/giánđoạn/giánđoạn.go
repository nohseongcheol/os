/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Giánđoạn

import . "unsafe"
import . "reflect"

import . "cổng"
import . "gdt"
import . "multitasking"
import . "console"

func giánđoạnignore()

func giánđoạnexceptionhandler()
func giánđoạnexceptionhandler0x00()
func giánđoạnexceptionhandler0x01()
func giánđoạnexceptionhandler0x02()
func giánđoạnexceptionhandler0x03()
func giánđoạnexceptionhandler0x04()
func giánđoạnexceptionhandler0x05()
func giánđoạnexceptionhandler0x06()
func giánđoạnexceptionhandler0x07()
func giánđoạnexceptionhandler0x08()
func giánđoạnexceptionhandler0x09()
func giánđoạnexceptionhandler0x0a()
func giánđoạnexceptionhandler0x0b()
func giánđoạnexceptionhandler0x0c()
func giánđoạnexceptionhandler0x0d()
func giánđoạnexceptionhandler0x0e()
func giánđoạnexceptionhandler0x0f()
func giánđoạnexceptionhandler0x10()
func giánđoạnexceptionhandler0x11()
func giánđoạnexceptionhandler0x12()
func giánđoạnexceptionhandler0x13()

func giánđoạnrequesthandler0x00()
func giánđoạnrequesthandler0x01()
func giánđoạnrequesthandler0x02()
func giánđoạnrequesthandler0x03()
func giánđoạnrequesthandler0x04()
func giánđoạnrequesthandler0x05()
func giánđoạnrequesthandler0x06()
func giánđoạnrequesthandler0x07()
func giánđoạnrequesthandler0x08()
func giánđoạnrequesthandler0x09()
func giánđoạnrequesthandler0x0a()
func giánđoạnrequesthandler0x0b()
func giánđoạnrequesthandler0x0c()
func giánđoạnrequesthandler0x0d()
func giánđoạnrequesthandler0x0e()
func giánđoạnrequesthandler0x0f()

func giánđoạnrequesthandler0x80()
func giánđoạnrequesthandler0x81()
func giánđoạnrequesthandler0x82()

func ThửIn(vịtrí uint8, data uint8)
func đặtds(dssegment uint32)
func đặtgs(gssegment uint32)
func giánđoạnThoátVònglặp()

type TGiánđoạnhandler struct {
	GiánđoạnSỐ	uint8
	Giánđoạnmanager	uintptr
}
type IGiánđoạnhandler interface {
	HandleGiánđoạn(uint32) uint32
}

func MớiGiánđoạnhandler(Giánđoạnmanager uintptr, GiánđoạnSỐ uint8) *TGiánđoạnhandler {
	giánđoạnhandler_2 := new(TGiánđoạnhandler)
	giánđoạnhandler_2.GiánđoạnSỐ = GiánđoạnSỐ
	giánđoạnhandler_2.Giánđoạnmanager = Giánđoạnmanager
	return giánđoạnhandler_2

}

var handler_2 [256]uintptr

func (mình *TGiánđoạnhandler) Init(GiánđoạnSỐ uint8, Giánđoạnmanager uintptr, funcaddress uintptr) {

	handler_2[GiánđoạnSỐ] = funcaddress

	mình.GiánđoạnSỐ = GiánđoạnSỐ
	mình.Giánđoạnmanager = Giánđoạnmanager

}
func (mình *TGiánđoạnhandler) ĐặthandleGiánđoạnfuction(GiánđoạnSỐ uint32, address uintptr) {
	handler_2[GiánđoạnSỐ] = address
}
func (mình *TGiánđoạnhandler) Huỷbỏ() {
	mìnhuintptr := uintptr(Pointer(mình))
	Giánđoạnmanager := (*TGiánđoạnmanager)(Pointer(mình.Giánđoạnmanager))
	if mìnhuintptr == Giánđoạnmanager.Gethandler(mình.GiánđoạnSỐ) {
		Giánđoạnmanager.Đặthandler(0, mình.GiánđoạnSỐ)
	}

}
func (mình *TGiánđoạnhandler) ĐặtGiánđoạnmanager(Giánđoạnmanager uintptr) {
}
func (mình *TGiánđoạnhandler) ĐặtGiánđoạnSỐ(GiánđoạnSỐ uint8) {
	mình.GiánđoạnSỐ = GiánđoạnSỐ
}
func (mình *TGiánđoạnhandler) HandleGiánđoạn(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MIn(buffer)
	return esp
}
func HandleGiánđoạn1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MIn(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TGiánđoạndescriptorBảngContrỏ struct {
}

var idtdata [256 * 8]uint8
var HoạtđộngGiánđoạnmanager uintptr = 0

const giánđoạndebug = false

type TGiánđoạnmanager struct {
	handler_2	[256]uintptr

	phầncứngGiánđoạnoffset	uint16

	tácvụmanager	*TTácvụmanager
}

var PrimarypicLệnhioCổng uint16 = 0x20
var PrimarypicdataioCổng uint16 = 0x21
var SecondarypicLệnhioCổng uint16 = 0xA0
var SecondarypicdataioCổng uint16 = 0xA1

func (mình *TGiánđoạnmanager) Init(phầncứngGiánđoạnoffset uint16, toàncụcdescriptorBảng *TShareddescriptorBảng, tácvụmanager *TTácvụmanager) {

	mình.tácvụmanager = tácvụmanager

	mình.phầncứngGiánđoạnoffset = phầncứngGiánđoạnoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtGiánđoạngate uint8 = 0xE
	address = uint32(ValueOf(giánđoạnignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(giánđoạnexceptionhandler0x0f).Pointer())
		mình.GiánđoạndescriptorBảngentryĐặt(i, codesegment, address, 0, IdtGiánđoạngate)
	}

	address = uint32(ValueOf(giánđoạnexceptionhandler0x00).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x00, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x01).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x01, codesegment, address, 0, IdtGiánđoạngate)
	address = uint32(ValueOf(giánđoạnexceptionhandler0x02).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x02, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x03).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x03, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x04).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x04, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x05).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x05, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x06).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x06, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x07).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x07, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x08).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x08, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x09).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x09, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x0a).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x0A, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x0b).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x0B, codesegment, address, 0, IdtGiánđoạngate)
	address = uint32(ValueOf(giánđoạnexceptionhandler0x0c).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x0C, codesegment, address, 0, IdtGiánđoạngate)
	address = uint32(ValueOf(giánđoạnexceptionhandler0x0d).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x0D, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x0e).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x0E, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x0f).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x0F, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x10).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x10, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x11).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x11, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x12).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x12, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnexceptionhandler0x13).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x13, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x00).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x20, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x01).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x21, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x02).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x22, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x03).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x23, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x04).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x24, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x05).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x25, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x06).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x26, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x07).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x27, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x08).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x28, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x09).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x29, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x0a).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x2A, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x0b).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x2B, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x0c).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x2C, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x0d).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x2D, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x0e).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x2E, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x0f).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x2F, codesegment, address, 0, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x80).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x80, codesegment, address, 3, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x81).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x81, codesegment, address, 3, IdtGiánđoạngate)

	address = uint32(ValueOf(giánđoạnrequesthandler0x82).Pointer())
	mình.GiánđoạndescriptorBảngentryĐặt(0x82, codesegment, address, 3, IdtGiánđoạngate)

	CổngGhibyte(PrimarypicLệnhioCổng, 0x11)
	CổngGhibyte(SecondarypicLệnhioCổng, 0x11)

	CổngGhibyte(PrimarypicdataioCổng, 0x20)
	CổngGhibyte(SecondarypicdataioCổng, 0x28)

	CổngGhibyte(PrimarypicdataioCổng, 0x04)
	CổngGhibyte(SecondarypicdataioCổng, 0x02)

	CổngGhibyte(PrimarypicdataioCổng, 0x01)
	CổngGhibyte(SecondarypicdataioCổng, 0x01)

	CổngGhibyte(PrimarypicdataioCổng, 0xF8)
	CổngGhibyte(SecondarypicdataioCổng, 0xEF)

	idtContrỏ := [6]uint8{0, 0, 0, 0, 0, 0}
	cỡ := (*uint16)(Pointer(&idtContrỏ[0]))
	(*cỡ) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtContrỏ[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtContrỏ)))
}
func Lidt(lidtaddr uintptr)

func (mình *TGiánđoạnmanager) GiánđoạndescriptorBảngentryĐặt(giánđoạn int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorKiểu uint8) {

	handleraddressThấpbit := (*uint16)(Pointer(&idtdata[giánđoạn*8+0]))
	(*handleraddressThấpbit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[giánđoạn*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[giánđoạn*8+4]))
	(*reserved) = 0

	var IdtdescriptorCó uint8 = 0x80
	truycập := (*uint8)(Pointer(&idtdata[giánđoạn*8+5]))
	(*truycập) = (IdtdescriptorCó | DescriptorKiểu | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressCaobit := (*uint16)(Pointer(&idtdata[giánđoạn*8+6]))
	(*handleraddressCaobit) = uint16((handler >> 16) & 0xFFFF)

}

func (mình *TGiánđoạnmanager) Đặthandler(handler uintptr, GiánđoạnSỐ uint8) {
	handler_2[GiánđoạnSỐ] = handler
}
func (mình *TGiánđoạnmanager) Gethandler(GiánđoạnSỐ uint8) uintptr {
	return handler_2[GiánđoạnSỐ]
}
func (mình *TGiánđoạnmanager) DohandleGiánđoạn(giánđoạn uint8, esp uint32) uint32 {

	if giánđoạndebug {
		console_2.MInxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32In(uint32(giánđoạn))
		console_2.MIn(":")
		console_2.MUnsignedinteger32In(esp)
	}
	handlerChạy := false
	if handler_2[giánđoạn] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[giánđoạn])))
		esp = myfunction(esp)
		handlerChạy = true

	}

	if !handlerChạy && giánđoạn == uint8(mình.phầncứngGiánđoạnoffset) && mình.tácvụmanager != nil {
		esp = uint32(uintptr(Pointer(mình.tácvụmanager.Schedule((*TcpuTrạngthái)(Pointer(uintptr(esp)))))))

	}
	if !handlerChạy && giánđoạn == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if giánđoạn <= 0x1F {
	}
	if 0x20 <= giánđoạn && giánđoạn < 0x30 {
		if 0x28 <= giánđoạn {
			CổngGhibyte(SecondarypicLệnhioCổng, 0x20)
		}
		CổngGhibyte(PrimarypicLệnhioCổng, 0x20)
	}
	return esp
}

var sốlượng2 uint8 = 1

func đặtcr3(address uint32)

var console_2 TConsole = TConsole{}

func HandleGiánđoạn(esp uint32, giánđoạn uint32) uint32 {

	if giánđoạndebug && giánđoạn != 0x80 && giánđoạn != 0x20 {
		console_2.MInxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32In(uint32(giánđoạn))
		console_2.MIn(":")
		console_2.MUnsignedinteger32In(esp)
	}

	if HoạtđộngGiánđoạnmanager != 0 {
		p := (*TGiánđoạnmanager)(Pointer(HoạtđộngGiánđoạnmanager))
		esp = p.DohandleGiánđoạn(uint8(giánđoạn), esp)
		return esp
	}
	if handler_2[giánđoạn] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[giánđoạn])))
		esp = myfunction(esp)
	}
	if giánđoạn == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= giánđoạn && giánđoạn < 0x30 {
		if 0x28 <= giánđoạn {
			CổngGhibyte(SecondarypicLệnhioCổng, 0x20)
		}
		CổngGhibyte(PrimarypicLệnhioCổng, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuTrạngthái)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(giánđoạnThoátVònglặp).Pointer())
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

func exceptionhasLỗicode(giánđoạn uint32) bool {
	switch giánđoạn {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionTên(giánđoạn uint32) string {
	switch giánđoạn {
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

func exceptionframeGiátrị(frame uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(frame + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func inTrangfaultThôngtin(lỗi uint32) {
	MEmergencylogCHUỖI(" pf=[")
	if (lỗi & 0x01) != 0 {
		MEmergencylogCHUỖI("protection")
	} else {
		MEmergencylogCHUỖI("not-present")
	}
	if (lỗi & 0x02) != 0 {
		MEmergencylogCHUỖI(",write")
	} else {
		MEmergencylogCHUỖI(",read")
	}
	if (lỗi & 0x04) != 0 {
		MEmergencylogCHUỖI(",user")
	} else {
		MEmergencylogCHUỖI(",kernel")
	}
	if (lỗi & 0x08) != 0 {
		MEmergencylogCHUỖI(",reserved-bit")
	}
	if (lỗi & 0x10) != 0 {
		MEmergencylogCHUỖI(",instruction-fetch")
	}
	MEmergencylogCHUỖI("]")
}

func inexceptionselectorThôngtin(lỗi uint32) {
	MEmergencylogCHUỖI(" selector=")
	MEmergencylogunsignedinteger32(lỗi & 0xFFFFFFF8)
	MEmergencylogCHUỖI(" index=")
	MEmergencylogunsignedinteger32(lỗi >> 3)
	MEmergencylogCHUỖI(" table=")
	if (lỗi & 0x02) != 0 {
		MEmergencylogCHUỖI("IDT")
	} else if (lỗi & 0x04) != 0 {
		MEmergencylogCHUỖI("LDT")
	} else {
		MEmergencylogCHUỖI("GDT")
	}
	MEmergencylogCHUỖI(" ext=")
	MEmergencylogunsignedinteger32(lỗi & 0x01)
}

func Handleexception(esp uint32, giánđoạn uint32) uint32 {
	MEmergencylogCHUỖI("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(giánđoạn))
	MEmergencylogCHUỖI(" ")
	MEmergencylogCHUỖI(exceptionTên(giánđoạn))
	MEmergencylogCHUỖI(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogCHUỖI(" invalid-frame")
		if exceptionhasLỗicode(giánđoạn) {
			MEmergencylogCHUỖI(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			inexceptionselectorThôngtin(esp)
		}
		MEmergencylogCHUỖI("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var lỗi uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasLỗicode(giánđoạn) {
		lỗi = exceptionframeGiátrị(esp, 0)
		eipoffset = 4
	}
	eip := exceptionframeGiátrị(esp, eipoffset)
	cs := exceptionframeGiátrị(esp, eipoffset+4)
	eflags := exceptionframeGiátrị(esp, eipoffset+8)

	MEmergencylogCHUỖI(" err=")
	MEmergencylogunsignedinteger32(lỗi)
	MEmergencylogCHUỖI(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogCHUỖI(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogCHUỖI(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogCHUỖI(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogCHUỖI(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if giánđoạn == 0x0E {
		MEmergencylogCHUỖI(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		inTrangfaultThôngtin(lỗi)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogCHUỖI(" useresp=")
		MEmergencylogunsignedinteger32(exceptionframeGiátrị(esp, eipoffset+12))
		MEmergencylogCHUỖI(" ss=")
		MEmergencylogunsignedinteger32(exceptionframeGiátrị(esp, eipoffset+16))
	}

	if exceptionhasLỗicode(giánđoạn) {
		inexceptionselectorThôngtin(lỗi)
	}
	MEmergencylogCHUỖI("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandlefatalGiánđoạnframe(savedesp uint32, giánđoạn uint32) uint32 {
	Handleexception(savedesp+52, giánđoạn)
	haltafterfatalexception()
	return savedesp
}

func GiánđoạnHoạtđộng()
func (mình *TGiánđoạnmanager) Hoạtđộng() {
	if HoạtđộngGiánđoạnmanager != 0 {
		mình.Deactive()
	}
	address := uintptr(Pointer(mình))
	HoạtđộngGiánđoạnmanager = address
	GiánđoạnHoạtđộng()
}
func Giánđoạndeactive()
func (mình *TGiánđoạnmanager) Deactive() {
	HoạtđộngGiánđoạnmanager = 0
	Giánđoạndeactive()
}

func MyhandleGiánđoạn(giánđoạn uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MIn(buffer)
	return esp
}
func MyThử(giánđoạn uint8, esp uint32)

func UnhandleGiánđoạn() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MIn(buffer)
}

func giánđoạnhandler_2(giánđoạn uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MIn(buffer)
	console_2.MHexadecimalIn(0x40)
	return esp
}
func inesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Inxy(esp, 20, 21)
}
func gettls() uint32
func Intls() {

}
