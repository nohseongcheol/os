/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Katkestus

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multitasking"
import . "console"

func katkestusignore()

func katkestusexceptionhandler()
func katkestusexceptionhandler0x00()
func katkestusexceptionhandler0x01()
func katkestusexceptionhandler0x02()
func katkestusexceptionhandler0x03()
func katkestusexceptionhandler0x04()
func katkestusexceptionhandler0x05()
func katkestusexceptionhandler0x06()
func katkestusexceptionhandler0x07()
func katkestusexceptionhandler0x08()
func katkestusexceptionhandler0x09()
func katkestusexceptionhandler0x0a()
func katkestusexceptionhandler0x0b()
func katkestusexceptionhandler0x0c()
func katkestusexceptionhandler0x0d()
func katkestusexceptionhandler0x0e()
func katkestusexceptionhandler0x0f()
func katkestusexceptionhandler0x10()
func katkestusexceptionhandler0x11()
func katkestusexceptionhandler0x12()
func katkestusexceptionhandler0x13()

func katkestusrequesthandler0x00()
func katkestusrequesthandler0x01()
func katkestusrequesthandler0x02()
func katkestusrequesthandler0x03()
func katkestusrequesthandler0x04()
func katkestusrequesthandler0x05()
func katkestusrequesthandler0x06()
func katkestusrequesthandler0x07()
func katkestusrequesthandler0x08()
func katkestusrequesthandler0x09()
func katkestusrequesthandler0x0a()
func katkestusrequesthandler0x0b()
func katkestusrequesthandler0x0c()
func katkestusrequesthandler0x0d()
func katkestusrequesthandler0x0e()
func katkestusrequesthandler0x0f()

func katkestusrequesthandler0x80()
func katkestusrequesthandler0x81()
func katkestusrequesthandler0x82()

func TestiPrindi(asukoht uint8, data uint8)
func määrads(dssegment uint32)
func määrags(gssegment uint32)
func katkestusVäljuloop()

type TKatkestushandler struct {
	KatkestusArv		uint8
	Katkestusmanager	uintptr
}
type IKatkestushandler interface {
	HandleKatkestus(uint32) uint32
}

func UusKatkestushandler(Katkestusmanager uintptr, KatkestusArv uint8) *TKatkestushandler {
	katkestushandler_2 := new(TKatkestushandler)
	katkestushandler_2.KatkestusArv = KatkestusArv
	katkestushandler_2.Katkestusmanager = Katkestusmanager
	return katkestushandler_2

}

var handler_2 [256]uintptr

func (ise *TKatkestushandler) Init(KatkestusArv uint8, Katkestusmanager uintptr, funcaddress uintptr) {

	handler_2[KatkestusArv] = funcaddress

	ise.KatkestusArv = KatkestusArv
	ise.Katkestusmanager = Katkestusmanager

}
func (ise *TKatkestushandler) MäärahandleKatkestusfuction(KatkestusArv uint32, address uintptr) {
	handler_2[KatkestusArv] = address
}
func (ise *TKatkestushandler) Hävita() {
	iseuintptr := uintptr(Pointer(ise))
	Katkestusmanager := (*TKatkestusmanager)(Pointer(ise.Katkestusmanager))
	if iseuintptr == Katkestusmanager.Gethandler(ise.KatkestusArv) {
		Katkestusmanager.Määrahandler(0, ise.KatkestusArv)
	}

}
func (ise *TKatkestushandler) MääraKatkestusmanager(Katkestusmanager uintptr) {
}
func (ise *TKatkestushandler) MääraKatkestusArv(KatkestusArv uint8) {
	ise.KatkestusArv = KatkestusArv
}
func (ise *TKatkestushandler) HandleKatkestus(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MPrindi(buffer)
	return esp
}
func HandleKatkestus1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MPrindi(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TKatkestusdescriptorTabelKursor struct {
}

var idtdata [256 * 8]uint8
var AktiivneKatkestusmanager uintptr = 0

const katkestusSilumine = false

type TKatkestusmanager struct {
	handler_2	[256]uintptr

	riistvaraKatkestusoffset	uint16

	taskmanager	*TTaskmanager
}

var PrimarypicKäskioport uint16 = 0x20
var Primarypicdataioport uint16 = 0x21
var SecondarypicKäskioport uint16 = 0xA0
var Secondarypicdataioport uint16 = 0xA1

func (ise *TKatkestusmanager) Init(riistvaraKatkestusoffset uint16, globaalnedescriptorTabel *TShareddescriptorTabel, taskmanager *TTaskmanager) {

	ise.taskmanager = taskmanager

	ise.riistvaraKatkestusoffset = riistvaraKatkestusoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtKatkestusgate uint8 = 0xE
	address = uint32(ValueOf(katkestusignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(katkestusexceptionhandler0x0f).Pointer())
		ise.KatkestusdescriptorTabelkirjeMäära(i, codesegment, address, 0, IdtKatkestusgate)
	}

	address = uint32(ValueOf(katkestusexceptionhandler0x00).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x00, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x01).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x01, codesegment, address, 0, IdtKatkestusgate)
	address = uint32(ValueOf(katkestusexceptionhandler0x02).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x02, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x03).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x03, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x04).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x04, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x05).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x05, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x06).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x06, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x07).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x07, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x08).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x08, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x09).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x09, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x0a).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x0A, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x0b).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x0B, codesegment, address, 0, IdtKatkestusgate)
	address = uint32(ValueOf(katkestusexceptionhandler0x0c).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x0C, codesegment, address, 0, IdtKatkestusgate)
	address = uint32(ValueOf(katkestusexceptionhandler0x0d).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x0D, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x0e).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x0E, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x0f).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x0F, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x10).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x10, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x11).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x11, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x12).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x12, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusexceptionhandler0x13).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x13, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x00).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x20, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x01).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x21, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x02).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x22, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x03).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x23, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x04).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x24, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x05).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x25, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x06).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x26, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x07).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x27, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x08).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x28, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x09).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x29, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x0a).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x2A, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x0b).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x2B, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x0c).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x2C, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x0d).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x2D, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x0e).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x2E, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x0f).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x2F, codesegment, address, 0, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x80).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x80, codesegment, address, 3, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x81).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x81, codesegment, address, 3, IdtKatkestusgate)

	address = uint32(ValueOf(katkestusrequesthandler0x82).Pointer())
	ise.KatkestusdescriptorTabelkirjeMäära(0x82, codesegment, address, 3, IdtKatkestusgate)

	PortKirjutaminebyte(PrimarypicKäskioport, 0x11)
	PortKirjutaminebyte(SecondarypicKäskioport, 0x11)

	PortKirjutaminebyte(Primarypicdataioport, 0x20)
	PortKirjutaminebyte(Secondarypicdataioport, 0x28)

	PortKirjutaminebyte(Primarypicdataioport, 0x04)
	PortKirjutaminebyte(Secondarypicdataioport, 0x02)

	PortKirjutaminebyte(Primarypicdataioport, 0x01)
	PortKirjutaminebyte(Secondarypicdataioport, 0x01)

	PortKirjutaminebyte(Primarypicdataioport, 0xF8)
	PortKirjutaminebyte(Secondarypicdataioport, 0xEF)

	idtKursor := [6]uint8{0, 0, 0, 0, 0, 0}
	suurus := (*uint16)(Pointer(&idtKursor[0]))
	(*suurus) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtKursor[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtKursor)))
}
func Lidt(lidtaddr uintptr)

func (ise *TKatkestusmanager) KatkestusdescriptorTabelkirjeMäära(katkestus int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorLiik uint8) {

	handleraddressMadalbitti := (*uint16)(Pointer(&idtdata[katkestus*8+0]))
	(*handleraddressMadalbitti) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[katkestus*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[katkestus*8+4]))
	(*reserved) = 0

	var IdtdescriptorOlemas uint8 = 0x80
	ligipääs := (*uint8)(Pointer(&idtdata[katkestus*8+5]))
	(*ligipääs) = (IdtdescriptorOlemas | DescriptorLiik | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressKõrgebitti := (*uint16)(Pointer(&idtdata[katkestus*8+6]))
	(*handleraddressKõrgebitti) = uint16((handler >> 16) & 0xFFFF)

}

func (ise *TKatkestusmanager) Määrahandler(handler uintptr, KatkestusArv uint8) {
	handler_2[KatkestusArv] = handler
}
func (ise *TKatkestusmanager) Gethandler(KatkestusArv uint8) uintptr {
	return handler_2[KatkestusArv]
}
func (ise *TKatkestusmanager) DohandleKatkestus(katkestus uint8, esp uint32) uint32 {

	if katkestusSilumine {
		console_2.MPrindixy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Prindi(uint32(katkestus))
		console_2.MPrindi(":")
		console_2.MUnsignedinteger32Prindi(esp)
	}
	handlerKäivita := false
	if handler_2[katkestus] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[katkestus])))
		esp = myfunction(esp)
		handlerKäivita = true

	}

	if !handlerKäivita && katkestus == uint8(ise.riistvaraKatkestusoffset) && ise.taskmanager != nil {
		esp = uint32(uintptr(Pointer(ise.taskmanager.Schedule((*TcpuOlek)(Pointer(uintptr(esp)))))))

	}
	if !handlerKäivita && katkestus == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if katkestus <= 0x1F {
	}
	if 0x20 <= katkestus && katkestus < 0x30 {
		if 0x28 <= katkestus {
			PortKirjutaminebyte(SecondarypicKäskioport, 0x20)
		}
		PortKirjutaminebyte(PrimarypicKäskioport, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func määracr3(address uint32)

var console_2 TConsole = TConsole{}

func HandleKatkestus(esp uint32, katkestus uint32) uint32 {

	if katkestusSilumine && katkestus != 0x80 && katkestus != 0x20 {
		console_2.MPrindixy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Prindi(uint32(katkestus))
		console_2.MPrindi(":")
		console_2.MUnsignedinteger32Prindi(esp)
	}

	if AktiivneKatkestusmanager != 0 {
		p := (*TKatkestusmanager)(Pointer(AktiivneKatkestusmanager))
		esp = p.DohandleKatkestus(uint8(katkestus), esp)
		return esp
	}
	if handler_2[katkestus] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[katkestus])))
		esp = myfunction(esp)
	}
	if katkestus == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= katkestus && katkestus < 0x30 {
		if 0x28 <= katkestus {
			PortKirjutaminebyte(SecondarypicKäskioport, 0x20)
		}
		PortKirjutaminebyte(PrimarypicKäskioport, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	protsessor := (*TcpuOlek)(Pointer(uintptr(esp)))
	if protsessor.Eax == 1 || protsessor.Eax == 252 {
		protsessor.Eip = uint32(ValueOf(katkestusVäljuloop).Pointer())
		protsessor.Cs = Segkernelcode
		protsessor.Ds = Segkerneldata
		protsessor.Es = Segkerneldata
		protsessor.Fs = Segkerneldata
		protsessor.Gs = Segkernelgs
		protsessor.Ss = Segkerneldata
		protsessor.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasVigacode(katkestus uint32) bool {
	switch katkestus {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNimi(katkestus uint32) string {
	switch katkestus {
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

func exceptionRaamVäärtus(raam uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(raam + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func prindiLehekülgfaultinfo(viga uint32) {
	MEmergencylogstring(" pf=[")
	if (viga & 0x01) != 0 {
		MEmergencylogstring("protection")
	} else {
		MEmergencylogstring("not-present")
	}
	if (viga & 0x02) != 0 {
		MEmergencylogstring(",write")
	} else {
		MEmergencylogstring(",read")
	}
	if (viga & 0x04) != 0 {
		MEmergencylogstring(",user")
	} else {
		MEmergencylogstring(",kernel")
	}
	if (viga & 0x08) != 0 {
		MEmergencylogstring(",reserved-bit")
	}
	if (viga & 0x10) != 0 {
		MEmergencylogstring(",instruction-fetch")
	}
	MEmergencylogstring("]")
}

func prindiexceptionselectorinfo(viga uint32) {
	MEmergencylogstring(" selector=")
	MEmergencylogunsignedinteger32(viga & 0xFFFFFFF8)
	MEmergencylogstring(" index=")
	MEmergencylogunsignedinteger32(viga >> 3)
	MEmergencylogstring(" table=")
	if (viga & 0x02) != 0 {
		MEmergencylogstring("IDT")
	} else if (viga & 0x04) != 0 {
		MEmergencylogstring("LDT")
	} else {
		MEmergencylogstring("GDT")
	}
	MEmergencylogstring(" ext=")
	MEmergencylogunsignedinteger32(viga & 0x01)
}

func Handleexception(esp uint32, katkestus uint32) uint32 {
	MEmergencylogstring("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(katkestus))
	MEmergencylogstring(" ")
	MEmergencylogstring(exceptionNimi(katkestus))
	MEmergencylogstring(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogstring(" invalid-frame")
		if exceptionhasVigacode(katkestus) {
			MEmergencylogstring(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			prindiexceptionselectorinfo(esp)
		}
		MEmergencylogstring("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var viga uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasVigacode(katkestus) {
		viga = exceptionRaamVäärtus(esp, 0)
		eipoffset = 4
	}
	eip := exceptionRaamVäärtus(esp, eipoffset)
	cs := exceptionRaamVäärtus(esp, eipoffset+4)
	eflags := exceptionRaamVäärtus(esp, eipoffset+8)

	MEmergencylogstring(" err=")
	MEmergencylogunsignedinteger32(viga)
	MEmergencylogstring(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogstring(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogstring(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogstring(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogstring(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if katkestus == 0x0E {
		MEmergencylogstring(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		prindiLehekülgfaultinfo(viga)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogstring(" useresp=")
		MEmergencylogunsignedinteger32(exceptionRaamVäärtus(esp, eipoffset+12))
		MEmergencylogstring(" ss=")
		MEmergencylogunsignedinteger32(exceptionRaamVäärtus(esp, eipoffset+16))
	}

	if exceptionhasVigacode(katkestus) {
		prindiexceptionselectorinfo(viga)
	}
	MEmergencylogstring("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandlefatalKatkestusRaam(savedesp uint32, katkestus uint32) uint32 {
	Handleexception(savedesp+52, katkestus)
	haltafterfatalexception()
	return savedesp
}

func KatkestusAktiivne()
func (ise *TKatkestusmanager) Aktiivne() {
	if AktiivneKatkestusmanager != 0 {
		ise.Deactive()
	}
	address := uintptr(Pointer(ise))
	AktiivneKatkestusmanager = address
	KatkestusAktiivne()
}
func Katkestusdeactive()
func (ise *TKatkestusmanager) Deactive() {
	AktiivneKatkestusmanager = 0
	Katkestusdeactive()
}

func MyhandleKatkestus(katkestus uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MPrindi(buffer)
	return esp
}
func MyTesti(katkestus uint8, esp uint32)

func UnhandleKatkestus() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MPrindi(buffer)
}

func katkestushandler_2(katkestus uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MPrindi(buffer)
	console_2.MHexadecimalPrindi(0x40)
	return esp
}
func prindiesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Prindixy(esp, 20, 21)
}
func gettls() uint32
func Prinditls() {

}
