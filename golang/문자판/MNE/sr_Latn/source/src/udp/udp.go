/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package udp

import . "unsafe"
import . "konzola"
import . "util"
import . "memorijamanager"
import . "ipv4"

var udpKonzola = TKonzola{}

type TKorisnikdatagramprotocolheaderbuffer struct {
	izvorPortbroj		[2]byte
	odredištePortbroj	[2]byte

	dužina		[2]byte
	checksum	[2]byte
}

var udpheaderVeličina uint32 = 8

type TKorisnikdatagramprotocolheader struct {
	izvorPortbroj		uint16
	odredištePortbroj	uint16

	dužina		uint16
	checksum	uint16
}

func (isti *TKorisnikdatagramprotocolheader) Init(buffer_2 *TKorisnikdatagramprotocolheaderbuffer) {
	isti.izvorPortbroj = Niztounsignedinteger16(buffer_2.izvorPortbroj)
	isti.odredištePortbroj = Niztounsignedinteger16(buffer_2.odredištePortbroj)

	isti.dužina = Niztounsignedinteger16(buffer_2.dužina)
	isti.checksum = Niztounsignedinteger16(buffer_2.checksum)
}
func (isti *TKorisnikdatagramprotocolheader) Skupbuffer(buffer_2 *TKorisnikdatagramprotocolheaderbuffer) {

	buffer_2.izvorPortbroj = Unsignedinteger16toNiz(isti.izvorPortbroj)
	buffer_2.odredištePortbroj = Unsignedinteger16toNiz(isti.odredištePortbroj)

	buffer_2.dužina = Unsignedinteger16toNiz(isti.dužina)
	buffer_2.checksum = Unsignedinteger16toNiz(isti.checksum)

}

type IKorisnikdatagramprotocolhandler interface {
	RučkaKorisnikdatagramprotocolporuka(priključnica *TKorisnikdatagramprotocolPriključnica, data uintptr, veličina uint16)
}

type TKorisnikdatagramprotocolhandler struct {
}

func (isti *TKorisnikdatagramprotocolhandler) Init(backend TInternetprotocolprovider) {
}
func (isti *TKorisnikdatagramprotocolhandler) RučkaKorisnikdatagramprotocolporuka(priključnica *TKorisnikdatagramprotocolPriključnica, data uintptr, veličina uint16) {
}

type IKorisnikdatagramprotocolPriključnica interface {
	RučkaKorisnikdatagramprotocolporuka(data uintptr, veličina uint16)
}
type TKorisnikdatagramprotocolPriključnica struct {
	udaljenoPortbroj	uint16
	udaljenoip	uint32
	lokalnaPortbroj	uint16
	lokalnaip	uint32

	listening	bool
}

var udpprovider TKorisnikdatagramprotocolprovider
var udphandler IKorisnikdatagramprotocolhandler

func (isti *TKorisnikdatagramprotocolPriključnica) Test() {
}
func (isti *TKorisnikdatagramprotocolPriključnica) Init(pudpprovider TKorisnikdatagramprotocolprovider, pudphandler IKorisnikdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	isti.listening = false
}
func (isti *TKorisnikdatagramprotocolPriključnica) RučkaKorisnikdatagramprotocolporuka(data uintptr, veličina uint16) {
	if udphandler != nil {
		udphandler.RučkaKorisnikdatagramprotocolporuka(isti, data, veličina)
	}
}
func (isti *TKorisnikdatagramprotocolPriključnica) Pošalji(pdata []byte, veličina uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(veličina); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Pošalji(isti, data, veličina)
}
func (isti *TKorisnikdatagramprotocolPriključnica) Prekinivezu() {
	udpprovider.Prekinivezu(isti)
}

type TKorisnikdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TKorisnikdatagramprotocolPriključnica
var brojsockets int
var slobodnoPort uint16

func (isti *TKorisnikdatagramprotocolprovider) Init(pipprovider TInternetprotocolprovider, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	brojsockets = 0
	slobodnoPort = 1024
}
func (isti *TKorisnikdatagramprotocolprovider) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, internetprotocolpayload uintptr, veličina uint32) bool {
	if veličina < udpheaderVeličina {
		return false
	}

	var buffer_2 *TKorisnikdatagramprotocolheaderbuffer = (*TKorisnikdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TKorisnikdatagramprotocolheader
	msg.Init(buffer_2)

	var priključnica *TKorisnikdatagramprotocolPriključnica = nil

	for i := 0; i < brojsockets && priključnica == nil; i++ {
		if sockets[i].lokalnaPortbroj == msg.odredištePortbroj && sockets[i].lokalnaip == odredišteipaddressMrežabyteorder && sockets[i].listening == true {
			priključnica = &sockets[i]
			priključnica.listening = false
			priključnica.udaljenoPortbroj = msg.izvorPortbroj
			priključnica.udaljenoip = izvoripaddressMrežabyteorder
		} else if sockets[i].lokalnaPortbroj == msg.odredištePortbroj && sockets[i].lokalnaip == odredišteipaddressMrežabyteorder && sockets[i].udaljenoPortbroj == msg.izvorPortbroj && sockets[i].udaljenoip == izvoripaddressMrežabyteorder {
			priključnica = &sockets[i]

		}
	}

	msg.Skupbuffer(buffer_2)
	if priključnica != nil {
		priključnica.RučkaKorisnikdatagramprotocolporuka(internetprotocolpayload+uintptr(udpheaderVeličina), uint16(veličina-udpheaderVeličina))
	}

	return false
}

func (isti *TKorisnikdatagramprotocolprovider) Povežise(ip uint32, port uint16) *TKorisnikdatagramprotocolPriključnica {
	var memorijamanager = &TMemorijamanager{}
	var priključnica = (*TKorisnikdatagramprotocolPriključnica)(memorijamanager.Malloc(50))

	if priključnica != nil {

		priključnica.Init(*isti, nil)
		priključnica.udaljenoPortbroj = port
		priključnica.udaljenoip = ip
		priključnica.lokalnaPortbroj = slobodnoPort
		slobodnoPort++
		priključnica.lokalnaip = uint32((*iphandler.Providerget()).Getipaddress())

		priključnica.udaljenoPortbroj = Unsignedinteger16r(priključnica.udaljenoPortbroj)
		priključnica.lokalnaPortbroj = Unsignedinteger16r(priključnica.lokalnaPortbroj)

		sockets[brojsockets] = *priključnica
		brojsockets++

	}
	return priključnica

}
func (isti *TKorisnikdatagramprotocolprovider) Listen(port uint16) *TKorisnikdatagramprotocolPriključnica {
	var priključnica = &TKorisnikdatagramprotocolPriključnica{}
	priključnica = nil
	if priključnica != nil {
		priključnica.Init(*isti, nil)
		priključnica.listening = true
		priključnica.lokalnaPortbroj = port
		priključnica.lokalnaip = uint32((*iphandler.Providerget()).Getipaddress())

		priključnica.lokalnaPortbroj = Unsignedinteger16r(priključnica.lokalnaPortbroj)
	}
	return priključnica
}
func (isti *TKorisnikdatagramprotocolprovider) Prekinivezu(priključnica *TKorisnikdatagramprotocolPriključnica) {
	for i := 0; i < brojsockets && priključnica == nil; i++ {
		if sockets[i] == *priključnica {
			brojsockets--
			sockets[i] = sockets[brojsockets]
			break
		}
	}
}
func (isti *TKorisnikdatagramprotocolprovider) Pošalji(priključnica *TKorisnikdatagramprotocolPriključnica, pdata uintptr, veličina uint16) {
	var ukupnoDužina = uint32(veličina) + udpheaderVeličina

	var buffer_2 [4096]byte

	var msgbuffer = (*TKorisnikdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TKorisnikdatagramprotocolheader{}

	msg.izvorPortbroj = priključnica.lokalnaPortbroj
	msg.odredištePortbroj = priključnica.udaljenoPortbroj
	msg.dužina = Unsignedinteger16r(uint16(ukupnoDužina))

	msg.checksum = 0x0
	msg.Skupbuffer(msgbuffer)

	var dataBajtova [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(veličina); i++ {
		buffer_2[int(udpheaderVeličina)+i] = dataBajtova[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Pošalji(priključnica.udaljenoip, 0x11, data, ukupnoDužina)

}
func (isti *TKorisnikdatagramprotocolprovider) Bind(priključnica *TKorisnikdatagramprotocolPriključnica, handler *TKorisnikdatagramprotocolhandler) {
}
