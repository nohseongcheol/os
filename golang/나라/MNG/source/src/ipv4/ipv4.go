/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "консол"
import . "итернэтframe"
import . "arp"

var ipКонсол TКонсол = TКонсол{}

type TИнтернетprotocolv4Мэдээbuffer struct {
	lenver		byte
	tos		byte
	нийтlength	[2]byte

	ident			[2]byte
	төлвүүдandoffset	[2]byte

	цагtolive	byte
	protocol	byte
	checksum	[2]byte

	эхipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipХэмжээ uint8 = (4 + 4 + 4 + 8)

type TИнтернетprotocolv4Мэдээ struct {
	headerlength	uint8
	version		uint8
	tos		uint8
	нийтlength	uint16

	ident			uint16
	төлвүүдandoffset	uint16

	цагtolive	uint8
	protocol	uint8
	checksum	uint16

	эхipaddress		uint32
	destinationipaddress	uint32
}

func (self *TИнтернетprotocolv4Мэдээ) Init(buffer_2 TИнтернетprotocolv4Мэдээbuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerlength = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.нийтlength = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.нийтlength))

	self.ident = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.ident))
	self.төлвүүдandoffset = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.төлвүүдandoffset))

	self.цагtolive = buffer_2.цагtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.checksum))

	self.эхipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.эхipaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TИнтернетprotocolv4Мэдээ) Setbuffer(buffer_2 *TИнтернетprotocolv4Мэдээbuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerlength & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.нийтlength = Unsignedinteger16toarray(self.нийтlength)

	buffer_2.ident = Unsignedinteger16toarray(self.ident)
	buffer_2.төлвүүдandoffset = Unsignedinteger16toarray(self.төлвүүдandoffset)

	buffer_2.цагtolive = self.цагtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toarray(self.checksum)

	buffer_2.эхipaddress = Unsignedinteger32toarray(self.эхipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)

}

type IИнтернетprotocolhandler interface {
	Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8)
	Интернетprotocolreceivewhen(эхipaddressСүлжээbyteorder uint32, destinationipaddressСүлжээbyteorder uint32, datapointer uintptr, хэмжээ uint32) bool
	Send(destinationipaddressСүлжээbyteorder uint32, pprotocol uint8, datapointer uintptr, хэмжээ uint32)
	Providerget() *TИнтернетprotocolprovider
}

type TИнтернетprotocolhandler struct {
}

var ipИтернэтframehandler IpИтернэтframehandler = IpИтернэтframehandler{}
var protocol uint8

func (self *TИнтернетprotocolhandler) Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TИнтернетprotocolhandler) Интернетprotocolreceivewhen(эхipaddressСүлжээbyteorder uint32, destinationipaddressСүлжээbyteorder uint32, datapointer uintptr, хэмжээ uint32) bool {
	ipКонсол.MХэвлэх(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TИнтернетprotocolhandler) Send(destinationipaddressСүлжээbyteorder uint32, pprotocol uint8, datapointer uintptr, хэмжээ uint32) {

	ipprovider.Send(destinationipaddressСүлжээbyteorder, pprotocol, datapointer, хэмжээ)
}
func (self *TИнтернетprotocolhandler) Providerget() *TИнтернетprotocolprovider {
	return &ipprovider
}

type IpИтернэтframehandler struct {
	TИтернэтframehandler
}

var ipprovider TИнтернетprotocolprovider

func (self *IpИтернэтframehandler) Итернэтframereceivewhen(datapointer uintptr, хэмжээ int) bool {
	ipКонсол.MХэвлэх(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Итернэтframereceivewhen(datapointer, uint32(хэмжээ))

}

func (self *IpИтернэтframehandler) Send(destinationipaddressСүлжээbyteorder uint64, datapointer uintptr, хэмжээ uint32) {
	ipКонсол.MХэвлэх(([]byte)("ipefhandler:send\n"))
	var итернэтТөрөлbe = Unsignedinteger16r(0x0800)
	self.TИтернэтframehandler.Framesend(destinationipaddressСүлжээbyteorder, итернэтТөрөлbe, datapointer, хэмжээ)

}

var handler_2 [255]IИнтернетprotocolhandler

type TИнтернетprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IИтернэтframehandler

func (self *TИнтернетprotocolprovider) Init(pefprovider TИтернэтframeprovider, pefhandler IИтернэтframehandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

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
func (self *TИнтернетprotocolprovider) Итернэтframereceivewhen(итернэтframepayload uintptr, хэмжээ uint32) bool {
	if хэмжээ < uint32(ipХэмжээ) {
		return false
	}

	var buffer_2 *TИнтернетprotocolv4Мэдээbuffer = (*TИнтернетprotocolv4Мэдээbuffer)(Pointer(итернэтframepayload))
	var интернетprotocolМэдээ TИнтернетprotocolv4Мэдээ
	интернетprotocolМэдээ.Init(*buffer_2)

	var reply bool = false

	if интернетprotocolМэдээ.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var length uint32 = uint32(интернетprotocolМэдээ.нийтlength)
		if length > хэмжээ {
			length = хэмжээ
		}
		if handler_2[интернетprotocolМэдээ.protocol] != nil {
			reply = handler_2[интернетprotocolМэдээ.protocol].Интернетprotocolreceivewhen(интернетprotocolМэдээ.эхipaddress, интернетprotocolМэдээ.destinationipaddress, итернэтframepayload+uintptr(4*интернетprotocolМэдээ.headerlength), uint32(length-uint32(4*интернетprotocolМэдээ.headerlength)))

		}
	}

	if reply {

		var temporary = интернетprotocolМэдээ.destinationipaddress
		интернетprotocolМэдээ.destinationipaddress = интернетprotocolМэдээ.эхipaddress
		интернетprotocolМэдээ.эхipaddress = temporary

		интернетprotocolМэдээ.цагtolive = 0x40
		интернетprotocolМэдээ.checksum = 0

		интернетprotocolМэдээ.Setbuffer(buffer_2)
		интернетprotocolМэдээ.checksum = self.Checksum((*([4096]uint16))(Pointer(итернэтframepayload)), uint32(4*интернетprotocolМэдээ.headerlength))

		интернетprotocolМэдээ.Setbuffer(buffer_2)

	}

	ipКонсол.MХэвлэх(([]byte)("ipmessage"))
	ipКонсол.MUnsignedinteger32Хэвлэх(интернетprotocolМэдээ.эхipaddress)
	ipКонсол.MХэвлэх(([]byte)(":"))
	ipКонсол.MUnsignedinteger32Хэвлэх(интернетprotocolМэдээ.destinationipaddress)
	ipКонсол.MХэвлэх(([]byte)(":"))
	ipКонсол.MUnsignedinteger16Хэвлэх(uint16(интернетprotocolМэдээ.headerlength))
	ipКонсол.MХэвлэх(([]byte)(":"))
	ipКонсол.MUnsignedinteger16Хэвлэх(uint16(интернетprotocolМэдээ.version))
	ipКонсол.MХэвлэх(([]byte)(":"))
	ipКонсол.MUnsignedinteger16Хэвлэх(интернетprotocolМэдээ.нийтlength)
	ipКонсол.MХэвлэх(([]byte)(":"))
	ipКонсол.MUnsignedinteger32Хэвлэх(uint32(efhandler.Getipaddress()))
	ipКонсол.MХэвлэх(([]byte)(":"))
	ipКонсол.MХэвлэх(([]byte)("\n"))

	return reply

}
func (self *TИнтернетprotocolprovider) Send(destinationipaddressСүлжээbyteorder uint32, protocol uint8, datapointer uintptr, хэмжээ uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TИнтернетprotocolv4Мэдээbuffer = (*TИнтернетprotocolv4Мэдээbuffer)(Pointer(&buffer1_2))
	var мэдээ TИнтернетprotocolv4Мэдээ = TИнтернетprotocolv4Мэдээ{}
	мэдээ.version = 4
	мэдээ.headerlength = ipХэмжээ / 4
	мэдээ.tos = 0
	мэдээ.нийтlength = Unsignedinteger16r(uint16(хэмжээ + uint32(ipХэмжээ)))

	мэдээ.ident = 0x0100
	мэдээ.төлвүүдandoffset = 0x0040
	мэдээ.цагtolive = 0x40
	мэдээ.protocol = protocol

	мэдээ.destinationipaddress = destinationipaddressСүлжээbyteorder

	мэдээ.эхipaddress = uint32(efhandler.Getipaddress())

	мэдээ.checksum = 0

	мэдээ.Setbuffer(buffer_2)
	мэдээ.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipХэмжээ))
	мэдээ.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(хэмжээ); i++ {

		buffer1_2[i+int(ipХэмжээ)] = databuffer_2[i]
	}

	ipКонсол.MХэвлэхxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(хэмжээ)+int(ipХэмжээ); i++ {
		ipКонсол.MHexadecimalХэвлэх(buffer1_2[i])
	}
	ipКонсол.MХэвлэх(([]byte)(":"))
	ipКонсол.MХэвлэх(([]byte)("]\n"))

	var дараахhopipaddressСүлжээbyteorder uint32 = destinationipaddressСүлжээbyteorder
	if (destinationipaddressСүлжээbyteorder & self.Subnetmask) != (мэдээ.эхipaddress & self.Subnetmask) {
		дараахhopipaddressСүлжээbyteorder = self.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipКонсол.MUnsignedinteger32Хэвлэх(дараахhopipaddressСүлжээbyteorder)

	var итернэтТөрөлbe = Unsignedinteger16r(0x0800)
	efhandler.Framesend(self.arpprovider.Resolve(дараахhopipaddressСүлжээbyteorder), итернэтТөрөлbe, senddatapointer, uint32(ipХэмжээ)+uint32(хэмжээ))

}
func (self *TИнтернетprotocolprovider) Checksum(pdata *[4096]uint16, lengthinБайт uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataБайт [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (lengthinБайт % 2) != 0 {
		temporary += uint32(uint16(dataБайт[lengthinБайт-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TИнтернетprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
