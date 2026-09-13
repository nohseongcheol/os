package ipv4

import . "unsafe"
import . "util"
import . "konsoly"
import . "ethernetframe"
import . "arp"

var ipKonsoly TKonsoly = TKonsoly{}

type TInternetprotocolv4Hafatrabuffer struct {
	lenver		byte
	tos		byte
	tontalinylength	[2]byte

	ident		[2]byte
	sainaandoffset	[2]byte

	fotoanatolive	byte
	protocol	byte
	checksum	[2]byte

	loharanoipaddress	[4]byte
	destinationipaddress	[4]byte
}

var ipHabe uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Hafatra struct {
	headerlength	uint8
	version		uint8
	tos		uint8
	tontalinylength	uint16

	ident		uint16
	sainaandoffset	uint16

	fotoanatolive	uint8
	protocol	uint8
	checksum	uint16

	loharanoipaddress	uint32
	destinationipaddress	uint32
}

func (nytena *TInternetprotocolv4Hafatra) Init(buffer_2 TInternetprotocolv4Hafatrabuffer) {

	nytena.version = ((buffer_2.lenver & 0xF0) >> 4)
	nytena.headerlength = buffer_2.lenver & 0x0F
	nytena.tos = buffer_2.tos
	nytena.tontalinylength = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.tontalinylength))

	nytena.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	nytena.sainaandoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.sainaandoffset))

	nytena.fotoanatolive = buffer_2.fotoanatolive
	nytena.protocol = buffer_2.protocol
	nytena.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	nytena.loharanoipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.loharanoipaddress))
	nytena.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))

}
func (nytena *TInternetprotocolv4Hafatra) Setbuffer(buffer_2 *TInternetprotocolv4Hafatrabuffer) {

	buffer_2.lenver = byte(((nytena.version & 0x0F) << 4) | (nytena.headerlength & 0x0F))
	buffer_2.tos = nytena.tos
	buffer_2.tontalinylength = Unsignedinteger16toarray(nytena.tontalinylength)

	buffer_2.ident = Unsignedinteger16toarray(nytena.ident)
	buffer_2.sainaandoffset = Unsignedinteger16toarray(nytena.sainaandoffset)

	buffer_2.fotoanatolive = nytena.fotoanatolive
	buffer_2.protocol = nytena.protocol
	buffer_2.checksum = Unsignedinteger16toarray(nytena.checksum)

	buffer_2.loharanoipaddress = Unsignedinteger32toarray(nytena.loharanoipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(nytena.destinationipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(loharanoipaddressRezobyteorder uint32, destinationipaddressRezobyteorder uint32, datapointer uintptr, habe uint32) bool
	Send(destinationipaddressRezobyteorder uint32, pprotocol uint8, datapointer uintptr, habe uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetframehandler Ipethernetframehandler = Ipethernetframehandler{}
var protocol uint8

func (nytena *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (nytena *TInternetprotocolhandler) Internetprotocolreceivewhen(loharanoipaddressRezobyteorder uint32, destinationipaddressRezobyteorder uint32, datapointer uintptr, habe uint32) bool {
	ipKonsoly.MAtontay(([]byte)("ipHandler:OnInternet"))
	return false
}
func (nytena *TInternetprotocolhandler) Send(destinationipaddressRezobyteorder uint32, pprotocol uint8, datapointer uintptr, habe uint32) {

	ipprovider.Send(destinationipaddressRezobyteorder, pprotocol, datapointer, habe)
}
func (nytena *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var ipprovider TInternetprotocolprovider

func (nytena *Ipethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, habe int) bool {
	ipKonsoly.MAtontay(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetframereceivewhen(datapointer, uint32(habe))

}

func (nytena *Ipethernetframehandler) Send(destinationipaddressRezobyteorder uint64, datapointer uintptr, habe uint32) {
	ipKonsoly.MAtontay(([]byte)("ipefhandler:send\n"))
	var ethernetKarazanabe = Unsignedinteger16r(0x0800)
	nytena.TEthernetframehandler.Framesend(destinationipaddressRezobyteorder, ethernetKarazanabe, datapointer, habe)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetframehandler

func (nytena *TInternetprotocolprovider) Init(pefprovider TEthernetframeprovider, pefhandler IEthernetframehandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Sethandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	nytena.arpprovider = arp
	nytena.Gatewayip = gatewayip
	nytena.Subnetmask = subnetmask
	ipprovider = *nytena
}
func (nytena *TInternetprotocolprovider) Ethernetframereceivewhen(ethernetframepayload uintptr, habe uint32) bool {
	if habe < uint32(ipHabe) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Hafatrabuffer = (*TInternetprotocolv4Hafatrabuffer)(Pointer(ethernetframepayload))
	var internetprotocolHafatra TInternetprotocolv4Hafatra
	internetprotocolHafatra.Init(*buffer_2)

	var reply bool = false

	if internetprotocolHafatra.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var length uint32 = uint32(internetprotocolHafatra.tontalinylength)
		if length > habe {
			length = habe
		}
		if handler_2[internetprotocolHafatra.protocol] != nil {
			reply = handler_2[internetprotocolHafatra.protocol].Internetprotocolreceivewhen(internetprotocolHafatra.loharanoipaddress, internetprotocolHafatra.destinationipaddress, ethernetframepayload+uintptr(4*internetprotocolHafatra.headerlength), uint32(length-uint32(4*internetprotocolHafatra.headerlength)))

		}
	}

	if reply {

		var temporary = internetprotocolHafatra.destinationipaddress
		internetprotocolHafatra.destinationipaddress = internetprotocolHafatra.loharanoipaddress
		internetprotocolHafatra.loharanoipaddress = temporary

		internetprotocolHafatra.fotoanatolive = 0x40
		internetprotocolHafatra.checksum = 0

		internetprotocolHafatra.Setbuffer(buffer_2)
		internetprotocolHafatra.checksum = nytena.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*internetprotocolHafatra.headerlength))

		internetprotocolHafatra.Setbuffer(buffer_2)

	}

	ipKonsoly.MAtontay(([]byte)("ipmessage"))
	ipKonsoly.MUnsignedinteger32Atontay(internetprotocolHafatra.loharanoipaddress)
	ipKonsoly.MAtontay(([]byte)(":"))
	ipKonsoly.MUnsignedinteger32Atontay(internetprotocolHafatra.destinationipaddress)
	ipKonsoly.MAtontay(([]byte)(":"))
	ipKonsoly.MUnsignedinteger16Atontay(uint16(internetprotocolHafatra.headerlength))
	ipKonsoly.MAtontay(([]byte)(":"))
	ipKonsoly.MUnsignedinteger16Atontay(uint16(internetprotocolHafatra.version))
	ipKonsoly.MAtontay(([]byte)(":"))
	ipKonsoly.MUnsignedinteger16Atontay(internetprotocolHafatra.tontalinylength)
	ipKonsoly.MAtontay(([]byte)(":"))
	ipKonsoly.MUnsignedinteger32Atontay(uint32(efhandler.Getipaddress()))
	ipKonsoly.MAtontay(([]byte)(":"))
	ipKonsoly.MAtontay(([]byte)("\n"))

	return reply

}
func (nytena *TInternetprotocolprovider) Send(destinationipaddressRezobyteorder uint32, protocol uint8, datapointer uintptr, habe uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Hafatrabuffer = (*TInternetprotocolv4Hafatrabuffer)(Pointer(&buffer1_2))
	var hafatra TInternetprotocolv4Hafatra = TInternetprotocolv4Hafatra{}
	hafatra.version = 4
	hafatra.headerlength = ipHabe / 4
	hafatra.tos = 0
	hafatra.tontalinylength = Unsignedinteger16r(uint16(habe + uint32(ipHabe)))

	hafatra.ident = 0x0100
	hafatra.sainaandoffset = 0x0040
	hafatra.fotoanatolive = 0x40
	hafatra.protocol = protocol

	hafatra.destinationipaddress = destinationipaddressRezobyteorder

	hafatra.loharanoipaddress = uint32(efhandler.Getipaddress())

	hafatra.checksum = 0

	hafatra.Setbuffer(buffer_2)
	hafatra.checksum = nytena.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipHabe))
	hafatra.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(habe); i++ {

		buffer1_2[i+int(ipHabe)] = databuffer_2[i]
	}

	ipKonsoly.MAtontayxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(habe)+int(ipHabe); i++ {
		ipKonsoly.MHexadecimalAtontay(buffer1_2[i])
	}
	ipKonsoly.MAtontay(([]byte)(":"))
	ipKonsoly.MAtontay(([]byte)("]\n"))

	var manarakahopipaddressRezobyteorder uint32 = destinationipaddressRezobyteorder
	if (destinationipaddressRezobyteorder & nytena.Subnetmask) != (hafatra.loharanoipaddress & nytena.Subnetmask) {
		manarakahopipaddressRezobyteorder = nytena.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipKonsoly.MUnsignedinteger32Atontay(manarakahopipaddressRezobyteorder)

	var ethernetKarazanabe = Unsignedinteger16r(0x0800)
	efhandler.Framesend(nytena.arpprovider.Resolve(manarakahopipaddressRezobyteorder), ethernetKarazanabe, senddatapointer, uint32(ipHabe)+uint32(habe))

}
func (nytena *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, lengthAnatyOctet uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataOctet [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthAnatyOctet % 2) != 0 {
		temporary += uint32(uint16(dataOctet[lengthAnatyOctet-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (nytena *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
