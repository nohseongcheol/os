/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "konzol"
import . "memóriamanager"
import . "ethernetKeret"
import . "ipv4"
import . "util"

var icmpKonzol = TKonzol{}

type TInternetVezérlésÜzenetprotocolÜzenetbuffer struct {
	Típus	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpMéret int = 64

type TInternetVezérlésÜzenetprotocolÜzenet struct {
	Típus	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetVezérlésÜzenetprotocolÜzenet) Init(buffer_2 TInternetVezérlésÜzenetprotocolÜzenetbuffer) {
	self.Típus = buffer_2.Típus
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Tömbtounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Tömbtounsignedinteger32(buffer_2.data))
}

func (self *TInternetVezérlésÜzenetprotocolÜzenet) Halmazbuffer(buffer_2 *TInternetVezérlésÜzenetprotocolÜzenetbuffer) {
	buffer_2.Típus = self.Típus
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toTömb(self.checksum)
	buffer_2.data = Unsignedinteger32toTömb(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetVezérlésÜzenetprotocol

func (self *Icmphandler) Internetprotocolreceivewhen(forrásipaddressHálózatbyteorder uint32, célipaddressHálózatbyteorder uint32, dataMutató uintptr, méret uint32) bool {
	return icmp.Internetprotocolreceivewhen(forrásipaddressHálózatbyteorder, célipaddressHálózatbyteorder, dataMutató, méret)
}

var iphandler IInternetprotocolhandler

type TInternetVezérlésÜzenetprotocol struct {
}

func (self *TInternetVezérlésÜzenetprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetVezérlésÜzenetprotocol) Internetprotocolreceivewhen(forrásipaddressHálózatbyteorder uint32, célipaddressHálózatbyteorder uint32, dataMutató uintptr, méret uint32) bool {
	if méret < uint32(icmpMéret) {
		return false
	}

	var buffer_2 *TInternetVezérlésÜzenetprotocolÜzenetbuffer = (*TInternetVezérlésÜzenetprotocolÜzenetbuffer)(Pointer(dataMutató))
	var msg TInternetVezérlésÜzenetprotocolÜzenet = TInternetVezérlésÜzenetprotocolÜzenet{}
	msg.Init(*buffer_2)

	icmpKonzol.MNyomtatás(([]byte)("icmp:OnInternet"))
	icmpKonzol.MUnsignedinteger16Nyomtatás(uint16(msg.Típus))
	icmpKonzol.MNyomtatás(([]byte)(":"))

	switch msg.Típus {
	case 0:
		icmpKonzol.MNyomtatás(([]byte)("ping response from "))
		break

	case 8:
		icmpKonzol.MNyomtatás(([]byte)("ping send "))
		msg.Típus = 0

		msg.checksum = 0
		msg.Halmazbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataMutató)), uint32(icmpMéret))

		msg.Halmazbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetVezérlésÜzenetprotocol) EchorequestKüldés(ipHálózatbyteorder uint32) bool {
	var icmp TInternetVezérlésÜzenetprotocolÜzenet = TInternetVezérlésÜzenetprotocolÜzenet{}

	var memóriamanager = &TMemóriamanager{}
	var buffer_2 = (*TInternetVezérlésÜzenetprotocolÜzenetbuffer)(memóriamanager.Malloc(1024))

	icmp.Típus = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Halmazbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpMéret))
	icmp.Halmazbuffer(buffer_2)

	var dataMutató uintptr = uintptr(Pointer(buffer_2))
	iphandler.Küldés(ipHálózatbyteorder, 0x01, dataMutató, uint32(icmpMéret))

	return false

}
