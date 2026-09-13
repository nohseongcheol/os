package icmp

import . "unsafe"
import . "konzola"
import . "pamäťmanager"
import . "ethernetRámec"
import . "ipv4"
import . "util"

var icmpKonzola = TKonzola{}

type TInternetOvládanieSprávaprotocolSprávabuffer struct {
	Typ	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpVeľkosť int = 64

type TInternetOvládanieSprávaprotocolSpráva struct {
	Typ	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (vlastný *TInternetOvládanieSprávaprotocolSpráva) Init(buffer_2 TInternetOvládanieSprávaprotocolSprávabuffer) {
	vlastný.Typ = buffer_2.Typ
	vlastný.code = buffer_2.code

	vlastný.checksum = Unsignedinteger16r(Poletounsignedinteger16(buffer_2.checksum))
	vlastný.data = Unsignedinteger32r(Poletounsignedinteger32(buffer_2.data))
}

func (vlastný *TInternetOvládanieSprávaprotocolSpráva) Sadabuffer(buffer_2 *TInternetOvládanieSprávaprotocolSprávabuffer) {
	buffer_2.Typ = vlastný.Typ
	buffer_2.code = vlastný.code

	buffer_2.checksum = Unsignedinteger16toPole(vlastný.checksum)
	buffer_2.data = Unsignedinteger32toPole(vlastný.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetOvládanieSprávaprotocol

func (vlastný *Icmphandler) Internetprotocolreceivewhen(zdrojipaddressSieťbyteorder uint32, cieľipaddressSieťbyteorder uint32, dataKurzor uintptr, veľkosť uint32) bool {
	return icmp.Internetprotocolreceivewhen(zdrojipaddressSieťbyteorder, cieľipaddressSieťbyteorder, dataKurzor, veľkosť)
}

var iphandler IInternetprotocolhandler

type TInternetOvládanieSprávaprotocol struct {
}

func (vlastný *TInternetOvládanieSprávaprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = vlastný
}
func (vlastný *TInternetOvládanieSprávaprotocol) Internetprotocolreceivewhen(zdrojipaddressSieťbyteorder uint32, cieľipaddressSieťbyteorder uint32, dataKurzor uintptr, veľkosť uint32) bool {
	if veľkosť < uint32(icmpVeľkosť) {
		return false
	}

	var buffer_2 *TInternetOvládanieSprávaprotocolSprávabuffer = (*TInternetOvládanieSprávaprotocolSprávabuffer)(Pointer(dataKurzor))
	var msg TInternetOvládanieSprávaprotocolSpráva = TInternetOvládanieSprávaprotocolSpráva{}
	msg.Init(*buffer_2)

	icmpKonzola.MTlačiť(([]byte)("icmp:OnInternet"))
	icmpKonzola.MUnsignedinteger16Tlačiť(uint16(msg.Typ))
	icmpKonzola.MTlačiť(([]byte)(":"))

	switch msg.Typ {
	case 0:
		icmpKonzola.MTlačiť(([]byte)("ping response from "))
		break

	case 8:
		icmpKonzola.MTlačiť(([]byte)("ping send "))
		msg.Typ = 0

		msg.checksum = 0
		msg.Sadabuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataKurzor)), uint32(icmpVeľkosť))

		msg.Sadabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (vlastný *TInternetOvládanieSprávaprotocol) EchorequestPoslať(ipSieťbyteorder uint32) bool {
	var icmp TInternetOvládanieSprávaprotocolSpráva = TInternetOvládanieSprávaprotocolSpráva{}

	var pamäťmanager = &TPamäťmanager{}
	var buffer_2 = (*TInternetOvládanieSprávaprotocolSprávabuffer)(pamäťmanager.Malloc(1024))

	icmp.Typ = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Sadabuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpVeľkosť))
	icmp.Sadabuffer(buffer_2)

	var dataKurzor uintptr = uintptr(Pointer(buffer_2))
	iphandler.Poslať(ipSieťbyteorder, 0x01, dataKurzor, uint32(icmpVeľkosť))

	return false

}
