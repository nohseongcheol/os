/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protocol_voor_verbonden_netwerken_4

import . "unsafe"
import . "util"
import . "console"
import . "frame_van_het_gedeelde_medium_netwerk"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4Berichtbuffer struct {
	lenver		byte
	tos		byte
	totaalLengte	[2]byte

	ident			[2]byte
	vlaggenenVerschuiving	[2]byte

	tijdnaarlive	byte
	protocol	byte
	checksum	[2]byte

	bronipaddress		[4]byte
	bestemmingipaddress	[4]byte
}

var ipGrootte uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Bericht struct {
	headerLengte	uint8
	versie		uint8
	tos		uint8
	totaalLengte	uint16

	ident			uint16
	vlaggenenVerschuiving	uint16

	tijdnaarlive	uint8
	protocol	uint8
	checksum	uint16

	bronipaddress		uint32
	bestemmingipaddress	uint32
}

func (zelf *TInternetprotocolv4Bericht) Init(buffer_2 TInternetprotocolv4Berichtbuffer) {

	zelf.versie = ((buffer_2.lenver & 0xF0) >> 4)
	zelf.headerLengte = buffer_2.lenver & 0x0F
	zelf.tos = buffer_2.tos
	zelf.totaalLengte = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer_2.totaalLengte))

	zelf.ident = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer_2.ident))
	zelf.vlaggenenVerschuiving = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer_2.vlaggenenVerschuiving))

	zelf.tijdnaarlive = buffer_2.tijdnaarlive
	zelf.protocol = buffer_2.protocol
	zelf.checksum = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer_2.checksum))

	zelf.bronipaddress = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer_2.bronipaddress))
	zelf.bestemmingipaddress = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer_2.bestemmingipaddress))

}
func (zelf *TInternetprotocolv4Bericht) Instellenbuffer(buffer_2 *TInternetprotocolv4Berichtbuffer) {

	buffer_2.lenver = byte(((zelf.versie & 0x0F) << 4) | (zelf.headerLengte & 0x0F))
	buffer_2.tos = zelf.tos
	buffer_2.totaalLengte = Unsignedinteger16naarReeks(zelf.totaalLengte)

	buffer_2.ident = Unsignedinteger16naarReeks(zelf.ident)
	buffer_2.vlaggenenVerschuiving = Unsignedinteger16naarReeks(zelf.vlaggenenVerschuiving)

	buffer_2.tijdnaarlive = zelf.tijdnaarlive
	buffer_2.protocol = zelf.protocol
	buffer_2.checksum = Unsignedinteger16naarReeks(zelf.checksum)

	buffer_2.bronipaddress = Unsignedinteger32naarReeks(zelf.bronipaddress)
	buffer_2.bestemmingipaddress = Unsignedinteger32naarReeks(zelf.bestemmingipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TProtocolleverancier_voor_verbonden_netwerken, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(bronipaddressNetwerkbyteorder uint32, bestemmingipaddressNetwerkbyteorder uint32, dataMuisaanwijzer uintptr, grootte uint32) bool
	Verzenden(bestemmingipaddressNetwerkbyteorder uint32, pprotocol uint8, dataMuisaanwijzer uintptr, grootte uint32)
	Providerget() *TProtocolleverancier_voor_verbonden_netwerken
}

type TInternetprotocolhandler struct {
}

var ipethernetframehandler Ipethernetframehandler = Ipethernetframehandler{}
var protocol uint8

func (zelf *TInternetprotocolhandler) Init(backend TProtocolleverancier_voor_verbonden_netwerken, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (zelf *TInternetprotocolhandler) Internetprotocolreceivewhen(bronipaddressNetwerkbyteorder uint32, bestemmingipaddressNetwerkbyteorder uint32, dataMuisaanwijzer uintptr, grootte uint32) bool {
	ipconsole.MAfdrukken(([]byte)("ipHandler:OnInternet"))
	return false
}
func (zelf *TInternetprotocolhandler) Verzenden(bestemmingipaddressNetwerkbyteorder uint32, pprotocol uint8, dataMuisaanwijzer uintptr, grootte uint32) {

	protocolleverancier_voor_verbonden_netwerken.Verzenden(bestemmingipaddressNetwerkbyteorder, pprotocol, dataMuisaanwijzer, grootte)
}
func (zelf *TInternetprotocolhandler) Providerget() *TProtocolleverancier_voor_verbonden_netwerken {
	return &protocolleverancier_voor_verbonden_netwerken
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var protocolleverancier_voor_verbonden_netwerken TProtocolleverancier_voor_verbonden_netwerken

func (zelf *Ipethernetframehandler) Ethernetframereceivewhen(dataMuisaanwijzer uintptr, grootte int) bool {
	ipconsole.MAfdrukken(([]byte)("iphandler:onEtherfameRecv\n"))
	return protocolleverancier_voor_verbonden_netwerken.Ethernetframereceivewhen(dataMuisaanwijzer, uint32(grootte))

}

func (zelf *Ipethernetframehandler) Verzenden(bestemmingipaddressNetwerkbyteorder uint64, dataMuisaanwijzer uintptr, grootte uint32) {
	ipconsole.MAfdrukken(([]byte)("ipefhandler:send\n"))
	var ethernetSoortbe = Unsignedinteger16r(0x0800)
	zelf.TEthernetframehandler.FrameVerzenden(bestemmingipaddressNetwerkbyteorder, ethernetSoortbe, dataMuisaanwijzer, grootte)

}

var handler_2 [255]IInternetprotocolhandler

type TProtocolleverancier_voor_verbonden_netwerken struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMasker	uint32
}

var efhandler IEthernetframehandler

func (zelf *TProtocolleverancier_voor_verbonden_netwerken) Init(pefprovider TFrameleverancier_van_het_gedeelde_medium_netwerk, pefhandler IEthernetframehandler, arp Arpprovider, gatewayip uint32, subnetMasker uint32) {

	efhandler = pefhandler
	efhandler.Instellenhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	zelf.arpprovider = arp
	zelf.Gatewayip = gatewayip
	zelf.SubnetMasker = subnetMasker
	protocolleverancier_voor_verbonden_netwerken = *zelf
}
func (zelf *TProtocolleverancier_voor_verbonden_netwerken) Ethernetframereceivewhen(ethernetframepayload uintptr, grootte uint32) bool {
	if grootte < uint32(ipGrootte) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Berichtbuffer = (*TInternetprotocolv4Berichtbuffer)(Pointer(ethernetframepayload))
	var internetprotocolBericht TInternetprotocolv4Bericht
	internetprotocolBericht.Init(*buffer_2)

	var reply bool = false

	if internetprotocolBericht.bestemmingipaddress == uint32(efhandler.Getipaddress()) {

		var lengte uint32 = uint32(internetprotocolBericht.totaalLengte)
		if lengte > grootte {
			lengte = grootte
		}
		if handler_2[internetprotocolBericht.protocol] != nil {
			reply = handler_2[internetprotocolBericht.protocol].Internetprotocolreceivewhen(internetprotocolBericht.bronipaddress, internetprotocolBericht.bestemmingipaddress, ethernetframepayload+uintptr(4*internetprotocolBericht.headerLengte), uint32(lengte-uint32(4*internetprotocolBericht.headerLengte)))

		}
	}

	if reply {

		var temporary = internetprotocolBericht.bestemmingipaddress
		internetprotocolBericht.bestemmingipaddress = internetprotocolBericht.bronipaddress
		internetprotocolBericht.bronipaddress = temporary

		internetprotocolBericht.tijdnaarlive = 0x40
		internetprotocolBericht.checksum = 0

		internetprotocolBericht.Instellenbuffer(buffer_2)
		internetprotocolBericht.checksum = zelf.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*internetprotocolBericht.headerLengte))

		internetprotocolBericht.Instellenbuffer(buffer_2)

	}

	ipconsole.MAfdrukken(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Afdrukken(internetprotocolBericht.bronipaddress)
	ipconsole.MAfdrukken(([]byte)(":"))
	ipconsole.MUnsignedinteger32Afdrukken(internetprotocolBericht.bestemmingipaddress)
	ipconsole.MAfdrukken(([]byte)(":"))
	ipconsole.MUnsignedinteger16Afdrukken(uint16(internetprotocolBericht.headerLengte))
	ipconsole.MAfdrukken(([]byte)(":"))
	ipconsole.MUnsignedinteger16Afdrukken(uint16(internetprotocolBericht.versie))
	ipconsole.MAfdrukken(([]byte)(":"))
	ipconsole.MUnsignedinteger16Afdrukken(internetprotocolBericht.totaalLengte)
	ipconsole.MAfdrukken(([]byte)(":"))
	ipconsole.MUnsignedinteger32Afdrukken(uint32(efhandler.Getipaddress()))
	ipconsole.MAfdrukken(([]byte)(":"))
	ipconsole.MAfdrukken(([]byte)("\n"))

	return reply

}
func (zelf *TProtocolleverancier_voor_verbonden_netwerken) Verzenden(bestemmingipaddressNetwerkbyteorder uint32, protocol uint8, dataMuisaanwijzer uintptr, grootte uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Berichtbuffer = (*TInternetprotocolv4Berichtbuffer)(Pointer(&buffer1_2))
	var bericht TInternetprotocolv4Bericht = TInternetprotocolv4Bericht{}
	bericht.versie = 4
	bericht.headerLengte = ipGrootte / 4
	bericht.tos = 0
	bericht.totaalLengte = Unsignedinteger16r(uint16(grootte + uint32(ipGrootte)))

	bericht.ident = 0x0100
	bericht.vlaggenenVerschuiving = 0x0040
	bericht.tijdnaarlive = 0x40
	bericht.protocol = protocol

	bericht.bestemmingipaddress = bestemmingipaddressNetwerkbyteorder

	bericht.bronipaddress = uint32(efhandler.Getipaddress())

	bericht.checksum = 0

	bericht.Instellenbuffer(buffer_2)
	bericht.checksum = zelf.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipGrootte))
	bericht.Instellenbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataMuisaanwijzer))

	for i := 0; i < int(grootte); i++ {

		buffer1_2[i+int(ipGrootte)] = databuffer_2[i]
	}

	ipconsole.MAfdrukkenxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(grootte)+int(ipGrootte); i++ {
		ipconsole.MHexadecimalAfdrukken(buffer1_2[i])
	}
	ipconsole.MAfdrukken(([]byte)(":"))
	ipconsole.MAfdrukken(([]byte)("]\n"))

	var volgendehopipaddressNetwerkbyteorder uint32 = bestemmingipaddressNetwerkbyteorder
	if (bestemmingipaddressNetwerkbyteorder & zelf.SubnetMasker) != (bericht.bronipaddress & zelf.SubnetMasker) {
		volgendehopipaddressNetwerkbyteorder = zelf.Gatewayip
	}

	var verzendendataMuisaanwijzer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Afdrukken(volgendehopipaddressNetwerkbyteorder)

	var ethernetSoortbe = Unsignedinteger16r(0x0800)
	efhandler.FrameVerzenden(zelf.arpprovider.Resolve(volgendehopipaddressNetwerkbyteorder), ethernetSoortbe, verzendendataMuisaanwijzer, uint32(ipGrootte)+uint32(grootte))

}
func (zelf *TProtocolleverancier_voor_verbonden_netwerken) Checksum(pdata *[4096]uint16, lengteinbytes uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var databytes [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengteinbytes % 2) != 0 {
		temporary += uint32(uint16(databytes[lengteinbytes-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (zelf *TProtocolleverancier_voor_verbonden_netwerken) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
