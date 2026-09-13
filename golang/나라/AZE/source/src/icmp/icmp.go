package icmp

import . "unsafe"
import . "console"
import . "yaddaşmanager"
import . "eternetframe"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetcontrolİsmarıcprotocolİsmarıcbuffer struct {
	Növ	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpBöyüklük int = 64

type TInternetcontrolİsmarıcprotocolİsmarıc struct {
	Növ	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetcontrolİsmarıcprotocolİsmarıc) Init(buffer_2 TInternetcontrolİsmarıcprotocolİsmarıcbuffer) {
	self.Növ = buffer_2.Növ
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (self *TInternetcontrolİsmarıcprotocolİsmarıc) Setbuffer(buffer_2 *TInternetcontrolİsmarıcprotocolİsmarıcbuffer) {
	buffer_2.Növ = self.Növ
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)
	buffer_2.data = Unsignedinteger32toarray(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolİsmarıcprotocol

func (self *Icmphandler) Internetprotocolreceivewhen(mənbəipaddressŞəbəkəbyteorder uint32, destinationipaddressŞəbəkəbyteorder uint32, datapointer uintptr, böyüklük uint32) bool {
	return icmp.Internetprotocolreceivewhen(mənbəipaddressŞəbəkəbyteorder, destinationipaddressŞəbəkəbyteorder, datapointer, böyüklük)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolİsmarıcprotocol struct {
}

func (self *TInternetcontrolİsmarıcprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetcontrolİsmarıcprotocol) Internetprotocolreceivewhen(mənbəipaddressŞəbəkəbyteorder uint32, destinationipaddressŞəbəkəbyteorder uint32, datapointer uintptr, böyüklük uint32) bool {
	if böyüklük < uint32(icmpBöyüklük) {
		return false
	}

	var buffer_2 *TInternetcontrolİsmarıcprotocolİsmarıcbuffer = (*TInternetcontrolİsmarıcprotocolİsmarıcbuffer)(Pointer(datapointer))
	var msg TInternetcontrolİsmarıcprotocolİsmarıc = TInternetcontrolİsmarıcprotocolİsmarıc{}
	msg.Init(*buffer_2)

	icmpconsole.MÇapEt(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16ÇapEt(uint16(msg.Növ))
	icmpconsole.MÇapEt(([]byte)(":"))

	switch msg.Növ {
	case 0:
		icmpconsole.MÇapEt(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MÇapEt(([]byte)("ping send "))
		msg.Növ = 0

		msg.checksum = 0
		msg.Setbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpBöyüklük))

		msg.Setbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetcontrolİsmarıcprotocol) Echorequestsend(ipŞəbəkəbyteorder uint32) bool {
	var icmp TInternetcontrolİsmarıcprotocolİsmarıc = TInternetcontrolİsmarıcprotocolİsmarıc{}

	var yaddaşmanager = &TYaddaşmanager{}
	var buffer_2 = (*TInternetcontrolİsmarıcprotocolİsmarıcbuffer)(yaddaşmanager.Malloc(1024))

	icmp.Növ = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Setbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpBöyüklük))
	icmp.Setbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipŞəbəkəbyteorder, 0x01, datapointer, uint32(icmpBöyüklük))

	return false

}
