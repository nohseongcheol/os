/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetIkadiri"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInterinetiprotocolv4Ubutumwabuffer struct {
	lenver			byte
	tos			byte
	igiteranyolength	[2]byte

	ident			[2]byte
	amabenderaandoffset	[2]byte

	igihetolive	byte
	protocol	byte
	checksum	[2]byte

	inkomokoipaddress	[4]byte
	destinationipaddress	[4]byte
}

var ipIngano uint8 = (4 + 4 + 4 + 8)

type TInterinetiprotocolv4Ubutumwa struct {
	headerlength		uint8
	version			uint8
	tos			uint8
	igiteranyolength	uint16

	ident			uint16
	amabenderaandoffset	uint16

	igihetolive	uint8
	protocol	uint8
	checksum	uint16

	inkomokoipaddress	uint32
	destinationipaddress	uint32
}

func (self *TInterinetiprotocolv4Ubutumwa) Init(buffer_2 TInterinetiprotocolv4Ubutumwabuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerlength = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.igiteranyolength = Unsignedinteger16r(Imbonerahamwetounsignedinteger16(buffer_2.igiteranyolength))

	self.ident = Unsignedinteger16r(Imbonerahamwetounsignedinteger16(buffer_2.ident))
	self.amabenderaandoffset = Unsignedinteger16r(Imbonerahamwetounsignedinteger16(buffer_2.amabenderaandoffset))

	self.igihetolive = buffer_2.igihetolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Imbonerahamwetounsignedinteger16(buffer_2.checksum))

	self.inkomokoipaddress = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer_2.inkomokoipaddress))
	self.destinationipaddress = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TInterinetiprotocolv4Ubutumwa) Setbuffer(buffer_2 *TInterinetiprotocolv4Ubutumwabuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerlength & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.igiteranyolength = Unsignedinteger16toImbonerahamwe(self.igiteranyolength)

	buffer_2.ident = Unsignedinteger16toImbonerahamwe(self.ident)
	buffer_2.amabenderaandoffset = Unsignedinteger16toImbonerahamwe(self.amabenderaandoffset)

	buffer_2.igihetolive = self.igihetolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toImbonerahamwe(self.checksum)

	buffer_2.inkomokoipaddress = Unsignedinteger32toImbonerahamwe(self.inkomokoipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toImbonerahamwe(self.destinationipaddress)

}

type IInterinetiprotocolhandler interface {
	Init(backend TInterinetiprotocolprovider, pihandler IInterinetiprotocolhandler, pprotocol uint8)
	Interinetiprotocolreceivewhen(inkomokoipaddressurusobebyteorder uint32, destinationipaddressurusobebyteorder uint32, datapointer uintptr, ingano uint32) bool
	Send(destinationipaddressurusobebyteorder uint32, pprotocol uint8, datapointer uintptr, ingano uint32)
	Providerget() *TInterinetiprotocolprovider
}

type TInterinetiprotocolhandler struct {
}

var ipethernetIkadirihandler IpethernetIkadirihandler = IpethernetIkadirihandler{}
var protocol uint8

func (self *TInterinetiprotocolhandler) Init(backend TInterinetiprotocolprovider, pihandler IInterinetiprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInterinetiprotocolhandler) Interinetiprotocolreceivewhen(inkomokoipaddressurusobebyteorder uint32, destinationipaddressurusobebyteorder uint32, datapointer uintptr, ingano uint32) bool {
	ipconsole.MGucapa(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInterinetiprotocolhandler) Send(destinationipaddressurusobebyteorder uint32, pprotocol uint8, datapointer uintptr, ingano uint32) {

	ipprovider.Send(destinationipaddressurusobebyteorder, pprotocol, datapointer, ingano)
}
func (self *TInterinetiprotocolhandler) Providerget() *TInterinetiprotocolprovider {
	return &ipprovider
}

type IpethernetIkadirihandler struct {
	TEthernetIkadirihandler
}

var ipprovider TInterinetiprotocolprovider

func (self *IpethernetIkadirihandler) EthernetIkadirireceivewhen(datapointer uintptr, ingano int) bool {
	ipconsole.MGucapa(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetIkadirireceivewhen(datapointer, uint32(ingano))

}

func (self *IpethernetIkadirihandler) Send(destinationipaddressurusobebyteorder uint64, datapointer uintptr, ingano uint32) {
	ipconsole.MGucapa(([]byte)("ipefhandler:send\n"))
	var ethernetUbwokobe = Unsignedinteger16r(0x0800)
	self.TEthernetIkadirihandler.Ikadirisend(destinationipaddressurusobebyteorder, ethernetUbwokobe, datapointer, ingano)

}

var handler_2 [255]IInterinetiprotocolhandler

type TInterinetiprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetIkadirihandler

func (self *TInterinetiprotocolprovider) Init(pefprovider TEthernetIkadiriprovider, pefhandler IEthernetIkadirihandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Sethandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnetmask = subnetmask
	ipprovider = *self
}
func (self *TInterinetiprotocolprovider) EthernetIkadirireceivewhen(ethernetIkadiripayload uintptr, ingano uint32) bool {
	if ingano < uint32(ipIngano) {
		return false
	}

	var buffer_2 *TInterinetiprotocolv4Ubutumwabuffer = (*TInterinetiprotocolv4Ubutumwabuffer)(Pointer(ethernetIkadiripayload))
	var interinetiprotocolUbutumwa TInterinetiprotocolv4Ubutumwa
	interinetiprotocolUbutumwa.Init(*buffer_2)

	var reply bool = false

	if interinetiprotocolUbutumwa.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var length uint32 = uint32(interinetiprotocolUbutumwa.igiteranyolength)
		if length > ingano {
			length = ingano
		}
		if handler_2[interinetiprotocolUbutumwa.protocol] != nil {
			reply = handler_2[interinetiprotocolUbutumwa.protocol].Interinetiprotocolreceivewhen(interinetiprotocolUbutumwa.inkomokoipaddress, interinetiprotocolUbutumwa.destinationipaddress, ethernetIkadiripayload+uintptr(4*interinetiprotocolUbutumwa.headerlength), uint32(length-uint32(4*interinetiprotocolUbutumwa.headerlength)))

		}
	}

	if reply {

		var temporary = interinetiprotocolUbutumwa.destinationipaddress
		interinetiprotocolUbutumwa.destinationipaddress = interinetiprotocolUbutumwa.inkomokoipaddress
		interinetiprotocolUbutumwa.inkomokoipaddress = temporary

		interinetiprotocolUbutumwa.igihetolive = 0x40
		interinetiprotocolUbutumwa.checksum = 0

		interinetiprotocolUbutumwa.Setbuffer(buffer_2)
		interinetiprotocolUbutumwa.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetIkadiripayload)), uint32(4*interinetiprotocolUbutumwa.headerlength))

		interinetiprotocolUbutumwa.Setbuffer(buffer_2)

	}

	ipconsole.MGucapa(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Gucapa(interinetiprotocolUbutumwa.inkomokoipaddress)
	ipconsole.MGucapa(([]byte)(":"))
	ipconsole.MUnsignedinteger32Gucapa(interinetiprotocolUbutumwa.destinationipaddress)
	ipconsole.MGucapa(([]byte)(":"))
	ipconsole.MUnsignedinteger16Gucapa(uint16(interinetiprotocolUbutumwa.headerlength))
	ipconsole.MGucapa(([]byte)(":"))
	ipconsole.MUnsignedinteger16Gucapa(uint16(interinetiprotocolUbutumwa.version))
	ipconsole.MGucapa(([]byte)(":"))
	ipconsole.MUnsignedinteger16Gucapa(interinetiprotocolUbutumwa.igiteranyolength)
	ipconsole.MGucapa(([]byte)(":"))
	ipconsole.MUnsignedinteger32Gucapa(uint32(efhandler.Getipaddress()))
	ipconsole.MGucapa(([]byte)(":"))
	ipconsole.MGucapa(([]byte)("\n"))

	return reply

}
func (self *TInterinetiprotocolprovider) Send(destinationipaddressurusobebyteorder uint32, protocol uint8, datapointer uintptr, ingano uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInterinetiprotocolv4Ubutumwabuffer = (*TInterinetiprotocolv4Ubutumwabuffer)(Pointer(&buffer1_2))
	var ubutumwa TInterinetiprotocolv4Ubutumwa = TInterinetiprotocolv4Ubutumwa{}
	ubutumwa.version = 4
	ubutumwa.headerlength = ipIngano / 4
	ubutumwa.tos = 0
	ubutumwa.igiteranyolength = Unsignedinteger16r(uint16(ingano + uint32(ipIngano)))

	ubutumwa.ident = 0x0100
	ubutumwa.amabenderaandoffset = 0x0040
	ubutumwa.igihetolive = 0x40
	ubutumwa.protocol = protocol

	ubutumwa.destinationipaddress = destinationipaddressurusobebyteorder

	ubutumwa.inkomokoipaddress = uint32(efhandler.Getipaddress())

	ubutumwa.checksum = 0

	ubutumwa.Setbuffer(buffer_2)
	ubutumwa.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipIngano))
	ubutumwa.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(ingano); i++ {

		buffer1_2[i+int(ipIngano)] = databuffer_2[i]
	}

	ipconsole.MGucapaxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(ingano)+int(ipIngano); i++ {
		ipconsole.MHexadecimalGucapa(buffer1_2[i])
	}
	ipconsole.MGucapa(([]byte)(":"))
	ipconsole.MGucapa(([]byte)("]\n"))

	var ikurikirahopipaddressurusobebyteorder uint32 = destinationipaddressurusobebyteorder
	if (destinationipaddressurusobebyteorder & self.Subnetmask) != (ubutumwa.inkomokoipaddress & self.Subnetmask) {
		ikurikirahopipaddressurusobebyteorder = self.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Gucapa(ikurikirahopipaddressurusobebyteorder)

	var ethernetUbwokobe = Unsignedinteger16r(0x0800)
	efhandler.Ikadirisend(self.arpprovider.Resolve(ikurikirahopipaddressurusobebyteorder), ethernetUbwokobe, senddatapointer, uint32(ipIngano)+uint32(ingano))

}
func (self *TInterinetiprotocolprovider) Checksum(pdata *[4096]uint16, lengthImbereBayite uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBayite [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthImbereBayite % 2) != 0 {
		temporary += uint32(uint16(dataBayite[lengthImbereBayite-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInterinetiprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
