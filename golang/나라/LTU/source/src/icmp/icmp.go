package icmp

import . "unsafe"
import . "console"
import . "atmintismanager"
import . "laidinisKadras"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetasValdymasPranešimasprotocolPranešimasbuffer struct {
	Tipas	byte
	code	byte

	kontrolinėsuma	[2]byte
	data		[4]byte
}

var icmpDydis int = 64

type TInternetasValdymasPranešimasprotocolPranešimas struct {
	Tipas	uint8
	code	uint8

	kontrolinėsuma	uint16
	data		uint32
}

func (self *TInternetasValdymasPranešimasprotocolPranešimas) Init(buffer_2 TInternetasValdymasPranešimasprotocolPranešimasbuffer) {
	self.Tipas = buffer_2.Tipas
	self.code = buffer_2.code

	self.kontrolinėsuma = Unsignedinteger16r(Masyvastounsignedinteger16(buffer_2.kontrolinėsuma))
	self.data = Unsignedinteger32r(Masyvastounsignedinteger32(buffer_2.data))
}

func (self *TInternetasValdymasPranešimasprotocolPranešimas) Nustatytabuffer(buffer_2 *TInternetasValdymasPranešimasprotocolPranešimasbuffer) {
	buffer_2.Tipas = self.Tipas
	buffer_2.code = self.code

	buffer_2.kontrolinėsuma = Unsignedinteger16toMasyvas(self.kontrolinėsuma)
	buffer_2.data = Unsignedinteger32toMasyvas(self.data)
}

type Icmphandler struct {
	TInternetasprotocolhandler
}

var icmp *TInternetasValdymasPranešimasprotocol

func (self *Icmphandler) Internetasprotocolreceivewhen(šaltinisipaddressTinklasbyteorder uint32, tikslasipaddressTinklasbyteorder uint32, dataRodyklė uintptr, dydis uint32) bool {
	return icmp.Internetasprotocolreceivewhen(šaltinisipaddressTinklasbyteorder, tikslasipaddressTinklasbyteorder, dataRodyklė, dydis)
}

var iphandler IInternetasprotocolhandler

type TInternetasValdymasPranešimasprotocol struct {
}

func (self *TInternetasValdymasPranešimasprotocol) Init(backend TInternetasprotocolprovider, handler IInternetasprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = self
}
func (self *TInternetasValdymasPranešimasprotocol) Internetasprotocolreceivewhen(šaltinisipaddressTinklasbyteorder uint32, tikslasipaddressTinklasbyteorder uint32, dataRodyklė uintptr, dydis uint32) bool {
	if dydis < uint32(icmpDydis) {
		return false
	}

	var buffer_2 *TInternetasValdymasPranešimasprotocolPranešimasbuffer = (*TInternetasValdymasPranešimasprotocolPranešimasbuffer)(Pointer(dataRodyklė))
	var msg TInternetasValdymasPranešimasprotocolPranešimas = TInternetasValdymasPranešimasprotocolPranešimas{}
	msg.Init(*buffer_2)

	icmpconsole.MSpausdinti(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Spausdinti(uint16(msg.Tipas))
	icmpconsole.MSpausdinti(([]byte)(":"))

	switch msg.Tipas {
	case 0:
		icmpconsole.MSpausdinti(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MSpausdinti(([]byte)("ping send "))
		msg.Tipas = 0

		msg.kontrolinėsuma = 0
		msg.Nustatytabuffer(buffer_2)
		msg.kontrolinėsuma = iphandler.Providerget().Kontrolinėsuma((*([4096]uint16))(Pointer(dataRodyklė)), uint32(icmpDydis))

		msg.Nustatytabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TInternetasValdymasPranešimasprotocol) EchorequestSiųsti(ipTinklasbyteorder uint32) bool {
	var icmp TInternetasValdymasPranešimasprotocolPranešimas = TInternetasValdymasPranešimasprotocolPranešimas{}

	var atmintismanager = &TAtmintismanager{}
	var buffer_2 = (*TInternetasValdymasPranešimasprotocolPranešimasbuffer)(atmintismanager.Malloc(1024))

	icmp.Tipas = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.kontrolinėsuma = 0
	icmp.Nustatytabuffer(buffer_2)
	icmp.kontrolinėsuma = iphandler.Providerget().Kontrolinėsuma((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpDydis))
	icmp.Nustatytabuffer(buffer_2)

	var dataRodyklė uintptr = uintptr(Pointer(buffer_2))
	iphandler.Siųsti(ipTinklasbyteorder, 0x01, dataRodyklė, uint32(icmpDydis))

	return false

}
