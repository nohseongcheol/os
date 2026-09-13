package icmp

import . "unsafe"
import . "console"
import . "memoriemanager"
import . "ethernetCadru"
import . "ipv4"
import . "util"

var icmpconsole = TConsole{}

type TInternetcontrolMesajprotocolMesajbuffer struct {
	Tip	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpMărime int = 64

type TInternetcontrolMesajprotocolMesaj struct {
	Tip	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (sine *TInternetcontrolMesajprotocolMesaj) Init(buffer_2 TInternetcontrolMesajprotocolMesajbuffer) {
	sine.Tip = buffer_2.Tip
	sine.code = buffer_2.code

	sine.checksum = Unsignedinteger16r(Vectortounsignedinteger16(buffer_2.checksum))
	sine.data = Unsignedinteger32r(Vectortounsignedinteger32(buffer_2.data))
}

func (sine *TInternetcontrolMesajprotocolMesaj) Definitbuffer(buffer_2 *TInternetcontrolMesajprotocolMesajbuffer) {
	buffer_2.Tip = sine.Tip
	buffer_2.code = sine.code

	buffer_2.checksum = Unsignedinteger16toVector(sine.checksum)
	buffer_2.data = Unsignedinteger32toVector(sine.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolMesajprotocol

func (sine *Icmphandler) Internetprotocolreceivewhen(sursăipaddressRețeabyteorder uint32, destinațieipaddressRețeabyteorder uint32, dataIndicator uintptr, mărime uint32) bool {
	return icmp.Internetprotocolreceivewhen(sursăipaddressRețeabyteorder, destinațieipaddressRețeabyteorder, dataIndicator, mărime)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolMesajprotocol struct {
}

func (sine *TInternetcontrolMesajprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = sine
}
func (sine *TInternetcontrolMesajprotocol) Internetprotocolreceivewhen(sursăipaddressRețeabyteorder uint32, destinațieipaddressRețeabyteorder uint32, dataIndicator uintptr, mărime uint32) bool {
	if mărime < uint32(icmpMărime) {
		return false
	}

	var buffer_2 *TInternetcontrolMesajprotocolMesajbuffer = (*TInternetcontrolMesajprotocolMesajbuffer)(Pointer(dataIndicator))
	var msg TInternetcontrolMesajprotocolMesaj = TInternetcontrolMesajprotocolMesaj{}
	msg.Init(*buffer_2)

	icmpconsole.MTipărește(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Tipărește(uint16(msg.Tip))
	icmpconsole.MTipărește(([]byte)(":"))

	switch msg.Tip {
	case 0:
		icmpconsole.MTipărește(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MTipărește(([]byte)("ping send "))
		msg.Tip = 0

		msg.checksum = 0
		msg.Definitbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataIndicator)), uint32(icmpMărime))

		msg.Definitbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (sine *TInternetcontrolMesajprotocol) EchorequestTrimite(ipRețeabyteorder uint32) bool {
	var icmp TInternetcontrolMesajprotocolMesaj = TInternetcontrolMesajprotocolMesaj{}

	var memoriemanager = &TMemoriemanager{}
	var buffer_2 = (*TInternetcontrolMesajprotocolMesajbuffer)(memoriemanager.Malloc(1024))

	icmp.Tip = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Definitbuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpMărime))
	icmp.Definitbuffer(buffer_2)

	var dataIndicator uintptr = uintptr(Pointer(buffer_2))
	iphandler.Trimite(ipRețeabyteorder, 0x01, dataIndicator, uint32(icmpMărime))

	return false

}
