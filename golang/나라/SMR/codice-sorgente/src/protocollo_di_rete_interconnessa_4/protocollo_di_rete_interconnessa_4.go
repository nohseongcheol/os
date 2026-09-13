package protocollo_di_rete_interconnessa_4

import . "unsafe"
import . "util"
import . "console"
import . "trama_della_rete_a_mezzo_condiviso"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4Messaggiobuffer struct {
	lenver		byte
	tos		byte
	totaleDurata	[2]byte

	ident		[2]byte
	flageoffset	[2]byte

	oratolive	byte
	protocol	byte
	checksum	[2]byte

	origineipaddress	[4]byte
	destinazioneipaddress	[4]byte
}

var ipDimensione uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Messaggio struct {
	headerDurata	uint8
	versione	uint8
	tos		uint8
	totaleDurata	uint16

	ident		uint16
	flageoffset	uint16

	oratolive	uint8
	protocol	uint8
	checksum	uint16

	origineipaddress	uint32
	destinazioneipaddress	uint32
}

func (séstesso *TInternetprotocolv4Messaggio) Init(buffer_2 TInternetprotocolv4Messaggiobuffer) {

	séstesso.versione = ((buffer_2.lenver & 0xF0) >> 4)
	séstesso.headerDurata = buffer_2.lenver & 0x0F
	séstesso.tos = buffer_2.tos
	séstesso.totaleDurata = Unsignedinteger16r(Serietounsignedinteger16(buffer_2.totaleDurata))

	séstesso.ident = Unsignedinteger16r(Serietounsignedinteger16(buffer_2.ident))
	séstesso.flageoffset = Unsignedinteger16r(Serietounsignedinteger16(buffer_2.flageoffset))

	séstesso.oratolive = buffer_2.oratolive
	séstesso.protocol = buffer_2.protocol
	séstesso.checksum = Unsignedinteger16r(Serietounsignedinteger16(buffer_2.checksum))

	séstesso.origineipaddress = Unsignedinteger32r(Serietounsignedinteger32(buffer_2.origineipaddress))
	séstesso.destinazioneipaddress = Unsignedinteger32r(Serietounsignedinteger32(buffer_2.destinazioneipaddress))

}
func (séstesso *TInternetprotocolv4Messaggio) Impostabuffer(buffer_2 *TInternetprotocolv4Messaggiobuffer) {

	buffer_2.lenver = byte(((séstesso.versione & 0x0F) << 4) | (séstesso.headerDurata & 0x0F))
	buffer_2.tos = séstesso.tos
	buffer_2.totaleDurata = Unsignedinteger16toSerie(séstesso.totaleDurata)

	buffer_2.ident = Unsignedinteger16toSerie(séstesso.ident)
	buffer_2.flageoffset = Unsignedinteger16toSerie(séstesso.flageoffset)

	buffer_2.oratolive = séstesso.oratolive
	buffer_2.protocol = séstesso.protocol
	buffer_2.checksum = Unsignedinteger16toSerie(séstesso.checksum)

	buffer_2.origineipaddress = Unsignedinteger32toSerie(séstesso.origineipaddress)
	buffer_2.destinazioneipaddress = Unsignedinteger32toSerie(séstesso.destinazioneipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TFornitore_del_protocollo_di_rete_interconnessa, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(origineipaddressRetebyteorder uint32, destinazioneipaddressRetebyteorder uint32, dataPuntatore uintptr, dimensione uint32) bool
	Spedisci(destinazioneipaddressRetebyteorder uint32, pprotocol uint8, dataPuntatore uintptr, dimensione uint32)
	Providerget() *TFornitore_del_protocollo_di_rete_interconnessa
}

type TInternetprotocolhandler struct {
}

var ipethernetRiquadrohandler IpethernetRiquadrohandler = IpethernetRiquadrohandler{}
var protocol uint8

func (séstesso *TInternetprotocolhandler) Init(backend TFornitore_del_protocollo_di_rete_interconnessa, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (séstesso *TInternetprotocolhandler) Internetprotocolreceivewhen(origineipaddressRetebyteorder uint32, destinazioneipaddressRetebyteorder uint32, dataPuntatore uintptr, dimensione uint32) bool {
	ipconsole.MStampa(([]byte)("ipHandler:OnInternet"))
	return false
}
func (séstesso *TInternetprotocolhandler) Spedisci(destinazioneipaddressRetebyteorder uint32, pprotocol uint8, dataPuntatore uintptr, dimensione uint32) {

	fornitore_del_protocollo_di_rete_interconnessa.Spedisci(destinazioneipaddressRetebyteorder, pprotocol, dataPuntatore, dimensione)
}
func (séstesso *TInternetprotocolhandler) Providerget() *TFornitore_del_protocollo_di_rete_interconnessa {
	return &fornitore_del_protocollo_di_rete_interconnessa
}

type IpethernetRiquadrohandler struct {
	TEthernetRiquadrohandler
}

var fornitore_del_protocollo_di_rete_interconnessa TFornitore_del_protocollo_di_rete_interconnessa

func (séstesso *IpethernetRiquadrohandler) EthernetRiquadroreceivewhen(dataPuntatore uintptr, dimensione int) bool {
	ipconsole.MStampa(([]byte)("iphandler:onEtherfameRecv\n"))
	return fornitore_del_protocollo_di_rete_interconnessa.EthernetRiquadroreceivewhen(dataPuntatore, uint32(dimensione))

}

func (séstesso *IpethernetRiquadrohandler) Spedisci(destinazioneipaddressRetebyteorder uint64, dataPuntatore uintptr, dimensione uint32) {
	ipconsole.MStampa(([]byte)("ipefhandler:send\n"))
	var ethernetTipobe = Unsignedinteger16r(0x0800)
	séstesso.TEthernetRiquadrohandler.RiquadroSpedisci(destinazioneipaddressRetebyteorder, ethernetTipobe, dataPuntatore, dimensione)

}

var handler_2 [255]IInternetprotocolhandler

type TFornitore_del_protocollo_di_rete_interconnessa struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaschera	uint32
}

var efhandler IEthernetRiquadrohandler

func (séstesso *TFornitore_del_protocollo_di_rete_interconnessa) Init(pefprovider TFornitore_di_trame_di_rete_a_mezzo_condiviso, pefhandler IEthernetRiquadrohandler, arp Arpprovider, gatewayip uint32, subnetMaschera uint32) {

	efhandler = pefhandler
	efhandler.Impostahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	séstesso.arpprovider = arp
	séstesso.Gatewayip = gatewayip
	séstesso.SubnetMaschera = subnetMaschera
	fornitore_del_protocollo_di_rete_interconnessa = *séstesso
}
func (séstesso *TFornitore_del_protocollo_di_rete_interconnessa) EthernetRiquadroreceivewhen(ethernetRiquadropayload uintptr, dimensione uint32) bool {
	if dimensione < uint32(ipDimensione) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Messaggiobuffer = (*TInternetprotocolv4Messaggiobuffer)(Pointer(ethernetRiquadropayload))
	var internetprotocolMessaggio TInternetprotocolv4Messaggio
	internetprotocolMessaggio.Init(*buffer_2)

	var reply bool = false

	if internetprotocolMessaggio.destinazioneipaddress == uint32(efhandler.Getipaddress()) {

		var durata uint32 = uint32(internetprotocolMessaggio.totaleDurata)
		if durata > dimensione {
			durata = dimensione
		}
		if handler_2[internetprotocolMessaggio.protocol] != nil {
			reply = handler_2[internetprotocolMessaggio.protocol].Internetprotocolreceivewhen(internetprotocolMessaggio.origineipaddress, internetprotocolMessaggio.destinazioneipaddress, ethernetRiquadropayload+uintptr(4*internetprotocolMessaggio.headerDurata), uint32(durata-uint32(4*internetprotocolMessaggio.headerDurata)))

		}
	}

	if reply {

		var temporary = internetprotocolMessaggio.destinazioneipaddress
		internetprotocolMessaggio.destinazioneipaddress = internetprotocolMessaggio.origineipaddress
		internetprotocolMessaggio.origineipaddress = temporary

		internetprotocolMessaggio.oratolive = 0x40
		internetprotocolMessaggio.checksum = 0

		internetprotocolMessaggio.Impostabuffer(buffer_2)
		internetprotocolMessaggio.checksum = séstesso.Checksum((*([4096]uint16))(Pointer(ethernetRiquadropayload)), uint32(4*internetprotocolMessaggio.headerDurata))

		internetprotocolMessaggio.Impostabuffer(buffer_2)

	}

	ipconsole.MStampa(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Stampa(internetprotocolMessaggio.origineipaddress)
	ipconsole.MStampa(([]byte)(":"))
	ipconsole.MUnsignedinteger32Stampa(internetprotocolMessaggio.destinazioneipaddress)
	ipconsole.MStampa(([]byte)(":"))
	ipconsole.MUnsignedinteger16Stampa(uint16(internetprotocolMessaggio.headerDurata))
	ipconsole.MStampa(([]byte)(":"))
	ipconsole.MUnsignedinteger16Stampa(uint16(internetprotocolMessaggio.versione))
	ipconsole.MStampa(([]byte)(":"))
	ipconsole.MUnsignedinteger16Stampa(internetprotocolMessaggio.totaleDurata)
	ipconsole.MStampa(([]byte)(":"))
	ipconsole.MUnsignedinteger32Stampa(uint32(efhandler.Getipaddress()))
	ipconsole.MStampa(([]byte)(":"))
	ipconsole.MStampa(([]byte)("\n"))

	return reply

}
func (séstesso *TFornitore_del_protocollo_di_rete_interconnessa) Spedisci(destinazioneipaddressRetebyteorder uint32, protocol uint8, dataPuntatore uintptr, dimensione uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Messaggiobuffer = (*TInternetprotocolv4Messaggiobuffer)(Pointer(&buffer1_2))
	var messaggio TInternetprotocolv4Messaggio = TInternetprotocolv4Messaggio{}
	messaggio.versione = 4
	messaggio.headerDurata = ipDimensione / 4
	messaggio.tos = 0
	messaggio.totaleDurata = Unsignedinteger16r(uint16(dimensione + uint32(ipDimensione)))

	messaggio.ident = 0x0100
	messaggio.flageoffset = 0x0040
	messaggio.oratolive = 0x40
	messaggio.protocol = protocol

	messaggio.destinazioneipaddress = destinazioneipaddressRetebyteorder

	messaggio.origineipaddress = uint32(efhandler.Getipaddress())

	messaggio.checksum = 0

	messaggio.Impostabuffer(buffer_2)
	messaggio.checksum = séstesso.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipDimensione))
	messaggio.Impostabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataPuntatore))

	for i := 0; i < int(dimensione); i++ {

		buffer1_2[i+int(ipDimensione)] = databuffer_2[i]
	}

	ipconsole.MStampaxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(dimensione)+int(ipDimensione); i++ {
		ipconsole.MHexadecimalStampa(buffer1_2[i])
	}
	ipconsole.MStampa(([]byte)(":"))
	ipconsole.MStampa(([]byte)("]\n"))

	var successivohopipaddressRetebyteorder uint32 = destinazioneipaddressRetebyteorder
	if (destinazioneipaddressRetebyteorder & séstesso.SubnetMaschera) != (messaggio.origineipaddress & séstesso.SubnetMaschera) {
		successivohopipaddressRetebyteorder = séstesso.Gatewayip
	}

	var spediscidataPuntatore = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Stampa(successivohopipaddressRetebyteorder)

	var ethernetTipobe = Unsignedinteger16r(0x0800)
	efhandler.RiquadroSpedisci(séstesso.arpprovider.Resolve(successivohopipaddressRetebyteorder), ethernetTipobe, spediscidataPuntatore, uint32(ipDimensione)+uint32(dimensione))

}
func (séstesso *TFornitore_del_protocollo_di_rete_interconnessa) Checksum(pdata *[4096]uint16, durataIngressoByte uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataByte [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (durataIngressoByte % 2) != 0 {
		temporary += uint32(uint16(dataByte[durataIngressoByte-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (séstesso *TFornitore_del_protocollo_di_rete_interconnessa) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
