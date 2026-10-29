/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package icmp

import . "unsafe"
import . "console"
import . "mälumanager"
import . "ethernetRaam"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetJuhtTeadeprotocolTeadebuffer struct {
	Liik	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpSuurus int = 64

type TInternetJuhtTeadeprotocolTeade struct {
	Liik	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (ise *TInternetJuhtTeadeprotocolTeade) Init(buffer_2 TInternetJuhtTeadeprotocolTeadebuffer) {
	ise.Liik = buffer_2.Liik
	ise.code = buffer_2.code

	ise.checksum = Unsignedinteger16r(Massiivtounsignedinteger16(buffer_2.checksum))
	ise.data = Unsignedinteger32r(Massiivtounsignedinteger32(buffer_2.data))
}

func (ise *TInternetJuhtTeadeprotocolTeade) Määrabuffer(buffer_2 *TInternetJuhtTeadeprotocolTeadebuffer) {
	buffer_2.Liik = ise.Liik
	buffer_2.code = ise.code

	buffer_2.checksum = Unsignedinteger16toMassiiv(ise.checksum)
	buffer_2.data = Unsignedinteger32toMassiiv(ise.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetJuhtTeadeprotocol

func (ise *Icmphandler) Internetprotocolreceivewhen(aLLIKASipaddressVõrkbyteorder uint32, sihtfailipaddressVõrkbyteorder uint32, dataKursor uintptr, suurus uint32) bool {
	return icmp.Internetprotocolreceivewhen(aLLIKASipaddressVõrkbyteorder, sihtfailipaddressVõrkbyteorder, dataKursor, suurus)
}

var iphandler IInternetprotocolhandler

type TInternetJuhtTeadeprotocol struct {
}

func (ise *TInternetJuhtTeadeprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = ise
}
func (ise *TInternetJuhtTeadeprotocol) Internetprotocolreceivewhen(aLLIKASipaddressVõrkbyteorder uint32, sihtfailipaddressVõrkbyteorder uint32, dataKursor uintptr, suurus uint32) bool {
	if suurus < uint32(icmpSuurus) {
		return false
	}

	var buffer_2 *TInternetJuhtTeadeprotocolTeadebuffer = (*TInternetJuhtTeadeprotocolTeadebuffer)(Pointer(dataKursor))
	var msg TInternetJuhtTeadeprotocolTeade = TInternetJuhtTeadeprotocolTeade{}
	msg.Init(*buffer_2)

	icmpconsole.MPrindi(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Prindi(uint16(msg.Liik))
	icmpconsole.MPrindi(([]byte)(":"))

	switch msg.Liik {
	case 0:
		icmpconsole.MPrindi(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MPrindi(([]byte)("ping send "))
		msg.Liik = 0

		msg.checksum = 0
		msg.Määrabuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataKursor)), uint32(icmpSuurus))

		msg.Määrabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (ise *TInternetJuhtTeadeprotocol) EchorequestSaada(ipVõrkbyteorder uint32) bool {
	var icmp TInternetJuhtTeadeprotocolTeade = TInternetJuhtTeadeprotocolTeade{}

	var mälumanager = &TMälumanager{}
	var buffer_2 = (*TInternetJuhtTeadeprotocolTeadebuffer)(mälumanager.Malloc(1024))

	icmp.Liik = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Määrabuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpSuurus))
	icmp.Määrabuffer(buffer_2)

	var dataKursor uintptr = uintptr(Pointer(buffer_2))
	iphandler.Saada(ipVõrkbyteorder, 0x01, dataKursor, uint32(icmpSuurus))

	return false

}
