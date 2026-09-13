package icmp

import . "unsafe"
import . "konsolë"
import . "memoriaManazhuesi"
import . "ethernetKornizë"
import . "ipv4"
import . "util"

var icmpKonsolë = TKonsolë{}

type TInternetcontrolMesazhiprotocolMesazhibuffer struct {
	Lloji	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpMadhësia int = 64

type TInternetcontrolMesazhiprotocolMesazhi struct {
	Lloji	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (vetvetja *TInternetcontrolMesazhiprotocolMesazhi) Init(buffer_2 TInternetcontrolMesazhiprotocolMesazhibuffer) {
	vetvetja.Lloji = buffer_2.Lloji
	vetvetja.code = buffer_2.code

	vetvetja.checksum = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer_2.checksum))
	vetvetja.data = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer_2.data))
}

func (vetvetja *TInternetcontrolMesazhiprotocolMesazhi) Caktonibuffer(buffer_2 *TInternetcontrolMesazhiprotocolMesazhibuffer) {
	buffer_2.Lloji = vetvetja.Lloji
	buffer_2.code = vetvetja.code

	buffer_2.checksum = Unsignedinteger16toRreshtimi(vetvetja.checksum)
	buffer_2.data = Unsignedinteger32toRreshtimi(vetvetja.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var icmp *TInternetcontrolMesazhiprotocol

func (vetvetja *Icmphandler) Internetprotocolreceivewhen(burimiipaddressRrjetibyteorder uint32, destinacioniipaddressRrjetibyteorder uint32, dataKursori uintptr, madhësia uint32) bool {
	return icmp.Internetprotocolreceivewhen(burimiipaddressRrjetibyteorder, destinacioniipaddressRrjetibyteorder, dataKursori, madhësia)
}

var iphandler IInternetprotocolhandler

type TInternetcontrolMesazhiprotocol struct {
}

func (vetvetja *TInternetcontrolMesazhiprotocol) Init(backend TInternetprotocolprovider, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	icmp = vetvetja
}
func (vetvetja *TInternetcontrolMesazhiprotocol) Internetprotocolreceivewhen(burimiipaddressRrjetibyteorder uint32, destinacioniipaddressRrjetibyteorder uint32, dataKursori uintptr, madhësia uint32) bool {
	if madhësia < uint32(icmpMadhësia) {
		return false
	}

	var buffer_2 *TInternetcontrolMesazhiprotocolMesazhibuffer = (*TInternetcontrolMesazhiprotocolMesazhibuffer)(Pointer(dataKursori))
	var msg TInternetcontrolMesazhiprotocolMesazhi = TInternetcontrolMesazhiprotocolMesazhi{}
	msg.Init(*buffer_2)

	icmpKonsolë.MPrinto(([]byte)("icmp:OnInternet"))
	icmpKonsolë.MUnsignedinteger16Printo(uint16(msg.Lloji))
	icmpKonsolë.MPrinto(([]byte)(":"))

	switch msg.Lloji {
	case 0:
		icmpKonsolë.MPrinto(([]byte)("ping response from "))
		break

	case 8:
		icmpKonsolë.MPrinto(([]byte)("ping send "))
		msg.Lloji = 0

		msg.checksum = 0
		msg.Caktonibuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataKursori)), uint32(icmpMadhësia))

		msg.Caktonibuffer(buffer_2)

		return true
		break
	}
	return false
}

func (vetvetja *TInternetcontrolMesazhiprotocol) EchorequestDërgo(ipRrjetibyteorder uint32) bool {
	var icmp TInternetcontrolMesazhiprotocolMesazhi = TInternetcontrolMesazhiprotocolMesazhi{}

	var memoriaManazhuesi = &TMemoriaManazhuesi{}
	var buffer_2 = (*TInternetcontrolMesazhiprotocolMesazhibuffer)(memoriaManazhuesi.Malloc(1024))

	icmp.Lloji = 8
	icmp.code = 0
	icmp.data = 0x3713
	icmp.checksum = 0
	icmp.Caktonibuffer(buffer_2)
	icmp.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpMadhësia))
	icmp.Caktonibuffer(buffer_2)

	var dataKursori uintptr = uintptr(Pointer(buffer_2))
	iphandler.Dërgo(ipRrjetibyteorder, 0x01, dataKursori, uint32(icmpMadhësia))

	return false

}
