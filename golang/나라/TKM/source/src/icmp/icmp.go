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

type TInternetcontrolSargytprotocolSargytbuffer struct {
	Hil	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpUlulyk int = 64

type TInternetcontrolSargytprotocolSargyt struct {
	Hil	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetcontrolSargytprotocolSargyt) Init(buffer_2 TInternetcontrolSargytprotocolSargytbuffer) {
	self.Hil = buffer_2.Hil
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (self *TInternetcontrolSargytprotocolSargyt) Setbuffer(buffer_2 *TInternetcontrolSargytprotocolSargytbuffer) {
	buffer_2.Hil = self.Hil
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)
	buffer_2.data = Unsignedinteger32toarray(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolSargytprotocol

func (self *Icmphandler) Internetprotocolreceivewhen(çeşmeipaddressŞebekebyteorder uint32, destinationipaddressŞebekebyteorder uint32, datapointer uintptr, ululyk uint32) bool {
	return icmp.Internetprotocolreceivewhen(çeşmeipaddressŞebekebyteorder, destinationipaddressŞebekebyteorder, datapointer, ululyk)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolSargytprotocol struct {
}

func (self *TInternetcontrolSargytprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetcontrolSargytprotocol) Internetprotocolreceivewhen(çeşmeipaddressŞebekebyteorder uint32, destinationipaddressŞebekebyteorder uint32, datapointer uintptr, ululyk uint32) bool {
	if ululyk < uint32(icmpUlulyk) {
		return false
	}

	var buffer_2 *TInternetcontrolSargytprotocolSargytbuffer = (*TInternetcontrolSargytprotocolSargytbuffer)(Pointer(datapointer))
	var msg TInternetcontrolSargytprotocolSargyt = TInternetcontrolSargytprotocolSargyt{}
	msg.Init(*buffer_2)

	icmpconsole.MÇap(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Çap(uint16(msg.Hil))
	icmpconsole.MÇap(([]byte)(":"))

	switch msg.Hil {
	case 0:
		icmpconsole.MÇap(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MÇap(([]byte)("ping send "))
		msg.Hil = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpUlulyk))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetcontrolSargytprotocol) Echorequestsend(ipŞebekebyteorder uint32) bool {
	var icmp TInternetcontrolSargytprotocolSargyt = TInternetcontrolSargytprotocolSargyt{}

	var memorymanager = &TMemorymanager{}
	var buffer_2 = (*TInternetcontrolSargytprotocolSargytbuffer)(memorymanager.Malloc(1024))

	icmp.Hil = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpUlulyk))
	icmp.Setbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipŞebekebyteorder, 0x01, datapointer, uint32(icmpUlulyk))

	return false

}
