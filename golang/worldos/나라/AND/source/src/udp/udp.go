/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "consola"
import . "util"
import . "memòriamanager"
import . "ipv4"

var udpConsola = TConsola{}

type TUsuaridatagramprotocolheaderbuffer struct {
	origenportNombre	[2]byte
	destinacióportNombre	[2]byte

	durada		[2]byte
	checksum	[2]byte
}

var udpheaderMida uint32 = 8

type TUsuaridatagramprotocolheader struct {
	origenportNombre	uint16
	destinacióportNombre	uint16

	durada		uint16
	checksum	uint16
}

func (unmateix *TUsuaridatagramprotocolheader) Init(buffer_2 *TUsuaridatagramprotocolheaderbuffer) {
	unmateix.origenportNombre = Matriutounsignedinteger16(buffer_2.origenportNombre)
	unmateix.destinacióportNombre = Matriutounsignedinteger16(buffer_2.destinacióportNombre)

	unmateix.durada = Matriutounsignedinteger16(buffer_2.durada)
	unmateix.checksum = Matriutounsignedinteger16(buffer_2.checksum)
}
func (unmateix *TUsuaridatagramprotocolheader) Estableixbuffer(buffer_2 *TUsuaridatagramprotocolheaderbuffer) {

	buffer_2.origenportNombre = Unsignedinteger16toMatriu(unmateix.origenportNombre)
	buffer_2.destinacióportNombre = Unsignedinteger16toMatriu(unmateix.destinacióportNombre)

	buffer_2.durada = Unsignedinteger16toMatriu(unmateix.durada)
	buffer_2.checksum = Unsignedinteger16toMatriu(unmateix.checksum)

}

type IUsuaridatagramprotocolhandler interface {
	GestorUsuaridatagramprotocolMissatge(sòcol *TUsuaridatagramprotocolSòcol, data uintptr, mida uint16)
}

type TUsuaridatagramprotocolhandler struct {
}

func (unmateix *TUsuaridatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (unmateix *TUsuaridatagramprotocolhandler) GestorUsuaridatagramprotocolMissatge(sòcol *TUsuaridatagramprotocolSòcol, data uintptr, mida uint16) {
}

type IUsuaridatagramprotocolSòcol interface {
	GestorUsuaridatagramprotocolMissatge(data uintptr, mida uint16)
}
type TUsuaridatagramprotocolSòcol struct {
	remotportNombre	uint16
	remotip		uint32
	localportNombre	uint16
	localip		uint32

	listening	bool
}

var udpprovider TUsuaridatagramprotocolprovider
var udphandler IUsuaridatagramprotocolhandler

func (unmateix *TUsuaridatagramprotocolSòcol) Prova() {
}
func (unmateix *TUsuaridatagramprotocolSòcol) Init(pudpprovider TUsuaridatagramprotocolprovider, pudphandler IUsuaridatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	unmateix.listening = false
}
func (unmateix *TUsuaridatagramprotocolSòcol) GestorUsuaridatagramprotocolMissatge(data uintptr, mida uint16) {
	if udphandler != nil {
		udphandler.GestorUsuaridatagramprotocolMissatge(unmateix, data, mida)
	}
}
func (unmateix *TUsuaridatagramprotocolSòcol) Envia(pdata []byte, mida uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(mida); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Envia(unmateix, data, mida)
}
func (unmateix *TUsuaridatagramprotocolSòcol) Desconnecta() {
	udpprovider.Desconnecta(unmateix)
}

type TUsuaridatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TUsuaridatagramprotocolSòcol
var nombresockets int
var lliureport uint16

func (unmateix *TUsuaridatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	nombresockets = 0
	lliureport = 1024
}
func (unmateix *TUsuaridatagramprotocolprovider) Internetprotocolreceivewhen(origenipAdreçaXarxabyteorder uint32, destinacióipAdreçaXarxabyteorder uint32, internetprotocolpayload uintptr, mida uint32) bool {
	if mida < udpheaderMida {
		return false
	}

	var buffer_2 *TUsuaridatagramprotocolheaderbuffer = (*TUsuaridatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TUsuaridatagramprotocolheader
	msg.Init(buffer_2)

	var sòcol *TUsuaridatagramprotocolSòcol = nil

	for i := 0; i < nombresockets && sòcol == nil; i++ {
		if sockets[i].localportNombre == msg.destinacióportNombre && sockets[i].localip == destinacióipAdreçaXarxabyteorder && sockets[i].listening == true {
			sòcol = &sockets[i]
			sòcol.listening = false
			sòcol.remotportNombre = msg.origenportNombre
			sòcol.remotip = origenipAdreçaXarxabyteorder
		} else if sockets[i].localportNombre == msg.destinacióportNombre && sockets[i].localip == destinacióipAdreçaXarxabyteorder && sockets[i].remotportNombre == msg.origenportNombre && sockets[i].remotip == origenipAdreçaXarxabyteorder {
			sòcol = &sockets[i]

		}
	}

	msg.Estableixbuffer(buffer_2)
	if sòcol != nil {
		sòcol.GestorUsuaridatagramprotocolMissatge(internetprotocolpayload+uintptr(udpheaderMida), uint16(mida-udpheaderMida))
	}

	return false
}

func (unmateix *TUsuaridatagramprotocolprovider) Connecta(ip uint32, port uint16) *TUsuaridatagramprotocolSòcol {
	var memòriamanager = &TMemòriamanager{}
	var sòcol = (*TUsuaridatagramprotocolSòcol)(memòriamanager.Malloc(50))

	if sòcol != nil {

		sòcol.Init(*unmateix, nil)
		sòcol.remotportNombre = port
		sòcol.remotip = ip
		sòcol.localportNombre = lliureport
		lliureport++
		sòcol.localip = uint32((*iphandler.Providerget()).GetipAdreça())

		sòcol.remotportNombre = Unsignedinteger16r(sòcol.remotportNombre)
		sòcol.localportNombre = Unsignedinteger16r(sòcol.localportNombre)

		sockets[nombresockets] = *sòcol
		nombresockets++

	}
	return sòcol

}
func (unmateix *TUsuaridatagramprotocolprovider) Listen(port uint16) *TUsuaridatagramprotocolSòcol {
	var sòcol = &TUsuaridatagramprotocolSòcol{}
	sòcol = nil
	if sòcol != nil {
		sòcol.Init(*unmateix, nil)
		sòcol.listening = true
		sòcol.localportNombre = port
		sòcol.localip = uint32((*iphandler.Providerget()).GetipAdreça())

		sòcol.localportNombre = Unsignedinteger16r(sòcol.localportNombre)
	}
	return sòcol
}
func (unmateix *TUsuaridatagramprotocolprovider) Desconnecta(sòcol *TUsuaridatagramprotocolSòcol) {
	for i := 0; i < nombresockets && sòcol == nil; i++ {
		if sockets[i] == *sòcol {
			nombresockets--
			sockets[i] = sockets[nombresockets]
			break
		}
	}
}
func (unmateix *TUsuaridatagramprotocolprovider) Envia(sòcol *TUsuaridatagramprotocolSòcol, pdata uintptr, mida uint16) {
	var totalDurada = uint32(mida) + udpheaderMida

	var buffer_2 [4096]byte

	var msgbuffer = (*TUsuaridatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TUsuaridatagramprotocolheader{}

	msg.origenportNombre = sòcol.localportNombre
	msg.destinacióportNombre = sòcol.remotportNombre
	msg.durada = Unsignedinteger16r(uint16(totalDurada))

	msg.checksum = 0x0
	msg.Estableixbuffer(msgbuffer)

	var databytes [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(mida); i++ {
		buffer_2[int(udpheaderMida)+i] = databytes[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Envia(sòcol.remotip, 0x11, data, totalDurada)

}
func (unmateix *TUsuaridatagramprotocolprovider) Vincula(sòcol *TUsuaridatagramprotocolSòcol, handler *TUsuaridatagramprotocolhandler) {
}
