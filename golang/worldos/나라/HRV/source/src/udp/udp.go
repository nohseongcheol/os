/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "console"
import . "util"
import . "memorijamanager"
import . "ipv4"

var udpconsole = TConsole{}

type TKorisnikdatagramprotocolheaderbuffer struct {
	izvorportBROJ		[2]byte
	odredišteportBROJ	[2]byte

	dužina		[2]byte
	checksum	[2]byte
}

var udpheaderVeličina uint32 = 8

type TKorisnikdatagramprotocolheader struct {
	izvorportBROJ		uint16
	odredišteportBROJ	uint16

	dužina		uint16
	checksum	uint16
}

func (sam *TKorisnikdatagramprotocolheader) Init(buffer_2 *TKorisnikdatagramprotocolheaderbuffer) {
	sam.izvorportBROJ = Niztounsignedinteger16(buffer_2.izvorportBROJ)
	sam.odredišteportBROJ = Niztounsignedinteger16(buffer_2.odredišteportBROJ)

	sam.dužina = Niztounsignedinteger16(buffer_2.dužina)
	sam.checksum = Niztounsignedinteger16(buffer_2.checksum)
}
func (sam *TKorisnikdatagramprotocolheader) Postavibuffer(buffer_2 *TKorisnikdatagramprotocolheaderbuffer) {

	buffer_2.izvorportBROJ = Unsignedinteger16toNiz(sam.izvorportBROJ)
	buffer_2.odredišteportBROJ = Unsignedinteger16toNiz(sam.odredišteportBROJ)

	buffer_2.dužina = Unsignedinteger16toNiz(sam.dužina)
	buffer_2.checksum = Unsignedinteger16toNiz(sam.checksum)

}

type IKorisnikdatagramprotocolhandler interface {
	RučkaKorisnikdatagramprotocolPORUKA(utorsocket *TKorisnikdatagramprotocolUtorsocket, data uintptr, veličina uint16)
}

type TKorisnikdatagramprotocolhandler struct {
}

func (sam *TKorisnikdatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (sam *TKorisnikdatagramprotocolhandler) RučkaKorisnikdatagramprotocolPORUKA(utorsocket *TKorisnikdatagramprotocolUtorsocket, data uintptr, veličina uint16) {
}

type IKorisnikdatagramprotocolUtorsocket interface {
	RučkaKorisnikdatagramprotocolPORUKA(data uintptr, veličina uint16)
}
type TKorisnikdatagramprotocolUtorsocket struct {
	udaljenoportBROJ	uint16
	udaljenoip		uint32
	localportBROJ		uint16
	localip			uint32

	listening	bool
}

var udpprovider TKorisnikdatagramprotocolprovider
var udphandler IKorisnikdatagramprotocolhandler

func (sam *TKorisnikdatagramprotocolUtorsocket) Provjeri() {
}
func (sam *TKorisnikdatagramprotocolUtorsocket) Init(pudpprovider TKorisnikdatagramprotocolprovider, pudphandler IKorisnikdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	sam.listening = false
}
func (sam *TKorisnikdatagramprotocolUtorsocket) RučkaKorisnikdatagramprotocolPORUKA(data uintptr, veličina uint16) {
	if udphandler != nil {
		udphandler.RučkaKorisnikdatagramprotocolPORUKA(sam, data, veličina)
	}
}
func (sam *TKorisnikdatagramprotocolUtorsocket) Pošalji(pdata []byte, veličina uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(veličina); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Pošalji(sam, data, veličina)
}
func (sam *TKorisnikdatagramprotocolUtorsocket) Odspoji() {
	udpprovider.Odspoji(sam)
}

type TKorisnikdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TKorisnikdatagramprotocolUtorsocket
var bROJsockets int
var slobodnoport uint16

func (sam *TKorisnikdatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	bROJsockets = 0
	slobodnoport = 1024
}
func (sam *TKorisnikdatagramprotocolprovider) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, internetprotocolpayload uintptr, veličina uint32) bool {
	if veličina < udpheaderVeličina {
		return false
	}

	var buffer_2 *TKorisnikdatagramprotocolheaderbuffer = (*TKorisnikdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TKorisnikdatagramprotocolheader
	msg.Init(buffer_2)

	var utorsocket *TKorisnikdatagramprotocolUtorsocket = nil

	for i := 0; i < bROJsockets && utorsocket == nil; i++ {
		if sockets[i].localportBROJ == msg.odredišteportBROJ && sockets[i].localip == odredišteipaddressMrežabyteorder && sockets[i].listening == true {
			utorsocket = &sockets[i]
			utorsocket.listening = false
			utorsocket.udaljenoportBROJ = msg.izvorportBROJ
			utorsocket.udaljenoip = izvoripaddressMrežabyteorder
		} else if sockets[i].localportBROJ == msg.odredišteportBROJ && sockets[i].localip == odredišteipaddressMrežabyteorder && sockets[i].udaljenoportBROJ == msg.izvorportBROJ && sockets[i].udaljenoip == izvoripaddressMrežabyteorder {
			utorsocket = &sockets[i]

		}
	}

	msg.Postavibuffer(buffer_2)
	if utorsocket != nil {
		utorsocket.RučkaKorisnikdatagramprotocolPORUKA(internetprotocolpayload+uintptr(udpheaderVeličina), uint16(veličina-udpheaderVeličina))
	}

	return false
}

func (sam *TKorisnikdatagramprotocolprovider) Spojise(ip uint32, port uint16) *TKorisnikdatagramprotocolUtorsocket {
	var memorijamanager = &TMemorijamanager{}
	var utorsocket = (*TKorisnikdatagramprotocolUtorsocket)(memorijamanager.Malloc(50))

	if utorsocket != nil {

		utorsocket.Init(*sam, nil)
		utorsocket.udaljenoportBROJ = port
		utorsocket.udaljenoip = ip
		utorsocket.localportBROJ = slobodnoport
		slobodnoport++
		utorsocket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		utorsocket.udaljenoportBROJ = Unsignedinteger16r(utorsocket.udaljenoportBROJ)
		utorsocket.localportBROJ = Unsignedinteger16r(utorsocket.localportBROJ)

		sockets[bROJsockets] = *utorsocket
		bROJsockets++

	}
	return utorsocket

}
func (sam *TKorisnikdatagramprotocolprovider) Listen(port uint16) *TKorisnikdatagramprotocolUtorsocket {
	var utorsocket = &TKorisnikdatagramprotocolUtorsocket{}
	utorsocket = nil
	if utorsocket != nil {
		utorsocket.Init(*sam, nil)
		utorsocket.listening = true
		utorsocket.localportBROJ = port
		utorsocket.localip = uint32((*iphandler.Providerget()).Getipaddress())

		utorsocket.localportBROJ = Unsignedinteger16r(utorsocket.localportBROJ)
	}
	return utorsocket
}
func (sam *TKorisnikdatagramprotocolprovider) Odspoji(utorsocket *TKorisnikdatagramprotocolUtorsocket) {
	for i := 0; i < bROJsockets && utorsocket == nil; i++ {
		if sockets[i] == *utorsocket {
			bROJsockets--
			sockets[i] = sockets[bROJsockets]
			break
		}
	}
}
func (sam *TKorisnikdatagramprotocolprovider) Pošalji(utorsocket *TKorisnikdatagramprotocolUtorsocket, pdata uintptr, veličina uint16) {
	var ukupnoDužina = uint32(veličina) + udpheaderVeličina

	var buffer_2 [4096]byte

	var msgbuffer = (*TKorisnikdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TKorisnikdatagramprotocolheader{}

	msg.izvorportBROJ = utorsocket.localportBROJ
	msg.odredišteportBROJ = utorsocket.udaljenoportBROJ
	msg.dužina = Unsignedinteger16r(uint16(ukupnoDužina))

	msg.checksum = 0x0
	msg.Postavibuffer(msgbuffer)

	var dataBajtova [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(veličina); i++ {
		buffer_2[int(udpheaderVeličina)+i] = dataBajtova[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Pošalji(utorsocket.udaljenoip, 0x11, data, ukupnoDužina)

}
func (sam *TKorisnikdatagramprotocolprovider) Bind(utorsocket *TKorisnikdatagramprotocolUtorsocket, handler *TKorisnikdatagramprotocolhandler) {
}
