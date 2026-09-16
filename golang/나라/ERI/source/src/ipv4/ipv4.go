/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetframe"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4messagebuffer struct {
	lenver		byte
	tos		byte
	totallength	[2]byte

	ident		[2]byte
	flagsandoffset	[2]byte

	timetolive	byte
	protocol	byte
	checksum	[2]byte

	sourceipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipsize uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4message struct {
	headerlength	uint8
	version		uint8
	tos		uint8
	totallength	uint16

	ident		uint16
	flagsandoffset	uint16

	timetolive	uint8
	protocol	uint8
	checksum	uint16

	sourceipaddress		uint32
	destinationipaddress	uint32
}

func (self *TInternetprotocolv4message) Init(buffer_2 TInternetprotocolv4messagebuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerlength = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.totallength = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.totallength))

	self.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	self.flagsandoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.flagsandoffset))

	self.timetolive = buffer_2.timetolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	self.sourceipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.sourceipaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TInternetprotocolv4message) Setbuffer(buffer_2 *TInternetprotocolv4messagebuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerlength & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.totallength = Unsignedinteger16toarray(self.totallength)

	buffer_2.ident = Unsignedinteger16toarray(self.ident)
	buffer_2.flagsandoffset = Unsignedinteger16toarray(self.flagsandoffset)

	buffer_2.timetolive = self.timetolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

	buffer_2.sourceipaddress = Unsignedinteger32toarray(self.sourceipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder uint32, destinationipaddressnetworkbyteorder uint32, datapointer uintptr, size uint32) bool
	Send(destinationipaddressnetworkbyteorder uint32, pprotocol uint8, datapointer uintptr, size uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetframehandler Ipethernetframehandler = Ipethernetframehandler{}
var protocol uint8

func (self *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(sourceipaddressnetworkbyteorder uint32, destinationipaddressnetworkbyteorder uint32, datapointer uintptr, size uint32) bool {
	ipconsole.MPrint(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Send(destinationipaddressnetworkbyteorder uint32, pprotocol uint8, datapointer uintptr, size uint32) {

	ipprovider.Send(destinationipaddressnetworkbyteorder, pprotocol, datapointer, size)
}
func (self *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var ipprovider TInternetprotocolprovider

func (self *Ipethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, size int) bool {
	ipconsole.MPrint(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetframereceivewhen(datapointer, uint32(size))

}

func (self *Ipethernetframehandler) Send(destinationipaddressnetworkbyteorder uint64, datapointer uintptr, size uint32) {
	ipconsole.MPrint(([]byte)("ipefhandler:send\n"))
	var ethernettypebe = Unsignedinteger16r(0x0800)
	self.TEthernetframehandler.Framesend(destinationipaddressnetworkbyteorder, ethernettypebe, datapointer, size)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetframehandler

func (self *TInternetprotocolprovider) Init(pefprovider TEthernetframeprovider, pefhandler IEthernetframehandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

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
func (self *TInternetprotocolprovider) Ethernetframereceivewhen(ethernetframepayload uintptr, size uint32) bool {
	if size < uint32(ipsize) {
		return false
	}

	var buffer_2 *TInternetprotocolv4messagebuffer = (*TInternetprotocolv4messagebuffer)(Pointer(ethernetframepayload))
	var internetprotocolmessage TInternetprotocolv4message
	internetprotocolmessage.Init(*buffer_2)

	var reply bool = false

	if internetprotocolmessage.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var length uint32 = uint32(internetprotocolmessage.totallength)
		if length > size {
			length = size
		}
		if handler_2[internetprotocolmessage.protocol] != nil {
			reply = handler_2[internetprotocolmessage.protocol].Internetprotocolreceivewhen(internetprotocolmessage.sourceipaddress, internetprotocolmessage.destinationipaddress, ethernetframepayload+uintptr(4*internetprotocolmessage.headerlength), uint32(length-uint32(4*internetprotocolmessage.headerlength)))

		}
	}

	if reply {

		var temporary = internetprotocolmessage.destinationipaddress
		internetprotocolmessage.destinationipaddress = internetprotocolmessage.sourceipaddress
		internetprotocolmessage.sourceipaddress = temporary

		internetprotocolmessage.timetolive = 0x40
		internetprotocolmessage.checksum = 0

		internetprotocolmessage.Setbuffer(buffer_2)
		internetprotocolmessage.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*internetprotocolmessage.headerlength))

		internetprotocolmessage.Setbuffer(buffer_2)

	}

	ipconsole.MPrint(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32print(internetprotocolmessage.sourceipaddress)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger32print(internetprotocolmessage.destinationipaddress)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(uint16(internetprotocolmessage.headerlength))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(uint16(internetprotocolmessage.version))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(internetprotocolmessage.totallength)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger32print(uint32(efhandler.Getipaddress()))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MPrint(([]byte)("\n"))

	return reply

}
func (self *TInternetprotocolprovider) Send(destinationipaddressnetworkbyteorder uint32, protocol uint8, datapointer uintptr, size uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4messagebuffer = (*TInternetprotocolv4messagebuffer)(Pointer(&buffer1_2))
	var message TInternetprotocolv4message = TInternetprotocolv4message{}
	message.version = 4
	message.headerlength = ipsize / 4
	message.tos = 0
	message.totallength = Unsignedinteger16r(uint16(size + uint32(ipsize)))

	message.ident = 0x0100
	message.flagsandoffset = 0x0040
	message.timetolive = 0x40
	message.protocol = protocol

	message.destinationipaddress = destinationipaddressnetworkbyteorder

	message.sourceipaddress = uint32(efhandler.Getipaddress())

	message.checksum = 0

	message.Setbuffer(buffer_2)
	message.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipsize))
	message.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(size); i++ {

		buffer1_2[i+int(ipsize)] = databuffer_2[i]
	}

	ipconsole.MPrintxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(size)+int(ipsize); i++ {
		ipconsole.MHexadecimalprint(buffer1_2[i])
	}
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MPrint(([]byte)("]\n"))

	var nexthopipaddressnetworkbyteorder uint32 = destinationipaddressnetworkbyteorder
	if (destinationipaddressnetworkbyteorder & self.Subnetmask) != (message.sourceipaddress & self.Subnetmask) {
		nexthopipaddressnetworkbyteorder = self.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32print(nexthopipaddressnetworkbyteorder)

	var ethernettypebe = Unsignedinteger16r(0x0800)
	efhandler.Framesend(self.arpprovider.Resolve(nexthopipaddressnetworkbyteorder), ethernettypebe, senddatapointer, uint32(ipsize)+uint32(size))

}
func (self *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, lengthinbytes uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var databytes [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthinbytes % 2) != 0 {
		temporary += uint32(uint16(databytes[lengthinbytes-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
