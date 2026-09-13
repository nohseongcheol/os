package protocollo_dei_messaggi_di_controllo_della_rete_interconnessa

import . "unsafe"
import . "console"
import . "memoriamanager"
import . "trama_della_rete_a_mezzo_condiviso"
import . "protocollo_di_rete_interconnessa_4"
import . "util"

var icmpconsole = TConsole{}

type TInternetCtrlMessaggioprotocolMessaggiobuffer struct {
	Tipo	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpDimensione int = 64

type TInternetCtrlMessaggioprotocolMessaggio struct {
	Tipo	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (séstesso *TInternetCtrlMessaggioprotocolMessaggio) Init(buffer_2 TInternetCtrlMessaggioprotocolMessaggiobuffer) {
	séstesso.Tipo = buffer_2.Tipo
	séstesso.code = buffer_2.code

	séstesso.checksum = Unsignedinteger16r(Serietounsignedinteger16(buffer_2.checksum))
	séstesso.data = Unsignedinteger32r(Serietounsignedinteger32(buffer_2.data))
}

func (séstesso *TInternetCtrlMessaggioprotocolMessaggio) Impostabuffer(buffer_2 *TInternetCtrlMessaggioprotocolMessaggiobuffer) {
	buffer_2.Tipo = séstesso.Tipo
	buffer_2.code = séstesso.code

	buffer_2.checksum = Unsignedinteger16toSerie(séstesso.checksum)
	buffer_2.data = Unsignedinteger32toSerie(séstesso.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var protocollo_dei_messaggi_di_controllo_della_rete_interconnessa *TProtocollo_dei_messaggi_di_controllo_della_rete_interconnessa

func (séstesso *Icmphandler) Internetprotocolreceivewhen(origineipaddressRetebyteorder uint32, destinazioneipaddressRetebyteorder uint32, dataPuntatore uintptr, dimensione uint32) bool {
	return protocollo_dei_messaggi_di_controllo_della_rete_interconnessa.Internetprotocolreceivewhen(origineipaddressRetebyteorder, destinazioneipaddressRetebyteorder, dataPuntatore, dimensione)
}

var iphandler IInternetprotocolhandler

type TProtocollo_dei_messaggi_di_controllo_della_rete_interconnessa struct {
}

func (séstesso *TProtocollo_dei_messaggi_di_controllo_della_rete_interconnessa) Init(backend TFornitore_del_protocollo_di_rete_interconnessa, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	protocollo_dei_messaggi_di_controllo_della_rete_interconnessa = séstesso
}
func (séstesso *TProtocollo_dei_messaggi_di_controllo_della_rete_interconnessa) Internetprotocolreceivewhen(origineipaddressRetebyteorder uint32, destinazioneipaddressRetebyteorder uint32, dataPuntatore uintptr, dimensione uint32) bool {
	if dimensione < uint32(icmpDimensione) {
		return false
	}

	var buffer_2 *TInternetCtrlMessaggioprotocolMessaggiobuffer = (*TInternetCtrlMessaggioprotocolMessaggiobuffer)(Pointer(dataPuntatore))
	var msg TInternetCtrlMessaggioprotocolMessaggio = TInternetCtrlMessaggioprotocolMessaggio{}
	msg.Init(*buffer_2)

	icmpconsole.MStampa(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Stampa(uint16(msg.Tipo))
	icmpconsole.MStampa(([]byte)(":"))

	switch msg.Tipo {
	case 0:
		icmpconsole.MStampa(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MStampa(([]byte)("ping send "))
		msg.Tipo = 0

		msg.checksum = 0
		msg.Impostabuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataPuntatore)), uint32(icmpDimensione))

		msg.Impostabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (séstesso *TProtocollo_dei_messaggi_di_controllo_della_rete_interconnessa) EchorequestSpedisci(ipRetebyteorder uint32) bool {
	var protocollo_dei_messaggi_di_controllo_della_rete_interconnessa TInternetCtrlMessaggioprotocolMessaggio = TInternetCtrlMessaggioprotocolMessaggio{}

	var memoriamanager = &TMemoriamanager{}
	var buffer_2 = (*TInternetCtrlMessaggioprotocolMessaggiobuffer)(memoriamanager.Alloca_memoria(1024))

	protocollo_dei_messaggi_di_controllo_della_rete_interconnessa.Tipo = 8
	protocollo_dei_messaggi_di_controllo_della_rete_interconnessa.code = 0
	protocollo_dei_messaggi_di_controllo_della_rete_interconnessa.data = 0x3713
	protocollo_dei_messaggi_di_controllo_della_rete_interconnessa.checksum = 0
	protocollo_dei_messaggi_di_controllo_della_rete_interconnessa.Impostabuffer(buffer_2)
	protocollo_dei_messaggi_di_controllo_della_rete_interconnessa.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpDimensione))
	protocollo_dei_messaggi_di_controllo_della_rete_interconnessa.Impostabuffer(buffer_2)

	var dataPuntatore uintptr = uintptr(Pointer(buffer_2))
	iphandler.Spedisci(ipRetebyteorder, 0x01, dataPuntatore, uint32(icmpDimensione))

	return false

}
