package icmp

import . "unsafe"
import . "console"
import . "זיכרוןmanager"
import . "אתרנטframe"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type Tאינטרנטבקרההודעהprotocolהודעהbuffer struct {
	Tסוג	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpגודל int = 64

type Tאינטרנטבקרההודעהprotocolהודעה struct {
	Tסוג	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *Tאינטרנטבקרההודעהprotocolהודעה) Init(buffer_2 Tאינטרנטבקרההודעהprotocolהודעהbuffer) {
	self.Tסוג = buffer_2.Tסוג
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer_2.data))
}

func (self *Tאינטרנטבקרההודעהprotocolהודעה) Sקבעbuffer(buffer_2 *Tאינטרנטבקרההודעהprotocolהודעהbuffer) {
	buffer_2.Tסוג = self.Tסוג
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toמערך(self.checksum)
	buffer_2.data = Unsignedinteger32toמערך(self.data)
}

type Icmphandler struct {
	Tאינטרנטprotocolhandler
}

var icmp *Tאינטרנטבקרההודעהprotocol

func (self *Icmphandler) Oאינטרנטprotocolreceivewhen(מקורipaddressרשתbyteorder uint32, יעדipaddressרשתbyteorder uint32, dataסמן uintptr, גודל uint32) bool {
	return icmp.Oאינטרנטprotocolreceivewhen(מקורipaddressרשתbyteorder, יעדipaddressרשתbyteorder, dataסמן, גודל)
}

var iphandler Iאינטרנטprotocolhandler

type Tאינטרנטבקרההודעהprotocol struct {
}

func (self *Tאינטרנטבקרההודעהprotocol) Init(backend Tאינטרנטprotocolprovider, handler Iאינטרנטprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *Tאינטרנטבקרההודעהprotocol) Oאינטרנטprotocolreceivewhen(מקורipaddressרשתbyteorder uint32, יעדipaddressרשתbyteorder uint32, dataסמן uintptr, גודל uint32) bool {
	if גודל < uint32(icmpגודל) {
		return false
	}

	var buffer_2 *Tאינטרנטבקרההודעהprotocolהודעהbuffer = (*Tאינטרנטבקרההודעהprotocolהודעהbuffer)(Pointer(dataסמן))
	var msg Tאינטרנטבקרההודעהprotocolהודעה = Tאינטרנטבקרההודעהprotocolהודעה{}
	msg.Init(*buffer_2)

	icmpconsole.Mהדפסה(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16הדפסה(uint16(msg.Tסוג))
	icmpconsole.Mהדפסה(([]byte)(":"))

	switch msg.Tסוג {
	case 0:
		icmpconsole.Mהדפסה(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.Mהדפסה(([]byte)("ping send "))
		msg.Tסוג = 0

		msg.checksum = 0
		msg.Sקבעbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataסמן)), uint32(icmpגודל))

		msg.Sקבעbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *Tאינטרנטבקרההודעהprotocol) Echorequestשלח(ipרשתbyteorder uint32) bool {
	var icmp Tאינטרנטבקרההודעהprotocolהודעה = Tאינטרנטבקרההודעהprotocolהודעה{}

	var זיכרוןmanager = &Tזיכרוןmanager{}
	var buffer_2 = (*Tאינטרנטבקרההודעהprotocolהודעהbuffer)(זיכרוןmanager.Malloc(1024))

	icmp.Tסוג = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Sקבעbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpגודל))
	icmp.Sקבעbuffer(buffer_2)

	var dataסמן uintptr = uintptr(Pointer(buffer_2))
	iphandler.Sשלח(ipרשתbyteorder, 0x01, dataסמן, uint32(icmpגודל))

	return false

}
