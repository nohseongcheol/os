/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "eternetframe"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4İsmarıcbuffer struct {
	lenver		byte
	tos		byte
	cəmilength	[2]byte

	ident			[2]byte
	bayraqlarandoffset	[2]byte

	zamantolive	byte
	protocol	byte
	checksum	[2]byte

	mənbəipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipBöyüklük uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4İsmarıc struct {
	headerlength	uint8
	version		uint8
	tos		uint8
	cəmilength	uint16

	ident			uint16
	bayraqlarandoffset	uint16

	zamantolive	uint8
	protocol	uint8
	checksum	uint16

	mənbəipaddress		uint32
	destinationipaddress	uint32
}

func (self *TInternetprotocolv4İsmarıc) Init(buffer_2 TInternetprotocolv4İsmarıcbuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerlength = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.cəmilength = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.cəmilength))

	self.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	self.bayraqlarandoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.bayraqlarandoffset))

	self.zamantolive = buffer_2.zamantolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	self.mənbəipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.mənbəipaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TInternetprotocolv4İsmarıc) Setbuffer(buffer_2 *TInternetprotocolv4İsmarıcbuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerlength & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.cəmilength = Unsignedinteger16toarray(self.cəmilength)

	buffer_2.ident = Unsignedinteger16toarray(self.ident)
	buffer_2.bayraqlarandoffset = Unsignedinteger16toarray(self.bayraqlarandoffset)

	buffer_2.zamantolive = self.zamantolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

	buffer_2.mənbəipaddress = Unsignedinteger32toarray(self.mənbəipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(mənbəipaddressŞəbəkəbyteorder uint32, destinationipaddressŞəbəkəbyteorder uint32, datapointer uintptr, böyüklük uint32) bool
	Send(destinationipaddressŞəbəkəbyteorder uint32, pprotocol uint8, datapointer uintptr, böyüklük uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipEternetframehandler IpEternetframehandler = IpEternetframehandler{}
var protocol uint8

func (self *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(mənbəipaddressŞəbəkəbyteorder uint32, destinationipaddressŞəbəkəbyteorder uint32, datapointer uintptr, böyüklük uint32) bool {
	ipconsole.MÇapEt(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Send(destinationipaddressŞəbəkəbyteorder uint32, pprotocol uint8, datapointer uintptr, böyüklük uint32) {

	ipprovider.Send(destinationipaddressŞəbəkəbyteorder, pprotocol, datapointer, böyüklük)
}
func (self *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpEternetframehandler struct {
	TEternetframehandler
}

var ipprovider TInternetprotocolprovider

func (self *IpEternetframehandler) Eternetframereceivewhen(datapointer uintptr, böyüklük int) bool {
	ipconsole.MÇapEt(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Eternetframereceivewhen(datapointer, uint32(böyüklük))

}

func (self *IpEternetframehandler) Send(destinationipaddressŞəbəkəbyteorder uint64, datapointer uintptr, böyüklük uint32) {
	ipconsole.MÇapEt(([]byte)("ipefhandler:send\n"))
	var eternetNövbe = Unsignedinteger16r(0x0800)
	self.TEternetframehandler.Framesend(destinationipaddressŞəbəkəbyteorder, eternetNövbe, datapointer, böyüklük)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEternetframehandler

func (self *TInternetprotocolprovider) Init(pefprovider TEternetframeprovider, pefhandler IEternetframehandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

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
func (self *TInternetprotocolprovider) Eternetframereceivewhen(eternetframepayload uintptr, böyüklük uint32) bool {
	if böyüklük < uint32(ipBöyüklük) {
		return false
	}

	var buffer_2 *TInternetprotocolv4İsmarıcbuffer = (*TInternetprotocolv4İsmarıcbuffer)(Pointer(eternetframepayload))
	var internetprotocolİsmarıc TInternetprotocolv4İsmarıc
	internetprotocolİsmarıc.Init(*buffer_2)

	var reply bool = false

	if internetprotocolİsmarıc.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var length uint32 = uint32(internetprotocolİsmarıc.cəmilength)
		if length > böyüklük {
			length = böyüklük
		}
		if handler_2[internetprotocolİsmarıc.protocol] != nil {
			reply = handler_2[internetprotocolİsmarıc.protocol].Internetprotocolreceivewhen(internetprotocolİsmarıc.mənbəipaddress, internetprotocolİsmarıc.destinationipaddress, eternetframepayload+uintptr(4*internetprotocolİsmarıc.headerlength), uint32(length-uint32(4*internetprotocolİsmarıc.headerlength)))

		}
	}

	if reply {

		var temporary = internetprotocolİsmarıc.destinationipaddress
		internetprotocolİsmarıc.destinationipaddress = internetprotocolİsmarıc.mənbəipaddress
		internetprotocolİsmarıc.mənbəipaddress = temporary

		internetprotocolİsmarıc.zamantolive = 0x40
		internetprotocolİsmarıc.checksum = 0

		internetprotocolİsmarıc.Setbuffer(buffer_2)
		internetprotocolİsmarıc.checksum = self.Checksum((*([4096]uint16))(Pointer(eternetframepayload)), uint32(4*internetprotocolİsmarıc.headerlength))

		internetprotocolİsmarıc.Setbuffer(buffer_2)

	}

	ipconsole.MÇapEt(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32ÇapEt(internetprotocolİsmarıc.mənbəipaddress)
	ipconsole.MÇapEt(([]byte)(":"))
	ipconsole.MUnsignedinteger32ÇapEt(internetprotocolİsmarıc.destinationipaddress)
	ipconsole.MÇapEt(([]byte)(":"))
	ipconsole.MUnsignedinteger16ÇapEt(uint16(internetprotocolİsmarıc.headerlength))
	ipconsole.MÇapEt(([]byte)(":"))
	ipconsole.MUnsignedinteger16ÇapEt(uint16(internetprotocolİsmarıc.version))
	ipconsole.MÇapEt(([]byte)(":"))
	ipconsole.MUnsignedinteger16ÇapEt(internetprotocolİsmarıc.cəmilength)
	ipconsole.MÇapEt(([]byte)(":"))
	ipconsole.MUnsignedinteger32ÇapEt(uint32(efhandler.Getipaddress()))
	ipconsole.MÇapEt(([]byte)(":"))
	ipconsole.MÇapEt(([]byte)("\n"))

	return reply

}
func (self *TInternetprotocolprovider) Send(destinationipaddressŞəbəkəbyteorder uint32, protocol uint8, datapointer uintptr, böyüklük uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4İsmarıcbuffer = (*TInternetprotocolv4İsmarıcbuffer)(Pointer(&buffer1_2))
	var ismarıc TInternetprotocolv4İsmarıc = TInternetprotocolv4İsmarıc{}
	ismarıc.version = 4
	ismarıc.headerlength = ipBöyüklük / 4
	ismarıc.tos = 0
	ismarıc.cəmilength = Unsignedinteger16r(uint16(böyüklük + uint32(ipBöyüklük)))

	ismarıc.ident = 0x0100
	ismarıc.bayraqlarandoffset = 0x0040
	ismarıc.zamantolive = 0x40
	ismarıc.protocol = protocol

	ismarıc.destinationipaddress = destinationipaddressŞəbəkəbyteorder

	ismarıc.mənbəipaddress = uint32(efhandler.Getipaddress())

	ismarıc.checksum = 0

	ismarıc.Setbuffer(buffer_2)
	ismarıc.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipBöyüklük))
	ismarıc.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(böyüklük); i++ {

		buffer1_2[i+int(ipBöyüklük)] = databuffer_2[i]
	}

	ipconsole.MÇapEtxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(böyüklük)+int(ipBöyüklük); i++ {
		ipconsole.MHexadecimalÇapEt(buffer1_2[i])
	}
	ipconsole.MÇapEt(([]byte)(":"))
	ipconsole.MÇapEt(([]byte)("]\n"))

	var sonrakıhopipaddressŞəbəkəbyteorder uint32 = destinationipaddressŞəbəkəbyteorder
	if (destinationipaddressŞəbəkəbyteorder & self.Subnetmask) != (ismarıc.mənbəipaddress & self.Subnetmask) {
		sonrakıhopipaddressŞəbəkəbyteorder = self.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32ÇapEt(sonrakıhopipaddressŞəbəkəbyteorder)

	var eternetNövbe = Unsignedinteger16r(0x0800)
	efhandler.Framesend(self.arpprovider.Resolve(sonrakıhopipaddressŞəbəkəbyteorder), eternetNövbe, senddatapointer, uint32(ipBöyüklük)+uint32(böyüklük))

}
func (self *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, lengthinBayt uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBayt [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthinBayt % 2) != 0 {
		temporary += uint32(uint16(dataBayt[lengthinBayt-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
