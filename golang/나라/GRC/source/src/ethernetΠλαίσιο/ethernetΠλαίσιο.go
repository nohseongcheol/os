package ethernetΠλαίσιο

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetΠλαίσιοheaderbuffer struct {
	προορισμόςmacbe	[6]byte
	πηγήmacbe	[6]byte
	ethernetΤύποςbe	[2]byte
}

var πλαίσιοheaderΜέγεθος int = 14

type TEthernetΠλαίσιοheader struct {
	προορισμόςmacbe	uint64
	πηγήmacbe	uint64
	ethernetΤύποςbe	uint16
}

func (self *TEthernetΠλαίσιοheader) Init(buffer_2 TEthernetΠλαίσιοheaderbuffer) {
	self.προορισμόςmacbe = (Διάταξηtounsignedinteger48(buffer_2.προορισμόςmacbe))
	self.πηγήmacbe = (Διάταξηtounsignedinteger48(buffer_2.πηγήmacbe))
	self.ethernetΤύποςbe = (Διάταξηtounsignedinteger16(buffer_2.ethernetΤύποςbe))

}
func (self *TEthernetΠλαίσιοheader) Σύνολοbuffer(buffer_2 *TEthernetΠλαίσιοheaderbuffer) {
	buffer_2.προορισμόςmacbe = Unsignedinteger48toΔιάταξη(Unsignedinteger48r(self.προορισμόςmacbe))
	buffer_2.πηγήmacbe = Unsignedinteger48toΔιάταξη(Unsignedinteger48r(self.πηγήmacbe))
	buffer_2.ethernetΤύποςbe = Unsignedinteger16toΔιάταξη(Unsignedinteger16r(self.ethernetΤύποςbe))
}

type IEthernetΠλαίσιοhandler interface {
	Init(backend TEthernetΠλαίσιοprovider)
	Σύνολοhandler(handler IEthernetΠλαίσιοhandler, ethernetΤύπος uint16)
	EthernetΠλαίσιοreceivewhen(dataΔείκτης uintptr, μέγεθος int) bool
	Αποστολή(προορισμόςmacbe uint64, dataΔείκτης uintptr, μέγεθος uint32)
	ΠλαίσιοΑποστολή(προορισμόςmacbe uint64, ethernetΤύποςbe uint16, dataΔείκτης uintptr, μέγεθος uint32)
	Providerget() TEthernetΠλαίσιοprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetΠλαίσιοhandler struct {
}

var πλαίσιο TEthernetΠλαίσιοheader
var Backend TEthernetΠλαίσιοprovider
var handler_2 [65535]IEthernetΠλαίσιοhandler
var efhandler *TEthernetΠλαίσιοhandler = nil

func (self *TEthernetΠλαίσιοhandler) Init(backend TEthernetΠλαίσιοprovider) {
	Backend = backend
}

func (self *TEthernetΠλαίσιοhandler) Σύνολοhandler(handler IEthernetΠλαίσιοhandler, pethernetΤύπος uint16) {
	handler_2[pethernetΤύπος] = handler
}
func (self *TEthernetΠλαίσιοhandler) Σύνολοbackend(backend TEthernetΠλαίσιοprovider) {
	Backend = backend
}
func (self *TEthernetΠλαίσιοhandler) Getbackend() TEthernetΠλαίσιοprovider {
	return Backend
}
func (self *TEthernetΠλαίσιοhandler) EthernetΠλαίσιοreceivewhen(dataΔείκτης uintptr, μέγεθος int) bool {
	ethernetconsole.MΕκτύπωση(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEthernetΠλαίσιοhandler) Αποστολή(προορισμόςmacbe uint64, dataΔείκτης uintptr, μέγεθος uint32) {
	Backend.ΠλαίσιοΑποστολή(προορισμόςmacbe, πλαίσιο.ethernetΤύποςbe, dataΔείκτης, μέγεθος)
}
func (self *TEthernetΠλαίσιοhandler) ΠλαίσιοΑποστολή(προορισμόςmacbe uint64, ethernetΤύποςbe uint16, dataΔείκτης uintptr, μέγεθος uint32) {
	Backend.ΠλαίσιοΑποστολή(προορισμόςmacbe, ethernetΤύποςbe, dataΔείκτης, μέγεθος)
}
func (self *TEthernetΠλαίσιοhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEthernetΠλαίσιοhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEthernetΠλαίσιοhandler) Providerget() TEthernetΠλαίσιοprovider {
	return Backend
}

type TEthernetΠλαίσιοrawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetΠλαίσιοprovider

func (self *TEthernetΠλαίσιοrawdatahandler) Init(pprovider TEthernetΠλαίσιοprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEthernetΠλαίσιοrawdatahandler) Ενεργήrawdatareceive(dataΔείκτης uintptr, μέγεθος int) bool {
	return provider.Ενεργήrawdatareceive(dataΔείκτης, μέγεθος)
}
func (self *TEthernetΠλαίσιοrawdatahandler) Αποστολή(dataΔείκτης uintptr, μέγεθος uint32) {
	provider.Αποστολή(dataΔείκτης, μέγεθος)
}
func (self *TEthernetΠλαίσιοrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEthernetΠλαίσιοrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEthernetΠλαίσιοrawdatahandler) Providerget() TEthernetΠλαίσιοprovider {
	return provider
}

type TEthernetΠλαίσιοprovider struct {
	δίκτυοΧαρτιά	Tamdam79c973
	handler_2	[65565]IEthernetΠλαίσιοhandler
}

func (self *TEthernetΠλαίσιοprovider) Init(backend Tamdam79c973) {

	self.δίκτυοΧαρτιά = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TEthernetΠλαίσιοprovider) Ενεργήrawdatareceive(dataΔείκτης uintptr, μέγεθος int) bool {

	var buffer_2 *TEthernetΠλαίσιοheaderbuffer = (*TEthernetΠλαίσιοheaderbuffer)(Pointer(dataΔείκτης))
	var πλαίσιο TEthernetΠλαίσιοheader = TEthernetΠλαίσιοheader{}
	πλαίσιο.Init(*buffer_2)
	var reply bool = false

	if πλαίσιο.προορισμόςmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(πλαίσιο.προορισμόςmacbe) == self.Getmacaddress() {
		if handler_2[πλαίσιο.ethernetΤύποςbe] != nil {
			ethernetconsole.MΕκτύπωση(([]byte)("provider\n"))

			var δείκτης uintptr = uintptr(Pointer(dataΔείκτης)) + uintptr(πλαίσιοheaderΜέγεθος)
			reply = handler_2[πλαίσιο.ethernetΤύποςbe].EthernetΠλαίσιοreceivewhen(δείκτης, μέγεθος-πλαίσιοheaderΜέγεθος)

		}
	}

	if reply {
		πλαίσιο.προορισμόςmacbe = πλαίσιο.πηγήmacbe
		πλαίσιο.πηγήmacbe = Unsignedinteger48r(self.Getmacaddress())
		πλαίσιο.Σύνολοbuffer(buffer_2)

	}

	ethernetconsole.MΕκτύπωσηxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Εκτύπωση(πλαίσιο.πηγήmacbe)
	ethernetconsole.MΕκτύπωση(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Εκτύπωση(πλαίσιο.προορισμόςmacbe)
	ethernetconsole.MΕκτύπωση(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Εκτύπωση(self.Getmacaddress())
	ethernetconsole.MΕκτύπωση(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Εκτύπωση(πλαίσιο.ethernetΤύποςbe)
	ethernetconsole.MΕκτύπωση(([]byte)("]"))

	return reply

}
func (self *TEthernetΠλαίσιοprovider) Αποστολή(dataΔείκτης uintptr, μέγεθος uint32) {
	self.δίκτυοΧαρτιά.Αποστολή(dataΔείκτης, μέγεθος)
}
func (self *TEthernetΠλαίσιοprovider) ΠλαίσιοΑποστολή(προορισμόςmacbe uint64, ethernetΤύποςbe uint16, dataΔείκτης uintptr, μέγεθος uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetΠλαίσιοheaderbuffer = (*TEthernetΠλαίσιοheaderbuffer)(Pointer(&buffer2_2))

	var πλαίσιο TEthernetΠλαίσιοheader = TEthernetΠλαίσιοheader{}
	πλαίσιο.Init(*buffer_2)

	πλαίσιο.προορισμόςmacbe = Unsignedinteger48r(προορισμόςmacbe)
	πλαίσιο.πηγήmacbe = Unsignedinteger48r(self.δίκτυοΧαρτιά.Getmacaddress())
	πλαίσιο.ethernetΤύποςbe = Unsignedinteger16r(ethernetΤύποςbe)

	πλαίσιο.Σύνολοbuffer(buffer_2)
	var πηγή_2 [4096]byte = *(*([4096]byte))(Pointer(dataΔείκτης))

	var i uint32 = 0
	for i = 0; i < μέγεθος; i++ {
		buffer2_2[uint32(πλαίσιοheaderΜέγεθος)+i] = πηγή_2[i]

	}

	var δείκτης uintptr = uintptr(Pointer(&buffer2_2))

	self.δίκτυοΧαρτιά.Αποστολή(δείκτης, μέγεθος+uint32(πλαίσιοheaderΜέγεθος))

}
func (self *TEthernetΠλαίσιοprovider) Getmacaddress() uint64 {
	return self.δίκτυοΧαρτιά.Getmacaddress()
}
func (self *TEthernetΠλαίσιοprovider) Getipaddress() uint64 {
	return self.δίκτυοΧαρτιά.Getipaddress()
}
