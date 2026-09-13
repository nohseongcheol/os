package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetCadru"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4Mesajbuffer struct {
	lenver		byte
	tos		byte
	totalDurată	[2]byte

	ident			[2]byte
	indicatorișioffset	[2]byte

	orătolive	byte
	protocol	byte
	checksum	[2]byte

	sursăipaddress		[4]byte
	destinațieipaddress	[4]byte
}

var ipMărime uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Mesaj struct {
	headerDurată	uint8
	versiune	uint8
	tos		uint8
	totalDurată	uint16

	ident			uint16
	indicatorișioffset	uint16

	orătolive	uint8
	protocol	uint8
	checksum	uint16

	sursăipaddress		uint32
	destinațieipaddress	uint32
}

func (sine *TInternetprotocolv4Mesaj) Init(buffer_2 TInternetprotocolv4Mesajbuffer) {

	sine.versiune = ((buffer_2.lenver & 0xF0) >> 4)
	sine.headerDurată = buffer_2.lenver & 0x0F
	sine.tos = buffer_2.tos
	sine.totalDurată = Unsignedinteger16r(Vectortounsignedinteger16(buffer_2.totalDurată))

	sine.ident = Unsignedinteger16r(Vectortounsignedinteger16(buffer_2.ident))
	sine.indicatorișioffset = Unsignedinteger16r(Vectortounsignedinteger16(buffer_2.indicatorișioffset))

	sine.orătolive = buffer_2.orătolive
	sine.protocol = buffer_2.protocol
	sine.checksum = Unsignedinteger16r(Vectortounsignedinteger16(buffer_2.checksum))

	sine.sursăipaddress = Unsignedinteger32r(Vectortounsignedinteger32(buffer_2.sursăipaddress))
	sine.destinațieipaddress = Unsignedinteger32r(Vectortounsignedinteger32(buffer_2.destinațieipaddress))

}
func (sine *TInternetprotocolv4Mesaj) Definitbuffer(buffer_2 *TInternetprotocolv4Mesajbuffer) {

	buffer_2.lenver = byte(((sine.versiune & 0x0F) << 4) | (sine.headerDurată & 0x0F))
	buffer_2.tos = sine.tos
	buffer_2.totalDurată = Unsignedinteger16toVector(sine.totalDurată)

	buffer_2.ident = Unsignedinteger16toVector(sine.ident)
	buffer_2.indicatorișioffset = Unsignedinteger16toVector(sine.indicatorișioffset)

	buffer_2.orătolive = sine.orătolive
	buffer_2.protocol = sine.protocol
	buffer_2.checksum = Unsignedinteger16toVector(sine.checksum)

	buffer_2.sursăipaddress = Unsignedinteger32toVector(sine.sursăipaddress)
	buffer_2.destinațieipaddress = Unsignedinteger32toVector(sine.destinațieipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(sursăipaddressRețeabyteorder uint32, destinațieipaddressRețeabyteorder uint32, dataIndicator uintptr, mărime uint32) bool
	Trimite(destinațieipaddressRețeabyteorder uint32, pprotocol uint8, dataIndicator uintptr, mărime uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetCadruhandler IpethernetCadruhandler = IpethernetCadruhandler{}
var protocol uint8

func (sine *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (sine *TInternetprotocolhandler) Internetprotocolreceivewhen(sursăipaddressRețeabyteorder uint32, destinațieipaddressRețeabyteorder uint32, dataIndicator uintptr, mărime uint32) bool {
	ipconsole.MTipărește(([]byte)("ipHandler:OnInternet"))
	return false
}
func (sine *TInternetprotocolhandler) Trimite(destinațieipaddressRețeabyteorder uint32, pprotocol uint8, dataIndicator uintptr, mărime uint32) {

	ipprovider.Trimite(destinațieipaddressRețeabyteorder, pprotocol, dataIndicator, mărime)
}
func (sine *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpethernetCadruhandler struct {
	TEthernetCadruhandler
}

var ipprovider TInternetprotocolprovider

func (sine *IpethernetCadruhandler) EthernetCadrureceivewhen(dataIndicator uintptr, mărime int) bool {
	ipconsole.MTipărește(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetCadrureceivewhen(dataIndicator, uint32(mărime))

}

func (sine *IpethernetCadruhandler) Trimite(destinațieipaddressRețeabyteorder uint64, dataIndicator uintptr, mărime uint32) {
	ipconsole.MTipărește(([]byte)("ipefhandler:send\n"))
	var ethernetTipbe = Unsignedinteger16r(0x0800)
	sine.TEthernetCadruhandler.CadruTrimite(destinațieipaddressRețeabyteorder, ethernetTipbe, dataIndicator, mărime)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMasca	uint32
}

var efhandler IEthernetCadruhandler

func (sine *TInternetprotocolprovider) Init(pefprovider TEthernetCadruprovider, pefhandler IEthernetCadruhandler, arp Arpprovider, gatewayip uint32, subnetMasca uint32) {

	efhandler = pefhandler
	efhandler.Definithandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	sine.arpprovider = arp
	sine.Gatewayip = gatewayip
	sine.SubnetMasca = subnetMasca
	ipprovider = *sine
}
func (sine *TInternetprotocolprovider) EthernetCadrureceivewhen(ethernetCadrupayload uintptr, mărime uint32) bool {
	if mărime < uint32(ipMărime) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Mesajbuffer = (*TInternetprotocolv4Mesajbuffer)(Pointer(ethernetCadrupayload))
	var internetprotocolMesaj TInternetprotocolv4Mesaj
	internetprotocolMesaj.Init(*buffer_2)

	var reply bool = false

	if internetprotocolMesaj.destinațieipaddress == uint32(efhandler.Getipaddress()) {

		var durată uint32 = uint32(internetprotocolMesaj.totalDurată)
		if durată > mărime {
			durată = mărime
		}
		if handler_2[internetprotocolMesaj.protocol] != nil {
			reply = handler_2[internetprotocolMesaj.protocol].Internetprotocolreceivewhen(internetprotocolMesaj.sursăipaddress, internetprotocolMesaj.destinațieipaddress, ethernetCadrupayload+uintptr(4*internetprotocolMesaj.headerDurată), uint32(durată-uint32(4*internetprotocolMesaj.headerDurată)))

		}
	}

	if reply {

		var temporary = internetprotocolMesaj.destinațieipaddress
		internetprotocolMesaj.destinațieipaddress = internetprotocolMesaj.sursăipaddress
		internetprotocolMesaj.sursăipaddress = temporary

		internetprotocolMesaj.orătolive = 0x40
		internetprotocolMesaj.checksum = 0

		internetprotocolMesaj.Definitbuffer(buffer_2)
		internetprotocolMesaj.checksum = sine.Checksum((*([4096]uint16))(Pointer(ethernetCadrupayload)), uint32(4*internetprotocolMesaj.headerDurată))

		internetprotocolMesaj.Definitbuffer(buffer_2)

	}

	ipconsole.MTipărește(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Tipărește(internetprotocolMesaj.sursăipaddress)
	ipconsole.MTipărește(([]byte)(":"))
	ipconsole.MUnsignedinteger32Tipărește(internetprotocolMesaj.destinațieipaddress)
	ipconsole.MTipărește(([]byte)(":"))
	ipconsole.MUnsignedinteger16Tipărește(uint16(internetprotocolMesaj.headerDurată))
	ipconsole.MTipărește(([]byte)(":"))
	ipconsole.MUnsignedinteger16Tipărește(uint16(internetprotocolMesaj.versiune))
	ipconsole.MTipărește(([]byte)(":"))
	ipconsole.MUnsignedinteger16Tipărește(internetprotocolMesaj.totalDurată)
	ipconsole.MTipărește(([]byte)(":"))
	ipconsole.MUnsignedinteger32Tipărește(uint32(efhandler.Getipaddress()))
	ipconsole.MTipărește(([]byte)(":"))
	ipconsole.MTipărește(([]byte)("\n"))

	return reply

}
func (sine *TInternetprotocolprovider) Trimite(destinațieipaddressRețeabyteorder uint32, protocol uint8, dataIndicator uintptr, mărime uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Mesajbuffer = (*TInternetprotocolv4Mesajbuffer)(Pointer(&buffer1_2))
	var mesaj TInternetprotocolv4Mesaj = TInternetprotocolv4Mesaj{}
	mesaj.versiune = 4
	mesaj.headerDurată = ipMărime / 4
	mesaj.tos = 0
	mesaj.totalDurată = Unsignedinteger16r(uint16(mărime + uint32(ipMărime)))

	mesaj.ident = 0x0100
	mesaj.indicatorișioffset = 0x0040
	mesaj.orătolive = 0x40
	mesaj.protocol = protocol

	mesaj.destinațieipaddress = destinațieipaddressRețeabyteorder

	mesaj.sursăipaddress = uint32(efhandler.Getipaddress())

	mesaj.checksum = 0

	mesaj.Definitbuffer(buffer_2)
	mesaj.checksum = sine.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipMărime))
	mesaj.Definitbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataIndicator))

	for i := 0; i < int(mărime); i++ {

		buffer1_2[i+int(ipMărime)] = databuffer_2[i]
	}

	ipconsole.MTipăreștexy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(mărime)+int(ipMărime); i++ {
		ipconsole.MHexadecimalTipărește(buffer1_2[i])
	}
	ipconsole.MTipărește(([]byte)(":"))
	ipconsole.MTipărește(([]byte)("]\n"))

	var înaintehopipaddressRețeabyteorder uint32 = destinațieipaddressRețeabyteorder
	if (destinațieipaddressRețeabyteorder & sine.SubnetMasca) != (mesaj.sursăipaddress & sine.SubnetMasca) {
		înaintehopipaddressRețeabyteorder = sine.Gatewayip
	}

	var trimitedataIndicator = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Tipărește(înaintehopipaddressRețeabyteorder)

	var ethernetTipbe = Unsignedinteger16r(0x0800)
	efhandler.CadruTrimite(sine.arpprovider.Resolve(înaintehopipaddressRețeabyteorder), ethernetTipbe, trimitedataIndicator, uint32(ipMărime)+uint32(mărime))

}
func (sine *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, duratăIntrareOcteți uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataOcteți [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (duratăIntrareOcteți % 2) != 0 {
		temporary += uint32(uint16(dataOcteți[duratăIntrareOcteți-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (sine *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
