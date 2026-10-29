/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "ububikomanager"
import . "ethernetIkadiri"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInterineticontrolUbutumwaprotocolUbutumwabuffer struct {
	Ubwoko_2	byte
	code		byte

	checksum	[2]byte
	data		[4]byte
}

var icmpIngano int = 64

type TInterineticontrolUbutumwaprotocolUbutumwa struct {
	Ubwoko_2	uint8
	code		uint8

	checksum	uint16
	data		uint32
}

func (self *TInterineticontrolUbutumwaprotocolUbutumwa) Init(buffer_2 TInterineticontrolUbutumwaprotocolUbutumwabuffer) {
	self.Ubwoko_2 = buffer_2.Ubwoko_2
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Imbonerahamwetounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer_2.data))
}

func (self *TInterineticontrolUbutumwaprotocolUbutumwa) Setbuffer(buffer_2 *TInterineticontrolUbutumwaprotocolUbutumwabuffer) {
	buffer_2.Ubwoko_2 = self.Ubwoko_2
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toImbonerahamwe(self.checksum)
	buffer_2.data = Unsignedinteger32toImbonerahamwe(self.data)
}

type Icmphandler struct {
	TInterinetiprotocolhandler
}

var icmp *TInterineticontrolUbutumwaprotocol

func (self *Icmphandler) Interinetiprotocolreceivewhen(inkomokoipaddressurusobebyteorder uint32, destinationipaddressurusobebyteorder uint32, datapointer uintptr, ingano uint32) bool {
	return icmp.Interinetiprotocolreceivewhen(inkomokoipaddressurusobebyteorder, destinationipaddressurusobebyteorder, datapointer, ingano)
}

var iphandler IInterinetiprotocolhandler

type TInterineticontrolUbutumwaprotocol struct {
}

func (self *TInterineticontrolUbutumwaprotocol) Init(backend TInterinetiprotocolprovider, handler IInterinetiprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInterineticontrolUbutumwaprotocol) Interinetiprotocolreceivewhen(inkomokoipaddressurusobebyteorder uint32, destinationipaddressurusobebyteorder uint32, datapointer uintptr, ingano uint32) bool {
	if ingano < uint32(icmpIngano) {
		return false
	}

	var buffer_2 *TInterineticontrolUbutumwaprotocolUbutumwabuffer = (*TInterineticontrolUbutumwaprotocolUbutumwabuffer)(Pointer(datapointer))
	var msg TInterineticontrolUbutumwaprotocolUbutumwa = TInterineticontrolUbutumwaprotocolUbutumwa{}
	msg.Init(*buffer_2)

	icmpconsole.MGucapa(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Gucapa(uint16(msg.Ubwoko_2))
	icmpconsole.MGucapa(([]byte)(":"))

	switch msg.Ubwoko_2 {
	case 0:
		icmpconsole.MGucapa(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MGucapa(([]byte)("ping send "))
		msg.Ubwoko_2 = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpIngano))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInterineticontrolUbutumwaprotocol) Echorequestsend(ipurusobebyteorder uint32) bool {
	var icmp TInterineticontrolUbutumwaprotocolUbutumwa = TInterineticontrolUbutumwaprotocolUbutumwa{}

	var ububikomanager = &TUbubikomanager{}
	var buffer_2 = (*TInterineticontrolUbutumwaprotocolUbutumwabuffer)(ububikomanager.Malloc(1024))

	icmp.Ubwoko_2 = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpIngano))
	icmp.Setbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipurusobebyteorder, 0x01, datapointer, uint32(icmpIngano))

	return false

}
