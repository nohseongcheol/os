/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package benutzerdatagrammprotokoll

import . "unsafe"
import . "konsole"
import . "hilfswerkzeug"
import . "speicherVerwalter"
import . "netzverbundprotokoll4"

var udpKonsole = TKonsole{}

type TBenutzerdatagramprotocolKopfbuffer struct {
	quellportnummer	[2]byte
	zielportnummer	[2]byte

	länge		[2]byte
	prüfsumme	[2]byte
}

var udpKopfGröße uint32 = 8

type TBenutzerdatagrammkopf struct {
	quellportnummer	uint16
	zielportnummer	uint16

	länge		uint16
	prüfsumme	uint16
}

func (selbst *TBenutzerdatagrammkopf) Init(buffer_2 *TBenutzerdatagramprotocolKopfbuffer) {
	selbst.quellportnummer = Feldtounsignedinteger16(buffer_2.quellportnummer)
	selbst.zielportnummer = Feldtounsignedinteger16(buffer_2.zielportnummer)

	selbst.länge = Feldtounsignedinteger16(buffer_2.länge)
	selbst.prüfsumme = Feldtounsignedinteger16(buffer_2.prüfsumme)
}
func (selbst *TBenutzerdatagrammkopf) Setzenbuffer(buffer_2 *TBenutzerdatagramprotocolKopfbuffer) {

	buffer_2.quellportnummer = Unsignedinteger16toFeld(selbst.quellportnummer)
	buffer_2.zielportnummer = Unsignedinteger16toFeld(selbst.zielportnummer)

	buffer_2.länge = Unsignedinteger16toFeld(selbst.länge)
	buffer_2.prüfsumme = Unsignedinteger16toFeld(selbst.prüfsumme)

}

type IBenutzerdatagramprotocolhandler interface {
	GriffBenutzerdatagramprotocolNachricht(netzanschluss *TBenutzerdatagrammendpunkt, daten uintptr, größe uint16)
}

type TBenutzerdatagramprotocolhandler struct {
}

func (selbst *TBenutzerdatagramprotocolhandler) Init(backend TNetzverbundprotokollanbieter) {
}
func (selbst *TBenutzerdatagramprotocolhandler) GriffBenutzerdatagramprotocolNachricht(netzanschluss *TBenutzerdatagrammendpunkt, daten uintptr, größe uint16) {
}

type IBenutzerdatagramprotocolNetzanschluss interface {
	GriffBenutzerdatagramprotocolNachricht(daten uintptr, größe uint16)
}
type TBenutzerdatagrammendpunkt struct {
	entferntAnschlussNummer	uint16
	entferntip		uint32
	lokalAnschlussNummer	uint16
	lokalip			uint32

	listening	bool
}

var udpprovider TBenutzerdatagramprotocolprovider
var udphandler IBenutzerdatagramprotocolhandler

func (selbst *TBenutzerdatagrammendpunkt) Testen() {
}
func (selbst *TBenutzerdatagrammendpunkt) Init(pudpprovider TBenutzerdatagramprotocolprovider, pudphandler IBenutzerdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	selbst.listening = false
}
func (selbst *TBenutzerdatagrammendpunkt) GriffBenutzerdatagramprotocolNachricht(daten uintptr, größe uint16) {
	if udphandler != nil {
		udphandler.GriffBenutzerdatagramprotocolNachricht(selbst, daten, größe)
	}
}
func (selbst *TBenutzerdatagrammendpunkt) Senden(pDaten []byte, größe uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(größe); i++ {
		buffer_2[i] = pDaten[i]
	}
	var daten = uintptr(Pointer(&buffer_2))
	udpprovider.Senden(selbst, daten, größe)
}
func (selbst *TBenutzerdatagrammendpunkt) Trennen() {
	udpprovider.Trennen(selbst)
}

type TBenutzerdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TBenutzerdatagrammendpunkt
var nummersockets int
var freiAnschluss uint16

func (selbst *TBenutzerdatagramprotocolprovider) Init(pipprovider TNetzverbundprotokollanbieter, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	nummersockets = 0
	freiAnschluss = 1024
}
func (selbst *TBenutzerdatagramprotocolprovider) Internetprotocolreceivewhen(quelleipaddressNetzwerkByteorder uint32, zielipaddressNetzwerkByteorder uint32, internetprotocolpayload uintptr, größe uint32) bool {
	if größe < udpKopfGröße {
		return false
	}

	var buffer_2 *TBenutzerdatagramprotocolKopfbuffer = (*TBenutzerdatagramprotocolKopfbuffer)(Pointer(internetprotocolpayload))
	var msg TBenutzerdatagrammkopf
	msg.Init(buffer_2)

	var netzanschluss *TBenutzerdatagrammendpunkt = nil

	for i := 0; i < nummersockets && netzanschluss == nil; i++ {
		if sockets[i].lokalAnschlussNummer == msg.zielportnummer && sockets[i].lokalip == zielipaddressNetzwerkByteorder && sockets[i].listening == true {
			netzanschluss = &sockets[i]
			netzanschluss.listening = false
			netzanschluss.entferntAnschlussNummer = msg.quellportnummer
			netzanschluss.entferntip = quelleipaddressNetzwerkByteorder
		} else if sockets[i].lokalAnschlussNummer == msg.zielportnummer && sockets[i].lokalip == zielipaddressNetzwerkByteorder && sockets[i].entferntAnschlussNummer == msg.quellportnummer && sockets[i].entferntip == quelleipaddressNetzwerkByteorder {
			netzanschluss = &sockets[i]

		}
	}

	msg.Setzenbuffer(buffer_2)
	if netzanschluss != nil {
		netzanschluss.GriffBenutzerdatagramprotocolNachricht(internetprotocolpayload+uintptr(udpKopfGröße), uint16(größe-udpKopfGröße))
	}

	return false
}

func (selbst *TBenutzerdatagramprotocolprovider) Verbinden(ip uint32, anschluss uint16) *TBenutzerdatagrammendpunkt {
	var speicherVerwalter = &TSpeicherVerwalter{}
	var netzanschluss = (*TBenutzerdatagrammendpunkt)(speicherVerwalter.Speicher_reservieren(50))

	if netzanschluss != nil {

		netzanschluss.Init(*selbst, nil)
		netzanschluss.entferntAnschlussNummer = anschluss
		netzanschluss.entferntip = ip
		netzanschluss.lokalAnschlussNummer = freiAnschluss
		freiAnschluss++
		netzanschluss.lokalip = uint32((*iphandler.Providerget()).Getipaddress())

		netzanschluss.entferntAnschlussNummer = Unsignedinteger16r(netzanschluss.entferntAnschlussNummer)
		netzanschluss.lokalAnschlussNummer = Unsignedinteger16r(netzanschluss.lokalAnschlussNummer)

		sockets[nummersockets] = *netzanschluss
		nummersockets++

	}
	return netzanschluss

}
func (selbst *TBenutzerdatagramprotocolprovider) Listen(anschluss uint16) *TBenutzerdatagrammendpunkt {
	var netzanschluss = &TBenutzerdatagrammendpunkt{}
	netzanschluss = nil
	if netzanschluss != nil {
		netzanschluss.Init(*selbst, nil)
		netzanschluss.listening = true
		netzanschluss.lokalAnschlussNummer = anschluss
		netzanschluss.lokalip = uint32((*iphandler.Providerget()).Getipaddress())

		netzanschluss.lokalAnschlussNummer = Unsignedinteger16r(netzanschluss.lokalAnschlussNummer)
	}
	return netzanschluss
}
func (selbst *TBenutzerdatagramprotocolprovider) Trennen(netzanschluss *TBenutzerdatagrammendpunkt) {
	for i := 0; i < nummersockets && netzanschluss == nil; i++ {
		if sockets[i] == *netzanschluss {
			nummersockets--
			sockets[i] = sockets[nummersockets]
			break
		}
	}
}
func (selbst *TBenutzerdatagramprotocolprovider) Senden(netzanschluss *TBenutzerdatagrammendpunkt, pDaten uintptr, größe uint16) {
	var gesamtLänge = uint32(größe) + udpKopfGröße

	var buffer_2 [4096]byte

	var msgbuffer = (*TBenutzerdatagramprotocolKopfbuffer)(Pointer(&buffer_2))

	var msg = TBenutzerdatagrammkopf{}

	msg.quellportnummer = netzanschluss.lokalAnschlussNummer
	msg.zielportnummer = netzanschluss.entferntAnschlussNummer
	msg.länge = Unsignedinteger16r(uint16(gesamtLänge))

	msg.prüfsumme = 0x0
	msg.Setzenbuffer(msgbuffer)

	var datenByte [4096]byte = *(*[4096]byte)(Pointer(pDaten))
	for i := 0; i < int(größe); i++ {
		buffer_2[int(udpKopfGröße)+i] = datenByte[i]
	}

	var daten uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Senden(netzanschluss.entferntip, 0x11, daten, gesamtLänge)

}
func (selbst *TBenutzerdatagramprotocolprovider) Bindung(netzanschluss *TBenutzerdatagrammendpunkt, handler *TBenutzerdatagramprotocolhandler) {
}
