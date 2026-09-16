/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interupsi

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func interupsiignore()

func interupsiexceptionhandler()
func interupsiexceptionhandler0x00()
func interupsiexceptionhandler0x01()
func interupsiexceptionhandler0x02()
func interupsiexceptionhandler0x03()
func interupsiexceptionhandler0x04()
func interupsiexceptionhandler0x05()
func interupsiexceptionhandler0x06()
func interupsiexceptionhandler0x07()
func interupsiexceptionhandler0x08()
func interupsiexceptionhandler0x09()
func interupsiexceptionhandler0x0a()
func interupsiexceptionhandler0x0b()
func interupsiexceptionhandler0x0c()
func interupsiexceptionhandler0x0d()
func interupsiexceptionhandler0x0e()
func interupsiexceptionhandler0x0f()
func interupsiexceptionhandler0x10()
func interupsiexceptionhandler0x11()
func interupsiexceptionhandler0x12()
func interupsiexceptionhandler0x13()

func interupsirequesthandler0x00()
func interupsirequesthandler0x01()
func interupsirequesthandler0x02()
func interupsirequesthandler0x03()
func interupsirequesthandler0x04()
func interupsirequesthandler0x05()
func interupsirequesthandler0x06()
func interupsirequesthandler0x07()
func interupsirequesthandler0x08()
func interupsirequesthandler0x09()
func interupsirequesthandler0x0a()
func interupsirequesthandler0x0b()
func interupsirequesthandler0x0c()
func interupsirequesthandler0x0d()
func interupsirequesthandler0x0e()
func interupsirequesthandler0x0f()

func interupsirequesthandler0x80()
func interupsirequesthandler0x81()
func interupsirequesthandler0x82()

func TesCetak(posisi uint8, data uint8)
func aturds(dssegment uint32)
func aturgs(gssegment uint32)
func interupsiKeluarloop()

type TInterupsihandler struct {
	InterupsiNomor		uint8
	Interupsimanager	uintptr
}
type IInterupsihandler interface {
	PenangananInterupsi(uint32) uint32
}

func BaruInterupsihandler(Interupsimanager uintptr, InterupsiNomor uint8) *TInterupsihandler {
	interupsihandler_2 := new(TInterupsihandler)
	interupsihandler_2.InterupsiNomor = InterupsiNomor
	interupsihandler_2.Interupsimanager = Interupsimanager
	return interupsihandler_2

}

var handler_2 [256]uintptr

func (dirisendiri *TInterupsihandler) Init(InterupsiNomor uint8, Interupsimanager uintptr, funcaddress uintptr) {

	handler_2[InterupsiNomor] = funcaddress

	dirisendiri.InterupsiNomor = InterupsiNomor
	dirisendiri.Interupsimanager = Interupsimanager

}
func (dirisendiri *TInterupsihandler) AturPenangananInterupsifuction(InterupsiNomor uint32, address uintptr) {
	handler_2[InterupsiNomor] = address
}
func (dirisendiri *TInterupsihandler) Lenyapkan() {
	dirisendiriuintptr := uintptr(Pointer(dirisendiri))
	Interupsimanager := (*TInterupsimanager)(Pointer(dirisendiri.Interupsimanager))
	if dirisendiriuintptr == Interupsimanager.Gethandler(dirisendiri.InterupsiNomor) {
		Interupsimanager.Aturhandler(0, dirisendiri.InterupsiNomor)
	}

}
func (dirisendiri *TInterupsihandler) AturInterupsimanager(Interupsimanager uintptr) {
}
func (dirisendiri *TInterupsihandler) AturInterupsiNomor(InterupsiNomor uint8) {
	dirisendiri.InterupsiNomor = InterupsiNomor
}
func (dirisendiri *TInterupsihandler) PenangananInterupsi(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
	return esp
}
func PenangananInterupsi1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TInterupsidescriptorTabelPenunjuk struct {
}

var idtdata [256 * 8]uint8
var AktifInterupsimanager uintptr = 0

const interupsidebug = false

type TInterupsimanager struct {
	handler_2	[256]uintptr

	perangkatkerasInterupsioffset	uint16

	tugasmanager	*TTugasmanager
}

var PrimarypicPerintahioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicPerintahioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (dirisendiri *TInterupsimanager) Init(perangkatkerasInterupsioffset uint16, globaldescriptorTabel *TShareddescriptorTabel, tugasmanager *TTugasmanager) {

	dirisendiri.tugasmanager = tugasmanager

	dirisendiri.perangkatkerasInterupsioffset = perangkatkerasInterupsioffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtInterupsigate uint8 = 0xE
	address = uint32(ValueOf(interupsiignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(interupsiexceptionhandler0x0f).Pointer())
		dirisendiri.InterupsidescriptorTabelentriAtur(i, codesegment, address, 0, IdtInterupsigate)
	}

	address = uint32(ValueOf(interupsiexceptionhandler0x00).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x00, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x01).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x01, codesegment, address, 0, IdtInterupsigate)
	address = uint32(ValueOf(interupsiexceptionhandler0x02).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x02, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x03).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x03, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x04).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x04, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x05).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x05, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x06).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x06, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x07).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x07, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x08).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x08, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x09).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x09, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x0a).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x0A, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x0b).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x0B, codesegment, address, 0, IdtInterupsigate)
	address = uint32(ValueOf(interupsiexceptionhandler0x0c).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x0C, codesegment, address, 0, IdtInterupsigate)
	address = uint32(ValueOf(interupsiexceptionhandler0x0d).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x0D, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x0e).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x0E, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x0f).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x0F, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x10).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x10, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x11).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x11, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x12).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x12, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsiexceptionhandler0x13).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x13, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x00).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x20, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x01).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x21, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x02).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x22, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x03).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x23, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x04).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x24, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x05).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x25, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x06).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x26, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x07).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x27, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x08).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x28, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x09).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x29, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x0a).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x2A, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x0b).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x2B, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x0c).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x2C, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x0d).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x2D, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x0e).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x2E, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x0f).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x2F, codesegment, address, 0, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x80).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x80, codesegment, address, 3, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x81).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x81, codesegment, address, 3, IdtInterupsigate)

	address = uint32(ValueOf(interupsirequesthandler0x82).Pointer())
	dirisendiri.InterupsidescriptorTabelentriAtur(0x82, codesegment, address, 3, IdtInterupsigate)

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

	idtPenunjuk := [6]uint8{0, 0, 0, 0, 0, 0}
	ukuran := (*uint16)(Pointer(&idtPenunjuk[0]))
	(*ukuran) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtPenunjuk[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtPenunjuk)))
}
func Lidt(lidtaddr uintptr)

func (dirisendiri *TInterupsimanager) InterupsidescriptorTabelentriAtur(interupsi int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTipe uint8) {

	handleraddressRendahbit := (*uint16)(Pointer(&idtdata[interupsi*8+0]))
	(*handleraddressRendahbit) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[interupsi*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[interupsi*8+4]))
	(*reserved) = 0

	var IdtdescriptorAda uint8 = 0x80
	akses := (*uint8)(Pointer(&idtdata[interupsi*8+5]))
	(*akses) = (IdtdescriptorAda | DescriptorTipe | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressTinggibit := (*uint16)(Pointer(&idtdata[interupsi*8+6]))
	(*handleraddressTinggibit) = uint16((handler >> 16) & 0xFFFF)

}

func (dirisendiri *TInterupsimanager) Aturhandler(handler uintptr, InterupsiNomor uint8) {
	handler_2[InterupsiNomor] = handler
}
func (dirisendiri *TInterupsimanager) Gethandler(InterupsiNomor uint8) uintptr {
	return handler_2[InterupsiNomor]
}
func (dirisendiri *TInterupsimanager) DoPenangananInterupsi(interupsi uint8, esp uint32) uint32 {

	if interupsidebug {
		console_2.MCetakxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Cetak(uint32(interupsi))
		console_2.MCetak(":")
		console_2.MUnsignedinteger32Cetak(esp)
	}
	handlerJalankan := false
	if handler_2[interupsi] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interupsi])))
		esp = myfunction(esp)
		handlerJalankan = true

	}

	if !handlerJalankan && interupsi == uint8(dirisendiri.perangkatkerasInterupsioffset) && dirisendiri.tugasmanager != nil {
		esp = uint32(uintptr(Pointer(dirisendiri.tugasmanager.Schedule((*TcpuStatus)(Pointer(uintptr(esp)))))))

	}
	if !handlerJalankan && interupsi == 0x80 {
		esp = penangananunhandledsyscall(esp)
	}

	if interupsi <= 0x1F {
	}
	if 0x20 <= interupsi && interupsi < 0x30 {
		if 0x28 <= interupsi {
			PortTulisbyte(SecondarypicPerintahioport, 0x20)
		}
		PortTulisbyte(PrimarypicPerintahioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func aturcr3(address uint32)

var console_2 TConsole = TConsole{}

func PenangananInterupsi(esp uint32, interupsi uint32) uint32 {

	if interupsidebug && interupsi != 0x80 && interupsi != 0x20 {
		console_2.MCetakxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Cetak(uint32(interupsi))
		console_2.MCetak(":")
		console_2.MUnsignedinteger32Cetak(esp)
	}

	if AktifInterupsimanager != 0 {
		p := (*TInterupsimanager)(Pointer(AktifInterupsimanager))
		esp = p.DoPenangananInterupsi(uint8(interupsi), esp)
		return esp
	}
	if handler_2[interupsi] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interupsi])))
		esp = myfunction(esp)
	}
	if interupsi == 0x80 {
		return penangananunhandledsyscall(esp)
	}
	if 0x20 <= interupsi && interupsi < 0x30 {
		if 0x28 <= interupsi {
			PortTulisbyte(SecondarypicPerintahioport, 0x20)
		}
		PortTulisbyte(PrimarypicPerintahioport, 0x20)
	}

	return esp
}

func penangananunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStatus)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(interupsiKeluarloop).Pointer())
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

func exceptionhasGalatcode(interupsi uint32) bool {
	switch interupsi {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNama(interupsi uint32) string {
	switch interupsi {
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

func cetakHalamanfaultinfo(galat uint32) {
	MEmergencylogBenang(" pf=[")
	if (galat & 0x01) != 0 {
		MEmergencylogBenang("protection")
	} else {
		MEmergencylogBenang("not-present")
	}
	if (galat & 0x02) != 0 {
		MEmergencylogBenang(",write")
	} else {
		MEmergencylogBenang(",read")
	}
	if (galat & 0x04) != 0 {
		MEmergencylogBenang(",user")
	} else {
		MEmergencylogBenang(",kernel")
	}
	if (galat & 0x08) != 0 {
		MEmergencylogBenang(",reserved-bit")
	}
	if (galat & 0x10) != 0 {
		MEmergencylogBenang(",instruction-fetch")
	}
	MEmergencylogBenang("]")
}

func cetakexceptionselectorinfo(galat uint32) {
	MEmergencylogBenang(" selector=")
	MEmergencylogunsignedinteger32(galat & 0xFFFFFFF8)
	MEmergencylogBenang(" index=")
	MEmergencylogunsignedinteger32(galat >> 3)
	MEmergencylogBenang(" table=")
	if (galat & 0x02) != 0 {
		MEmergencylogBenang("IDT")
	} else if (galat & 0x04) != 0 {
		MEmergencylogBenang("LDT")
	} else {
		MEmergencylogBenang("GDT")
	}
	MEmergencylogBenang(" ext=")
	MEmergencylogunsignedinteger32(galat & 0x01)
}

func Penangananexception(esp uint32, interupsi uint32) uint32 {
	MEmergencylogBenang("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(interupsi))
	MEmergencylogBenang(" ")
	MEmergencylogBenang(exceptionNama(interupsi))
	MEmergencylogBenang(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogBenang(" invalid-frame")
		if exceptionhasGalatcode(interupsi) {
			MEmergencylogBenang(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			cetakexceptionselectorinfo(esp)
		}
		MEmergencylogBenang("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var galat uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasGalatcode(interupsi) {
		galat = exceptionBingkaiNilai(esp, 0)
		eipoffset = 4
	}
	eip := exceptionBingkaiNilai(esp, eipoffset)
	cs := exceptionBingkaiNilai(esp, eipoffset+4)
	eflags := exceptionBingkaiNilai(esp, eipoffset+8)

	MEmergencylogBenang(" err=")
	MEmergencylogunsignedinteger32(galat)
	MEmergencylogBenang(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogBenang(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogBenang(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogBenang(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogBenang(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if interupsi == 0x0E {
		MEmergencylogBenang(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		cetakHalamanfaultinfo(galat)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogBenang(" useresp=")
		MEmergencylogunsignedinteger32(exceptionBingkaiNilai(esp, eipoffset+12))
		MEmergencylogBenang(" ss=")
		MEmergencylogunsignedinteger32(exceptionBingkaiNilai(esp, eipoffset+16))
	}

	if exceptionhasGalatcode(interupsi) {
		cetakexceptionselectorinfo(galat)
	}
	MEmergencylogBenang("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func PenangananfatalInterupsiBingkai(savedesp uint32, interupsi uint32) uint32 {
	Penangananexception(savedesp+52, interupsi)
	haltafterfatalexception()
	return savedesp
}

func InterupsiAktif()
func (dirisendiri *TInterupsimanager) Aktif() {
	if AktifInterupsimanager != 0 {
		dirisendiri.Deactive()
	}
	address := uintptr(Pointer(dirisendiri))
	AktifInterupsimanager = address
	InterupsiAktif()
}
func Interupsideactive()
func (dirisendiri *TInterupsimanager) Deactive() {
	AktifInterupsimanager = 0
	Interupsideactive()
}

func MyPenangananInterupsi(interupsi uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
	return esp
}
func MyTes(interupsi uint8, esp uint32)

func UnhandleInterupsi() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MCetak(buffer)
}

func interupsihandler_2(interupsi uint8, esp uint32) uint32 {
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
