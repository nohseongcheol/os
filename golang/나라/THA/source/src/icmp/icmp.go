package icmp

import . "unsafe"
import . "console"
import . "memorymanager"
import . "ethernetเฟรม"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetcontrolmessageprotocolmessagebuffer struct {
	Tประเภท	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpขนาด int = 64

type TInternetcontrolmessageprotocolmessage struct {
	Tประเภท	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetcontrolmessageprotocolmessage) Init(buffer_2 TInternetcontrolmessageprotocolmessagebuffer) {
	self.Tประเภท = buffer_2.Tประเภท
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (self *TInternetcontrolmessageprotocolmessage) Sกำหนดbuffer(buffer_2 *TInternetcontrolmessageprotocolmessagebuffer) {
	buffer_2.Tประเภท = self.Tประเภท
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)
	buffer_2.data = Unsignedinteger32toarray(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolmessageprotocol

func (self *Icmphandler) Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder uint32, ปลายทางipaddressnetworkbyteorder uint32, datapointer uintptr, ขนาด uint32) bool {
	return icmp.Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder, ปลายทางipaddressnetworkbyteorder, datapointer, ขนาด)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolmessageprotocol struct {
}

func (self *TInternetcontrolmessageprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetcontrolmessageprotocol) Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder uint32, ปลายทางipaddressnetworkbyteorder uint32, datapointer uintptr, ขนาด uint32) bool {
	if ขนาด < uint32(icmpขนาด) {
		return false
	}

	var buffer_2 *TInternetcontrolmessageprotocolmessagebuffer = (*TInternetcontrolmessageprotocolmessagebuffer)(Pointer(datapointer))
	var msg TInternetcontrolmessageprotocolmessage = TInternetcontrolmessageprotocolmessage{}
	msg.Init(*buffer_2)

	icmpconsole.MPrint(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16print(uint16(msg.Tประเภท))
	icmpconsole.MPrint(([]byte)(":"))

	switch msg.Tประเภท {
	case 0:
		icmpconsole.MPrint(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MPrint(([]byte)("ping send "))
		msg.Tประเภท = 0

		msg.checksum = 0
		msg.Sกำหนดbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpขนาด))

		msg.Sกำหนดbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetcontrolmessageprotocol) Echorequestsend(ipnetworkbyteorder uint32) bool {
	var icmp TInternetcontrolmessageprotocolmessage = TInternetcontrolmessageprotocolmessage{}

	var memorymanager = &TMemorymanager{}
	var buffer_2 = (*TInternetcontrolmessageprotocolmessagebuffer)(memorymanager.Malloc(1024))

	icmp.Tประเภท = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Sกำหนดbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpขนาด))
	icmp.Sกำหนดbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipnetworkbyteorder, 0x01, datapointer, uint32(icmpขนาด))

	return false

}
