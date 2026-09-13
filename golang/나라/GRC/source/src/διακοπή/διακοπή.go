package Διακοπή

import . "unsafe"
import . "reflect"

import . "θύρα"
import . "gdt"
import . "multitasking"
import . "console"

func διακοπήignore()

func διακοπήexceptionhandler()
func διακοπήexceptionhandler0x00()
func διακοπήexceptionhandler0x01()
func διακοπήexceptionhandler0x02()
func διακοπήexceptionhandler0x03()
func διακοπήexceptionhandler0x04()
func διακοπήexceptionhandler0x05()
func διακοπήexceptionhandler0x06()
func διακοπήexceptionhandler0x07()
func διακοπήexceptionhandler0x08()
func διακοπήexceptionhandler0x09()
func διακοπήexceptionhandler0x0a()
func διακοπήexceptionhandler0x0b()
func διακοπήexceptionhandler0x0c()
func διακοπήexceptionhandler0x0d()
func διακοπήexceptionhandler0x0e()
func διακοπήexceptionhandler0x0f()
func διακοπήexceptionhandler0x10()
func διακοπήexceptionhandler0x11()
func διακοπήexceptionhandler0x12()
func διακοπήexceptionhandler0x13()

func διακοπήrequesthandler0x00()
func διακοπήrequesthandler0x01()
func διακοπήrequesthandler0x02()
func διακοπήrequesthandler0x03()
func διακοπήrequesthandler0x04()
func διακοπήrequesthandler0x05()
func διακοπήrequesthandler0x06()
func διακοπήrequesthandler0x07()
func διακοπήrequesthandler0x08()
func διακοπήrequesthandler0x09()
func διακοπήrequesthandler0x0a()
func διακοπήrequesthandler0x0b()
func διακοπήrequesthandler0x0c()
func διακοπήrequesthandler0x0d()
func διακοπήrequesthandler0x0e()
func διακοπήrequesthandler0x0f()

func διακοπήrequesthandler0x80()
func διακοπήrequesthandler0x81()
func διακοπήrequesthandler0x82()

func ΔοκιμήΕκτύπωση(θέση uint8, data uint8)
func σύνολοds(dssegment uint32)
func σύνολοgs(gssegment uint32)
func διακοπήΈξοδοςloop()

type TΔιακοπήhandler struct {
	ΔιακοπήΑριθμός	uint8
	Διακοπήmanager	uintptr
}
type IΔιακοπήhandler interface {
	ΧειρολαβήΔιακοπή(uint32) uint32
}

func ΝέοΔιακοπήhandler(Διακοπήmanager uintptr, ΔιακοπήΑριθμός uint8) *TΔιακοπήhandler {
	διακοπήhandler_2 := new(TΔιακοπήhandler)
	διακοπήhandler_2.ΔιακοπήΑριθμός = ΔιακοπήΑριθμός
	διακοπήhandler_2.Διακοπήmanager = Διακοπήmanager
	return διακοπήhandler_2

}

var handler_2 [256]uintptr

func (self *TΔιακοπήhandler) Init(ΔιακοπήΑριθμός uint8, Διακοπήmanager uintptr, funcaddress uintptr) {

	handler_2[ΔιακοπήΑριθμός] = funcaddress

	self.ΔιακοπήΑριθμός = ΔιακοπήΑριθμός
	self.Διακοπήmanager = Διακοπήmanager

}
func (self *TΔιακοπήhandler) ΣύνολοΧειρολαβήΔιακοπήfuction(ΔιακοπήΑριθμός uint32, address uintptr) {
	handler_2[ΔιακοπήΑριθμός] = address
}
func (self *TΔιακοπήhandler) Καταστροφή() {
	selfuintptr := uintptr(Pointer(self))
	Διακοπήmanager := (*TΔιακοπήmanager)(Pointer(self.Διακοπήmanager))
	if selfuintptr == Διακοπήmanager.Gethandler(self.ΔιακοπήΑριθμός) {
		Διακοπήmanager.Σύνολοhandler(0, self.ΔιακοπήΑριθμός)
	}

}
func (self *TΔιακοπήhandler) ΣύνολοΔιακοπήmanager(Διακοπήmanager uintptr) {
}
func (self *TΔιακοπήhandler) ΣύνολοΔιακοπήΑριθμός(ΔιακοπήΑριθμός uint8) {
	self.ΔιακοπήΑριθμός = ΔιακοπήΑριθμός
}
func (self *TΔιακοπήhandler) ΧειρολαβήΔιακοπή(esp uint32) uint32 {
	buffer := []byte("\n\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MΕκτύπωση(buffer)
	return esp
}
func ΧειρολαβήΔιακοπή1() {
	buffer := []byte("\n\n\n\n   TInterruptHandler")
	console_2 := TConsole{}
	console_2.MΕκτύπωση(buffer)
}

type TGatedescriptor struct {
	gatedata [8]uint8
}
type TΔιακοπήdescriptorΠίνακαςΔείκτης struct {
}

var idtdata [256 * 8]uint8
var ΕνεργόΔιακοπήmanager uintptr = 0

const διακοπήΔιόρθωση = false

type TΔιακοπήmanager struct {
	handler_2	[256]uintptr

	υλικόΔιακοπήoffset	uint16

	διεργασίαmanager	*TΔιεργασίαmanager
}

var PrimarypicΕντολήioΘύρα uint16 = 0x20
var PrimarypicdataioΘύρα uint16 = 0x21
var SecondarypicΕντολήioΘύρα uint16 = 0xA0
var SecondarypicdataioΘύρα uint16 = 0xA1

func (self *TΔιακοπήmanager) Init(υλικόΔιακοπήoffset uint16, καθολικάdescriptorΠίνακας *TShareddescriptorΠίνακας, διεργασίαmanager *TΔιεργασίαmanager) {

	self.διεργασίαmanager = διεργασίαmanager

	self.υλικόΔιακοπήoffset = υλικόΔιακοπήoffset
	codesegment := uint16(Segkernelcode)

	for i := 0; i < (256 * 8); i++ {
		idtdata[i] = 0
	}
	var address uint32
	var IdtΔιακοπήgate uint8 = 0xE
	address = uint32(ValueOf(διακοπήignore).Pointer())
	for i := 0; i < 256; i++ {
		handler_2[i] = 0
		address = uint32(ValueOf(διακοπήexceptionhandler0x0f).Pointer())
		self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(i, codesegment, address, 0, IdtΔιακοπήgate)
	}

	address = uint32(ValueOf(διακοπήexceptionhandler0x00).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x00, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x01).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x01, codesegment, address, 0, IdtΔιακοπήgate)
	address = uint32(ValueOf(διακοπήexceptionhandler0x02).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x02, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x03).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x03, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x04).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x04, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x05).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x05, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x06).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x06, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x07).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x07, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x08).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x08, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x09).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x09, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x0a).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x0A, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x0b).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x0B, codesegment, address, 0, IdtΔιακοπήgate)
	address = uint32(ValueOf(διακοπήexceptionhandler0x0c).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x0C, codesegment, address, 0, IdtΔιακοπήgate)
	address = uint32(ValueOf(διακοπήexceptionhandler0x0d).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x0D, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x0e).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x0E, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x0f).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x0F, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x10).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x10, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x11).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x11, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x12).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x12, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήexceptionhandler0x13).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x13, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x00).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x20, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x01).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x21, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x02).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x22, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x03).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x23, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x04).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x24, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x05).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x25, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x06).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x26, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x07).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x27, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x08).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x28, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x09).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x29, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x0a).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x2A, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x0b).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x2B, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x0c).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x2C, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x0d).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x2D, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x0e).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x2E, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x0f).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x2F, codesegment, address, 0, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x80).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x80, codesegment, address, 3, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x81).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x81, codesegment, address, 3, IdtΔιακοπήgate)

	address = uint32(ValueOf(διακοπήrequesthandler0x82).Pointer())
	self.ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(0x82, codesegment, address, 3, IdtΔιακοπήgate)

	ΘύραΕγγραφήbyte(PrimarypicΕντολήioΘύρα, 0x11)
	ΘύραΕγγραφήbyte(SecondarypicΕντολήioΘύρα, 0x11)

	ΘύραΕγγραφήbyte(PrimarypicdataioΘύρα, 0x20)
	ΘύραΕγγραφήbyte(SecondarypicdataioΘύρα, 0x28)

	ΘύραΕγγραφήbyte(PrimarypicdataioΘύρα, 0x04)
	ΘύραΕγγραφήbyte(SecondarypicdataioΘύρα, 0x02)

	ΘύραΕγγραφήbyte(PrimarypicdataioΘύρα, 0x01)
	ΘύραΕγγραφήbyte(SecondarypicdataioΘύρα, 0x01)

	ΘύραΕγγραφήbyte(PrimarypicdataioΘύρα, 0xF8)
	ΘύραΕγγραφήbyte(SecondarypicdataioΘύρα, 0xEF)

	idtΔείκτης := [6]uint8{0, 0, 0, 0, 0, 0}
	μέγεθος := (*uint16)(Pointer(&idtΔείκτης[0]))
	(*μέγεθος) = (uint16)(Sizeof(idtdata) - 1)

	base := (*uint32)(Pointer(&idtΔείκτης[2]))
	(*base) = uint32(uintptr(Pointer(&idtdata)))

	Lidt(uintptr(Pointer(&idtΔείκτης)))
}
func Lidt(lidtaddr uintptr)

func (self *TΔιακοπήmanager) ΔιακοπήdescriptorΠίνακαςκαταχώρησησύνολο(διακοπή int,
	codesegment uint16,
	handler uint32,
	Descriptorprivilegelevel uint8,
	DescriptorΤύπος uint8) {

	handleraddressΧαμηλήbits := (*uint16)(Pointer(&idtdata[διακοπή*8+0]))
	(*handleraddressΧαμηλήbits) = uint16(handler & 0xFFFF)

	gdtcodesegmentselector := (*uint16)(Pointer(&idtdata[διακοπή*8+2]))
	(*gdtcodesegmentselector) = codesegment

	reserved := (*uint8)(Pointer(&idtdata[διακοπή*8+4]))
	(*reserved) = 0

	var IdtdescriptorΠαρούσα uint8 = 0x80
	προσπέλαση := (*uint8)(Pointer(&idtdata[διακοπή*8+5]))
	(*προσπέλαση) = (IdtdescriptorΠαρούσα | DescriptorΤύπος | ((Descriptorprivilegelevel & 3) << 5))

	handleraddressΥψηλήbits := (*uint16)(Pointer(&idtdata[διακοπή*8+6]))
	(*handleraddressΥψηλήbits) = uint16((handler >> 16) & 0xFFFF)

}

func (self *TΔιακοπήmanager) Σύνολοhandler(handler uintptr, ΔιακοπήΑριθμός uint8) {
	handler_2[ΔιακοπήΑριθμός] = handler
}
func (self *TΔιακοπήmanager) Gethandler(ΔιακοπήΑριθμός uint8) uintptr {
	return handler_2[ΔιακοπήΑριθμός]
}
func (self *TΔιακοπήmanager) DoΧειρολαβήΔιακοπή(διακοπή uint8, esp uint32) uint32 {

	if διακοπήΔιόρθωση {
		console_2.MΕκτύπωσηxy("[esp:", 1, 20)
		console_2.MUnsignedinteger32Εκτύπωση(uint32(διακοπή))
		console_2.MΕκτύπωση(":")
		console_2.MUnsignedinteger32Εκτύπωση(esp)
	}
	handlerΕκτέλεση := false
	if handler_2[διακοπή] != 0 {

		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[διακοπή])))
		esp = myfunction(esp)
		handlerΕκτέλεση = true

	}

	if !handlerΕκτέλεση && διακοπή == uint8(self.υλικόΔιακοπήoffset) && self.διεργασίαmanager != nil {
		esp = uint32(uintptr(Pointer(self.διεργασίαmanager.Schedule((*TcpuΚατάσταση)(Pointer(uintptr(esp)))))))

	}
	if !handlerΕκτέλεση && διακοπή == 0x80 {
		esp = χειρολαβήunhandledsyscall(esp)
	}

	if διακοπή <= 0x1F {
	}
	if 0x20 <= διακοπή && διακοπή < 0x30 {
		if 0x28 <= διακοπή {
			ΘύραΕγγραφήbyte(SecondarypicΕντολήioΘύρα, 0x20)
		}
		ΘύραΕγγραφήbyte(PrimarypicΕντολήioΘύρα, 0x20)
	}
	return esp
}

var count2 uint8 = 1

func σύνολοcr3(address uint32)

var console_2 TConsole = TConsole{}

func ΧειρολαβήΔιακοπή(esp uint32, διακοπή uint32) uint32 {

	if διακοπήΔιόρθωση && διακοπή != 0x80 && διακοπή != 0x20 {
		console_2.MΕκτύπωσηxy("[esp:", 1, 21)
		console_2.MUnsignedinteger32Εκτύπωση(uint32(διακοπή))
		console_2.MΕκτύπωση(":")
		console_2.MUnsignedinteger32Εκτύπωση(esp)
	}

	if ΕνεργόΔιακοπήmanager != 0 {
		p := (*TΔιακοπήmanager)(Pointer(ΕνεργόΔιακοπήmanager))
		esp = p.DoΧειρολαβήΔιακοπή(uint8(διακοπή), esp)
		return esp
	}
	if handler_2[διακοπή] != 0 {
		myfunction := (*(*(func(uint32) uint32))(Pointer(handler_2[διακοπή])))
		esp = myfunction(esp)
	}
	if διακοπή == 0x80 {
		return χειρολαβήunhandledsyscall(esp)
	}
	if 0x20 <= διακοπή && διακοπή < 0x30 {
		if 0x28 <= διακοπή {
			ΘύραΕγγραφήbyte(SecondarypicΕντολήioΘύρα, 0x20)
		}
		ΘύραΕγγραφήbyte(PrimarypicΕντολήioΘύρα, 0x20)
	}

	return esp
}

func χειρολαβήunhandledsyscall(esp uint32) uint32 {
	επεξεργαστής := (*TcpuΚατάσταση)(Pointer(uintptr(esp)))
	if επεξεργαστής.Eax == 1 || επεξεργαστής.Eax == 252 {
		επεξεργαστής.Eip = uint32(ValueOf(διακοπήΈξοδοςloop).Pointer())
		επεξεργαστής.Cs = Segkernelcode
		επεξεργαστής.Ds = Segkerneldata
		επεξεργαστής.Es = Segkerneldata
		επεξεργαστής.Fs = Segkerneldata
		επεξεργαστής.Gs = Segkernelgs
		επεξεργαστής.Ss = Segkerneldata
		επεξεργαστής.Eflags = 0x202
	}
	return esp
}

var except uint8 = 0

func exceptionhasΣφάλμαcode(διακοπή uint32) bool {
	switch διακοπή {
	case 0x08, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x11:
		return true
	}
	return false
}

func exceptionΌνομα(διακοπή uint32) string {
	switch διακοπή {
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

func exceptionΠλαίσιοΤιμή(πλαίσιο uint32, offset uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(πλαίσιο + offset)))
}

func exceptioncr0() uint32
func exceptioncr2() uint32
func exceptioncr3() uint32

func εκτύπωσηΣελίδαfaultπληροφορία(σφάλλω uint32) {
	MEmergencyΚαταγραφήΣυμβολοσειρά(" pf=[")
	if (σφάλλω & 0x01) != 0 {
		MEmergencyΚαταγραφήΣυμβολοσειρά("protection")
	} else {
		MEmergencyΚαταγραφήΣυμβολοσειρά("not-present")
	}
	if (σφάλλω & 0x02) != 0 {
		MEmergencyΚαταγραφήΣυμβολοσειρά(",write")
	} else {
		MEmergencyΚαταγραφήΣυμβολοσειρά(",read")
	}
	if (σφάλλω & 0x04) != 0 {
		MEmergencyΚαταγραφήΣυμβολοσειρά(",user")
	} else {
		MEmergencyΚαταγραφήΣυμβολοσειρά(",kernel")
	}
	if (σφάλλω & 0x08) != 0 {
		MEmergencyΚαταγραφήΣυμβολοσειρά(",reserved-bit")
	}
	if (σφάλλω & 0x10) != 0 {
		MEmergencyΚαταγραφήΣυμβολοσειρά(",instruction-fetch")
	}
	MEmergencyΚαταγραφήΣυμβολοσειρά("]")
}

func εκτύπωσηexceptionselectorπληροφορία(σφάλλω uint32) {
	MEmergencyΚαταγραφήΣυμβολοσειρά(" selector=")
	MEmergencyΚαταγραφήunsignedinteger32(σφάλλω & 0xFFFFFFF8)
	MEmergencyΚαταγραφήΣυμβολοσειρά(" index=")
	MEmergencyΚαταγραφήunsignedinteger32(σφάλλω >> 3)
	MEmergencyΚαταγραφήΣυμβολοσειρά(" table=")
	if (σφάλλω & 0x02) != 0 {
		MEmergencyΚαταγραφήΣυμβολοσειρά("IDT")
	} else if (σφάλλω & 0x04) != 0 {
		MEmergencyΚαταγραφήΣυμβολοσειρά("LDT")
	} else {
		MEmergencyΚαταγραφήΣυμβολοσειρά("GDT")
	}
	MEmergencyΚαταγραφήΣυμβολοσειρά(" ext=")
	MEmergencyΚαταγραφήunsignedinteger32(σφάλλω & 0x01)
}

func Χειρολαβήexception(esp uint32, διακοπή uint32) uint32 {
	MEmergencyΚαταγραφήΣυμβολοσειρά("\nEXCEPTION vec=")
	MEmergencyΚαταγραφήhexadecimal8(uint8(διακοπή))
	MEmergencyΚαταγραφήΣυμβολοσειρά(" ")
	MEmergencyΚαταγραφήΣυμβολοσειρά(exceptionΌνομα(διακοπή))
	MEmergencyΚαταγραφήΣυμβολοσειρά(" frame=")
	MEmergencyΚαταγραφήunsignedinteger32(esp)

	if esp < 0x1000 {
		MEmergencyΚαταγραφήΣυμβολοσειρά(" invalid-frame")
		if exceptionhasΣφάλμαcode(διακοπή) {
			MEmergencyΚαταγραφήΣυμβολοσειρά(" raw-error-or-bad-esp=")
			MEmergencyΚαταγραφήunsignedinteger32(esp)
			εκτύπωσηexceptionselectorπληροφορία(esp)
		}
		MEmergencyΚαταγραφήΣυμβολοσειρά("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
		except++
		return esp
	}

	var σφάλλω uint32 = 0
	var eipoffset uint32 = 0
	if exceptionhasΣφάλμαcode(διακοπή) {
		σφάλλω = exceptionΠλαίσιοΤιμή(esp, 0)
		eipoffset = 4
	}
	eip := exceptionΠλαίσιοΤιμή(esp, eipoffset)
	cs := exceptionΠλαίσιοΤιμή(esp, eipoffset+4)
	eflags := exceptionΠλαίσιοΤιμή(esp, eipoffset+8)

	MEmergencyΚαταγραφήΣυμβολοσειρά(" err=")
	MEmergencyΚαταγραφήunsignedinteger32(σφάλλω)
	MEmergencyΚαταγραφήΣυμβολοσειρά(" eip=")
	MEmergencyΚαταγραφήunsignedinteger32(eip)
	MEmergencyΚαταγραφήΣυμβολοσειρά(" cs=")
	MEmergencyΚαταγραφήunsignedinteger32(cs)
	MEmergencyΚαταγραφήΣυμβολοσειρά(" eflags=")
	MEmergencyΚαταγραφήunsignedinteger32(eflags)
	MEmergencyΚαταγραφήΣυμβολοσειρά(" cr0=")
	MEmergencyΚαταγραφήunsignedinteger32(exceptioncr0())
	MEmergencyΚαταγραφήΣυμβολοσειρά(" cr3=")
	MEmergencyΚαταγραφήunsignedinteger32(exceptioncr3())

	if διακοπή == 0x0E {
		MEmergencyΚαταγραφήΣυμβολοσειρά(" cr2=")
		MEmergencyΚαταγραφήunsignedinteger32(exceptioncr2())
		εκτύπωσηΣελίδαfaultπληροφορία(σφάλλω)
	}

	if (cs & 0x03) != 0 {
		MEmergencyΚαταγραφήΣυμβολοσειρά(" useresp=")
		MEmergencyΚαταγραφήunsignedinteger32(exceptionΠλαίσιοΤιμή(esp, eipoffset+12))
		MEmergencyΚαταγραφήΣυμβολοσειρά(" ss=")
		MEmergencyΚαταγραφήunsignedinteger32(exceptionΠλαίσιοΤιμή(esp, eipoffset+16))
	}

	if exceptionhasΣφάλμαcode(διακοπή) {
		εκτύπωσηexceptionselectorπληροφορία(σφάλλω)
	}
	MEmergencyΚαταγραφήΣυμβολοσειρά("\n=== ENGOS HALTED AFTER EXCEPTION ===\n")
	except++

	return esp
}

func haltafterfatalexception()

func ΧειρολαβήfatalΔιακοπήΠλαίσιο(savedesp uint32, διακοπή uint32) uint32 {
	Χειρολαβήexception(savedesp+52, διακοπή)
	haltafterfatalexception()
	return savedesp
}

func ΔιακοπήΕνεργό()
func (self *TΔιακοπήmanager) Ενεργό() {
	if ΕνεργόΔιακοπήmanager != 0 {
		self.Deactive()
	}
	address := uintptr(Pointer(self))
	ΕνεργόΔιακοπήmanager = address
	ΔιακοπήΕνεργό()
}
func Διακοπήdeactive()
func (self *TΔιακοπήmanager) Deactive() {
	ΕνεργόΔιακοπήmanager = 0
	Διακοπήdeactive()
}

func MyΧειρολαβήΔιακοπή(διακοπή uint8, esp uint32) uint32 {
	buffer := []byte("interrupt")
	console_2 := TConsole{}
	console_2.MΕκτύπωση(buffer)
	return esp
}
func MyΔοκιμή(διακοπή uint8, esp uint32)

func UnhandleΔιακοπή() {
	buffer := []byte("unhandle interrupt\n")
	console_2 := TConsole{}
	console_2.MΕκτύπωση(buffer)
}

func διακοπήhandler_2(διακοπή uint8, esp uint32) uint32 {
	buffer := []byte("interrupt\nhandler\nhi")
	console_2 := TConsole{}
	console_2.MΕκτύπωση(buffer)
	console_2.MHexadecimalΕκτύπωση(0x40)
	return esp
}
func εκτύπωσηesp(esp uint32) {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Εκτύπωσηxy(esp, 20, 21)
}
func gettls() uint32
func Εκτύπωσηtls() {

}
