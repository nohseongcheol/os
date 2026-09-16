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

type TInternetprotocolv4boðanbuffer struct {
	lenver		byte
	tos		byte
	totalLongd	[2]byte

	ident		[2]byte
	flagsandoffset	[2]byte

	timetolive	byte
	protocol	byte
	checksum	[2]byte

	sourceipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipStødd uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4boðan struct {
	headerLongd	uint8
	version		uint8
	tos		uint8
	totalLongd	uint16

	ident		uint16
	flagsandoffset	uint16

	timetolive	uint8
	protocol	uint8
	checksum	uint16

	sourceipaddress		uint32
	destinationipaddress	uint32
}

func (self *TInternetprotocolv4boðan) Init(buffer_2 TInternetprotocolv4boðanbuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerLongd = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.totalLongd = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.totalLongd))

	self.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	self.flagsandoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.flagsandoffset))

	self.timetolive = buffer_2.timetolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	self.sourceipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.sourceipaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TInternetprotocolv4boðan) Setbuffer(buffer_2 *TInternetprotocolv4boðanbuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerLongd & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.totalLongd = Unsignedinteger16toarray(self.totalLongd)

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
	Internetprotocolreceivewhen(sourceipaddressNetbyteorder uint32, destinationipaddressNetbyteorder uint32, datapointer uintptr, stødd uint32) bool
	Send(destinationipaddressNetbyteorder uint32, pprotocol uint8, datapointer uintptr, stødd uint32)
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
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(sourceipaddressNetbyteorder uint32, destinationipaddressNetbyteorder uint32, datapointer uintptr, stødd uint32) bool {
	ipconsole.MPrint(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Send(destinationipaddressNetbyteorder uint32, pprotocol uint8, datapointer uintptr, stødd uint32) {

	ipprovider.Send(destinationipaddressNetbyteorder, pprotocol, datapointer, stødd)
}
func (self *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var ipprovider TInternetprotocolprovider

func (self *Ipethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, stødd int) bool {
	ipconsole.MPrint(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetframereceivewhen(datapointer, uint32(stødd))

}

func (self *Ipethernetframehandler) Send(destinationipaddressNetbyteorder uint64, datapointer uintptr, stødd uint32) {
	ipconsole.MPrint(([]byte)("ipefhandler:send\n"))
	var ethernettypebe = Unsignedinteger16r(0x0800)
	self.TEthernetframehandler.Framesend(destinationipaddressNetbyteorder, ethernettypebe, datapointer, stødd)

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
func (self *TInternetprotocolprovider) Ethernetframereceivewhen(ethernetframepayload uintptr, stødd uint32) bool {
	if stødd < uint32(ipStødd) {
		return false
	}

	var buffer_2 *TInternetprotocolv4boðanbuffer = (*TInternetprotocolv4boðanbuffer)(Pointer(ethernetframepayload))
	var internetprotocolboðan TInternetprotocolv4boðan
	internetprotocolboðan.Init(*buffer_2)

	var reply bool = false

	if internetprotocolboðan.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var longd uint32 = uint32(internetprotocolboðan.totalLongd)
		if longd > stødd {
			longd = stødd
		}
		if handler_2[internetprotocolboðan.protocol] != nil {
			reply = handler_2[internetprotocolboðan.protocol].Internetprotocolreceivewhen(internetprotocolboðan.sourceipaddress, internetprotocolboðan.destinationipaddress, ethernetframepayload+uintptr(4*internetprotocolboðan.headerLongd), uint32(longd-uint32(4*internetprotocolboðan.headerLongd)))

		}
	}

	if reply {

		var temporary = internetprotocolboðan.destinationipaddress
		internetprotocolboðan.destinationipaddress = internetprotocolboðan.sourceipaddress
		internetprotocolboðan.sourceipaddress = temporary

		internetprotocolboðan.timetolive = 0x40
		internetprotocolboðan.checksum = 0

		internetprotocolboðan.Setbuffer(buffer_2)
		internetprotocolboðan.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*internetprotocolboðan.headerLongd))

		internetprotocolboðan.Setbuffer(buffer_2)

	}

	ipconsole.MPrint(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32print(internetprotocolboðan.sourceipaddress)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger32print(internetprotocolboðan.destinationipaddress)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(uint16(internetprotocolboðan.headerLongd))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(uint16(internetprotocolboðan.version))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger16print(internetprotocolboðan.totalLongd)
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MUnsignedinteger32print(uint32(efhandler.Getipaddress()))
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MPrint(([]byte)("\n"))

	return reply

}
func (self *TInternetprotocolprovider) Send(destinationipaddressNetbyteorder uint32, protocol uint8, datapointer uintptr, stødd uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4boðanbuffer = (*TInternetprotocolv4boðanbuffer)(Pointer(&buffer1_2))
	var boðan TInternetprotocolv4boðan = TInternetprotocolv4boðan{}
	boðan.version = 4
	boðan.headerLongd = ipStødd / 4
	boðan.tos = 0
	boðan.totalLongd = Unsignedinteger16r(uint16(stødd + uint32(ipStødd)))

	boðan.ident = 0x0100
	boðan.flagsandoffset = 0x0040
	boðan.timetolive = 0x40
	boðan.protocol = protocol

	boðan.destinationipaddress = destinationipaddressNetbyteorder

	boðan.sourceipaddress = uint32(efhandler.Getipaddress())

	boðan.checksum = 0

	boðan.Setbuffer(buffer_2)
	boðan.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipStødd))
	boðan.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(stødd); i++ {

		buffer1_2[i+int(ipStødd)] = databuffer_2[i]
	}

	ipconsole.MPrintxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(stødd)+int(ipStødd); i++ {
		ipconsole.MHexadecimalprint(buffer1_2[i])
	}
	ipconsole.MPrint(([]byte)(":"))
	ipconsole.MPrint(([]byte)("]\n"))

	var næstahopipaddressNetbyteorder uint32 = destinationipaddressNetbyteorder
	if (destinationipaddressNetbyteorder & self.Subnetmask) != (boðan.sourceipaddress & self.Subnetmask) {
		næstahopipaddressNetbyteorder = self.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32print(næstahopipaddressNetbyteorder)

	var ethernettypebe = Unsignedinteger16r(0x0800)
	efhandler.Framesend(self.arpprovider.Resolve(næstahopipaddressNetbyteorder), ethernettypebe, senddatapointer, uint32(ipStødd)+uint32(stødd))

}
func (self *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, longdinbýt uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var databýt [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (longdinbýt % 2) != 0 {
		temporary += uint32(uint16(databýt[longdinbýt-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
