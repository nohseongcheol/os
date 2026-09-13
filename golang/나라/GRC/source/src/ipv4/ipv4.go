package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetΠλαίσιο"
import . "arp"

var ipconsole TConsole = TConsole{}

type TΔιαδίκτυοprotocolv4Μήνυμαbuffer struct {
	lenver		byte
	tos		byte
	σύνολοΔιάρκεια	[2]byte

	ident			[2]byte
	διακόπτεςΚΑΙoffset	[2]byte

	ώραtolive	byte
	protocol	byte
	checksum	[2]byte

	πηγήipaddress		[4]byte
	προορισμόςipaddress	[4]byte
}

var ipΜέγεθος uint8 = (4 + 4 + 4 + 8)

type TΔιαδίκτυοprotocolv4Μήνυμα struct {
	headerΔιάρκεια	uint8
	έκδοση		uint8
	tos		uint8
	σύνολοΔιάρκεια	uint16

	ident			uint16
	διακόπτεςΚΑΙoffset	uint16

	ώραtolive	uint8
	protocol	uint8
	checksum	uint16

	πηγήipaddress		uint32
	προορισμόςipaddress	uint32
}

func (self *TΔιαδίκτυοprotocolv4Μήνυμα) Init(buffer_2 TΔιαδίκτυοprotocolv4Μήνυμαbuffer) {

	self.έκδοση = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerΔιάρκεια = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.σύνολοΔιάρκεια = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer_2.σύνολοΔιάρκεια))

	self.ident = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer_2.ident))
	self.διακόπτεςΚΑΙoffset = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer_2.διακόπτεςΚΑΙoffset))

	self.ώραtolive = buffer_2.ώραtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer_2.checksum))

	self.πηγήipaddress = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer_2.πηγήipaddress))
	self.προορισμόςipaddress = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer_2.προορισμόςipaddress))

}
func (self *TΔιαδίκτυοprotocolv4Μήνυμα) Σύνολοbuffer(buffer_2 *TΔιαδίκτυοprotocolv4Μήνυμαbuffer) {

	buffer_2.lenver = byte(((self.έκδοση & 0x0F) << 4) | (self.headerΔιάρκεια & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.σύνολοΔιάρκεια = Unsignedinteger16toΔιάταξη(self.σύνολοΔιάρκεια)

	buffer_2.ident = Unsignedinteger16toΔιάταξη(self.ident)
	buffer_2.διακόπτεςΚΑΙoffset = Unsignedinteger16toΔιάταξη(self.διακόπτεςΚΑΙoffset)

	buffer_2.ώραtolive = self.ώραtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toΔιάταξη(self.checksum)

	buffer_2.πηγήipaddress = Unsignedinteger32toΔιάταξη(self.πηγήipaddress)
	buffer_2.προορισμόςipaddress = Unsignedinteger32toΔιάταξη(self.προορισμόςipaddress)

}

type IΔιαδίκτυοprotocolhandler interface {
	Init(backend TΔιαδίκτυοprotocolprovider, pihandler IΔιαδίκτυοprotocolhandler, pprotocol uint8)
	Διαδίκτυοprotocolreceivewhen(πηγήipaddressΔίκτυοbyteorder uint32, προορισμόςipaddressΔίκτυοbyteorder uint32, dataΔείκτης uintptr, μέγεθος uint32) bool
	Αποστολή(προορισμόςipaddressΔίκτυοbyteorder uint32, pprotocol uint8, dataΔείκτης uintptr, μέγεθος uint32)
	Providerget() *TΔιαδίκτυοprotocolprovider
}

type TΔιαδίκτυοprotocolhandler struct {
}

var ipethernetΠλαίσιοhandler IpethernetΠλαίσιοhandler = IpethernetΠλαίσιοhandler{}
var protocol uint8

func (self *TΔιαδίκτυοprotocolhandler) Init(backend TΔιαδίκτυοprotocolprovider, pihandler IΔιαδίκτυοprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TΔιαδίκτυοprotocolhandler) Διαδίκτυοprotocolreceivewhen(πηγήipaddressΔίκτυοbyteorder uint32, προορισμόςipaddressΔίκτυοbyteorder uint32, dataΔείκτης uintptr, μέγεθος uint32) bool {
	ipconsole.MΕκτύπωση(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TΔιαδίκτυοprotocolhandler) Αποστολή(προορισμόςipaddressΔίκτυοbyteorder uint32, pprotocol uint8, dataΔείκτης uintptr, μέγεθος uint32) {

	ipprovider.Αποστολή(προορισμόςipaddressΔίκτυοbyteorder, pprotocol, dataΔείκτης, μέγεθος)
}
func (self *TΔιαδίκτυοprotocolhandler) Providerget() *TΔιαδίκτυοprotocolprovider {
	return &ipprovider
}

type IpethernetΠλαίσιοhandler struct {
	TEthernetΠλαίσιοhandler
}

var ipprovider TΔιαδίκτυοprotocolprovider

func (self *IpethernetΠλαίσιοhandler) EthernetΠλαίσιοreceivewhen(dataΔείκτης uintptr, μέγεθος int) bool {
	ipconsole.MΕκτύπωση(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetΠλαίσιοreceivewhen(dataΔείκτης, uint32(μέγεθος))

}

func (self *IpethernetΠλαίσιοhandler) Αποστολή(προορισμόςipaddressΔίκτυοbyteorder uint64, dataΔείκτης uintptr, μέγεθος uint32) {
	ipconsole.MΕκτύπωση(([]byte)("ipefhandler:send\n"))
	var ethernetΤύποςbe = Unsignedinteger16r(0x0800)
	self.TEthernetΠλαίσιοhandler.ΠλαίσιοΑποστολή(προορισμόςipaddressΔίκτυοbyteorder, ethernetΤύποςbe, dataΔείκτης, μέγεθος)

}

var handler_2 [255]IΔιαδίκτυοprotocolhandler

type TΔιαδίκτυοprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetΜάσκα	uint32
}

var efhandler IEthernetΠλαίσιοhandler

func (self *TΔιαδίκτυοprotocolprovider) Init(pefprovider TEthernetΠλαίσιοprovider, pefhandler IEthernetΠλαίσιοhandler, arp Arpprovider, gatewayip uint32, subnetΜάσκα uint32) {

	efhandler = pefhandler
	efhandler.Σύνολοhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.SubnetΜάσκα = subnetΜάσκα
	ipprovider = *self
}
func (self *TΔιαδίκτυοprotocolprovider) EthernetΠλαίσιοreceivewhen(ethernetΠλαίσιοpayload uintptr, μέγεθος uint32) bool {
	if μέγεθος < uint32(ipΜέγεθος) {
		return false
	}

	var buffer_2 *TΔιαδίκτυοprotocolv4Μήνυμαbuffer = (*TΔιαδίκτυοprotocolv4Μήνυμαbuffer)(Pointer(ethernetΠλαίσιοpayload))
	var διαδίκτυοprotocolΜήνυμα TΔιαδίκτυοprotocolv4Μήνυμα
	διαδίκτυοprotocolΜήνυμα.Init(*buffer_2)

	var reply bool = false

	if διαδίκτυοprotocolΜήνυμα.προορισμόςipaddress == uint32(efhandler.Getipaddress()) {

		var διάρκεια uint32 = uint32(διαδίκτυοprotocolΜήνυμα.σύνολοΔιάρκεια)
		if διάρκεια > μέγεθος {
			διάρκεια = μέγεθος
		}
		if handler_2[διαδίκτυοprotocolΜήνυμα.protocol] != nil {
			reply = handler_2[διαδίκτυοprotocolΜήνυμα.protocol].Διαδίκτυοprotocolreceivewhen(διαδίκτυοprotocolΜήνυμα.πηγήipaddress, διαδίκτυοprotocolΜήνυμα.προορισμόςipaddress, ethernetΠλαίσιοpayload+uintptr(4*διαδίκτυοprotocolΜήνυμα.headerΔιάρκεια), uint32(διάρκεια-uint32(4*διαδίκτυοprotocolΜήνυμα.headerΔιάρκεια)))

		}
	}

	if reply {

		var temporary = διαδίκτυοprotocolΜήνυμα.προορισμόςipaddress
		διαδίκτυοprotocolΜήνυμα.προορισμόςipaddress = διαδίκτυοprotocolΜήνυμα.πηγήipaddress
		διαδίκτυοprotocolΜήνυμα.πηγήipaddress = temporary

		διαδίκτυοprotocolΜήνυμα.ώραtolive = 0x40
		διαδίκτυοprotocolΜήνυμα.checksum = 0

		διαδίκτυοprotocolΜήνυμα.Σύνολοbuffer(buffer_2)
		διαδίκτυοprotocolΜήνυμα.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetΠλαίσιοpayload)), uint32(4*διαδίκτυοprotocolΜήνυμα.headerΔιάρκεια))

		διαδίκτυοprotocolΜήνυμα.Σύνολοbuffer(buffer_2)

	}

	ipconsole.MΕκτύπωση(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Εκτύπωση(διαδίκτυοprotocolΜήνυμα.πηγήipaddress)
	ipconsole.MΕκτύπωση(([]byte)(":"))
	ipconsole.MUnsignedinteger32Εκτύπωση(διαδίκτυοprotocolΜήνυμα.προορισμόςipaddress)
	ipconsole.MΕκτύπωση(([]byte)(":"))
	ipconsole.MUnsignedinteger16Εκτύπωση(uint16(διαδίκτυοprotocolΜήνυμα.headerΔιάρκεια))
	ipconsole.MΕκτύπωση(([]byte)(":"))
	ipconsole.MUnsignedinteger16Εκτύπωση(uint16(διαδίκτυοprotocolΜήνυμα.έκδοση))
	ipconsole.MΕκτύπωση(([]byte)(":"))
	ipconsole.MUnsignedinteger16Εκτύπωση(διαδίκτυοprotocolΜήνυμα.σύνολοΔιάρκεια)
	ipconsole.MΕκτύπωση(([]byte)(":"))
	ipconsole.MUnsignedinteger32Εκτύπωση(uint32(efhandler.Getipaddress()))
	ipconsole.MΕκτύπωση(([]byte)(":"))
	ipconsole.MΕκτύπωση(([]byte)("\n"))

	return reply

}
func (self *TΔιαδίκτυοprotocolprovider) Αποστολή(προορισμόςipaddressΔίκτυοbyteorder uint32, protocol uint8, dataΔείκτης uintptr, μέγεθος uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TΔιαδίκτυοprotocolv4Μήνυμαbuffer = (*TΔιαδίκτυοprotocolv4Μήνυμαbuffer)(Pointer(&buffer1_2))
	var μήνυμα TΔιαδίκτυοprotocolv4Μήνυμα = TΔιαδίκτυοprotocolv4Μήνυμα{}
	μήνυμα.έκδοση = 4
	μήνυμα.headerΔιάρκεια = ipΜέγεθος / 4
	μήνυμα.tos = 0
	μήνυμα.σύνολοΔιάρκεια = Unsignedinteger16r(uint16(μέγεθος + uint32(ipΜέγεθος)))

	μήνυμα.ident = 0x0100
	μήνυμα.διακόπτεςΚΑΙoffset = 0x0040
	μήνυμα.ώραtolive = 0x40
	μήνυμα.protocol = protocol

	μήνυμα.προορισμόςipaddress = προορισμόςipaddressΔίκτυοbyteorder

	μήνυμα.πηγήipaddress = uint32(efhandler.Getipaddress())

	μήνυμα.checksum = 0

	μήνυμα.Σύνολοbuffer(buffer_2)
	μήνυμα.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipΜέγεθος))
	μήνυμα.Σύνολοbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataΔείκτης))

	for i := 0; i < int(μέγεθος); i++ {

		buffer1_2[i+int(ipΜέγεθος)] = databuffer_2[i]
	}

	ipconsole.MΕκτύπωσηxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(μέγεθος)+int(ipΜέγεθος); i++ {
		ipconsole.MHexadecimalΕκτύπωση(buffer1_2[i])
	}
	ipconsole.MΕκτύπωση(([]byte)(":"))
	ipconsole.MΕκτύπωση(([]byte)("]\n"))

	var επόμενοhopipaddressΔίκτυοbyteorder uint32 = προορισμόςipaddressΔίκτυοbyteorder
	if (προορισμόςipaddressΔίκτυοbyteorder & self.SubnetΜάσκα) != (μήνυμα.πηγήipaddress & self.SubnetΜάσκα) {
		επόμενοhopipaddressΔίκτυοbyteorder = self.Gatewayip
	}

	var αποστολήdataΔείκτης = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Εκτύπωση(επόμενοhopipaddressΔίκτυοbyteorder)

	var ethernetΤύποςbe = Unsignedinteger16r(0x0800)
	efhandler.ΠλαίσιοΑποστολή(self.arpprovider.Resolve(επόμενοhopipaddressΔίκτυοbyteorder), ethernetΤύποςbe, αποστολήdataΔείκτης, uint32(ipΜέγεθος)+uint32(μέγεθος))

}
func (self *TΔιαδίκτυοprotocolprovider) Checksum(pdata *[4096]uint16, διάρκειασεbytes uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var databytes [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (διάρκειασεbytes % 2) != 0 {
		temporary += uint32(uint16(databytes[διάρκειασεbytes-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TΔιαδίκτυοprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
