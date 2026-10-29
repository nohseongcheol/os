/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protokoll_för_sammankopplade_nät_4

import . "unsafe"
import . "util"
import . "konsol"
import . "ram_i_nät_med_delat_medium"
import . "arp"

var ipKonsol TKonsol = TKonsol{}

type TInternetprotocolv4Meddelandebuffer struct {
	lenver		byte
	tos		byte
	totaltLängd	[2]byte

	ident			[2]byte
	flaggorochFörskjutning	[2]byte

	tidtolive	byte
	protocol	byte
	kontrollsumma	[2]byte

	källaipAdress	[4]byte
	målipAdress	[4]byte
}

var ipStorlek uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Meddelande struct {
	headerLängd	uint8
	version		uint8
	tos		uint8
	totaltLängd	uint16

	ident			uint16
	flaggorochFörskjutning	uint16

	tidtolive	uint8
	protocol	uint8
	kontrollsumma	uint16

	källaipAdress	uint32
	målipAdress	uint32
}

func (själv *TInternetprotocolv4Meddelande) Init(buffer_2 TInternetprotocolv4Meddelandebuffer) {

	själv.version = ((buffer_2.lenver & 0xF0) >> 4)
	själv.headerLängd = buffer_2.lenver & 0x0F
	själv.tos = buffer_2.tos
	själv.totaltLängd = Unsignedinteger16r(Vektortounsignedinteger16(buffer_2.totaltLängd))

	själv.ident = Unsignedinteger16r(Vektortounsignedinteger16(buffer_2.ident))
	själv.flaggorochFörskjutning = Unsignedinteger16r(Vektortounsignedinteger16(buffer_2.flaggorochFörskjutning))

	själv.tidtolive = buffer_2.tidtolive
	själv.protocol = buffer_2.protocol
	själv.kontrollsumma = Unsignedinteger16r(Vektortounsignedinteger16(buffer_2.kontrollsumma))

	själv.källaipAdress = Unsignedinteger32r(Vektortounsignedinteger32(buffer_2.källaipAdress))
	själv.målipAdress = Unsignedinteger32r(Vektortounsignedinteger32(buffer_2.målipAdress))

}
func (själv *TInternetprotocolv4Meddelande) Mängdbuffer(buffer_2 *TInternetprotocolv4Meddelandebuffer) {

	buffer_2.lenver = byte(((själv.version & 0x0F) << 4) | (själv.headerLängd & 0x0F))
	buffer_2.tos = själv.tos
	buffer_2.totaltLängd = Unsignedinteger16toVektor(själv.totaltLängd)

	buffer_2.ident = Unsignedinteger16toVektor(själv.ident)
	buffer_2.flaggorochFörskjutning = Unsignedinteger16toVektor(själv.flaggorochFörskjutning)

	buffer_2.tidtolive = själv.tidtolive
	buffer_2.protocol = själv.protocol
	buffer_2.kontrollsumma = Unsignedinteger16toVektor(själv.kontrollsumma)

	buffer_2.källaipAdress = Unsignedinteger32toVektor(själv.källaipAdress)
	buffer_2.målipAdress = Unsignedinteger32toVektor(själv.målipAdress)

}

type IInternetprotocolhandler interface {
	Init(backend TProtokolleverantör_för_sammankopplade_nät, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(källaipAdressNätverkbyteorder uint32, målipAdressNätverkbyteorder uint32, dataMuspekare uintptr, storlek uint32) bool
	Skicka(målipAdressNätverkbyteorder uint32, pprotocol uint8, dataMuspekare uintptr, storlek uint32)
	Providerget() *TProtokolleverantör_för_sammankopplade_nät
}

type TInternetprotocolhandler struct {
}

var ipethernetRamhandler IpethernetRamhandler = IpethernetRamhandler{}
var protocol uint8

func (själv *TInternetprotocolhandler) Init(backend TProtokolleverantör_för_sammankopplade_nät, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (själv *TInternetprotocolhandler) Internetprotocolreceivewhen(källaipAdressNätverkbyteorder uint32, målipAdressNätverkbyteorder uint32, dataMuspekare uintptr, storlek uint32) bool {
	ipKonsol.MSkrivut(([]byte)("ipHandler:OnInternet"))
	return false
}
func (själv *TInternetprotocolhandler) Skicka(målipAdressNätverkbyteorder uint32, pprotocol uint8, dataMuspekare uintptr, storlek uint32) {

	protokolleverantör_för_sammankopplade_nät.Skicka(målipAdressNätverkbyteorder, pprotocol, dataMuspekare, storlek)
}
func (själv *TInternetprotocolhandler) Providerget() *TProtokolleverantör_för_sammankopplade_nät {
	return &protokolleverantör_för_sammankopplade_nät
}

type IpethernetRamhandler struct {
	TEthernetRamhandler
}

var protokolleverantör_för_sammankopplade_nät TProtokolleverantör_för_sammankopplade_nät

func (själv *IpethernetRamhandler) EthernetRamreceivewhen(dataMuspekare uintptr, storlek int) bool {
	ipKonsol.MSkrivut(([]byte)("iphandler:onEtherfameRecv\n"))
	return protokolleverantör_för_sammankopplade_nät.EthernetRamreceivewhen(dataMuspekare, uint32(storlek))

}

func (själv *IpethernetRamhandler) Skicka(målipAdressNätverkbyteorder uint64, dataMuspekare uintptr, storlek uint32) {
	ipKonsol.MSkrivut(([]byte)("ipefhandler:send\n"))
	var ethernetTypbe = Unsignedinteger16r(0x0800)
	själv.TEthernetRamhandler.RamSkicka(målipAdressNätverkbyteorder, ethernetTypbe, dataMuspekare, storlek)

}

var handler_2 [255]IInternetprotocolhandler

type TProtokolleverantör_för_sammankopplade_nät struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetRamhandler

func (själv *TProtokolleverantör_för_sammankopplade_nät) Init(pefprovider TRamleverantör_för_nät_med_delat_medium, pefhandler IEthernetRamhandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Mängdhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	själv.arpprovider = arp
	själv.Gatewayip = gatewayip
	själv.Subnetmask = subnetmask
	protokolleverantör_för_sammankopplade_nät = *själv
}
func (själv *TProtokolleverantör_för_sammankopplade_nät) EthernetRamreceivewhen(ethernetRampayload uintptr, storlek uint32) bool {
	if storlek < uint32(ipStorlek) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Meddelandebuffer = (*TInternetprotocolv4Meddelandebuffer)(Pointer(ethernetRampayload))
	var internetprotocolMeddelande TInternetprotocolv4Meddelande
	internetprotocolMeddelande.Init(*buffer_2)

	var reply bool = false

	if internetprotocolMeddelande.målipAdress == uint32(efhandler.GetipAdress()) {

		var längd uint32 = uint32(internetprotocolMeddelande.totaltLängd)
		if längd > storlek {
			längd = storlek
		}
		if handler_2[internetprotocolMeddelande.protocol] != nil {
			reply = handler_2[internetprotocolMeddelande.protocol].Internetprotocolreceivewhen(internetprotocolMeddelande.källaipAdress, internetprotocolMeddelande.målipAdress, ethernetRampayload+uintptr(4*internetprotocolMeddelande.headerLängd), uint32(längd-uint32(4*internetprotocolMeddelande.headerLängd)))

		}
	}

	if reply {

		var temporary = internetprotocolMeddelande.målipAdress
		internetprotocolMeddelande.målipAdress = internetprotocolMeddelande.källaipAdress
		internetprotocolMeddelande.källaipAdress = temporary

		internetprotocolMeddelande.tidtolive = 0x40
		internetprotocolMeddelande.kontrollsumma = 0

		internetprotocolMeddelande.Mängdbuffer(buffer_2)
		internetprotocolMeddelande.kontrollsumma = själv.Kontrollsumma((*([4096]uint16))(Pointer(ethernetRampayload)), uint32(4*internetprotocolMeddelande.headerLängd))

		internetprotocolMeddelande.Mängdbuffer(buffer_2)

	}

	ipKonsol.MSkrivut(([]byte)("ipmessage"))
	ipKonsol.MUnsignedinteger32Skrivut(internetprotocolMeddelande.källaipAdress)
	ipKonsol.MSkrivut(([]byte)(":"))
	ipKonsol.MUnsignedinteger32Skrivut(internetprotocolMeddelande.målipAdress)
	ipKonsol.MSkrivut(([]byte)(":"))
	ipKonsol.MUnsignedinteger16Skrivut(uint16(internetprotocolMeddelande.headerLängd))
	ipKonsol.MSkrivut(([]byte)(":"))
	ipKonsol.MUnsignedinteger16Skrivut(uint16(internetprotocolMeddelande.version))
	ipKonsol.MSkrivut(([]byte)(":"))
	ipKonsol.MUnsignedinteger16Skrivut(internetprotocolMeddelande.totaltLängd)
	ipKonsol.MSkrivut(([]byte)(":"))
	ipKonsol.MUnsignedinteger32Skrivut(uint32(efhandler.GetipAdress()))
	ipKonsol.MSkrivut(([]byte)(":"))
	ipKonsol.MSkrivut(([]byte)("\n"))

	return reply

}
func (själv *TProtokolleverantör_för_sammankopplade_nät) Skicka(målipAdressNätverkbyteorder uint32, protocol uint8, dataMuspekare uintptr, storlek uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Meddelandebuffer = (*TInternetprotocolv4Meddelandebuffer)(Pointer(&buffer1_2))
	var meddelande TInternetprotocolv4Meddelande = TInternetprotocolv4Meddelande{}
	meddelande.version = 4
	meddelande.headerLängd = ipStorlek / 4
	meddelande.tos = 0
	meddelande.totaltLängd = Unsignedinteger16r(uint16(storlek + uint32(ipStorlek)))

	meddelande.ident = 0x0100
	meddelande.flaggorochFörskjutning = 0x0040
	meddelande.tidtolive = 0x40
	meddelande.protocol = protocol

	meddelande.målipAdress = målipAdressNätverkbyteorder

	meddelande.källaipAdress = uint32(efhandler.GetipAdress())

	meddelande.kontrollsumma = 0

	meddelande.Mängdbuffer(buffer_2)
	meddelande.kontrollsumma = själv.Kontrollsumma((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipStorlek))
	meddelande.Mängdbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataMuspekare))

	for i := 0; i < int(storlek); i++ {

		buffer1_2[i+int(ipStorlek)] = databuffer_2[i]
	}

	ipKonsol.MSkrivutxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(storlek)+int(ipStorlek); i++ {
		ipKonsol.MHexadecimalSkrivut(buffer1_2[i])
	}
	ipKonsol.MSkrivut(([]byte)(":"))
	ipKonsol.MSkrivut(([]byte)("]\n"))

	var nästahopipAdressNätverkbyteorder uint32 = målipAdressNätverkbyteorder
	if (målipAdressNätverkbyteorder & själv.Subnetmask) != (meddelande.källaipAdress & själv.Subnetmask) {
		nästahopipAdressNätverkbyteorder = själv.Gatewayip
	}

	var skickadataMuspekare = uintptr(Pointer(&buffer1_2))
	ipKonsol.MUnsignedinteger32Skrivut(nästahopipAdressNätverkbyteorder)

	var ethernetTypbe = Unsignedinteger16r(0x0800)
	efhandler.RamSkicka(själv.arpprovider.Resolve(nästahopipAdressNätverkbyteorder), ethernetTypbe, skickadataMuspekare, uint32(ipStorlek)+uint32(storlek))

}
func (själv *TProtokolleverantör_för_sammankopplade_nät) Kontrollsumma(pdata *[4096]uint16, längdiByte uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataByte [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (längdiByte % 2) != 0 {
		temporary += uint32(uint16(dataByte[längdiByte-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (själv *TProtokolleverantör_för_sammankopplade_nät) GetipAdress() uint64 {
	return efhandler.GetipAdress()
}
