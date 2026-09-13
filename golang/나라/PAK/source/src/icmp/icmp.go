package icmp

import . "unsafe"
import . "console"
import . "یادداشتmanager"
import . "ایتھرنیٹframe"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type Tانٹرنیٹcontrolپیغامprotocolپیغامbuffer struct {
	Tنوعیت	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpحجم int = 64

type Tانٹرنیٹcontrolپیغامprotocolپیغام struct {
	Tنوعیت	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *Tانٹرنیٹcontrolپیغامprotocolپیغام) Init(buffer_2 Tانٹرنیٹcontrolپیغامprotocolپیغامbuffer) {
	self.Tنوعیت = buffer_2.Tنوعیت
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer_2.data))
}

func (self *Tانٹرنیٹcontrolپیغامprotocolپیغام) Sسیٹbuffer(buffer_2 *Tانٹرنیٹcontrolپیغامprotocolپیغامbuffer) {
	buffer_2.Tنوعیت = self.Tنوعیت
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toلڑی(self.checksum)
	buffer_2.data = Unsignedinteger32toلڑی(self.data)
}

type Icmphandler struct {
	Tانٹرنیٹprotocolhandler
}

var icmp *Tانٹرنیٹcontrolپیغامprotocol

func (self *Icmphandler) Oانٹرنیٹprotocolreceivewhen(مصدرipaddressنیٹورکbyteorder uint32, destinationipaddressنیٹورکbyteorder uint32, dataپؤائنٹر uintptr, حجم uint32) bool {
	return icmp.Oانٹرنیٹprotocolreceivewhen(مصدرipaddressنیٹورکbyteorder, destinationipaddressنیٹورکbyteorder, dataپؤائنٹر, حجم)
}

var iphandler Iانٹرنیٹprotocolhandler

type Tانٹرنیٹcontrolپیغامprotocol struct {
}

func (self *Tانٹرنیٹcontrolپیغامprotocol) Init(backend Tانٹرنیٹprotocolprovider, handler Iانٹرنیٹprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *Tانٹرنیٹcontrolپیغامprotocol) Oانٹرنیٹprotocolreceivewhen(مصدرipaddressنیٹورکbyteorder uint32, destinationipaddressنیٹورکbyteorder uint32, dataپؤائنٹر uintptr, حجم uint32) bool {
	if حجم < uint32(icmpحجم) {
		return false
	}

	var buffer_2 *Tانٹرنیٹcontrolپیغامprotocolپیغامbuffer = (*Tانٹرنیٹcontrolپیغامprotocolپیغامbuffer)(Pointer(dataپؤائنٹر))
	var msg Tانٹرنیٹcontrolپیغامprotocolپیغام = Tانٹرنیٹcontrolپیغامprotocolپیغام{}
	msg.Init(*buffer_2)

	icmpconsole.Mچھاپیں(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16چھاپیں(uint16(msg.Tنوعیت))
	icmpconsole.Mچھاپیں(([]byte)(":"))

	switch msg.Tنوعیت {
	case 0:
		icmpconsole.Mچھاپیں(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.Mچھاپیں(([]byte)("ping send "))
		msg.Tنوعیت = 0

		msg.checksum = 0
		msg.Sسیٹbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataپؤائنٹر)), uint32(icmpحجم))

		msg.Sسیٹbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *Tانٹرنیٹcontrolپیغامprotocol) Echorequestsend(ipنیٹورکbyteorder uint32) bool {
	var icmp Tانٹرنیٹcontrolپیغامprotocolپیغام = Tانٹرنیٹcontrolپیغامprotocolپیغام{}

	var یادداشتmanager = &Tیادداشتmanager{}
	var buffer_2 = (*Tانٹرنیٹcontrolپیغامprotocolپیغامbuffer)(یادداشتmanager.Malloc(1024))

	icmp.Tنوعیت = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Sسیٹbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpحجم))
	icmp.Sسیٹbuffer(buffer_2)

	var dataپؤائنٹر uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipنیٹورکbyteorder, 0x01, dataپؤائنٹر, uint32(icmpحجم))

	return false

}
