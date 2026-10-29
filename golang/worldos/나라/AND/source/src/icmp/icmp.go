/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "consola"
import . "memòriamanager"
import . "cableMarc"
import . "ipv4"
import . "util"

var icmpConsola = TConsola{}

type TInternetcontrolMissatgeprotocolMissatgebuffer struct {
	Tipus	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpMida int = 64

type TInternetcontrolMissatgeprotocolMissatge struct {
	Tipus	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (unmateix *TInternetcontrolMissatgeprotocolMissatge) Init(buffer_2 TInternetcontrolMissatgeprotocolMissatgebuffer) {
	unmateix.Tipus = buffer_2.Tipus
	unmateix.code = buffer_2.code

	unmateix.checksum = Unsignedinteger16r(Matriutounsignedinteger16(buffer_2.checksum))
	unmateix.data = Unsignedinteger32r(Matriutounsignedinteger32(buffer_2.data))
}

func (unmateix *TInternetcontrolMissatgeprotocolMissatge) Estableixbuffer(buffer_2 *TInternetcontrolMissatgeprotocolMissatgebuffer) {
	buffer_2.Tipus = unmateix.Tipus
	buffer_2.code = unmateix.code

	buffer_2.checksum = Unsignedinteger16toMatriu(unmateix.checksum)
	buffer_2.data = Unsignedinteger32toMatriu(unmateix.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolMissatgeprotocol

func (unmateix *Icmphandler) Internetprotocolreceivewhen(origenipAdreçaXarxabyteorder uint32, destinacióipAdreçaXarxabyteorder uint32, dataPunter uintptr, mida uint32) bool {
	return icmp.Internetprotocolreceivewhen(origenipAdreçaXarxabyteorder, destinacióipAdreçaXarxabyteorder, dataPunter, mida)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolMissatgeprotocol struct {
}

func (unmateix *TInternetcontrolMissatgeprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = unmateix
}
func (unmateix *TInternetcontrolMissatgeprotocol) Internetprotocolreceivewhen(origenipAdreçaXarxabyteorder uint32, destinacióipAdreçaXarxabyteorder uint32, dataPunter uintptr, mida uint32) bool {
	if mida < uint32(icmpMida) {
		return false
	}

	var buffer_2 *TInternetcontrolMissatgeprotocolMissatgebuffer = (*TInternetcontrolMissatgeprotocolMissatgebuffer)(Pointer(dataPunter))
	var msg TInternetcontrolMissatgeprotocolMissatge = TInternetcontrolMissatgeprotocolMissatge{}
	msg.Init(*buffer_2)

	icmpConsola.MImprimeix(([]byte)("icmp:OnInternet"))
	icmpConsola.MUnsignedinteger16Imprimeix(uint16(msg.Tipus))
	icmpConsola.MImprimeix(([]byte)(":"))

	switch msg.Tipus {
	case 0:
		icmpConsola.MImprimeix(([]byte)("ping response from "))
		break

	case 8:
		icmpConsola.MImprimeix(([]byte)("ping send "))
		msg.Tipus = 0

		msg.checksum = 0
		msg.Estableixbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataPunter)), uint32(icmpMida))

		msg.Estableixbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (unmateix *TInternetcontrolMissatgeprotocol) EchorequestEnvia(ipXarxabyteorder uint32) bool {
	var icmp TInternetcontrolMissatgeprotocolMissatge = TInternetcontrolMissatgeprotocolMissatge{}

	var memòriamanager = &TMemòriamanager{}
	var buffer_2 = (*TInternetcontrolMissatgeprotocolMissatgebuffer)(memòriamanager.Malloc(1024))

	icmp.Tipus = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Estableixbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpMida))
	icmp.Estableixbuffer(buffer_2)

	var dataPunter uintptr = uintptr(Pointer(buffer_2))
	iphandler.Envia(ipXarxabyteorder, 0x01, dataPunter, uint32(icmpMida))

	return false

}
