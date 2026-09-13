package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetframe"
import . "arp"

var ipconsole TConsole = TConsole{}

type TИнтернетprotocolv4messagebuffer struct {
	lenver		byte
	tos		byte
	бардыгыУзундук	[2]byte

	ident			[2]byte
	желектериandoffset	[2]byte

	timetolive	byte
	protocol	byte
	checksum	[2]byte

	баштапкытекстipaddress	[4]byte
	destinationipaddress	[4]byte
}

var ipӨлчөм uint8 = (4 + 4 + 4 + 8)

type TИнтернетprotocolv4message struct {
	headerУзундук	uint8
	version		uint8
	tos		uint8
	бардыгыУзундук	uint16

	ident			uint16
	желектериandoffset	uint16

	timetolive	uint8
	protocol	uint8
	checksum	uint16

	баштапкытекстipaddress	uint32
	destinationipaddress	uint32
}

func (self *TИнтернетprotocolv4message) Init(buffer_2 TИнтернетprotocolv4messagebuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerУзундук = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.бардыгыУзундук = Unsignedinteger16r(Массивtounsignedinteger16(buffer_2.бардыгыУзундук))

	self.ident = Unsignedinteger16r(Массивtounsignedinteger16(buffer_2.ident))
	self.желектериandoffset = Unsignedinteger16r(Массивtounsignedinteger16(buffer_2.желектериandoffset))

	self.timetolive = buffer_2.timetolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Массивtounsignedinteger16(buffer_2.checksum))

	self.баштапкытекстipaddress = Unsignedinteger32r(Массивtounsignedinteger32(buffer_2.баштапкытекстipaddress))
	self.destinationipaddress = Unsignedinteger32r(Массивtounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TИнтернетprotocolv4message) Setbuffer(buffer_2 *TИнтернетprotocolv4messagebuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerУзундук & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.бардыгыУзундук = Unsignedinteger16toМассив(self.бардыгыУзундук)

	buffer_2.ident = Unsignedinteger16toМассив(self.ident)
	buffer_2.желектериandoffset = Unsignedinteger16toМассив(self.желектериandoffset)

	buffer_2.timetolive = self.timetolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toМассив(self.checksum)

	buffer_2.баштапкытекстipaddress = Unsignedinteger32toМассив(self.баштапкытекстipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toМассив(self.destinationipaddress)

}

type IИнтернетprotocolhandler interface {
	Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8)
	Интернетprotocolreceivewhen(баштапкытекстipaddressТармакbyteorder uint32, destinationipaddressТармакbyteorder uint32, dataКөрсөткүч uintptr, өлчөм uint32) bool
	Send(destinationipaddressТармакbyteorder uint32, pprotocol uint8, dataКөрсөткүч uintptr, өлчөм uint32)
	Providerget() *TИнтернетprotocolprovider
}

type TИнтернетprotocolhandler struct {
}

var ipethernetframehandler Ipethernetframehandler = Ipethernetframehandler{}
var protocol uint8

func (self *TИнтернетprotocolhandler) Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TИнтернетprotocolhandler) Интернетprotocolreceivewhen(баштапкытекстipaddressТармакbyteorder uint32, destinationipaddressТармакbyteorder uint32, dataКөрсөткүч uintptr, өлчөм uint32) bool {
	ipconsole.MБасма(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TИнтернетprotocolhandler) Send(destinationipaddressТармакbyteorder uint32, pprotocol uint8, dataКөрсөткүч uintptr, өлчөм uint32) {

	ipprovider.Send(destinationipaddressТармакbyteorder, pprotocol, dataКөрсөткүч, өлчөм)
}
func (self *TИнтернетprotocolhandler) Providerget() *TИнтернетprotocolprovider {
	return &ipprovider
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var ipprovider TИнтернетprotocolprovider

func (self *Ipethernetframehandler) Ethernetframereceivewhen(dataКөрсөткүч uintptr, өлчөм int) bool {
	ipconsole.MБасма(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetframereceivewhen(dataКөрсөткүч, uint32(өлчөм))

}

func (self *Ipethernetframehandler) Send(destinationipaddressТармакbyteorder uint64, dataКөрсөткүч uintptr, өлчөм uint32) {
	ipconsole.MБасма(([]byte)("ipefhandler:send\n"))
	var ethernetТүрүbe = Unsignedinteger16r(0x0800)
	self.TEthernetframehandler.Framesend(destinationipaddressТармакbyteorder, ethernetТүрүbe, dataКөрсөткүч, өлчөм)

}

var handler_2 [255]IИнтернетprotocolhandler

type TИнтернетprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetframehandler

func (self *TИнтернетprotocolprovider) Init(pefprovider TEthernetframeprovider, pefhandler IEthernetframehandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

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
func (self *TИнтернетprotocolprovider) Ethernetframereceivewhen(ethernetframepayload uintptr, өлчөм uint32) bool {
	if өлчөм < uint32(ipӨлчөм) {
		return false
	}

	var buffer_2 *TИнтернетprotocolv4messagebuffer = (*TИнтернетprotocolv4messagebuffer)(Pointer(ethernetframepayload))
	var интернетprotocolmessage TИнтернетprotocolv4message
	интернетprotocolmessage.Init(*buffer_2)

	var reply bool = false

	if интернетprotocolmessage.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var узундук uint32 = uint32(интернетprotocolmessage.бардыгыУзундук)
		if узундук > өлчөм {
			узундук = өлчөм
		}
		if handler_2[интернетprotocolmessage.protocol] != nil {
			reply = handler_2[интернетprotocolmessage.protocol].Интернетprotocolreceivewhen(интернетprotocolmessage.баштапкытекстipaddress, интернетprotocolmessage.destinationipaddress, ethernetframepayload+uintptr(4*интернетprotocolmessage.headerУзундук), uint32(узундук-uint32(4*интернетprotocolmessage.headerУзундук)))

		}
	}

	if reply {

		var temporary = интернетprotocolmessage.destinationipaddress
		интернетprotocolmessage.destinationipaddress = интернетprotocolmessage.баштапкытекстipaddress
		интернетprotocolmessage.баштапкытекстipaddress = temporary

		интернетprotocolmessage.timetolive = 0x40
		интернетprotocolmessage.checksum = 0

		интернетprotocolmessage.Setbuffer(buffer_2)
		интернетprotocolmessage.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*интернетprotocolmessage.headerУзундук))

		интернетprotocolmessage.Setbuffer(buffer_2)

	}

	ipconsole.MБасма(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Басма(интернетprotocolmessage.баштапкытекстipaddress)
	ipconsole.MБасма(([]byte)(":"))
	ipconsole.MUnsignedinteger32Басма(интернетprotocolmessage.destinationipaddress)
	ipconsole.MБасма(([]byte)(":"))
	ipconsole.MUnsignedinteger16Басма(uint16(интернетprotocolmessage.headerУзундук))
	ipconsole.MБасма(([]byte)(":"))
	ipconsole.MUnsignedinteger16Басма(uint16(интернетprotocolmessage.version))
	ipconsole.MБасма(([]byte)(":"))
	ipconsole.MUnsignedinteger16Басма(интернетprotocolmessage.бардыгыУзундук)
	ipconsole.MБасма(([]byte)(":"))
	ipconsole.MUnsignedinteger32Басма(uint32(efhandler.Getipaddress()))
	ipconsole.MБасма(([]byte)(":"))
	ipconsole.MБасма(([]byte)("\n"))

	return reply

}
func (self *TИнтернетprotocolprovider) Send(destinationipaddressТармакbyteorder uint32, protocol uint8, dataКөрсөткүч uintptr, өлчөм uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TИнтернетprotocolv4messagebuffer = (*TИнтернетprotocolv4messagebuffer)(Pointer(&buffer1_2))
	var message TИнтернетprotocolv4message = TИнтернетprotocolv4message{}
	message.version = 4
	message.headerУзундук = ipӨлчөм / 4
	message.tos = 0
	message.бардыгыУзундук = Unsignedinteger16r(uint16(өлчөм + uint32(ipӨлчөм)))

	message.ident = 0x0100
	message.желектериandoffset = 0x0040
	message.timetolive = 0x40
	message.protocol = protocol

	message.destinationipaddress = destinationipaddressТармакbyteorder

	message.баштапкытекстipaddress = uint32(efhandler.Getipaddress())

	message.checksum = 0

	message.Setbuffer(buffer_2)
	message.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipӨлчөм))
	message.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataКөрсөткүч))

	for i := 0; i < int(өлчөм); i++ {

		buffer1_2[i+int(ipӨлчөм)] = databuffer_2[i]
	}

	ipconsole.MБасмаxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(өлчөм)+int(ipӨлчөм); i++ {
		ipconsole.MHexadecimalБасма(buffer1_2[i])
	}
	ipconsole.MБасма(([]byte)(":"))
	ipconsole.MБасма(([]byte)("]\n"))

	var кийинкиhopipaddressТармакbyteorder uint32 = destinationipaddressТармакbyteorder
	if (destinationipaddressТармакbyteorder & self.Subnetmask) != (message.баштапкытекстipaddress & self.Subnetmask) {
		кийинкиhopipaddressТармакbyteorder = self.Gatewayip
	}

	var senddataКөрсөткүч = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Басма(кийинкиhopipaddressТармакbyteorder)

	var ethernetТүрүbe = Unsignedinteger16r(0x0800)
	efhandler.Framesend(self.arpprovider.Resolve(кийинкиhopipaddressТармакbyteorder), ethernetТүрүbe, senddataКөрсөткүч, uint32(ipӨлчөм)+uint32(өлчөм))

}
func (self *TИнтернетprotocolprovider) Checksum(pdata *[4096]uint16, узундукЧоңойтууБайт uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataБайт [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (узундукЧоңойтууБайт % 2) != 0 {
		temporary += uint32(uint16(dataБайт[узундукЧоңойтууБайт-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TИнтернетprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
