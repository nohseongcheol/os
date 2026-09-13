package netzverbundprotokoll4

import . "unsafe"
import . "hilfswerkzeug"
import . "konsole"
import . "rahmen_des_gemeinsamen_Übertragungsnetzes"
import . "arp"

var ipKonsole TKonsole = TKonsole{}

type TInternetprotocolv4Nachrichtbuffer struct {
	lenver		byte
	tos		byte
	gesamtLänge	[2]byte

	ident			[2]byte
	optionenundVersatz	[2]byte

	zeittolive	byte
	protocol	byte
	prüfsumme	[2]byte

	quelleipaddress	[4]byte
	zielipaddress	[4]byte
}

var ipGröße uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Nachricht struct {
	kopfLänge	uint8
	version		uint8
	tos		uint8
	gesamtLänge	uint16

	ident			uint16
	optionenundVersatz	uint16

	zeittolive	uint8
	protocol	uint8
	prüfsumme	uint16

	quelleipaddress	uint32
	zielipaddress	uint32
}

func (selbst *TInternetprotocolv4Nachricht) Init(buffer_2 TInternetprotocolv4Nachrichtbuffer) {

	selbst.version = ((buffer_2.lenver & 0xF0) >> 4)
	selbst.kopfLänge = buffer_2.lenver & 0x0F
	selbst.tos = buffer_2.tos
	selbst.gesamtLänge = Unsignedinteger16r(Feldtounsignedinteger16(buffer_2.gesamtLänge))

	selbst.ident = Unsignedinteger16r(Feldtounsignedinteger16(buffer_2.ident))
	selbst.optionenundVersatz = Unsignedinteger16r(Feldtounsignedinteger16(buffer_2.optionenundVersatz))

	selbst.zeittolive = buffer_2.zeittolive
	selbst.protocol = buffer_2.protocol
	selbst.prüfsumme = Unsignedinteger16r(Feldtounsignedinteger16(buffer_2.prüfsumme))

	selbst.quelleipaddress = Unsignedinteger32r(Feldtounsignedinteger32(buffer_2.quelleipaddress))
	selbst.zielipaddress = Unsignedinteger32r(Feldtounsignedinteger32(buffer_2.zielipaddress))

}
func (selbst *TInternetprotocolv4Nachricht) Setzenbuffer(buffer_2 *TInternetprotocolv4Nachrichtbuffer) {

	buffer_2.lenver = byte(((selbst.version & 0x0F) << 4) | (selbst.kopfLänge & 0x0F))
	buffer_2.tos = selbst.tos
	buffer_2.gesamtLänge = Unsignedinteger16toFeld(selbst.gesamtLänge)

	buffer_2.ident = Unsignedinteger16toFeld(selbst.ident)
	buffer_2.optionenundVersatz = Unsignedinteger16toFeld(selbst.optionenundVersatz)

	buffer_2.zeittolive = selbst.zeittolive
	buffer_2.protocol = selbst.protocol
	buffer_2.prüfsumme = Unsignedinteger16toFeld(selbst.prüfsumme)

	buffer_2.quelleipaddress = Unsignedinteger32toFeld(selbst.quelleipaddress)
	buffer_2.zielipaddress = Unsignedinteger32toFeld(selbst.zielipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TNetzverbundprotokollanbieter, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(quelleipaddressNetzwerkByteorder uint32, zielipaddressNetzwerkByteorder uint32, datenZeiger uintptr, größe uint32) bool
	Senden(zielipaddressNetzwerkByteorder uint32, pprotocol uint8, datenZeiger uintptr, größe uint32)
	Providerget() *TNetzverbundprotokollanbieter
}

type TInternetprotocolhandler struct {
}

var ipEthernetRahmenhandler IpEthernetRahmenhandler = IpEthernetRahmenhandler{}
var protocol uint8

func (selbst *TInternetprotocolhandler) Init(backend TNetzverbundprotokollanbieter, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (selbst *TInternetprotocolhandler) Internetprotocolreceivewhen(quelleipaddressNetzwerkByteorder uint32, zielipaddressNetzwerkByteorder uint32, datenZeiger uintptr, größe uint32) bool {
	ipKonsole.MDrucken(([]byte)("ipHandler:OnInternet"))
	return false
}
func (selbst *TInternetprotocolhandler) Senden(zielipaddressNetzwerkByteorder uint32, pprotocol uint8, datenZeiger uintptr, größe uint32) {

	netzverbundprotokollanbieter.Senden(zielipaddressNetzwerkByteorder, pprotocol, datenZeiger, größe)
}
func (selbst *TInternetprotocolhandler) Providerget() *TNetzverbundprotokollanbieter {
	return &netzverbundprotokollanbieter
}

type IpEthernetRahmenhandler struct {
	TEthernetRahmenhandler
}

var netzverbundprotokollanbieter TNetzverbundprotokollanbieter

func (selbst *IpEthernetRahmenhandler) EthernetRahmenreceivewhen(datenZeiger uintptr, größe int) bool {
	ipKonsole.MDrucken(([]byte)("iphandler:onEtherfameRecv\n"))
	return netzverbundprotokollanbieter.EthernetRahmenreceivewhen(datenZeiger, uint32(größe))

}

func (selbst *IpEthernetRahmenhandler) Senden(zielipaddressNetzwerkByteorder uint64, datenZeiger uintptr, größe uint32) {
	ipKonsole.MDrucken(([]byte)("ipefhandler:send\n"))
	var ethernetTypbe = Unsignedinteger16r(0x0800)
	selbst.TEthernetRahmenhandler.RahmenSenden(zielipaddressNetzwerkByteorder, ethernetTypbe, datenZeiger, größe)

}

var handler_2 [255]IInternetprotocolhandler

type TNetzverbundprotokollanbieter struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaske	uint32
}

var efhandler IEthernetRahmenhandler

func (selbst *TNetzverbundprotokollanbieter) Init(pefprovider TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes, pefhandler IEthernetRahmenhandler, arp Arpprovider, gatewayip uint32, subnetMaske uint32) {

	efhandler = pefhandler
	efhandler.Setzenhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	selbst.arpprovider = arp
	selbst.Gatewayip = gatewayip
	selbst.SubnetMaske = subnetMaske
	netzverbundprotokollanbieter = *selbst
}
func (selbst *TNetzverbundprotokollanbieter) EthernetRahmenreceivewhen(ethernetRahmenpayload uintptr, größe uint32) bool {
	if größe < uint32(ipGröße) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Nachrichtbuffer = (*TInternetprotocolv4Nachrichtbuffer)(Pointer(ethernetRahmenpayload))
	var internetprotocolNachricht TInternetprotocolv4Nachricht
	internetprotocolNachricht.Init(*buffer_2)

	var reply bool = false

	if internetprotocolNachricht.zielipaddress == uint32(efhandler.Getipaddress()) {

		var länge uint32 = uint32(internetprotocolNachricht.gesamtLänge)
		if länge > größe {
			länge = größe
		}
		if handler_2[internetprotocolNachricht.protocol] != nil {
			reply = handler_2[internetprotocolNachricht.protocol].Internetprotocolreceivewhen(internetprotocolNachricht.quelleipaddress, internetprotocolNachricht.zielipaddress, ethernetRahmenpayload+uintptr(4*internetprotocolNachricht.kopfLänge), uint32(länge-uint32(4*internetprotocolNachricht.kopfLänge)))

		}
	}

	if reply {

		var temporary = internetprotocolNachricht.zielipaddress
		internetprotocolNachricht.zielipaddress = internetprotocolNachricht.quelleipaddress
		internetprotocolNachricht.quelleipaddress = temporary

		internetprotocolNachricht.zeittolive = 0x40
		internetprotocolNachricht.prüfsumme = 0

		internetprotocolNachricht.Setzenbuffer(buffer_2)
		internetprotocolNachricht.prüfsumme = selbst.Prüfsumme((*([4096]uint16))(Pointer(ethernetRahmenpayload)), uint32(4*internetprotocolNachricht.kopfLänge))

		internetprotocolNachricht.Setzenbuffer(buffer_2)

	}

	ipKonsole.MDrucken(([]byte)("ipmessage"))
	ipKonsole.MUnsignedinteger32Drucken(internetprotocolNachricht.quelleipaddress)
	ipKonsole.MDrucken(([]byte)(":"))
	ipKonsole.MUnsignedinteger32Drucken(internetprotocolNachricht.zielipaddress)
	ipKonsole.MDrucken(([]byte)(":"))
	ipKonsole.MUnsignedinteger16Drucken(uint16(internetprotocolNachricht.kopfLänge))
	ipKonsole.MDrucken(([]byte)(":"))
	ipKonsole.MUnsignedinteger16Drucken(uint16(internetprotocolNachricht.version))
	ipKonsole.MDrucken(([]byte)(":"))
	ipKonsole.MUnsignedinteger16Drucken(internetprotocolNachricht.gesamtLänge)
	ipKonsole.MDrucken(([]byte)(":"))
	ipKonsole.MUnsignedinteger32Drucken(uint32(efhandler.Getipaddress()))
	ipKonsole.MDrucken(([]byte)(":"))
	ipKonsole.MDrucken(([]byte)("\n"))

	return reply

}
func (selbst *TNetzverbundprotokollanbieter) Senden(zielipaddressNetzwerkByteorder uint32, protocol uint8, datenZeiger uintptr, größe uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Nachrichtbuffer = (*TInternetprotocolv4Nachrichtbuffer)(Pointer(&buffer1_2))
	var nachricht TInternetprotocolv4Nachricht = TInternetprotocolv4Nachricht{}
	nachricht.version = 4
	nachricht.kopfLänge = ipGröße / 4
	nachricht.tos = 0
	nachricht.gesamtLänge = Unsignedinteger16r(uint16(größe + uint32(ipGröße)))

	nachricht.ident = 0x0100
	nachricht.optionenundVersatz = 0x0040
	nachricht.zeittolive = 0x40
	nachricht.protocol = protocol

	nachricht.zielipaddress = zielipaddressNetzwerkByteorder

	nachricht.quelleipaddress = uint32(efhandler.Getipaddress())

	nachricht.prüfsumme = 0

	nachricht.Setzenbuffer(buffer_2)
	nachricht.prüfsumme = selbst.Prüfsumme((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipGröße))
	nachricht.Setzenbuffer(buffer_2)

	var datenbuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datenZeiger))

	for i := 0; i < int(größe); i++ {

		buffer1_2[i+int(ipGröße)] = datenbuffer_2[i]
	}

	ipKonsole.MDruckenxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(größe)+int(ipGröße); i++ {
		ipKonsole.MHexadecimalDrucken(buffer1_2[i])
	}
	ipKonsole.MDrucken(([]byte)(":"))
	ipKonsole.MDrucken(([]byte)("]\n"))

	var weiterhopipaddressNetzwerkByteorder uint32 = zielipaddressNetzwerkByteorder
	if (zielipaddressNetzwerkByteorder & selbst.SubnetMaske) != (nachricht.quelleipaddress & selbst.SubnetMaske) {
		weiterhopipaddressNetzwerkByteorder = selbst.Gatewayip
	}

	var sendenDatenZeiger = uintptr(Pointer(&buffer1_2))
	ipKonsole.MUnsignedinteger32Drucken(weiterhopipaddressNetzwerkByteorder)

	var ethernetTypbe = Unsignedinteger16r(0x0800)
	efhandler.RahmenSenden(selbst.arpprovider.Auflösen(weiterhopipaddressNetzwerkByteorder), ethernetTypbe, sendenDatenZeiger, uint32(ipGröße)+uint32(größe))

}
func (selbst *TNetzverbundprotokollanbieter) Prüfsumme(pDaten *[4096]uint16, längeEinByte uint32) uint16 {
	var daten [4096]uint16 = *pDaten
	var temporary uint32 = 0
	var datenByte [4096]byte = *(*([4096]byte))(Pointer(&daten))
	if (längeEinByte % 2) != 0 {
		temporary += uint32(uint16(datenByte[längeEinByte-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (selbst *TNetzverbundprotokollanbieter) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
