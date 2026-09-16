/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Pārtraukums

import . "unsafe"
import . "reflect"

import . "ports"
import . "gdt"
import . "multitasking"
import . "console"

func pārtraukumsignore()

func pārtraukumsexceptionhandler()
func pārtraukumsexceptionhandler0x00()
func pārtraukumsexceptionhandler0x01()
func pārtraukumsexceptionhandler0x02()
func pārtraukumsexceptionhandler0x03()
func pārtraukumsexceptionhandler0x04()
func pārtraukumsexceptionhandler0x05()
func pārtraukumsexceptionhandler0x06()
func pārtraukumsexceptionhandler0x07()
func pārtraukumsexceptionhandler0x08()
func pārtraukumsexceptionhandler0x09()
func pārtraukumsexceptionhandler0x0a()
func pārtraukumsexceptionhandler0x0b()
func pārtraukumsexceptionhandler0x0c()
func pārtraukumsexceptionhandler0x0d()
func pārtraukumsexceptionhandler0x0e()
func pārtraukumsexceptionhandler0x0f()
func pārtraukumsexceptionhandler0x10()
func pārtraukumsexceptionhandler0x11()
func pārtraukumsexceptionhandler0x12()
func pārtraukumsexceptionhandler0x13()

func pārtraukumsrequesthandler0x00()
func pārtraukumsrequesthandler0x01()
func pārtraukumsrequesthandler0x02()
func pārtraukumsrequesthandler0x03()
func pārtraukumsrequesthandler0x04()
func pārtraukumsrequesthandler0x05()
func pārtraukumsrequesthandler0x06()
func pārtraukumsrequesthandler0x07()
func pārtraukumsrequesthandler0x08()
func pārtraukumsrequesthandler0x09()
func pārtraukumsrequesthandler0x0a()
func pārtraukumsrequesthandler0x0b()
func pārtraukumsrequesthandler0x0c()
func pārtraukumsrequesthandler0x0d()
func pārtraukumsrequesthandler0x0e()
func pārtraukumsrequesthandler0x0f()

func pārtraukumsrequesthandler0x80()
func pārtraukumsrequesthandler0x81()
func pārtraukumsrequesthandler0x82()

func PārbaudītDrukāt(novietojums uint8, data uint8)
func kopads(dssegment uint32)
func kopags(gssegment uint32)
func pārtraukumsIzietloop()

type TPārtraukumshandler struct {
	PārtraukumsSkaitlis	uint8
	Pārtraukumsmanager	uintptr
}
type IPārtraukumshandler interface {
	HandlePārtraukums(uint32) uint32
}

func JaunsPārtraukumshandler(Pārtraukumsmanager uintptr, PārtraukumsSkaitlis uint8) *TPārtraukumshandler {
	pārtraukumshandler_2 := new(TPārtraukumshandler)
	pārtraukumshandler_2.PārtraukumsSkaitlis = PārtraukumsSkaitlis
	pārtraukumshandler_2.Pārtraukumsmanager = Pārtraukumsmanager
	return pārtraukumshandler_2

}

var handler_2 [256]uintptr

func (pats *TPārtraukumshandler) Init(PārtraukumsSkaitlis uint8, Pārtraukumsmanager uintptr, funcaddress uintptr) {

	handler_2[PārtraukumsSkaitlis] = funcaddress

	pats.PārtraukumsSkaitlis = PārtraukumsSkaitlis
	pats.Pārtraukumsmanager = Pārtraukumsmanager

}
func (pats *TPārtraukumshandler) KopahandlePārtraukumsfuction(PārtraukumsSkaitlis uint32, address uintptr) {
	handler_2[PārtraukumsSkaitlis] = address
}
func (pats *TPārtraukumshandler) Iznīcināt() {
	patsuintptr := uintptr(Pointer(pats))
	Pārtraukumsmanager := (*TPārtraukumsmanager)(Pointer(pats.Pārtraukumsmanager))
	if patsuintptr == Pārtraukumsmanager.Gethandler(pats.PārtraukumsSkaitlis) {
		Pārtraukumsmanager.Kopahandler(0, pats.PārtraukumsSkaitlis)
	}

}
func (pats *TPārtraukumshandler) KopaPārtraukumsmanager(Pārtraukumsmanager uintptr) {
}
func (pats *TPārtraukumshandler) KopaPārtraukumsSkaitlis(PārtraukumsSkaitlis uint8) {
	pats.PārtraukumsSkaitlis = PārtraukumsSkaitlis
}
func (pats *TPārtraukumshandler) HandlePārtraukums(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MDrukāt(buffer)
	return esp
}
func HandlePārtraukums1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MDrukāt(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TPārtraukumsdescriptorTabulaKursors struct {
}

var idtdata [256 * 8]uint8
var AktīvsPārtraukumsmanager uintptr = 0

const pārtraukumsAtkļūdot = false

type TPārtraukumsmanager struct {
	handler_2	[256]uintptr

	aparatūraPārtraukumsoffset	uint16

	taskmanager	*TTaskmanager
}

var PrimarypicKomandaioPorts uint16 = 0x20
var PrimarypicdataioPorts uint16 = 0x21
var SecondarypicKomandaioPorts uint16 = 0xA0
var SecondarypicdataioPorts uint16 = 0xA1

func (pats *TPārtraukumsmanager) Init(aparatūraPārtraukumsoffset uint16, globālaisdescriptorTabula *TShareddescriptorTabula, taskmanager *TTaskmanager) {

	pats.taskmanager = taskmanager

	pats.aparatūraPārtraukumsoffset = aparatūraPārtraukumsoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtPārtraukumsgate uint8 = 0xE
	address = uint32(ValueOf(pārtraukumsignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(pārtraukumsexceptionhandler0x0f).Pointer())
		pats.PārtraukumsdescriptorTabulaierakstskopa(i, codesegment, address, 0, IdtPārtraukumsgate)
	}

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x00).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x00, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x01).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x01, codesegment, address, 0, IdtPārtraukumsgate)
	address = uint32(ValueOf(pārtraukumsexceptionhandler0x02).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x02, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x03).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x03, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x04).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x04, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x05).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x05, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x06).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x06, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x07).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x07, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x08).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x08, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x09).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x09, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x0a).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x0A, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x0b).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x0B, codesegment, address, 0, IdtPārtraukumsgate)
	address = uint32(ValueOf(pārtraukumsexceptionhandler0x0c).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x0C, codesegment, address, 0, IdtPārtraukumsgate)
	address = uint32(ValueOf(pārtraukumsexceptionhandler0x0d).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x0D, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x0e).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x0E, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x0f).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x0F, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x10).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x10, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x11).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x11, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x12).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x12, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsexceptionhandler0x13).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x13, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x00).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x20, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x01).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x21, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x02).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x22, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x03).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x23, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x04).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x24, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x05).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x25, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x06).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x26, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x07).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x27, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x08).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x28, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x09).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x29, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x0a).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x2A, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x0b).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x2B, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x0c).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x2C, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x0d).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x2D, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x0e).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x2E, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x0f).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x2F, codesegment, address, 0, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x80).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x80, codesegment, address, 3, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x81).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x81, codesegment, address, 3, IdtPārtraukumsgate)

	address = uint32(ValueOf(pārtraukumsrequesthandler0x82).Pointer())
	pats.PārtraukumsdescriptorTabulaierakstskopa(0x82, codesegment, address, 3, IdtPārtraukumsgate)

	PortsRakstītbyte(PrimarypicKomandaioPorts, 0x11)
	PortsRakstītbyte(SecondarypicKomandaioPorts, 0x11)

	PortsRakstītbyte(PrimarypicdataioPorts, 0x20)
	PortsRakstītbyte(SecondarypicdataioPorts, 0x28)

	PortsRakstītbyte(PrimarypicdataioPorts, 0x04)
	PortsRakstītbyte(SecondarypicdataioPorts, 0x02)

	PortsRakstītbyte(PrimarypicdataioPorts, 0x01)
	PortsRakstītbyte(SecondarypicdataioPorts, 0x01)

	PortsRakstītbyte(PrimarypicdataioPorts, 0xF8)
	PortsRakstītbyte(SecondarypicdataioPorts, 0xEF)

	idtKursors := [6]uint8{0, 0, 0, 0, 0, 0}
	izmērs := (*uint16)(Pointer(&idtKursors[0]))
	(*izmērs) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtKursors[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtKursors)))
}
func Lidt(lidtaddr uintptr)

func (pats *TPārtraukumsmanager) PārtraukumsdescriptorTabulaierakstskopa(pārtraukums int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorTips uint8) {

	handleraddressKlusibiti := (*uint16)(Pointer(&idtdata[pārtraukums*8+0]))
	(*handleraddressKlusibiti) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[pārtraukums*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[pārtraukums*8+4]))
	(*reserved) = 0

	var IdtdescriptorKlātesošs uint8 = 0x80
	piekļūt := (*uint8)(Pointer(&idtdata[pārtraukums*8+5]))
	(*piekļūt) = (IdtdescriptorKlātesošs | DescriptorTips | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressAugstabiti := (*uint16)(Pointer(&idtdata[pārtraukums*8+6]))
	(*handleraddressAugstabiti) = uint16((handler >> 16) & 0xFFFF)

}

func (pats *TPārtraukumsmanager) Kopahandler(handler uintptr, PārtraukumsSkaitlis uint8) {
	handler_2[PārtraukumsSkaitlis] = handler
}
func (pats *TPārtraukumsmanager) Gethandler(PārtraukumsSkaitlis uint8) uintptr {
	return handler_2[PārtraukumsSkaitlis]
}
func (pats *TPārtraukumsmanager) DohandlePārtraukums(pārtraukums uint8, esp uint32) uint32 {

	if pārtraukumsAtkļūdot {
		console_2.MDrukātxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Drukāt(uint32(pārtraukums))
		console_2.MDrukāt(":")
		console_2.MUnsignedinteger32Drukāt(esp)
	}
	handlerPalaist := false
	if handler_2[pārtraukums] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[pārtraukums])))
		esp = myfunction(esp)
		handlerPalaist = true

	}

	if !handlerPalaist && pārtraukums == uint8(pats.aparatūraPārtraukumsoffset) && pats.taskmanager != nil {
		esp = uint32(uintptr(Pointer(pats.taskmanager.Schedule((*TcpuStāvoklis)(Pointer(uintptr(esp)))))))

	}
	if !handlerPalaist && pārtraukums == 0x80 {
		esp = handleunhandledsyscall(esp)
	}

	if pārtraukums <= 0x1F {
	}
	if 0x20 <= pārtraukums && pārtraukums < 0x30 {
		if 0x28 <= pārtraukums {
			PortsRakstītbyte(SecondarypicKomandaioPorts, 0x20)
		}
		PortsRakstītbyte(PrimarypicKomandaioPorts, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func kopacr3(address uint32)

var console_2 TConsole = TConsole{}

func HandlePārtraukums(esp uint32, pārtraukums uint32) uint32 {

	if pārtraukumsAtkļūdot && pārtraukums != 0x80 && pārtraukums != 0x20 {
		console_2.MDrukātxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Drukāt(uint32(pārtraukums))
		console_2.MDrukāt(":")
		console_2.MUnsignedinteger32Drukāt(esp)
	}

	if AktīvsPārtraukumsmanager != 0 {
		p := (*TPārtraukumsmanager)(Pointer(AktīvsPārtraukumsmanager))
		esp = p.DohandlePārtraukums(uint8(pārtraukums), esp)
		return esp
	}
	if handler_2[pārtraukums] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[pārtraukums])))
		esp = myfunction(esp)
	}
	if pārtraukums == 0x80 {
		return handleunhandledsyscall(esp)
	}
	if 0x20 <= pārtraukums && pārtraukums < 0x30 {
		if 0x28 <= pārtraukums {
			PortsRakstītbyte(SecondarypicKomandaioPorts, 0x20)
		}
		PortsRakstītbyte(PrimarypicKomandaioPorts, 0x20)
	}

	return esp
}

func handleunhandledsyscall(esp uint32) uint32 {
	cpu := (*TcpuStāvoklis)(Pointer(uintptr(esp)))
	if cpu.Eax == 1 || cpu.Eax == 252 {
		cpu.Eip = uint32(ValueOf(pārtraukumsIzietloop).Pointer())
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

func exceptionhasKļūdacode(pārtraukums uint32) bool {
	switch pārtraukums {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNosaukums(pārtraukums uint32) string {
	switch pārtraukums {
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

func exceptionIetvarsVērtība(ietvars uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ietvars + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func drukātLapafaultinfo(err uint32) {
	MEmergencylogvirkne(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencylogvirkne("protection")
	} else {
		MEmergencylogvirkne("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencylogvirkne(",write")
	} else {
		MEmergencylogvirkne(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencylogvirkne(",user")
	} else {
		MEmergencylogvirkne(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencylogvirkne(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencylogvirkne(",instruction-fetch")
	}
	MEmergencylogvirkne("]")
}

func drukātexceptionselectorinfo(err uint32) {
	MEmergencylogvirkne(" selector=")
	MEmergencylogunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencylogvirkne(" index=")
	MEmergencylogunsignedinteger32(err >> 3)
	MEmergencylogvirkne(" table=")
	if (err & 0x02) != 0 {
		MEmergencylogvirkne("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencylogvirkne("LDT")
	} else {
		MEmergencylogvirkne("GDT")
	}
	MEmergencylogvirkne(" ext=")
	MEmergencylogunsignedinteger32(err & 0x01)
}

func Handleexception(esp uint32, pārtraukums uint32) uint32 {
	MEmergencylogvirkne("\nEXCEPTION vec=")
	MEmergencyloghexadecimal8(uint8(pārtraukums))
	MEmergencylogvirkne(" ")
	MEmergencylogvirkne(exceptionNosaukums(pārtraukums))
	MEmergencylogvirkne(" frame=")
	MEmergencylogunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencylogvirkne(" invalid-frame")
		if exceptionhasKļūdacode(pārtraukums) {
			MEmergencylogvirkne(" raw-error-or-bad-esp=")
			MEmergencylogunsignedinteger32(esp)
			drukātexceptionselectorinfo(esp)
		}
		MEmergencylogvirkne("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasKļūdacode(pārtraukums) {
		err = exceptionIetvarsVērtība(esp, 0)
		eipoffset = 4
	}
	eip := exceptionIetvarsVērtība(esp, eipoffset)
	cs := exceptionIetvarsVērtība(esp, eipoffset+4)
	eflags := exceptionIetvarsVērtība(esp, eipoffset+8)

	MEmergencylogvirkne(" err=")
	MEmergencylogunsignedinteger32(err)
	MEmergencylogvirkne(" eip=")
	MEmergencylogunsignedinteger32(eip)
	MEmergencylogvirkne(" cs=")
	MEmergencylogunsignedinteger32(cs)
	MEmergencylogvirkne(" eflags=")
	MEmergencylogunsignedinteger32(eflags)
	MEmergencylogvirkne(" cr0=")
	MEmergencylogunsignedinteger32(exceptioncr0())
	MEmergencylogvirkne(" cr3=")
	MEmergencylogunsignedinteger32(exceptioncr3())

	if pārtraukums == 0x0E {
		MEmergencylogvirkne(" cr2=")
		MEmergencylogunsignedinteger32(exceptioncr2())
		drukātLapafaultinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencylogvirkne(" useresp=")
		MEmergencylogunsignedinteger32(exceptionIetvarsVērtība(esp, eipoffset+12))
		MEmergencylogvirkne(" ss=")
		MEmergencylogunsignedinteger32(exceptionIetvarsVērtība(esp, eipoffset+16))
	}

	if exceptionhasKļūdacode(pārtraukums) {
		drukātexceptionselectorinfo(err)
	}
	MEmergencylogvirkne("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func HandlefatalPārtraukumsIetvars(savedesp uint32, pārtraukums uint32) uint32 {
	Handleexception(savedesp+52, pārtraukums)
	haltafterfatalexception()
	return savedesp
}

func PārtraukumsAktīvs()
func (pats *TPārtraukumsmanager) Aktīvs() {
	if AktīvsPārtraukumsmanager != 0 {
		pats.Deactive()
	}
	address := uintptr(Pointer(pats))
	AktīvsPārtraukumsmanager = address
	PārtraukumsAktīvs()
}
func Pārtraukumsdeactive()
func (pats *TPārtraukumsmanager) Deactive() {
	AktīvsPārtraukumsmanager = 0
	Pārtraukumsdeactive()
}

func MyhandlePārtraukums(pārtraukums uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MDrukāt(buffer)
	return esp
}
func MyPārbaudīt(pārtraukums uint8, esp uint32)

func UnhandlePārtraukums() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MDrukāt(buffer)
}

func pārtraukumshandler_2(pārtraukums uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MDrukāt(buffer)
	console_2.MHexadecimalDrukāt(0x40)
	return esp
}
func drukātesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Drukātxy(esp, 20, 21)
}
func gettls() uint32
func Drukāttls() {

}
