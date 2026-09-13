package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetframe"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4PORUKAbuffer struct {
	lenver		byte
	tos		byte
	ukupnoDužina	[2]byte

	ident			[2]byte
	zastaviceandoffset	[2]byte

	vrijemetolive	byte
	protocol	byte
	checksum	[2]byte

	izvoripaddress		[4]byte
	odredišteipaddress	[4]byte
}

var ipVeličina uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4PORUKA struct {
	headerDužina	uint8
	inačica		uint8
	tos		uint8
	ukupnoDužina	uint16

	ident			uint16
	zastaviceandoffset	uint16

	vrijemetolive	uint8
	protocol	uint8
	checksum	uint16

	izvoripaddress		uint32
	odredišteipaddress	uint32
}

func (sam *TInternetprotocolv4PORUKA) Init(buffer_2 TInternetprotocolv4PORUKAbuffer) {

	sam.inačica = ((buffer_2.lenver & 0xF0) >> 4)
	sam.headerDužina = buffer_2.lenver & 0x0F
	sam.tos = buffer_2.tos
	sam.ukupnoDužina = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.ukupnoDužina))

	sam.ident = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.ident))
	sam.zastaviceandoffset = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.zastaviceandoffset))

	sam.vrijemetolive = buffer_2.vrijemetolive
	sam.protocol = buffer_2.protocol
	sam.checksum = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.checksum))

	sam.izvoripaddress = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.izvoripaddress))
	sam.odredišteipaddress = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.odredišteipaddress))

}
func (sam *TInternetprotocolv4PORUKA) Postavibuffer(buffer_2 *TInternetprotocolv4PORUKAbuffer) {

	buffer_2.lenver = byte(((sam.inačica & 0x0F) << 4) | (sam.headerDužina & 0x0F))
	buffer_2.tos = sam.tos
	buffer_2.ukupnoDužina = Unsignedinteger16toNiz(sam.ukupnoDužina)

	buffer_2.ident = Unsignedinteger16toNiz(sam.ident)
	buffer_2.zastaviceandoffset = Unsignedinteger16toNiz(sam.zastaviceandoffset)

	buffer_2.vrijemetolive = sam.vrijemetolive
	buffer_2.protocol = sam.protocol
	buffer_2.checksum = Unsignedinteger16toNiz(sam.checksum)

	buffer_2.izvoripaddress = Unsignedinteger32toNiz(sam.izvoripaddress)
	buffer_2.odredišteipaddress = Unsignedinteger32toNiz(sam.odredišteipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, dataPokazivač uintptr, veličina uint32) bool
	Pošalji(odredišteipaddressMrežabyteorder uint32, pprotocol uint8, dataPokazivač uintptr, veličina uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetframehandler Ipethernetframehandler = Ipethernetframehandler{}
var protocol uint8

func (sam *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (sam *TInternetprotocolhandler) Internetprotocolreceivewhen(izvoripaddressMrežabyteorder uint32, odredišteipaddressMrežabyteorder uint32, dataPokazivač uintptr, veličina uint32) bool {
	ipconsole.MIspis(([]byte)("ipHandler:OnInternet"))
	return false
}
func (sam *TInternetprotocolhandler) Pošalji(odredišteipaddressMrežabyteorder uint32, pprotocol uint8, dataPokazivač uintptr, veličina uint32) {

	ipprovider.Pošalji(odredišteipaddressMrežabyteorder, pprotocol, dataPokazivač, veličina)
}
func (sam *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var ipprovider TInternetprotocolprovider

func (sam *Ipethernetframehandler) Ethernetframereceivewhen(dataPokazivač uintptr, veličina int) bool {
	ipconsole.MIspis(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetframereceivewhen(dataPokazivač, uint32(veličina))

}

func (sam *Ipethernetframehandler) Pošalji(odredišteipaddressMrežabyteorder uint64, dataPokazivač uintptr, veličina uint32) {
	ipconsole.MIspis(([]byte)("ipefhandler:send\n"))
	var ethernetVrstabe = Unsignedinteger16r(0x0800)
	sam.TEthernetframehandler.FramePošalji(odredišteipaddressMrežabyteorder, ethernetVrstabe, dataPokazivač, veličina)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaska	uint32
}

var efhandler IEthernetframehandler

func (sam *TInternetprotocolprovider) Init(pefprovider TEthernetframeprovider, pefhandler IEthernetframehandler, arp Arpprovider, gatewayip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Postavihandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	sam.arpprovider = arp
	sam.Gatewayip = gatewayip
	sam.SubnetMaska = subnetMaska
	ipprovider = *sam
}
func (sam *TInternetprotocolprovider) Ethernetframereceivewhen(ethernetframepayload uintptr, veličina uint32) bool {
	if veličina < uint32(ipVeličina) {
		return false
	}

	var buffer_2 *TInternetprotocolv4PORUKAbuffer = (*TInternetprotocolv4PORUKAbuffer)(Pointer(ethernetframepayload))
	var internetprotocolPORUKA TInternetprotocolv4PORUKA
	internetprotocolPORUKA.Init(*buffer_2)

	var reply bool = false

	if internetprotocolPORUKA.odredišteipaddress == uint32(efhandler.Getipaddress()) {

		var dužina uint32 = uint32(internetprotocolPORUKA.ukupnoDužina)
		if dužina > veličina {
			dužina = veličina
		}
		if handler_2[internetprotocolPORUKA.protocol] != nil {
			reply = handler_2[internetprotocolPORUKA.protocol].Internetprotocolreceivewhen(internetprotocolPORUKA.izvoripaddress, internetprotocolPORUKA.odredišteipaddress, ethernetframepayload+uintptr(4*internetprotocolPORUKA.headerDužina), uint32(dužina-uint32(4*internetprotocolPORUKA.headerDužina)))

		}
	}

	if reply {

		var temporary = internetprotocolPORUKA.odredišteipaddress
		internetprotocolPORUKA.odredišteipaddress = internetprotocolPORUKA.izvoripaddress
		internetprotocolPORUKA.izvoripaddress = temporary

		internetprotocolPORUKA.vrijemetolive = 0x40
		internetprotocolPORUKA.checksum = 0

		internetprotocolPORUKA.Postavibuffer(buffer_2)
		internetprotocolPORUKA.checksum = sam.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*internetprotocolPORUKA.headerDužina))

		internetprotocolPORUKA.Postavibuffer(buffer_2)

	}

	ipconsole.MIspis(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Ispis(internetprotocolPORUKA.izvoripaddress)
	ipconsole.MIspis(([]byte)(":"))
	ipconsole.MUnsignedinteger32Ispis(internetprotocolPORUKA.odredišteipaddress)
	ipconsole.MIspis(([]byte)(":"))
	ipconsole.MUnsignedinteger16Ispis(uint16(internetprotocolPORUKA.headerDužina))
	ipconsole.MIspis(([]byte)(":"))
	ipconsole.MUnsignedinteger16Ispis(uint16(internetprotocolPORUKA.inačica))
	ipconsole.MIspis(([]byte)(":"))
	ipconsole.MUnsignedinteger16Ispis(internetprotocolPORUKA.ukupnoDužina)
	ipconsole.MIspis(([]byte)(":"))
	ipconsole.MUnsignedinteger32Ispis(uint32(efhandler.Getipaddress()))
	ipconsole.MIspis(([]byte)(":"))
	ipconsole.MIspis(([]byte)("\n"))

	return reply

}
func (sam *TInternetprotocolprovider) Pošalji(odredišteipaddressMrežabyteorder uint32, protocol uint8, dataPokazivač uintptr, veličina uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4PORUKAbuffer = (*TInternetprotocolv4PORUKAbuffer)(Pointer(&buffer1_2))
	var pORUKA TInternetprotocolv4PORUKA = TInternetprotocolv4PORUKA{}
	pORUKA.inačica = 4
	pORUKA.headerDužina = ipVeličina / 4
	pORUKA.tos = 0
	pORUKA.ukupnoDužina = Unsignedinteger16r(uint16(veličina + uint32(ipVeličina)))

	pORUKA.ident = 0x0100
	pORUKA.zastaviceandoffset = 0x0040
	pORUKA.vrijemetolive = 0x40
	pORUKA.protocol = protocol

	pORUKA.odredišteipaddress = odredišteipaddressMrežabyteorder

	pORUKA.izvoripaddress = uint32(efhandler.Getipaddress())

	pORUKA.checksum = 0

	pORUKA.Postavibuffer(buffer_2)
	pORUKA.checksum = sam.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipVeličina))
	pORUKA.Postavibuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))

	for i := 0; i < int(veličina); i++ {

		buffer1_2[i+int(ipVeličina)] = databuffer_2[i]
	}

	ipconsole.MIspisxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(veličina)+int(ipVeličina); i++ {
		ipconsole.MHexadecimalIspis(buffer1_2[i])
	}
	ipconsole.MIspis(([]byte)(":"))
	ipconsole.MIspis(([]byte)("]\n"))

	var slijedećehopipaddressMrežabyteorder uint32 = odredišteipaddressMrežabyteorder
	if (odredišteipaddressMrežabyteorder & sam.SubnetMaska) != (pORUKA.izvoripaddress & sam.SubnetMaska) {
		slijedećehopipaddressMrežabyteorder = sam.Gatewayip
	}

	var pošaljidataPokazivač = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Ispis(slijedećehopipaddressMrežabyteorder)

	var ethernetVrstabe = Unsignedinteger16r(0x0800)
	efhandler.FramePošalji(sam.arpprovider.Resolve(slijedećehopipaddressMrežabyteorder), ethernetVrstabe, pošaljidataPokazivač, uint32(ipVeličina)+uint32(veličina))

}
func (sam *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, dužinaPovećajBajtova uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBajtova [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (dužinaPovećajBajtova % 2) != 0 {
		temporary += uint32(uint16(dataBajtova[dužinaPovećajBajtova-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (sam *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
