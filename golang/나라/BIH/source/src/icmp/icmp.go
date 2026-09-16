/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "memorijamanager"
import . "ethernetOkvir"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetcontrolPorukaprotocolPorukabuffer struct {
	Tip	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpVeličina int = 64

type TInternetcontrolPorukaprotocolPoruka struct {
	Tip	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TInternetcontrolPorukaprotocolPoruka) Init(buffer_2 TInternetcontrolPorukaprotocolPorukabuffer) {
	self.Tip = buffer_2.Tip
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.data))
}

func (self *TInternetcontrolPorukaprotocolPoruka) Skupbuffer(buffer_2 *TInternetcontrolPorukaprotocolPorukabuffer) {
	buffer_2.Tip = self.Tip
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)
	buffer_2.data = Unsignedinteger32toarray(self.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolPorukaprotocol

func (self *Icmphandler) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, datapointer uintptr, veličina uint32) bool {
	return icmp.Internetprotocolreceivewhen(izvoripaddressMrežabyteorder, odredišteipaddressMrežabyteorder, datapointer, veličina)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolPorukaprotocol struct {
}

func (self *TInternetcontrolPorukaprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetcontrolPorukaprotocol) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, datapointer uintptr, veličina uint32) bool {
	if veličina < uint32(icmpVeličina) {
		return false
	}

	var buffer_2 *TInternetcontrolPorukaprotocolPorukabuffer = (*TInternetcontrolPorukaprotocolPorukabuffer)(Pointer(datapointer))
	var msg TInternetcontrolPorukaprotocolPoruka = TInternetcontrolPorukaprotocolPoruka{}
	msg.Init(*buffer_2)

	icmpconsole.MŠtampaj(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Štampaj(uint16(msg.Tip))
	icmpconsole.MŠtampaj(([]byte)(":"))

	switch msg.Tip {
	case 0:
		icmpconsole.MŠtampaj(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MŠtampaj(([]byte)("ping send "))
		msg.Tip = 0

		msg.checksum = 0
		msg.Skupbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(datapointer)), uint32(icmpVeličina))

		msg.Skupbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetcontrolPorukaprotocol) EchorequestPošalji(ipMrežabyteorder uint32) bool {
	var icmp TInternetcontrolPorukaprotocolPoruka = TInternetcontrolPorukaprotocolPoruka{}

	var memorijamanager = &TMemorijamanager{}
	var buffer_2 = (*TInternetcontrolPorukaprotocolPorukabuffer)(memorijamanager.Malloc(1024))

	icmp.Tip = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Skupbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpVeličina))
	icmp.Skupbuffer(buffer_2)

	var datapointer uintptr = uintptr(Pointer(buffer_2))
	iphandler.Pošalji(ipMrežabyteorder, 0x01, datapointer, uint32(icmpVeličina))

	return false

}
