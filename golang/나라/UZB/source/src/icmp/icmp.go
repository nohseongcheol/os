/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "xotiramanager"
import . "ethernetRamka"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetcontrolXABARprotocolXABARbuffer struct {
	Turi	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpHajmi int = 64

type TInternetcontrolXABARprotocolXABAR struct {
	Turi	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetcontrolXABARprotocolXABAR) Init(buffer_2 TInternetcontrolXABARprotocolXABARbuffer) {
	self.Turi = buffer_2.Turi
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (self *TInternetcontrolXABARprotocolXABAR) Setbuffer(buffer_2 *TInternetcontrolXABARprotocolXABARbuffer) {
	buffer_2.Turi = self.Turi
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)
	buffer_2.data = Unsignedinteger32toarray(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolXABARprotocol

func (self *Icmphandler) Internetprotocolreceivewhen(sourceipaddressTarmoqbyteorder uint32, destinationipaddressTarmoqbyteorder uint32, dataKorsatgich uintptr, hajmi uint32) bool {
	return icmp.Internetprotocolreceivewhen(sourceipaddressTarmoqbyteorder, destinationipaddressTarmoqbyteorder, dataKorsatgich, hajmi)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolXABARprotocol struct {
}

func (self *TInternetcontrolXABARprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetcontrolXABARprotocol) Internetprotocolreceivewhen(sourceipaddressTarmoqbyteorder uint32, destinationipaddressTarmoqbyteorder uint32, dataKorsatgich uintptr, hajmi uint32) bool {
	if hajmi < uint32(icmpHajmi) {
		return false
	}

	var buffer_2 *TInternetcontrolXABARprotocolXABARbuffer = (*TInternetcontrolXABARprotocolXABARbuffer)(Pointer(dataKorsatgich))
	var msg TInternetcontrolXABARprotocolXABAR = TInternetcontrolXABARprotocolXABAR{}
	msg.Init(*buffer_2)

	icmpconsole.MChopetish(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Chopetish(uint16(msg.Turi))
	icmpconsole.MChopetish(([]byte)(":"))

	switch msg.Turi {
	case 0:
		icmpconsole.MChopetish(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MChopetish(([]byte)("ping send "))
		msg.Turi = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataKorsatgich)), uint32(icmpHajmi))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetcontrolXABARprotocol) EchorequestJoʻnatish(ipTarmoqbyteorder uint32) bool {
	var icmp TInternetcontrolXABARprotocolXABAR = TInternetcontrolXABARprotocolXABAR{}

	var xotiramanager = &TXotiramanager{}
	var buffer_2 = (*TInternetcontrolXABARprotocolXABARbuffer)(xotiramanager.Malloc(1024))

	icmp.Turi = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpHajmi))
	icmp.Setbuffer(buffer_2)

	var dataKorsatgich uintptr = uintptr(Pointer(buffer_2))
	iphandler.Joʻnatish(ipTarmoqbyteorder, 0x01, dataKorsatgich, uint32(icmpHajmi))

	return false

}
