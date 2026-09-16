/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "hukommelsemanager"
import . "ethernetRamme"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetKontrolMeddelelseprotocolMeddelelsebuffer struct {
	TypeVærdi	byte
	code		byte

	checksum	[2]byte
	data		[4]byte
}

var icmpStørrelse int = 64

type TInternetKontrolMeddelelseprotocolMeddelelse struct {
	TypeVærdi	uint8
	code		uint8

	checksum	uint16
	data		uint32
}

func (selv *TInternetKontrolMeddelelseprotocolMeddelelse) Init(buffer_2 TInternetKontrolMeddelelseprotocolMeddelelsebuffer) {
	selv.TypeVærdi = buffer_2.TypeVærdi
	selv.code = buffer_2.code

	selv.checksum = Unsignedinteger16r(Tabeltounsignedinteger16(buffer_2.checksum))
	selv.data = Unsignedinteger32r(Tabeltounsignedinteger32(buffer_2.data))
}

func (selv *TInternetKontrolMeddelelseprotocolMeddelelse) Satbuffer(buffer_2 *TInternetKontrolMeddelelseprotocolMeddelelsebuffer) {
	buffer_2.TypeVærdi = selv.TypeVærdi
	buffer_2.code = selv.code

	buffer_2.checksum = Unsignedinteger16toTabel(selv.checksum)
	buffer_2.data = Unsignedinteger32toTabel(selv.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetKontrolMeddelelseprotocol

func (selv *Icmphandler) Internetprotocolreceivewhen(kildeipaddressNetværkbyteorder uint32, destinationipaddressNetværkbyteorder uint32, dataMarkør uintptr, størrelse uint32) bool {
	return icmp.Internetprotocolreceivewhen(kildeipaddressNetværkbyteorder, destinationipaddressNetværkbyteorder, dataMarkør, størrelse)
}

var iphandler IInternetprotocolhandler

type TInternetKontrolMeddelelseprotocol struct {
}

func (selv *TInternetKontrolMeddelelseprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = selv
}
func (selv *TInternetKontrolMeddelelseprotocol) Internetprotocolreceivewhen(kildeipaddressNetværkbyteorder uint32, destinationipaddressNetværkbyteorder uint32, dataMarkør uintptr, størrelse uint32) bool {
	if størrelse < uint32(icmpStørrelse) {
		return false
	}

	var buffer_2 *TInternetKontrolMeddelelseprotocolMeddelelsebuffer = (*TInternetKontrolMeddelelseprotocolMeddelelsebuffer)(Pointer(dataMarkør))
	var msg TInternetKontrolMeddelelseprotocolMeddelelse = TInternetKontrolMeddelelseprotocolMeddelelse{}
	msg.Init(*buffer_2)

	icmpconsole.MUdskriv(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Udskriv(uint16(msg.TypeVærdi))
	icmpconsole.MUdskriv(([]byte)(":"))

	switch msg.TypeVærdi {
	case 0:
		icmpconsole.MUdskriv(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MUdskriv(([]byte)("ping send "))
		msg.TypeVærdi = 0

		msg.checksum = 0
		msg.Satbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataMarkør)), uint32(icmpStørrelse))

		msg.Satbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (selv *TInternetKontrolMeddelelseprotocol) Echorequestsend(ipNetværkbyteorder uint32) bool {
	var icmp TInternetKontrolMeddelelseprotocolMeddelelse = TInternetKontrolMeddelelseprotocolMeddelelse{}

	var hukommelsemanager = &THukommelsemanager{}
	var buffer_2 = (*TInternetKontrolMeddelelseprotocolMeddelelsebuffer)(hukommelsemanager.Malloc(1024))

	icmp.TypeVærdi = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Satbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpStørrelse))
	icmp.Satbuffer(buffer_2)

	var dataMarkør uintptr = uintptr(Pointer(buffer_2))
	iphandler.Send(ipNetværkbyteorder, 0x01, dataMarkør, uint32(icmpStørrelse))

	return false

}
