package amdam79c973

import . "unsafe"
import . "διακοπή"
import . "console"
import . "θύρα"
import . "pci"

var δίκτυοΧαρτιάconsole TConsole = TConsole{}

type TInitializationΜπλοκ struct {
	κΑΤΑΣΤΑΣΗ		uint16
	αριθμόςΑποστολήbuffer	uint8
	αριθμόςrecvbuffer	uint8

	physicaladdress	uint64

	λογικήaddress			uint64
	recvbufferΠεριγραφήaddress	uintptr
	αποστολήbufferΠεριγραφήaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	διακόπτες	uint32
	διακόπτες2	uint32
	διαθέσιμα	uint32
}

type IRawdatahandler interface {
	Ενεργήrawdatareceive(dataΔείκτης uintptr, μέγεθος int) bool
	Αποστολή(dataΔείκτης uintptr, μέγεθος uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Σύνολοbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Ενεργήrawdatareceive(dataΔείκτης uintptr, μέγεθος int) bool {
	δίκτυοΧαρτιάconsole.MΕκτύπωσηxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Αποστολή(dataΔείκτης uintptr, μέγεθος uint32) {
	δίκτυοΧαρτιάconsole.MΕκτύπωσηxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Αποστολή(dataΔείκτης, μέγεθος)
}

var Macaddress0Θύρα uint16
var Macaddress2Θύρα uint16
var Macaddress4Θύρα uint16
var registerdataΘύρα uint16
var registeraddressΘύρα uint16
var επαναφοράΘύρα uint16
var busΈλεγχοςregisterdataΘύρα uint16

var initΜπλοκ TInitializationΜπλοκ

var αποστολήbufferΠεριγραφή [8]TBufferdescriptor
var αποστολήbufferΠεριγραφήΜνήμη [2048 + 15]byte
var αποστολήbuffer [2*1024 + 15][8]uint8
var τρέχονΑποστολήbuffer uint8

var recvbufferΠεριγραφή [8]TBufferdescriptor
var recvbufferΠεριγραφήΜνήμη [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var τρέχονrecvbuffer uint8
var funcΤιμή func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TΔιακοπήhandler
	συσκευήdescriptor	TPeripheralcomponentinterconnectΣυσκευήdescriptor
	διακοπή			*TΔιακοπήmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(διακοπή *TΔιακοπήmanager, συσκευήdescriptor TPeripheralcomponentinterconnectΣυσκευήdescriptor, handler IRawdatahandler) {

	self.συσκευήdescriptor = συσκευήdescriptor

	funcΤιμή = (*Tamdam79c973).ΧειρολαβήΔιακοπή
	var address uintptr
	address = uintptr(Pointer(&funcΤιμή))

	self.Init(uint8(0x20+συσκευήdescriptor.Διακοπή), uintptr(Pointer(διακοπή)), address)

	Macaddress0Θύρα = uint16(συσκευήdescriptor.Θύραbase)
	Macaddress2Θύρα = uint16(συσκευήdescriptor.Θύραbase) + 0x02
	Macaddress4Θύρα = uint16(συσκευήdescriptor.Θύραbase) + 0x04
	registerdataΘύρα = uint16(συσκευήdescriptor.Θύραbase) + 0x10
	registeraddressΘύρα = uint16(συσκευήdescriptor.Θύραbase) + 0x12
	επαναφοράΘύρα = uint16(συσκευήdescriptor.Θύραbase) + 0x14
	busΈλεγχοςregisterdataΘύρα = uint16(συσκευήdescriptor.Θύραbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	τρέχονΑποστολήbuffer = 0
	τρέχονrecvbuffer = 0

	var Mac0 uint64 = uint64(ΘύραΑνάγνωσηλέξη(Macaddress0Θύρα) % 256)
	var Mac1 uint64 = uint64(ΘύραΑνάγνωσηλέξη(Macaddress0Θύρα) / 256)
	var Mac2 uint64 = uint64(ΘύραΑνάγνωσηλέξη(Macaddress2Θύρα) % 256)
	var Mac3 uint64 = uint64(ΘύραΑνάγνωσηλέξη(Macaddress2Θύρα) / 256)
	var Mac4 uint64 = uint64(ΘύραΑνάγνωσηλέξη(Macaddress4Θύρα) % 256)
	var Mac5 uint64 = uint64(ΘύραΑνάγνωσηλέξη(Macaddress4Θύρα) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MΕκτύπωσηxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalΕκτύπωση(uint8(συσκευήdescriptor.Διακοπή))
	console_2.MΕκτύπωση(([]byte)("]"))
	console_2.MΕκτύπωση(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16Εκτύπωση(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32Εκτύπωση(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MΕκτύπωση(([]byte)("]"))

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 20)
	ΘύραΕγγραφήλέξη(busΈλεγχοςregisterdataΘύρα, 0x102)

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 0)
	ΘύραΕγγραφήλέξη(registerdataΘύρα, 0x04)

	initΜπλοκ.κΑΤΑΣΤΑΣΗ = 0x0000
	initΜπλοκ.αριθμόςΑποστολήbuffer = 3
	initΜπλοκ.αριθμόςrecvbuffer = 3

	initΜπλοκ.physicaladdress = Mac

	initΜπλοκ.λογικήaddress = 0

	αποστολήbufferΠεριγραφή = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&αποστολήbufferΠεριγραφήΜνήμη)) + 15) & ^(uintptr)(0xF)))
	initΜπλοκ.αποστολήbufferΠεριγραφήaddress = uintptr(Pointer(&αποστολήbufferΠεριγραφή))
	recvbufferΠεριγραφή = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferΠεριγραφήΜνήμη)) + 15) & ^(uintptr)(0xF)))
	initΜπλοκ.recvbufferΠεριγραφήaddress = uintptr(Pointer(&recvbufferΠεριγραφή))

	for i := 0; i < 8; i++ {
		αποστολήbufferΠεριγραφή[i].address_2 = uint32((uintptr(Pointer(&αποστολήbuffer[i])) + 15) & ^(uintptr(0xF)))
		αποστολήbufferΠεριγραφή[i].διακόπτες = 0x7FF | 0xF000
		αποστολήbufferΠεριγραφή[i].διακόπτες2 = 0
		αποστολήbufferΠεριγραφή[i].διαθέσιμα = 0

		recvbufferΠεριγραφή[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferΠεριγραφή[i].διακόπτες = 0xF7FF | 0x80000000

	}

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 1)
	ΘύραΕγγραφήλέξη(registerdataΘύρα, uint16(uintptr(Pointer(&initΜπλοκ))&0xFFFF))

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 2)
	ΘύραΕγγραφήλέξη(registerdataΘύρα, uint16((uintptr(Pointer(&initΜπλοκ))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Ενεργοποίηση() {
	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 0)
	ΘύραΕγγραφήλέξη(registerdataΘύρα, 0x41)

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 4)
	temporary := ΘύραΑνάγνωσηλέξη(registerdataΘύρα)
	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 4)
	ΘύραΕγγραφήλέξη(registerdataΘύρα, temporary|0xC00)

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 0)
	ΘύραΕγγραφήλέξη(registerdataΘύρα, 0x42)

}
func (self *Tamdam79c973) Επαναφορά() int {
	ΘύραΑνάγνωσηλέξη(επαναφοράΘύρα)
	ΘύραΕγγραφήλέξη(επαναφοράΘύρα, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) ΧειρολαβήΔιακοπή(esp uint32) uint32 {

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 0)
	temporary := uint32(ΘύραΑνάγνωσηλέξη(registerdataΘύρα))
	console_2.MΕκτύπωση(([]byte)("interrupt("))
	console_2.MUnsignedinteger32Εκτύπωση(esp)
	console_2.MΕκτύπωση(([]byte)(":"))
	console_2.MUnsignedinteger32Εκτύπωση(temporary)
	console_2.MΕκτύπωση(([]byte)(":"))
	console_2.MUnsignedinteger16Εκτύπωση(count)
	count++
	console_2.MΕκτύπωση(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MΕκτύπωση(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MΕκτύπωση(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MΕκτύπωση(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MΕκτύπωση(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MΕκτύπωση(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MΕκτύπωση(([]byte)("am79c973 data sent"))
	}

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 0)
	ΘύραΕγγραφήλέξη(registerdataΘύρα, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MΕκτύπωση(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Αποστολή(dataΔείκτης uintptr, μέγεθος uint32) {
	var αποστολήdescriptor uint16 = uint16(τρέχονΑποστολήbuffer)
	τρέχονΑποστολήbuffer = 0

	if μέγεθος > 1518 {
		μέγεθος = 1518
	}

	var πηγή_2 [4096]byte = *(*([4096]byte))(Pointer(dataΔείκτης))
	var προορισμός_2 uint32 = αποστολήbufferΠεριγραφή[αποστολήdescriptor].address_2 + μέγεθος - 1

	for i := 0; i < int(μέγεθος); i++ {

		*(*byte)(Pointer(uintptr(προορισμός_2))) = πηγή_2[int(μέγεθος)-i-1]

		προορισμός_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataΔείκτης))
	console_2.MΕκτύπωσηxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalΕκτύπωση(data[i])
		console_2.MΕκτύπωση(([]byte)(":"))
	}
	console_2.MΕκτύπωση(([]byte)("\n"))

	αποστολήbufferΠεριγραφή[αποστολήdescriptor].διαθέσιμα = 0
	αποστολήbufferΠεριγραφή[αποστολήdescriptor].διακόπτες2 = 0
	αποστολήbufferΠεριγραφή[αποστολήdescriptor].διακόπτες = 0x8300F000 | uint32((-μέγεθος)&0xFFF)

	ΘύραΕγγραφήλέξη(registeraddressΘύρα, 0)
	ΘύραΕγγραφήλέξη(registerdataΘύρα, 0x48)

}
func (self *Tamdam79c973) Receive() {
	console_2.MΕκτύπωση(([]byte)(":"))
	console_2.MUnsignedinteger32Εκτύπωση(uint32(uintptr(Pointer(&αποστολήbuffer))))
	console_2.MΕκτύπωση(([]byte)(":"))
	console_2.MHexadecimalΕκτύπωση(αποστολήbuffer[0][0])
	console_2.MHexadecimalΕκτύπωση(αποστολήbuffer[0][1])
	console_2.MΕκτύπωση(([]byte)(":"))
	τρέχονrecvbuffer = 0

	for ; (recvbufferΠεριγραφή[τρέχονrecvbuffer].διακόπτες & 0x80000000) == 0; τρέχονrecvbuffer = (τρέχονrecvbuffer + 1) % 8 {

		if !(recvbufferΠεριγραφή[τρέχονrecvbuffer].διακόπτες&0x40000000 != 0) && ((recvbufferΠεριγραφή[τρέχονrecvbuffer].διακόπτες & 0x03000000) == 0x03000000) {
			var μέγεθος uint32 = recvbufferΠεριγραφή[τρέχονrecvbuffer].διακόπτες & 0xFFF
			if μέγεθος > 64 {
				μέγεθος -= 4
			}

			console_2.MΕκτύπωση([]byte(" size : ["))
			console_2.MUnsignedinteger32Εκτύπωση(μέγεθος)
			console_2.MΕκτύπωση([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferΠεριγραφή[τρέχονrecvbuffer].address_2)))
			var δείκτης uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Ενεργήrawdatareceive(δείκτης, int(μέγεθος)) {

					console_2.MΕκτύπωσηxy(([]byte)("self.Send"), 0, 22)

					self.Αποστολή(δείκτης, μέγεθος)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalΕκτύπωση(buffer_2[i])
				console_2.MΕκτύπωση([]byte(":"))
			}

		}
		recvbufferΠεριγραφή[τρέχονrecvbuffer].διακόπτες2 = 0
		recvbufferΠεριγραφή[τρέχονrecvbuffer].διακόπτες = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Σύνολοhandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initΜπλοκ.physicaladdress
}
func (self *Tamdam79c973) Σύνολοipaddress(ip uint64) {
	initΜπλοκ.λογικήaddress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initΜπλοκ.λογικήaddress
}
