/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "konsoly"
import . "arikaMpandrindra"
import . "ethernetframe"
import . "ipv4"
import . "util"

var icmpKonsoly = TKonsoly{}

type TInternetcontrolHafatraprotocolHafatrabuffer struct {
	Karazana	byte
	code		byte

	checksum	[2]byte
	data		[4]byte
}

var icmpHabe int = 64

type TInternetcontrolHafatraprotocolHafatra struct {
	Karazana	uint8
	code		uint8

	checksum	uint16
	data		uint32
}

func (nytena *TInternetcontrolHafatraprotocolHafatra) Init(buffer_2 TInternetcontrolHafatraprotocolHafatrabuffer) {
	nytena.Karazana = buffer_2.Karazana
	nytena.code = buffer_2.code

	nytena.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	nytena.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (nytena *TInternetcontrolHafatraprotocolHafatra) Setbuffer(buffer_2 *TInternetcontrolHafatraprotocolHafatrabuffer) {
	buffer_2.Karazana = nytena.Karazana
	buffer_2.code = nytena.code

	buffer_2.checksum = Unsignedinteger16toarray(nytena.checksum)
	buffer_2.data = Unsignedinteger32toarray(nytena.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolHafatraprotocol

func (nytena *Icmphandler) Internetprotocolreceivewhen(loharanoipaddressRezobyteorder uint32, destinationipaddressRezobyteorder uint32, datapointer uintptr, habe uint32) bool {
	return icmp.Internetprotocolreceivewhen(loharanoipaddressRezobyteorder, destinationipaddressRezobyteorder, datapointer, habe)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolHafatraprotocol struct {
}

func (nytena *TInternetcontrolHafatraprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = nytena
}
func (nytena *TInternetcontrolHafatraprotocol) Internetprotocolreceivewhen(loharanoipaddressRezobyteorder uint32, destinationipaddressRezobyteorder uint32, datapointer uintptr, habe uint32) bool {
	if habe < uint32(icmpHabe) {
		return false
	}

	var buffer_2 *TInternetcontrolHafatraprotocolHafatrabuffer = (*TInternetcontrolHafatraprotocolHafatrabuffer)(Pointer(datapointer))
	var msg TInternetcontrolHafatraprotocolHafatra = TInternetcontrolHafatraprotocolHafatra{}
	msg.Init(*buffer_2)

	icmpKonsoly.MAtontay(([]byte)("icmp:OnInternet"))
	icmpKonsoly.MUnsignedinteger16Atontay(uint16(msg.Karazana))
	icmpKonsoly.MAtontay(([]byte)(":"))

	switch msg.Karazana {
	case 0:
		icmpKonsoly.MAtontay(([]byte)("ping response from "))
		break

	case 8:
		icmpKonsoly.MAtontay(([]byte)("ping send "))
		msg.Karazana = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpHabe))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (nytena *TInternetcontrolHafatraprotocol) Echorequestsend(ipRezobyteorder uint32) bool {
	var icmp TInternetcontrolHafatraprotocolHafatra = TInternetcontrolHafatraprotocolHafatra{}

	var arikaMpandrindra = &TArikaMpandrindra{}
	var buffer_2 = (*TInternetcontrolHafatraprotocolHafatrabuffer)(arikaMpandrindra.Malloc(1024))

	icmp.Karazana = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpHabe))
	icmp.Setbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipRezobyteorder, 0x01, datapointer, uint32(icmpHabe))

	return false

}
