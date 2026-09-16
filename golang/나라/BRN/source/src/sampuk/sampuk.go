/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Sampuk

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func sampukignore()

func sampukexceptionhandler()
func sampukexceptionhandler0x00()
func sampukexceptionhandler0x01()
func sampukexceptionhandler0x02()
func sampukexceptionhandler0x03()
func sampukexceptionhandler0x04()
func sampukexceptionhandler0x05()
func sampukexceptionhandler0x06()
func sampukexceptionhandler0x07()
func sampukexceptionhandler0x08()
func sampukexceptionhandler0x09()
func sampukexceptionhandler0x0a()
func sampukexceptionhandler0x0b()
func sampukexceptionhandler0x0c()
func sampukexceptionhandler0x0d()
func sampukexceptionhandler0x0e()
func sampukexceptionhandler0x0f()
func sampukexceptionhandler0x10()
func sampukexceptionhandler0x11()
func sampukexceptionhandler0x12()
func sampukexceptionhandler0x13()

func sampukrequesthandler0x00()
func sampukrequesthandler0x01()
func sampukrequesthandler0x02()
func sampukrequesthandler0x03()
func sampukrequesthandler0x04()
func sampukrequesthandler0x05()
func sampukrequesthandler0x06()
func sampukrequesthandler0x07()
func sampukrequesthandler0x08()
func sampukrequesthandler0x09()
func sampukrequesthandler0x0a()
func sampukrequesthandler0x0b()
func sampukrequesthandler0x0c()
func sampukrequesthandler0x0d()
func sampukrequesthandler0x0e()
func sampukrequesthandler0x0f()

func sampukrequesthandler0x80()
func sampukrequesthandler0x81()
func sampukrequesthandler0x82()

func UjiCetak(kedudukan uint8, data uint8)
func tetapkands(dssegment uint32)
func tetapkangs(gssegment uint32)
func sampukKeluarloop()

type TSampukhandler struct {
	SampukNOMBOR	uint8
	Sampukmanager	uintptr
}
type ISampukhandler interface {
	KendaliSampuk(uint32) uint32
}

func BaharuSampukhandler(Sampukmanager uintptr, SampukNOMBOR uint8) *TSampukhandler {
	sampukhandler_2 := new(TSampukhandler)
	sampukhandler_2.SampukNOMBOR = SampukNOMBOR
	sampukhandler_2.Sampukmanager = Sampukmanager
	return sampukhandler_2

}

var handler_2 [256]uintptr

func (diri *TSampukhandler) Init(SampukNOMBOR uint8, Sampukmanager uintptr, funcaddress uintptr) {

	handler_2[SampukNOMBOR] = funcaddress

	diri.SampukNOMBOR = SampukNOMBOR
	diri.Sampukmanager = Sampukmanager

}
func (diri *TSampukhandler) TetapkanKendaliSampukfuction(SampukNOMBOR uint32, address uintptr) {
	handler_2[SampukNOMBOR] = address
}
func (diri *TSampukhandler) Musnah() {
	diriuintptr := uintptr(Pointer(diri))
	Sampukmanager := (*TSampukmanager)(Pointer(diri.Sampukmanager))
	if diriuintptr == Sampukmanager.Gethandler(diri.SampukNOMBOR) {
		Sampukmanager.Tetapkanhandler(0, diri.SampukNOMBOR)
	}

}
func (diri *TSampukhandler) TetapkanSampukmanager(Sampukmanager uintptr) {
}
func (diri *TSampukhandler) TetapkanSampukNOMBOR(SampukNOMBOR uint8) {
	diri.SampukNOMBOR = SampukNOMBOR
}
func (diri *TSampukhandler) KendaliSampuk(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
	return esp
}
func KendaliSampuk1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TSampukdescriptorJadualPenuding struct {
}

var idtdata [256 * 8]uint8
var AktifSampukmanager uintptr = 0

const sampukNyahpepijat = false

type TSampukmanager struct {
	handler_2	[256]uintptr

	perkakasanSampukoffset	uint16

	tugasmanager	*TTugasmanager
}

var PrimarypicPerintahioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicPerintahioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (diri *TSampukmanager) Init(perkakasanSampukoffset uint16, sejagatdescriptorJadual *TShareddescriptorJadual, tugasmanager *TTugasmanager) {

	diri.tugasmanager = tugasmanager

	diri.perkakasanSampukoffset = perkakasanSampukoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtSampukgate uint8 = 0xE
	address = uint32(ValueOf(sampukignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(sampukexceptionhandler0x0f).Pointer())
		diri.SampukdescriptorJadualentryTetapkan(i, codesegment, address, 0, IdtSampukgate)
	}

	address = uint32(ValueOf(sampukexceptionhandler0x00).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x00, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x01).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x01, codesegment, address, 0, IdtSampukgate)
	address = uint32(ValueOf(sampukexceptionhandler0x02).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x02, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x03).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x03, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x04).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x04, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x05).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x05, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x06).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x06, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x07).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x07, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x08).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x08, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x09).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x09, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x0a).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x0A, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x0b).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x0B, codesegment, address, 0, IdtSampukgate)
	address = uint32(ValueOf(sampukexceptionhandler0x0c).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x0C, codesegment, address, 0, IdtSampukgate)
	address = uint32(ValueOf(sampukexceptionhandler0x0d).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x0D, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x0e).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x0E, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x0f).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x0F, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x10).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x10, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x11).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x11, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x12).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x12, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukexceptionhandler0x13).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x13, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x00).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x20, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x01).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x21, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x02).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x22, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x03).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x23, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x04).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x24, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x05).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x25, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x06).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x26, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x07).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x27, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x08).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x28, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x09).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x29, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x0a).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x2A, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x0b).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x2B, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x0c).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x2C, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x0d).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x2D, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x0e).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x2E, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x0f).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x2F, codesegment, address, 0, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x80).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x80, codesegment, address, 3, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x81).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x81, codesegment, address, 3, IdtSampukgate)

	address = uint32(ValueOf(sampukrequesthandler0x82).Pointer())
	diri.SampukdescriptorJadualentryTetapkan(0x82, codesegment, address, 3, IdtSampukgate)

	PortTulisbyte(PrimarypicPerintahioport, 0x11)
	PortTulisbyte(SecondarypicPerintahioport, 0x11)

	PortTulisbyte(Primarypicdataioport, 0x20)
	PortTulisbyte(Secondarypicdataioport, 0x28)

	PortTulisbyte(Primarypicdataioport, 0x04)
	PortTulisbyte(Secondarypicdataioport, 0x02)

	PortTulisbyte(Primarypicdataioport, 0x01)
	PortTulisbyte(Secondarypicdataioport, 0x01)

	PortTulisbyte(Primarypicdataioport, 0xF8)
	PortTulisbyte(Secondarypicdataioport, 0xEF)

	idtPenuding := [6]uint8{0, 0, 0, 0, 0, 0}
	saiz := (*uint16)(Pointer(&idtPenuding[0]))
	(*saiz) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtPenuding[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtPenuding)))
}
func Lidt(lidtaddr uintptr)

func (diri *TSampukmanager) SampukdescriptorJadualentryTetapkan(sampuk int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorJenis uint8) {

	handleraddressRendahbit := (*uint16)(Pointer(&idtdata[sampuk*8+0]))
	(*handleraddressRendahbit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[sampuk*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[sampuk*8+4]))
	(*reserved) = 0

	var IdtdescriptorHadir uint8 = 0x80
	capai := (*uint8)(Pointer(&idtdata[sampuk*8+5]))
	(*capai) = (IdtdescriptorHadir | DescriptorJenis | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressTinggibit := (*uint16)(Pointer(&idtdata[sampuk*8+6]))
	(*handleraddressTinggibit) = uint16((handler >> 16) & 0xFFFF)

}

func (diri *TSampukmanager) Tetapkanhandler(handler uintptr, SampukNOMBOR uint8) {
	handler_2[SampukNOMBOR] = handler
}
func (diri *TSampukmanager) Gethandler(SampukNOMBOR uint8) uintptr {
	return handler_2[SampukNOMBOR]
}
func (diri *TSampukmanager) DoKendaliSampuk(sampuk uint8, esp uint32) uint32 {

	if sampukNyahpepijat {
		console_2.MCetakxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Cetak(uint32(sampuk))
		console_2.MCetak(":")
		console_2.MUnsignedinteger32Cetak(esp)
	}
	handlerLaksana := false
	if handler_2[sampuk] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[sampuk])))
		esp = myfunction(esp)
		handlerLaksana = true

	}

	if !handlerLaksana && sampuk == uint8(diri.perkakasanSampukoffset) && diri.tugasmanager != nil {
		esp = uint32(uintptr(Pointer(diri.tugasmanager.Schedule((*TcpuKeadaan)(Pointer(uintptr(esp)))))))

	}
	if !handlerLaksana && sampuk == 0x80 {
		esp = kendaliunhandledsyscall(esp)
	}

	if sampuk <= 0x1F {
	}
	if 0x20 <= sampuk && sampuk < 0x30 {
		if 0x28 <= sampuk {
			PortTulisbyte(SecondarypicPerintahioport, 0x20)
		}
		PortTulisbyte(PrimarypicPerintahioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func tetapkancr3(address uint32)

var console_2 TConsole = TConsole{}

func KendaliSampuk(esp uint32, sampuk uint32) uint32 {

	if sampukNyahpepijat && sampuk != 0x80 && sampuk != 0x20 {
		console_2.MCetakxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Cetak(uint32(sampuk))
		console_2.MCetak(":")
		console_2.MUnsignedinteger32Cetak(esp)
	}

	if AktifSampukmanager != 0 {
		p := (*TSampukmanager)(Pointer(AktifSampukmanager))
		esp = p.DoKendaliSampuk(uint8(sampuk), esp)
		return esp
	}
	if handler_2[sampuk] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[sampuk])))
		esp = myfunction(esp)
	}
	if sampuk == 0x80 {
		return kendaliunhandledsyscall(esp)
	}
	if 0x20 <= sampuk && sampuk < 0x30 {
		if 0x28 <= sampuk {
			PortTulisbyte(SecondarypicPerintahioport, 0x20)
		}
		PortTulisbyte(PrimarypicPerintahioport, 0x20)
	}

	return esp
}

func kendaliunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuKeadaan)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(sampukKeluarloop).Pointer())
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

func exceptionhasRalatcode(sampuk uint32) bool {
	switch sampuk {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNama(sampuk uint32) string {
	switch sampuk {
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

func exceptionBingkaiNilai(bingkai uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(bingkai + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func cetakHalamanfaultMaklumat(err uint32) {
	MEmergencylogRentetan(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogRentetan("protection")
	} else {
		MEmergencylogRentetan("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogRentetan(",write")
	} else {
		MEmergencylogRentetan(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogRentetan(",user")
	} else {
		MEmergencylogRentetan(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogRentetan(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogRentetan(",instruction-fetch")
	}
	MEmergencylogRentetan("]")
}

func cetakexceptionselectorMaklumat(err uint32) {
	MEmergencylogRentetan(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogRentetan(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogRentetan(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogRentetan("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogRentetan("LDT")
	} else {
		MEmergencylogRentetan("GDT")
	}
	MEmergencylogRentetan(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Kendaliexception(esp uint32, sampuk uint32) uint32 {
	MEmergencylogRentetan("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(sampuk))
	MEmergencylogRentetan(" ")
	MEmergencylogRentetan(exceptionNama(sampuk))
	MEmergencylogRentetan(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogRentetan(" invalid-frame")
		if exceptionhasRalatcode(sampuk) {
			MEmergencylogRentetan(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			cetakexceptionselectorMaklumat(esp)
		}
		MEmergencylogRentetan("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasRalatcode(sampuk) {
		err = exceptionBingkaiNilai(esp, 0)
		eipoffset = 4
	}
	eip := exceptionBingkaiNilai(esp, eipoffset)
	cs := exceptionBingkaiNilai(esp, eipoffset+4)
	eflags := exceptionBingkaiNilai(esp, eipoffset+8)

	MEmergencylogRentetan(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogRentetan(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogRentetan(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogRentetan(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogRentetan(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogRentetan(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if sampuk == 0x0E {
		MEmergencylogRentetan(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		cetakHalamanfaultMaklumat(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogRentetan(" useresp=")
		MEmergencylogunsignedinteger32(exceptionBingkaiNilai(esp, eipoffset+12))
		MEmergencylogRentetan(" ss=")
		MEmergencylogunsignedinteger32(exceptionBingkaiNilai(esp, eipoffset+16))
	}

	if exceptionhasRalatcode(sampuk) {
		cetakexceptionselectorMaklumat(err)
	}
	MEmergencylogRentetan("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltSelepasfatalexception()

func KendalifatalSampukBingkai(savedesp uint32, sampuk uint32) uint32 {
	Kendaliexception(savedesp+52, sampuk)
	haltSelepasfatalexception()
	return savedesp
}

func SampukAktif()
func (diri *TSampukmanager) Aktif() {
	if AktifSampukmanager != 0 {
		diri.Deactive()
	}
	address := uintptr(Pointer(diri))
	AktifSampukmanager = address
	SampukAktif()
}
func Sampukdeactive()
func (diri *TSampukmanager) Deactive() {
	AktifSampukmanager = 0
	Sampukdeactive()
}

func MyKendaliSampuk(sampuk uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
	return esp
}
func MyUji(sampuk uint8, esp uint32)

func UnhandleSampuk() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
}

func sampukhandler_2(sampuk uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
	console_2.MHexadecimalCetak(0x40)
	return esp
}
func cetakesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Cetakxy(esp, 20, 21)
}
func gettls() uint32
func Cetaktls() {

}
