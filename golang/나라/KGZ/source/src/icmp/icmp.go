package icmp

import . "unsafe"
import . "console"
import . "эсиmanager"
import . "ethernetframe"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TИнтернетcontrolmessageprotocolmessagebuffer struct {
	Түрү	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpӨлчөм int = 64

type TИнтернетcontrolmessageprotocolmessage struct {
	Түрү	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TИнтернетcontrolmessageprotocolmessage) Init(buffer_2 TИнтернетcontrolmessageprotocolmessagebuffer) {
	self.Түрү = buffer_2.Түрү
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Массивtounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Массивtounsignedinteger32(buffer_2.data))
}

func (self *TИнтернетcontrolmessageprotocolmessage) Setbuffer(buffer_2 *TИнтернетcontrolmessageprotocolmessagebuffer) {
	buffer_2.Түрү = self.Түрү
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toМассив(self.checksum)
	buffer_2.data = Unsignedinteger32toМассив(self.data)
}

type Icmphandler struct {
	TИнтернетprotocolhandler
}

var icmp *TИнтернетcontrolmessageprotocol

func (self *Icmphandler) Интернетprotocolreceivewhen(баштапкытекстipaddressТармакbyteorder uint32, destinationipaddressТармакbyteorder uint32, dataКөрсөткүч uintptr, өлчөм uint32) bool {
	return icmp.Интернетprotocolreceivewhen(баштапкытекстipaddressТармакbyteorder, destinationipaddressТармакbyteorder, dataКөрсөткүч, өлчөм)
}

var iphandler IИнтернетprotocolhandler

type TИнтернетcontrolmessageprotocol struct {
}

func (self *TИнтернетcontrolmessageprotocol) Init(backend TИнтернетprotocolprovider, handler IИнтернетprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TИнтернетcontrolmessageprotocol) Интернетprotocolreceivewhen(баштапкытекстipaddressТармакbyteorder uint32, destinationipaddressТармакbyteorder uint32, dataКөрсөткүч uintptr, өлчөм uint32) bool {
	if өлчөм < uint32(icmpӨлчөм) {
		return false
	}

	var buffer_2 *TИнтернетcontrolmessageprotocolmessagebuffer = (*TИнтернетcontrolmessageprotocolmessagebuffer)(Pointer(dataКөрсөткүч))
	var msg TИнтернетcontrolmessageprotocolmessage = TИнтернетcontrolmessageprotocolmessage{}
	msg.Init(*buffer_2)

	icmpconsole.MБасма(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Басма(uint16(msg.Түрү))
	icmpconsole.MБасма(([]byte)(":"))

	switch msg.Түрү {
	case 0:
		icmpconsole.MБасма(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MБасма(([]byte)("ping send "))
		msg.Түрү = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataКөрсөткүч)), uint32(icmpӨлчөм))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TИнтернетcontrolmessageprotocol) Echorequestsend(ipТармакbyteorder uint32) bool {
	var icmp TИнтернетcontrolmessageprotocolmessage = TИнтернетcontrolmessageprotocolmessage{}

	var эсиmanager = &TЭсиmanager{}
	var buffer_2 = (*TИнтернетcontrolmessageprotocolmessagebuffer)(эсиmanager.Malloc(1024))

	icmp.Түрү = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpӨлчөм))
	icmp.Setbuffer(buffer_2)

	var dataКөрсөткүч uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipТармакbyteorder, 0x01, dataКөрсөткүч, uint32(icmpӨлчөм))

	return false

}
