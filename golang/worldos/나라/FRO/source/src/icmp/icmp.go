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

type TInternetcontrolboðanprotocolboðanbuffer struct {
	TypeValue	byte
	code		byte

	checksum	[2]byte
	data		[4]byte
}

var icmpStødd int = 64

type TInternetcontrolboðanprotocolboðan struct {
	TypeValue	uint8
	code		uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetcontrolboðanprotocolboðan) Init(buffer_2 TInternetcontrolboðanprotocolboðanbuffer) {
	self.TypeValue = buffer_2.TypeValue
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (self *TInternetcontrolboðanprotocolboðan) Setbuffer(buffer_2 *TInternetcontrolboðanprotocolboðanbuffer) {
	buffer_2.TypeValue = self.TypeValue
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)
	buffer_2.data = Unsignedinteger32toarray(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolboðanprotocol

func (self *Icmphandler) Internetprotocolreceivewhen(sourceipaddressNetbyteorder uint32, destinationipaddressNetbyteorder uint32, datapointer uintptr, stødd uint32) bool {
	return icmp.Internetprotocolreceivewhen(sourceipaddressNetbyteorder, destinationipaddressNetbyteorder, datapointer, stødd)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolboðanprotocol struct {
}

func (self *TInternetcontrolboðanprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetcontrolboðanprotocol) Internetprotocolreceivewhen(sourceipaddressNetbyteorder uint32, destinationipaddressNetbyteorder uint32, datapointer uintptr, stødd uint32) bool {
	if stødd < uint32(icmpStødd) {
		return false
	}

	var buffer_2 *TInternetcontrolboðanprotocolboðanbuffer = (*TInternetcontrolboðanprotocolboðanbuffer)(Pointer(datapointer))
	var msg TInternetcontrolboðanprotocolboðan = TInternetcontrolboðanprotocolboðan{}
	msg.Init(*buffer_2)

	icmpconsole.MPrint(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16print(uint16(msg.TypeValue))
	icmpconsole.MPrint(([]byte)(":"))

	switch msg.TypeValue {
	case 0:
		icmpconsole.MPrint(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MPrint(([]byte)("ping send "))
		msg.TypeValue = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpStødd))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetcontrolboðanprotocol) Echorequestsend(ipNetbyteorder uint32) bool {
	var icmp TInternetcontrolboðanprotocolboðan = TInternetcontrolboðanprotocolboðan{}

	var memorymanager = &TMemorymanager{}
	var buffer_2 = (*TInternetcontrolboðanprotocolboðanbuffer)(memorymanager.Malloc(1024))

	icmp.TypeValue = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpStødd))
	icmp.Setbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipNetbyteorder, 0x01, datapointer, uint32(icmpStødd))

	return false

}
