package verkkojen_yhdyskäytäntö_4

import . "unsafe"
import . "util"
import . "konsoli"
import . "jaetun_siirtotien_verkkokehys"
import . "arp"

var ipKonsoli TKonsoli = TKonsoli{}

type TInternetprotocolv4Viestibuffer struct {
	lenver		byte
	tos		byte
	yhteensäKesto	[2]byte

	ident		[2]byte
	liputandoffset	[2]byte

	aikatolive	byte
	protocol	byte
	checksum	[2]byte

	lähdeipaddress	[4]byte
	kohdeipaddress	[4]byte
}

var ipKoko uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Viesti struct {
	headerKesto	uint8
	versio		uint8
	tos		uint8
	yhteensäKesto	uint16

	ident		uint16
	liputandoffset	uint16

	aikatolive	uint8
	protocol	uint8
	checksum	uint16

	lähdeipaddress	uint32
	kohdeipaddress	uint32
}

func (itse *TInternetprotocolv4Viesti) Init(buffer_2 TInternetprotocolv4Viestibuffer) {

	itse.versio = ((buffer_2.lenver & 0xF0) >> 4)
	itse.headerKesto = buffer_2.lenver & 0x0F
	itse.tos = buffer_2.tos
	itse.yhteensäKesto = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer_2.yhteensäKesto))

	itse.ident = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer_2.ident))
	itse.liputandoffset = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer_2.liputandoffset))

	itse.aikatolive = buffer_2.aikatolive
	itse.protocol = buffer_2.protocol
	itse.checksum = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer_2.checksum))

	itse.lähdeipaddress = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer_2.lähdeipaddress))
	itse.kohdeipaddress = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer_2.kohdeipaddress))

}
func (itse *TInternetprotocolv4Viesti) Asetabuffer(buffer_2 *TInternetprotocolv4Viestibuffer) {

	buffer_2.lenver = byte(((itse.versio & 0x0F) << 4) | (itse.headerKesto & 0x0F))
	buffer_2.tos = itse.tos
	buffer_2.yhteensäKesto = Unsignedinteger16toTaulukko(itse.yhteensäKesto)

	buffer_2.ident = Unsignedinteger16toTaulukko(itse.ident)
	buffer_2.liputandoffset = Unsignedinteger16toTaulukko(itse.liputandoffset)

	buffer_2.aikatolive = itse.aikatolive
	buffer_2.protocol = itse.protocol
	buffer_2.checksum = Unsignedinteger16toTaulukko(itse.checksum)

	buffer_2.lähdeipaddress = Unsignedinteger32toTaulukko(itse.lähdeipaddress)
	buffer_2.kohdeipaddress = Unsignedinteger32toTaulukko(itse.kohdeipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TVerkkojen_yhteyskäytännön_tarjoaja, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(lähdeipaddressVerkkobyteorder uint32, kohdeipaddressVerkkobyteorder uint32, dataOsoitin uintptr, koko uint32) bool
	Lähetä(kohdeipaddressVerkkobyteorder uint32, pprotocol uint8, dataOsoitin uintptr, koko uint32)
	Providerget() *TVerkkojen_yhteyskäytännön_tarjoaja
}

type TInternetprotocolhandler struct {
}

var ipethernetKehyshandler IpethernetKehyshandler = IpethernetKehyshandler{}
var protocol uint8

func (itse *TInternetprotocolhandler) Init(backend TVerkkojen_yhteyskäytännön_tarjoaja, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (itse *TInternetprotocolhandler) Internetprotocolreceivewhen(lähdeipaddressVerkkobyteorder uint32, kohdeipaddressVerkkobyteorder uint32, dataOsoitin uintptr, koko uint32) bool {
	ipKonsoli.MTulosta(([]byte)("ipHandler:OnInternet"))
	return false
}
func (itse *TInternetprotocolhandler) Lähetä(kohdeipaddressVerkkobyteorder uint32, pprotocol uint8, dataOsoitin uintptr, koko uint32) {

	verkkojen_yhteyskäytännön_tarjoaja.Lähetä(kohdeipaddressVerkkobyteorder, pprotocol, dataOsoitin, koko)
}
func (itse *TInternetprotocolhandler) Providerget() *TVerkkojen_yhteyskäytännön_tarjoaja {
	return &verkkojen_yhteyskäytännön_tarjoaja
}

type IpethernetKehyshandler struct {
	TEthernetKehyshandler
}

var verkkojen_yhteyskäytännön_tarjoaja TVerkkojen_yhteyskäytännön_tarjoaja

func (itse *IpethernetKehyshandler) EthernetKehysreceivewhen(dataOsoitin uintptr, koko int) bool {
	ipKonsoli.MTulosta(([]byte)("iphandler:onEtherfameRecv\n"))
	return verkkojen_yhteyskäytännön_tarjoaja.EthernetKehysreceivewhen(dataOsoitin, uint32(koko))

}

func (itse *IpethernetKehyshandler) Lähetä(kohdeipaddressVerkkobyteorder uint64, dataOsoitin uintptr, koko uint32) {
	ipKonsoli.MTulosta(([]byte)("ipefhandler:send\n"))
	var ethernetTyyppibe = Unsignedinteger16r(0x0800)
	itse.TEthernetKehyshandler.KehysLähetä(kohdeipaddressVerkkobyteorder, ethernetTyyppibe, dataOsoitin, koko)

}

var handler_2 [255]IInternetprotocolhandler

type TVerkkojen_yhteyskäytännön_tarjoaja struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetPeite	uint32
}

var efhandler IEthernetKehyshandler

func (itse *TVerkkojen_yhteyskäytännön_tarjoaja) Init(pefprovider TJaetun_siirtotien_verkkokehysten_tarjoaja, pefhandler IEthernetKehyshandler, arp Arpprovider, gatewayip uint32, subnetPeite uint32) {

	efhandler = pefhandler
	efhandler.Asetahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	itse.arpprovider = arp
	itse.Gatewayip = gatewayip
	itse.SubnetPeite = subnetPeite
	verkkojen_yhteyskäytännön_tarjoaja = *itse
}
func (itse *TVerkkojen_yhteyskäytännön_tarjoaja) EthernetKehysreceivewhen(ethernetKehyspayload uintptr, koko uint32) bool {
	if koko < uint32(ipKoko) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Viestibuffer = (*TInternetprotocolv4Viestibuffer)(Pointer(ethernetKehyspayload))
	var internetprotocolViesti TInternetprotocolv4Viesti
	internetprotocolViesti.Init(*buffer_2)

	var reply bool = false

	if internetprotocolViesti.kohdeipaddress == uint32(efhandler.Getipaddress()) {

		var kesto uint32 = uint32(internetprotocolViesti.yhteensäKesto)
		if kesto > koko {
			kesto = koko
		}
		if handler_2[internetprotocolViesti.protocol] != nil {
			reply = handler_2[internetprotocolViesti.protocol].Internetprotocolreceivewhen(internetprotocolViesti.lähdeipaddress, internetprotocolViesti.kohdeipaddress, ethernetKehyspayload+uintptr(4*internetprotocolViesti.headerKesto), uint32(kesto-uint32(4*internetprotocolViesti.headerKesto)))

		}
	}

	if reply {

		var temporary = internetprotocolViesti.kohdeipaddress
		internetprotocolViesti.kohdeipaddress = internetprotocolViesti.lähdeipaddress
		internetprotocolViesti.lähdeipaddress = temporary

		internetprotocolViesti.aikatolive = 0x40
		internetprotocolViesti.checksum = 0

		internetprotocolViesti.Asetabuffer(buffer_2)
		internetprotocolViesti.checksum = itse.Checksum((*([4096]uint16))(Pointer(ethernetKehyspayload)), uint32(4*internetprotocolViesti.headerKesto))

		internetprotocolViesti.Asetabuffer(buffer_2)

	}

	ipKonsoli.MTulosta(([]byte)("ipmessage"))
	ipKonsoli.MUnsignedinteger32Tulosta(internetprotocolViesti.lähdeipaddress)
	ipKonsoli.MTulosta(([]byte)(":"))
	ipKonsoli.MUnsignedinteger32Tulosta(internetprotocolViesti.kohdeipaddress)
	ipKonsoli.MTulosta(([]byte)(":"))
	ipKonsoli.MUnsignedinteger16Tulosta(uint16(internetprotocolViesti.headerKesto))
	ipKonsoli.MTulosta(([]byte)(":"))
	ipKonsoli.MUnsignedinteger16Tulosta(uint16(internetprotocolViesti.versio))
	ipKonsoli.MTulosta(([]byte)(":"))
	ipKonsoli.MUnsignedinteger16Tulosta(internetprotocolViesti.yhteensäKesto)
	ipKonsoli.MTulosta(([]byte)(":"))
	ipKonsoli.MUnsignedinteger32Tulosta(uint32(efhandler.Getipaddress()))
	ipKonsoli.MTulosta(([]byte)(":"))
	ipKonsoli.MTulosta(([]byte)("\n"))

	return reply

}
func (itse *TVerkkojen_yhteyskäytännön_tarjoaja) Lähetä(kohdeipaddressVerkkobyteorder uint32, protocol uint8, dataOsoitin uintptr, koko uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Viestibuffer = (*TInternetprotocolv4Viestibuffer)(Pointer(&buffer1_2))
	var viesti TInternetprotocolv4Viesti = TInternetprotocolv4Viesti{}
	viesti.versio = 4
	viesti.headerKesto = ipKoko / 4
	viesti.tos = 0
	viesti.yhteensäKesto = Unsignedinteger16r(uint16(koko + uint32(ipKoko)))

	viesti.ident = 0x0100
	viesti.liputandoffset = 0x0040
	viesti.aikatolive = 0x40
	viesti.protocol = protocol

	viesti.kohdeipaddress = kohdeipaddressVerkkobyteorder

	viesti.lähdeipaddress = uint32(efhandler.Getipaddress())

	viesti.checksum = 0

	viesti.Asetabuffer(buffer_2)
	viesti.checksum = itse.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipKoko))
	viesti.Asetabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataOsoitin))

	for i := 0; i < int(koko); i++ {

		buffer1_2[i+int(ipKoko)] = databuffer_2[i]
	}

	ipKonsoli.MTulostaxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(koko)+int(ipKoko); i++ {
		ipKonsoli.MHexadecimalTulosta(buffer1_2[i])
	}
	ipKonsoli.MTulosta(([]byte)(":"))
	ipKonsoli.MTulosta(([]byte)("]\n"))

	var seuraavahopipaddressVerkkobyteorder uint32 = kohdeipaddressVerkkobyteorder
	if (kohdeipaddressVerkkobyteorder & itse.SubnetPeite) != (viesti.lähdeipaddress & itse.SubnetPeite) {
		seuraavahopipaddressVerkkobyteorder = itse.Gatewayip
	}

	var lähetädataOsoitin = uintptr(Pointer(&buffer1_2))
	ipKonsoli.MUnsignedinteger32Tulosta(seuraavahopipaddressVerkkobyteorder)

	var ethernetTyyppibe = Unsignedinteger16r(0x0800)
	efhandler.KehysLähetä(itse.arpprovider.Resolve(seuraavahopipaddressVerkkobyteorder), ethernetTyyppibe, lähetädataOsoitin, uint32(ipKoko)+uint32(koko))

}
func (itse *TVerkkojen_yhteyskäytännön_tarjoaja) Checksum(pdata *[4096]uint16, kestoSaapuvatavua uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var datatavua [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (kestoSaapuvatavua % 2) != 0 {
		temporary += uint32(uint16(datatavua[kestoSaapuvatavua-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (itse *TVerkkojen_yhteyskäytännön_tarjoaja) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
