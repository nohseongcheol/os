package icmp

import . "unsafe"
import . "консол"
import . "санахойЗохицуулагч"
import . "итернэтframe"
import . "ipv4"
import . "util"

var icmpКонсол = TКонсол{}

type TИнтернетcontrolМэдээprotocolМэдээbuffer struct {
	Төрөл	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpХэмжээ int = 64

type TИнтернетcontrolМэдээprotocolМэдээ struct {
	Төрөл	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TИнтернетcontrolМэдээprotocolМэдээ) Init(buffer_2 TИнтернетcontrolМэдээprotocolМэдээbuffer) {
	self.Төрөл = buffer_2.Төрөл
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (self *TИнтернетcontrolМэдээprotocolМэдээ) Setbuffer(buffer_2 *TИнтернетcontrolМэдээprotocolМэдээbuffer) {
	buffer_2.Төрөл = self.Төрөл
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)
	buffer_2.data = Unsignedinteger32toarray(self.data)
}

type Icmphandler struct {
	TИнтернетprotocolhandler
}

var icmp *TИнтернетcontrolМэдээprotocol

func (self *Icmphandler) Интернетprotocolreceivewhen(эхipaddressСүлжээbyteorder uint32, destinationipaddressСүлжээbyteorder uint32, datapointer uintptr, хэмжээ uint32) bool {
	return icmp.Интернетprotocolreceivewhen(эхipaddressСүлжээbyteorder, destinationipaddressСүлжээbyteorder, datapointer, хэмжээ)
}

var iphandler IИнтернетprotocolhandler

type TИнтернетcontrolМэдээprotocol struct {
}

func (self *TИнтернетcontrolМэдээprotocol) Init(backend TИнтернетprotocolprovider, handler IИнтернетprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TИнтернетcontrolМэдээprotocol) Интернетprotocolreceivewhen(эхipaddressСүлжээbyteorder uint32, destinationipaddressСүлжээbyteorder uint32, datapointer uintptr, хэмжээ uint32) bool {
	if хэмжээ < uint32(icmpХэмжээ) {
		return false
	}

	var buffer_2 *TИнтернетcontrolМэдээprotocolМэдээbuffer = (*TИнтернетcontrolМэдээprotocolМэдээbuffer)(Pointer(datapointer))
	var msg TИнтернетcontrolМэдээprotocolМэдээ = TИнтернетcontrolМэдээprotocolМэдээ{}
	msg.Init(*buffer_2)

	icmpКонсол.MХэвлэх(([]byte)("icmp:OnInternet"))
	icmpКонсол.MUnsignedinteger16Хэвлэх(uint16(msg.Төрөл))
	icmpКонсол.MХэвлэх(([]byte)(":"))

	switch msg.Төрөл {
	case 0:
		icmpКонсол.MХэвлэх(([]byte)("ping response from "))
		break

	case 8:
		icmpКонсол.MХэвлэх(([]byte)("ping send "))
		msg.Төрөл = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpХэмжээ))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TИнтернетcontrolМэдээprotocol) Echorequestsend(ipСүлжээbyteorder uint32) bool {
	var icmp TИнтернетcontrolМэдээprotocolМэдээ = TИнтернетcontrolМэдээprotocolМэдээ{}

	var санахойЗохицуулагч = &TСанахойЗохицуулагч{}
	var buffer_2 = (*TИнтернетcontrolМэдээprotocolМэдээbuffer)(санахойЗохицуулагч.Malloc(1024))

	icmp.Төрөл = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpХэмжээ))
	icmp.Setbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipСүлжээbyteorder, 0x01, datapointer, uint32(icmpХэмжээ))

	return false

}
