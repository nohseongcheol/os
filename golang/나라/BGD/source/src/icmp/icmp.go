/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "memorymanager"
import . "ethernetframe"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetcontrolmessageprotocolmessagebuffer struct {
	Tধরণ	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpsize int = 64

type TInternetcontrolmessageprotocolmessage struct {
	Tধরণ	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetcontrolmessageprotocolmessage) Init(buffer_2 TInternetcontrolmessageprotocolmessagebuffer) {
	self.Tধরণ = buffer_2.Tধরণ
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (self *TInternetcontrolmessageprotocolmessage) Setbuffer(buffer_2 *TInternetcontrolmessageprotocolmessagebuffer) {
	buffer_2.Tধরণ = self.Tধরণ
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)
	buffer_2.data = Unsignedinteger32toarray(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolmessageprotocol

func (self *Icmphandler) Internetprotocolreceivewhen(উৎসipaddressnetworkbyteorder uint32, destinationipaddressnetworkbyteorder uint32, datapointer uintptr, size uint32) bool {
	return icmp.Internetprotocolreceivewhen(উৎসipaddressnetworkbyteorder, destinationipaddressnetworkbyteorder, datapointer, size)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolmessageprotocol struct {
}

func (self *TInternetcontrolmessageprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetcontrolmessageprotocol) Internetprotocolreceivewhen(উৎসipaddressnetworkbyteorder uint32, destinationipaddressnetworkbyteorder uint32, datapointer uintptr, size uint32) bool {
	if size < uint32(icmpsize) {
		return false
	}

	var buffer_2 *TInternetcontrolmessageprotocolmessagebuffer = (*TInternetcontrolmessageprotocolmessagebuffer)(Pointer(datapointer))
	var msg TInternetcontrolmessageprotocolmessage = TInternetcontrolmessageprotocolmessage{}
	msg.Init(*buffer_2)

	icmpconsole.MPrint(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16print(uint16(msg.Tধরণ))
	icmpconsole.MPrint(([]byte)(":"))

	switch msg.Tধরণ {
	case 0:
		icmpconsole.MPrint(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MPrint(([]byte)("ping send "))
		msg.Tধরণ = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpsize))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetcontrolmessageprotocol) Echorequestsend(ipnetworkbyteorder uint32) bool {
	var icmp TInternetcontrolmessageprotocolmessage = TInternetcontrolmessageprotocolmessage{}

	var memorymanager = &TMemorymanager{}
	var buffer_2 = (*TInternetcontrolmessageprotocolmessagebuffer)(memorymanager.Malloc(1024))

	icmp.Tধরণ = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpsize))
	icmp.Setbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipnetworkbyteorder, 0x01, datapointer, uint32(icmpsize))

	return false

}
