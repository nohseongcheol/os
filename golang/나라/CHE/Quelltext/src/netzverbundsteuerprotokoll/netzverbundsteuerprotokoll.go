package netzverbundsteuerprotokoll

import . "unsafe"
import . "konsole"
import . "speicherVerwalter"
import . "rahmen_des_gemeinsamen_Übertragungsnetzes"
import . "netzverbundprotokoll4"
import . "hilfswerkzeug"

var icmpKonsole = TKonsole{}

type TInternetStrgNachrichtprotocolNachrichtbuffer struct {
	Typ	byte
	code	byte

	prüfsumme	[2]byte
	daten		[4]byte
}

var icmpGröße int = 64

type TInternetStrgNachrichtprotocolNachricht struct {
	Typ	uint8
	code	uint8

	prüfsumme	uint16
	daten		uint32
}

func (selbst *TInternetStrgNachrichtprotocolNachricht) Init(buffer_2 TInternetStrgNachrichtprotocolNachrichtbuffer) {
	selbst.Typ = buffer_2.Typ
	selbst.code = buffer_2.code

	selbst.prüfsumme = Unsignedinteger16r(Feldtounsignedinteger16(buffer_2.prüfsumme))
	selbst.daten = Unsignedinteger32r(Feldtounsignedinteger32(buffer_2.daten))
}

func (selbst *TInternetStrgNachrichtprotocolNachricht) Setzenbuffer(buffer_2 *TInternetStrgNachrichtprotocolNachrichtbuffer) {
	buffer_2.Typ = selbst.Typ
	buffer_2.code = selbst.code

	buffer_2.prüfsumme = Unsignedinteger16toFeld(selbst.prüfsumme)
	buffer_2.daten = Unsignedinteger32toFeld(selbst.daten)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var netzverbundsteuerprotokoll *TNetzverbundsteuerprotokoll

func (selbst *Icmphandler) Internetprotocolreceivewhen(quelleipaddressNetzwerkByteorder uint32, zielipaddressNetzwerkByteorder uint32, datenZeiger uintptr, größe uint32) bool {
	return netzverbundsteuerprotokoll.Internetprotocolreceivewhen(quelleipaddressNetzwerkByteorder, zielipaddressNetzwerkByteorder, datenZeiger, größe)
}

var iphandler IInternetprotocolhandler

type TNetzverbundsteuerprotokoll struct {
}

func (selbst *TNetzverbundsteuerprotokoll) Init(backend TNetzverbundprotokollanbieter, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	netzverbundsteuerprotokoll = selbst
}
func (selbst *TNetzverbundsteuerprotokoll) Internetprotocolreceivewhen(quelleipaddressNetzwerkByteorder uint32, zielipaddressNetzwerkByteorder uint32, datenZeiger uintptr, größe uint32) bool {
	if größe < uint32(icmpGröße) {
		return false
	}

	var buffer_2 *TInternetStrgNachrichtprotocolNachrichtbuffer = (*TInternetStrgNachrichtprotocolNachrichtbuffer)(Pointer(datenZeiger))
	var msg TInternetStrgNachrichtprotocolNachricht = TInternetStrgNachrichtprotocolNachricht{}
	msg.Init(*buffer_2)

	icmpKonsole.MDrucken(([]byte)("icmp:OnInternet"))
	icmpKonsole.MUnsignedinteger16Drucken(uint16(msg.Typ))
	icmpKonsole.MDrucken(([]byte)(":"))

	switch msg.Typ {
	case 0:
		icmpKonsole.MDrucken(([]byte)("ping response from "))
		break

	case 8:
		icmpKonsole.MDrucken(([]byte)("ping send "))
		msg.Typ = 0

		msg.prüfsumme = 0
		msg.Setzenbuffer(buffer_2)
		msg.prüfsumme = iphandler.Providerget().Prüfsumme((*([4096]uint16))(Pointer(datenZeiger)), uint32(icmpGröße))

		msg.Setzenbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (selbst *TNetzverbundsteuerprotokoll) EchorequestSenden(ipNetzwerkByteorder uint32) bool {
	var netzverbundsteuerprotokoll TInternetStrgNachrichtprotocolNachricht = TInternetStrgNachrichtprotocolNachricht{}

	var speicherVerwalter = &TSpeicherVerwalter{}
	var buffer_2 = (*TInternetStrgNachrichtprotocolNachrichtbuffer)(speicherVerwalter.Speicher_reservieren(1024))

	netzverbundsteuerprotokoll.Typ = 8
	netzverbundsteuerprotokoll.code = 0
	netzverbundsteuerprotokoll.daten = 0x3713
	netzverbundsteuerprotokoll.prüfsumme = 0
	netzverbundsteuerprotokoll.Setzenbuffer(buffer_2)
	netzverbundsteuerprotokoll.prüfsumme = iphandler.Providerget().Prüfsumme((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpGröße))
	netzverbundsteuerprotokoll.Setzenbuffer(buffer_2)

	var datenZeiger uintptr = uintptr(Pointer(buffer_2))
	iphandler.Senden(ipNetzwerkByteorder, 0x01, datenZeiger, uint32(icmpGröße))

	return false

}
