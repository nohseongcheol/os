/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Interruption

import . "unsafe"
import . "reflect"

import . "port"
import . "gdt"
import . "multiplegestionTâches"
import . "console"

func interruptionignore()

func interruptionexceptionhandler()
func interruptionexceptionhandler0x00()
func interruptionexceptionhandler0x01()
func interruptionexceptionhandler0x02()
func interruptionexceptionhandler0x03()
func interruptionexceptionhandler0x04()
func interruptionexceptionhandler0x05()
func interruptionexceptionhandler0x06()
func interruptionexceptionhandler0x07()
func interruptionexceptionhandler0x08()
func interruptionexceptionhandler0x09()
func interruptionexceptionhandler0x0a()
func interruptionexceptionhandler0x0b()
func interruptionexceptionhandler0x0c()
func interruptionexceptionhandler0x0d()
func interruptionexceptionhandler0x0e()
func interruptionexceptionhandler0x0f()
func interruptionexceptionhandler0x10()
func interruptionexceptionhandler0x11()
func interruptionexceptionhandler0x12()
func interruptionexceptionhandler0x13()

func interruptionrequesthandler0x00()
func interruptionrequesthandler0x01()
func interruptionrequesthandler0x02()
func interruptionrequesthandler0x03()
func interruptionrequesthandler0x04()
func interruptionrequesthandler0x05()
func interruptionrequesthandler0x06()
func interruptionrequesthandler0x07()
func interruptionrequesthandler0x08()
func interruptionrequesthandler0x09()
func interruptionrequesthandler0x0a()
func interruptionrequesthandler0x0b()
func interruptionrequesthandler0x0c()
func interruptionrequesthandler0x0d()
func interruptionrequesthandler0x0e()
func interruptionrequesthandler0x0f()

func interruptionrequesthandler0x80()
func interruptionrequesthandler0x81()
func interruptionrequesthandler0x82()

func TesterImprimer(position uint8, données uint8)
func ensembleds(dssegment uint32)
func ensemblegs(gssegment uint32)
func interruptionQuitterBoucles()

type TInterruptionhandler struct {
	InterruptionNombre		uint8
	Interruptiongestionnaire	uintptr
}
type IInterruptionhandler interface {
	Poignéeinterruption(uint32) uint32
}

func Nouveauinterruptionhandler(Interruptiongestionnaire uintptr, InterruptionNombre uint8) *TInterruptionhandler {
	interruptionhandler_2 := new(TInterruptionhandler)
	interruptionhandler_2.InterruptionNombre = InterruptionNombre
	interruptionhandler_2.Interruptiongestionnaire = Interruptiongestionnaire
	return interruptionhandler_2

}

var handler_2 [256]uintptr

func (self *TInterruptionhandler) Init(InterruptionNombre uint8, Interruptiongestionnaire uintptr, funcaddress uintptr) {

	handler_2[InterruptionNombre] = funcaddress

	self.InterruptionNombre = InterruptionNombre
	self.Interruptiongestionnaire = Interruptiongestionnaire

}
func (self *TInterruptionhandler) EnsemblePoignéeinterruptionfuction(InterruptionNombre uint32, address uintptr) {
	handler_2[InterruptionNombre] = address
}
func (self *TInterruptionhandler) Détruire() {
	selfuintptr := uintptr(Pointer(self))
	Interruptiongestionnaire := (*TInterruptiongestionnaire)(Pointer(self.Interruptiongestionnaire))
	if selfuintptr == Interruptiongestionnaire.Gethandler(self.InterruptionNombre) {
		Interruptiongestionnaire.Ensemblehandler(0, self.InterruptionNombre)
	}

}
func (self *TInterruptionhandler) Ensembleinterruptiongestionnaire(Interruptiongestionnaire uintptr) {
}
func (self *TInterruptionhandler) EnsembleinterruptionNombre(InterruptionNombre uint8) {
	self.InterruptionNombre = InterruptionNombre
}
func (self *TInterruptionhandler) Poignéeinterruption(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MImprimer(buffer)
	return esp
}
func Poignéeinterruption1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MImprimer(buffer)
}

type TPortedescriptor struct {
	portedonnées [8]uint8
}
type TInterruptiondescriptorTableauPointeur struct {
}

var idtdonnées [256 * 8]uint8
var Actifinterruptiongestionnaire uintptr = 0

const interruptionDéboguer = false

type TInterruptiongestionnaire struct {
	handler_2	[256]uintptr

	matérielinterruptionDécalage	uint16

	tâchegestionnaire	*TTâchegestionnaire
}

var PrimarypicCommandeESport uint16 = 0x20
var PrimarypicdonnéesESport uint16 = 0x21
var SecondarypicCommandeESport uint16 = 0xA0
var SecondarypicdonnéesESport uint16 = 0xA1

func (self *TInterruptiongestionnaire) Init(matérielinterruptionDécalage uint16, globaldescriptorTableau *TShareddescriptorTableau, tâchegestionnaire *TTâchegestionnaire) {

	self.tâchegestionnaire = tâchegestionnaire

	self.matérielinterruptionDécalage = matérielinterruptionDécalage
	codesegment := uint16(Segnoyaucode)

	for i := 0; i < (256 * 8); i++ {
		idtdonnées[i] = 0
	}
	var address uint32
	var Idtinterruptionporte uint8 = 0xE
	address = uint32(ValueOf(interruptionignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(interruptionexceptionhandler0x0f).Pointer())
		self.InterruptiondescriptorTableauélémentensemble(i, codesegment, address, 0, Idtinterruptionporte)
	}

	address = uint32(ValueOf(interruptionexceptionhandler0x00).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x00, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x01).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x01, codesegment, address, 0, Idtinterruptionporte)
	address = uint32(ValueOf(interruptionexceptionhandler0x02).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x02, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x03).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x03, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x04).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x04, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x05).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x05, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x06).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x06, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x07).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x07, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x08).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x08, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x09).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x09, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x0a).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x0A, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x0b).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x0B, codesegment, address, 0, Idtinterruptionporte)
	address = uint32(ValueOf(interruptionexceptionhandler0x0c).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x0C, codesegment, address, 0, Idtinterruptionporte)
	address = uint32(ValueOf(interruptionexceptionhandler0x0d).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x0D, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x0e).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x0E, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x0f).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x0F, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x10).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x10, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x11).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x11, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x12).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x12, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionexceptionhandler0x13).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x13, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x00).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x20, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x01).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x21, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x02).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x22, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x03).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x23, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x04).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x24, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x05).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x25, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x06).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x26, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x07).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x27, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x08).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x28, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x09).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x29, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x0a).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x2A, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x0b).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x2B, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x0c).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x2C, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x0d).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x2D, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x0e).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x2E, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x0f).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x2F, codesegment, address, 0, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x80).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x80, codesegment, address, 3, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x81).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x81, codesegment, address, 3, Idtinterruptionporte)

	address = uint32(ValueOf(interruptionrequesthandler0x82).Pointer())
	self.InterruptiondescriptorTableauélémentensemble(0x82, codesegment, address, 3, Idtinterruptionporte)

	Portécrireoctet(PrimarypicCommandeESport, 0x11)
	Portécrireoctet(SecondarypicCommandeESport, 0x11)

	Portécrireoctet(PrimarypicdonnéesESport, 0x20)
	Portécrireoctet(SecondarypicdonnéesESport, 0x28)

	Portécrireoctet(PrimarypicdonnéesESport, 0x04)
	Portécrireoctet(SecondarypicdonnéesESport, 0x02)

	Portécrireoctet(PrimarypicdonnéesESport, 0x01)
	Portécrireoctet(SecondarypicdonnéesESport, 0x01)

	Portécrireoctet(PrimarypicdonnéesESport, 0xF8)
	Portécrireoctet(SecondarypicdonnéesESport, 0xEF)

	idtPointeur := [6]uint8{0, 0, 0, 0, 0, 0}
	taille := (*uint16)(Pointer(&idtPointeur[0]))
	(*taille) = (uint16)(Sizeof(idtdonnées) - 1)

	base := (*uint32)(Pointer(&idtPointeur[2]))
	(*base) = uint32(uintptr(Pointer(&idtdonnées)))

	Lidt(uintptr(Pointer(&idtPointeur)))
}
func Lidt(lidtaddr uintptr)

func (self *TInterruptiongestionnaire) InterruptiondescriptorTableauélémentensemble(interruption int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	Descriptortype uint8) {

	handleraddressBassebits := (*uint16)(Pointer(&idtdonnées[interruption*8+0]))
	(*handleraddressBassebits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdonnées[interruption*8+2]))
	(*gdtcodesegmentselector) = codesegment

	réservé := (*uint8)(Pointer(&idtdonnées[interruption*8+4]))
	(*réservé) = 0

	var IdtdescriptorPrésente uint8 = 0x80
	accès := (*uint8)(Pointer(&idtdonnées[interruption*8+5]))
	(*accès) = (IdtdescriptorPrésente | Descriptortype | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressÉlevéebits := (*uint16)(Pointer(&idtdonnées[interruption*8+6]))
	(*handleraddressÉlevéebits) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TInterruptiongestionnaire) Ensemblehandler(handler uintptr, InterruptionNombre uint8) {
	handler_2[InterruptionNombre] = handler
}
func (self *TInterruptiongestionnaire) Gethandler(InterruptionNombre uint8) uintptr {
	return handler_2[InterruptionNombre]
}
func (self *TInterruptiongestionnaire) DoPoignéeinterruption(interruption uint8, esp uint32) uint32 {

	if interruptionDéboguer {
		console_2.MImprimerxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Imprimer(uint32(interruption))
		console_2.MImprimer(":")
		console_2.MUnsignedinteger32Imprimer(esp)
	}
	handlerDémarrer := false
	if handler_2[interruption] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interruption])))
		esp = myfunction(esp)
		handlerDémarrer = true

	}

	if !handlerDémarrer && interruption == uint8(self.matérielinterruptionDécalage) && self.tâchegestionnaire != nil {
		esp = uint32(uintptr(Pointer(self.tâchegestionnaire.Schedule((*TcpuÉtat)(Pointer(uintptr(esp)))))))

	}
	if !handlerDémarrer && interruption == 0x80 {
		esp = poignéeunhandledsyscall(esp)
	}

	if interruption <= 0x1F {
	}
	if 0x20 <= interruption && interruption < 0x30 {
		if 0x28 <= interruption {
			Portécrireoctet(SecondarypicCommandeESport, 0x20)
		}
		Portécrireoctet(PrimarypicCommandeESport, 0x20)
	}
	return esp
}

var nombre2 uint8 = 1

func ensemblecr3(address uint32)

var console_2 TConsole = TConsole{}

func Poignéeinterruption(esp uint32, interruption uint32) uint32 {

	if interruptionDéboguer && interruption != 0x80 && interruption != 0x20 {
		console_2.MImprimerxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Imprimer(uint32(interruption))
		console_2.MImprimer(":")
		console_2.MUnsignedinteger32Imprimer(esp)
	}

	if Actifinterruptiongestionnaire != 0 {
		p := (*TInterruptiongestionnaire)(Pointer(Actifinterruptiongestionnaire))
		esp = p.DoPoignéeinterruption(uint8(interruption), esp)
		return esp
	}
	if handler_2[interruption] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[interruption])))
		esp = myfunction(esp)
	}
	if interruption == 0x80 {
		return poignéeunhandledsyscall(esp)
	}
	if 0x20 <= interruption && interruption < 0x30 {
		if 0x28 <= interruption {
			Portécrireoctet(SecondarypicCommandeESport, 0x20)
		}
		Portécrireoctet(PrimarypicCommandeESport, 0x20)
	}

	return esp
}

func poignéeunhandledsyscall(esp uint32) uint32 {
	processeur := (*TcpuÉtat)(Pointer(uintptr(esp)))
	if processeur.Eax == 1 || processeur.Eax == 252 {
		processeur.Eip = uint32(ValueOf(interruptionQuitterBoucles).Pointer())
		processeur.Cs = Segnoyaucode
		processeur.Ds = Segnoyaudonnées
		processeur.Es = Segnoyaudonnées
		processeur.Fs = Segnoyaudonnées
		processeur.Gs = Segnoyaugs
		processeur.Ss = Segnoyaudonnées
		processeur.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasErreurcode(interruption uint32) bool {
	switch interruption {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionNom(interruption uint32) string {
	switch interruption {
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

func exceptiontrameValeur(trame uint32, décalage uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(trame + décalage)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func imprimerpagedéfautinfo(err uint32) {
	MEmergencyJournalChaîne(" pf=[")
	if (err & 0x01) != 0 {
		MEmergencyJournalChaîne("protection")
	} else {
		MEmergencyJournalChaîne("not-present")
	}
	if (err & 0x02) != 0 {
		MEmergencyJournalChaîne(",write")
	} else {
		MEmergencyJournalChaîne(",read")
	}
	if (err & 0x04) != 0 {
		MEmergencyJournalChaîne(",user")
	} else {
		MEmergencyJournalChaîne(",kernel")
	}
	if (err & 0x08) != 0 {
		MEmergencyJournalChaîne(",reserved-bit")
	}
	if (err & 0x10) != 0 {
		MEmergencyJournalChaîne(",instruction-fetch")
	}
	MEmergencyJournalChaîne("]")
}

func imprimerexceptionselectorinfo(err uint32) {
	MEmergencyJournalChaîne(" selector=")
	MEmergencyJournalunsignedinteger32(err & 0xFFFFFFF8)
	MEmergencyJournalChaîne(" index=")
	MEmergencyJournalunsignedinteger32(err >> 3)
	MEmergencyJournalChaîne(" table=")
	if (err & 0x02) != 0 {
		MEmergencyJournalChaîne("IDT")
	} else if (err & 0x04) != 0 {
		MEmergencyJournalChaîne("LDT")
	} else {
		MEmergencyJournalChaîne("GDT")
	}
	MEmergencyJournalChaîne(" ext=")
	MEmergencyJournalunsignedinteger32(err & 0x01)
}

func Poignéeexception(esp uint32, interruption uint32) uint32 {
	MEmergencyJournalChaîne("\nEXCEPTION vec=")
	MEmergencyJournalhexadecimal8(uint8(interruption))
	MEmergencyJournalChaîne(" ")
	MEmergencyJournalChaîne(exceptionNom(interruption))
	MEmergencyJournalChaîne(" frame=")
	MEmergencyJournalunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyJournalChaîne(" invalid-frame")
		if exceptionhasErreurcode(interruption) {
			MEmergencyJournalChaîne(" raw-error-or-bad-esp=")
			MEmergencyJournalunsignedinteger32(esp)
			imprimerexceptionselectorinfo(esp)
		}
		MEmergencyJournalChaîne("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var err uint32 = 0
	var eipDécalage uint32 = 0
	if exceptionhasErreurcode(interruption) {
		err = exceptiontrameValeur(esp, 0)
		eipDécalage = 4
	}
	eip := exceptiontrameValeur(esp, eipDécalage)
	cs := exceptiontrameValeur(esp, eipDécalage+4)
	eflags := exceptiontrameValeur(esp, eipDécalage+8)

	MEmergencyJournalChaîne(" err=")
	MEmergencyJournalunsignedinteger32(err)
	MEmergencyJournalChaîne(" eip=")
	MEmergencyJournalunsignedinteger32(eip)
	MEmergencyJournalChaîne(" cs=")
	MEmergencyJournalunsignedinteger32(cs)
	MEmergencyJournalChaîne(" eflags=")
	MEmergencyJournalunsignedinteger32(eflags)
	MEmergencyJournalChaîne(" cr0=")
	MEmergencyJournalunsignedinteger32(exceptioncr0())
	MEmergencyJournalChaîne(" cr3=")
	MEmergencyJournalunsignedinteger32(exceptioncr3())

	if interruption == 0x0E {
		MEmergencyJournalChaîne(" cr2=")
		MEmergencyJournalunsignedinteger32(exceptioncr2())
		imprimerpagedéfautinfo(err)
	}

	if (cs & 0x03) != 0 {
		MEmergencyJournalChaîne(" useresp=")
		MEmergencyJournalunsignedinteger32(exceptiontrameValeur(esp, eipDécalage+12))
		MEmergencyJournalChaîne(" ss=")
		MEmergencyJournalunsignedinteger32(exceptiontrameValeur(esp, eipDécalage+16))
	}

	if exceptionhasErreurcode(interruption) {
		imprimerexceptionselectorinfo(err)
	}
	MEmergencyJournalChaîne("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltAprèsfatalexception()

func Poignéefatalinterruptiontrame(sauvegardéesp uint32, interruption uint32) uint32 {
	Poignéeexception(sauvegardéesp+52, interruption)
	haltAprèsfatalexception()
	return sauvegardéesp
}

func InterruptionActif()
func (self *TInterruptiongestionnaire) Actif() {
	if Actifinterruptiongestionnaire != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	Actifinterruptiongestionnaire = address
	InterruptionActif()
}
func Interruptiondeactive()
func (self *TInterruptiongestionnaire) Deactive() {
	Actifinterruptiongestionnaire = 0
	Interruptiondeactive()
}

func MyPoignéeinterruption(interruption uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MImprimer(buffer)
	return esp
}
func MyTester(interruption uint8, esp uint32)

func Unhandleinterruption() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MImprimer(buffer)
}

func interruptionhandler_2(interruption uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MImprimer(buffer)
	console_2.MHexadecimalImprimer(0x40)
	return esp
}
func imprimeresp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Imprimerxy(esp, 20, 21)
}
func gettls() uint32
func Imprimertls() {

}
