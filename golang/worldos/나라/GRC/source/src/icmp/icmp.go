/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "μνήμηmanager"
import . "ethernetΠλαίσιο"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμαbuffer struct {
	Τύπος	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpΜέγεθος int = 64

type TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμα struct {
	Τύπος	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμα) Init(buffer_2 TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμαbuffer) {
	self.Τύπος = buffer_2.Τύπος
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Διάταξηtounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer_2.data))
}

func (self *TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμα) Σύνολοbuffer(buffer_2 *TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμαbuffer) {
	buffer_2.Τύπος = self.Τύπος
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toΔιάταξη(self.checksum)
	buffer_2.data = Unsignedinteger32toΔιάταξη(self.data)
}

type Icmphandler struct {
	TΔιαδίκτυοprotocolhandler
}

var icmp *TΔιαδίκτυοΈλεγχοςΜήνυμαprotocol

func (self *Icmphandler) Διαδίκτυοprotocolreceivewhen(πηγήipaddressΔίκτυοbyteorder uint32, προορισμόςipaddressΔίκτυοbyteorder uint32, dataΔείκτης uintptr, μέγεθος uint32) bool {
	return icmp.Διαδίκτυοprotocolreceivewhen(πηγήipaddressΔίκτυοbyteorder, προορισμόςipaddressΔίκτυοbyteorder, dataΔείκτης, μέγεθος)
}

var iphandler IΔιαδίκτυοprotocolhandler

type TΔιαδίκτυοΈλεγχοςΜήνυμαprotocol struct {
}

func (self *TΔιαδίκτυοΈλεγχοςΜήνυμαprotocol) Init(backend TΔιαδίκτυοprotocolprovider, handler IΔιαδίκτυοprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TΔιαδίκτυοΈλεγχοςΜήνυμαprotocol) Διαδίκτυοprotocolreceivewhen(πηγήipaddressΔίκτυοbyteorder uint32, προορισμόςipaddressΔίκτυοbyteorder uint32, dataΔείκτης uintptr, μέγεθος uint32) bool {
	if μέγεθος < uint32(icmpΜέγεθος) {
		return false
	}

	var buffer_2 *TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμαbuffer = (*TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμαbuffer)(Pointer(dataΔείκτης))
	var msg TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμα = TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμα{}
	msg.Init(*buffer_2)

	icmpconsole.MΕκτύπωση(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Εκτύπωση(uint16(msg.Τύπος))
	icmpconsole.MΕκτύπωση(([]byte)(":"))

	switch msg.Τύπος {
	case 0:
		icmpconsole.MΕκτύπωση(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MΕκτύπωση(([]byte)("ping send "))
		msg.Τύπος = 0

		msg.checksum = 0
		msg.Σύνολοbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataΔείκτης)), uint32(icmpΜέγεθος))

		msg.Σύνολοbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TΔιαδίκτυοΈλεγχοςΜήνυμαprotocol) EchorequestΑποστολή(ipΔίκτυοbyteorder uint32) bool {
	var icmp TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμα = TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμα{}

	var μνήμηmanager = &TΜνήμηmanager{}
	var buffer_2 = (*TΔιαδίκτυοΈλεγχοςΜήνυμαprotocolΜήνυμαbuffer)(μνήμηmanager.Malloc(1024))

	icmp.Τύπος = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Σύνολοbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpΜέγεθος))
	icmp.Σύνολοbuffer(buffer_2)

	var dataΔείκτης uintptr = uintptr(Pointer(buffer_2))
	iphandler.Αποστολή(ipΔίκτυοbyteorder, 0x01, dataΔείκτης, uint32(icmpΜέγεθος))

	return false

}
