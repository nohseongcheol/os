/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protocollo_dei_datagrammi_utente

import . "unsafe"
import . "console"
import . "util"
import . "memoriamanager"
import . "protocollo_di_rete_interconnessa_4"

var udpconsole = TConsole{}

type TUtentedatagramprotocolheaderbuffer struct {
	numero_della_porta_sorgente	[2]byte
	numero_della_porta_di_destinazione	[2]byte

	durata		[2]byte
	checksum	[2]byte
}

var udpheaderDimensione uint32 = 8

type TIntestazione_dei_datagrammi_utente struct {
	numero_della_porta_sorgente	uint16
	numero_della_porta_di_destinazione	uint16

	durata		uint16
	checksum	uint16
}

func (séstesso *TIntestazione_dei_datagrammi_utente) Init(buffer_2 *TUtentedatagramprotocolheaderbuffer) {
	séstesso.numero_della_porta_sorgente = Serietounsignedinteger16(buffer_2.numero_della_porta_sorgente)
	séstesso.numero_della_porta_di_destinazione = Serietounsignedinteger16(buffer_2.numero_della_porta_di_destinazione)

	séstesso.durata = Serietounsignedinteger16(buffer_2.durata)
	séstesso.checksum = Serietounsignedinteger16(buffer_2.checksum)
}
func (séstesso *TIntestazione_dei_datagrammi_utente) Impostabuffer(buffer_2 *TUtentedatagramprotocolheaderbuffer) {

	buffer_2.numero_della_porta_sorgente = Unsignedinteger16toSerie(séstesso.numero_della_porta_sorgente)
	buffer_2.numero_della_porta_di_destinazione = Unsignedinteger16toSerie(séstesso.numero_della_porta_di_destinazione)

	buffer_2.durata = Unsignedinteger16toSerie(séstesso.durata)
	buffer_2.checksum = Unsignedinteger16toSerie(séstesso.checksum)

}

type IUtentedatagramprotocolhandler interface {
	ManigliaUtentedatagramprotocolMessaggio(socket *TEstremo_di_comunicazione_dei_datagrammi_utente, data uintptr, dimensione uint16)
}

type TUtentedatagramprotocolhandler struct {
}

func (séstesso *TUtentedatagramprotocolhandler) Init(backend TFornitore_del_protocollo_di_rete_interconnessa) {
}
func (séstesso *TUtentedatagramprotocolhandler) ManigliaUtentedatagramprotocolMessaggio(socket *TEstremo_di_comunicazione_dei_datagrammi_utente, data uintptr, dimensione uint16) {
}

type IUtentedatagramprotocolsocket interface {
	ManigliaUtentedatagramprotocolMessaggio(data uintptr, dimensione uint16)
}
type TEstremo_di_comunicazione_dei_datagrammi_utente struct {
	remotoPortaNumero	uint16
	remotoip		uint32
	localePortaNumero	uint16
	localeip		uint32

	listening	bool
}

var udpprovider TUtentedatagramprotocolprovider
var udphandler IUtentedatagramprotocolhandler

func (séstesso *TEstremo_di_comunicazione_dei_datagrammi_utente) Prova() {
}
func (séstesso *TEstremo_di_comunicazione_dei_datagrammi_utente) Init(pudpprovider TUtentedatagramprotocolprovider, pudphandler IUtentedatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	séstesso.listening = false
}
func (séstesso *TEstremo_di_comunicazione_dei_datagrammi_utente) ManigliaUtentedatagramprotocolMessaggio(data uintptr, dimensione uint16) {
	if udphandler != nil {
		udphandler.ManigliaUtentedatagramprotocolMessaggio(séstesso, data, dimensione)
	}
}
func (séstesso *TEstremo_di_comunicazione_dei_datagrammi_utente) Spedisci(pdata []byte, dimensione uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(dimensione); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Spedisci(séstesso, data, dimensione)
}
func (séstesso *TEstremo_di_comunicazione_dei_datagrammi_utente) Disconnetti() {
	udpprovider.Disconnetti(séstesso)
}

type TUtentedatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TEstremo_di_comunicazione_dei_datagrammi_utente
var numerosockets int
var liberoPorta uint16

func (séstesso *TUtentedatagramprotocolprovider) Init(pipprovider TFornitore_del_protocollo_di_rete_interconnessa, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	numerosockets = 0
	liberoPorta = 1024
}
func (séstesso *TUtentedatagramprotocolprovider) Internetprotocolreceivewhen(origineipaddressRetebyteorder uint32, destinazioneipaddressRetebyteorder uint32, internetprotocolpayload uintptr, dimensione uint32) bool {
	if dimensione < udpheaderDimensione {
		return false
	}

	var buffer_2 *TUtentedatagramprotocolheaderbuffer = (*TUtentedatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TIntestazione_dei_datagrammi_utente
	msg.Init(buffer_2)

	var socket *TEstremo_di_comunicazione_dei_datagrammi_utente = nil

	for i := 0; i < numerosockets && socket == nil; i++ {
		if sockets[i].localePortaNumero == msg.numero_della_porta_di_destinazione && sockets[i].localeip == destinazioneipaddressRetebyteorder && sockets[i].listening == true {
			socket = &sockets[i]
			socket.listening = false
			socket.remotoPortaNumero = msg.numero_della_porta_sorgente
			socket.remotoip = origineipaddressRetebyteorder
		} else if sockets[i].localePortaNumero == msg.numero_della_porta_di_destinazione && sockets[i].localeip == destinazioneipaddressRetebyteorder && sockets[i].remotoPortaNumero == msg.numero_della_porta_sorgente && sockets[i].remotoip == origineipaddressRetebyteorder {
			socket = &sockets[i]

		}
	}

	msg.Impostabuffer(buffer_2)
	if socket != nil {
		socket.ManigliaUtentedatagramprotocolMessaggio(internetprotocolpayload+uintptr(udpheaderDimensione), uint16(dimensione-udpheaderDimensione))
	}

	return false
}

func (séstesso *TUtentedatagramprotocolprovider) Connetti(ip uint32, porta uint16) *TEstremo_di_comunicazione_dei_datagrammi_utente {
	var memoriamanager = &TMemoriamanager{}
	var socket = (*TEstremo_di_comunicazione_dei_datagrammi_utente)(memoriamanager.Alloca_memoria(50))

	if socket != nil {

		socket.Init(*séstesso, nil)
		socket.remotoPortaNumero = porta
		socket.remotoip = ip
		socket.localePortaNumero = liberoPorta
		liberoPorta++
		socket.localeip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.remotoPortaNumero = Unsignedinteger16r(socket.remotoPortaNumero)
		socket.localePortaNumero = Unsignedinteger16r(socket.localePortaNumero)

		sockets[numerosockets] = *socket
		numerosockets++

	}
	return socket

}
func (séstesso *TUtentedatagramprotocolprovider) Listen(porta uint16) *TEstremo_di_comunicazione_dei_datagrammi_utente {
	var socket = &TEstremo_di_comunicazione_dei_datagrammi_utente{}
	socket = nil
	if socket != nil {
		socket.Init(*séstesso, nil)
		socket.listening = true
		socket.localePortaNumero = porta
		socket.localeip = uint32((*iphandler.Providerget()).Getipaddress())

		socket.localePortaNumero = Unsignedinteger16r(socket.localePortaNumero)
	}
	return socket
}
func (séstesso *TUtentedatagramprotocolprovider) Disconnetti(socket *TEstremo_di_comunicazione_dei_datagrammi_utente) {
	for i := 0; i < numerosockets && socket == nil; i++ {
		if sockets[i] == *socket {
			numerosockets--
			sockets[i] = sockets[numerosockets]
			break
		}
	}
}
func (séstesso *TUtentedatagramprotocolprovider) Spedisci(socket *TEstremo_di_comunicazione_dei_datagrammi_utente, pdata uintptr, dimensione uint16) {
	var totaleDurata = uint32(dimensione) + udpheaderDimensione

	var buffer_2 [4096]byte

	var msgbuffer = (*TUtentedatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TIntestazione_dei_datagrammi_utente{}

	msg.numero_della_porta_sorgente = socket.localePortaNumero
	msg.numero_della_porta_di_destinazione = socket.remotoPortaNumero
	msg.durata = Unsignedinteger16r(uint16(totaleDurata))

	msg.checksum = 0x0
	msg.Impostabuffer(msgbuffer)

	var dataByte [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(dimensione); i++ {
		buffer_2[int(udpheaderDimensione)+i] = dataByte[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Spedisci(socket.remotoip, 0x11, data, totaleDurata)

}
func (séstesso *TUtentedatagramprotocolprovider) Bind(socket *TEstremo_di_comunicazione_dei_datagrammi_utente, handler *TUtentedatagramprotocolhandler) {
}
