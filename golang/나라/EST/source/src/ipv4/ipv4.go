package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetRaam"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4Teadebuffer struct {
	lenver		byte
	tos		byte
	kokkuKestus	[2]byte

	ident		[2]byte
	lipudjaoffset	[2]byte

	aegtolive	byte
	protocol	byte
	checksum	[2]byte

	aLLIKASipaddress	[4]byte
	sihtfailipaddress	[4]byte
}

var ipSuurus uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Teade struct {
	headerKestus	uint8
	versioon	uint8
	tos		uint8
	kokkuKestus	uint16

	ident		uint16
	lipudjaoffset	uint16

	aegtolive	uint8
	protocol	uint8
	checksum	uint16

	aLLIKASipaddress	uint32
	sihtfailipaddress	uint32
}

func (ise *TInternetprotocolv4Teade) Init(buffer_2 TInternetprotocolv4Teadebuffer) {

	ise.versioon = ((buffer_2.lenver & 0xF0) >> 4)
	ise.headerKestus = buffer_2.lenver & 0x0F
	ise.tos = buffer_2.tos
	ise.kokkuKestus = Unsignedinteger16r(Massiivtounsignedinteger16(buffer_2.kokkuKestus))

	ise.ident = Unsignedinteger16r(Massiivtounsignedinteger16(buffer_2.ident))
	ise.lipudjaoffset = Unsignedinteger16r(Massiivtounsignedinteger16(buffer_2.lipudjaoffset))

	ise.aegtolive = buffer_2.aegtolive
	ise.protocol = buffer_2.protocol
	ise.checksum = Unsignedinteger16r(Massiivtounsignedinteger16(buffer_2.checksum))

	ise.aLLIKASipaddress = Unsignedinteger32r(Massiivtounsignedinteger32(buffer_2.aLLIKASipaddress))
	ise.sihtfailipaddress = Unsignedinteger32r(Massiivtounsignedinteger32(buffer_2.sihtfailipaddress))

}
func (ise *TInternetprotocolv4Teade) Määrabuffer(buffer_2 *TInternetprotocolv4Teadebuffer) {

	buffer_2.lenver = byte(((ise.versioon & 0x0F) << 4) | (ise.headerKestus & 0x0F))
	buffer_2.tos = ise.tos
	buffer_2.kokkuKestus = Unsignedinteger16toMassiiv(ise.kokkuKestus)

	buffer_2.ident = Unsignedinteger16toMassiiv(ise.ident)
	buffer_2.lipudjaoffset = Unsignedinteger16toMassiiv(ise.lipudjaoffset)

	buffer_2.aegtolive = ise.aegtolive
	buffer_2.protocol = ise.protocol
	buffer_2.checksum = Unsignedinteger16toMassiiv(ise.checksum)

	buffer_2.aLLIKASipaddress = Unsignedinteger32toMassiiv(ise.aLLIKASipaddress)
	buffer_2.sihtfailipaddress = Unsignedinteger32toMassiiv(ise.sihtfailipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(aLLIKASipaddressVõrkbyteorder uint32, sihtfailipaddressVõrkbyteorder uint32, dataKursor uintptr, suurus uint32) bool
	Saada(sihtfailipaddressVõrkbyteorder uint32, pprotocol uint8, dataKursor uintptr, suurus uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetRaamhandler IpethernetRaamhandler = IpethernetRaamhandler{}
var protocol uint8

func (ise *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (ise *TInternetprotocolhandler) Internetprotocolreceivewhen(aLLIKASipaddressVõrkbyteorder uint32, sihtfailipaddressVõrkbyteorder uint32, dataKursor uintptr, suurus uint32) bool {
	ipconsole.MPrindi(([]byte)("ipHandler:OnInternet"))
	return false
}
func (ise *TInternetprotocolhandler) Saada(sihtfailipaddressVõrkbyteorder uint32, pprotocol uint8, dataKursor uintptr, suurus uint32) {

	ipprovider.Saada(sihtfailipaddressVõrkbyteorder, pprotocol, dataKursor, suurus)
}
func (ise *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpethernetRaamhandler struct {
	TEthernetRaamhandler
}

var ipprovider TInternetprotocolprovider

func (ise *IpethernetRaamhandler) EthernetRaamreceivewhen(dataKursor uintptr, suurus int) bool {
	ipconsole.MPrindi(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetRaamreceivewhen(dataKursor, uint32(suurus))

}

func (ise *IpethernetRaamhandler) Saada(sihtfailipaddressVõrkbyteorder uint64, dataKursor uintptr, suurus uint32) {
	ipconsole.MPrindi(([]byte)("ipefhandler:send\n"))
	var ethernetLiikbe = Unsignedinteger16r(0x0800)
	ise.TEthernetRaamhandler.RaamSaada(sihtfailipaddressVõrkbyteorder, ethernetLiikbe, dataKursor, suurus)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetRaamhandler

func (ise *TInternetprotocolprovider) Init(pefprovider TEthernetRaamprovider, pefhandler IEthernetRaamhandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Määrahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	ise.arpprovider = arp
	ise.Gatewayip = gatewayip
	ise.Subnetmask = subnetmask
	ipprovider = *ise
}
func (ise *TInternetprotocolprovider) EthernetRaamreceivewhen(ethernetRaampayload uintptr, suurus uint32) bool {
	if suurus < uint32(ipSuurus) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Teadebuffer = (*TInternetprotocolv4Teadebuffer)(Pointer(ethernetRaampayload))
	var internetprotocolTeade TInternetprotocolv4Teade
	internetprotocolTeade.Init(*buffer_2)

	var reply bool = false

	if internetprotocolTeade.sihtfailipaddress == uint32(efhandler.Getipaddress()) {

		var kestus uint32 = uint32(internetprotocolTeade.kokkuKestus)
		if kestus > suurus {
			kestus = suurus
		}
		if handler_2[internetprotocolTeade.protocol] != nil {
			reply = handler_2[internetprotocolTeade.protocol].Internetprotocolreceivewhen(internetprotocolTeade.aLLIKASipaddress, internetprotocolTeade.sihtfailipaddress, ethernetRaampayload+uintptr(4*internetprotocolTeade.headerKestus), uint32(kestus-uint32(4*internetprotocolTeade.headerKestus)))

		}
	}

	if reply {

		var temporary = internetprotocolTeade.sihtfailipaddress
		internetprotocolTeade.sihtfailipaddress = internetprotocolTeade.aLLIKASipaddress
		internetprotocolTeade.aLLIKASipaddress = temporary

		internetprotocolTeade.aegtolive = 0x40
		internetprotocolTeade.checksum = 0

		internetprotocolTeade.Määrabuffer(buffer_2)
		internetprotocolTeade.checksum = ise.Checksum((*([4096]uint16))(Pointer(ethernetRaampayload)), uint32(4*internetprotocolTeade.headerKestus))

		internetprotocolTeade.Määrabuffer(buffer_2)

	}

	ipconsole.MPrindi(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Prindi(internetprotocolTeade.aLLIKASipaddress)
	ipconsole.MPrindi(([]byte)(":"))
	ipconsole.MUnsignedinteger32Prindi(internetprotocolTeade.sihtfailipaddress)
	ipconsole.MPrindi(([]byte)(":"))
	ipconsole.MUnsignedinteger16Prindi(uint16(internetprotocolTeade.headerKestus))
	ipconsole.MPrindi(([]byte)(":"))
	ipconsole.MUnsignedinteger16Prindi(uint16(internetprotocolTeade.versioon))
	ipconsole.MPrindi(([]byte)(":"))
	ipconsole.MUnsignedinteger16Prindi(internetprotocolTeade.kokkuKestus)
	ipconsole.MPrindi(([]byte)(":"))
	ipconsole.MUnsignedinteger32Prindi(uint32(efhandler.Getipaddress()))
	ipconsole.MPrindi(([]byte)(":"))
	ipconsole.MPrindi(([]byte)("\n"))

	return reply

}
func (ise *TInternetprotocolprovider) Saada(sihtfailipaddressVõrkbyteorder uint32, protocol uint8, dataKursor uintptr, suurus uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Teadebuffer = (*TInternetprotocolv4Teadebuffer)(Pointer(&buffer1_2))
	var teade TInternetprotocolv4Teade = TInternetprotocolv4Teade{}
	teade.versioon = 4
	teade.headerKestus = ipSuurus / 4
	teade.tos = 0
	teade.kokkuKestus = Unsignedinteger16r(uint16(suurus + uint32(ipSuurus)))

	teade.ident = 0x0100
	teade.lipudjaoffset = 0x0040
	teade.aegtolive = 0x40
	teade.protocol = protocol

	teade.sihtfailipaddress = sihtfailipaddressVõrkbyteorder

	teade.aLLIKASipaddress = uint32(efhandler.Getipaddress())

	teade.checksum = 0

	teade.Määrabuffer(buffer_2)
	teade.checksum = ise.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipSuurus))
	teade.Määrabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursor))

	for i := 0; i < int(suurus); i++ {

		buffer1_2[i+int(ipSuurus)] = databuffer_2[i]
	}

	ipconsole.MPrindixy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(suurus)+int(ipSuurus); i++ {
		ipconsole.MHexadecimalPrindi(buffer1_2[i])
	}
	ipconsole.MPrindi(([]byte)(":"))
	ipconsole.MPrindi(([]byte)("]\n"))

	var järgminehopipaddressVõrkbyteorder uint32 = sihtfailipaddressVõrkbyteorder
	if (sihtfailipaddressVõrkbyteorder & ise.Subnetmask) != (teade.aLLIKASipaddress & ise.Subnetmask) {
		järgminehopipaddressVõrkbyteorder = ise.Gatewayip
	}

	var saadadataKursor = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Prindi(järgminehopipaddressVõrkbyteorder)

	var ethernetLiikbe = Unsignedinteger16r(0x0800)
	efhandler.RaamSaada(ise.arpprovider.Resolve(järgminehopipaddressVõrkbyteorder), ethernetLiikbe, saadadataKursor, uint32(ipSuurus)+uint32(suurus))

}
func (ise *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, kestusSissebaiti uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var databaiti [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (kestusSissebaiti % 2) != 0 {
		temporary += uint32(uint16(databaiti[kestusSissebaiti-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (ise *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
