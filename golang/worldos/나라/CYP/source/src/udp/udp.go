/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "μνήμηmanager"
import . "ipv4"

var udpconsole = TConsole{}

type TΧρήστηςdatagramprotocolheaderbuffer struct {
	πηγήΘύραΑριθμός		[2]byte
	προορισμόςΘύραΑριθμός	[2]byte

	διάρκεια	[2]byte
	checksum	[2]byte
}

var udpheaderΜέγεθος uint32 = 8

type TΧρήστηςdatagramprotocolheader struct {
	πηγήΘύραΑριθμός		uint16
	προορισμόςΘύραΑριθμός	uint16

	διάρκεια	uint16
	checksum	uint16
}

func (self *TΧρήστηςdatagramprotocolheader) Init(buffer_2 *TΧρήστηςdatagramprotocolheaderbuffer) {
	self.πηγήΘύραΑριθμός = Διάταξηtounsignedinteger16(buffer_2.πηγήΘύραΑριθμός)
	self.προορισμόςΘύραΑριθμός = Διάταξηtounsignedinteger16(buffer_2.προορισμόςΘύραΑριθμός)

	self.διάρκεια = Διάταξηtounsignedinteger16(buffer_2.διάρκεια)
	self.checksum = Διάταξηtounsignedinteger16(buffer_2.checksum)
}
func (self *TΧρήστηςdatagramprotocolheader) Σύνολοbuffer(buffer_2 *TΧρήστηςdatagramprotocolheaderbuffer) {

	buffer_2.πηγήΘύραΑριθμός = Unsignedinteger16toΔιάταξη(self.πηγήΘύραΑριθμός)
	buffer_2.προορισμόςΘύραΑριθμός = Unsignedinteger16toΔιάταξη(self.προορισμόςΘύραΑριθμός)

	buffer_2.διάρκεια = Unsignedinteger16toΔιάταξη(self.διάρκεια)
	buffer_2.checksum = Unsignedinteger16toΔιάταξη(self.checksum)

}

type IΧρήστηςdatagramprotocolhandler interface {
	ΧειρολαβήΧρήστηςdatagramprotocolΜήνυμα(υποδοχή *TΧρήστηςdatagramprotocolΥποδοχή, data uintptr, μέγεθος uint16)
}

type TΧρήστηςdatagramprotocolhandler struct {
}

func (self *TΧρήστηςdatagramprotocolhandler) Init(backend TΔιαδίκτυοprotocolprovider) {
}
func (self *TΧρήστηςdatagramprotocolhandler) ΧειρολαβήΧρήστηςdatagramprotocolΜήνυμα(υποδοχή *TΧρήστηςdatagramprotocolΥποδοχή, data uintptr, μέγεθος uint16) {
}

type IΧρήστηςdatagramprotocolΥποδοχή interface {
	ΧειρολαβήΧρήστηςdatagramprotocolΜήνυμα(data uintptr, μέγεθος uint16)
}
type TΧρήστηςdatagramprotocolΥποδοχή struct {
	απομακρυσμένοΘύραΑριθμός	uint16
	απομακρυσμένοip			uint32
	τοπικόΘύραΑριθμός		uint16
	τοπικόip			uint32

	listening	bool
}

var udpprovider TΧρήστηςdatagramprotocolprovider
var udphandler IΧρήστηςdatagramprotocolhandler

func (self *TΧρήστηςdatagramprotocolΥποδοχή) Δοκιμή() {
}
func (self *TΧρήστηςdatagramprotocolΥποδοχή) Init(pudpprovider TΧρήστηςdatagramprotocolprovider, pudphandler IΧρήστηςdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TΧρήστηςdatagramprotocolΥποδοχή) ΧειρολαβήΧρήστηςdatagramprotocolΜήνυμα(data uintptr, μέγεθος uint16) {
	if udphandler != nil {
		udphandler.ΧειρολαβήΧρήστηςdatagramprotocolΜήνυμα(self, data, μέγεθος)
	}
}
func (self *TΧρήστηςdatagramprotocolΥποδοχή) Αποστολή(pdata []byte, μέγεθος uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(μέγεθος); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Αποστολή(self, data, μέγεθος)
}
func (self *TΧρήστηςdatagramprotocolΥποδοχή) Αποσύνδεση() {
	udpprovider.Αποσύνδεση(self)
}

type TΧρήστηςdatagramprotocolprovider struct {
}

var iphandler IΔιαδίκτυοprotocolhandler
var sockets [65535]TΧρήστηςdatagramprotocolΥποδοχή
var αριθμόςsockets int
var ελεύθεραΘύρα uint16

func (self *TΧρήστηςdatagramprotocolprovider) Init(pipprovider TΔιαδίκτυοprotocolprovider, piphandler IΔιαδίκτυοprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	αριθμόςsockets = 0
	ελεύθεραΘύρα = 1024
}
func (self *TΧρήστηςdatagramprotocolprovider) Διαδίκτυοprotocolreceivewhen(πηγήipaddressΔίκτυοbyteorder uint32, προορισμόςipaddressΔίκτυοbyteorder uint32, διαδίκτυοprotocolpayload uintptr, μέγεθος uint32) bool {
	if μέγεθος < udpheaderΜέγεθος {
		return false
	}

	var buffer_2 *TΧρήστηςdatagramprotocolheaderbuffer = (*TΧρήστηςdatagramprotocolheaderbuffer)(Pointer(διαδίκτυοprotocolpayload))
	var msg TΧρήστηςdatagramprotocolheader
	msg.Init(buffer_2)

	var υποδοχή *TΧρήστηςdatagramprotocolΥποδοχή = nil

	for i := 0; i < αριθμόςsockets && υποδοχή == nil; i++ {
		if sockets[i].τοπικόΘύραΑριθμός == msg.προορισμόςΘύραΑριθμός && sockets[i].τοπικόip == προορισμόςipaddressΔίκτυοbyteorder && sockets[i].listening == true {
			υποδοχή = &sockets[i]
			υποδοχή.listening = false
			υποδοχή.απομακρυσμένοΘύραΑριθμός = msg.πηγήΘύραΑριθμός
			υποδοχή.απομακρυσμένοip = πηγήipaddressΔίκτυοbyteorder
		} else if sockets[i].τοπικόΘύραΑριθμός == msg.προορισμόςΘύραΑριθμός && sockets[i].τοπικόip == προορισμόςipaddressΔίκτυοbyteorder && sockets[i].απομακρυσμένοΘύραΑριθμός == msg.πηγήΘύραΑριθμός && sockets[i].απομακρυσμένοip == πηγήipaddressΔίκτυοbyteorder {
			υποδοχή = &sockets[i]

		}
	}

	msg.Σύνολοbuffer(buffer_2)
	if υποδοχή != nil {
		υποδοχή.ΧειρολαβήΧρήστηςdatagramprotocolΜήνυμα(διαδίκτυοprotocolpayload+uintptr(udpheaderΜέγεθος), uint16(μέγεθος-udpheaderΜέγεθος))
	}

	return false
}

func (self *TΧρήστηςdatagramprotocolprovider) Σύνδεση(ip uint32, θύρα uint16) *TΧρήστηςdatagramprotocolΥποδοχή {
	var μνήμηmanager = &TΜνήμηmanager{}
	var υποδοχή = (*TΧρήστηςdatagramprotocolΥποδοχή)(μνήμηmanager.Malloc(50))

	if υποδοχή != nil {

		υποδοχή.Init(*self, nil)
		υποδοχή.απομακρυσμένοΘύραΑριθμός = θύρα
		υποδοχή.απομακρυσμένοip = ip
		υποδοχή.τοπικόΘύραΑριθμός = ελεύθεραΘύρα
		ελεύθεραΘύρα++
		υποδοχή.τοπικόip = uint32((*iphandler.Providerget()).Getipaddress())

		υποδοχή.απομακρυσμένοΘύραΑριθμός = Unsignedinteger16r(υποδοχή.απομακρυσμένοΘύραΑριθμός)
		υποδοχή.τοπικόΘύραΑριθμός = Unsignedinteger16r(υποδοχή.τοπικόΘύραΑριθμός)

		sockets[αριθμόςsockets] = *υποδοχή
		αριθμόςsockets++

	}
	return υποδοχή

}
func (self *TΧρήστηςdatagramprotocolprovider) Listen(θύρα uint16) *TΧρήστηςdatagramprotocolΥποδοχή {
	var υποδοχή = &TΧρήστηςdatagramprotocolΥποδοχή{}
	υποδοχή = nil
	if υποδοχή != nil {
		υποδοχή.Init(*self, nil)
		υποδοχή.listening = true
		υποδοχή.τοπικόΘύραΑριθμός = θύρα
		υποδοχή.τοπικόip = uint32((*iphandler.Providerget()).Getipaddress())

		υποδοχή.τοπικόΘύραΑριθμός = Unsignedinteger16r(υποδοχή.τοπικόΘύραΑριθμός)
	}
	return υποδοχή
}
func (self *TΧρήστηςdatagramprotocolprovider) Αποσύνδεση(υποδοχή *TΧρήστηςdatagramprotocolΥποδοχή) {
	for i := 0; i < αριθμόςsockets && υποδοχή == nil; i++ {
		if sockets[i] == *υποδοχή {
			αριθμόςsockets--
			sockets[i] = sockets[αριθμόςsockets]
			break
		}
	}
}
func (self *TΧρήστηςdatagramprotocolprovider) Αποστολή(υποδοχή *TΧρήστηςdatagramprotocolΥποδοχή, pdata uintptr, μέγεθος uint16) {
	var σύνολοΔιάρκεια = uint32(μέγεθος) + udpheaderΜέγεθος

	var buffer_2 [4096]byte

	var msgbuffer = (*TΧρήστηςdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TΧρήστηςdatagramprotocolheader{}

	msg.πηγήΘύραΑριθμός = υποδοχή.τοπικόΘύραΑριθμός
	msg.προορισμόςΘύραΑριθμός = υποδοχή.απομακρυσμένοΘύραΑριθμός
	msg.διάρκεια = Unsignedinteger16r(uint16(σύνολοΔιάρκεια))

	msg.checksum = 0x0
	msg.Σύνολοbuffer(msgbuffer)

	var databytes [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(μέγεθος); i++ {
		buffer_2[int(udpheaderΜέγεθος)+i] = databytes[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Αποστολή(υποδοχή.απομακρυσμένοip, 0x11, data, σύνολοΔιάρκεια)

}
func (self *TΧρήστηςdatagramprotocolprovider) Bind(υποδοχή *TΧρήστηςdatagramprotocolΥποδοχή, handler *TΧρήστηςdatagramprotocolhandler,) {
}
