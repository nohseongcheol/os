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

type TInternetprotocolv4Sargytbuffer struct {
	lenver		byte
	tos		byte
	totallength	[2]byte

	ident		[2]byte
	flagsandoffset	[2]byte

	zamantolive	byte
	protocol	byte
	checksum	[2]byte

	çeşmeipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipUlulyk uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Sargyt struct {
	headerlength	uint8
	version		uint8
	tos		uint8
	totallength	uint16

	ident		uint16
	flagsandoffset	uint16

	zamantolive	uint8
	protocol	uint8
	checksum	uint16

	çeşmeipaddress		uint32
	destinationipaddress	uint32
}

func (self *TInternetprotocolv4Sargyt) Init(buffer_2 TInternetprotocolv4Sargytbuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerlength = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.totallength = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.totallength))

	self.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	self.flagsandoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.flagsandoffset))

	self.zamantolive = buffer_2.zamantolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	self.çeşmeipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.çeşmeipaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TInternetprotocolv4Sargyt) Setbuffer(buffer_2 *TInternetprotocolv4Sargytbuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerlength & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.totallength = Unsignedinteger16toarray(self.totallength)

	buffer_2.ident = Unsignedinteger16toarray(self.ident)
	buffer_2.flagsandoffset = Unsignedinteger16toarray(self.flagsandoffset)

	buffer_2.zamantolive = self.zamantolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

	buffer_2.çeşmeipaddress = Unsignedinteger32toarray(self.çeşmeipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(çeşmeipaddressŞebekebyteorder uint32, destinationipaddressŞebekebyteorder uint32, datapointer uintptr, ululyk uint32) bool
	Send(destinationipaddressŞebekebyteorder uint32, pprotocol uint8, datapointer uintptr, ululyk uint32)
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
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(çeşmeipaddressŞebekebyteorder uint32, destinationipaddressŞebekebyteorder uint32, datapointer uintptr, ululyk uint32) bool {
	ipconsole.MÇap(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Send(destinationipaddressŞebekebyteorder uint32, pprotocol uint8, datapointer uintptr, ululyk uint32) {

	ipprovider.Send(destinationipaddressŞebekebyteorder, pprotocol, datapointer, ululyk)
}
func (self *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var ipprovider TInternetprotocolprovider

func (self *Ipethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, ululyk int) bool {
	ipconsole.MÇap(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Ethernetframereceivewhen(datapointer, uint32(ululyk))

}

func (self *Ipethernetframehandler) Send(destinationipaddressŞebekebyteorder uint64, datapointer uintptr, ululyk uint32) {
	ipconsole.MÇap(([]byte)("ipefhandler:send\n"))
	var ethernetHilbe = Unsignedinteger16r(0x0800)
	self.TEthernetframehandler.Framesend(destinationipaddressŞebekebyteorder, ethernetHilbe, datapointer, ululyk)

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
func (self *TInternetprotocolprovider) Ethernetframereceivewhen(ethernetframepayload uintptr, ululyk uint32) bool {
	if ululyk < uint32(ipUlulyk) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Sargytbuffer = (*TInternetprotocolv4Sargytbuffer)(Pointer(ethernetframepayload))
	var internetprotocolSargyt TInternetprotocolv4Sargyt
	internetprotocolSargyt.Init(*buffer_2)

	var reply bool = false

	if internetprotocolSargyt.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var length uint32 = uint32(internetprotocolSargyt.totallength)
		if length > ululyk {
			length = ululyk
		}
		if handler_2[internetprotocolSargyt.protocol] != nil {
			reply = handler_2[internetprotocolSargyt.protocol].Internetprotocolreceivewhen(internetprotocolSargyt.çeşmeipaddress, internetprotocolSargyt.destinationipaddress, ethernetframepayload+uintptr(4*internetprotocolSargyt.headerlength), uint32(length-uint32(4*internetprotocolSargyt.headerlength)))

		}
	}

	if reply {

		var temporary = internetprotocolSargyt.destinationipaddress
		internetprotocolSargyt.destinationipaddress = internetprotocolSargyt.çeşmeipaddress
		internetprotocolSargyt.çeşmeipaddress = temporary

		internetprotocolSargyt.zamantolive = 0x40
		internetprotocolSargyt.checksum = 0

		internetprotocolSargyt.Setbuffer(buffer_2)
		internetprotocolSargyt.checksum = self.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*internetprotocolSargyt.headerlength))

		internetprotocolSargyt.Setbuffer(buffer_2)

	}

	ipconsole.MÇap(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Çap(internetprotocolSargyt.çeşmeipaddress)
	ipconsole.MÇap(([]byte)(":"))
	ipconsole.MUnsignedinteger32Çap(internetprotocolSargyt.destinationipaddress)
	ipconsole.MÇap(([]byte)(":"))
	ipconsole.MUnsignedinteger16Çap(uint16(internetprotocolSargyt.headerlength))
	ipconsole.MÇap(([]byte)(":"))
	ipconsole.MUnsignedinteger16Çap(uint16(internetprotocolSargyt.version))
	ipconsole.MÇap(([]byte)(":"))
	ipconsole.MUnsignedinteger16Çap(internetprotocolSargyt.totallength)
	ipconsole.MÇap(([]byte)(":"))
	ipconsole.MUnsignedinteger32Çap(uint32(efhandler.Getipaddress()))
	ipconsole.MÇap(([]byte)(":"))
	ipconsole.MÇap(([]byte)("\n"))

	return reply

}
func (self *TInternetprotocolprovider) Send(destinationipaddressŞebekebyteorder uint32, protocol uint8, datapointer uintptr, ululyk uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Sargytbuffer = (*TInternetprotocolv4Sargytbuffer)(Pointer(&buffer1_2))
	var sargyt TInternetprotocolv4Sargyt = TInternetprotocolv4Sargyt{}
	sargyt.version = 4
	sargyt.headerlength = ipUlulyk / 4
	sargyt.tos = 0
	sargyt.totallength = Unsignedinteger16r(uint16(ululyk + uint32(ipUlulyk)))

	sargyt.ident = 0x0100
	sargyt.flagsandoffset = 0x0040
	sargyt.zamantolive = 0x40
	sargyt.protocol = protocol

	sargyt.destinationipaddress = destinationipaddressŞebekebyteorder

	sargyt.çeşmeipaddress = uint32(efhandler.Getipaddress())

	sargyt.checksum = 0

	sargyt.Setbuffer(buffer_2)
	sargyt.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipUlulyk))
	sargyt.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(ululyk); i++ {

		buffer1_2[i+int(ipUlulyk)] = databuffer_2[i]
	}

	ipconsole.MÇapxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(ululyk)+int(ipUlulyk); i++ {
		ipconsole.MHexadecimalÇap(buffer1_2[i])
	}
	ipconsole.MÇap(([]byte)(":"))
	ipconsole.MÇap(([]byte)("]\n"))

	var nexthopipaddressŞebekebyteorder uint32 = destinationipaddressŞebekebyteorder
	if (destinationipaddressŞebekebyteorder & self.Subnetmask) != (sargyt.çeşmeipaddress & self.Subnetmask) {
		nexthopipaddressŞebekebyteorder = self.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Çap(nexthopipaddressŞebekebyteorder)

	var ethernetHilbe = Unsignedinteger16r(0x0800)
	efhandler.Framesend(self.arpprovider.Resolve(nexthopipaddressŞebekebyteorder), ethernetHilbe, senddatapointer, uint32(ipUlulyk)+uint32(ululyk))

}
func (self *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, lengthinBaýtlar uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBaýtlar [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthinBaýtlar % 2) != 0 {
		temporary += uint32(uint16(dataBaýtlar[lengthinBaýtlar-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
