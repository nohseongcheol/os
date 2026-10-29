/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "minnemanager"
import . "ethernetRamme"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternettKontrollMeldingprotocolMeldingbuffer struct {
	Filtype	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpStørrelse int = 64

type TInternettKontrollMeldingprotocolMelding struct {
	Filtype	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (selv *TInternettKontrollMeldingprotocolMelding) Init(buffer_2 TInternettKontrollMeldingprotocolMeldingbuffer) {
	selv.Filtype = buffer_2.Filtype
	selv.code = buffer_2.code

	selv.checksum = Unsignedinteger16r(Tabelltounsignedinteger16(buffer_2.checksum))
	selv.data = Unsignedinteger32r(Tabelltounsignedinteger32(buffer_2.data))
}

func (selv *TInternettKontrollMeldingprotocolMelding) Settbuffer(buffer_2 *TInternettKontrollMeldingprotocolMeldingbuffer) {
	buffer_2.Filtype = selv.Filtype
	buffer_2.code = selv.code

	buffer_2.checksum = Unsignedinteger16toTabell(selv.checksum)
	buffer_2.data = Unsignedinteger32toTabell(selv.data)
}

type Icmphandler struct {
	TInternettprotocolhandler
}

var icmp *TInternettKontrollMeldingprotocol

func (selv *Icmphandler) Internettprotocolreceivewhen(kildeipaddressNettverkbyteorder uint32, målipaddressNettverkbyteorder uint32, dataPeker uintptr, størrelse uint32) bool {
	return icmp.Internettprotocolreceivewhen(kildeipaddressNettverkbyteorder, målipaddressNettverkbyteorder, dataPeker, størrelse)
}

var iphandler IInternettprotocolhandler

type TInternettKontrollMeldingprotocol struct {
}

func (selv *TInternettKontrollMeldingprotocol) Init(backend TInternettprotocolprovider, handler IInternettprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = selv
}
func (selv *TInternettKontrollMeldingprotocol) Internettprotocolreceivewhen(kildeipaddressNettverkbyteorder uint32, målipaddressNettverkbyteorder uint32, dataPeker uintptr, størrelse uint32) bool {
	if størrelse < uint32(icmpStørrelse) {
		return false
	}

	var buffer_2 *TInternettKontrollMeldingprotocolMeldingbuffer = (*TInternettKontrollMeldingprotocolMeldingbuffer)(Pointer(dataPeker))
	var msg TInternettKontrollMeldingprotocolMelding = TInternettKontrollMeldingprotocolMelding{}
	msg.Init(*buffer_2)

	icmpconsole.MSkrivut(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Skrivut(uint16(msg.Filtype))
	icmpconsole.MSkrivut(([]byte)(":"))

	switch msg.Filtype {
	case 0:
		icmpconsole.MSkrivut(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MSkrivut(([]byte)("ping send "))
		msg.Filtype = 0

		msg.checksum = 0
		msg.Settbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataPeker)), uint32(icmpStørrelse))

		msg.Settbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (selv *TInternettKontrollMeldingprotocol) Echorequestsend(ipNettverkbyteorder uint32) bool {
	var icmp TInternettKontrollMeldingprotocolMelding = TInternettKontrollMeldingprotocolMelding{}

	var minnemanager = &TMinnemanager{}
	var buffer_2 = (*TInternettKontrollMeldingprotocolMeldingbuffer)(minnemanager.Malloc(1024))

	icmp.Filtype = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Settbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpStørrelse))
	icmp.Settbuffer(buffer_2)

	var dataPeker uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipNettverkbyteorder, 0x01, dataPeker, uint32(icmpStørrelse))

	return false

}
